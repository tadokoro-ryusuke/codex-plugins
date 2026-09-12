# Astra Skill Refresh

## Scope and completion

Apply the 2026-09-11 OpenAI article [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) to the marketplace's current skills. Preserve domain guidance and operational constraints while narrowing discovery, loading references by need, and removing unnecessary process or approval stops. Set the approved dev-core defaults to Astra high for the parent, implementation, and independent review, with optional read-only Sol medium research; preserve explicit overrides.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Audit all source plugin skills and implement justified changes | satisfied | Scoped diff and recorded audit disposition |
| Resolve default implementation to Astra high, preserve overrides and capability failures | satisfied | CLI regression Red/Green |
| Preserve discovery, bundled links, safety and completion behavior | satisfied | Package validation and independent scenario checks |
| Validate and refresh changed installed plugins | satisfied | Offline suite, validators, review, supported installer and source/cache comparison |

## Decisions and ownership

- Start from clean `main` at `9240d5b`; work on `codex/astra-skill-refresh`.
- Root owns dev-core entrypoints/references, repository guidance, README, versions, integration and validation.
- `/root/astra_profile` owns collaboration skill/profile and routing tests/cases.
- `/root/skills_audit` audits non-dev-core plugins read-only before any bounded edits.
- Keep historical plans as historical records. Do not claim source validation proves live model selection or improved cost/quality.
- The original request authorized implementation only. The later main-delivery request explicitly authorizes commits and a push to main; no PR is requested.

## Progress and evidence

- Read the official article and current skill-creator guidance, repository instructions, existing cost-aware plan and current profile.
- Current profile: parent Astra medium, implementer Sol medium, reviewer Astra high.
- Branch creation required filesystem escalation for Git metadata and then succeeded.

## Blockers

None.

## Current next action

Implementation and installation are complete; the delivery candidate is verified. Publishing to main is now authorized. Record the remote revision and CI outcome in the final delivery report. The host owns the active parent selection.

## Audit disposition and current validation

- Audited all 27 source skills across five plugins; changed 25. Kept
  `github-workflows` and `global-landing-design` because their routing, scope,
  authorization, and evidence guidance already fit this request.
- Shortened source skill names/descriptions from 10,212 to 4,116 characters
  (about 60%); entrypoint lines from 2,714 to 1,769. These are source-size
  measurements, not model token, selection-accuracy, or quality benchmarks.
- Moved substantial conditional domain guidance into 11 focused references;
  preserved existing explicit-only policies for reference skills.
- Removed fixed hypothesis/search/pass counts, broad tutorial examples, repeated
  orchestration reads, and planning/client-draft stops that ignored existing
  authorization. Preserved executable-behavior TDD, security/ownership boundaries,
  required gates, current evidence, three-failed-fix limits, and real sign-off.
- New source versions: dev-core 5.2.0, indie-product-marketing 0.3.0,
  ui-ux-pro-max 1.3.0, hotl-engineering 2.0.1.
- Live installer inventory shows local dev-core, indie-product-marketing, and
  hotl-engineering installed and enabled. The installed UI UX Pro Max comes from
  a different marketplace; update this repository's UI source only and preserve
  that installed vendor plugin. Do not install a second UI plugin.
- Root independently reproduced the routing Red against the HEAD profile in a
  disposable fixture: 17 tests, four intended failures, exit 1. Raw log:
  `/private/tmp/astra-role-independent-red.log`.
- Root ran the complete offline suite on the new profile: 60 tests passed,
  exit 0; `/private/tmp/astra-skill-suite.log`. The actual resolver is unchanged;
  CLI tests cover defaults, explicit/custom overrides, unavailable model/effort,
  fresh context, and write policy.
- Root ran repository validation, 33-case eval-schema validation, SessionStart
  fixture, bundled agent TOML checks, all 25 changed skill official validators,
  all four changed plugin official validators, Markdown link resolution, and
  `git diff --check`: passed. The 33 cases are specifications, not 33 executed
  model scenarios.
- Root ran bundled UI search from `/private/tmp` for UX keyboard navigation and
  React form validation; both returned three results using the source data.
- Python 3.9 and bundled Python lacked PyYAML. Created an isolated temporary
  Python 3.12 environment with PyYAML 6.0.2 for official validators and the full
  suite; no project or global dependency configuration was changed.
- Stable candidate identity excluding this evidence plan:
  `eef1836b44fc0f0e5da4f84e8d4f9da9c00f3df1b8258320b4ef2f098db7d085`.

## Review and behavioral check assignments

- `/root/skills_audit`: independent read-only review of root/reference-agent
  changes in dev-core, HOTL, and repository guidance; no claim of independence
  for its own indie/UI edits. Root inspected those diffs and reran the UI CLI.
- `/root/forward_check`: fresh-context execution of a plan-and-fix request in
  `/private/tmp/astra-skill-forward`, with source skills and raw fixture only.
- These checks and the refresh are completed in the final record below.

## Final review, forward test, and installation

- Independent review found one malformed job table; corrected its delimiter to
  seven columns and verified header/delimiter/data alignment. Follow-up review
  confirmed no unresolved findings in its scope.
