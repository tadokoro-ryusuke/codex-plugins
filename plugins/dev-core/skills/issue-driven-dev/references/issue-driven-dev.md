# issue-driven-dev — detailed reference

Detailed material referenced from SKILL.md by § number. Copy the templates as-is and adjust only the minimum needed to fit the project.

## §1 Three Issue Forms (YAML) templates

Place the following three files in `.github/ISSUE_TEMPLATE/`. Unlike Markdown templates, Issue Forms enforce input fields structurally, so "issues without acceptance criteria" are blocked at the form level.

### §1.1 Bug report — `bug_report.yml`

```yaml
name: Bug report
description: Report behavior that differs from what is expected
title: "[Bug]: "
labels: ["type/bug", "status/needs-triage"]
body:
  - type: textarea
    id: summary
    attributes:
      label: What is happening (current behavior)
      description: Observed facts only. Put speculation under "Technical notes"
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Numbered steps. Include the reproduction rate (always / sometimes / specific conditions)
      placeholder: |
        1. ...
        2. ...
        3. ...
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS / browser / app version / environment (production, staging, local)
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Error logs / screenshots
      description: Full error messages and stack traces
  - type: textarea
    id: notes
    attributes:
      label: Technical notes (optional)
      description: Suspected cause, files likely involved, recent related changes
```

### §1.2 Feature request — `feature_request.yml`

```yaml
name: Feature request
description: Propose a new feature or improvement
title: "[Feature]: "
labels: ["type/feature", "status/needs-triage"]
body:
  - type: textarea
    id: background
    attributes:
      label: Background / why it is needed
      description: The problem this feature solves. Who is hurting (business context)
    validations:
      required: true
  - type: textarea
    id: story
    attributes:
      label: User story
      placeholder: "As a ..., I want to ..., because ..."
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance criteria
      description: Verifiable conditions as checkboxes. These become the completion conditions and the test spec verbatim
      placeholder: |
        - [ ] Condition 1
        - [ ] Condition 2
    validations:
      required: true
  - type: textarea
    id: out_of_scope
    attributes:
      label: Out of scope
      description: State explicitly what this issue will NOT do
    validations:
      required: true
  - type: textarea
    id: notes
    attributes:
      label: Technical notes (optional)
```

### §1.3 Task — `task.yml`

```yaml
name: Task
description: A unit of work such as refactoring, configuration change, or investigation
title: "[Task]: "
labels: ["type/chore", "status/needs-triage"]
body:
  - type: textarea
    id: background
    attributes:
      label: Background / why
    validations:
      required: true
  - type: textarea
    id: work
    attributes:
      label: Work description
      description: What to do and how. One line is fine if under 30 minutes or self-evident
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Completion conditions
      description: Required for work over 30 minutes, and for any work delegated to an AI agent
      placeholder: |
        - [ ] Condition 1
```

Note: setting `blank_issues_enabled: false` in `config.yml` prevents blank issues that bypass the templates (enable it once the workflow has settled).

## §2 The 3-axis label system and initial milestone set

### §2.1 Label definitions

Hold the line at 3 axes × at most 5 labels each. When you want more attributes, use GitHub Projects custom fields instead.

| Label | Meaning |
|---|---|
| `type/bug` | Fixing behavior that differs from expectations |
| `type/feature` | New feature or improvement |
| `type/chore` | Refactoring, dependency updates, configuration, investigation |
| `type/docs` | Documentation-only change |
| `priority/P0` | Immediate. Production incident or security issue. Stops other work |
| `priority/P1` | Handle within the current milestone |
| `priority/P2` | Handle in a later milestone |
| `priority/P3` | Someday. Review quarterly and consider closing |
| `status/needs-triage` | Unsorted (default for new issues) |
| `status/ready` | Acceptance criteria vetted by a human. Assignable to an agent |
| `status/blocked` | Cannot start due to a dependency or external factor (state the reason in a comment) |

Operating rules:

- `status/ready` is proof that "a human has vetted the acceptance criteria." An AI that bulk-generated issues must never mark its own issues `ready`.
- When applying `status/blocked`, always comment what is blocking and what unblocks it.
- Never create cross-axis labels (e.g., `urgent-bug`). One label per axis per issue.

### §2.2 Milestone operation

