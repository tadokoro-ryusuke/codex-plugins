# TDD Implementation

Use this when executing a plan or running a standalone TDD cycle.

## Preparation

1. Read the plan or summarize the requested feature.
2. Check `git status --short` and avoid mixing unrelated user changes.
3. Inspect relevant existing tests and implementation files.
4. Identify the package manager and project commands from `package.json`, `AGENTS.md`, Makefiles, or local docs.

## Red/Green/Refactor Loop

For each small behavior:

1. Red: write or update one focused failing test.
2. Run the narrowest relevant test and confirm it fails for the expected reason.
3. Green: implement the smallest change that makes the test pass.
4. Run the narrow test again and confirm it passes.
5. Refactor: improve names, duplication, boundaries, or architecture while tests stay green.
6. Run the narrow test after refactoring.
7. Broaden verification when the behavior touches shared code.

## Commit Discipline

Commit only when the user asked for commits or the workflow explicitly includes them. When committing:

- Stage files by purpose, never with `git add .`.
- Use focused Conventional Commit style messages.
- Keep tests and implementation together when they validate the same behavior.

## Stop Conditions

- Stop and report if the same fix path fails three times.
- Stop before destructive cleanup or overwriting user changes.
- Stop if a test failure reveals ambiguous requirements that cannot be resolved from the codebase.

## Final Report

Include changed files, behavior implemented, tests run, and residual risk.

