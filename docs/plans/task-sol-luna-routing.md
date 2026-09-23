# GPT-6 Sol/Luna execution routing

## Outcome and authorization

Implement the user-approved recommendations in `../research/gpt-6-sol-luna-model-routing.md` for dev-core. Preserve explicit selections, custom profiles, ownership and review gates. Do not commit, push, or create a PR without a separate request.

Delivery authorization: the user subsequently requested pushing this change to
`main` on 2026-09-23. Commit and push the reviewed release and its two documents;
preserve any unrelated work and verify the remote revision and CI separately.

## Completion contract

| Criterion | State | Evidence |
| --- | --- | --- |
| Central defaults and implementation presets resolve against current host capabilities | satisfied | Bundled profile and CLI tests; resolver output inspected against host capability snapshot |
| Legacy profiles, explicit overrides, write policies and strict unavailable behavior remain compatible | satisfied | 28 resolver tests, including malformed presets, unavailable efforts and missing custom entries |
| Execute/debug/TDD instructions and behavior cases agree with the resolver | satisfied | Shared contract and 57 schema-valid cases inspected in independent source review; full live case inventory remains unexecuted |
| Required validators, offline tests and changed skill checks pass | satisfied | 71 offline tests; plugin/eval validators; four skill checks; SessionStart and TOML checks |
| Fresh native skill smoke and independent grading are recorded with routing limits | satisfied | Unhinted routine/high flow plus explicit bounded/max dispatch; each passed 5 external grader assertions and scope checks |
| Independent review findings are resolved and the reviewed diff is identified | satisfied | Fresh Astra/high reviewer found no actionable defect; 13-file source manifest matched |
| Version and installation state are recorded accurately | satisfied | 5.5.0 installed/enabled; 81 source/cache files matched; fresh verifier catalog references 5.5.0; current parent retains stale old hook reference |

## Decisions

- Keep the existing three roles. Keep parent and reviewer at Astra high; use Sol medium for general delegated implementation and Luna high for bounded read-only research.
- Add optional `implementation_presets` to schema version 1: `routine` = Luna high, `bounded` = Luna max, `complex` = Sol high. Keep critical design, integration and acceptance with the parent; use explicit authorized Astra selection for a rescue or comparison baseline.
- Select topology before model. The parent classifies work using the shared contract; the resolver does not guess task difficulty. Small coupled work can remain in the current parent.
- Automatically choose presets only from the bundled profile and without explicit role overrides. Custom profiles keep their defaults unless the user/project explicitly selects one of their own presets. Never merge missing presets or roles from the bundle.
- A preset changes only model and effort; inherit the implementer's scoped write policy. Reject preset selection on other roles and ambiguous combinations with model/effort overrides. Reject malformed preset configuration.
- Record requested routing separately from runtime/provider identity. A smoke does not establish comparative quality or cost superiority.

## Work and ownership

1. Parent: source policy, entrypoint references, evaluation cases/guidance, README, version, this plan and release validation.
2. Bounded implementation child: only execution-profile.json, resolve_execution_role.py and scripts/tests/test_execution_roles.py. Test new behavior first, then implement. Parent does not edit those files concurrently.
3. Fresh native smoke coordinator: isolated temporary fixture only; use source skills, current capabilities and native children. Parent owns the independent grader.
4. Fresh reviewer: read-only inspection of the stable source diff and raw validation evidence.

## Dispatch ledger

| Work | Benefit and bounds | Requested selection/source | Agent/input | Status and artifacts |
| --- | --- | --- | --- | --- |
| Resolver/profile/tests | Parallel executable implementation with exclusive three-file ownership; preserve public CLI compatibility | Sol high; user-approved complex implementation recommendation, explicit resolver override | /root/routing_implementation; base db5b5e6 on codex/sol-luna-routing | completed; three-file diff and Red/Green logs inspected by parent |
| Native smoke coordinator | Fresh skill behavior in an isolated fixture; fixture-only writes, source skills/capabilities read-only | Astra high; approved parent recommendation | /root/native_smoke_coordinator; fixture initial a26fdcd85225dd3e0cec19312415fb70e44ea400 | completed; routine Luna/high, fresh Astra/high review, independent grader 5/5 and scope passed |
| Independent source review | Fresh read-only review of routing contracts, compatibility, tests and evidence | Astra high; resolved bundled reviewer | /root/independent_routing_review; 13-file source manifest below | completed; no actionable defect, classification/evaluation limits recorded |
| Explicit max smoke | Independent implementation of an untouched fixture, two-file ownership, separate grader | Luna max; resolved bundled bounded preset, explicit dispatch test | /root/luna_max_smoke; fixture initial 4f50d56d3928a7d5f8c6b36a770682309e3c4ec4 | completed after explicit fixture authorization; external grader 5/5 and scope passed |
| Installed plugin and max-fixture verification | Fresh read-only context after install; cache/source hashes, independent assertions, task-linked runtime metadata | Astra high; approved independent reviewer recommendation | /root/installed_plugin_verification; installed 5.5.0 and pinned max diff | completed; raw JSON and actual diff returned and inspected by outer parent |

