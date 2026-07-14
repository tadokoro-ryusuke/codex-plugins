# Task Planning

Use this when the user wants to turn an idea into a design plan, implementation plan, BDD scenarios, or a GitHub issue draft.

## Flow

1. Inspect the repository, existing tests, project instructions, and referenced artifacts before asking questions.
2. Separate what remains into verified facts, reversible assumptions, and material decisions:
   - Resolve facts from evidence.
   - State a safe default for reversible assumptions and continue.
   - Ask one question at a time only when a material decision changes scope, architecture, security, irreversible data, external side effects, or product intent. Include a recommended answer and its trade-off.
3. Clarify the task title, goal, background, constraints, scope, and non-goals using that uncertainty gate.
4. Write the user story in this form:

   ```text
   As a [persona],
   I want [capability],
   so that [value].
   ```

5. Define acceptance criteria as a completion contract. Give each criterion an ID, required evidence, and initial status `pending`.
6. Create BDD scenarios covering normal, error, and boundary cases.
7. Draft the design:
   - Relevant layers, modules, routes, APIs, data models, and boundaries.
   - FSD, Clean Architecture, DDD, frontend, or backend implications when relevant.
   - Tradeoffs, assumptions, and decisions that affect implementation.
8. Draft a TDD execution plan:
   - Tidy First preparation.
   - Red/Green/Refactor iterations.
   - Files or modules likely to change.
   - Test strategy.
   - Verification commands.
9. Add durable state: evidence baseline, progress log, decision log, current next action, risks, and stop conditions.
10. Add workspace and delivery strategy. Default commit, push, issue, and PR actions to `not requested` unless explicitly authorized.
11. Save the plan under `docs/plans/task-<slug>.md` by default for task creation or future execution. Keep it inline only when the user asks for a lightweight plan.
12. If GitHub CLI is available and the user wants an issue, create or draft an issue from the plan.

## Canonical Plan Template

Use `../../dev-task/assets/plan-template.md` as the single source of truth for
the plan format. Do not maintain or invent a second embedded template here.

## Quality Bar

- The plan must be specific enough that another Codex thread could execute it.
- Every acceptance criterion must start pending and map to evidence that can prove it satisfied.
- Design notes should be concrete but not speculative. Mark assumptions explicitly.
- The plan should name likely files or modules, not just abstract layers.
- Keep issue creation optional; not every plan needs a GitHub issue.
- Do not ask the user for facts available in the repository, and do not block on a safe reversible choice.
