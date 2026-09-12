# Batch design

Specify the unit of work, business date or equivalent run key, trigger, window,
dependencies, inputs and outputs, commit boundary, failure behavior, and rerun
procedure for each job. Use stable IDs across the job list, job net, and specs.

| Job ID | Purpose | Trigger | Window | Depends on | Rerun method | Error records |
|---|---|---|---|---|---|---|
| J020 | Daily sales aggregation | J010 completion | 02:00–03:00 | J010 | Rebuild the selected business date | Quarantine with tracked recovery |

Chain dependent jobs on explicit completion or data-readiness signals; elapsed
clock time is not evidence that a predecessor finished. Keep asynchronous child
work visible to the workflow's completion and recovery accounting.

## Idempotency and recovery

Define the observable guarantee: repeating the same run unit and parameters must
not duplicate business effects. Choose a mechanism suited to the operation:

- A processed status requires atomic claiming and completion semantics.
- DELETE/INSERT requires a bounded run unit and protection against partial rebuilds.
- UPSERT requires correct uniqueness keys and defined conflict behavior.
- External side effects may need idempotency keys, an outbox, or compensation;
  a database-only pattern does not cover them automatically.

Pass the business date as an explicit argument for date-based jobs. Do not derive
that business identity from the current time on a later retry; use clock time for
execution metadata where appropriate. Define whether recovery resumes failed work
or reruns a safely repeatable unit, including partial commits and skipped records.

Address duplicate launches, concurrency, overrun monitoring, and the production
volume assumptions. Specify the required behavior rather than mandating a new
scheduler or lock service when the existing platform already provides it.

## Business failure decisions

Reuse agreed priorities for online opening versus batch completion, stop versus
skip behavior, downstream handling of error records, and incident escalation.
Prepare proposed criteria when undecided, but do not finalize a business tradeoff
or claim client sign-off without owner authority. Record whose decision is needed
and which delivery or operation depends on it; continue other authorized design.
