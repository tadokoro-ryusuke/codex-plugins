"""Parse shipped YAML and exercise embedded authorization/preflight code offline."""

from fnmatch import fnmatchcase
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / "plugins/hotl-engineering/skills/hotl-engineering/assets/workflows"


def workflow(name):
    return yaml.safe_load((WORKFLOWS / name).read_text())


# Expressions an outsider can inject into. Pass them through env: instead of expanding them in run: or prompt:
UNTRUSTED_EXPRESSION = re.compile(r"\$\{\{[^}]*(inputs\.|github\.event\.|client_payload)")
# Tools the incident-triage agent may get. Bash pre-approves only read-only command prefixes
TRIAGE_TOOLS = {"Read", "Grep", "Glob", "Bash"}
TRIAGE_READ_ONLY_COMMANDS = ("az monitor activity-log list", "az monitor log-analytics query",
                             "az monitor metrics list", "az containerapp revision list",
                             "az containerapp show", "az containerapp logs show",
                             "gh pr list", "gh run list")


# Jobs that run an agent, and the repository variable that supplies each model ID. Templates never contain model IDs
AGENT_MODEL_VARS = {("incident-triage.yml", "triage"): "HOTL_MODEL_LIGHT",
                    ("ai-review.yml", "review"): "HOTL_MODEL_LIGHT",
                    ("ai-review.yml", "deep-review"): "HOTL_MODEL_DEEP",
                    ("agent-implement.yml", "implement"): "HOTL_MODEL_LIGHT"}
# Review jobs and their verdict directories. The agent can only comment and write its verdict file
REVIEW_VERDICT_DIRS = {"review": "review-light", "deep-review": "review-deep"}


def agent_step(steps):
    index = next(i for i, step in enumerate(steps) if "claude-code-action" in step.get("uses", ""))
    return index, steps[index]


# The set of tools each agent can use (--tools). The upstream action accumulates repeated flags,
# so the checks combine every occurrence too
AGENT_TOOLS = {("incident-triage.yml", "triage"): {"Read", "Grep", "Glob", "Bash"},
               ("ai-review.yml", "review"): {"Read", "Grep", "Glob", "Bash", "Write"},
               ("ai-review.yml", "deep-review"): {"Read", "Grep", "Glob", "Bash", "Write"},
               ("agent-implement.yml", "implement"): {"Read", "Grep", "Glob", "Edit", "MultiEdit", "Write", "Bash"}}
FLAG_ALIASES = {"--allowed-tools": "--allowedTools", "--disallowed-tools": "--disallowedTools"}
# The upstream action accumulates repeated occurrences of these two flags; every other flag uses its last occurrence
ACCUMULATED_FLAGS = ("--allowedTools", "--disallowedTools")


def parse_claude_args(claude_args):
    """Read claude_args with shell rules, splitting accumulated flags from last-occurrence-wins flags."""
    # Like upstream, drop lines starting with # and let accumulated flags take every value that follows
    text = "\n".join(line for line in claude_args.splitlines() if not line.strip().startswith("#"))
    tokens = shlex.split(text)
    accumulated = {flag: [] for flag in ACCUMULATED_FLAGS}
    last = {}
    i = 0
    while i < len(tokens):
        name = FLAG_ALIASES.get(tokens[i], tokens[i])
        values = []
        while i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
            values.append(tokens[i + 1])
            i += 1
            if name not in accumulated:
                break
        i += 1
        if name in accumulated:
            for value in values:
                accumulated[name] += [tool.strip() for tool in value.split(",") if tool.strip()]
        else:
            last[name] = values[0] if values else None
    return accumulated, last


def tool_list(claude_args, flag):
    accumulated, last = parse_claude_args(claude_args)
    if flag in accumulated:
        return accumulated[flag]
    return [tool.strip() for tool in (last.get(flag) or "").split(",") if tool.strip()]


