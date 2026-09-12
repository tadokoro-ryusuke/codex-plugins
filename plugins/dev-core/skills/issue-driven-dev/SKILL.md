---
name: issue-driven-dev
description: "Issue and review workflow design for human and agent teams. Use when drafting work orders, splitting issues, or maintaining their decision and PR traceability."
---

# Issue-Driven Development

Make the reason for work, observable completion conditions, and decision history
traceable. Use the existing issue or authorized task as the work order; this skill
does not require creating an external issue or opening a PR for every local edit.

Reuse the user's accepted scope, priorities, and acceptance criteria. An agent may
draft precise criteria from an unambiguous request and prepare the work; reserve
material product, contract, and release-risk changes for the authorized owner.
Do not treat an already approved task as needing fresh approval simply because
its decisions are being transferred into a template.

## Prepare a usable work order

State the problem and expected behavior, verifiable completion conditions, and
scope boundaries that prevent likely confusion. For bugs, include reproduction,
environment, and observed evidence. Scale the format to the task; a clear one-line
completion condition is enough for a trivial edit.

Split substantial work into cohesive, reviewable outcomes with minimal dependencies.
Prefer vertical slices when they deliver independently verifiable value. Do not
force a one-issue/one-PR ratio when the repository needs a different traceable shape.
Delegate bounded work with the relevant raw context and acceptance criteria; verify
agent claims against files and actual execution evidence.

## Load only the relevant operating detail

- For GitHub Issue Forms or concrete ticket examples, read
  [issue templates](references/issue-driven-dev.md).
- For labels, triage, branches, or PR review policy, read
  [issue and review operations](references/issue-and-review-operations.md).
- For ADRs, design docs, or current operating documentation, read
  [decision records](references/decision-records.md).

Use `$test-design` when acceptance criteria need test-design work,
`$verification-loop` for implementation evidence, and `$cicd-release-design` for
release gates. Do not load them solely because the ticket mentions tests or CI.

## Complete the authorized work cycle

Report which completion conditions are met with evidence, and which remain open.
Keep decisions linked to their work order; prepare comment or PR text locally when
posting is not authorized. Create, post, commit, merge, deploy, or notify only within
existing user authorization and repository protections.

Use closing keywords such as `Fixes #N` only when the PR actually completes the
issue and auto-closure is intended. Verify remote issue or merge state before
claiming it; a prepared body or local commit is not evidence of delivery.
