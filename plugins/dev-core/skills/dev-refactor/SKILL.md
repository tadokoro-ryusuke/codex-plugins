---
name: dev-refactor
description: "Refactor existing code while preserving behavior when structural improvements are requested."
---

# Dev Refactor

Use this skill for behavior-preserving improvements.

## Workflow

1. Read `../dev-workflow/references/orchestration.md` only when coordinating a multi-step plan or handoff; a focused task can use the matching reference below directly.
2. Read the Refactoring section in `../dev-workflow/references/review-refactor-verify.md`.
3. Establish current behavior with tests or code inspection.
4. Make small refactor batches.
5. Run focused checks after each meaningful batch.
6. Use `dev-review` criteria before finalizing non-trivial refactors.

## Constraints

- Preserve external behavior unless the user explicitly requests behavior change.
- Do not combine refactoring with broad feature work.
- Stop if tests are absent and behavior cannot be inferred safely.