Effective model/effort: task-linked session metadata and response usage records
establish client runtime configuration for the resolver implementer (Sol/high),
native coordinator (Astra/high), first fixture implementer (Luna/high), and source
reviewer (Astra/high). A separate final check establishes the explicit max fixture
implementer's Luna/max client configuration across both turns, with matched parent
ID and usage records (`/private/tmp/codex-sol-luna-max-runtime-verification.json`,
session `01a0cc61-3b20-7cb3-ae93-d2595e85def9`). The usage records have no provider model field; provider
identity remains unverified. Filtered evidence:
`/private/tmp/codex-sol-luna-runtime-evidence.json`. Inspect only linked session
metadata, turn configuration and usage, without unrelated conversation content.
Write boundaries are instruction-level when the host does not expose a per-agent sandbox.

## Progress and evidence

- 2026-09-23: Read current source contracts, resolver, tests and prior research. Initial checkout had only the related research report untracked. Created `codex/sol-luna-routing`; no unrelated changes present.
- Implemented 5.5.0 source routing, shared execute/debug/TDD contract, README and eight additional behavior cases. Kept the original research report as historical evidence with a link to this implementation.
- Resolver Red: `/private/tmp/codex-sol-luna-resolver-red.log`, 28 tests with 25 failures and one error against pre-change behavior. Green: `/private/tmp/codex-sol-luna-resolver-green.log`, 28 passed after implementation; parent inspected the actual code/test diff and both logs.
- Full offline suite: Python 3.12 / PyYAML 6.0.2 via temporary uv environment, `python -m unittest discover -s scripts/tests -v`, 71 passed in 10.299s; raw log `/private/tmp/codex-sol-luna-offline-tests.log`. Fixtures/mock services do not prove live behavior.
- `node scripts/validate-codex-plugins.mjs`, `node scripts/validate-skill-evals.mjs` (57 cases), `git diff --check`, four changed skill `quick_validate.py` checks, SessionStart fixture check and bundled agent TOML validation passed.
- A separate optional CI-style destructive-command hook smoke was blocked before execution because the active PreToolUse hook matched the literal synthetic payload in the command. Did not disable or bypass the hook. Removed that optional hook test from the unaffected skill/TOML validation command and reran those checks successfully. The destructive-command hook itself is unchanged and that extra deny/pass smoke remains unexecuted in this turn.
- Inspected `codex plugin list`: installed dev-core is 5.4.0, enabled, sourced from this local repository. Installation remains pending until source validation and review finish.
- Stable source review candidate: 13 tracked files, per-file SHA256 manifest `/private/tmp/codex-sol-luna-source-manifest.json`, manifest SHA256 `dbf801fc3d276399767776643a32d11d66917e03d7a796010634f86726cc41d5`. Evidence-only plan updates and the historical research report are outside this source manifest.
- First native fixture coordinator selected `routine` (Luna/high) for the small quantity-validation task. Preserve that unhinted observation; it does not cover max dispatch or prove classification consistency. Prepare a separate explicit `bounded` (Luna/max) dispatch smoke without using the first implementation as input. Do not compare their efficiency as matched experiments: coordination and review arrangements differ.
- Independent review completed with no actionable defect. Reviewer inspected source/assertions and raw prior logs, reran packaging/eval/diff checks, and used in-memory probes for custom-profile defaults with same-named presets, unavailable unselected presets under explicit overrides, and malformed types. Parent confirmed source-manifest parity. Review noted overlapping routine/bounded criteria: retain parent judgment and classify the first smoke as routine/high evidence only.
- Broader live general/complex/custom/debug/TDD classification cases and repeated matched quality/cost comparisons remain unexecuted. This release adopts the user's approved defaults, without claiming empirical optimality.
- First native smoke completed: coordinator inspected Red/Green, fresh reviewer found no actionable defect and passed 11 boundary probes. Outer parent then inspected actual source/test diff and ran the external grader: 5/5 independent assertions and scope passed (`/private/tmp/codex-sol-luna-native-grade.json`). Source/test diff SHA256 `745467d3f42be0aabebbb981a7035f0e70f5d24cf25902aa76446f0319214253`.
- Initial max-fixture edit was rejected by automatic approval review as insufficiently connected to the user's authorization. No alternate editing route was attempted. User explicitly approved the exact two-file temporary fixture test through the input UI; the same Luna/max agent resumed normally. It reported Red (10 failures) and Green/refactor (4 tests passed), with source/test diff SHA256 `51ec02bc89642c2fe46a119190de50c16b36ca19e38cc04a58e200769a740490`; independent grading pending.
- `codex plugin add dev-core@codex-plugins --json` succeeded and reported version 5.5.0 at `/Users/poshiri/.codex/plugins/cache/codex-plugins/dev-core/5.5.0`. Installation removed the old 5.4.0 cache; this outer context's next shell check was blocked by its stale 5.4.0 PreToolUse path. Did not disable or bypass the hook. A fresh read-only verifier is checking installed/cache state and the max fixture through its normal tools; a fresh user task is required for updated skill activation.
- Final independent verification completed through normal tools without hook errors or hook changes: `codex plugin list` shows 5.5.0 installed/enabled; all 81 source/cache files match by path and SHA256 (generated Python caches excluded); all 13 reviewed source-manifest entries remain unchanged. Evidence: `/private/tmp/codex-sol-luna-installed-verification.json`. Fresh verifier's skill catalog references 5.5.0; runtime hook version remains unknown.
- Max fixture independent grade: Python 3.9.6 standard-library grader, exit 0, 5/5 assertions and scope passed; no skipped tests. Grader logs and before/after hashes are in `/private/tmp/codex-sol-luna-max-independent-grade.json` and `.log`. Actual two-file diff is `/private/tmp/codex-sol-luna-max-reviewed-diff.log`, hash matches `51ec02bc89642c2fe46a119190de50c16b36ca19e38cc04a58e200769a740490`. Outer parent inspected the returned raw grader JSON, actual diff and parity report. Fixture plan remained unchanged under the child's two-file allowance; this release plan records final acceptance.
- Both smoke outcomes establish their fixed local contract only. The first independently selected routine/high; the second explicitly selected bounded/max. Neither establishes unhinted max classification, comparative quality, speed or cost optimality. Source implementation/review evidence and fixture validation remain separate from provider attestation.
- Main delivery preparation: inspected current Git scope (13 modified source files and these two new documents), confirmed all 13 source hashes still match the reviewed manifest, and inspected the earlier 71-test raw log. Reused that unchanged-source test evidence; reran plugin/eval validators and diff checks successfully. The new turn exposes 5.5.0 skills and normal shell commands work again. Keep the earlier stale-hook incident as historical evidence.
- Remote preparation: the SSH agent could not sign during fetch. Used the existing GitHub CLI credential helper with a per-command HTTPS URL; kept the configured SSH remote unchanged. Fresh `origin/main` and local base both resolve to `db5b5e6558a5bf7c741db5675930aac50c8dd775` (ahead/behind 0/0), so this release needs no conflict resolution.

## Blockers and failed-attempt history

- No design blocker or repeated unsuccessful implementation fixes. Initial sandboxed branch creation could not write Git metadata; the authorized escalated branch creation succeeded. Max-fixture authorization rejection was resolved by the user's explicit approval. Keep that permission event separate from TDD Red and failed-fix counts.

## Current next action

Implementation, validation, independent review and local installation are complete.
Publish the user-authorized release to `main` after checking remote ancestry.
Record actual local/remote commit and CI results in the delivery response and
`/private/tmp/codex-sol-luna-main-delivery.json`; do not infer remote success from
this preparation record. Repeated matched model comparisons remain future
evaluation work, not a completion claim of this release.
