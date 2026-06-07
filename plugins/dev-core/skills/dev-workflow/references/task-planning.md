# Task Planning

Use this when the user wants to turn an idea into a design plan, implementation plan, BDD scenarios, or a GitHub issue draft.

## Flow

1. Clarify the task title, goal, background, constraints, scope, and non-goals.
2. Write the user story in this form:

   ```text
   As a [persona],
   I want [capability],
   so that [value].
   ```

3. Define acceptance criteria as checkable bullets.
4. Create BDD scenarios covering normal, error, and boundary cases.
5. Inspect the codebase enough to identify likely modules, existing tests, and architectural constraints.
6. Draft the design:
   - Relevant layers, modules, routes, APIs, data models, and boundaries.
   - FSD, Clean Architecture, DDD, frontend, or backend implications when relevant.
   - Tradeoffs, assumptions, and decisions that affect implementation.
7. Draft a TDD execution plan:
   - Tidy First preparation.
   - Red/Green/Refactor iterations.
   - Files or modules likely to change.
   - Test strategy.
   - Verification commands.
   - Commit grouping.
8. Add branch, commit, and PR strategy when execution may follow.
9. Save the plan under `docs/plans/task-<slug>.md` by default for task creation or future execution. Keep it inline only when the user asks for a lightweight plan.
10. If GitHub CLI is available and the user wants an issue, create or draft an issue from the plan.

## Plan Template

```markdown
# [Task Title]

## Background

## Scope

## Non-Goals

## User Story

## Acceptance Criteria

## BDD Scenarios

## Codebase Notes

## Design

### Architecture

### Data And API

### UI And UX

## TDD Implementation Plan

### Tidy First

### Iteration 1
- Red:
- Green:
- Refactor:
- Verification:

## Branch, Commit, And PR Strategy

## Risks And Decisions

## Verification

## Execution Checklist
```

## Quality Bar

- The plan must be specific enough that another Codex thread could execute it.
- Every acceptance criterion should map to at least one test or verification step.
- Design notes should be concrete but not speculative. Mark assumptions explicitly.
- The plan should name likely files or modules, not just abstract layers.
- Keep issue creation optional; not every plan needs a GitHub issue.
