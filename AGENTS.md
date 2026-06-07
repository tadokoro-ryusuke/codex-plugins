# AGENTS.md

This repository is a Codex plugin marketplace source. Keep it Codex-native.

## Repository Shape

- Marketplace catalog: `.agents/plugins/marketplace.json`.
- Plugin roots: `plugins/<plugin-name>/`.
- Codex manifests: `plugins/<plugin-name>/.codex-plugin/plugin.json`.
- Skills: `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.

## Editing Rules

- Do not add `.claude-plugin`, Claude slash commands, or Claude-only command metadata here.
- Prefer a focused skill plus `references/` over copying long command prompts into `SKILL.md`.
- Keep skill frontmatter to `name` and `description`.
- Keep `plugin.json` paths relative and use `skills: "./skills/"` when skills are bundled.
- Keep marketplace `source.path` as `./plugins/<plugin-name>`.
- Run plugin validation before handing back changes.

## Migration Notes

- Claude commands become Codex skills or skill references.
- Claude agent-team workflows become explicit Codex subagent/thread guidance; do not imply Codex spawns subagents automatically.
- Claude permission snippets belong in Codex config/rules documentation, not in plugin manifests.
- Claude prompt hooks are not ported directly; Codex hooks currently run command handlers, while prompt handlers are parsed but skipped.

