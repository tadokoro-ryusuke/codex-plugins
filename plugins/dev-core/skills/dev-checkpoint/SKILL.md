---
name: dev-checkpoint
description: "Checkpoint and handoff workflow for resumable development state. Use to checkpoint, pause, resume, hand off, summarize progress, capture evidence, or record next actions."
---

# Dev Checkpoint

Use this skill when work needs a durable handoff or resumable state.

## Workflow

1. Read `../dev-workflow/references/orchestration.md`.
2. Read the Checkpoints section in `../dev-workflow/references/e2e-checkpoint.md`.
3. Capture goal, completed steps, files changed, commands run, results, blockers, decisions, and next actions.
4. Save under `docs/checkpoints/checkpoint-<timestamp>.md` only when the user wants a file.

## Output

Make the checkpoint useful to a fresh Codex thread. Include exact paths and commands, but avoid noisy logs unless they are essential.
