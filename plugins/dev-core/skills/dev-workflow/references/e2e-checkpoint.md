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
2. When a `docs/plans/task-*.md` plan exists, update its completion contract, progress log, decision log, blockers, evidence, and current next action.
3. List completed steps and files changed.
4. Record commands run and results.
5. Capture one exact next action and unresolved decisions.
6. Create `docs/checkpoints/checkpoint-<timestamp>.md` only when no plan exists or the user requests a separate handoff artifact.

Keep one durable source of execution state. Do not create checkpoint files for tiny tasks unless the user asks.
