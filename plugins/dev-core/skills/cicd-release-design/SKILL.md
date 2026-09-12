---
name: cicd-release-design
description: "CI/CD and release design for pipeline, rollout, or rollback work. Use when creating or reviewing delivery gates and production promotion plans."
---

# CI/CD and Release Design

Design the requested delivery change against the repository's actual pipeline,
runtime, and operating authority. Distinguish deploy (placing code in an
environment) from release (exposing behavior to users). Reuse existing commands,
providers, and runbooks; do not introduce an unrelated delivery platform.

## Select the current work

- For pipeline checks, workflow permissions, or credential handling, read
  [pipeline design](references/pipeline-design.md).
- For rollout strategy, flags, migrations, or rollback, read
  [release and recovery](references/release-and-recovery.md).
- For diagnosing a failing existing pipeline, use `$dev-debug`; for designing test
  depth, use `$test-design`. Load either only when needed.

## Preserve delivery invariants

Verify the exact revision and environment that will be promoted. Keep required
contract and security gates blocking; do not lower thresholds or defer a required
check merely to satisfy a timing target. Treat local tests, CI, deployed state,
and user-visible behavior as distinct evidence.

Design permissions for the actual effect. Reuse recorded approval and bounded
recovery authority; do not ask again for the same authorized action. Preparing a
workflow or runbook does not itself authorize changing remote protections,
reading credentials, deploying, or notifying customers. Keep owner decisions on
release risk and permission expansion explicit while completing authorized drafts.

Hand back the changed pipeline or runbook, verification evidence, and any remaining
promotion decision. Include only the applicable rollout, flag, or migration
artifacts. When delivery metrics are in scope, verify the current framework's
primary definitions and measure a service over time rather than individual output.
