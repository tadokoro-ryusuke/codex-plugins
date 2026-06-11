# Task: <title>

- Status: draft | approved | in-progress | done
- Plan file: docs/plans/task-<slug>.md
- Related issue/PR: <link or "none">

## Scope

What this task delivers, in one or two sentences.

## Non-Goals

What is deliberately out of scope.

## Design Notes

Key decisions, affected modules, data flow, and why this approach. Reference
concrete files (path:line) discovered while inspecting the repo.

## Acceptance Criteria

- [ ] Observable, testable outcome 1
- [ ] Observable, testable outcome 2

## BDD Scenarios

```gherkin
Scenario: <name>
  Given <precondition>
  When <action>
  Then <observable result>
```

## TDD Iterations

1. <behavior 1> — test file: <path>
2. <behavior 2> — test file: <path>

Each iteration is one Red → Green → Refactor → Commit cycle.

## Verification Commands

```bash
# the project's actual commands (build, typecheck, lint, test, e2e)
```

## Branch / Commit Strategy

- Branch: <name>
- Commit granularity: one commit per TDD iteration unless noted.

## Risks

- <risk> — mitigation: <plan>
