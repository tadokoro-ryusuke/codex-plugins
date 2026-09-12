---
name: dev-workflow
description: "Coordinate multi-phase development when no narrower dev-core workflow fits."
---

# Dev Workflow

Use this skill as the shared orchestrator for the narrower dev-core entrypoint skills. Prefer a specific skill when the user intent is clear.

## Choose the needed workflow

Use one matching entrypoint or reference. Load orchestration for coordination,
shared ownership, or durable multi-step state; do not add it to a focused review,
diagnosis, or test cycle solely because this skill is available.

| Task | Entrypoint | Supporting guidance |
| --- | --- | --- |
| Coordinate a multi-step plan | `dev-execute` | `references/orchestration.md` |
| Define requirements and acceptance | `dev-task` | `references/task-planning.md` |
| Implement one test-driven behavior | `dev-tdd` | `references/tdd-implementation.md` |
| Investigate a failure | `dev-debug` | `references/systematic-debugging.md` |
| Review or refactor a change | `dev-review` or `dev-refactor` | `references/review-refactor-verify.md` |
| Test browser behavior or capture a handoff | `dev-e2e` or `dev-checkpoint` | Matching section of `references/e2e-checkpoint.md` |

Use `$verification-loop` when selecting completion checks, and `$codex-collab`
when the work benefits from authorized delegation. Load reference skills such as
`$best-practices`, `$frontend-patterns`, or `$backend-patterns` only for decisions
that need those standards; they are not prerequisites for every edit.

## Codex-Specific Rules

- Prefer concrete repository evidence over command-template ceremony.
- Verify facts from the repository first. Continue with a stated reversible default; ask only when missing information changes the requested outcome materially or makes action unsafe.
- Use `update_plan` for substantial multi-step work when that tool is available; otherwise keep progress in the existing plan artifact. Do not invent a tool call or create a second plan just for the UI.
- Use subagents only when the user directly requests them or an applicable `AGENTS.md` or skill explicitly authorizes a bounded delegation. Follow `references/orchestration.md` for the subagent gate.
- Do not run destructive commands without explicit approval.
- Do not claim a check passed unless you ran it in the current turn and saw passing output.

## Completion Standard

Finish with:

- What changed or what was found.
- Verification commands run and their result.
- Remaining risks or blocked items, if any.
