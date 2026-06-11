---
name: dev-workflow
description: "Shared dev-core orchestration for multi-phase coding work. Use for phase gates, planning, implementation, verification, review, debugging, handoff, or fallback when no narrower dev-* skill applies."
---

# Dev Workflow

Use this skill as the shared orchestrator for the narrower dev-core entrypoint skills. Prefer a specific skill when the user intent is clear.

## Start Here

1. Classify the user request.
2. Read `references/orchestration.md` for any multi-phase task.
3. Read only the matching workflow reference below.
4. Combine it with `$verification-loop` or `$codex-collab` when the task needs that workflow. Load the reference skills `$best-practices`, `$frontend-patterns`, or `$backend-patterns` explicitly when their standards matter — they are not injected implicitly.

## Workflow Map

| User asks for | Read |
| --- | --- |
| Multi-phase implementation, phase gates, handoff, state tracking | `references/orchestration.md` |
| Requirement shaping, BDD scenarios, TDD plan, issue-ready plan | `references/task-planning.md` |
| Execute an existing plan, TDD cycle, Red/Green/Refactor/Commit | `references/tdd-implementation.md` |
| Debug an error, root cause analysis, repeated failed fixes | `references/systematic-debugging.md` |
| Refactor, review, final verification, PR readiness | `references/review-refactor-verify.md` |
| Playwright E2E, checkpoint, resume work | `references/e2e-checkpoint.md` |

## Narrow Entrypoints

- Use `dev-task` for task planning.
- Use `dev-execute` for executing a plan.
- Use `dev-debug` for root-cause debugging.
- Use `dev-tdd` for a standalone TDD cycle.
- Use `dev-review` for a dev-core code review.
- Use `dev-refactor` for behavior-preserving refactoring.
- Use `dev-e2e` for Playwright E2E work.
- Use `dev-checkpoint` for resumable handoff notes.

## Codex-Specific Rules

- Prefer concrete repository evidence over command-template ceremony.
- Ask for clarification only when missing information makes implementation unsafe.
- Use `update_plan` for multi-step work in this thread when the work is substantial.
- Use parallel subagents only when the user explicitly asks for parallel agent work, delegation, or second opinions. Follow `references/orchestration.md` for the subagent gate.
- Do not run destructive commands without explicit approval.
- Do not claim a check passed unless you ran it in the current turn and saw passing output.

## Completion Standard

Finish with:

- What changed or what was found.
- Verification commands run and their result.
- Remaining risks or blocked items, if any.
