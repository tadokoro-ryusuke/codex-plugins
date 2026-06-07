---
name: dev-execute
description: "Execute an existing development plan with branch/worktree preparation, gated TDD, verification, review, refactor/fix loops, and final reporting. Use to implement, continue, resume, or complete docs/plans work."
---

# Dev Execute

Use this skill to implement an existing plan as an end-to-end Codex workflow.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read `../dev-workflow/references/tdd-implementation.md`.
3. Read `../dev-workflow/references/review-refactor-verify.md` before review/finalization.
4. Use `verification-loop` for final evidence.
5. Use `codex-collab` when the user asks for second opinion, rescue, or parallel review.

## Execution Contract

- Start by reading the plan and checking `git status --short`.
- Choose the workspace path deliberately: stay on a Codex worktree when one is already active; otherwise create a local branch only when the repo is clean enough and the task is execution-scoped.
- Convert the plan into small implementation steps with `update_plan`.
- For each step: Red, Green, Refactor, focused verification, and self-review before moving on.
- After implementation: run broader verification, then a zero-trust review gate.
- If review finds real issues, fix or refactor narrowly and re-run affected checks. Stop after three failed similar rounds.
- Commit, push, or open a PR only when explicitly requested or the current user request includes that delivery.

## Stop Rules

Stop and report when a gate fails, the plan is materially wrong, branch/worktree preparation is unsafe, unrelated user changes block safe editing, or the same fix path fails three times.
