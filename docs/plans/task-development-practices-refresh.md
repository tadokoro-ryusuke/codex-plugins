# Development practices refresh

- Status: done
- Date: 2026-09-05
- Baseline: main at d17d0ab; working tree clean at intake
- Workspace: codex/development-practices-refresh

## Goal and scope

Audit and improve development instructions, orchestration, verification, and
delivery templates in dev-core, github-tools, and hotl-engineering using current
primary sources and reproducible repository evidence.

Preserve the existing TDD/evidence discipline, explicit delegation gate, plugin
layout, and user authority. Exclude marketing/design content, sibling repository
edits, commits, pushes, deployed workflows, account configuration, and plugin
installation. Prepare source versions for a later release; source validation is
not installed-runtime or hosted-CI proof.

## Completion contract

| ID | Observable result | Required evidence | Observed | Status |
| --- | --- | --- | --- | --- |
| AC-1 | Prioritized findings distinguish current sources, reproduced defects, and local policy | Dated research report with direct source URLs and affected paths | docs/research/development-practices-2026-09-05.md; 13 findings, 10 primary sources | satisfied |
| AC-2 | Verification reports all detected stacks and missing prerequisites without a false success | Isolated command fixtures fail before fixes and pass afterward | 9 runner tests; 7 failed before the fix, 9 passed after | satisfied |
| AC-3 | Selected delivery-template defects have deterministic regressions and fixes | Local fixture tests plus workflow inspection | 12 eval/verdict tests and 6 workflow tests passed; cloud adapters explicitly remain project requirements | satisfied |
| AC-4 | Development instructions define proportional checks, delegation contracts, evidence freshness, and approval continuity | Cross-file review and expanded behavioral scenarios | Reviewed shared/narrow instructions; 15 behavior cases defined and schema-validated, model execution not claimed | satisfied |
| AC-5 | Updated packages are internally consistent and reviewable | Repository validators, hook/script tests, syntax checks, final diff review | Both validators, 27 tests, 7 actionlint YAML checks, 10 official skill validations, 3 plugin validations, hooks/TOML/syntax and diff checks passed | satisfied |

## Implementation sequence

1. Complete primary-source audit and inspect verification/delivery failure paths.
2. Add failing regression fixtures for confirmed script/template defects.
3. Implement narrow fixes; run focused tests.
4. Align workflow/reference instructions, behavior-eval cases, and package versions.
5. Run repository checks, one bounded independent read-only review, and record results.

## Decisions

- Apply dev-workflow and skill-creator; use official OpenAI documentation for
  current Codex behavior. Apply dev-execute to this execution plan, including its
  explicit authorization for one bounded read-only independent review.
- Treat tests of script behavior separately from skill-behavior evaluations;
  schema validation alone cannot demonstrate agent behavior.
- Fix verified high-impact issues first. Record provider/platform-specific
  deployment choices as adaptation requirements rather than inventing defaults.

## Progress and evidence

- Intake: inspected AGENTS.md, README, orchestration, verification runner,
  skill-eval validator and six cases, GitHub PR workflow, HOTL templates.
- Created branch after normal sandbox blocked writing the Git ref; scoped
  escalation succeeded. No user data or previous changes were modified.
- Official sources opened: Build skills, Subagents, Evaluation best practices.
- Verification regression baseline: 9 CLI fixtures, 7 failures before changes;
  all 9 pass afterward (isolated PATH, no project installs/network execution).
- HOTL independent review reproduced absent/malformed verdict acceptance and
  target-error averaging. Parent fixtures independently reproduce and fix them.
- HOTL gate tests: 11 pass (target/judge failure, revision mismatch, schema,
  required tiers, observation mode). Workflow tests: authorization/preflight
  failed before fixes; all 4 now pass with YAML parsing and offline execution.
- Updated development orchestration, proportional verification/test guidance,
  authorization continuity, review roles, and HOTL adaptation requirements.
- Final review added regressions for required baseline and fresh output; guarded
  artifact publishing against missing output directories. Full suite: 27 passed.
- Recorded source versions: dev-core 5.0.0, github-tools 1.4.0, HOTL 2.0.0.
- Scope completion is source-only. No hosted workflow, cloud recovery, installed
  cache, or model-behavior success claim. No commits, push, or external deployment.

## Stop conditions

Stop the affected path after three similar failed fixes or on unapproved
destructive/external actions. Continue independent safe work. Re-plan when
evidence changes scope; keep unsupported criteria pending.

## Current next action

Completed the source update. The next optional delivery action is user review of
the recorded migration requirements and branch diff before authorizing release.
