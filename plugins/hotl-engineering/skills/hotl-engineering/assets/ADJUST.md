# ADJUST.md — Replacement Points When Applying the Template

Adapt these pnpm + Next.js/TS + Azure Container Apps + AWS Bedrock examples to
the selected project. They are not a ready-to-deploy universal stack. Preserve
existing enforced gates; introduce new advisory checks proportionately.

## Common to all files
- [ ] Model IDs are not written in the templates. Set them as repository variables; a job whose variable is unset fails before the agent runs
      - `HOTL_MODEL_LIGHT`: ai-review (every PR), incident-triage, agent-implement
      - `HOTL_MODEL_DEEP`: the ai-review Tier 2 deep-dive review
      - `HOTL_JUDGE_MODEL`: the eval-gate judge (ideally a different model from the generator)
      - Use the model ID or inference profile ID of a model your organization has enabled on Bedrock. Check
        current model IDs in Anthropic's model tables for "Claude in Amazon Bedrock" and "Claude on Amazon
        Bedrock (legacy)". Do not pick a deprecated model (such as Sonnet 4.5). Record the date you set the
        variables and the date you checked the model tables
- [ ] AWS region (ap-northeast-1) → your organization's region
- [ ] Secret names (GITHUB_OIDC_ROLE / AZURE_CLIENT_ID* / TEAMS_WEBHOOK_URL, etc.) → align with the secrets that actually exist; if not yet created, attach the creation steps to the deliverable
- [ ] Pin third-party actions (`dorny/paths-filter` / `marocchino/sticky-pull-request-comment` /
      `gitleaks/gitleaks-action`, etc.) to a commit SHA rather than a tag
      (the template writes `@vN` for readability; since CI itself is Tier 2, pinning is the default when applying it)

## workflows/ci.yml
- [ ] pnpm → the actual package manager (npm/yarn/uv/poetry). For a Python stack, map L1-L5 to ruff / mypy / pip-audit / pytest
- [ ] `pnpm lint` / `pnpm test` / `pnpm build` → the script names that actually exist
- [ ] Coverage threshold → set vitest.config's `coverage.thresholds` (whole codebase) from a realistic
      value matched to existing coverage results, then raise it gradually. To require coverage only on
      changed files, choose a tool that actually measures the diff and confirm with a fixture that it
      accepts your coverage output format before adopting it
- [ ] Observe newly introduced noisy checks during calibration; do not weaken an existing enforced security job

## workflows/ai-review.yml
- [ ] Tier 2 paths-filter → fully rewrite to the risk paths identified in the assessment (most important)
- [ ] Keep CODEOWNERS and the paths definition in sync
- [ ] Copy `assets/scripts/check_review_verdicts.py` to `.github/scripts/check_review_verdicts.py` on the trusted base before enabling the workflow
- [ ] Keep `AI_REVIEW_ENFORCE` unset during observation; record incomplete evidence as incomplete, then enforce after calibration
- [ ] Require fresh light/deep verdicts with nonnegative counts and the reviewed head SHA; test missing, malformed, wrong-revision, failed, and skipped cases
- [ ] Restrict credentials and permitted tools for the review provider; PR content and model output remain untrusted even when JSON validates
- [ ] Limit the review jobs' `--allowedTools` to the PR comment tools plus a write to the one verdict file
      (`Edit(//<absolute path>)`). Keep `github_token: ${{ github.token }}`. Create the verdict directory fresh
      before the agent runs (no previous verdict survives)
- [ ] Keep `--setting-sources user` and `--strict-mcp-config` in every agent's `claude_args`. `--allowedTools` only
      adds pre-approvals and is not an upper bound, so without them the repository's (including the PR head's)
      Claude Code project settings (`settings.json` allow rules) and `.mcp.json` widen the agent's permissions

## workflows/agent-implement.yml
- [ ] Add an Issue template (acceptance criteria required) alongside it in .github/ISSUE_TEMPLATE/
- [ ] Confirm that the blocked operations (adding a dependency, dropping a column) match the project's actual situation
- [ ] Verify that the read-only authorization job can query the label actor's repository permission; the sample requires admin permission and fails closed on API errors
- [ ] Configure environment reviewers and preserve the approved issue text/revision before enabling autonomous implementation; an editable issue body is not a durable approval snapshot
- [ ] Replace the lint / typecheck / test commands in `--allowedTools` with scripts that actually exist in the project.
      Install dependencies in a step before the agent; never allow install as a direct agent command.
      Keep pushes fixed to the Issue's branch and do not add `gh api`, merge, or force push. Do not let the agent
      open the PR (prefix rules cannot constrain `gh pr create` arguments); a separate job opens it with a fixed
      repo, head, base, and Draft flag. Limit file-edit approvals to the working tree (`Edit(//<workspace>/**)`)
      and the two PR files; never add bare Edit / Write (they can rewrite Actions environment files outside the working tree)
- [ ] The step that opens the PR uses GITHUB_TOKEN by default, so pull_request workflows do not run automatically
      on that PR. To run CI or ai-review on it, create your own GitHub App (write access to Contents and Pull requests)
      and set `vars.HOTL_APP_ID` and `secrets.HOTL_APP_PRIVATE_KEY`
- [ ] Tests and git commit (hooks) run repository code while the job's credentials are in the environment.
      Operations inside those child processes are not limited by the pre-approvals. Where outsiders can file Issues,
      always combine environment reviewers with finalizing the Issue body at CP1

