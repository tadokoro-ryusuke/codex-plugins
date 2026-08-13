---
name: test-design
description: "Test strategy, test design, and acceptance-criteria authoring: test plans, test-perspective matrices, test-case design, acceptance test specs and result reports, coverage policy, pyramid/trophy allocation, how much E2E to write, technique selection (equivalence partitioning, boundary values, decision tables, state transitions, pairwise), risk-based prioritization, and flaky-test policy. Designs tests — it does not run them (execution and evidence reporting: $verification-loop). Reference skill; invoke explicitly with $test-design when planning test strategy, designing test cases, or drafting acceptance criteria."
---

# Test Design — Test Strategy, Test Design, Acceptance Criteria

**Boundary: this skill covers the design question — where to place tests, how deep, and with which technique. Test execution and evidence-based completion judgment → $verification-loop.**

In contract development, tests feed directly into client acceptance (the formal pass/fail judgment on deliverables — *kenshū* in Japanese practice) and into contract non-conformity liability. So test planning starts at the **estimation and contract stage**, not after implementation.
Why: when acceptance criteria arrive late, you personally absorb both the "he said, she said" dispute risk and the full cost of rework.

## Division of labor: what AI does / what only humans may decide

| AI (the agent running this skill) does | Only humans may decide |
|---|---|
| Draft the test-perspective matrix | What NOT to test (risk acceptance) |
| Mechanically expand techniques into cases (equivalence classes, boundary values) | Finalizing acceptance criteria and getting client agreement |
| Backfill unit tests on existing code | Final verdict on test *quality* (rejecting tests that only look like tests) |
| Run exploratory testing via a browser agent | Approving risk-based priorities (which features get shallow coverage) |
| Detect flaky tests and propose quarantine | Approving the overall test strategy and scope |

Why split it this way: some reports find no significant correlation between AI-generated test volume and issue resolution (a guideline as of 2026 — verify against primary sources). Use AI as an **amplifier on top of human-owned acceptance criteria**, never as the owner.

## Step 1: Pick a test allocation model from the project type

Choose exactly one allocation model first, and state it in the test plan.
Why: without a declared allocation, tests pile up wherever they are easiest to write — manual checks and E2E.

1. **Test pyramid** (the default): unit tests as the base at 70–80%, integration in the middle, E2E kept minimal
   - Why: the economics of execution speed, maintenance cost, and debugging signal overwhelmingly favor the lower layers
2. **E2E covers only the happy paths of the most critical user journeys.** Rule of thumb: 5–15 scenarios
   - Why: more E2E feels safer, but flakiness destroys CI credibility long before the safety materializes
3. **Testing trophy** (Kent C. Dodds): a variant that makes integration (component-integration) tests the thickest layer

| Project type | Recommended model | Notes |
|---|---|---|
| API / backend-centric | Pyramid | Make domain-logic unit tests the thickest layer |
| Frontend-centric (React/Next, etc.) | Trophy | Component-integration tests match reality best |
| Business systems (complex state & permissions) | Pyramid | Weight decision-table and state-transition techniques (Step 4) |
| Unsure | Pyramid | Adjust with risk-based weighting (Step 2) |

**The ice-cream cone (inverted pyramid) is forbidden.** Depending on manual testing plus E2E is the classic contract-work failure pattern.
Why: every fix inflates regression effort until defect handling turns the project unprofitable.

## Step 2: Weight test depth by risk

**A plan that tests every feature at equal depth is forbidden.**
Why: an equal-depth plan degrades into everything-half-done the moment the schedule slips.

1. Prioritize each feature by "failure impact × probability of occurrence"
2. Tier the depth by priority:
   - **High**: technique-driven case design + automated tests + exploratory testing
   - **Medium**: automated tests for the main happy and error paths
   - **Low**: happy path only, or explicitly "not tested" with accepted risk
3. Every "not tested" decision requires explicit human approval and goes into the test plan
   - Why: risk acceptance is a contractual liability judgment — never territory an AI decides on its own

## Step 3: Build the test-perspective matrix

Alongside external design, build a feature × perspective matrix.
Why: the matrix is the parent of your acceptance criteria. Closing gaps in "angles of attack" before writing cases is far cheaper than after.

Template (add or drop perspective columns per project):

| Feature | Normal | Error | Boundary | Permissions | Performance | Compatibility |
|---|---|---|---|---|---|---|
| Login | Y | Y (lockout after repeated failures) | Y (password min/max length) | — | Y (concurrent logins) | Y (target browsers) |
| Order entry | Y | Y (out of stock, double submit) | Y (quantity 0 / upper limit) | Y (per-role allow/deny) | — | — |
| … | | | | | | |

- Each cell gets more than Y/—: add one representative perspective in parentheses
- A "—" is a declaration of "not tested" and must be treated as Step 2 risk acceptance
- Reserve one slot for **exploratory testing** (session-based, with a charter and a time box) as the final critique before acceptance
  - Why: a solo contractor has no independent QA department — this is the only place an off-script, customer's-eye check is guaranteed

## Step 4: Choose techniques and expand into cases

Turn each matrix cell into cases using ISTQB techniques. The canonical reference is the ISTQB Foundation Level syllabus.

| Technique | What it does | When to use |
|---|---|---|
| Equivalence partitioning | Split inputs into equivalence classes, test one representative each | First move for every input field. Minimizes case count |
| Boundary value analysis | Target the boundary ±1 | Numeric ranges, string lengths, dates. Bugs cluster at boundaries |
| Decision table | Enumerate condition combinations in a table | Multi-condition business rules: discount logic, permission checks |
| State transition testing | Cover states and (valid/invalid) transitions | Screen flows, status management (orders, approval flows) |
| Pairwise | Compress combinatorial explosion via 2-factor coverage | OS × browser × role combinations. Standard tool: Microsoft PICT |

