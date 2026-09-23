# Planned Execution and Delegation

Use this contract when planned execution benefits from delegation or needs
independent review, or when dev-debug/dev-tdd selects a bounded handoff.
Honor explicit user instructions over these defaults. Keep narrow standalone
tasks outside the full execution workflow. Use the optional research role only
for the bounded information-gathering work described below.

## Choose ownership and review before resolving roles

Keep sequential or tightly coupled implementation with the parent regardless of
plan size. Delegate only when independent progress, specialized evidence, or
context isolation offers a concrete benefit beyond handoff, waiting, integration,
and verification costs. A role name or a runnable test alone is not that benefit.
Honor explicit delegation requests within host capabilities and safe ownership.

Choose the smallest useful arrangement: parent implementation and self-review,
parent implementation with independent review, or bounded delegated work with
parent integration. Select review separately using the gate in
`../../dev-workflow/references/orchestration.md`. Preserve required independent
review even when the parent implements; do not require an implementer child just
to obtain a reviewer. Use tools directly for deterministic work.

Record the benefit and boundaries briefly in the existing plan; do not spawn a
router or produce a separate orchestration plan just to make this choice.

## Resolve selected roles before dispatch

Read `../assets/execution-profile.json` as the single source of default model and
reasoning settings. The parent recommendation guides task setup; the host owns
the active parent model. Do not pretend to switch it, create a replacement user
task, or infer its effective setting from the recommendation. Record the active
setting only when the host exposes it; otherwise label it unknown.

Check the active parent setting against the recommendation when setting up roles.
Report a mismatch once; a profile edit does not change the running task. Use a
supported host setting control only under applicable user authority. If none is
available, explain how the user can select the setting. A bundled recommendation
does not block suitable work in the existing parent; preserve explicit task
requirements. Do not edit internal runtime state to simulate a change.

Use a task-authorized profile path when one is supplied; otherwise use the bundled
profile. Apply an explicit model/effort override for the relevant role when the
user or applicable project instruction requests it. Preserve custom profiles and
explicit selections. Do not install models or change personal configuration as
part of resolution.

Use the selected profile's parent recommendation for requirements, design,
integration, and acceptance decisions. Keep ambiguous requirements, architecture,
and consequential scope decisions with the parent. A standalone skill invocation
does not change the active model or require a child.

Use the selected profile's reviewer when independent review is selected. Apply
changed role selections only under explicit task/project authority and record
their source in the dispatch ledger. Use original requirements and fresh review
context; a different reviewer model is not itself evidence of independence.

### Select an implementation preset

Classify the work in the parent after choosing delegation. Do not create a router
agent or use a resolver to infer difficulty. Keep all model/effort values in the
profile; refer to these preset names in handoffs and record the selection reason.

When using the bundled profile without an explicit role override, this contract
authorizes selecting its implementation preset by these criteria:

| Selection | Use when |
| --- | --- |
| `routine` | The edit is short, mechanical and low risk, with exact acceptance checks; delegate only if the ownership decision already justifies it. |
| `bounded` | Behavior and interfaces are settled, allowed files and local dependencies are known, and independent checks can verify the result without new design decisions. |
| Role default (no preset) | General implementation has a bounded outcome but requires ordinary code investigation or integration choices. |
| `complex` | A delegated item requires substantial cross-module reasoning, competing technical hypotheses, or a complex implementation within parent-owned decisions. |

Use `bounded` only when all its conditions hold. A small diff, one passing test,
or a low file count does not establish them. For unresolved authorization,
migration, concurrency or public-contract decisions, first return those decisions
to the parent. After the parent settles them, choose a suitable implementation
scope and retain required independent review. Keep ambiguous root-cause judgment
with the parent; a complex child may gather and test bounded hypotheses.

Preserve explicit task model/effort overrides by omitting `--preset`. For a custom
profile, use its role default unless the user or project explicitly selects one
of its presets. Do not infer opt-in from a matching preset name, copy bundled
presets into a custom profile, or synthesize a missing selection. Legacy profiles
without presets remain valid.

Resolve the chosen selection before dispatch. The resolver accepts presets only
for `implementer`, rejects combining them with `--model`/`--effort`, and inherits
the role's write policy. Define optional `implementation_presets` as a mapping of
non-empty names to objects containing only `model` and `reasoning_effort`; presets
cannot expand ownership. Missing presets and unavailable settings are errors.

