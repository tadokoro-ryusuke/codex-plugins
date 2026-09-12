---
name: codex-collab
description: "Delegate bounded implementation, review, or investigation when collaboration is requested or authorized by applicable instructions."
---

# Codex Collab

Coordinate independent reasoning inside Codex: reviews that don't trust the implementer, rescue when an approach is looping, and explicit parallel subagent work.

For substantial approved-plan execution, read
`references/planned-execution.md`. Resolve implementation/review settings from
`assets/execution-profile.json` with `scripts/resolve_execution_role.py`; this
defines defaults for that workflow, not for every collaboration request.
For bounded dev-core source lookup or log classification, the optional researcher
role is authorized under the "Optional bounded research" section of
`references/planned-execution.md`; do not load the full execution workflow for it.
For a native-agent evaluation of that workflow, read
`references/execution-evaluation.md` and use `scripts/execution_smoke.py`.

## Principles

1. Keep the main thread focused on requirements, decisions, and final synthesis.
2. Use independent review to challenge your own implementation claims.
3. Treat every agent result as untrusted until verified against files, diffs, logs, or command output.
4. Stop after three failed attempts at the same fix path. Report the attempts and switch to a fresh diagnosis or ask for user direction.

## Choosing the Codex surface

- `/review` or a review-style response: review of the current working tree.
- Subagents: for bounded work authorized by the user or applicable instructions. Use them when independent work or review justifies the coordination cost.
- New task or fork: only for a user-requested task operation. Use authorized subagents for internal bounded work; do not silently create user-owned tasks.
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
4. Form competing root-cause hypotheses from the evidence.
5. Validate or eliminate each hypothesis before editing.
6. Make the smallest fix that addresses the confirmed root cause.
7. Run $verification-loop and report evidence.

## Parallel subagents

Follow the delegation contract in
`../dev-workflow/references/orchestration.md`: scope, raw evidence, ownership,
completion criteria, and stop condition. Specify shared resources as well as file
ownership. Prefer independent exploration, test runs, triage, and review; parallel
edits need disjoint ownership and resources. Respect the host's role, concurrency,
model, and sandbox limits.

Request concise findings plus command results or artifact references that the
parent can verify. Use the profile for planned execution or its optional research role;
otherwise inherit model settings unless an explicit instruction selects an
override.

Good splits: security / test-gap / maintainability review; backend / frontend / infrastructure analysis; reproduction triage / code-path trace / fix strategy.

### Bundled role definitions

This skill ships ready-made custom agent roles:

- `assets/agents/code-reviewer.toml` — zero-trust reviewer, read-only sandbox.
- `assets/agents/security-auditor.toml` — OWASP Top 10 auditor, read-only sandbox.

To use them, copy the files into `<repo>/.codex/agents/` (project-wide) or `~/.codex/agents/` (personal), then reference the role when spawning (e.g. "spawn the code-reviewer agent on this diff").

These optional TOML assets define review behavior and sandbox preferences. They
do not load the JSON execution profile automatically. For planned execution,
pass the resolved model/effort explicitly through the host's supported spawn
interface. No custom-role installation is needed when that interface accepts
model settings and a bounded task prompt directly.

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
