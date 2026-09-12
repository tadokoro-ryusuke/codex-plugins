---
name: backend-patterns
description: "Backend implementation patterns for API, data-access, and domain changes. Use when implementing or reviewing these boundaries."
---

# Backend Patterns

Follow the target repository's contracts, language idioms, and architecture. Use
these patterns where they solve the current problem; do not introduce a new
layering scheme for a focused change. Check project dependencies and official
framework documentation before choosing concrete APIs.

## API contracts

Preserve established endpoint naming, response shapes, and status-code semantics.
Validate untrusted inputs and enforce authorization at the server boundary.
Keep success and error responses unambiguous; use a discriminated union when the
project has no established shape. Do not replace an existing public contract merely
to match an example.

## Domain and persistence boundaries

Keep business policy independent of volatile infrastructure when substitution,
testing, or multiple adapters make that boundary useful. Use the existing service
or use-case shape; a class with a single `execute` method is an option, not a rule.
Introduce a repository interface when it provides a meaningful domain boundary,
not as a mandatory wrapper around every ORM call.

Return expected failures using the language's established mechanism. Use Rust's
native `Result` and Go's `(T, error)`; use dedicated exceptions or established
structured returns in Python. At serialization boundaries such as Tauri commands,
map domain errors to a serializable public error without leaking internal details.
For TypeScript, follow the project's Result or exception convention rather than
adding a competing one.

## Transactions and external effects

Group writes that must succeed atomically in a transaction. Define the boundary
from the business invariant rather than wrapping unrelated writes together.
Use consistent lock ordering where locking is required, and inspect the ORM's
actual transaction semantics.

A database transaction does not make an email, payment, or remote API call atomic.
Keep remote latency outside held database locks; use the project's outbox,
idempotency, or compensation mechanism when durable cross-system effects matter.
Do not report all effects as completed when only the database commit succeeded.

## Caching

For cache-aside behavior, check the cache, read the source on a miss, and populate
the cache. Define invalidation on writes and TTLs for the use case. Include tenant,
identity, or permission scope in keys where it affects the result; do not let cached
authorization-sensitive data cross those boundaries.

Use `$best-practices` for TDD and shared coding standards, or `$test-design` when the
change needs a test strategy beyond the existing suite.
