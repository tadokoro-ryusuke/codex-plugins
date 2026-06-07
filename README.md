# Codex Plugins

This repository is a Codex-native marketplace source for reusable plugins and agent skills.

It started from the Claude Code oriented `../cc-plugins` repository, but the structure here is intentionally Codex-specific:

- Plugin manifests live at `plugins/<plugin>/.codex-plugin/plugin.json`.
- The marketplace catalog lives at `.agents/plugins/marketplace.json`.
- Reusable workflows are packaged as skills under `plugins/<plugin>/skills/`.
- Claude command and agent concepts are converted to Codex skills, references, hooks guidance, and subagent/thread workflows instead of being copied verbatim.

## Plugins

| Plugin | Purpose |
| --- | --- |
| `dev-core` | TDD, architecture, debugging, verification, review, and continuous improvement workflows. |
| `github-tools` | Pull request preparation and documentation update workflows using GitHub CLI where available. |
| `ms-office-suite` | PDF and DOCX creation, extraction, editing, forms, tracked changes, and OOXML workflows. |
| `ui-ux-pro-max` | Searchable UI/UX design intelligence for frontend and product design tasks. |

## Codex Research Baseline

The migration follows the current Codex manual guidance captured in `docs/research/codex-plugin-research.md`:

- Use skills as the reusable workflow authoring format.
- Use plugins as installable distribution units for skills, MCP servers, apps, and optional assets.
- Prefer skills over deprecated custom prompts for shared reusable prompts.
- Keep `SKILL.md` concise and use references/scripts for progressive disclosure.
- Use Codex subagents only when explicitly requested or when the workflow asks for parallel agent work.

## Validation

Run local validation after edits:

```bash
python3 -m pip install --target /private/tmp/codex-pyyaml PyYAML
export PYTHONPATH=/private/tmp/codex-pyyaml
python3 /Users/poshiri/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dev-core
python3 /Users/poshiri/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/github-tools
python3 /Users/poshiri/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/ms-office-suite
python3 /Users/poshiri/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/ui-ux-pro-max
node scripts/validate-codex-plugins.mjs
```

The `PYTHONPATH` lines are only needed when the local Python does not already include PyYAML.

## Dev Core Entrypoints

Use narrow skills for daily work and let `dev-workflow` provide shared orchestration:

| Skill | Use for |
| --- | --- |
| `$dev-task` | Turn an idea into acceptance criteria, BDD scenarios, and a TDD plan. |
| `$dev-execute` | Execute an existing plan with gated TDD, verification, and review. |
| `$dev-debug` | Investigate errors from root cause before fixing. |
| `$dev-tdd` | Run a focused test-first cycle for one behavior or regression. |
| `$dev-review` | Review with dev-core criteria: behavior, security, tests, architecture, maintainability, conventions. |
| `$dev-refactor` | Refactor safely without behavior changes. |
| `$dev-e2e` | Run or diagnose Playwright E2E tests. |
| `$dev-checkpoint` | Capture resumable state for handoff or continuation. |
| `$dev-workflow` | Shared multi-phase orchestration when no narrower skill fits. |