def rule_matches(rule, tool):
    """Approximate whether a Claude Code permission rule (Tool or Tool(pattern)) matches a tool call."""
    rule_name, _, rule_pattern = rule.partition("(")
    tool_name, _, tool_argument = tool.partition("(")
    if rule_name != tool_name:
        return False
    if not rule_pattern:
        return True
    pattern = rule_pattern[:-1]
    if pattern.endswith(":*"):
        pattern = pattern[:-2] + " *"
    argument = tool_argument[:-1] if tool_argument else ""
    if argument.endswith(":*"):
        argument = argument[:-2] + " x"
    return fnmatchcase(argument, pattern) or fnmatchcase(argument + " x", pattern)


def is_read_only_triage_tool(tool):
    """Reject bare Bash, broad wildcards, and prefixes that include mutating subcommands."""
    if tool in TRIAGE_TOOLS - {"Bash"}:
        return True
    return tool in {f"Bash({command}:*)" for command in TRIAGE_READ_ONLY_COMMANDS}


def pinned_sdk(path):
    match = re.search(r'pip install "(anthropic\[bedrock\][^"]*)"', path.read_text())
    return match.group(1) if match else None


def run_step(step, env, cwd, path_prefix=None):
    """Run a run: block under the GitHub Actions default shell (bash -e -o pipefail)."""
    full_env = {**os.environ, **env}
    if path_prefix:
        full_env["PATH"] = f"{path_prefix}{os.pathsep}{full_env['PATH']}"
    return subprocess.run(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", step["run"]],
                          env=full_env, cwd=cwd, capture_output=True, text=True, timeout=10)


