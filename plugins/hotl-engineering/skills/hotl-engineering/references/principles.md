# Principles — 12 Principles for AI-Native Development Operations

Each principle follows "Principle / Rationale / Practical manifestation." Use this as the starting point for advisory responses.
Rationale sources are surveys as of 2025-2026 (DORA 2025, SRE Report 2026, Anthropic practical knowledge).
Facts may change over time, but the principles themselves remain stable.

## 1. AI is an amplifier, not a solution
**Rationale**: DORA 2025 — AI amplifies the existing engineering environment. Mature organizations can convert productivity gains into delivery performance, while fragmented organizations accelerate the accumulation of technical debt.
**Practice**: Start any AI-adoption consultation with a maturity assessment of the foundation (VCS, testing, observability, process). Oppose proposals that merely increase agent volume while the foundation is weak.

## 2. The scarce resource is human cognitive bandwidth. Organizational design is the design of its allocation
**Rationale**: Generation cost keeps falling as models improve, but the human cost of review and judgment does not fall. Even in incidents, the binding constraint is human cognitive bandwidth, not observability data.
**Practice**: Score every design proposal by "how many times, and for how long, a human must engage in judgment." Keep approval points countable (in HOTL, 4 points: CP1-CP4). If approval points start proliferating, the design has rotted.

## 3. Investment in verification beats investment in generation
**Rationale**: The ceiling on how much work can run unattended is set by "what can be verified mechanically." It is worth spending a week building out verification skills, tests, and evals (Anthropic internal insight).
**Practice**: Convert "I want to add more agents" requests into "what will verify this?" Do not approve automation that has no means of verification.

## 4. Autonomy can only be raised in stages (RO → Advised → Approved → Autonomous)
**Rationale**: The trust-building cycle cannot be skipped. No organization jumps straight to autonomous remediation (AI SRE practice).
**Practice**: Require every automation to state its current stage explicitly. Require quantitative track record for promotion (the promotion criteria in decision-frameworks.md). Do not hesitate to demote.

## 5. Stratify by risk. A uniform gate kills both speed and safety
**Practice**: Tier 0 (docs / dependency patches) / Tier 1 (normal) / Tier 2 (auth, permissions, migrations, confidentiality boundaries, CI itself). Enforce the Tier 2 definition mechanically in two places — paths-filter and CODEOWNERS — and always keep them in sync. "Strict everywhere" always degrades into "lax everywhere."

## 6. Gates go comment-only → calibration → enforcement. False positives destroy trust
**Rationale**: Enforcing from day one causes teams to revolt against false positives that a calibration period would have resolved, and the tool gets ripped out entirely (the most common failure pattern in AI code review adoption).
**Practice**: Reject any new-gate rollout plan that does not include a calibration period (roughly 2 weeks).

## 7. Prompt changes are change-management items with the same weight as code changes
**Rationale**: The deployable unit for an agent is the bundle of "model + prompt + tool definitions" (agent version). Promotion is judged by eval results, not by test pass/fail.
**Practice**: Close off any path that lets a prompt reach production directly. Treat prompt improvements without an eval-gate the same as "refactoring without tests."

## 8. Thresholds should be dual: relative (vs. baseline) and absolute (floor)
**Rationale**: Relative-only thresholds let degradation accumulate gradually (boiling frog). Absolute-only thresholds settle for initial quality.
**Practice**: Require this dual structure for every threshold design — evals, SLOs, coverage.

## 9. What cannot be protected by an average must be protected by must-pass
**Rationale**: For MNPI boundaries, access control, and injection resistance, "95% accuracy" is meaningless. Separate domains where a single leak is fatal from the score average, and block on 100% required plus any single failure.
**Practice**: In an eval-design review, first ask "what are the must-pass categories?"

## 10. Generate the audit trail automatically as a byproduct of the workflow
**Rationale**: Retrofitted audit trails always have gaps. If PR-approval logs, eval reports, deployment approvals, and rollback records land automatically in immutable storage by design, audit response becomes a matter of presenting configuration values.
**Practice**: For J-SOX matters, see references/jsox-audit.md.

## 11. Failure is an asset. Recycle it under the 24-hour rule
**Practice**: Turn production retrieval misses and wrong answers into golden-set entries within 24 hours. After an agent repeats the same kind of mistake twice, add one line to AGENTS.md / the skill. Datasets and normative files are "growing assets," not documents you write once and forget.

## 12. Before buying, try the existing platform plus in-house read-only
**Rationale**: The market for tools like AI SRE is in a period of proliferation, and much of it is overkill for small teams. Most of the value lies in "automating context assembly," which can often be built in-house on the existing agent platform.
**Practice**: Run the buy-vs-build questions in decision-frameworks.md before considering a purchase.
