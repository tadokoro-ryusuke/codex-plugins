---
name: dev-checkpoint
description: "Checkpoint and handoff workflow for resumable development state. Use to checkpoint, pause, resume, hand off, summarize progress, capture evidence, or record next actions."
---

# Dev Checkpoint

Use this skill when work needs a durable handoff or resumable state.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read the Checkpoints section in `../dev-workflow/references/e2e-checkpoint.md`.
3. If work has a `docs/plans/task-*.md` plan, update that plan's status, completion contract, progress log, decision log, blockers, evidence, and current next action. Keep one durable source of execution state.
4. If no plan exists or the user explicitly asks for a standalone handoff, capture goal, completed steps, files changed, commands run, results, blockers, decisions, and next actions from `assets/checkpoint-template.md`.
5. Save a standalone checkpoint under `docs/checkpoints/checkpoint-<timestamp>.md` only when step 4 applies.

## Output

Make the durable state useful to a fresh Codex thread. Include exact paths, current evidence, and the single next action, but avoid noisy logs unless they are essential.
