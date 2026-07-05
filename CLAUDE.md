@AGENTS.md

# Claude Code notes

- This repository is Codex-native: keep all plugin/skill content in English and imperative, even when the conversation with the user is in Japanese.
- Do not introduce Claude-specific frontmatter or paths into skills (`allowed-tools:`, `argument-hint:`, `.claude/`, `.claude-plugin`, `CLAUDE_*` env vars) — they break Codex conventions here.
