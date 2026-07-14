---
name: codex-collab
description: "Codex-native collaboration for independent review, second opinions, rescue after repeated failures, bounded subagent delegation, and thread handoffs. Use when the user asks for collaboration or when an applicable AGENTS.md or skill explicitly authorizes an independent review, read-heavy delegation, or rescue pass."
---

# Codex Collab

Coordinate independent reasoning inside Codex: reviews that don't trust the implementer, rescue when an approach is looping, and explicit parallel subagent work.

## Principles

1. Keep the main thread focused on requirements, decisions, and final synthesis.
2. Use independent review to challenge your own implementation claims.
3. Treat every agent result as untrusted until verified against files, diffs, logs, or command output.
4. Stop after three failed attempts at the same fix path. Report the attempts and switch to a fresh diagnosis or ask for user direction.

## Choosing the Codex surface

- `/review` or a review-style response: review of the current working tree.
- Subagents: when the user directly asks or an applicable `AGENTS.md` or skill explicitly authorizes a bounded task. Do not infer authorization from task size alone.
- New thread or fork: isolated exploration without polluting the main thread.
- Browser / computer use: only when the task needs UI inspection or browser testing.
- MCP/connectors: when the needed context lives outside the repo (GitHub, Slack, docs, issue trackers).

## Independent review

1. Identify the review target: working tree, branch, PR, file, plan, or failure log.
2. Gather the smallest useful artifact set: `git status`, relevant diffs, changed files, failing outputs.
3. Review as an independent critic. Prioritize bugs, regressions, security, missing tests, and unclear contracts.
4. Verify each finding against concrete files or command output before reporting it.
5. Present findings first, ordered by severity, with file references.

## Rescue workflow

Use when the same issue has failed three times, the current approach is looping, or the user asks for rescue:

1. Freeze implementation. Do not attempt the fourth similar fix.
2. Summarize the failed attempts with evidence and why each failed.
3. Rebuild the problem statement from symptoms, reproduction steps, and logs.
4. Produce three independent root-cause hypotheses.
5. Validate or eliminate each hypothesis before editing.
6. Make the smallest fix that addresses the confirmed root cause.
7. Run $verification-loop and report evidence.

## Parallel subagents

Subagents require a direct user request or explicit authorization in an applicable project instruction or skill. Requirements and behavior:

- Current Codex releases enable subagent workflows by default. Local configuration can still limit roles, concurrency, models, and sandbox behavior.
- Subagents inherit the current sandbox policy — be deliberate when running with elevated permissions.
- Prefer parallel subagents for read-heavy work: exploration, test runs, triage, review. Avoid parallel write-heavy work (edit conflicts).
- Ask each subagent for a concise summary with evidence, not raw logs. Synthesize and independently verify claims before acting.

Good splits: security / test-gap / maintainability review; backend / frontend / infrastructure analysis; reproduction triage / code-path trace / fix strategy.

### Bundled role definitions

This skill ships ready-made custom agent roles:

- `assets/agents/code-reviewer.toml` — zero-trust reviewer, read-only sandbox.
- `assets/agents/security-auditor.toml` — OWASP Top 10 auditor, read-only sandbox.

To use them, copy the files into `<repo>/.codex/agents/` (project-wide) or `~/.codex/agents/` (personal), then reference the role when spawning (e.g. "spawn the code-reviewer agent on this diff").

## Output shape

For reviews:

```text
Findings
- [severity] file:line - issue and impact

Open Questions
- Anything blocking certainty

Verification
- Commands or artifacts checked
```

For rescue:

```text
Rescue Summary
- Attempts tried
- Confirmed root cause
- Fix applied
- Verification evidence
```
