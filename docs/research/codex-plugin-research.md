# Codex Plugin Research Notes

Research dates: 2026-06-07 (initial migration), 2026-06-11 (refresh).

Primary sources: `developers.openai.com/codex` (plugins, plugins/build, skills, hooks, subagents, custom-prompts, config-reference, changelog), the Agent Skills standard at `agentskills.io`, the bundled system skills (`plugin-creator`, `skill-creator` under `$CODEX_HOME/skills/.system/`), and `openai/skills`.

## Current Findings (2026-06-11)

### Plugins and marketplaces

- Plugins bundle skills, hooks, app integrations, and MCP servers. Only `plugin.json` lives in `.codex-plugin/`; everything else sits at the plugin root.
- Required manifest fields per the bundled validator: `name`, `version` (strict semver), `description`, `author.name`, and the `interface` block (`displayName`, `shortDescription`, `longDescription`, `developerName`, `category`).
- Marketplace catalogs live at `.agents/plugins/marketplace.json` (repo-scoped) or `~/.agents/plugins/marketplace.json` (personal). Source types: `local`, `git-subdir` (with `url`/`path`/`ref`), and repo-root URLs.
- Remote install flow: `codex plugin marketplace add owner/repo [--ref X] [--sparse DIR]`, then `codex plugin add <plugin>@<marketplace>`. `--json` output shipped in CLI 0.138–0.139 (June 2026).
- Local iteration: bump the version (or `+codex.<timestamp>` cachebuster) and `codex plugin add` again; start a new thread to pick up changes.

### Skills

- Codex follows the Agent Skills standard. Frontmatter: `name`, `description` required; `license`, `compatibility`, `metadata` optional. UI metadata goes in `agents/openai.yaml`, not frontmatter.
- Progressive disclosure: metadata always loaded (the initial skills list is capped around 8,000 characters); SKILL.md body (< 500 lines / ~5k tokens) loads on activation; `references/`, `scripts/`, `assets/` load on demand.
- `agents/openai.yaml` supports `interface` (display_name, short_description, icons, brand_color, default_prompt mentioning `$skill`), `policy.allow_implicit_invocation` (false = not injected into model context; explicit `$skill` still works), and `dependencies.tools` (MCP).
- Official quality bar: write only what the agent doesn't know; defaults, not menus; procedures, not declarations; bundle a tested script when the agent keeps rewriting the same logic; descriptions state what + when with trigger words and are testable against trigger/no-trigger prompts.
- Custom prompts are deprecated in favor of skills (since 2026-01).

### Hooks (GA since 2026-05)

- Events: `SessionStart`, `SubagentStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop`.
- Only `"type": "command"` handlers execute; `prompt`/`agent` handlers are parsed but skipped.
- Payload arrives as JSON on stdin (`tool_name`, `tool_input.command`, etc.). PreToolUse blocks by printing `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", ...}}` (or exit 2 with stderr reason). SessionStart stdout becomes extra developer context.
- Plugins bundle hooks at the default path `hooks/hooks.json` (auto-discovered). Declaring `hooks` in `plugin.json` is documented upstream but rejected by the bundled plugin-creator validator, so this repo relies on the default path. Hook commands receive `PLUGIN_ROOT`/`PLUGIN_DATA`. Plugin hooks run only after the user reviews and trusts them.

### Subagents and custom agents

- Subagents are explicit-only; enable collaboration tools with `features.multi_agent = true` (`spawn_agent`, `send_input`, `wait_agent`, `close_agent`); `[agents] max_threads` defaults to 6; subagents inherit the current sandbox policy.
- Custom agent roles are standalone TOML files in `.codex/agents/` or `~/.codex/agents/` with `name`, `description`, `developer_instructions` and optional `model`, `model_reasoning_effort`, `sandbox_mode`, `nickname_candidates`. Plugins cannot install them, so dev-core ships them as `codex-collab` assets with copy instructions.

## Layout Decisions (current)

- Three plugins: `dev-core`, `github-tools`, `ui-ux-pro-max` (`ms-office-suite` removed 2026-06-11).
- All skill content in English; descriptions carry trigger phrases.
- Reference skills (`best-practices`, `backend-patterns`, `frontend-patterns`) set `allow_implicit_invocation: false`; workflow entrypoints stay implicit.
- `verification-loop` bundles `scripts/verify.sh` (stack-detecting six-step runner); `dev-task`/`dev-checkpoint` bundle output templates as assets.
- dev-core bundles hooks: PreToolUse destructive-command blocker (Python, permissionDecision deny) and SessionStart project-state injector (bash, stdout context).
- `scripts/validate-codex-plugins.mjs` mirrors the bundled validator plus repo conventions (hooks schema, openai.yaml presence, bundled-path existence, description length, body line cap).

## Known gaps / future candidates

- `ui-ux-pro-max` SKILL.md is ~240 lines; splitting usage examples into `references/` would tighten it further.
- The hub-and-spoke `../dev-workflow/references/` coupling means dev-core skills are not individually copyable; acceptable while they ship as one plugin.
- codex-plugin-scanner (community SARIF scanner) could be added to CI once its action is vetted.
