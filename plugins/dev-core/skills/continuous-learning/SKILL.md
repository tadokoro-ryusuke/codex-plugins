---
name: continuous-learning
description: "Prevent demonstrated recurring failures when a regression test, tool rule, or scoped instruction can address their cause."
---

# Continuous Learning

Turn a demonstrated recurring failure into the smallest useful prevention.
Do not turn every typo, expected TDD failure, or one-off environment problem into
a permanent rule. Prefer a regression test or existing tool configuration over
another generic instruction.

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

When the prevention is a written rule, state its scope, its reason, and when it was
added. Where an exception can exist, write the exception path into the rule as
"before X, do Y" instead of "never X". A bare "never" reads as a rule without
exceptions and can block work that was already approved; the reason and date let a
later review decide whether the rule still applies. For example: "Regenerate
`src/gen/` with the generator instead of editing it by hand, because the next run
discards hand edits (scope: `src/gen/`; added 2026-11). Before a temporary hand fix
for a generator bug, get the owner's approval."

Use command handlers for this repository's portable hooks. Current Codex also
supports MCP tool hooks; prompt/agent handlers are parsed but skipped. Plugin
hooks require user trust review. Use the host's documented event/payload contract;
shell and unified-exec hooks use the canonical Bash name and command field.
The dev-core plugin ships command examples in its hooks directory.

### 4. Verify the prevention works

- Pipe a synthetic payload to the hook in an isolated fixture and inspect its decision. Never execute a destructive operation to test a blocker.
- Write the same bad code — does lint or a test catch it?
- Start a fresh session — is the new rule actually loaded and followed?

### 5. Review and retire rules

Rules and cautions pile up in instruction files, memory, and notes. Agents follow
them closely, so stale ones lead to unneeded approval requests and routine work left
on hold. Review them when you change the model you work with, because how literally
a model follows written rules differs between models, and periodically (for example,
each quarter). Remove:

- rules whose reason no longer holds (the code, tool, or practice they assumed is gone);
- cautions aimed at a failure that no longer reproduces;
- prose rules that duplicate what lint, a hook, or a test already enforces.

Keep confirmation steps for risky or irreversible actions. Retire rules within the
authorized project scope; touch personal memory or global settings only on an
explicit request.

## Scope and durability

Keep prevention within the authorized task. Change project rules only for an
established project invariant; do not rewrite personal memory or global settings
without an explicit request. A shell-pattern hook is defense in depth, not a
complete security boundary. Test both its intended deny and safe pass-through
cases, and keep sandbox/approval controls in place.

## Compounding improvement

Each session improves the harness; the improved harness makes the next session more reliable.

```
Session 1: bug found        → rule added
Session 2: rule prevents it → new bug found → hook added
Session 3: hook + rule hold → attention moves to harder problems
Model change: review        → stale rules and hook-enforced duplicates retired
```

## Growing the Stop-time checks

Use a Stop hook only for a demonstrated recurring issue with an actionable,
low-noise check. Uncommitted changes are normal when commits were not requested;
TODOs and diagnostic logging need context. Do not block completion merely because
these strings exist, or append permanent checks without a recurrence signal.
