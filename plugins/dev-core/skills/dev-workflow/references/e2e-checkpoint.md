# E2E And Checkpoints

Use this for Playwright E2E work, progress snapshots, and resuming longer tasks.

## Playwright E2E

1. Confirm tests are not pointed at production systems.
2. Check Playwright availability with `npx playwright --version` or project docs.
3. Prefer existing test commands from `package.json`.
4. Use headed or debug mode only when the user asks or visual diagnosis is needed.
5. For new tests, prefer Page Object Model or established project patterns.
6. Report failures with test name, file, error, artifact path, and likely cause.

Common commands:

```bash
npx playwright test
npx playwright test tests/auth/
npx playwright test --headed
npx playwright show-report
```

## Checkpoints

Use checkpoints when work is long, interrupted, or needs handoff:

1. Summarize current goal.
2. List completed steps and files changed.
3. Record commands run and results.
4. Capture next actions and unresolved decisions.
5. Save under `docs/checkpoints/checkpoint-<timestamp>.md` when the user wants a durable file.

Do not create checkpoint files for tiny tasks unless the user asks.

