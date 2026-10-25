# E2E And Checkpoints

Use this for Playwright E2E work, progress snapshots, and resuming longer tasks.

## Playwright E2E

1. Confirm tests are not pointed at production systems.
2. Resolve Playwright from the project scripts or installed local environment; do not trigger an implicit download to check availability. Use `npx --no` when calling the CLI directly: a bare `npx` may fetch a package without asking in a non-interactive run, and `--no-install` is a deprecated alias. If Playwright is missing, report it instead of fetching it.
3. Prefer existing test commands from `package.json`.
4. Use headed or debug mode only when the user asks or visual diagnosis is needed.
5. Follow established project test patterns; introduce Page Objects only when repeated interactions justify them.
6. Locate elements as in `../../best-practices/references/testing.md` (section 9) unless the project has an established convention: role and accessible name first, test ids only as an agreed contract. Use the Locator API and auto-waiting assertions; Playwright discourages selector-string calls such as `page.fill(selector, ...)` and `page.click(selector)`. Never add fixed sleeps.
7. Report failures with test name, file, error, artifact path, and likely cause. Quote counts only from the actual run output, and report tests that passed only on retry as flaky.

Examples for a project with Playwright already installed; adapt to its package manager:

```bash
npx --no playwright test
npx --no playwright test tests/auth/
npx --no playwright test --headed
npx --no playwright show-report
npx --no playwright show-trace <trace.zip>
```

```typescript
// pages/LoginPage.ts
import { expect, type Page } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
    await expect(this.page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  }
}
```

### Unstable tests

Do not call a flaky test fixed after adding waits, skipping it, or loosening its
expectation. Keep the first failure (logs and trace), find the cause (waiting,
order dependence, shared state, time, external dependency), and fix that. If the
cause cannot be fixed, report what you tried; quarantine follows `$test-design`.

### Delegated runs

A delegated E2E run returns `completed`, `needs-parent`, or `blocked` with the
commands and raw results. It does not spawn other agents, commit, or publish.
Do not treat a partial result, `needs-parent`, or `blocked` as completion: provide
what is missing and rerun, or report the gap.

## Checkpoints

Use checkpoints when work is long, interrupted, or needs handoff:

1. Summarize current goal.
2. When a `docs/plans/task-*.md` plan exists, update its completion contract, progress log, decision log, blockers, evidence, and current next action.
3. List completed steps and files changed.
4. Record commands run and results.
5. Capture one exact next action and unresolved decisions.
6. Create `docs/checkpoints/checkpoint-<timestamp>.md` only when no plan exists or the user requests a separate handoff artifact.

Keep one durable source of execution state. Do not create checkpoint files for tiny tasks unless the user asks.
