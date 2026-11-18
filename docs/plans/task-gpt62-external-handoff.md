# GPT-6.2 Profile IDs and the External Handoff Contract

- Status: in-progress (draft pull request from `codex/gpt62-handoff`; merge is the maintainer's decision)
- Date: 2026-11-18
- Counterpart record (Japanese, with the full evidence baseline and review
  integration): cc-plugins `docs/plans/task-gpt62-herdr-2026-11.md`

## Outcome

1. The bundled execution profile names the GPT-6.2 model IDs.
2. A Codex session started by an external parent with a handoff has one
   contract to follow.

## Scope

- `plugins/dev-core/skills/codex-collab/assets/execution-profile.json`: replace
  `gpt-6-astra` with `gpt-6.2-astra` and `gpt-6-sol` with `gpt-6.2-sol`.
  `gpt-6-luna` stays (GPT-6.2 ships no Luna).
- Tests, behavior cases, the evaluation guide, and the README table follow the
  profile.
- `plugins/dev-core/skills/codex-collab/references/external-handoff.md` (new),
  referenced from `codex-collab` and `dev-execute`.
- `planned-execution.md`: handoffs ask for checks not run, problems encountered,
  shared-machine limits, and cleanup.
- `dev-core` 5.8.0.

## Non-goals

- Changing roles, presets, or effort levels. Earlier assignments were user
  decisions; launch-day public benchmarks do not justify a re-route.
- A Codex-as-parent procedure for driving terminals in a multiplexer. Not
  requested; listed as a follow-up.
- Reinstalling the plugin or editing personal Codex configuration.

## Decisions

- ID swap only. The assignment remains unmeasured; the README says so.
- The comparison arm in `execution-evaluation.md` uses the current reviewer-tier
  ID. All arms share one frozen profile revision and record the model each arm
  resolved to, because the profile mixes generations by design.
- The receiver contract lives in `codex-collab` (the collaboration entrypoint),
  and `dev-execute` points to it, so a child that never loads `dev-execute`
  still has one rule to follow. The parent's handoff stays self-contained
  because the receiving session may not have this plugin installed.

## Evidence

| Check | Result |
| --- | --- |
| Codex CLI 0.166.0 accepts `gpt-6.2-sol` and `gpt-6.2-astra` in one authenticated environment | Two minimal read-only `codex exec` runs, exit 0 |
| Resolver tests fail before the profile change and pass after | `test_execution_roles.py`: 7 failures with tests updated first, then 28 passing |
| Baseline suite with the CI prerequisites | 127 tests passing before the change |
| Validators and full suite after the change (`HOTL_REQUIRE_SDK=1`, PyYAML 6.0.2, anthropic 1.17.0) | `validate-codex-plugins.mjs` passed; `validate-skill-evals.mjs` passed (68 cases); 127 tests passing |
| No retired IDs or labels in the profile, its tests, behavior cases, the evaluation guide, or the README's current table | Scoped search returned no match |
| Independent read-only review of the change set | Findings on the receiver contract and the comparison wording were verified and applied |

## Not verified

- Behavior cases are schema-validated only; none was executed.
- No comparative run of model or effort assignments.

## Follow-ups

- Codex-as-parent terminal orchestration.
- Comparative evaluation of the profile on the GPT-6.2 IDs.
