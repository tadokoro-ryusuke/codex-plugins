---
name: dev-refactor
description: "Behavior-preserving refactoring workflow. Use to refactor, clean up, simplify, remove duplication, improve naming, reduce complexity, or prepare code for review."
---

# Dev Refactor

Use this skill for behavior-preserving improvements.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read the Refactoring section in `../dev-workflow/references/review-refactor-verify.md`.
3. Establish current behavior with tests or code inspection.
4. Make small refactor batches.
5. Run focused checks after each meaningful batch.
6. Use `dev-review` criteria before finalizing non-trivial refactors.

## Constraints

- Preserve external behavior unless the user explicitly requests behavior change.
- Do not combine refactoring with broad feature work.
- Stop if tests are absent and behavior cannot be inferred safely.
