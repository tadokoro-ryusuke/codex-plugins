# Task: Role-based model selection for planned execution

- Status: completed
- Date: 2026-09-05
- Baseline: main at db7a7cf, clean at intake
- Workspace: codex/role-based-execution

## Goal

Make substantial planned execution use a coordinating parent, a Sol medium
implementation agent, and a separate higher-capability review agent. Keep model
choices centralized, handoffs bounded, and observed evidence distinct from
requested settings.

## Scope and decisions

- Recommend Astra high for the parent; the host owns its actual model selection.
- Default implementation to gpt-5.6-sol / medium and review to gpt-6-astra / high.
- Honor explicit task-level model choices. Validate model and effort against the
  current host's exposed capabilities; do not silently substitute an unavailable
  model. Do not modify account configuration or create replacement user tasks.
- Delegate one writer at a time by default. Keep the parent out of the writer's
  files; allow parallel work only with disjoint ownership and shared resources.
- Use fresh, sufficient handoffs and a read-only reviewer who can challenge the
  plan as well as its implementation. Preserve task authority and TDD.
- Add deterministic resolver tests, role-specific behavior scenarios, and a
  bounded native-agent exercise. A successful request does not by itself prove
  the effective backend model or a general task success-rate improvement.
- Change dev-core source and its directly related docs/tests. After final source
  acceptance, refresh only the installed dev-core snapshot using the repository's
  documented installation command and verified local marketplace. The user
  subsequently authorized commit and push of this completed change. Personal
  model settings, PR creation, and deployment remain outside this step.

## Completion contract

| ID | Observable result | Required evidence | Observed | Status |
| --- | --- | --- | --- | --- |
| AC-1 | One profile selects the implementation/review models and effort | Resolver CLI fixtures including unsupported capabilities and explicit overrides | 12 resolver tests and both role CLI resolutions passed on resume | satisfied |
| AC-2 | Execute delegates implementation, preserves parent ownership, and defines exception/review flow | Cross-file review of execute, collaboration, orchestration, and plan template | Independent final review of 19 source/test files found no open findings; parent inspected the contract and diff | satisfied |
| AC-3 | Model selection and bounded handoffs work in an actual agent exercise | Native dispatch records and independently inspected outputs; disclose unavailable effective-model metadata | Sol medium implementation and fresh Astra high review requested; current code identity matched, independent grader passed all five behaviors and scope; effective metadata unverified | satisfied |
| AC-4 | Packaging and regressions remain valid | Repository and official validators, tests, syntax/diff checks, independent review | 55 tests, repository/official validators, 20 scenario schema checks, AST/TOML/diff checks passed; no open review findings | satisfied |
| AC-5 | Installed snapshot includes the final reviewed fixes | Local-marketplace reinstall, source/cache comparison, installed helper execution | Reinstalled 5.1.0; full plugin directory comparison identical; installed grader passed five behaviors and scope | satisfied |

## Ownership

- Parent: this plan, skill/reference instructions, role-specific evaluation cases,
  native evaluation preparation/grading, README, and plugin version.
- Sol medium implementation agent: the central execution profile, its resolver,
  and dedicated unit tests only. Return Red/Green evidence, files, and concerns.
- A second Sol medium implementation agent: the separate smoke-fixture assets,
  preparer/grader, and dedicated unit tests. Its write set does not overlap the
  resolver or parent-owned files; both use independent temporary test resources.
- Astra high review agent: read-only review of the final changes. Return concrete
  findings without editing or treating the implementation report as proof.

## Verification

- node scripts/validate-codex-plugins.mjs
- node scripts/validate-skill-evals.mjs
- Python 3.12 / PyYAML 6.0.2: python3 -m unittest discover -s scripts/tests -v
- Official skill/plugin validation and git diff --check.
- Native agent exercise in an isolated temporary repository; no live service,
  production credentials, account changes, or publishing.

## Progress

- Read current skills, custom role assets, CI, repository rules, and previous
  source/runtime verification caveats. Confirmed clean main before branching.
