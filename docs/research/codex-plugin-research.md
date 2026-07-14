# Codex Plugin Research Notes

Research dates: 2026-06-07 (initial migration), 2026-06-11 (refresh), 2026-07-14 (autonomous workflow review).

Primary sources: `developers.openai.com/codex` (plugins, skills, hooks, subagents, AGENTS.md), the Agent Skills standard at `agentskills.io`, the bundled system skills (`plugin-creator`, `skill-creator`), OpenAI's Harness Engineering report, Anthropic's long-running-agent and eval guidance, Matt Pocock's `grilling`, and obra's `superpowers`.

## Current Findings (2026-07-14)

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

- Current Codex releases enable subagent workflows by default. Delegate after a direct user request or an explicit applicable `AGENTS.md`/skill instruction; use bounded read-heavy tasks and avoid overlapping writes. Subagents inherit the current sandbox policy.
- Custom agent roles are standalone TOML files in `.codex/agents/` or `~/.codex/agents/` with `name`, `description`, `developer_instructions` and optional `model`, `model_reasoning_effort`, `sandbox_mode`, `nickname_candidates`. Plugins cannot install them, so dev-core ships them as `codex-collab` assets with copy instructions.

### External workflow practices reviewed

- Matt Pocock's [`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) demonstrates a compact decision interview: inspect facts first, ask one question at a time, recommend an answer, and wait. Adopt it as explicit `$dev-grill`, not an always-on planning tax.
- [`obra/superpowers`](https://github.com/obra/superpowers) reinforces small implementation steps, TDD, independent review, and evidence over claims. Adopt the gates, but do not force a large skill chain for routine edits.
- Anthropic's [long-running agent harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and [`cwc-long-running-agents`](https://github.com/anthropics/cwc-long-running-agents) use persistent progress, default-fail completion criteria, and a fresh evaluator. Adopt durable plan state and independent review with bounded stop conditions.
- Anthropic's [eval guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) recommends testing both trigger and no-trigger behavior on realistic tasks and grading outcomes instead of a rigid path. Add versioned behavior cases and deterministic schema validation first; keep live model grading out of required CI until calibrated.
- OpenAI's [Harness Engineering](https://openai.com/index/harness-engineering/) treats repository documentation, execution plans, validation, and feedback mechanisms as the system of record. Keep `AGENTS.md` short and make plans carry progress, decisions, evidence, and the next action.

### Autonomy boundary adopted

- Verify facts from the environment instead of asking.
- Continue with documented reversible defaults when the requested outcome does not change.
- Escalate material product judgment, security boundaries, destructive or irreversible actions, and external side effects.
- Require current evidence before marking completion criteria satisfied.
- Stop after three similar failures or one complete no-progress cycle.

## Layout Decisions (current)

- Four plugins: `dev-core`, `github-tools`, `hotl-engineering`, `ui-ux-pro-max` (`ms-office-suite` removed 2026-06-11).
- All skill content in English; descriptions carry trigger phrases.
- Reference skills (`best-practices`, `backend-patterns`, `frontend-patterns`) and the interview-style `dev-grill` entrypoint set `allow_implicit_invocation: false`; other workflow entrypoints stay implicit.
- `verification-loop` bundles `scripts/verify.sh` (stack-detecting six-step runner); `dev-task`/`dev-checkpoint` bundle output templates as assets.
- dev-core bundles hooks: a PreToolUse destructive-command blocker (Python, `permissionDecision: deny`) and a SessionStart project-state injector (bash). Because SessionStart stdout becomes developer context, the injector emits only allowlisted branch/hash metadata and active plan path/status; it never copies plan bodies or next-action text into that privileged context.
- `scripts/validate-codex-plugins.mjs` mirrors the bundled validator plus repo conventions (hooks schema, openai.yaml presence, bundled-path existence, description length, body line cap).
- `plugins/dev-core/evals/skill-behavior-cases.json` covers trigger/no-trigger, evidence, reversible defaults, material escalation, and delivery side effects; `scripts/validate-skill-evals.mjs` keeps the suite structurally executable.

## Known gaps / future candidates

- `ui-ux-pro-max` SKILL.md is ~240 lines; splitting usage examples into `references/` would tighten it further.
- The hub-and-spoke `../dev-workflow/references/` coupling means dev-core skills are not individually copyable; acceptable while they ship as one plugin.
- codex-plugin-scanner (community SARIF scanner) could be added to CI once its action is vetted.
- Behavior cases are currently an eval-ready dataset plus structural gate. Add calibrated clean-thread model runs only after collecting representative failures and acceptable variance.
