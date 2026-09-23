---
name: dev-tdd
description: "Implement one behavior or regression with a test-first Red/Green/Refactor cycle."
---

# Dev TDD

Use this skill so the user can say only the behavior. Do not require them to spell out Red/Green/Refactor.

## Workflow

1. Read `../dev-workflow/references/tdd-implementation.md`.
2. Identify one behavior or regression to drive the cycle.
3. Red: create or update a focused failing test and confirm the expected failure.
4. Green: implement the smallest passing change.
5. Refactor: improve structure while keeping tests green.
6. Run focused verification and broaden checks when shared code changed.

Keep a self-contained cycle with the current owner. If independent work or context
isolation justifies a bounded handoff, this skill authorizes delegation under
`../codex-collab/references/planned-execution.md`; select its preset only after
behavior, ownership and acceptance checks are settled. Preserve the review gate
and explicit/custom settings. Do not spawn a child just to run a test or change
the active parent model to match the profile.

## User-Facing Contract

Accept prompts such as:

```text
Use $dev-tdd to implement password reset validation.
```

The user should not need to mention Red, Green, or Refactor. Apply the cycle automatically.
