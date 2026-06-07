# TDD Implementation

Use this when executing a plan or running a standalone TDD cycle.

## Preparation And Workspace Gate

1. Read the plan or summarize the requested feature.
2. Check `git status --short` and avoid mixing unrelated user changes.
3. Decide where to work:
   - Continue on the current Codex worktree when one is active.
   - In a clean local checkout, create a branch for end-to-end execution when appropriate. Prefer repo convention; otherwise use `codex/<slug>`.
   - If unrelated changes exist, work around them only when safe. Stop before branch switches or edits that would overwrite them.
4. Inspect relevant existing tests and implementation files.
5. Identify the package manager and project commands from `package.json`, `AGENTS.md`, Makefiles, or local docs.
6. Convert the plan into small steps with `update_plan`.

## Tidy First

Do narrow preparation before feature code only when it reduces risk for the next TDD step:

- clarify names,
- isolate dependencies,
- add missing test seams,
- remove obvious duplication in the touched area.

Keep Tidy First behavior-preserving and verify it before starting Red.

## Red/Green/Refactor Loop

For each small behavior or plan iteration:

1. Red: write or update one focused failing test.
2. Run the narrowest relevant test and confirm it fails for the expected reason.
3. Green: implement the smallest change that makes the test pass.
4. Run the narrow test again and confirm it passes.
5. Refactor: improve names, duplication, boundaries, or architecture while tests stay green.
6. Run the narrow test after refactoring.
7. Run a focused self-review of the diff for that iteration.
8. Broaden verification when the behavior touches shared code.

## Iteration Status

After each iteration, classify the result:

| Status | Meaning | Next Action |
| --- | --- | --- |
| `COMPLETED` | Tests and focused checks pass with no material concerns. | Continue to the next iteration. |
| `COMPLETED_WITH_CONCERNS` | Checks pass but risk remains, such as weak coverage or ambiguous requirements. | Report the concern and either address it or ask before continuing. |
| `BLOCKED` | The plan conflicts with the codebase, tests cannot be written safely, or the same fix path failed three times. | Stop and report the blocker, attempts, and needed decision. |

Never ignore a blocked or concerning status just to keep the loop moving.

## Review And Refactor Gate

After all planned iterations:

1. Run focused and broad-enough verification with current-turn evidence.
2. Review the diff using `dev-review` criteria. Treat earlier implementation claims as untrusted.
3. If the review finds issues, fix or refactor narrowly.
4. Re-run affected checks after each fix/refactor round.
5. Stop after three similar failed rounds and report the remaining risk.

## Commit Discipline

Commit only when the user asked for commits or the workflow explicitly includes them. When committing:

- Stage files by purpose, never with `git add .`.
- Use focused Conventional Commit style messages.
- Keep tests and implementation together when they validate the same behavior.
- Push or create a PR only when the user asks for that delivery.

## Stop Conditions

- Stop and report if the same fix path fails three times.
- Stop before destructive cleanup or overwriting user changes.
- Stop if a test failure reveals ambiguous requirements that cannot be resolved from the codebase.

## Final Report

Include changed files, behavior implemented, tests run, and residual risk.