- Cut milestones **per release** (e.g., `v1.2.0`) or **per contract phase** (e.g., `Phase 2: Payments`). Never by any other unit (weeks, people).
- Always set a due date. The due date and completion rate (closed/total) become visible automatically; in contract development this backs client reporting and billing evidence.
- Do not force issues into a milestone they don't belong to (no empty milestones, no "misc" bucket). Manage the backlog with `priority/*` and triage instead.

## §3 Real examples of good issues (pass / fail)

### §3.1 Passing example

> **Title**: Allow resending the password reset email
>
> **Background / why**: Reset emails frequently land in spam, and users churn while locked out. One of the top support-ticket categories.
>
> **Current vs expected**: Currently no resend is possible for 60 minutes after a reset request. Expected: the resend button becomes enabled after a 60-second cooldown.
>
> **Acceptance criteria**:
> - [ ] The "Resend" button becomes enabled 60 seconds after a reset request
> - [ ] Resending invalidates the previous token and issues a new one
> - [ ] Resend requests within 60 seconds return 429, and the UI shows the remaining cooldown seconds
> - [ ] Automated tests cover the three points above
>
> **Out of scope**: Email template redesign; SMS-based reset.
>
> **Technical notes**: The existing RateLimiter middleware can likely be reused for rate limiting.

Why it passes: an implementer (human or AI) can start from this alone, the acceptance criteria are the test spec verbatim, and the explicit out-of-scope section keeps the implementation from ballooning.

### §3.2 Failing example, and how to fix it

> **Title**: Make the login stuff nicer

Why it fails, and the fix:

- "Nicer" is unverifiable → rewrite as observable current behavior and expected behavior.
- The concern is unclear (UI? security? performance?) → split into 1 issue = 1 concern.
- No acceptance criteria → if delegated to an agent, the agent ends up deciding its own completion conditions, and a human can no longer judge pass/fail on the result.

Exception: work under 30 minutes and self-evident, like "Fix typo: `recieve` → `receive` in README", may be title + one line. But if it is delegated to an AI agent, write one line of completion conditions even for trivial work.

## §4 ADR / Design Doc templates

### §4.1 ADR template (minimal MADR-style)

Store as `docs/adr/NNNN-<decision-summary>.md` in the repository, version-controlled alongside the code.

```markdown
# NNNN: <the decision in one sentence>

- Status: Accepted   <!-- Proposed / Accepted / Superseded by NNNN -->
- Date: YYYY-MM-DD

## Context

<!-- The situation that made this decision necessary. Constraints. What the problem was -->

## Decision

<!-- What was decided. State it in one declarative sentence -->

## Consequences

<!-- What gets better, what gets worse, and the trade-offs accepted -->

## Alternatives Considered

<!-- Options not taken, and why not -->
```

Supersede procedure:

1. To reverse a decision, **do not edit** the existing ADR. Create a new ADR with a new number.
2. In the new ADR's Context, write "Supersedes NNNN. Reason: …".
3. Change the old ADR's Status to `Superseded by NNNN` (the Status line is the only line that may ever change).

When to write one: every decision a successor (or an AI agent) would ask "why is it like this?" about. Mandatory for decisions touching architecture, technology selection, external integrations, or security.

### §4.2 Design Doc structure (Google-style)

Write before implementing. Speed over polish — the main goal is pre-implementation feedback. After implementation, do not update it; keep it as a historical artifact.

```markdown
# <Feature name> Design Doc

## Context and Scope
## Goals and Non-Goals
## Design
<!-- System diagram, data flow, APIs, data model. Make trade-offs explicit -->
## Alternatives Considered
## Cross-cutting Concerns
<!-- Security, privacy, observability, migration -->
```

How the two documents differ:

| | Design Doc / RFC | ADR |
|---|---|---|
| Role | Explore options and build agreement | Record a decision |
| Timing | Before implementation | Right after deciding |
| Updates | Frozen after implementation (historical) | Immutable (supersede to reverse) |
| Length | A few pages is fine | One decision per file, short |

Contract-development caution: do not conflate the design deliverables you owe the client with the internal Design Docs written for yourself and your agents. The scope and format of client deliverables is set by the contract — generate deliverable documents FROM your ADRs/Design Docs, so you never maintain two sources of truth.

### §4.3 Separating ADRs (immutable record) from AGENTS.md (present tense)

