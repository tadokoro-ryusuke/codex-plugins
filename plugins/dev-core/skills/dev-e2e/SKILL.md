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
4. Prefer existing project scripts and established Page Object patterns.
5. Report failures with test name, file, error, artifact path, and likely cause.

## Verification

Use Browser only when local UI inspection is needed and the relevant app target is known or obvious.
