---
name: dev-debug
description: "Diagnose and fix software failures when root cause is unclear or a regression needs investigation."
---

# Dev Debug

Use this skill to investigate before fixing.

## Workflow

1. Read `../dev-workflow/references/orchestration.md` only when coordinating a multi-step plan or handoff; a focused task can use the matching reference below directly.
2. Read `../dev-workflow/references/systematic-debugging.md`.
3. Reproduce or inspect the failure before editing when possible.
4. Form independent hypotheses and verify them with evidence.
5. After confirming root cause, use `dev-tdd` style regression-first fixing when practical.
6. Use `continuous-learning` when the failure pattern should become a durable guardrail.

For a useful bounded investigation or fix handoff, this skill authorizes delegation
under `../codex-collab/references/planned-execution.md`. Keep ambiguous root-cause
judgment with the parent; select a bounded implementation preset only after the
cause, behavior and ownership are settled. Do not turn standalone diagnosis into
a mandatory agent chain or change the active parent model.

## Hard Rules

- Do not patch before root cause is identified unless the user explicitly asks for exploratory changes.
- After three failed similar attempts, stop and switch to rescue or ask for direction.
- Final output must distinguish symptoms, evidence, root cause, fix, and verification.
