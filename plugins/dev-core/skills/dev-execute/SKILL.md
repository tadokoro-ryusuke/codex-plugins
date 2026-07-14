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
4. Use `$verification-loop` for final evidence (its bundled `verify.sh` runs all six steps).
5. For non-trivial changes, use `$codex-collab` for one bounded, read-only independent review when collaboration tools are available. This skill explicitly authorizes that review; do not delegate overlapping write work.

## Execution Contract

- Start by reading the plan and checking `git status --short`. If a legacy plan lacks a completion contract, progress log, decision log, blockers, or a current next action, backfill those sections from its acceptance criteria before changing code and record the migration. Ask only when no observable criterion can be derived safely.
- Choose the workspace path deliberately: stay on a Codex worktree when one is already active; otherwise create a local branch when the tree is clean or its only dirty changes are the target plan and in-scope planning artifacts. Preserve those related files across the switch. Do not switch over unrelated user changes.
- Convert the plan into small implementation steps with `update_plan`.
- Treat the plan's completion contract as default-fail: keep every criterion `pending` until current evidence proves it, then record the evidence and mark it `satisfied`.
- For each step: Red, Green, Refactor, focused verification, and self-review before moving on.
- After every iteration, update the plan's status, progress log, decision log, completion contract, and current next action. Update it again before a pause, handoff, or context compaction.
- Resolve safe, reversible, in-scope concerns yourself. Record non-blocking residual risk and continue. Ask only when a concern requires product judgment, expands scope materially, crosses a security boundary, or causes a destructive, irreversible, or external action.
- After implementation: run broader verification, then a zero-trust review gate.
- If review finds real issues, fix or refactor narrowly and re-run affected checks. Stop after three failed similar rounds.
- Commit, push, or open a PR only when explicitly requested or the current user request includes that delivery.

## Stop Rules

Stop and report when a gate fails, the plan is materially wrong, branch/worktree preparation is unsafe, unrelated user changes block safe editing, the same fix path fails three times, a full cycle produces no meaningful progress, or required evidence cannot be obtained safely.