- The fresh-context forward test completed planning, Red/Green implementation,
  and six local fixture tests without questions, extra authorization, or early
  stopping. Root independently asserted boundary behavior and confirmed fixture
  instructions were unchanged. Fixture: `/private/tmp/astra-skill-forward`.
- The observed run loaded nine skill/reference/template files. Narrowed the
  dev-task standards lookup and dev-execute orchestration/review reads for small
  steps; independent follow-up review and affected structural validators passed.
  These final read-routing refinements have no additional dynamic measurement.
- Final source candidate (excluding this plan): `091c17ac8c54d4d860046a1d1f0d0fc78e7abcd6f27a56729490322a50de441b`.
  Repository/eval validators and diff checks passed after the final edits.
- Refreshed only the three already-installed local plugins using the supported
  `codex plugin add <plugin>@codex-plugins --json` command. Verified their enabled
  versions and exact source/cache contents (excluding transient Python bytecode
  and OS metadata). Preserved other installed plugins, including vendor UI UX.
- Installed indie-product-marketing 0.3.0: 31 matching files.
- Installed hotl-engineering 2.0.1: 22 matching files.
- Installed dev-core 5.2.0: 81 matching files.
- Cached resolver confirmed implementer/reviewer Astra high, preserved explicit
  Sol medium override, and rejected unavailable high effort with exit 2 and no
  spawn request. This verifies installed resolution, not provider model identity.
- Installation evidence: `/private/tmp/astra-plugin-refresh.json`. No commit,
  push, PR, or new user-owned task was created.

## Approved role recommendation follow-up

- Status: complete. The user accepted the proposed operating split.
- Set the default parent recommendation to Astra high; keep implementation and
  independent review at Astra high. Permit Astra medium for an explicitly chosen
  execution-only parent when requirements and acceptance are already settled.
- Add an optional read-only researcher role using Sol medium for bounded source
  lookup, inventory, and log classification. Keep important design/root-cause
  judgments with the parent; do not create a research agent for every task.
- Preserve existing custom profiles with only implementation/review roles. If
  researcher is requested but absent, reject clearly rather than substitute a
  bundled model. Keep explicit overrides, capability checks and read-only policy.
- Root owns source, tests and integration; independent read-only review checks
  compatibility and the final diff. Record Red/Green before source edits.
- Next: add regression cases for the parent default and optional research role.

### Follow-up verification

- Red before source changes: 23 role tests, 10 intended failures including
  subtests; `/private/tmp/astra-role-followup-red.log`, exit 1.
- Green after the minimal resolver/profile change: 23 role tests passed;
  `/private/tmp/astra-role-followup-green.log`, exit 0.
- Full offline suite: 66 tests passed;
  `/private/tmp/astra-role-followup-suite.log`, exit 0.
- Repository validation, 37-case eval-schema validation, official collaboration
  skill and dev-core plugin validators, and diff checks passed. No new live
  model-routing benchmark was run; behavior-case validation checks its schema.
- Compared all prior changed/new files against the follow-up baseline hashes:
  only the eight intended existing files changed; the resolver is the sole
  additionally modified tracked file. Preserved the previous skill-refresh work.
- Next: complete independent review, reinstall dev-core 5.3.0, and verify cached
  parent/role settings and resolution.

### Follow-up completed

- Independent final review found no actionable issues; root inspected the actual
  resolver diff, tests, docs and logs and checked the candidate remained unchanged.
- Supported installer refreshed dev-core 5.3.0 and the CLI reports it enabled.
- All 81 packaged source/cache files match. Cached profile recommends
  Astra high for the parent; resolver returns Astra high for implementation and
  review, Sol medium/read-only for research, all with fresh contexts.
- Cached legacy two-role profile resolves implementation and rejects a missing
  researcher with exit 2 and no stdout.
- Evidence: `/private/tmp/astra-role-followup-install.json`. These checks establish
  installed configuration/resolution, not live provider model identity.
- No commit, push, new user-owned task, or unrelated plugin refresh was performed.

## Main delivery candidate (2026-09-12)

- The user explicitly requested a push to main. Classify all 42 tracked changes
  and 12 new Markdown files as the previously approved source/docs/test scope.
- Fetch confirmed local main, origin/main, and the starting branch HEAD at
  `9240d5b5ebe971e8c6c10ef8eb033c9b6f965388`; no remote changes need integration.
- Reran the full offline suite: 66 tests passed in 10.335 seconds. Evidence:
  `/private/tmp/astra-main-delivery-suite.log`.
- Reran repository validation, 37-case eval-schema validation, SessionStart
  fixtures, official validation of all 25 changed skills and four plugins,
  bundled agent TOML validation, and diff checks: passed.
- Matched all eight role-candidate files against their reviewed hashes.
  Independent delivery review found no blockers, version drift, credential
  indicators, or generated artifacts in the approved changes.
- Group delivery into the dev-core workflow/role update and the supporting
  design, marketing, delivery-guidance, and documentation update. Preserve the
  resulting commit history with a fast-forward main update and normal push.
- This record describes the verified pre-push candidate. The final task report
  records the published revision and that revision's GitHub Actions outcome.
  These checks do not establish live model identity or cost/quality improvements.