When evidence invalidates a bounded assignment, stop that path and return the
assumptions, failing evidence and attempt history to the parent. Re-scope first;
do not silently raise effort, widen writes, or reset failure counts with another
agent. The parent may select a different bundled preset for the revised scope
under this contract; preserve explicit/custom requirements. Use a fresh agent
and transfer ownership before changing model/effort.

### Optional bounded research

This skill authorizes the profile's `researcher` role for read-only source lookup,
API inventories, or log classification when independent work helps the active
dev-core task. Keep architecture, ambiguous root-cause conclusions, and acceptance
judgments with the parent. Research does not replace implementation or review,
and is not a prerequisite for every task. Use scripts directly for deterministic
checks rather than introducing another model role merely to execute them.

Give the researcher its question, permitted input paths, evidence to return, and
stop condition. Require source references, uncertainties, and no file or external
mutations. Use the same capability validation, fresh context, and parent evidence
checks as other roles. Resolve `--role researcher` only when dispatch is useful.

The researcher entry is optional in schema-version-1 custom profiles. Existing
profiles with only implementation and review remain valid. If the requested role
is absent, report that limitation; neither an explicit model override nor the
bundled profile may synthesize the missing role. Respect configured choices and
never silently fall back to a different model or effort.

### Validate host capabilities

Create a temporary capability JSON from the model identifiers, supported efforts,
and selection controls actually exposed by the current host:

- `can_select_model`: whether the spawn interface accepts an explicit model.
- `can_select_effort`: whether it accepts an explicit reasoning effort.
- `models`: a mapping of available model identifiers to supported effort strings.

Do not treat a model catalog or an example capability file as account availability.
If the host cannot establish these capabilities, report the unavailable evidence
and apply the unavailable-dispatch rules below.

Resolve only selected roles from the collaboration skill directory. For example:

```bash
python3 scripts/resolve_execution_role.py --role implementer --capabilities "$capabilities_file"
python3 scripts/resolve_execution_role.py --role implementer --preset bounded --capabilities "$capabilities_file"
python3 scripts/resolve_execution_role.py --role reviewer --capabilities "$capabilities_file"
```

Use `--profile` for the selected profile and both `--model` and `--effort` for an
explicit override; omit `--preset` when supplying that pair. Exit `2` means that dispatch request cannot be resolved; do not
silently launch another model or omit the specified effort.

Translate the returned model and reasoning settings into the host's actual spawn
arguments. Use a fresh agent context plus a sufficient handoff. On a host exposing
`fork_turns`, use the returned `none`; full-history forks on that interface inherit
the parent configuration and cannot apply these overrides. Do not invent tool
arguments on other hosts. Recheck capabilities after a host/session change.

The resolver does not launch an agent. Its `write_policy` is an ownership
instruction, not a sandbox setting. Use a read-only sandbox for review when the
host offers one; otherwise report read-only as an instruction-level boundary.

### Unavailable dispatch

Distinguish a bundled recommendation from a user/project-required model, role,
or custom profile. If optional delegation cannot run, disclose the limitation
and keep suitable implementation or research with the existing parent. Do not
resolve unused roles or block parent work on their availability. This changes
ownership, not the active parent model, and does not establish role execution.

Keep explicit model/role requirements and required independent review pending
when unavailable. Continue unaffected work and report the exact gap; do not
replace a custom profile, synthesize a missing role, self-review in place of a
required reviewer, or claim completion. Obtain applicable authority before
changing a required selection. The resolver remains strict for every dispatch.

## Parent responsibilities

Check that each work item has sufficient acceptance criteria before delegating.
Own the overall plan, scope decisions, dependency order, shared resources,
integration, and final acceptance. The parent may inspect code and run remaining
checks while a child works, but must not edit the child's files concurrently.

Default to one implementation owner at a time. Multiple implementation agents
are useful only when their file ownership, dependencies, and shared resources
are disjoint. Keep a named owner for shared interfaces and integration. Separate
worktrees do not isolate ports, databases, deployments, or credentials.

