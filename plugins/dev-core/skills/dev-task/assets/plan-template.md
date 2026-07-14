# Task: <title>

- Status: draft | approved | in-progress | blocked | done
- Plan file: docs/plans/task-<slug>.md
- Related issue/PR: <link or "none">
- Last updated: <ISO-8601 timestamp>

## Goal

What this task delivers and why it matters, in one or two sentences.

## Scope

What is included.

## Non-Goals

What is deliberately out of scope.

## Evidence Baseline

- Repository state inspected: <commands or files>
- Existing behavior verified: <command and result, or "not yet verified">

## Facts, Assumptions, And Decisions Needed

### Verified Facts

- <fact> — evidence: <path, command, or source>

### Reversible Assumptions

- <assumption> — default: <choice> — rollback: <how to change it>

### Material Decisions

- <decision or "none"> — owner: <user/Codex> — status: open | decided

## Design Notes

Record key decisions, affected modules, data flow, and why this approach fits.
Reference concrete files (`path:line`) discovered while inspecting the repo.

## Completion Contract

Every row starts `pending`. Change a row to `satisfied` only after opening or
running the named evidence in the current execution context.

| ID | Observable criterion | Required evidence | Evidence observed | Status |
| --- | --- | --- | --- | --- |
| AC-1 | <testable outcome> | <test, command, or inspected artifact> | not yet observed | pending |
| AC-2 | <testable outcome> | <test, command, or inspected artifact> | not yet observed | pending |

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

Each code-behavior iteration is one Red → Green → Refactor → focused verify
cycle. Commit only when the user explicitly requests commits.

## Verification Commands

```bash
# Project commands for build, typecheck, lint, test, security, and diff review.
```

## Delivery Strategy

- Workspace: existing worktree | branch <name> | current safe checkout
- Commit: not requested | requested with <granularity>
- Push/PR: not requested | requested with <target>

## Risks And Stop Conditions

- <risk> — mitigation: <plan>
- Stop on: destructive or external action without authority; three similar
  failed attempts; a no-progress cycle; evidence that contradicts the plan.

## Progress Log

- <timestamp> — <step> — <result and evidence>

## Decision Log

- <timestamp> — <decision> — <rationale and source>

## Blockers And Open Questions

- <blocker or open question, owner, and evidence needed; or "none">

## Current Next Action

<One exact file, command, or decision that a fresh thread should take next.>
