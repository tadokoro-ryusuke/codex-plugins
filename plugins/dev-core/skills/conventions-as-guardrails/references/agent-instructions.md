# Agent instructions

Keep `AGENTS.md` focused on information that changes the agent's decisions in this
repository: domain meaning, non-obvious boundaries, protected areas, operational
invariants, and exact verification commands or their maintained source.

Link architecture, deployment, schemas, and detailed workflows with a condition
for reading them. Do not instruct every task to load every reference. Use accurate
paths or stable symbols; avoid copying code and long best-practice passages already
owned by tools, skills, or source documents.

Write explicit prohibitions only where they protect a real invariant. Avoid
converting every preference or past failure into a universal ban. Put enforceable
formatting and lint rules in their configs and keep semantic intent in the document.
Preserve user scope and existing authorization; describe when a new decision is
needed instead of requiring approval before routine work.

Use one source of truth, with thin tool-specific wrappers if required. In a monorepo,
place package-specific guidance near that package when it would otherwise distract
unrelated work. Keep current operating instructions separate from historical ADRs;
update stale instructions as part of an authorized change without implying permission
to commit or publish them.

Before handing back, check that paths exist, instructions match actual commands and
ownership, and the new wording does not activate unrelated work or erase a needed
permission or correctness boundary.