## workflows/eval-gate.yml (agent systems only)
- [ ] Trigger paths (prompts/, etc.) → the actual location of your prompts and retrieval logic
- [ ] Set the TARGET_ENDPOINT / EVAL_BUCKET vars
- [ ] Route PR evaluations to an isolated preview of the candidate; require each target response to include the deployed `revision` matching `EXPECTED_REVISION`. A shared staging PASS is not PR evidence
- [ ] Keep runner and thresholds on the trusted base for PR execution. Review changes to threshold policy separately; do not let a candidate lower its own gate
- [ ] Do not use the thresholds.json values as-is; set them from the measured results of the first full run
- [ ] When upgrading from 2.0.x, replace `judge_total_floor` / `judge_total_drop_allowed` in thresholds.json with
      `judge_axis_pass_rate_floor` / `judge_axis_pass_rate_drop_allowed` and `judge.pass_score`, and regenerate
      baseline.json with a calibration run that omits `--baseline`. With the old settings or baseline,
      run_evals.py stops with the reason (it never silently skips the comparison)
- [ ] Keep the anthropic SDK major pinned (the template uses `>=1.17,<2`). 1.x and later do not accept
      sampling parameters (temperature etc.), so judge variance is handled by the vote count. Before
      moving to 2.x (API version 2026-10-21), move the judge to a model Bedrock supports for 2026-10-21
      (Claude 4.7 or later) together with the IAM and endpoint changes, and first pass a network-free
      contract test (codex-plugins' scripts/tests/test_hotl_sdk_contract.py is an example) on the new version
- [ ] Before changing the judge model (`HOTL_JUDGE_MODEL`), compare eval-gate results and L3 human calibration
      between the old and new models
- [ ] Bootstrap the reviewed baseline explicitly with a calibration run that omits `--baseline`; store it before enabling the workflow. Routine missing/failed downloads must not disable comparison
- [ ] Keep report/artifact output in a fresh runner temporary directory. Publish only fresh results; setup failures must never publish a candidate-supplied PASS report
- [ ] Keep the trusted-runner approach for PRs (checkout from the base side). For a PR that changes
      the runner (run_evals.py), notify the team that "the new runner first runs with secrets in the
      nightly run after merge"

## evals/run_evals.py (agent systems only)
- [ ] Rewrite `call_target()` to match the API contract of the system under evaluation (it is isolated to this one function)
- [ ] Preserve deployed-revision evidence from the target; never synthesize it from the expected SHA supplied by the runner
- [ ] Keep target/judge execution errors separate from quality scores and fail incomplete suites; validate all configured judge votes and score ranges
- [ ] The L1 metrics (recall@5 / MRR) assume retrieval-based QA. For an agent without retrieval, trim
      to deterministic checks only (prohibited output, format, refusal)
- [ ] Redesign the golden-set file names and categories for your own domain (the template's
      golden.sample.jsonl is a structural example; follow the category design in references/eval-design.md)

## workflows/deploy.yml
- [ ] The full set of deploy-target commands (assuming Container Apps) → rewrite for the actual
      platform. Invariant: staging automatic → environment approval (CP3) → health watch → automatic rollback
- [ ] Confirm the existence of a health endpoint equivalent to /api/health (implement it first if missing)
- [ ] Attach the setup steps for GitHub Environments (production) Required reviewers to the deliverable
- [ ] Implement executable `.github/scripts/capture-production-state.sh <output-json>` and `.github/scripts/restore-production-state.sh <input-json>`; production preflight intentionally fails until both exist
- [ ] Capture revision mode, immutable deployed image/revisions, and actual traffic weights. Reject unsupported state before deploying. Restore routing as well as the target revision/image, verify health, and return nonzero on any failure
- [ ] Rehearse success and failed recovery against the selected platform, bound timeouts, and connect an authorized human-notification channel for both outcomes. File existence is only a preflight, not recovery proof

## workflows/incident-triage.yml
- [ ] Guarantee via IaC/procedure that the investigation role is Read-Only (Reader + log viewing only)
- [ ] Rewrite the --allowedTools command list to the read-only commands of the target platform. Spell
      prefixes down to the specific subcommand (a broad prefix such as `az monitor:*` also allows
      mutating subcommands). Do not add general-purpose commands such as `gh api` or any write command.
      Keep the `--tools` restriction and the `--disallowedTools` ban on file-editing tools
- [ ] Keep `github_token: ${{ github.token }}` on claude-code-action. Without it, the Claude GitHub App
      token, which can write, is handed to the agent. Keep the triage job's permissions to read plus id-token
- [ ] Keep Issue creation and notification in the separate report job (never run the agent in a job
      that can write)
- [ ] Write the alert payload to a file through env: and have the agent read it. Never expand it with
      `${{ }}` in the prompt or in run:
- [ ] Only the agent's final answer goes into the Issue, but the final answer can still quote logs.
      Check who can read Issues (is the repository private?) and add masking before posting if needed
- [ ] The alert → repository_dispatch relay (Function/Logic App) requires separate implementation

## templates/
- [ ] AGENTS.md.template → fully rewrite to the project's absolute norms, commands, and conventions (keep only the template's structure)
- [ ] CODEOWNERS.template → actual usernames, Tier 2 paths
- [ ] setup-branch-protection.sh → run in Phase 2 (do not run in Phase 1)