class WorkflowTests(unittest.TestCase):
    def test_all_workflow_files_parse(self):
        for path in [*WORKFLOWS.glob("*.yml"), ROOT / ".github/workflows/validate.yml"]:
            with self.subTest(path=path):
                data = yaml.safe_load(path.read_text())
                self.assertIsInstance(data["jobs"], dict)

    def test_issue_permission_is_verified_before_privileged_job(self):
        data = workflow("agent-implement.yml")
        self.assertEqual(data["permissions"], {"contents": "read"})
        self.assertIn("authorize", data["jobs"])
        self.assertEqual(data["jobs"]["implement"]["needs"], "authorize")
        auth = data["jobs"]["authorize"]
        script = next(step["with"]["script"] for step in auth["steps"] if "with" in step and "script" in step["with"])
        for permission, allowed in (("admin", True), ("write", False), ("read", False), (None, False)):
            with self.subTest(permission=permission):
                harness = """
const outputs = {}; let error;
const context = {repo: {owner: 'fixture', repo: 'repo'}, payload: {sender: {login: 'fixture-user'}}};
const github = {rest: {repos: {getCollaboratorPermissionLevel: async (args) => {
  if (args.username !== 'fixture-user') throw new Error('wrong actor');
  return {data: {permission: PERMISSION}};
}}}};
const core = {setOutput: (key, value) => outputs[key] = value, setFailed: (value) => error = value};
await (async () => { SCRIPT })();
process.stdout.write(JSON.stringify({allowed: outputs.authorized === 'true' && !error}));
""".replace("PERMISSION", json.dumps(permission)).replace("SCRIPT", script)
                result = subprocess.run([shutil.which("node"), "--input-type=module", "-e", harness],
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["allowed"], allowed)

    def test_production_cannot_start_without_recovery_adapters(self):
        steps = workflow("deploy.yml")["jobs"]["production"]["steps"]
        preflight = next(step for step in steps if step.get("id") == "recovery-preflight")
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(["bash", "-e", "-c", preflight["run"]], cwd=directory,
                                    capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)

    def test_review_gate_wires_trusted_script_and_classification(self):
        gate = workflow("ai-review.yml")["jobs"]["ai-review-gate"]
        self.assertIn("classify", gate["needs"])
        command = next(step for step in gate["steps"] if step.get("name") == "Enforce gate")
        self.assertIn("EXPECTED_SHA", command["env"])
        self.assertIn(".trusted/.github/scripts/check_review_verdicts.py", command["run"])

    def test_eval_artifacts_are_fresh_and_outside_candidate_checkout(self):
        steps = workflow("eval-gate.yml")["jobs"]["eval"]["steps"]
        prepare = next(step for step in steps if step.get("id") == "artifacts")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            checkout.mkdir()
            runtime = root / "runtime"
            runtime.mkdir()
            outputs = root / "outputs"
            env = {**os.environ, "RUNNER_TEMP": str(runtime), "GITHUB_OUTPUT": str(outputs)}
            paths = []
            for _ in range(2):
                outputs.write_text("")
                result = subprocess.run(["bash", "-e", "-c", prepare["run"]], env=env,
                                        cwd=checkout, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                output = Path(dict(line.split("=", 1) for line in outputs.read_text().splitlines())["directory"])
                self.assertTrue(output.is_relative_to(runtime))
                self.assertEqual(list(output.iterdir()), [])
                paths.append(output)
            self.assertNotEqual(*paths)

    def test_artifact_upload_does_not_run_with_missing_directory(self):
        steps = workflow("eval-gate.yml")["jobs"]["eval"]["steps"]
        upload = next(step for step in steps if step.get("name") == "Upload artifact")
        expression = upload["if"].replace("always()", "True").replace("&&", " and ")
        expression = expression.replace("steps.artifacts.outcome", "outcome")
        expression = expression.replace("steps.artifacts.outputs.directory", "directory")
        for outcome, directory, allowed in (("failure", "", False), ("success", "", False),
                                            ("success", "/tmp/fixture", True)):
            with self.subTest(outcome=outcome, directory=directory):
                self.assertEqual(eval(expression, {"__builtins__": {}},
                                      {"outcome": outcome, "directory": directory}), allowed)

    def test_incident_triage_agent_cannot_write_to_github_or_files(self):
        data = workflow("incident-triage.yml")
        self.assertNotIn("write", (data.get("permissions") or {}).values())
        triage = data["jobs"]["triage"]
        self.assertEqual({key for key, value in triage["permissions"].items() if value == "write"},
                         {"id-token"})
        agent = next(step for step in triage["steps"] if "claude-code-action" in step.get("uses", ""))
        # Without this, the token is exchanged for the write-capable Claude GitHub App token
        self.assertEqual(agent["with"].get("github_token"), "${{ github.token }}")
        claude_args = agent["with"]["claude_args"]
        # --allowedTools only pre-approves; --tools restricts the set of available tools itself
        tools = set(tool_list(claude_args, "--tools"))
        self.assertTrue(tools)
        self.assertLessEqual(tools, TRIAGE_TOOLS)
        allowed = tool_list(claude_args, "--allowedTools")
        self.assertTrue(allowed)
        for tool in allowed:
            with self.subTest(tool=tool):
                self.assertTrue(is_read_only_triage_tool(tool))
        disallowed = set(tool_list(claude_args, "--disallowedTools"))
        self.assertLessEqual({"Edit", "MultiEdit", "Write", "NotebookEdit"}, disallowed)

    def test_read_only_tool_check_rejects_broad_or_mutating_grants(self):
        for tool in ("Bash", "Bash(*)", "Bash(az monitor:*)", "Bash(az webapp log:*)", "Bash(gh api:*)",
                     "Bash(gh issue create:*)", "Bash(git push:*)", "Edit", "Write", "WebFetch"):
            with self.subTest(tool=tool):
                self.assertFalse(is_read_only_triage_tool(tool))

    def test_incident_reporting_runs_outside_the_agent_job(self):
        jobs = workflow("incident-triage.yml")["jobs"]
        report = jobs["report"]
        self.assertEqual(report["needs"], "triage")
        self.assertEqual(report["permissions"], {"issues": "write"})
        self.assertFalse(any("claude-code-action" in step.get("uses", "") for step in report["steps"]))
        self.assertFalse(any("gh issue" in step.get("run", "") for step in jobs["triage"]["steps"]))

    def test_issue_body_contains_only_the_final_answer(self):
        # The execution file is the full SDK message array, including tool output (logs, file contents)
        steps = workflow("incident-triage.yml")["jobs"]["triage"]["steps"]
        extract = next(step for step in steps if step.get("id") == "summary")
        messages = [
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash"}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "SECRET_FIXTURE=abc"}]}},
            {"type": "result", "subtype": "success", "result": "Incident summary: fixture"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            execution = root / "execution.json"
            execution.write_text(json.dumps(messages))
            outputs = root / "outputs"
            outputs.write_text("")
            result = run_step(extract, {"EXECUTION_FILE": str(execution), "RUNNER_TEMP": str(root),
                                        "GITHUB_OUTPUT": str(outputs)}, root)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = Path(dict(line.split("=", 1) for line in outputs.read_text().splitlines())["path"])
            body = summary.read_text()
            self.assertIn("Incident summary: fixture", body)
            self.assertNotIn("SECRET_FIXTURE", body)
        upload = next(step for step in steps if "upload-artifact" in step.get("uses", ""))
        self.assertIn("steps.summary.outputs.path", upload["with"]["path"])

    def test_report_creates_an_issue_even_without_a_usable_result(self):
        steps = workflow("incident-triage.yml")["jobs"]["report"]["steps"]
        create = next(step for step in steps if step.get("id") == "issue")
        mock_gh = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$GH_CALLS"
case "$*" in *--body-file*) [ "${FAIL_BODY_FILE:-0}" = 1 ] && exit 1;; esac
echo "https://github.com/fixture/repo/issues/1"
"""
        # jq -r writes a newline even for an empty answer, so whitespace-only summaries must fall back too
        for case, summary_text, fail_body_file in (("missing", None, "0"), ("present", "Incident summary: fixture", "0"),
                                                   ("posting-fails", "Incident summary: fixture", "1"),
                                                   ("empty", "", "0"), ("newline-only", "\n", "0"),
                                                   ("whitespace-only", "  \n\t\n", "0")):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bin_dir = root / "bin"
                bin_dir.mkdir()
                (bin_dir / "gh").write_text(mock_gh)
                (bin_dir / "gh").chmod(0o755)
                result_dir = root / "triage"
                if summary_text is not None:
                    result_dir.mkdir()
                    (result_dir / "summary.md").write_text(summary_text)
                calls = root / "calls"
                calls.write_text("")
                outputs = root / "outputs"
                outputs.write_text("")
                env = {"GH_CALLS": str(calls), "FAIL_BODY_FILE": fail_body_file, "ALERT_NAME": "fixture",
                       "RESULT_DIR": str(result_dir), "RUN_URL": "https://example.invalid/run",
                       "GITHUB_OUTPUT": str(outputs)}
                result = run_step(create, env, root, path_prefix=str(bin_dir))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("url=https://github.com/fixture/repo/issues/1", outputs.read_text())
                last_call = calls.read_text().splitlines()[-1]
                if case == "present":
                    self.assertIn("--body-file", last_call)
                else:
                    self.assertIn("https://example.invalid/run", last_call)

    def test_untrusted_input_is_not_expanded_into_prompts_or_shell(self):
        for name in ("incident-triage.yml", "eval-gate.yml"):
            for job_name, job in workflow(name)["jobs"].items():
                for step in job["steps"]:
                    sources = [step.get("run", "")]
                    if "claude-code-action" in step.get("uses", ""):
                        sources.append(step["with"].get("prompt", ""))
                    for source in sources:
                        with self.subTest(workflow=name, job=job_name, step=step.get("name") or step.get("uses")):
                            self.assertIsNone(UNTRUSTED_EXPRESSION.search(source))

    def test_eval_gate_pins_the_sdk_version_tested_in_ci(self):
        # anthropic SDK 2.x sends API version 2026-10-21; 1.x rejects sampling parameters.
        # The template and the CI contract test (test_hotl_sdk_contract.py) must use the same version
        spec = pinned_sdk(WORKFLOWS / "eval-gate.yml")
        self.assertIsNotNone(spec)
        self.assertIn("<2", spec)
        ci = ROOT / ".github/workflows/validate.yml"
        self.assertEqual(pinned_sdk(ci), spec)
        self.assertEqual(yaml.safe_load(ci.read_text())["jobs"]["validate"]["env"].get("HOTL_REQUIRE_SDK"), "1")

    def test_agent_models_come_from_required_repository_variables(self):
        # Keep model IDs that will be retired out of the templates. If unset, fail before the agent runs
        for path in WORKFLOWS.glob("*.yml"):
            with self.subTest(workflow=path.name):
                self.assertNotIn("anthropic.claude-", path.read_text())
        for (name, job_name), variable in AGENT_MODEL_VARS.items():
            with self.subTest(workflow=name, job=job_name):
                steps = workflow(name)["jobs"][job_name]["steps"]
                index, agent = agent_step(steps)
                self.assertIn(f"--model ${{{{ vars.{variable} }}}}", agent["with"]["claude_args"])
                guard = next(step for step in steps[:index] if step.get("id") == "model")
                self.assertEqual(guard["env"]["MODEL"], f"${{{{ vars.{variable} }}}}")
                with tempfile.TemporaryDirectory() as directory:
                    self.assertNotEqual(run_step(guard, {"MODEL": ""}, directory).returncode, 0)
                    self.assertEqual(run_step(guard, {"MODEL": "fixture-model"}, directory).returncode, 0)
        gate = workflow("eval-gate.yml")["jobs"]["eval"]
        self.assertEqual(gate["env"]["JUDGE_MODEL"], "${{ vars.HOTL_JUDGE_MODEL }}")

    def test_agents_get_only_their_tools_and_ignore_repository_settings(self):
        # --allowedTools only adds pre-approvals and is not an upper bound. Read only user settings so the
        # repository's (including the PR head's) Claude Code project settings and .mcp.json cannot widen permissions
        for (name, job_name), expected in AGENT_TOOLS.items():
            with self.subTest(workflow=name, job=job_name):
                _, agent = agent_step(workflow(name)["jobs"][job_name]["steps"])
                claude_args = agent["with"]["claude_args"]
                _, last = parse_claude_args(claude_args)
                self.assertEqual(last.get("--setting-sources"), "user")
                self.assertIn("--strict-mcp-config", last)
                self.assertEqual(set(tool_list(claude_args, "--tools")), expected)
                # Neither the needed tools nor the pre-approved tools hit a deny rule
                denied = tool_list(claude_args, "--disallowedTools")
                for tool in sorted(expected) + tool_list(claude_args, "--allowedTools"):
                    with self.subTest(tool=tool):
                        self.assertFalse(any(rule_matches(rule, tool) for rule in denied))

    def test_review_agents_can_only_comment_and_write_their_verdict(self):
        jobs = workflow("ai-review.yml")["jobs"]
        for job_name, folder in REVIEW_VERDICT_DIRS.items():
            with self.subTest(job=job_name):
                steps = jobs[job_name]["steps"]
                index, agent = agent_step(steps)
                self.assertEqual(agent["with"].get("github_token"), "${{ github.token }}")
                claude_args = agent["with"]["claude_args"]
                self.assertLessEqual(set(tool_list(claude_args, "--tools")), {"Read", "Grep", "Glob", "Bash", "Write"})
                verdict = f"${{{{ runner.temp }}}}/{folder}/verdict.json"
                # The same comment tools as the upstream PR review example, plus a write to the one verdict file
                self.assertEqual(set(tool_list(claude_args, "--allowedTools")), {
                    "Read", "Grep", "Glob", "mcp__github_inline_comment__create_inline_comment",
                    "Bash(gh pr comment:*)", "Bash(gh pr diff:*)", "Bash(gh pr view:*)", f"Edit(/{verdict})"})
                self.assertIn(verdict, agent["with"]["prompt"])
                prepare = next(step for step in steps[:index] if step.get("id") == "verdict-dir")
                with tempfile.TemporaryDirectory() as directory:
                    stale = Path(directory) / folder / "verdict.json"
                    stale.parent.mkdir()
                    stale.write_text('{"critical": 0, "high": 0}')
                    result = run_step(prepare, {"RUNNER_TEMP": directory}, directory)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(stale.parent.is_dir())
                    self.assertFalse(stale.exists())

    def test_implementation_agent_tools_are_explicit_and_scoped(self):
        steps = workflow("agent-implement.yml")["jobs"]["implement"]["steps"]
        index, agent = agent_step(steps)
        claude_args = agent["with"]["claude_args"]
        file_tools = {"Read", "Grep", "Glob", "Edit", "MultiEdit", "Write"}
        self.assertLessEqual(set(tool_list(claude_args, "--tools")), file_tools | {"Bash"})
        allowed = tool_list(claude_args, "--allowedTools")
        issue = "${{ github.event.issue.number }}"
        branch = f"agent/issue-{issue}"
        # Only what the plan comment, branch, verification, commit, and push need. Pushes are fixed to the Issue's branch.
        # Opening the PR is not pre-approved (a later step opens it with fixed arguments)
        self.assertEqual({tool for tool in allowed if tool.startswith("Bash")}, {
            f"Bash(gh issue comment {issue}:*)", f"Bash(git switch -c {branch})", "Bash(git status)",
            "Bash(git diff:*)", "Bash(git add:*)", "Bash(git commit:*)", f"Bash(git push -u origin {branch})",
            "Bash(pnpm lint)", "Bash(pnpm typecheck)", "Bash(pnpm test:*)"})
        pr_dir = "${{ runner.temp }}/agent-pr"
        # Bare Edit / Write would also approve writes outside the working tree (such as Actions environment files)
        self.assertEqual({tool for tool in allowed if not tool.startswith("Bash")},
                         {"Read", "Grep", "Glob", "Edit(/${{ github.workspace }}/**)",
                          f"Edit(/{pr_dir}/title.txt)", f"Edit(/{pr_dir}/body.md)"})
        self.assertIn(f"{pr_dir}/title.txt", agent["with"]["prompt"])
        # Dependencies are installed from the lockfile before the agent runs (the agent may not install)
        self.assertTrue(any("pnpm install --frozen-lockfile" in step.get("run", "") for step in steps[:index]))

    def test_pull_request_is_opened_by_a_separate_trusted_job(self):
        # Opened on a fresh runner that runs neither the agent nor repository code (unaffected by the previous job's environment files)
        jobs = workflow("agent-implement.yml")["jobs"]
        opener_job = jobs["open-pr"]
        self.assertEqual(opener_job["needs"], "implement")
        self.assertEqual(opener_job["permissions"], {"contents": "read", "pull-requests": "write"})
        for step in opener_job["steps"]:
            with self.subTest(step=step.get("name") or step.get("uses")):
                self.assertNotIn("claude-code-action", step.get("uses", ""))
                self.assertNotIn("actions/checkout", step.get("uses", ""))
                self.assertNotIn("pnpm", step.get("run", ""))
        self.assertEqual(jobs["implement"]["outputs"]["before"], "${{ steps.before.outputs.sha }}")
        self.assertEqual(next(s for s in opener_job["steps"] if s.get("id") == "open-pr")["env"]["BEFORE"],
                         "${{ needs.implement.outputs.before }}")

    def test_branch_head_is_recorded_before_the_agent(self):
        steps = workflow("agent-implement.yml")["jobs"]["implement"]["steps"]
        index, _ = agent_step(steps)
        before = next(step for step in steps[:index] if step.get("id") == "before")
        mock = """#!/usr/bin/env bash
case "$MODE" in
  found) echo abc123 ;;
  missing) echo 'gh: Not Found (HTTP 404)' >&2; exit 1 ;;
  error) echo 'gh: Bad credentials (HTTP 401)' >&2; exit 1 ;;
