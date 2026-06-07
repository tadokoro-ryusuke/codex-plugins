---
name: dev-workflow
description: "Codex development workflow orchestration for task planning, TDD execution, systematic debugging, refactoring, code review, E2E testing, checkpointing, and final verification. Use when the user asks to plan a feature, execute a plan, debug a bug, run TDD, refactor, review code, run Playwright E2E, or create a progress checkpoint."
---

# Dev Workflow

Use this skill as the Codex-native replacement for the old Claude slash-command workflows.

## Start Here

1. Classify the user request.
2. Read only the matching reference below.
3. Combine it with `best-practices`, `verification-loop`, `frontend-patterns`, `backend-patterns`, or `codex-collab` when the task needs that expertise.
4. Use Codex tools directly; do not refer to Claude slash commands or Claude agent metadata.

## Workflow Map

| User asks for | Read |
| --- | --- |
| Requirement shaping, BDD scenarios, TDD plan, issue-ready plan | `references/task-planning.md` |
| Execute an existing plan, TDD cycle, Red/Green/Refactor/Commit | `references/tdd-implementation.md` |
| Debug an error, root cause analysis, repeated failed fixes | `references/systematic-debugging.md` |
| Refactor, review, final verification, PR readiness | `references/review-refactor-verify.md` |
| Playwright E2E, checkpoint, resume work | `references/e2e-checkpoint.md` |

## Codex-Specific Rules

- Prefer concrete repository evidence over command-template ceremony.
- Ask for clarification only when missing information makes implementation unsafe.
- Use `update_plan` for multi-step work in this thread when the work is substantial.
- Use parallel subagents only when the user explicitly asks for parallel agent work or second opinions.
- Do not run destructive commands without explicit approval.
- Do not claim a check passed unless you ran it in the current turn and saw passing output.

## Completion Standard

Finish with:

- What changed or what was found.
- Verification commands run and their result.
- Remaining risks or blocked items, if any.

