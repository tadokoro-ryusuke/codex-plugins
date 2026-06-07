---
name: dev-review
description: "Dev-core code review for working trees, branches, PRs, plans, or files. Use for review, PR review, second opinion, risk assessment, security, tests, architecture, and maintainability."
---

# Dev Review

Use this skill when the user wants dev-core review criteria, not just a generic review.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read the Code Review section in `../dev-workflow/references/review-refactor-verify.md`.
3. Gather the target: working tree, branch, PR, file, plan, or diff.
4. Review independently. Do not trust prior implementation claims.
5. Lead with findings, ordered by severity, with file references.

## Review Criteria

Check at least:

- Behavior correctness, edge cases, and regression risk.
- Security: auth, input validation, injection, secrets, unsafe dependencies.
- Test coverage: missing unit, integration, E2E, or regression tests.
- Architecture: FSD, Clean Architecture, DDD boundaries when relevant.
- Maintainability: naming, complexity, duplication, type safety, error handling.
- Project conventions from `AGENTS.md`, README, CI, package scripts, and surrounding code.

## Built-In Review

The built-in `/review` command is fine for generic review. Use `dev-review` when the dev-core rubric must be applied consistently.