esac
"""
        for mode, code, expected in (("found", 0, "sha=abc123"), ("missing", 0, "sha=none"), ("error", 1, None)):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bin_dir = root / "bin"
                bin_dir.mkdir()
                (bin_dir / "gh").write_text(mock)
                (bin_dir / "gh").chmod(0o755)
                outputs = root / "outputs"
                outputs.write_text("")
                result = run_step(before, {"MODE": mode, "RUNNER_TEMP": str(root), "GITHUB_OUTPUT": str(outputs),
                                           "GH_REPO": "fixture/repo", "BRANCH": "agent/issue-7"}, root,
                                  path_prefix=str(bin_dir))
                if code == 0:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(expected, outputs.read_text())
                else:
                    self.assertNotEqual(result.returncode, 0)

    def test_trusted_step_opens_the_draft_pull_request(self):
        steps = workflow("agent-implement.yml")["jobs"]["open-pr"]["steps"]
        opener = next(step for step in steps if step.get("id") == "open-pr")
        self.assertEqual(opener["env"]["BRANCH"], "agent/issue-${{ github.event.issue.number }}")
        self.assertEqual(opener["env"]["BASE"], "${{ github.event.repository.default_branch }}")
        mock = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$CALLS"
case "$*" in
  "api "*)
    case "$HEAD_MODE" in
      missing) echo 'gh: Not Found (HTTP 404)' >&2; exit 1 ;;
      error) echo 'gh: Bad credentials (HTTP 401)' >&2; exit 1 ;;
      *) echo "$HEAD_MODE" ;;
    esac ;;
  "pr list"*) [ "$EXISTING" = 1 ] && printf '%s\\n' 5 ;;
esac
exit 0
"""
        cases = (
            ("not-pushed", "missing", "none", "0", "body", 0, False),
            ("auth-error", "error", "none", "0", "body", 1, False),
            ("unchanged", "abc", "abc", "0", "body", 0, False),
            ("existing", "def", "abc", "1", "body", 0, False),
            ("created", "def", "none", "0", "Acceptance criteria mapping", 0, True),
            ("empty-body", "def", "abc", "0", "  \n", 0, True),
        )
        for case, head_mode, before, existing, body_text, code, creates in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bin_dir = root / "bin"
                bin_dir.mkdir()
                (bin_dir / "gh").write_text(mock)
                (bin_dir / "gh").chmod(0o755)
                pr_dir = root / "agent-pr"
                pr_dir.mkdir()
                (pr_dir / "title.txt").write_text("feat: fixture\n")
                (pr_dir / "body.md").write_text(body_text)
                calls = root / "calls"
                calls.write_text("")
                env = {"CALLS": str(calls), "HEAD_MODE": head_mode, "EXISTING": existing, "BEFORE": before,
                       "GH_REPO": "fixture/repo", "BRANCH": "agent/issue-7", "BASE": "main", "ISSUE": "7",
                       "PR_DIR": str(pr_dir), "RUNNER_TEMP": str(root), "RUN_URL": "https://example.invalid/run"}
                result = run_step(opener, env, root, path_prefix=str(bin_dir))
                if code == 0:
                    self.assertEqual(result.returncode, 0, result.stderr)
                else:
                    self.assertNotEqual(result.returncode, 0)
                create = [line for line in calls.read_text().splitlines() if line.startswith("pr create")]
                if not creates:
                    self.assertEqual(create, [])
                    continue
                self.assertEqual(len(create), 1)
                for expected in ("--repo fixture/repo", "--draft", "--head agent/issue-7", "--base main",
                                 "--title feat: fixture"):
                    self.assertIn(expected, create[0])
                body = (pr_dir / "body.md").read_text()
                self.assertIn("Closes #7", body)
                if case == "empty-body":
                    self.assertIn("https://example.invalid/run", body)

    def test_ci_does_not_claim_changed_file_coverage(self):
        # jest-coverage-report-action's threshold is whole-codebase, and its input format does not match vitest
        for job_name, job in workflow("ci.yml")["jobs"].items():
            for step in job.get("steps", []):
                with self.subTest(job=job_name, step=step.get("name") or step.get("uses")):
                    self.assertNotIn("jest-coverage-report-action", step.get("uses", ""))
                    self.assertNotIn("changed files", (step.get("name") or "").lower())


if __name__ == "__main__":
    unittest.main()
