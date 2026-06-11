# AGENTS.md

This repository is a Codex plugin marketplace source. Keep it Codex-native.

## Repository Shape

- Marketplace catalog: `.agents/plugins/marketplace.json`.
- Plugin roots: `plugins/<plugin-name>/`.
- Codex manifests: `plugins/<plugin-name>/.codex-plugin/plugin.json` (only `plugin.json` lives in `.codex-plugin/`).
- Skills: `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` plus optional `references/`, `scripts/`, `assets/`, and `agents/openai.yaml`.
- Hooks: `plugins/<plugin-name>/hooks/hooks.json` (auto-discovered default path; do NOT add a `hooks` field to `plugin.json` — the bundled plugin-creator validator rejects it).

## Editing Rules

- Write all skill content in English; imperative form.
- Skill frontmatter: `name` and `description` (optional `metadata`, `license`, `compatibility` are tolerated; nothing else). The description must state what the skill does AND when to use it, with trigger words up front.
- Keep `SKILL.md` under 500 lines; push detail into `references/` (one level deep) and deterministic logic into tested `scripts/`.
- Every skill ships `agents/openai.yaml` with `display_name`, `short_description`, and a `default_prompt` that mentions `$<skill-name>`. Pure reference skills set `policy.allow_implicit_invocation: false` to keep the always-on skill list inside Codex's ~8,000 character budget.
- Hook handlers must be `"type": "command"` — prompt handlers are parsed but skipped by Codex. Test hook scripts by piping sample payloads before committing.
- Keep `plugin.json` paths relative (`./`), `skills: "./skills/"`, and versions strict semver. Bump the version on every released change.
- Keep marketplace `source.path` as `./plugins/<plugin-name>` and include `policy` and `category` on every entry.
- Run `node scripts/validate-codex-plugins.mjs` before handing back changes.

## Codex Feature Notes

- Hooks are GA: events include `SessionStart`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`. Plugin hooks receive `PLUGIN_ROOT`/`PLUGIN_DATA` and require user trust review before running. PreToolUse blocks via `permissionDecision: "deny"` JSON on stdout; SessionStart stdout becomes developer context.
- Custom agent roles are standalone TOML files in `.codex/agents/` (project) or `~/.codex/agents/` (personal); plugins cannot install them directly, so ship them as skill `assets/` with copy instructions.
- Subagents are explicit-only (`features.multi_agent = true`); never imply Codex spawns them automatically.
- Custom prompts are deprecated; skills are the reusable workflow format.
