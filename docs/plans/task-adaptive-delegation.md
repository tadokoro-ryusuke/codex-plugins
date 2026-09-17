# Task: Match delegation and verification to the work

- Status: done
- Plan file: docs/plans/task-adaptive-delegation.md
- Related issue/PR: none
- Last updated: 2026-09-17

## Goal and authorization

Implement the user's accepted audit findings: choose delegation by independent
work and evidence, align always-loaded instructions, and add comparative
evaluation guidance. Complete local implementation, verification, independent
review, and the repository-required plugin refresh. The user subsequently
authorized committing and pushing this change to `codex/adaptive-delegation`.
PR creation and a new user-owned task are not requested.

## Baseline and scope

- Clean `main` at `2449ceed2ad96cb460469cde25936af1b51e7f54`; work on
  `codex/adaptive-delegation`.
- Preserve the current Astra/high role profile, optional Sol/medium researcher,
  explicit selections, capability checking, fresh review, and ownership controls.
- Change dev-core instructions, the SessionStart context, behavior cases,
  evaluation procedure, plan template, README, manifest version, and the
  repository's outdated skill-list budget note.
- Do not add a router agent, a new orchestration framework, silent model
  fallback, or claims of measured cost/quality improvement.
- Source audit: `/private/tmp/codex-plugin-subagent-audit-2026-09-17.md`.

## Design decisions

- Let the parent implement sequential or tightly coupled work regardless of
  size. Delegate when independent work, specialization, or context isolation
  offers a concrete benefit beyond coordination cost.
- Decide review separately. Require independent review for consequential
  contracts, security/permissions, persistent data, concurrency, or an explicit
  project/user gate; use proportional self-review for low-risk changes.
- Resolve only roles actually selected. Preserve exact explicit/custom model
  selections. If optional delegation cannot run, disclose the limitation and
  keep suitable work with the parent; never silently launch an alternate model
  or waive required independent review.
- Reuse inspected check artifacts only when relevant inputs and environment
  still match and project rules permit reuse; distinguish previous execution
  from a check executed now. Invalidate affected evidence after changes.
- Limit Three Strikes to similar fixes on the same failing path. Keep unrelated
  safe work moving and preserve history across owner changes.
- Record delegation benefit, bounds, return evidence, and cancellation ownership.
  Treat a budget limit as incomplete work, never success.

## Completion contract

| ID | Criterion | Required evidence | Status |
| --- | --- | --- | --- |
| AC-1 | Execution topology and review decisions are independent and consistent | Parent inspected the final contract/cases; fresh independent review found no actionable issues; profile/resolver unchanged | satisfied |
| AC-2 | SessionStart preserves state output and emits scoped guidance | Existing fixture and syntax checks passed; parent inspected heredoc-only diff; resumed task received the updated repository state and SessionStart discipline | satisfied |
| AC-3 | Comparative evaluation covers sequential, parallel, explicit, unavailable, and stop cases | 49-case schema passed; comparison procedure inspected; unhinted native execution and external grader passed; comparative benchmark remains unexecuted | satisfied |
| AC-4 | Packaging and executable helpers remain valid | Package validator, four changed-skill validators, 66 offline tests, hook fixture/syntax, and candidate diff check passed | satisfied |
| AC-5 | Candidate receives independent review and findings are resolved | Fresh reviewer inspected candidate 6112a63855534a63bd38ff97c733edfb2b5dafd96ab1ce021e1e08feeaff4ce4; no actionable findings; parent inspected relevant artifacts | satisfied |
| AC-6 | Plugin version and installed snapshot are aligned, or a concrete activation limit is disclosed | CLI confirms installed/enabled 5.4.0; source/cache comparison has no differences; resumed task loads the new SessionStart guidance and shell tools work | satisfied |

## Work and ownership

The parent owns skill prose, behavior cases, docs, versioning, integration, and
this plan. A bounded implementer may own only SessionStart and its existing test
while the parent updates the disjoint instructions. A fresh reviewer owns no
files. Forward tests use temporary fixtures with no external mutations.

## Delegation ledger

| Work item | Role / agent ID | Requested settings / source | Observed settings | Ownership and bounds | Evidence / status |
| --- | --- | --- | --- | --- | --- |
| Hook context alignment | implementer / /root/hook_alignment | Astra high, bundled profile, capability-resolved | unverified | SessionStart script and existing test only; stop on unrelated defects | completed; parent inspected diff and reran fixture + syntax checks |
| Final review | reviewer / /root/adaptive_review | Astra high, bundled profile, capability-resolved | unverified | read-only final candidate; no edits | completed, no actionable findings |

## Verification

- `node scripts/validate-codex-plugins.mjs`
- `node scripts/validate-skill-evals.mjs`
- `python3 -m unittest discover -s scripts/tests -v` with the required parser
- `bash plugins/dev-core/hooks/scripts/test_session_start.sh`
- `bash -n plugins/dev-core/hooks/scripts/session_start.sh`
- Bundled skill creator validation for changed SKILL.md files
- Bounded behavior exercises; do not equate them with a comparative benchmark
- `git diff --check` and final diff/working-tree inspection

