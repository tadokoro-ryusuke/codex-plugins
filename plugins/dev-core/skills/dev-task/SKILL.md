---
name: dev-task
description: "Plan feature, bug, or vague development work into a design plan, acceptance criteria, BDD scenarios, TDD iterations, and optional issue draft. Use for task creation, feature planning, breakdowns, or implementation prep."
---

# Dev Task

Use this skill to turn an idea into a durable design-and-implementation plan.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read `../dev-workflow/references/task-planning.md`.
3. Invoke `$best-practices` when architectural or TDD principles matter (it is not loaded implicitly).
4. Inspect the repo enough to make the plan concrete.
5. Write a design plan by default for task creation, feature planning, or work that will continue later. Start from `assets/plan-template.md` in this skill directory.
6. Save it under `docs/plans/task-<slug>.md` unless the user only wants a lightweight inline plan.
7. Create or draft a GitHub issue only when the user asks or the repo workflow clearly expects it.
8. Do not start implementation unless the user asks to continue into execution.

## Output

Produce a plan with scope, non-goals, design notes, acceptance criteria, BDD scenarios, TDD iterations, verification commands, branch/commit strategy, and risks. Keep it specific enough that `dev-execute` can implement it without re-discovering the task.
