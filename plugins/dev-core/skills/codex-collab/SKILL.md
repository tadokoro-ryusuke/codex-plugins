---
name: codex-collab
description: "Codex-native collaboration workflow for independent review, second opinions, rescue work, parallel subagents, and thread handoffs. Use when the user asks for Codex review, a second opinion, rescue after repeated failures, parallel agents, or a separate verification pass."
---

# Codex Collab

Use this skill to coordinate independent reasoning inside Codex without relying on Claude Code or `codex-plugin-cc`.

## Principles

1. Keep the main thread focused on requirements, decisions, and final synthesis.
2. Use independent review to challenge your own implementation claims.
3. Treat every agent result as untrusted until verified against files, diffs, logs, or command output.
4. Stop after three failed attempts at the same fix path. Report the attempts and switch to a fresh diagnosis or ask for user direction.

## Choosing The Codex Surface

- Use `/review` or a review-style response when the user wants a review of the current working tree.
- Use explicit subagents only when the user asks for parallel agents, second opinions, or delegation.
- Use a new thread or fork when the user wants an isolated exploration without polluting the main thread.
- Use Browser or Computer Use only when the task requires local UI inspection, browser testing, or desktop interaction.
- Use MCP/connectors when the needed context lives outside the repo, such as GitHub, Slack, docs, or issue trackers.

## Independent Review

When asked for a second opinion or review:

1. Identify the review target: working tree, branch, PR, file, plan, or failure log.
2. Gather the smallest useful artifact set: `git status`, relevant diffs, changed files, failing outputs.
3. Review as an independent critic. Prioritize bugs, regressions, security, missing tests, and unclear contracts.
4. Verify each finding against concrete files or command output before reporting it.
5. Present findings first, ordered by severity, with file references.

## Rescue Workflow

Use this when the same issue has failed three times, the current approach is looping, or the user asks for rescue:

1. Freeze implementation. Do not attempt the fourth similar fix.
2. Summarize the failed attempts with evidence and why each failed.
3. Rebuild the problem statement from symptoms, reproduction steps, and logs.
4. Produce three independent root-cause hypotheses.
5. Validate or eliminate each hypothesis before editing.
6. Make the smallest fix that addresses the confirmed root cause.
7. Run the relevant verification loop and report evidence.

## Parallel Subagents

Only use subagents when explicitly requested or clearly authorized by the user. Good splits:

- Security review, test-gap review, maintainability review.
- Backend analysis, frontend analysis, infrastructure analysis.
- Reproduction/log triage, code-path trace, fix strategy.

Ask each subagent to return a concise summary with evidence, not raw logs. After all agents finish, synthesize and independently verify their claims before acting.

## Output Shape

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

