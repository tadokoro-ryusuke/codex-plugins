# Development Orchestration

Use this reference when coordinating multi-step development, shared ownership,
or work that needs durable state. Use the narrower workflow directly for a
focused review, diagnosis, or test cycle.

## Scope and completion

Define the observable outcome and required evidence before substantial work.
Use the phases that the task needs: plan, prepare, implement, verify, review,
fix, and finish. A phase describes responsibility, not a mandatory ceremony.
Read only the project instructions and artifacts needed for the changed contract.

Continue authorized work through verification, requested runtime inspection,
and repair of verified in-scope problems. A first implementation or a passing
unit test does not end a task whose acceptance criteria require more. Once the
criteria and applicable gates are satisfied, report the result; do not expand
into unrelated redesign or repeat passing checks without a new reason.

Use `docs/plans/task-<slug>.md` when the work has dependent steps, shared contracts,
migrations, or future handoff. For a focused change, an acceptance criterion,
appropriate check, and diff review can be sufficient. Use `update_plan` if
available and useful; its absence is not a blocker or a reason for a second plan.

## Workspace and delivery

- Check `git status --short` before edits or workspace changes. Preserve unrelated
  changes and use the current Codex worktree when one is active.
- For end-to-end implementation in a clean local checkout, create an execution
  branch using repository conventions or `codex/<slug>`. Related planning files
  can be carried onto it. Work around unrelated dirt without switching over it;
  ask only if it cannot be safely preserved.
- If workspace preparation is blocked, continue independent work on a safe
  checkout and disclose the affected limitation.
- Commit, push, create issues, or open a PR only when the user authorized that
  delivery. Reuse authorization already present in the current request.

## Delegation and ownership

Use bounded delegation when the user or applicable instructions authorize it
and it adds useful parallel work or independent judgment. Avoid delegation whose
coordination overhead exceeds its benefit, overlapping writers, and assignments
that block all useful parent work.

For substantial planned execution, use the role profile and handoff contract in
`../../codex-collab/references/planned-execution.md`. That workflow authorizes
implementation and independent review roles with specific models. For other
work, inherit the configured model unless an applicable instruction selects an
override. A child performs its assigned role without restarting the parent
orchestration or spawning another execution chain.

Give each assignment its goal, raw input paths, allowed writes, dependencies,
acceptance evidence, and return conditions. Supply only task-relevant context;
give reviewers requirements and raw artifacts without a preferred verdict.
Continue independent work while the child runs, then inspect its actual diff,
checks, and findings before relying on its report.

Use the host's real tools and concurrency limits. Worktrees isolate files, not
databases, ports, deployments, or credentials; coordinate shared resources.
Create or fork a user-owned task only when the user requests that operation.

## Durable state and resume

Keep one source of execution state in the existing plan. If an older plan lacks
a completion contract or next action, derive them from its acceptance criteria
and record the migration. Ask only if no safe observable outcome can be derived.

- Start acceptance criteria `pending`; mark them `satisfied` only after inspecting
  evidence for the current inputs.
- Update progress, decisions, blockers, evidence, and the next action after
  meaningful iterations and before handoff or compaction. Do not copy unchanged
  logs into every update.
- On resume, recheck branch, HEAD, working diff, relevant inputs, and available
  tools. Keep old results as history and invalidate affected evidence after
  code, fixtures, dependencies, or configuration change.
- Record commands, working directory, input identity, outcomes, and useful
  artifact paths. Distinguish source, local runtime, device, and deployed
  evidence; keep secrets and customer data out of durable records.

## Verification and review

Keep project-required checks and test-first development for executable behavior.
Use `../../verification-loop/SKILL.md` when choosing checks, and the matching
section of `review-refactor-verify.md` for review or refactoring. Run focused
checks and broaden when changed shared contracts or unresolved risks justify it.

For non-trivial changes, review before completion. For substantial planned work,
obtain the independent review specified by the execution contract. Verify
findings against the actual inputs; resolve P0/P1 findings and fix or disclose
remaining concerns. Re-run affected checks after a fix; invalidate relevant
review evidence when the reviewed inputs change.

## Decision and stop boundaries

Resolve available facts from the environment. State safe reversible assumptions
and continue in scope. Reuse existing authorization; ask only for an unresolved
material decision or action outside that authority. Prepare the concrete
reviewable artifact before an approval question and explain any explicit rule
or tool rejection causing the stop.

Stop the affected path before destructive or unauthorized actions, unsafe
workspace changes, or a fourth similar failed fix attempt. If a cycle produces
no new evidence, reassess the approach instead of repeating it. Re-plan when
evidence contradicts the design and continue independent safe work.

Finish with the outcome, current verification and review evidence, and any
remaining blocker or limitation. Never claim a check passed without inspecting
its output in the current turn.
