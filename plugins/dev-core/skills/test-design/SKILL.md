---
name: test-design
description: "Test strategy, test design, and acceptance-criteria authoring: test plans, test-perspective matrices, test-case design, acceptance test specs and result reports, coverage policy, pyramid/trophy allocation, how much E2E to write, technique selection (equivalence partitioning, boundary values, decision tables, state transitions, pairwise), risk-based prioritization, and flaky-test policy. Designs tests — it does not run them (execution and evidence reporting: $verification-loop). Reference skill; invoke explicitly with $test-design when planning test strategy, designing test cases, or drafting acceptance criteria."
---

# Test Design — Test Strategy, Test Design, Acceptance Criteria

**Boundary: this skill covers the design question — where to place tests, how deep, and with which technique. Test execution and evidence-based completion judgment → $verification-loop.**

Start from the user's acceptance criteria and the repository's current testing
strategy. Use the contract-work section only for an actual client-acceptance or
contract-planning task. Do not introduce a client-approval workflow into routine
engineering work.

## Division of labor: what AI does / what only humans may decide

| Agent work within authorized scope | Decisions reserved for the owner |
|---|---|
| Draft the matrix and choose proportional checks | Material reduction of agreed acceptance coverage |
| Mechanically expand techniques into cases (equivalence classes, boundary values) | Finalizing acceptance criteria and getting client agreement |
| Write and critically review regression tests | Changes to the product's pass/fail contract |
| Run authorized exploratory testing | Accepting unresolved material release risk |
| Investigate flakes and propose bounded quarantine | Waiving required repository or client gates |

Reuse decisions and approval already present in the task. Judge generated tests
by the defects they detect and the contracts they cover, not by their volume.

## Step 1: Pick a test allocation model from the project type

Choose a useful allocation model and explain it only when the test strategy needs one.
Why: without a declared allocation, tests pile up wherever they are easiest to write — manual checks and E2E.

1. **Test pyramid**: prefer fast, focused lower-level tests where they establish the contract; add integration tests at real boundaries
   - Why: the economics of execution speed, maintenance cost, and debugging signal overwhelmingly favor the lower layers
2. **E2E covers critical journeys and failures that lower layers cannot prove**, including permission denial, recovery, and relevant browser/device integration
   - Bound runtime and flakiness; do not impose a universal scenario count or exclude critical error paths
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
3. Record omitted checks and distinguish not applicable, deferred, blocked, and explicitly waived
   - Choose routine depth within the agreed scope; ask before waiving required coverage or accepting a material release/contract risk not already authorized

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
- Label an empty cell with its reason; not applicable and knowingly waived are different decisions
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
- Preserve the repository's coverage gate and inspect uncovered changed behavior
  - Treat a percentage as a signal, not proof of correctness; do not add a universal target or weaken an agreed gate to turn a failure green
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

1. **Review tests independently from implementation claims**
   - Use a bounded read-only subagent when explicitly authorized by the user or an applicable instruction; otherwise review locally without creating a new user-owned task
2. **Humans own the canonical acceptance criteria.** AI drafts and expands the matrix and cases; it never finalizes the criteria
   - Why: acceptance criteria ARE the decision of what to build — the pass/fail line of acceptance must not be delegated to AI
3. **Investigate flakes before changing gates.** Preserve the first failure and use a bounded diagnostic retry
   - Never count retry-until-green as proof. If quarantine is authorized, retain an owner, expiry, tracked failure, and replacement coverage for critical paths. Create an external issue only when authorized
4. Review AI-generated tests against the Step 5 pillars before merging. Volume is not an outcome
5. When using E2E self-healing or agent-driven exploratory testing, humans predefine the judgment criteria (what counts as a failure)

## Test-plan review checklist

Self-check before finalizing the plan; resolve every unmet item before requesting human approval:

- [ ] Allocation model (pyramid/trophy) chosen with a project-type rationale
- [ ] E2E covers critical journeys and relevant failure/recovery paths without a fixed quota
- [ ] Not an ice-cream cone (manual + E2E dependent)
- [ ] Per-feature risk priorities exist; depth is not uniform across features
- [ ] Omitted checks have reasons; material waivers have explicit owner authorization
- [ ] Test-perspective matrix exists (feature × normal/error/boundary/permissions/performance/compatibility)
- [ ] Techniques (Step 4) selected per perspective
- [ ] Client agreement is addressed when contract acceptance is actually in scope
- [ ] Existing coverage gates are preserved and changed behavior has meaningful assertions
- [ ] Flake diagnosis and authorized independent review are proportionate to risk

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
