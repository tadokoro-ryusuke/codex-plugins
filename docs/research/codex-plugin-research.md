# Codex Plugin Research Notes

Research date: 2026-06-07.

Primary source used: current Codex manual fetched from `https://developers.openai.com/codex/codex-manual.md`.

## Findings

- Codex plugins bundle skills, app integrations, and MCP servers into reusable workflows.
- Skills are the workflow authoring format; plugins are the installable distribution unit.
- Codex uses progressive disclosure for skills: metadata first, `SKILL.md` after activation, references/scripts only when needed.
- Custom prompts are deprecated for reusable shared workflows. Use skills instead.
- A repo marketplace should expose plugin entries from `.agents/plugins/marketplace.json`, with `source.path` pointing to `./plugins/<plugin-name>`.
- Codex subagent workflows are explicit. They are useful for read-heavy exploration, tests, triage, and review, but should not be assumed to run automatically.
- Codex hooks can be bundled by plugins, but command handlers are the supported runtime path. Claude prompt hooks should be converted to skill guidance or command hooks.

## Migration Decisions

- Keep the four original plugin concepts: `dev-core`, `github-tools`, `ms-office-suite`, and `ui-ux-pro-max`.
- Move all plugin roots under `plugins/` to match Codex marketplace conventions.
- Convert Claude slash commands to Codex skills:
  - `dev-core` gets `dev-workflow`, with detailed workflow references.
  - `github-tools` gets `github-workflows`, with PR and docs references.
- Rewrite `codex-collab` as a Codex-native collaboration skill instead of keeping Claude Code + `codex-plugin-cc` assumptions.
- Remove Claude-only frontmatter fields from migrated skills where practical.
- Replace `${CLAUDE_SKILL_DIR}` examples with paths relative to the skill directory.

## Manual Anchors

- `/codex/plugins/build`: plugin structure, marketplaces, local plugin setup, sharing.
- `/codex/skills`: skill structure, triggering, progressive disclosure, optional `agents/openai.yaml`.
- `/codex/custom-prompts`: custom prompts are deprecated; skills are preferred for shared reusable prompts.
- `/codex/hooks`: hook discovery and supported command handler shape.
- `/codex/concepts/subagents`: subagents must be explicitly requested and are best for bounded parallel work.

