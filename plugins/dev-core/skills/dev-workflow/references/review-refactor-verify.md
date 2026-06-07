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

- Security: injection, authz/authn, secrets, SSRF, unsafe dependencies.
- Quality: SOLID, DRY, complexity, error handling, type safety.
- Project convention: structure, naming, test style, docs, commit shape.

## Verification

Use `verification-loop` for the full check. Adapt commands to the project, but keep the evidence rule:

- Build: compile or bundle.
- Type: TypeScript or language type checks.
- Lint/format: project lint command.
- Test: focused first, then broad enough for risk.
- Security: dependency audit and secret scan where relevant.
- Diff: inspect changed files and unintended churn.

