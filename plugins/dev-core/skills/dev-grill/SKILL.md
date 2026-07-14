---
name: dev-grill
description: "Grill and stress-test a plan, decision, or idea through one question at a time before implementation. Use only when the user explicitly asks to grill, challenge, pressure-test, interrogate, or find hidden assumptions in a proposal."
---

# Dev Grill

Pressure-test a proposal until the user and Codex share the same decision model. Keep this separate from routine planning so clear, reversible work can proceed without ceremony.

## Interview Contract

1. Inspect the repository, referenced documents, and available evidence before asking anything.
2. Build a private decision map with three buckets:
   - **Facts**: verify these from the environment; do not ask the user.
   - **Reversible assumptions**: state the recommended default and continue unless the user objects.
   - **Material decisions**: ask when the answer changes scope, architecture, security, irreversible data, external side effects, or product intent.
3. Ask exactly one material question at a time and wait for the answer.
4. For every question, give a recommended answer, the reason, and the main trade-off. Offer alternatives only when they are genuinely viable.
5. Follow the answer down the decision tree. Challenge contradictions, missing failure modes, and hidden dependencies instead of following a fixed questionnaire.
6. Stop when further questions no longer change the plan materially.

## Autonomy Guardrails

- Do not ask for information that repository inspection, documentation, or a safe read-only command can answer.
- Do not turn naming, formatting, or another low-risk reversible choice into a blocker.
- Do not implement, edit files, create issues, commit, push, or open a PR unless the user separately asks for that action.
- Surface uncertainty honestly. Distinguish an unknown fact from a judgment call.

## Exit Summary

Finish with:

- Confirmed goal and non-goals.
- Decisions made and their rationale.
- Reversible assumptions and defaults.
- Remaining risks or unresolved decisions.
- The next smallest action, without taking it unless authorized.
