---
name: dev-refactor
description: "Refactor existing code while preserving behavior when structural improvements are requested."
---

# Dev Refactor

Use this skill for behavior-preserving improvements.

## Workflow

1. Read `../dev-workflow/references/orchestration.md` only when coordinating a multi-step plan or handoff; a focused task can use the matching reference below directly.
2. Read the Refactoring section in `../dev-workflow/references/review-refactor-verify.md`.
3. Establish current behavior with tests. Where tests are thin, pin the behavior
   you will touch with characterization tests before changing code.
4. Make small refactor batches.
5. Run focused checks after each meaningful batch.
6. Use `dev-review` criteria before finalizing non-trivial refactors.
7. Before claiming completion or committing, meet the full-suite completion gate in `../verification-loop/SKILL.md`.

## Constraints

- Preserve external behavior unless the user explicitly requests behavior change.
  Report bugs, security problems, and React data-fetching effects you find instead
  of fixing them here; each changes behavior and needs its own change that starts
  from a failing test (`$dev-debug` or `$dev-tdd`).
- If a characterization test diverges from its recorded value, do not update the
  expectation: revert the batch, or stop and report the behavior change.
- Keep visual design (styles, class names, design tokens, layout) out of scope;
  do not invoke generative design skills. Split visual work into a separate request.
- Do not combine refactoring with broad feature work.
- Stop if tests are absent and behavior cannot be inferred safely.
