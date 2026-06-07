# Development Orchestration

Use this reference for multi-phase development work. It defines the shared state machine, gates, and stop rules used by the narrower dev-core skills.

## State Machine

Move through these states intentionally:

```text
intake -> plan -> implement -> verify -> review -> fix -> final
```

Not every task needs every state. Small TDD work may skip `plan`; pure review may start at `review`; debugging starts at `intake` then `verify` before `fix`.

## State Responsibilities

| State | Responsibility | Exit Gate |
| --- | --- | --- |
| `intake` | Understand the user request, repo state, constraints, and risk. | Goal and target are clear enough to act. |
| `plan` | Define acceptance criteria, test strategy, affected areas, and sequencing. | Plan maps behavior to tests or checks. |
| `implement` | Make the smallest safe change for the current step. | Change is scoped and consistent with the plan. |
| `verify` | Run focused then broader checks with current-turn evidence. | Claims are backed by command output or inspected artifacts. |
| `review` | Challenge the change against behavior, security, tests, architecture, and conventions. | No unresolved P0/P1 findings; lower findings are handled or disclosed. |
| `fix` | Address verified issues without expanding scope. | Regression is resolved and re-verified. |
| `final` | Summarize outcome, evidence, and residual risk. | User can see what happened and what remains. |

## Operating Rules

- Use `update_plan` for substantial multi-step work.
- Keep one active phase in focus; avoid doing planning, editing, and review all at once.
- Read `git status --short` before editing and work around unrelated user changes.
- Prefer focused checks first. Broaden only when risk or touched surface requires it.
- Commit only when the user explicitly asks for commits or the current task includes commit/push work.
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