## Progress and decisions

- 2026-09-17: Re-read current source, accepted audit, governing instructions,
  execution and verification skills. Created the branch from the clean baseline.
  Keep profile model values unchanged; alter when delegation is useful first.
- 2026-09-17: Updated ownership/review selection, strict dispatch versus optional
  parent execution, verified evidence reuse, cancellation bounds, and same-path
  failure handling. Added 12 behavior cases (49 total), comparative evaluation
  guidance, the current skill-list budget note, and version 5.4.0 metadata.
- 2026-09-17: Package validator, 49-case schema validator, SessionStart fixture,
  hook syntax, and diff whitespace checks passed. Default Python lacks PyYAML;
  run the offline suite in an isolated uv environment with Python 3.13 and the
  CI-pinned PyYAML 6.0.2. CI uses Python 3.12; report the local version explicitly.
- 2026-09-17: All 66 offline tests passed. Four changed SKILL.md files passed the
  bundled skill creator validator. Independent review matched the candidate hash
  and returned no actionable findings. The parent confirmed profile/resolver
  files have no diff.
- 2026-09-17: Native ephemeral CLI exercise used the source skill and an unhinted
  approved fixture plan. The observed trace contains no child dispatch. The agent
  implemented directly, demonstrated Red/Green, and passed six candidate tests.
  The external grader independently passed all five behavior assertions and
  scope checks. This is one decision/behavior smoke, not a comparative benchmark.
  User configuration was excluded to isolate source instructions; this exercise
  does not establish installed hook activation.
- 2026-09-17: A second ephemeral read-only exercise for prior-evidence reuse
  exited successfully. On resumption, the parent inspected the final response
  and completed command events: source/test/configuration fingerprints and
  interpreter/platform matched, the prior raw test log was inspected, and no
  test command was rerun. Git checks failed because this temporary fixture is
  not a repository; the final response disclosed that limitation.
- 2026-09-17: `codex plugin add dev-core@codex-plugins --json` returned version
  `5.4.0` installed at
  `/Users/poshiri/.codex/plugins/cache/codex-plugins/dev-core/5.4.0`.
  The next shell command was blocked before execution because this active task
  still references the removed `5.3.0/hooks/scripts/block_dangerous_commands.py`.
  No hook bypass or safety-configuration change was attempted. Source changes
  are reviewed and tested; remaining post-install verification needs a task that
  loads the new snapshot. No commit, push, or PR was made.
- 2026-09-17: The user requested push. This resumed task received the new
  SessionStart context and shell commands worked. `codex plugin list` reports
  installed/enabled 5.4.0; `diff -qr` found no source/cache differences. The source
  diff still matches reviewed candidate 6112a63855534a63bd38ff97c733edfb2b5dafd96ab1ce021e1e08feeaff4ce4.
  Package and 49-case schema validators passed again. The unchanged 66-test
  result remains prior execution evidence. All implementation acceptance
  criteria are satisfied; prepare the scoped commit and push the feature branch.
  The workflow runs only for pushes to main and pull requests, so this feature
  branch push alone does not trigger CI.

## Evidence artifacts and limits

- Candidate diff: `/private/tmp/adaptive-candidate.diff`.
- Offline tests: `/private/tmp/adaptive-offline-tests.log`.
- Native execution request, tool trace, result, and independent grade:
  `/private/tmp/adaptive-native-direct-request.txt`,
  `/private/tmp/adaptive-native-direct-trace.jsonl`,
  `/private/tmp/adaptive-native-direct-result.txt`,
  `/private/tmp/adaptive-native-direct-grade.json`.
- Evidence-reuse exercise (final response and command events inspected):
  `/private/tmp/adaptive-evidence-reuse-request.txt`,
  `/private/tmp/adaptive-evidence-reuse-trace.jsonl`,
  `/private/tmp/adaptive-evidence-reuse-result.txt`.
- Remaining 49-case live coverage and repeated topology comparisons are pending;
  do not infer cost, latency, or general quality improvement from the smoke.
- This plan's final status/evidence update occurred after the reviewed source
  candidate and is checked as delivery documentation. Plugin source is unchanged
  after review and validation.

## Sources used for the policy change

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra
- https://learn.chatgpt.com/docs/agent-configuration/subagents?surface=app
- https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- https://learn.chatgpt.com/docs/build-skills
- https://github.com/mizchi/skills/blob/main/multi-agent-orchestration/SKILL-ja.md

## Current next action

Commit the reviewed source and this completion record, push
`codex/adaptive-delegation` to origin under the user's explicit authorization,
and verify local/remote commit identity and working-tree state. Use Git and
GitHub as the authority for delivery status. No implementation work remains;
live coverage of all behavior cases and repeated comparative benchmarks are
future evaluation work, not evidence established by this change.
