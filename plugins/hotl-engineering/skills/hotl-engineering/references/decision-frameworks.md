# Decision Frameworks

Decision tables, criteria, and anti-patterns for use in advisory mode. Tools for translating
the principles (principles.md) into concrete decisions. Numbers reference the corresponding principle.

---

## F1. Risk-tier determination (Principle 5)

| Question | If Yes |
|---|---|
| Does it touch authentication, authorization, or permission filters? | Tier 2 |
| Does it touch the DB schema or a migration? | Tier 2 |
| Does it touch data flow across a confidentiality boundary (MNPI, personal data)? | Tier 2 |
| Does it change CI/CD, branch protection, or the workflow definitions themselves? | Tier 2 |
| None of the above, and it's only docs, added tests, or a dependency patch? | Tier 0 |
| Anything else | Tier 1 |

When in doubt, round up to the higher tier. However, if Tier 2 exceeds 30% of all PRs, the path definition is too broad.

## F2. Autonomy promotion criteria (Principle 4)

| Current → Next | Promotion condition (guideline) |
|---|---|
| Read-Only → Advised | Initial-investigation conclusions match the human's conclusion ≥ 70% (last 10 cases) |
| Advised → Approved | The human adopts the proposed action as-is ≥ 80% (last 20 cases) + zero cases where the proposal was harmful |
| Approved → Autonomous | 20 consecutive incident-free approved executions of the same operation type + the operation is reversible + the blast radius is defined |

Promote per operation type ("restarts are Autonomous, scaling changes are Approved" is a normal state).
A single serious incident triggers a two-stage demotion; feed the cause back into the golden set / runbook (Principle 11).

## F3. Buy vs. build (Principle 12) — especially AI SRE, monitoring, and review SaaS

Before considering a purchase, ask these in order:
1. What is the product's core value? If it's "automating context assembly," in-house is likely sufficient
2. Build an in-house Read-Only version (existing agent platform + read permissions + a boilerplate prompt) in
   one week — what gap remains unfilled? Is the price justified by that gap?
3. Are the vendor's effectiveness numbers (e.g., MTTR reduced by X%) measured at your own organization's scale?
   Have you discounted the positioning talk typical of a crowded market?
4. Where is the data sent? Is it compatible with confidentiality requirements (data residency)?
5. What is the cost of ripping it back out (lock-in: proprietary instrumentation, proprietary data formats)?

Domains where "buy" tends to be right: reliability-critical plumbing such as on-call management and
notification delivery, and commodity vulnerability databases. Domains where "build" tends to be right:
decision logic tightly coupled to your own data and your own permission model.

## F4. Criteria for switching to a new model or tool (Principles 7, 8)

1. Compare the current and new versions under identical conditions using your own eval set (golden set).
   Treat benchmark articles as reference values only
2. Check the must-pass category results first. Reject the switch if must-pass regresses even when the
   average improves
3. Record cost (token unit price × measured consumption) and latency at the same time
4. Ship the switch as a single agent version in one PR (run it through the eval-gate even if only the
   model ID changes)
5. Confirm the rollback procedure (a pointer to the previous version) before promoting

## F5. Criteria for enabling auto-merge (Principles 3, 5)

Do not enable auto-merge until all of the following are Yes:
- The mechanical Tier 0 determination (paths + dependency-patch check) has run for 4 weeks with zero misclassifications
- All gates (5 layers) run stably as required checks, with false positives under one per week
- Post-hoc monitoring: a mechanism for automatic revert after merge, or a deploy that can be rolled back immediately
- Audit explanation: "the scope and conditions of auto-merge" is documented

Even after enabling it, keep the scope to Tier 0 only. Extending to Tier 1 is generally not recommended —
from the Principle 2 (cognitive bandwidth) perspective, the value is thin relative to the risk spike.

## F6. Permission design for contractors and new members

- Cap repository permissions at Write. Grant branch-protection bypass to no one
- Run contractor deliverables through the same gates (do not vary the gate by person; only the tier varies)
- Use AGENTS.md / CODEOWNERS / skills as "onboarding material." Writing with the same norms and the same
  tools from day one keeps quality variance down
- For repositories handling confidential data, give contractors access only to a sanitized environment
  (staging with dummy data)

## F7. Ordering principle for rollout of a new mechanism (Principles 1, 6)

Rolling out a new mechanism must always follow: ① a dedicated owner (one person is enough) builds it
first → ② make the first users productive from day one → ③ an observation period → ④ enforcement →
⑤ expanding the autonomy scope. Company-wide rollout that skips ①, or enforcement that skips ③, is a
failure pattern.

---

## Anti-pattern catalog (call these out when you see them)

- **day-one enforcement**: Enforcing from day one with no calibration → the whole tool gets ripped out over false positives (Principle 6)
- **boiling frog baseline**: An eval with only a relative threshold and no absolute floor (Principle 8)
- **over-formalized spec**: A lengthy spec document for a single CRUD endpoint. Calibrate spec depth to the tier
- **bloated MCP / tool definitions**: Turning something a CLI would handle into an MCP tool, squeezing context.
  Always question the token cost of a tool definition
- **kitchen sink session**: Mixing unrelated tasks into one session and polluting the context
- **automation without verification**: Promoting to Autonomous on "it worked, so it's fine" (Principles 3, 4)
- **write-once-and-forget norms**: AGENTS.md / a golden set with no update rule (the 24-hour rule, the
  twice rule) (Principle 11)
- **escaping into the average**: Mixing a boundary that should be must-pass (permissions, injection) into
  the score average (Principle 9)
- **hollowed-out human approval**: CP2 has become a ritual of "it's green, so approve immediately." The
  choice is either raise the quality of the evidence presented (a review-perspective summary) or drop that
  tier to Tier 0
