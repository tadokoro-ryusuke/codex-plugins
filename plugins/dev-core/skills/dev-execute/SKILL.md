---
name: dev-execute
description: "Execute an existing development plan with gated TDD, verification, review, and final reporting. Use to implement, continue, resume, or complete docs/plans work."
---

# Dev Execute

Use this skill to implement an existing plan with explicit phase gates.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read `../dev-workflow/references/tdd-implementation.md`.
3. Read `../dev-workflow/references/review-refactor-verify.md` before review/finalization.
4. Use `verification-loop` for final evidence.
5. Use `codex-collab` when the user asks for second opinion, rescue, or parallel review.

## Execution Contract

- Start by reading the plan and checking `git status --short`.
- Convert the plan into small implementation steps with `update_plan`.
- For each step: write or adjust tests, implement narrowly, run focused checks, then proceed.
- Run a review gate before final response for non-trivial changes.
- Commit only when explicitly requested.

## Stop Rules

Stop and report when a gate fails, the plan is materially wrong, unrelated user changes block safe editing, or the same fix path fails three times.
