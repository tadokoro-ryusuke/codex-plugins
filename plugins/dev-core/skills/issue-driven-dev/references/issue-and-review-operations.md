# Issue and review operations

Reuse the project's taxonomy and workflow. When designing one from scratch, start
with a small set of type, priority, and status fields; labels such as `type/bug`,
`priority/P1`, and `status/blocked` are examples, not a migration mandate. Add a
field only when someone uses it for a decision.

Define what `ready` proves in this project. Preserve an explicit human-vetting gate
if one exists. Otherwise, record how the work order inherits the user's accepted
scope; do not label bulk-generated proposals as approved product decisions.
For a blocked item, record the dependency and what would unblock it.

Use milestones for the release, contract phase, or other planning unit the team
actually manages. Set dates when they represent a real commitment. Choose a triage
cadence from arrival rate and ownership; this reference does not schedule a recurring
task or require weekly external updates.

## Triage and contract scope

Inspect new work for duplicates, priority, scope, dependencies, and usable completion
conditions. Prepare proposals using available decisions. Apply labels, comments, or
closures only under existing authority, preserving links to the canonical work.

For actual contract development, distinguish covered work, a separate quotation,
and declined work. Reuse the agreed scope decision; prepare a complete comparison
when it is unresolved. Do not accept new commercial scope or implement work that
requires a new agreement before that agreement is authorized. Routine internal
engineering does not require a contract-triage gate.

## Branches and PRs

Follow the repository's branch and integration model. Choose short-lived feature
branches or trunk-based work based on release cadence, automated gates, and mixed
version/feature-flag needs. Do not introduce permanent release branches without
an operational requirement. Keep unrelated dirty work safe before switching branches.

Keep PRs cohesive and link them to the work they complete. Explain partial coverage
when several PRs implement one issue. Preserve the configured approval and merge
policy; creating a ticket does not authorize publication or merge.

## Review

Make findings actionable and distinguish blocking defects from suggestions or
questions. Use the team's format; Conventional Comments prefixes are an option.
Review observable behavior, design consequences, security boundaries, and missing
coverage, and verify findings against actual code or command output.

Use independent review where the task or policy requires it or complexity warrants
it and delegation is authorized. Independence does not prohibit an implementer from
writing TDD tests. Do not claim that an AI first pass is exhaustive or that a second
agent's conclusion proves correctness without checking its evidence.

Respect the owner's final approval and merge gates while completing permitted
repairs. Set review response expectations with the team rather than imposing a
one-business-day SLO on every repository.
