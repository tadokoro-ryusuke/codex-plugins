---
name: best-practices
description: "Dev-core coding standards for TDD and maintainable implementation. Use when applying or reviewing these standards in a code change."
---

# Dev Core Best Practices

Use these defaults where the target repository has no more specific convention.
Preserve the user's scope and established architecture; do not expand a focused
fix into a structural migration or add tooling just to match this reference.

## TDD for executable behavior

Use Red → Green → Refactor → Evidence:

1. Write one failing test for the changed behavior and confirm that failure comes
   from the missing or incorrect behavior, not unrelated setup.
2. Implement the minimum repair that satisfies the contract.
3. Refactor while the focused tests stay green.
4. Run the relevant verification and record actual results.

Reuse meaningful coverage when it already exercises the contract. Judge tests by
failures they detect, not count or wording matches. For documentation and other
non-executable changes, use appropriate content or structural validation instead
of tests that mirror the edit. Commit only under existing user or delivery authority.

## Cohesion and boundaries

Extract shared knowledge when it has a stable shared meaning; tolerate similar
code when an abstraction would couple unrelated behavior. Use dependency inversion
where it isolates volatile infrastructure from domain policy. Treat SOLID and DDD
as design heuristics, not requirements to introduce classes or repositories.

Use the repository's architectural model:

- Apply Feature-Sliced Design only to a frontend that uses it. Preserve its layer
  dependency rules and public slice APIs; do not apply `widgets`/`features` directory
  conventions to a backend, CLI, Worker, or Tauri Rust core.
- Where Clean Architecture is used, keep domain policy independent of infrastructure
  and transport adapters. Keep Tauri commands or HTTP handlers thin where a domain
  boundary exists; use the language's interface, trait, or protocol idiom.
- Where aggregates are used, access them through their root and align atomic writes
  with their invariants. Model identity separately from immutable value semantics.

## Coding conventions

Follow project naming, formatting, import order, and configured strictness. Prefer
intention-revealing names, guard clauses, and types plus explicit boundary validation.
Extract constants for domain meaning or repeated policy; use config for values
that vary by environment and the existing localization mechanism for UI text.
Do not turn a literal used once into an abstraction without a concrete benefit.

Keep unsafe operations and type escape hatches narrow and justified. Follow the
language's constraints: prefer `unknown` with validation to unrestricted TS `any`;
document Rust `unsafe` and non-test panic assumptions; explain Python type-ignore
exceptions; avoid Go `any` where a useful type is available. Run the checks the
repository requires instead of imposing a new linter or type checker on every task.

Avoid mutation of shared state when it obscures ownership. Split by cohesion,
testability, or an enforced limit; line counts alone do not establish a defect.
Resolve routine implementation choices within scope. Escalate material changes to
public contracts, security guarantees, or owner decisions outside existing authority.

## Security at changed boundaries

Inspect the trust boundaries affected by the change:

- Enforce authentication and authorization where protected actions occur; CORS and
  hidden UI are not authorization.
- Validate untrusted inputs, parameterize queries, escape output, and pass process
  arguments safely. Validate outbound destinations where SSRF is relevant.
- Keep secrets and sensitive data out of source, logs, and generated artifacts.
  Use the repository's credential mechanism and inspect the diff before delivery.
- Preserve dependency and CI integrity. Treat agent inputs and outputs as untrusted
  before privileged use.
- Handle partial failure, retries, exhaustion, and recovery without reporting success
  for unfinished effects. Protect financial operations against duplicate effects and
  preserve their transaction and audit invariants when those operations are in scope.

Use current primary standards when a versioned compliance mapping is requested;
this checklist alone does not establish compliance.

Use `$frontend-patterns` or `$backend-patterns` for implementation boundaries,
`$test-design` for strategy, and `$verification-loop` for execution evidence only
when the current task needs that material.
