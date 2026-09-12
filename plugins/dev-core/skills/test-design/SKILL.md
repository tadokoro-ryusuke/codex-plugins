---
name: test-design
description: "Test strategy and case design for changed behavior or acceptance planning. Use when selecting coverage, designing cases, or drafting verifiable acceptance criteria."
---

# Test Design

Design where tests belong and which failures they must detect. Start from the
user's acceptance criteria and the repository's existing suite. Execute checks and
judge completion through `$verification-loop` when that work is requested; a test
plan is not evidence that the behavior passed.

Reuse accepted scope and approvals. Choose routine techniques and proportional
coverage within that scope. Preserve required gates; reserve material reductions
of acceptance coverage, product pass/fail changes, and unresolved release-risk
acceptance for the authorized owner.

## Choose coverage by contract and risk

Inspect existing tests before adding more. Reuse tests that already prove the
contract and extend them only for a missing meaningful assertion or scenario.
For changed executable behavior, follow the repository's TDD discipline. Do not
add tests that only mirror implementation, wording, or generated file structure.

Place tests at the lowest level that proves the contract, with integration tests
at real boundaries. Cover critical journeys and relevant permission, failure,
and recovery paths in E2E when lower layers cannot establish them. Use pyramid or
trophy thinking if useful; avoid a universal ratio, E2E count, or coverage target.
Retain device or exploratory checks where their observation cannot be automated
meaningfully, and state their limits.

Weight depth by failure impact and likelihood. Record omitted checks as not
applicable, deferred, blocked, or explicitly waived; those statuses are different.
Do not weaken a required gate or count a retry-until-green result as proof.

## Turn risks into cases

For a strategy or substantial feature, use a feature × perspective matrix to expose
gaps before expanding cases. Select relevant columns such as normal, error,
boundary, permissions, performance, and compatibility; a focused bug does not
need a full project matrix.

| Technique | Use when |
|---|---|
| Equivalence partitioning | Representative input classes exercise different behavior |
| Boundary values | Range, length, date, or threshold edges may change the result |
| Decision tables | Several business conditions determine the outcome |
| State transitions | Valid and invalid transitions govern behavior |
| Pairwise | Configuration combinations grow rapidly; separately cover known higher-order risks |

Derive expected results from authoritative requirements or domain behavior, not
from the implementation under test. Resolve ambiguous business boundaries with
the owner when existing decisions do not determine them. Generated case volume
is not a substitute for correct classes and expected results.

## Judge test quality

Check whether each test detects a plausible regression, observes public behavior,
survives internal refactoring, gives useful failure feedback, and is maintainable.
For critical logic, ask which incorrect implementation could still pass. Preserve
the repository's coverage gate and inspect uncovered changed behavior; percentage
alone is not proof of correctness.

Review tests independently from implementation claims. Use bounded independent
review when warranted and authorized, or critically inspect locally; this does not
prohibit an implementer from writing TDD tests. Run exploratory work with a stated
question and time boundary when it adds evidence beyond scripted checks.

Investigate flakes using the preserved first failure and a bounded diagnostic retry.
An authorized quarantine needs an owner, expiry, tracked failure, and replacement
coverage for critical paths. Do not create external issues without authority.

## Contract acceptance only when in scope

For a client acceptance plan, specification, or result-report format, read
[contract acceptance](references/contract-acceptance.md). Do not add client sign-off
to routine internal engineering. Prepare complete reviewable drafts using existing
decisions; do not claim contractual agreement or test execution without evidence.

Hand back the coverage decisions, meaningful cases or changed tests, and the
remaining uncertainties relevant to the requested scope. Distinguish proposed
checks from executed evidence and required owner decisions.
