# Development Orchestration

Use this reference for multi-phase development work. It defines the shared state machine, gates, and stop rules used by the narrower dev-core skills.

## State Machine

Move through these states intentionally:

```text
intake -> plan -> prepare -> implement -> verify -> review -> refactor/fix -> final
```

Not every task needs every state. Small TDD work may skip durable planning; pure review may start at `review`; debugging starts at `intake` then `verify` before `refactor/fix`.

## State Responsibilities

| State | Responsibility | Exit Gate |
| --- | --- | --- |
| `intake` | Understand the user request, repo state, constraints, and risk. | Goal and target are clear enough to act. |
| `plan` | Define scope, non-goals, design notes, acceptance criteria, test strategy, affected areas, and sequencing. | Plan maps behavior to tests or checks. |
| `prepare` | Choose Codex worktree or local branch, inspect dirty state, and identify project commands. | Workspace is safe and commands are known enough to proceed. |
| `implement` | Make the smallest safe change for the current step. | Change is scoped and consistent with the plan. |
| `verify` | Run focused then broader checks with current-turn evidence. | Claims are backed by command output or inspected artifacts. |
| `review` | Challenge the change against behavior, security, tests, architecture, and conventions. | No unresolved P0/P1 findings; lower findings are handled or disclosed. |
| `refactor/fix` | Address verified issues or improve structure without expanding scope. | Regression is resolved and re-verified. |
| `final` | Summarize outcome, evidence, and residual risk. | User can see what happened and what remains. |

## Codex Execution Shape

Use Codex surfaces directly:

- **Skill**: reusable workflow instructions and references.
- **Plan artifact**: `docs/plans/task-<slug>.md` when work should survive into another thread.
- **Worktree**: preferred in the Codex app for background or parallel execution.
- **Local branch**: useful in CLI/local checkout when the repo is clean enough and the user expects implementation work.
- **Review pane or `/review`**: useful UI for inspecting diffs; `dev-review` supplies the stricter dev-core rubric.

Do not copy Claude slash-command or required-subagent mechanics into Codex. Encode them as gates, evidence requirements, and optional second-opinion steps.

## Branch And Worktree Gate

Before code changes:

1. Run `git status --short`.
2. If the thread is already on a Codex worktree, continue there unless the user asks for local handoff.
3. If working locally and the tree is clean, create a branch for execution when the user asked for end-to-end implementation. Prefer repo conventions; otherwise use `codex/<slug>`.
4. If there are unrelated local changes, do not switch branches or overwrite files. Work around them when safe; otherwise stop and ask.
5. If branch creation is blocked by another worktree or policy, continue on the current safe worktree or report the blocker.
6. Commit, push, or open a PR only when the user explicitly requests that delivery.

## Execution Loop

For plan execution, iterate:

```text
read plan -> prepare workspace -> Tidy First -> Red -> Green -> Refactor
  -> focused verify -> review gate -> fix/refactor if needed -> next iteration
  -> broad verify -> final review -> final report
```

The review gate is not a formality. Treat implementation claims as untrusted until the diff, tests, and verification evidence support them.

## Operating Rules

- Use `update_plan` for substantial multi-step work.
- Keep one active phase in focus; avoid doing planning, editing, and review all at once.
- Read `git status --short` before editing and work around unrelated user changes.
- Prefer focused checks first. Broaden only when risk or touched surface requires it.
- Commit only when the user explicitly asks for commits or the current task includes commit/push/PR work.
- Do not claim a check passed without current-turn evidence.
- Stop before destructive actions, ambiguous overwrites, or a fourth similar failed fix attempt.

## Gate Failures

When a gate fails:

1. State which gate failed.
2. Show the evidence.
3. Choose the smallest next action: clarify, fix, re-plan, or stop.
4. Do not proceed silently into the next state.

## Review Gate

For code-producing tasks, run a review pass before final response when the change is non-trivial.

Review at least:

- Behavior correctness and edge cases.
- Test coverage and missing regression tests.
- Security and data exposure.
- Architecture boundaries, including FSD, Clean Architecture, and DDD when relevant.
- Maintainability, naming, complexity, and duplication.
- Project conventions from `AGENTS.md`, README, package scripts, and existing code.

## Final Response Evidence

End with:

- Files or areas changed.
- Verification commands and results.
- Review outcome or unresolved findings.
- Residual risk or follow-up, if any.
