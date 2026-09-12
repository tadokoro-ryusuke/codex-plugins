---
name: external-design-deliverables
description: "Screen and batch basic-design deliverables for client review. Use when drafting or reviewing these designs or preparing their agreed delivery."
---

# External Design Deliverables

Prepare screen or batch designs that a client can review and an implementation
agent can use from the same version. Preserve traceable IDs, business decisions,
and the difference between a draft, an agreed specification, and verified behavior.

Use existing requirements, business flows, roles, and prior decisions. Resolve
routine design choices within authorized scope. If an input is missing, identify
its effect and continue the independent draft work with explicit assumptions;
ask only for a decision needed to settle a material ambiguity.

## Select the requested deliverable

Read only the relevant supporting material:

- For screen lists, navigation, wireframes, prototypes, or screen specs, read
  [screen design](references/screen-design.md).
- For job lists, dependencies, batch processing, or rerun behavior, read
  [batch design](references/batch-design.md).
- For a client review package, sign-off record, or agreed delivery, read
  [review and delivery](references/review-and-delivery.md).

API contracts, data models, authorization policy, and error-response contracts
belong to their existing design sources. Cross-reference those sources instead of
silently redefining them in a screen or job spec. Use `$test-design` when expanding
the design into acceptance tests.

## Preserve the agreement boundary

Build from structural decisions toward detail when those decisions remain open.
Reuse agreement already recorded in the task; do not require a new client approval
for every intermediate artifact. Prepare authorized drafts through to a concrete,
reviewable package, including proposed options or assumptions where needed.

Reserve final client sign-off, changes to contractual scope, and unresolved
business risk acceptance for the authorized owner. A design request authorizes
preparation, not contacting the client or claiming their approval. Keep those
external actions within existing user authorization.

Before handing back work, check applicable cross-references and states, distinguish
open decisions from defects, and state exactly what is ready for review or agreed
for delivery. Do not describe a prototype as implemented production behavior.
