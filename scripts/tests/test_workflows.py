"""Parse shipped YAML and exercise embedded authorization/preflight code offline."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / "plugins/hotl-engineering/skills/hotl-engineering/assets/workflows"


def workflow(name):
    return yaml.safe_load((WORKFLOWS / name).read_text())


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


if __name__ == "__main__":
    unittest.main()
