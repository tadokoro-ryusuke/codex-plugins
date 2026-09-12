# Decision records

Use the repository's existing documentation convention. Write an ADR when a durable
decision's rationale and consequences would otherwise be lost, especially for a
material architecture, integration, technology, or security tradeoff. Do not create
an ADR for every routine implementation choice merely because it touches that area.

## ADR template

Use one decision per file, such as `docs/adr/NNNN-<decision>.md`:

```markdown
# NNNN: <decision>

- Status: Proposed
- Date: YYYY-MM-DD

## Context
## Decision
## Consequences
## Alternatives considered
```

Mark a proposed decision accepted only when authority for that decision is recorded.
Preserve accepted history: supersede a changed decision with a new record and update
the old status/link rather than rewriting its original rationale. Follow the project's
convention for correcting factual errors without hiding the historical decision.

## Design doc

Use a design doc to explore a substantial design before implementation. Include
context, scope, goals, design, alternatives, and relevant cross-cutting concerns.
Keep it concise enough to obtain useful feedback; update it while the proposal is
active and identify the accepted version when it becomes historical.

## Current operating instructions

Keep `AGENTS.md` and README accurate for current operation, with links to the source
of detailed knowledge. Keep historical decisions distinct from current commands
and boundaries. For trimming or routing agent context, use `$conventions-as-guardrails`.
A document change does not grant authority to commit or publish it.

Client deliverables follow the actual agreement. Derive them from maintained design
sources and identify their reviewed version; an internal ADR is not automatically a
client sign-off or a substitute for the agreed delivery format.