README is the human entry point; AGENTS.md is the operating document for AI agents; both are "continuously updated present tense." That is a different role from the ADR, which is an immutable record: an ADR freezes the moment of decision, and reversal happens via a new superseding ADR. AGENTS.md holds only the current truth and is committed immediately on every change (freshness IS its reliability). Why: a stale present-tense document is worse than none — an AI will trust the outdated information and act on it. Past projects' ADR sets become reusable assets you can inject into agents as context on the next project, so add "can an AI reconstruct the context by reading this?" to your document-quality criteria.

What to put in and leave out (keep it thin, no duplicated ownership) → $conventions-as-guardrails Step 3.

## §5 Review discipline in detail

### §5.1 Conventional Comments quick reference

Make each comment's weight (must-fix or not) explicit with a prefix. The goal is that the reviewee — human or AI — can tell whether action is required.

| Prefix | Meaning | Action |
|---|---|---|
| `praise:` | Calling out something good | None |
| `nit:` | Trivial point (matter of taste) | Optional |
| `suggestion:` | Improvement proposal | Must consider; adoption optional |
| `question:` | Question for understanding | Answer required |
| `thought:` | Idea for the future | None (consider filing an issue) |
| `issue:` | Problem that needs fixing | Action required |
| `issue (blocking):` | Problem that blocks merge | No merge until resolved |

### §5.2 Review operating rules

- **Small CLs**: when in doubt, split smaller than feels natural. 1 PR = 1 issue = 1 concern keeps PRs naturally small.
- **Response SLO: within 1 business day.** A full review is not required — even "I'll look at this today" meets the SLO. Silence is what kills review culture.
- The approval bar is "definite improvement," not "perfect" (better, not perfect). If the change improves the codebase's health over time, let it through.
- Review for design and readability. A review that only checks "does it work" duplicates the automated tests and adds no value.

### §5.3 AI first-pass review + human final approval

| Role | What it covers |
|---|---|
| AI (first pass) | Exhaustive line-by-line check: security, convention violations, obvious bugs, missing tests |
| Human (final approval) | Judgment: design decisions, business fit, match against acceptance criteria, merge decision |

Operating cautions:

- Never accept AI findings at face value. Verify against primary sources (actual files, command output) before acting on them.
- Do not let the agent that wrote the implementation review its own work or generate its own tests (it becomes self-justifying). Separate review into a different agent or a different session.
- How to request an independent review → $codex-collab.

## §6 Weekly triage procedure

Run once a week on a fixed day (do not skip — a backlog of needs-triage shows up directly as lost throughput).

### §6.1 Procedure checklist

1. [ ] Open every `status/needs-triage` issue, oldest first
2. [ ] Close detected duplicates, leaving a link to the canonical issue
3. [ ] Apply `type/*` and `priority/*`
4. [ ] Route client-request issues through the contract triage gate (§6.2)
5. [ ] Vet acceptance criteria; promote to `status/ready` only those that pass the bar
6. [ ] Assign milestones (leave the rest in the backlog)
7. [ ] Check unblock conditions on `status/blocked` issues; move unblocked ones to `ready`
8. [ ] Decide whether to split any giant issue that has stayed open for weeks
9. [ ] Quarterly: sweep `priority/P3` — close what you decide not to do, with the reason written down

AI agents can be trusted with drafts for steps 1–3 (label proposals, duplicate detection, priority suggestions). Final calls on 4–9 are made by humans.

### §6.2 Contract triage gate (contract development only)

A human sorts every client-request issue into one of three buckets before any work starts:

| Bucket | Meaning | Next action |
|---|---|---|
| In scope | Covered by the current contract and scope | Normal triage (assign priority) |
| Quote separately | Out of scope; needs a new agreement | Route to your estimation and pricing process. Do not start implementation before agreement |
| Decline | Not doable for technical, contractual, or policy reasons | Write the reason on the issue and close it (how to communicate this to the client is a consensus-building problem — handle it in your client-communication process) |

Why the gate matters: without it, out-of-scope work silently piles up unpaid and leaves no change-management trail. Recording the sorting result and its reason on the issue is itself your change-management evidence in contract work.

Note: practices touching contracts and acceptance inspection (kenshū) are practical patterns, not legal advice (guidelines as of 2026; verify primary sources). Have a lawyer confirm anything that feeds back into contract clauses.
