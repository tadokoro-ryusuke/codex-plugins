---
name: frontend-patterns
description: "Web frontend implementation patterns for component, state, form, and data-flow changes. Use when implementing or reviewing UI code."
---

# Frontend Patterns

Follow the target frontend's component conventions, dependencies, and rendering
model. These principles also apply to a Tauri WebView; they do not prescribe a
framework migration or a redesign of the requested product.

## Components and state

Compose around cohesive behavior and stable interfaces. Split when ownership,
reuse, or testability improves; line count alone is not a reason to split.
Use typed props, constrained variants, and children or slots where composition
helps. Keep state local, lift it only as far as sharing requires, and use the
project's store for state that truly crosses those boundaries.

## Forms and permissions

Reuse the project's validation and form tooling. Keep field rules consistent
across applicable boundaries without exposing server-only logic to the client.
Show actionable field errors and retain recoverable input after failure.
Server-side validation and authorization remain authoritative; hidden controls
and client validation alone do not enforce either contract.

## Data flow

Model loading, empty, error, and successful states as applicable. Preserve the
project's caching and revalidation ownership so two layers do not fetch the same
data independently. For optimistic updates, define failure recovery and reconcile
with the server response.

Choose the fetching mechanism from the rendering model and trigger: server or
router loading for route data, an event handler for user-triggered work, and the
existing query library for cached client data. If a React effect owns a request,
handle cleanup and stale responses. Do not force Server Components into a client
SPA or add a query dependency just to satisfy a generic preference.

## Performance and verification

Measure the affected path before adding memoization, virtualization, or other
complexity. Use route-level loading and appropriately sized media when the
measured workload benefits. Preserve keyboard operation, focus behavior, and
accessible error feedback through state changes.

Cover changed executable behavior with the project's tests. Use `$test-design`
for test allocation decisions and `$verification-loop` for execution evidence;
a local component test does not establish browser, device, or production behavior.
