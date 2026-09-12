# Planned Execution With Role-Specific Models

Use this contract when `dev-execute` coordinates substantial approved-plan work.
Honor explicit user instructions over these defaults. Keep narrow standalone
tasks outside the full execution workflow. Use the optional research role only
for the bounded information-gathering work described below.

## Resolve roles before dispatch

Read `../assets/execution-profile.json` as the single source of default model and
reasoning settings. The parent recommendation guides task setup; the host owns
the active parent model. Do not pretend to switch it, create a replacement user
task, or infer its effective setting from the recommendation. Record the active
setting only when the host exposes it; otherwise label it unknown.

Check the active parent setting against the recommendation at execution setup.
Report a mismatch once; a profile edit does not change the running task. Use a
supported host setting control only under applicable user authority. If none is
available, explain how the user can select the setting and continue independent
authorized preparation; do not edit internal runtime state to simulate a change.

Use a task-authorized profile path when one is supplied; otherwise use the bundled
profile. Apply an explicit model/effort override for the relevant role when the
user or applicable project instruction requests it. Preserve custom profiles and
explicit selections. Do not install models or change personal configuration as
part of resolution.

### Match the execution shape to the work

Handle a small self-contained change directly when delegation adds more
coordination than useful work, unless explicitly requested otherwise. Do not
spawn a coordinator, implementer, and reviewer merely to edit a simple setting.
Preserve relevant tests and a proportional review; use the separate reviewer
for substantial planned changes under the existing execution gate.

Use the selected profile's implementation default for both ordinary and difficult
planned work. Complexity determines the handoff, scope, and checks; it does not
silently change the model or effort. Establish explicit acceptance criteria,
bounded ownership, and independently verifiable outcomes. Return unplanned public
contract or scope decisions to the parent before implementation.

Use the selected profile's parent recommendation for requirements, design,
integration, and acceptance decisions. For a parent dedicated to executing an
already-settled plan, this workflow permits recommending Astra medium when scope,
design, ownership, and acceptance evidence are specified. Record that selection
and preserve explicit task settings; a recommendation does not change the live
host setting. Reassess when new design or consequential acceptance decisions arise.

Retain the selected profile's independent reviewer for substantial work. Apply
changed role selections only under explicit task/project authority and record
their source in the dispatch ledger. Use original requirements and fresh review
context; a different reviewer model is not itself evidence of independence.

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
and continue preparation that does not depend on dispatch.

Resolve each role from the collaboration skill directory:

```bash
python3 scripts/resolve_execution_role.py --role implementer --capabilities "$capabilities_file"
python3 scripts/resolve_execution_role.py --role reviewer --capabilities "$capabilities_file"
```

Use `--profile` for the selected profile and both `--model` and `--effort` for an
explicit override. Exit `2` means the request cannot be resolved; do not silently
substitute the parent model or launch without the specified effort.

Translate the returned model and reasoning settings into the host's actual spawn
arguments. Use a fresh agent context plus a sufficient handoff. On a host exposing
`fork_turns`, use the returned `none`; full-history forks on that interface inherit
the parent configuration and cannot apply these overrides. Do not invent tool
arguments on other hosts. Recheck capabilities after a host/session change.

The resolver does not launch an agent. Its `write_policy` is an ownership
instruction, not a sandbox setting. Use a read-only sandbox for review when the
host offers one; otherwise report read-only as an instruction-level boundary.

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
4. Acceptance criteria, relevant project commands, and evidence to return.
5. Conditions for returning to the parent rather than guessing or expanding scope.

Tell the agent to implement with TDD and return the changed files, tests and
commands/results, input/output identity, remaining concerns, and one of
`completed`, `needs-parent`, or `blocked`. Let it choose routine implementation
details within the contract. Have it update only its assigned plan section when
that write is explicitly included; keep the overall plan under parent ownership.

Do not let an implementation child recursively invoke the full execution
workflow, spawn another implementation/review chain, commit, or publish under
authority absent from its handoff.

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

Once the candidate is stable, give a separate reviewer the original requirements,
relevant plan, diff identity, source/tests, and raw check artifacts. Let it
challenge the plan's assumptions as well as the code. Do not provide an expected
verdict, tell it the implementation is correct, or use the implementer's running
context as the review context.

Require read-only findings with severity, file/line evidence, concrete impact,
and remaining unknowns. Verify findings in the parent before assigning fixes.
Return fixes to the implementation owner, then recheck the affected tests and
review scope. Apply the existing zero-trust review and completion gates; model
capability does not replace evidence.

## Record what actually happened

Keep a compact dispatch ledger in the plan: work item, role, requested model and
effort, source of that selection, agent ID, input identity, ownership, status,
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
