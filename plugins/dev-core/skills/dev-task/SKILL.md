---
name: dev-task
description: "Plan feature, bug, or vague development work into acceptance criteria, BDD scenarios, a TDD plan, and optional issue draft. Use for task creation, feature planning, breakdowns, or implementation prep."
---

# Dev Task

Use this skill to turn an idea into a concrete, executable development task.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read `../dev-workflow/references/task-planning.md`.
3. Use `best-practices` when architectural or TDD principles matter.
4. Inspect the repo enough to make the plan concrete.
5. Save a plan under `docs/plans/task-<slug>.md` when the user asks for a durable plan or implementation will continue later.
6. Create or draft a GitHub issue only when the user asks or the repo workflow clearly expects it.

## Output

Produce acceptance criteria, BDD scenarios, a TDD plan, verification commands, and risks. Keep the plan specific enough that `dev-execute` can implement it.
