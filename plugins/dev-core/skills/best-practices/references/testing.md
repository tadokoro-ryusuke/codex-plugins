# Writing tests

Read this before writing, fixing, or reviewing tests. It covers how to write a
test; judging test quality and allocating coverage belong to `$test-design`.
Where the project's established conventions or `AGENTS.md` differ, follow them.

## 1. Structure and names

- Use Arrange-Act-Assert (or Given-When-Then).
- Name a test as the behavior it checks, so a failure points at the cause
  (for example, "returns 401 for an expired token").
- One behavior per test. Split a long test that alternates actions and assertions
  at its first assertion. A long test that fails turns locating the broken behavior
  into a separate investigation (Kent Beck, "Decompose run-on tests").

## 2. Name what breaks it

Before writing the body, name the production change that would make this test
fail. If you cannot, redesign the test to observe behavior. A test with no
nameable failure reason does not detect regressions.

## 3. Expected values

- Derive expected values from literals, hand-checked fixtures, or the specification.
  Do not import production code, its helpers, or its constants to compute them;
  an expected value computed from the implementation agrees with it even when the
  implementation is wrong (a tautological assertion).
- Give an unexplained number a named constant inside the test or a comment that
  states where it comes from.
- In property-based tests, do not let the model reimplement the logic under test;
  it would share the same mistakes.

## 4. Avoid change-detector tests

- Do not write tests that only pin a constant's value, wording, or private
  structure; test the behavior that depends on that decision.
- Run scripts and configuration and check their output, side effects, and exit
  code instead of grepping their text. A string match passes when behavior breaks
  and fails on harmless rewording.

## 5. Test double priority

Default to real > fake > stub > mock.

- Verify interactions with a mock only for unmanaged dependencies with externally
  observable side effects, such as sending email or calling a payment API.
- Verify read-only dependencies through the result that uses their return value.
  Do not make "the mock was called" the purpose of an assertion unless the
  arguments, count, or order are part of the contract.
- Make mock responses mirror the real data shape without dropping fields.
- When mock setup grows, consider dependency inversion or an integration test with
  the real component.
- Excess mocking does not verify real interactions. An empirical study found that
  coding-agent commits added mocks to tests more often than human commits
  ([arXiv 2602.00409](https://arxiv.org/abs/2602.00409), 2026-01; checked 2026-10-26).

## 6. Integration-test your own database and broker for real

- Use the real database or message broker the project owns by default
  (Testcontainers, a CI service container, a disposable database).
- Use an in-memory substitute only when you have established that its differences
  from production do not matter. If you build a fake, run the same contract tests
  against both the fake and the real dependency.
- Where Docker or similar is unavailable, do not swap in mocks to get a green
  result. Report that integration test as not run and leave it to CI
  (`$verification-loop` handles unexecuted checks).
- In-memory substitutes do not reproduce constraints, transactions, or dialect
  differences, so the defect first appears in production.

## 7. Test data

- Build data per test with factories or builders; avoid shared mutable fixtures.
- Isolate tests with transaction rollback, per-schema isolation, or truncation.
  Rollback isolation does not work when the code under test opens its own
  transactions or uses several connections.
- Do not use production data in tests.

## 8. Confirm Red

- In Red, confirm from the failure message that the test failed for the expected
  reason. A failure from setup, imports, or syntax does not count as Red.
- Do not write a test afterwards that merely ratifies the implementation.
- Do not make a failing test pass by weakening it without a specification change
  or an approved quarantine that meets `$test-design`'s conditions (see "Never
  weaken a test to pass" in `../SKILL.md`).

## 9. E2E locators

Follow Playwright's guidance and locate elements by user-visible attributes,
unless the project has an established convention:

1. `getByRole` (role and accessible name)
2. `getByLabel` / `getByPlaceholder` / `getByText` and other user-visible attributes
3. `getByTestId`, as a test contract the team has explicitly agreed on
4. CSS / XPath, as a last resort

Role-and-name locators survive visual changes and expose accessibility defects
such as an unnamed button. Wait with auto-waiting assertions
(`await expect(locator).toBeVisible()`), never a fixed sleep.
Source: https://playwright.dev/docs/locators (checked 2026-10-26).