- Reused current-session official documentation: Subagents, Sol model support,
  and model guidance. Runtime tools explicitly support model/effort overrides
  with fresh or limited-history agents; full-history forks inherit settings.
- Dispatched execution_policy and execution_smoke_harness with explicit
  gpt-5.6-sol / medium and fork_turns none. Runtime returned task IDs; effective
  backend metadata was not exposed by spawn/list responses.
- Parent inspected both implementations and independently ran their initial
  focused suites: 9 resolver and 10 smoke tests passed. Review identified invalid
  ownership/whitespace policy acceptance and incomplete grading evidence; returned
  focused corrections to the respective owners with Red/Green log requirements.
- Added role-aware execute/collaboration instructions, fresh handoffs, ownership
  transfer, parent decision returns, independent review, and requested/effective
  routing evidence. Added five behavioral scenarios; source version is 5.1.0.
- Independent source review found two P2 issues in evaluation: timestamp-valid
  bytecode could hide incorrect final source, and fixture preparation inherited
  Git signing/hooks. Root reproduced both. The implementation owner added two
  regressions and fixed source loading and preparation-only Git configuration.
- An installed-plugin update interrupted ordinary shell commands: this task
  retained a missing 5.0.0 hook path after the user installed 5.1.0. Preserved
  work without bypassing hooks; normal commands succeeded after session refresh.
- On resume, inspected branch, dirty scope, plan, source, and preserved fixture.
  Re-ran the focused 28 tests and full 55-test suite with Python 3.12; all passed.
  Repository/plugin validators, 20 behavior-case schema checks, both updated
  skill validators, Python AST, agent TOML, and diff whitespace checks passed.
- A fresh Astra high reviewer inspected all 19 scoped source/test files and
  independently closed both P2 findings with Python 3.12 regression tests.
  Its initial system-Python 3.9 cache-permission failure was an environment
  limitation; the required CI runtime is Python 3.12.
- Resumed the native fixture with a fresh coordinator. It independently ran
  the five fixture tests and requested a separate fresh Astra high reviewer.
  That reviewer found no actionable findings and matched the pinned candidate.
  The coordinator completed the fixture plan without rewriting source/tests.
- Root inspected final fixture source, tests, and plan, then ran the corrected
  independent grader: all five behavioral assertions and pre/post scope checks
  passed (exit 0). This closes the interrupted case without treating historical
  Red/Green reports as newly executed tests.
- Expanded the final activation step after observing that installed 5.1.0 lacks
  only the last two evaluation-helper fixes. Follow AGENTS.md's instruction to
  reinstall after source changes, after all children have finished. The CLI's
  marketplace listing resolves `codex-plugins` to this local repository, so no
  remote marketplace refresh or publication is needed.
- Ran `codex plugin add dev-core@codex-plugins --json`; exit 0, installed 5.1.0
  at the expected cache path. Full `diff -qr` between source and installed plugin
  returned 0 with no differences. Ran the installed grader on the preserved
  fixture: exit 0, all five behaviors and scope passed.

## Current evidence identity

- Source/test manifest SHA-256:
  `a0818d21a3cc6c99830e73b857871777d58cfe778dba936697b19dd7235f324b`.
- Manifest covers 19 changed/untracked source, test, and README files; excludes
  evolving plan/evidence notes. Final reviewer checked all hashes before/after.
- Local artifacts: `<evidence-dir>/source-manifest.json`,
  `full-tests.log`, `capabilities.json`, and `cache-comparison.json`.
- Full suite command: `PYTHONPATH=<pyyaml-dependency-dir>
  PYTHONDONTWRITEBYTECODE=1 <Python 3.12> -m unittest discover -s scripts/tests -v`
  from the repository root, exit 0, 55 tests. Python executable:
  `<python-3.12>`.

## Delegation ledger

