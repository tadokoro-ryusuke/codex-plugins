# Task Planning

Use this when the user wants to turn an idea into an implementation plan, BDD scenarios, or a GitHub issue draft.

## Flow

1. Clarify the task title, goal, background, and constraints.
2. Write the user story in this form:

   ```text
   As a [persona],
   I want [capability],
   so that [value].
   ```

3. Define acceptance criteria as checkable bullets.
4. Create BDD scenarios covering normal, error, and boundary cases.
5. Inspect the codebase enough to identify likely modules, existing tests, and architectural constraints.
6. Draft a TDD plan:
   - Tidy First preparation.
   - Red/Green/Refactor iterations.
   - Files or modules likely to change.
   - Test strategy.
   - Verification commands.
   - Commit grouping.
7. Save the plan under `docs/plans/task-<slug>.md` when the user wants a durable artifact or implementation will continue later.
8. If GitHub CLI is available and the user wants an issue, create or draft an issue from the plan.

## Plan Template

```markdown
# [Task Title]

## Background

## User Story

## Acceptance Criteria

## BDD Scenarios

## Codebase Notes

## TDD Implementation Plan

### Tidy First

### Iteration 1
- Red:
- Green:
- Refactor:
- Verification:

## Risks And Decisions

## Verification
```

## Quality Bar

- The plan must be specific enough that another Codex thread could execute it.
- Every acceptance criterion should map to at least one test or verification step.
- Keep issue creation optional; not every plan needs a GitHub issue.