- The mechanical expansion (enumerating cases after classes are drawn) can be delegated to AI. **Humans review the class boundaries and the correctness of expected results**
- Why: expansion is mechanical, but one wrong equivalence class silently invalidates every case built on it

## Step 5: Judge test quality with Khorikov's four pillars

Judge written tests (especially AI-generated ones) against the four pillars from Vladimir Khorikov's *Unit Testing Principles, Practices, and Patterns*:

1. **Resistance to refactoring**: does it test observable behavior, not implementation detail (does it survive internal restructuring)?
2. **Protection against regressions**: can this test catch a real bug (or is it an assertion-free "runs the code" test)?
3. **Fast feedback**: does it run quickly (slow tests stop being run)?
4. **Maintainability**: is the intent readable, is it easy to change?

Coverage policy rules:
- Run the coverage threshold (e.g. 80%) as a **ratchet — it never goes down**
  - Why: chasing the number alone mass-produces tests with zero regression-detection power, and a lowered threshold never recovers
- For critical logic, apply mutation-testing thinking: "could I write a bug that this test fails to catch?"

## Step 6: Contract-work acceptance flow — agree on acceptance criteria before signing

**Note: this section is a practical playbook, not legal advice. It reflects Japanese contract-development practice (acceptance / *kenshū*, contract non-conformity liability) as of 2026 — verify primary sources, and leave final contractual judgments on acceptance clauses and liability to a qualified lawyer. Pricing and effort decisions follow your own estimation process.**

Why this ordering: fixing acceptance criteria before the contract is signed is the cheapest known prevention for acceptance disputes.

1. **Estimation stage**: draft acceptance criteria from the test-perspective matrix (target features, perspectives, environments, exclusions)
2. **Before contract**: agree the acceptance criteria with the client and bind them to the contract (statement of work, purchase order, etc.)
   - Enforce "no issue enters implementation without acceptance criteria" from this point on → $issue-driven-dev
3. **At end of requirements definition**: finalize the test plan (scope, per-level policy, environments, exit criteria, risk-based priorities)
4. **Before delivery**: execute the acceptance test spec and deliver with the result report attached

Deliverable shapes:

- **Acceptance test specification**: one entry per client-agreed acceptance criterion — "ID / linked acceptance criterion / preconditions / inputs & steps / expected result / test environment"
- **Acceptance test result report**: "execution date / executor / environment / pass-fail per case / evidence (screenshots, logs, other execution artifacts) / failed items and remediation plan / open issues and agreements"
  - Why evidence is mandatory: acceptance is a contractual pass/fail judgment, and "it probably works" without execution output is not evidence (the execution side of this principle is $verification-loop's Iron Law)

## Step 7: Operating rules (the AI-agent era)

1. **Separate test generation and test review into different agents/sessions**
   - Why: an agent asked to test its own implementation tends to write self-justifying tests that merely ratify what it built
2. **Humans own the canonical acceptance criteria.** AI drafts and expands the matrix and cases; it never finalizes the criteria
   - Why: acceptance criteria ARE the decision of what to build — the pass/fail line of acceptance must not be delegated to AI
3. **Quarantine flaky tests immediately.** Pull them from CI until fixed and open a quarantine issue
   - Why: tolerated flaky tests spread CI distrust until every quality gate becomes theater. CI-side gate design → $cicd-release-design
4. Review AI-generated tests against the Step 5 pillars before merging. Volume is not an outcome
5. When using E2E self-healing or agent-driven exploratory testing, humans predefine the judgment criteria (what counts as a failure)

## Test-plan review checklist

Self-check before finalizing the plan; resolve every unmet item before requesting human approval:

- [ ] Allocation model (pyramid/trophy) chosen with a project-type rationale
- [ ] E2E limited to happy paths of the most critical journeys (guideline: 5–15)
- [ ] Not an ice-cream cone (manual + E2E dependent)
- [ ] Per-feature risk priorities exist; depth is not uniform across features
- [ ] "Not tested" areas are written down and a human approved the risk acceptance
- [ ] Test-perspective matrix exists (feature × normal/error/boundary/permissions/performance/compatibility)
- [ ] Techniques (Step 4) selected per perspective
- [ ] Acceptance criteria client-agreed before contract (or the agreement flow is in the plan)
- [ ] Coverage threshold defined with ratchet operation (never lowered)
- [ ] Flaky quarantine rule and generation/review agent separation built into operations

## Boundaries (one-line pointers)

- Test execution, 6-step verification, evidence-based completion → $verification-loop
- TDD workflow, how to write test code, design principles → $best-practices
- Root-causing test failures → $dev-debug
- Writing and splitting issues with acceptance criteria → $issue-driven-dev
- CI quality gates, coverage gates, quarantine implementation → $cicd-release-design
- Turning requirements into acceptance criteria, and walking the client through them → hand off to your requirements-definition and client-agreement process
- Independent review from a second model → $codex-collab

## Canonical resources

- Martin Fowler, "The Practical Test Pyramid" (martinfowler.com) / Mike Cohn, *Succeeding with Agile*
- ISTQB Foundation Level syllabus (free; JSTQB publishes the Japanese edition), ISO/IEC/IEEE 29119
- Vladimir Khorikov, *Unit Testing Principles, Practices, and Patterns*
- Lisa Crispin & Janet Gregory, *Agile Testing* (origin of the Agile Testing Quadrants)
- *Software Engineering at Google*, testing chapters (Small/Medium/Large test sizes)
- Juichi Takahashi, *知識ゼロから学ぶソフトウェアテスト* and *ソフトウェアテスト技法練習帳* (Japanese-language classics on test techniques)
