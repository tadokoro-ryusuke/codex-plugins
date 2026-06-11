---
name: continuous-learning
description: "Turn mistakes into durable prevention. Use after build/test/lint failures, review findings, repeated errors, or debugging sessions to encode the lesson into AGENTS.md, tests, lint rules, scripts, or Codex hooks so it cannot recur."
---

# Continuous Learning

Principle (Mitchell Hashimoto): every time the agent makes a mistake, build a mechanism that makes that mistake impossible to repeat.

## Learning loop

### 1. Detect the mistake

Identify what went wrong in this session: build errors, test failures, lint violations, review findings, or a pattern that keeps repeating (same bug class, same manual fix).

### 2. Classify the root cause

- **Missing rule**: no existing rule or skill covers the situation.
- **Ignored rule**: a rule exists but was not followed → needs enforcement, not more prose.
- **Missing knowledge**: a project-specific constraint was never written down.
- **Missing tooling**: an error that a machine could catch was left to manual checking.

### 3. Build the prevention

| Cause | Countermeasure | Where it lives |
|---|---|---|
| Missing rule | Add it to the relevant skill or project rules | `skills/*/SKILL.md`, project docs |
| Ignored rule | Enforce with a Codex hook (command handler) | `.codex/hooks.json` or a plugin's `hooks/hooks.json` |
| Missing knowledge | Record the project constraint | `AGENTS.md` (keep it under the ~32 KiB default read limit; link out for detail) |
| Missing tooling | Add a lint rule, test, or script | linter config, test files, `scripts/` |

Notes on Codex hooks: only `"type": "command"` handlers execute (prompt handlers are parsed but skipped), and plugin-bundled hooks require the user to review and trust them before they run. Events include `SessionStart`, `PreToolUse`, `PostToolUse`, `PreCompact`, and `Stop`. The dev-core plugin ships working examples in its `hooks/` directory.

### 4. Verify the prevention works

- Attempt the same forbidden operation — does the hook block it?
- Write the same bad code — does lint or a test catch it?
- Start a fresh session — is the new rule actually loaded and followed?

## Compounding improvement

Each session improves the harness; the improved harness makes the next session more reliable.

```
Session 1: bug found        → rule added
Session 2: rule prevents it → new bug found → hook added
Session 3: hook + rule hold → attention moves to harder problems
```

## Growing the Stop-time checks

Use a `Stop` hook or verification script to auto-detect recurring leftovers: uncommitted changes, stray `console.log`/`debugger`, new TODO/FIXME comments. When a new leftover class appears in review, add it to the detection list — the Stop check itself is a learning artifact.
