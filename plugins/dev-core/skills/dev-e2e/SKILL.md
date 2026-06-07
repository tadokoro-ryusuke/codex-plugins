---
name: dev-e2e
description: "Playwright E2E workflow for running, diagnosing, writing, or improving browser tests. Use for E2E tests, Playwright, browser failures, headed/debug runs, and test artifacts."
---

# Dev E2E

Use this skill for Playwright and browser-level testing.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read the Playwright E2E section in `../dev-workflow/references/e2e-checkpoint.md`.
3. Confirm tests are not pointed at production systems.
4. Prefer existing project scripts and established Page Object patterns.
5. Report failures with test name, file, error, artifact path, and likely cause.

## Verification

Use Browser only when local UI inspection is needed and the relevant app target is known or obvious.
