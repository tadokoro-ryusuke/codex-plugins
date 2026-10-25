# Review, Refactor, And Verify

Use this for refactoring, self-review, PR readiness, and final quality checks.

## Refactoring

1. Confirm the target: working tree, PR, branch, commit, file, or directory.
   - A working-tree target includes staged, unstaged, and untracked files.
   - For a PR, stop if the current branch is not the PR's head branch; do not
     switch branches over uncommitted changes, and leave the switch to the user.
   - If the target resolves to none of these, stop and report it instead of
     guessing, for example, recent commits.
2. Run existing tests and confirm they are green before changing code. If no test
   covers a behavior you will change, pin it first with a characterization test
   that records the current output (an approval test for large or structured
   output). The recorded value is current behavior, not the specification; list
   replacing it with intentional assertions as follow-up work.
3. Prioritize by concrete impact, likelihood, and the changed contract. Treat
   duplication, conditionals, size, naming, and formatting as investigation
   signals. Report a finding only when it causes an identifiable problem or
   violates an enforced repository rule; do not assign severity from size alone.
4. Preserve external behavior unless the user requested behavior change. Report,
   rather than fix, bugs, security problems, and changes that alter loading,
   fetch timing, or caching (such as replacing a React data-fetching effect); each
   needs its own change that starts from a failing test. Extract constants only
   when defaults stay unchanged.
5. Run tests after each meaningful refactor batch. If a pinned value diverges,
   revert the batch or stop and report the behavior change; never rewrite the
   expectation to match.
6. When delivery is authorized, push only the current branch, never the default
   branch.

## Code Review

Lead with findings:

```text
Findings
- [P1] path:line - issue, impact, and suggested fix.

Open Questions
- ...

Verification
- ...
```

Review axes:

- Behavior: correctness, edge cases, regression risk, and external contract changes.
- Security: injection, authz/authn, secrets, SSRF, unsafe dependencies.
- Tests: meaningful assertions, regression coverage, missing integration or E2E
  coverage, expected values derived independently of the implementation, and
  test doubles per `../../best-practices/references/testing.md`.
- Architecture: FSD, Clean Architecture, DDD, API boundaries, and dependency direction.
- Quality: SOLID, DRY, complexity, error handling, type safety, naming.
- Project convention: structure, naming, test style, docs, commit shape, scripts.
- Delivery: branch scope, PR risk, commit grouping, and whether remaining issues block merge.

### Zero-Trust Review

Do not accept implementation reports at face value:

- If tests are claimed, inspect that tests exist and assert the relevant behavior.
- If passing tests are claimed, inspect the diff for deleted, skipped, or focused
  tests, loosened expected values, and implementation special-casing of test
  inputs. Accept such a change only with a specification basis; without one, do
  not count the pass as evidence and report it as a finding.
- If typecheck or lint is claimed, still inspect the changed code for unsafe casts, ignored errors, and convention drift.
- If a change is described as "refactor only", inspect the diff for external behavior changes.
- Inspect the check artifacts and their input/environment identity. Apply the
  reuse rules in `../../verification-loop/SKILL.md`; label prior results as reused,
  and report missing or stale evidence instead of assuming success.

### Approval Gate

Approve only when:

- no P0/P1 findings remain,
- behavior and test coverage are adequate for the touched surface,
- security-sensitive changes have explicit scrutiny,
- residual risks are disclosed with practical next steps.

## Verification

Use `verification-loop` to choose applicable checks. Keep required project gates,
and run additional checks only when the changed contract or unresolved risk
justifies them. Once sufficient checks pass, finish the authorized work; do not
repeat a suite without a relevant change or new failure. Consider:

- Build: compile or bundle.
- Type: TypeScript or language type checks.
- Lint/format: project lint command.
- Test: focused first, then broad enough for risk.
- Security: dependency audit and secret scan where relevant.
- Diff: inspect changed files and unintended churn.
