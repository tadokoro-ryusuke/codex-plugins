---
name: dev-debug
description: "Diagnose and fix software failures when root cause is unclear or a regression needs investigation."
---

# Dev Debug

Use this skill to investigate before fixing.

## Workflow

1. Read `../dev-workflow/references/orchestration.md` only when coordinating a multi-step plan or handoff; a focused task can use the matching reference below directly.
2. Read `../dev-workflow/references/systematic-debugging.md`.
3. Build a reproduction command for the symptom and run it until its output shows
   the failure (red). If it cannot be reproduced, list what you tried and stop to
   ask for access, redacted logs, or instrumentation permission.
4. Form competing hypotheses with falsifiable predictions and verify them with evidence.
5. After confirming root cause, use `dev-tdd` style regression-first fixing when the
   fix is in scope; for a diagnosis-only request, report the cause and fix plan.
6. Use `continuous-learning` when the failure pattern should become a durable guardrail.

For a useful bounded investigation or fix handoff, this skill authorizes delegation
under `../codex-collab/references/planned-execution.md`. Keep ambiguous root-cause
judgment with the parent; select a bounded implementation preset only after the
cause, behavior and ownership are settled. Do not turn standalone diagnosis into
a mandatory agent chain or change the active parent model.

## Hard Rules

- Do not patch before root cause is identified unless the user explicitly asks for exploratory changes.
- Do not make a failing test pass by skipping, deleting, or loosening it without a specification change; see `../best-practices/SKILL.md`.
- After three failed similar attempts, stop that path and report the attempts, why each failed, and a recommendation. Switch to the in-session rescue diagnosis or ask for direction; hand rescue to another agent or model only with user consent or prior authorization.
- Remove tagged temporary instrumentation before finishing.
- Final output must distinguish symptoms, reproduction command and its red output, evidence, root cause, fix, and verification.
