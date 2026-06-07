# Review, Refactor, And Verify

Use this for refactoring, self-review, PR readiness, and final quality checks.

## Refactoring

1. Confirm the target: working tree, PR, branch, commit, file, or directory.
2. Run or inspect existing tests before changing behavior.
3. Prioritize:
   - Critical: security risk, bug, hardcoded secret, broken contract.
   - High: duplicated logic, complex conditionals, oversized functions.
   - Medium: naming, public API clarity, type precision.
   - Low: import ordering, formatting, comments.
4. Preserve external behavior unless the user requested behavior change.
5. Run tests after each meaningful refactor batch.

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
- Tests: meaningful assertions, regression coverage, missing integration or E2E coverage.
- Architecture: FSD, Clean Architecture, DDD, API boundaries, and dependency direction.
- Quality: SOLID, DRY, complexity, error handling, type safety, naming.
- Project convention: structure, naming, test style, docs, commit shape, scripts.
- Delivery: branch scope, PR risk, commit grouping, and whether remaining issues block merge.

### Zero-Trust Review

Do not accept implementation reports at face value:

- If tests are claimed, inspect that tests exist and assert the relevant behavior.
- If typecheck or lint is claimed, still inspect the changed code for unsafe casts, ignored errors, and convention drift.
- If a change is described as "refactor only", inspect the diff for external behavior changes.
- If verification was not run in the current turn, report it as missing evidence.

### Approval Gate

Approve only when:

- no P0/P1 findings remain,
- behavior and test coverage are adequate for the touched surface,
- security-sensitive changes have explicit scrutiny,
- residual risks are disclosed with practical next steps.

## Verification

Use `verification-loop` for the full check. Adapt commands to the project, but keep the evidence rule:

- Build: compile or bundle.
- Type: TypeScript or language type checks.
- Lint/format: project lint command.
- Test: focused first, then broad enough for risk.
- Security: dependency audit and secret scan where relevant.
- Diff: inspect changed files and unintended churn.
