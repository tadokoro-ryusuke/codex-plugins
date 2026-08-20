---
name: issue-driven-dev
description: "Issue-first development for human + AI agent teams: writing and decomposing GitHub Issues, Issue Forms (YAML) templates, a type/priority/status label system with milestone discipline, GitHub Flow vs trunk-based branching, delegating and parallelizing work across agents, ADR vs Design Doc record-keeping, and PR review discipline (small CLs, Conventional Comments, AI first-pass review). Reference skill; invoke explicitly with $issue-driven-dev when creating or splitting issues, ticketing work, designing labels or milestones, choosing a branch strategy, writing an ADR or design doc, or setting up issue/PR/review workflow."
---

# Issue-Driven Development — running human + AI agent work from issues

**Iron rule: every piece of work starts from an issue. One cycle = open an issue → cut a branch → implement → open a PR → review → merge closes the issue.**

Why: it forces the reason for the work (the "why") and the acceptance criteria to be written down before work starts; in contract development the issue trail doubles as agreement history, billing evidence, and handover material; and in an agent-driven setup the issue itself is the work order.

This skill is the knowledge source of truth for any workflow or agent that plans tasks or drafts issues.

## Division of labor: what AI does / what only humans decide

An agent executing this skill must not cross this line on its own.

| AI (the agent running this skill) does | Only humans decide |
|---|---|
| Draft issues, propose decompositions | Finalize priorities and acceptance criteria (= deciding what to build) |
| Apply labels, detect duplicates, propose triage | Contractual triage of client requests (quote separately / in scope / decline) |
| Implement, open PRs, first-pass review (exhaustive line-by-line) | Final review approval and merge |
| Draft ADRs / design docs / release notes | The decision itself (accepting an ADR's Decision, and owning it) |
| Check issue↔PR linkage, surface progress | Irreversible production actions (deploy approval, triggering rollback) |

Why: writing an issue is writing a delegation contract — the decision of what to build and accountability for the outcome cannot be delegated.

## Step 1: Write a good issue

Always structure the issue body as:

1. **Background / why** (business context): why this work is needed
2. **Current vs expected**: what happens now, what should happen (for bugs: repro steps, expected/actual, environment)
3. **Acceptance criteria**: checkbox list; verifiable conditions only
4. **Out of scope**: state explicitly what this issue will NOT do
5. Technical notes (optional): implementation hints, related files

The title states "what should become what" in one sentence.

**Bar to pass**: "a junior developer could start implementing from this alone" — which is exactly "an AI agent could start implementing from this alone." Never hand an agent an issue that is below this bar.

Why: vague tickets become vague code.

**Writing-cost calibration**: if the work is under 30 minutes or self-evident, a title plus one line is enough. Anything larger requires acceptance criteria. **Issues delegated to AI agents always require acceptance criteria.**

Put three Issue Forms (YAML) templates — bug report / feature request / task — in `.github/ISSUE_TEMPLATE/` so the structure is enforced at the form level → references/issue-driven-dev.md §1. Pass/fail examples → §3.

## Step 2: Decompose — 1 issue = 1 concern = 1 PR

- If an issue mixes multiple concerns, split it. Use a parent issue + sub-issues (GitHub tasklists) for hierarchy.
- Split along **vertical slices with minimal dependencies** (slices of user value), not horizontal layers.
- Why: independent issues let you run multiple agents in parallel. **The quality of issue decomposition directly sets your parallel-agent count — i.e., your throughput.**
- Write `Fixes #N` in the PR body so merging auto-closes the issue. Put the issue number in the branch name (e.g., `feature/123-user-login`).
- Why: without the issue↔PR link, change rationale becomes untraceable. Bake `Fixes #N` into the PR template to enforce it.
- Do not leave a giant issue open for weeks. Loss of visible progress is the signal to split.

## Step 3: Rationalize flow with labels and milestones

Limit labels to **3 axes × at most 5 each**:

| Axis | Example labels | Purpose |
|---|---|---|
| `type/*` | bug / feature / chore / docs | Kind of work |
| `priority/*` | P0 / P1 / P2 / P3 | Priority (P0 = drop everything) |
| `status/*` | needs-triage / ready / blocked | Processing state |

Why: the more labels exist, the less anyone applies them. Push any further attributes into GitHub Projects custom fields.

Cut milestones **per release or per contract phase**. Why: due dates and completion rates become visible automatically, and in contract development the milestone ties work to the contract (billing evidence). Initial set definition → references/issue-driven-dev.md §2.

## Step 4: Run triage

1. Every new issue lands as `status/needs-triage`.
2. Triage **weekly**: assign priority and milestone, then either promote to `ready` or close.
3. In contract development, run client-request issues through the **contract triage gate** here: a human sorts each into **quote separately / in scope / decline** (the AI only prepares the decision material). Route pricing decisions to your own estimation and pricing process.
4. Anything decided in chat, meetings, or hallway conversations must be written back as an issue comment. Enforce "discuss on the issue; record decisions on the issue."

Why: when decisions scatter outside the issue, the issue starts lying and stops being the source of truth. In contract work, the issue thread itself accumulates as your change-management audit trail for free.

Weekly triage checklist → references/issue-driven-dev.md §6.

## Step 5: Choose a branch strategy

| Strategy | What it is | When to choose it |
|---|---|---|
| **GitHub Flow** (default) | `main` is always deployable. Feature branch → PR → review → merge → deploy | Frequently-deployed SaaS/web work. When in doubt, pick this |
| **Trunk-based development** | Everyone (every agent) merges short-lived branches into `main` at least daily; unfinished features hide behind feature flags | Only when strong test automation and flag discipline already exist |
| Git Flow | Permanent develop/release branches | Only when the client mandates a standing release train. Otherwise overkill (guideline as of 2026) |

**The practical difference between the first two is only whether branch lifetime is capped at 1–2 days and whether feature-flag discipline exists.** Spend your time capping branch lifetime, not debating names.

CI quality gates, branch protection, deploy/release strategy design → $cicd-release-design.

## Step 6: Delegate to agents

- **The issue IS the agent's prompt.** Acceptance criteria become the agent's completion conditions and test spec verbatim.
- Delegation pattern: human dictates → AI drafts requirements → issue created → **human vets the acceptance criteria** → assign to an agent.
- When AI bulk-generates issues, **a human vets each one before it gets `ready`**. Why: mass-produced sloppy issues become noise and burn your triage bandwidth.
- To raise parallelism, reduce dependencies between issues (Step 2's vertical slicing) before adding more agents.
- When human review bandwidth becomes the bottleneck, first build automation that removes human touchpoints (CI gates, formalized acceptance criteria). Why: adding parallel agents does not add human judgment bandwidth.

## Step 7: Keep records — ADR vs Design Doc vs AGENTS.md

| Document | Granularity / lifespan | Purpose |
|---|---|---|
| **ADR** | One decision per file, **immutable** (reverse via a new superseding ADR) | Record the decision and its rationale |
| **Design Doc** | Per feature/system. Written before implementation; historical artifact after | Build consensus and explore options before building |
| **AGENTS.md / README** | Per repository, continuously updated | The current truth (shared entry point for humans and AI) |

- **Separation principle**: a Design Doc explores options and builds agreement; an ADR records a decision. Do not mix them.
- When to write an ADR: **mandatory for decisions touching architecture, technology selection, external integrations, or security.** Everything else can live in an issue comment. Rule of thumb: write down every decision a successor (or an AI) would ask "why is it like this?" about.
- Never rewrite an ADR after the fact. To reverse it, write a new ADR that supersedes it. Why: rewriting makes the history lie.
- Design Docs favor speed over polish; the main goal is pre-implementation feedback.
- **Keep ADRs (immutable record) and AGENTS.md (present tense) in separate roles**: an ADR freezes the moment of decision; AGENTS.md holds only the current truth and is updated continuously. Why: a stale "current truth" is worse than no document — AI agents will trust the outdated information.
- What to put in (and leave out of) AGENTS.md → $conventions-as-guardrails Step 3.
- Accumulate past projects' ADRs as a reusable asset — context you can inject into agents on the next project (your organization's knowledge base).

ADR / Design Doc templates → references/issue-driven-dev.md §4.

## Step 8: Enforce review discipline

- **Small CLs**: when in doubt, split smaller than feels natural. Why: the purpose of review is "improving the long-term health of the codebase," and oversized PRs are unreviewable.
- **Response SLO: within 1 business day.** Why: review latency decides whether review culture lives or dies.
- Use **Conventional Comments** prefixes (`nit:` `suggestion:` `issue:` `question:` …) to make each comment's weight explicit → references/issue-driven-dev.md §5.
- **AI first-pass review + human final approval**: AI covers exhaustiveness (every line — security, convention violations, obvious bugs); humans cover judgment (design decisions, business fit).
- Never accept AI findings at face value. Verify against primary sources (actual files, command output) before acting on them.
- The approval bar is "definite improvement," not "perfect" (better, not perfect).

## Completion checklist

Confirm at the end of each work cycle:

- [ ] The issue has acceptance criteria, and all are checked off
- [ ] The PR contains `Fixes #N` and merging closed the issue
- [ ] Implementation was verified with evidence → $verification-loop
- [ ] Decisions made outside the issue (chat, meetings) were written back to the issue
- [ ] No decision requiring an ADR (architecture / tech selection / external integration / security) went unrecorded
- [ ] No change to the "current truth" left AGENTS.md out of date

## Boundaries (pointers to other skills)

- Verifying implementation completion, evidence-based done criteria → $verification-loop
- TDD, SOLID, coding conventions, design principles → $best-practices
- Root-cause investigation for bug issues → $dev-debug
- Independent review / second opinion → $codex-collab
- Test techniques that make acceptance criteria verifiable, test planning → $test-design
- CI/CD quality gates, branch protection, deploy strategy → $cicd-release-design
- What belongs in AGENTS.md and convention design → $conventions-as-guardrails
- Upstream requirements definition and its decomposition into issues → hand off to your organization's requirements process (no dedicated skill in this repo)
- Client consensus-building and scope-change negotiation → handle through your client-communication / project-management process
- Estimation, pricing, contract terms → out of scope here; route to your own estimation and pricing process

---

Note: statements touching contracts — acceptance inspection (kenshū), contract triage, change management — are practical patterns, not legal advice (guidelines as of 2026; verify primary sources). Leave final judgment to a qualified lawyer.
