---
name: dev-task
description: "Plan development work when requirements, acceptance criteria, or implementation steps need definition."
---

# Dev Task

Use this skill to turn an idea into a durable design-and-implementation plan.

## Workflow

1. Read `../dev-workflow/references/orchestration.md` only when coordinating a multi-step plan or handoff; a focused task can use the matching reference below directly.
2. Read `../dev-workflow/references/task-planning.md`.
3. Invoke `$best-practices` only when an unresolved architecture or convention decision needs its guidance; an ordinary TDD cycle does not require loading another standards reference.
4. Inspect the repo before asking questions. Resolve facts from code, docs, configuration, and safe read-only commands.
5. Classify remaining uncertainty as a verified fact, a reversible assumption, or a material decision. State and use a safe default for reversible assumptions; ask only about material decisions.
6. Ask only the unresolved questions needed to proceed. Include a recommendation and primary trade-off. Use `$dev-grill` only when the user explicitly requests a deeper pressure test.
7. Write a design plan by default for task creation, feature planning, or work that will continue later. Start from `assets/plan-template.md` in this skill directory.
8. Save it under `docs/plans/task-<slug>.md` unless the user only wants a lightweight inline plan.
9. Create or draft a GitHub issue only when the user explicitly asks for it in the current request.
10. For a planning-only request, finish with the plan. If the current request also authorizes implementation, continue into execution without asking for the same approval again.

## Output

Produce a plan with scope, non-goals, design notes, acceptance criteria, BDD scenarios, TDD iterations, verification commands, delivery strategy, risks, and durable execution state. Express every acceptance criterion as a completion contract that starts `pending` and names the evidence required to satisfy it. Keep progress, decisions, and the next action in the plan so `dev-execute` can resume without re-discovering the task.
