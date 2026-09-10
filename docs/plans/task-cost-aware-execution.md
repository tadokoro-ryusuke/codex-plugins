# Cost-Aware Planned Execution

## Scope and status

- Status: implementation completed and installed; reviewed for main delivery on
  2026-09-10. Original base `de515af`, branch `codex/cost-aware-execution`.
- Apply the user's approved operating policy: recommend Astra medium for the
  parent, use Sol medium for ordinary implementation, retain Astra high for
  independent review of substantial work, and select Astra for difficult work.
- Keep small self-contained changes with one agent; preserve explicit task and
  custom-profile selections, capability checks, ownership, and evidence gates.
- Bump dev-core to 5.1.2. Complete source checks and review before installing.
- Do not commit or push this new change without a delivery request.

## Completion contract

| Criterion | Status | Evidence required |
| --- | --- | --- |
| Recommend Astra medium parent; resolve ordinary implementation to Sol medium | satisfied | Profile changed; intended CLI Red and successful Green command |
| Preserve explicit Astra/custom profiles and reject unavailable requested models | satisfied | Updated CLI regressions; Green command exit 0 |
| Define small-task, difficult-work, and runtime-model evidence rules | satisfied | Updated contract and 26 schema-valid cases; independent review found no actionable issues |
| Validate consistent 5.1.2 package and installed snapshot | satisfied | 59 tests passed; repository/official validators passed; all 70 installed files match source |
| Set this parent task to Astra medium | satisfied | Current parent turn-context records gpt-6-astra / medium after user resume |

## Work and decisions

1. Handle the bounded profile/test/document changes directly; a separate
   implementation agent would add little useful work for this scope.
2. Obtain one fresh read-only Astra high review while running independent checks.
3. Honor the host's actual parent selection. A profile edit cannot change it.
   Computer Use explicitly disallows operating the Codex app; do not bypass that
   restriction or edit internal state/configuration to simulate a live change.
4. Describe child session model/effort metadata as runtime-configuration evidence,
   distinct from spawn intent and provider response identity. Use only related
   session metadata and preserve historical records as history.
5. Do not claim cost or quality improvements without comparable task evidence.

## Progress and evidence

- Confirmed a clean main checkout with PR #5 merged at `de515af`.
- At initial inspection, the profile recommended Astra high parent and Astra medium implementer.
- Earlier log audit established parent Astra xhigh and five child session
  configurations matching their spawn requests; that is historical evidence.
- The current tools do not expose a direct setting-only update for this active
  parent. Computer Use returned that the Codex app is disallowed for safety.
- Updated the role CLI regressions before the profile. Using bundled Python 3.12
  with `PYTHONDONTWRITEBYTECODE=1`, ran `python3 -m unittest discover -s scripts/tests
  -p test_execution_roles.py -v`. Red: exit 1, 16 tests with three intended failures
  under the old Astra default; log `/private/tmp/cost-aware-red.log` was inspected.
  Changed the profile to parent Astra medium / implementer Sol medium / reviewer
  Astra high. Green: the same command exited 0; log `/private/tmp/cost-aware-green.log`
  was inspected after resume and confirms 16 tests passed.
- Changed the execution contract and README to describe task-size-based
  delegation, difficult-item Astra selection, active parent-setting mismatch,
  child runtime-configuration evidence, and consumption comparison boundaries.
  Changed the source manifest to 5.1.2.
- The next command (behavior-case edits and follow-up reads/checks) was blocked
  before execution by missing
  `~/.codex/plugins/cache/codex-plugins/dev-core/5.1.1/hooks/scripts/block_dangerous_commands.py`.
  At that interruption, source eval cases still contained the old 5.1.1 expectations; these were updated after resume.
  No official installer, commit, or push was run. Cache removal cause is unknown;
  do not bypass hooks or rerun the blocked edit through another tool.
- Resumed with functioning 5.1.2 hooks. Inspected the prior Green log: 16 tests,
  OK. Updated the four routing cases and added three cases for small direct work,
  parent mismatch, and child runtime evidence; schema validation passed (26 cases).
- Current parent session turn-context now records `gpt-6-astra` / `medium`.
  The user-side setting change is confirmed; no UI bypass was attempted.
- Stable tracked candidate SHA256:
  `5900b1057612bd9652853e71f68524ef80c10d5e1a5d04619773c38352fb7df8`
  (`/private/tmp/cost-aware-candidate.patch`).
- Repository and official plugin/skill validators passed on the current candidate;
  behavior-case schema validation passed with 26 cases. Installed 5.1.2 is enabled
  from this local source, but its eval JSON still differs; reinstall after review.

## Final verification

- Full Python suite: 59 tests passed, exit 0; inspected
  `/private/tmp/cost-aware-suite.log` (10.297 seconds).
- Repository plugin validator, behavior-case schema validator (26 cases), official
  plugin validator, official skill validator, and `git diff --check` passed.
  Schema validation does not establish 26 live model behavior executions.
- Official `codex plugin add dev-core@codex-plugins --json` succeeded for 5.1.2.
  Compared source/cache relative file names and bytes: all 70 files identical.
- Cached resolver verified ordinary Sol medium, reviewer Astra high, and explicit
  Astra medium implementation, with fresh context and correct write policies.
  Astra-only capabilities rejected unavailable default Sol with exit 2 and no
  stdout; no fallback occurred.
- Parent current turn-context records Astra medium. Reviewer child session linked
  to this parent and `/root/cost_aware_review` records Astra high. These confirm
  client runtime configuration, not provider-reported response identity.
- No comparative cost/quality benchmark was run and no savings are claimed.

## Review ledger

- Completed: `/root/cost_aware_review`, requested and runtime-confirmed
  `gpt-6-astra` / `high`, fresh context, read-only. No actionable findings.
- Reviewer inspected the candidate, surrounding workflow, resolver, tests, and
  raw Red/Green evidence. Root independently confirmed the unchanged tracked
  patch SHA above, inspected source/test routing, and ran final checks.
- Review covers the six tracked changes and the plan. Subsequent edits only
  record final evidence in this plan; implementation candidate remains unchanged.

## Current next action

No implementation remains. Start a new task to load the updated skill context.
For later routing evaluation, compare equivalent tasks and include review and
rework consumption; the source change does not establish savings.

## Main delivery review — 2026-09-10

- The user requested review of the current changes and delivery to `main`.
  Include the profile, execution contract, behavior specifications, CLI tests,
  manifest version, corresponding README guidance, and this record.
- A new independent read-only review found no actionable issues. The parent
  inspected the resolver, changed assertions, profile, contract, and diff.
- Current source checks passed: Python 3.12 / PyYAML 6.0.2 full suite (59 tests),
  repository plugin validator, eval schema validator (26 cases), official
  dev-core plugin and collaboration-skill validators, SessionStart fixture,
  bundled agent TOML validation, and `git diff --check`.
- The local PreToolUse deny-fixture command was blocked before execution by the
  active hook because its input contains a forbidden command string. Do not
  count it as passed; inspect the existing CI smoke step after delivery.
- The reviewed candidate starts at `de515af`; the remote `main` matched that
  revision at preparation. Keep the previously recorded install/runtime results
  as historical evidence. No new live model scenarios or comparative benchmark
  were run. Verify the published revision and CI separately after push.