| Work item | Role / agent ID | Requested model / effort | Input / ownership | Evidence / status |
| --- | --- | --- | --- | --- |
| Role policy | implementer / execution_policy | gpt-5.6-sol / medium | Central profile, resolver, dedicated tests only | Historical Red/Green; 12 tests independently passed on resume |
| Evaluation helper | implementer / execution_smoke_harness | gpt-5.6-sol / medium | Fixture assets, preparer/grader, dedicated tests only | Historical reproduction and fixes; 16 tests independently passed on resume |
| Final source review | reviewer / final_role_review | gpt-6-astra / high | Manifest above; no writes | No open findings; both prior P2s independently closed |
| Native case resume | coordinator / native_execution_resume | gpt-6-astra / high | Preserved isolated fixture and its plan; source skills read-only | Fixture plan completed; reviewed output matched; root independent grade passed |
| Native case review | reviewer / native_execution_resume/independent_quantity_review | gpt-6-astra / high | Pinned fixture source/tests; no writes | No actionable findings; code hashes unchanged |

All model-specific children use `fork_turns: none`. Selection follows the
central profile and host-exposed capabilities. Spawn/list responses expose
agent IDs, not effective backend model/effort metadata; mark that unverified.

## Native exercise result

- Fixture: `<fixture>`; baseline HEAD
  `faed3e722cc586fbb39700b8f2f4d99e285b0d8c`; branch `codex/line-quantities`.
- Historical implementation request: `gpt-5.6-sol`, `medium`, fresh context;
  returned `/root/native_execution_check/implement_quantity`.
- Fresh review request on resume: `gpt-6-astra`, `high`, fresh context;
  returned `/root/native_execution_resume/independent_quantity_review` and
  was also observed in the root's native agent inventory.
- Final source SHA-256:
  `127ba03272610a77bedb16ec89109d0c0c401a4f2cb32063fc6f73a73950bf4a`.
- Final tests SHA-256:
  `7c0560b471df023f8363b3627c79b925e95599510df67b9eeaf8c7a1d5959150`.
- Root grader command from repository root:
  `PYTHONDONTWRITEBYTECODE=1 <Python 3.12>
  plugins/dev-core/skills/codex-collab/scripts/execution_smoke.py grade
  --directory <fixture>`.
  Exit 0, five tests, no failures/errors/skips, scope passed. Raw result:
  `<evidence-dir>/native-grade.json`.
- Source/test identities remained stable across review, coordinator acceptance,
  and root grading. The coordinator changed only its plan on resume.
- This is one explicitly delegated smoke case, interrupted and resumed after a
  host refresh. It does not measure uninterrupted elapsed-time/cost improvement,
  the small-task delegation heuristic, or general success rate. The broader
  20-case suite received schema checks, not 20 native model executions.
- Effective backend model/effort remain unverified. Read-only review is an
  instruction boundary on this host, not a separately selected OS sandbox.

## Blockers and activation boundary

- No current blockers remain. The missing 5.0.0 hook reference was resolved by
  session refresh, without bypassing hooks.
- Before final installation, 14 of the 16 compared changed plugin files matched
  installed 5.1.0, while the two evaluation helpers differed. Reinstalling from
  the verified local marketplace synchronized the full plugin directory.
- Installed source equality was established with `diff -qr plugins/dev-core
  <plugin-cache>/codex-plugins/dev-core/5.1.0` (exit 0).
  Running that installed copy's `skills/codex-collab/scripts/execution_smoke.py`
  with the same grade arguments passed; raw output is
  `<evidence-dir>/installed-native-grade.json`.
- The refreshed session already loaded the 5.1.0 routing instructions before
  final reinstall; only the two evaluation-helper files changed in its cache.
  Do not infer effective backend model identity from this activation evidence.

## Current next action

No implementation work remains. Source implementation, independent review,
local native evaluation, and installed-snapshot verification are complete.
Commit and push were authorized on 2026-09-05; use Git history and the remote
branch identity for delivery status. Before delivery, recheck source hashes,
repository validators, the Python suite, and staged scope. Machine-specific
artifact paths are placeholders here; raw records remain local.
