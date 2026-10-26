---
name: dev-e2e
description: "Write, run, or diagnose Playwright browser tests when end-to-end behavior needs verification."
---

# Dev E2E

Use this skill for Playwright and browser-level testing.

## Workflow

1. Read `../dev-workflow/references/orchestration.md` only when coordinating a multi-step plan or handoff; a focused task can use the matching reference below directly.
2. Read the Playwright E2E section in `../dev-workflow/references/e2e-checkpoint.md`.
3. Confirm tests are not pointed at production systems.
4. Prefer existing project scripts and established Page Object patterns. Call the CLI with `npx --no` so it never fetches Playwright implicitly.
5. Write locators and waits as in `../best-practices/references/testing.md` (section 9): user-facing locators first and auto-waiting assertions, unless the project has an established convention.
6. Do not "fix" an unstable test with waits, skips, or loosened expectations; diagnose the cause from the first failure and its trace.
7. Report failures with test name, file, error, artifact path, and likely cause. Report retry-only passes as flaky, and do not treat a partial, `needs-parent`, or `blocked` delegated run as completion.

## Verification

Use Browser only when local UI inspection is needed and the relevant app target is known or obvious.