Perform useful coordination while a child works. Avoid implementing the same
change again or rerunning a completed suite without changed inputs or an
unresolved evidence gap. Inspect returned artifacts and actual command evidence;
do not accept a summary saying tests passed as sufficient proof.

## Implementation handoff

Give the implementation agent:

1. Its role and one bounded outcome, with the relevant plan section and raw input
   files. Include applicable instructions and decisions needed in a fresh context.
2. The checkout/branch and input revision or diff identity; identify existing
   changes that belong to other work.
3. An explicit allowed write set, dependencies, and shared-resource ownership.
4. Acceptance criteria, relevant project commands, and concise evidence to return.
5. Expected benefit, effort bounds, and conditions for returning to the parent
   rather than guessing or expanding scope.

Include only the necessary interfaces, decisions and evidence in the handoff.
Do not forward the parent's full history or a generic workflow manual merely
because the parent has a larger context window.

Tell the agent to use TDD for executable behavior or regressions and applicable
checks for other changes. Require the changed files, tests and commands/results,
input/output identity, remaining concerns, and one of
`completed`, `needs-parent`, or `blocked`. Let it choose routine implementation
details within the contract. Have it update only its assigned plan section when
that write is explicitly included; keep the overall plan under parent ownership.

Do not let an implementation child recursively invoke the full execution
workflow, spawn another implementation/review chain, commit, or publish under
authority absent from its handoff.

Use bounds appropriate to the work: a finite source set, a time/tool budget, or
a no-new-evidence stop condition. State numeric limits only when meaningful;
claim enforced token limits only when the host can measure and enforce them.
Stop redundant or superseded assignments through supported controls, confirm
that writing has stopped, inspect partial results, and transfer ownership before
another writer continues. Record remaining work after a limit; budget exhaustion
is not acceptance. Avoid repeated status polling without new information.

## Return decisions to the parent

Return with evidence when the plan contradicts the code, an unplanned public
contract or data change is needed, shared ownership overlaps, or a check reveals
a design question outside the handoff. Stop the failing path after three similar
failed fixes; do not mask that history by replacing the agent.

Resolve safe in-scope decisions in the parent. Refine the work item and return it
to the implementation owner. If an authorized model/effort change is needed, use
the same capability/override process and transfer write ownership before another
agent edits it. Reuse user authority; ask only for a material decision or action
that remains outside it.

## Independent review and acceptance

When independent review is selected and the candidate is stable, give a separate
reviewer the original requirements, relevant plan, diff identity, source/tests,
and raw check artifacts. Let it
challenge the plan's assumptions as well as the code. Do not provide an expected
verdict, tell it the implementation is correct, or use the implementer's running
context as the review context.

Require read-only findings with severity, file/line evidence, concrete impact,
and remaining unknowns. Verify findings in the parent before assigning fixes.
Return fixes to the implementation owner, then recheck the affected tests and
review scope. Apply the existing zero-trust review and completion gates; model
capability does not replace evidence.

## Record what actually happened

Keep a compact dispatch ledger in the plan: work item, expected benefit, bounds,
role, requested model and effort, source of that selection, agent ID, input
identity, ownership, status,
and returned artifacts. Record effective model/effort separately only when the
runtime reports them. A resolver result, echoed prompt, or accepted spawn request
proves the requested configuration, not backend execution identity.

When the host exposes related child session metadata, verify its parent/task
link and compare its recorded model/effort with the spawn request. Record the
source reference and distinguish `requested`, `runtime configuration verified`,
and `provider-reported model` evidence. Child turn-context settings plus response
usage records establish the client's executed configuration; do not claim a
provider response identity when the usage record has no model field. Inspect
only task-related metadata, not unrelated conversations or raw reasoning.

Compare total parent, implementation, review, and rework consumption for similar
tasks when evaluating routing. Keep cumulative and per-response usage separate
to avoid double counting. Record acceptance failures and human intervention as
well as usage; changing a default or completing one smoke case does not prove
better quality or lower total cost. Vary one routing choice at a time when
measuring its effect.

On resume, inspect this ledger and the current checkout before reusing an agent
or a result. Do not reuse a child for a different model/role merely by mentioning
the new settings in a follow-up. Use a supported reconfiguration operation or a
fresh agent, and transfer ownership explicitly. Preserve historical results as
history; invalidate acceptance evidence affected by later edits.
