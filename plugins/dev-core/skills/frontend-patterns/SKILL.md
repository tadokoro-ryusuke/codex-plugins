---
name: frontend-patterns
description: "Web frontend implementation patterns for component, state, form, data-flow, accessibility, and performance changes. Use when implementing or reviewing UI code."
---

# Frontend Patterns

Follow the target frontend's component conventions, dependencies, and rendering
model. These principles also apply to a Tauri WebView; they do not prescribe a
framework migration or a redesign of the requested product. Confirm library choices
from the project's dependency manifest and `AGENTS.md`, and framework APIs from the
official documentation. Facts below marked with a date were checked on 2026-10-26.

## Components and state

Compose around cohesive behavior and stable interfaces. Split when ownership,
reuse, or testability improves; line count alone is not a reason to split.
Use typed props, constrained variants, and children or slots where composition
helps. Extract behavior into hooks or composables so it can be tested apart from
rendering. Keep state local, lift it only as far as sharing requires, and use the
project's store for state that truly crosses those boundaries. Do not copy server
data into a store; the layer that fetched it (router loader or query library)
owns its cache.

## Forms and permissions

Reuse the project's validation and form tooling. Keep field rules consistent
across applicable boundaries without exposing server-only logic to the client.
Show actionable field errors and retain recoverable input after failure.
Branch on server error codes, not message text. Server-side validation and
authorization remain authoritative; requests can bypass the UI, so hidden controls
and client validation alone do not enforce either contract.

Write schemas for the project's library major version. Zod 4 moved string formats
to top-level APIs (`z.email()`), and the method forms such as `z.string().email()`
are deprecated but still work; a Zod 3 project keeps the method form
(https://zod.dev/v4/changelog). Check that form-library resolvers support that
major version.

## Data flow

Design the loading, empty, error, and success states that apply; do not forget
the empty state. Keep one layer responsible for caching and revalidating each piece
of data, so a router loader and a query library do not fetch it independently and
go stale separately. For optimistic updates, define failure recovery (restore the
previous view and tell the user what was not saved) and reconcile with the server
response (server-assigned IDs, corrected values) or revalidate.

Choose the fetching mechanism from the rendering model and trigger:

| Situation | Mechanism |
|---|---|
| Route data in an SSR or Server Components framework | Server side (Server Component or router loader) |
| Route data in a SPA or Tauri WebView | Router loader if present, or the existing query library |
| User-triggered work | Event handler (an action or mutation for writes) |
| Cached client data | The existing query library |

Do not bring SSR or per-request server fetching into a SPA or Tauri project. Tauri
serves the frontend as a static web host and does not natively support
server-based approaches such as SSR (https://v2.tauri.app/start/frontend/).
Do not add a query dependency just to satisfy a generic preference.

In React, prefer the mechanisms above to fetching in `useEffect`. When an effect
must own a request, its cleanup must ignore or abort stale responses
(https://react.dev/learn/synchronizing-with-effects):

```tsx
useEffect(() => {
  let ignore = false;
  fetchUser(id).then((user) => {
    if (!ignore) setUser(user);
  });
  return () => {
    ignore = true;
  };
}, [id]);
```

Replacing existing effect-based fetching changes loading behavior, fetch timing,
and caching. Do it only when the request includes it; otherwise fix missing cleanup
or report it.

Examples of optimistic update mechanics: React 19 `useOptimistic` shows the
optimistic value only while the action runs and then reverts to the source state,
so update the parent state only on success and catch errors to show them
(https://react.dev/reference/react/useOptimistic). TanStack Query either refetches
to restore the true value on failure, or saves the previous value in `onMutate`,
restores it in `onError`, and revalidates in `onSettled`
(https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates).

## React 19 and React Compiler

Use these only when the project is on React 19 or later (stable since 2024-12-05,
https://react.dev/blog/2024/12/05/react-19) or has adopted the compiler.

- Group submissions and mutations into Actions; use `<form action={fn}>` with
  `useActionState` for pending state, errors, and results.
- A successful `<form action>` resets uncontrolled fields
  (https://react.dev/reference/react-dom/components/form). If validation errors are
  returned rather than thrown, inputs can be lost; return the submitted values and
  restore them through `defaultValue`, or use controlled inputs.
- React Compiler 1.0 is stable since 2025-10-07
  (https://react.dev/blog/2025/10/07/react-compiler-1). Where it is adopted, leave
  memoization of new code to the compiler and keep `useMemo`/`useCallback` as escape
  hatches for precise control, such as stable effect dependencies. Keep existing
  memoization; removing it can change compiled output, so remove it only with
  thorough tests. Without the compiler, memoize only where measurement shows a benefit.

## Accessibility implementation

Follow the project's design system and accessibility checklist for WCAG
conformance checks, color, spacing, and contrast. In the implementation:

- Use native elements (`<button>`, `<a href>`, `<label>`, `<dialog>`) whenever they
  provide the needed semantics and behavior instead of rebuilding them with ARIA
  roles; they already handle keyboard, focus, and announcements
  (https://www.w3.org/TR/using-aria/).
- Move focus into a dialog when it opens. On close, return focus to the element
  that opened it, or to the logical next element if that one is gone or the
  workflow clearly continues elsewhere
  (https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).
- On client-side route changes, unless the framework announces them, move focus to
  the new page's heading or main region or announce the change in a live region;
  without a page reload, screen reader users may not notice the navigation.
- Set `aria-invalid="true"` on a field that failed validation (not before
  validation) and link its error text with `aria-describedby`
  (https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA21,
  https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA1). After a failed submit, move
  focus to the first invalid field or an error summary.
- Announce asynchronous status changes ("Saved", "N results", "Failed to load")
  without moving focus, through a live region: `role="status"`, or `role="alert"`
  for urgent errors (https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
  Render the live region empty before announcing; inserting the element and its
  content at once may not be read
  (https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions).
- Under `prefers-reduced-motion: reduce`, stop or reduce non-essential animation
  (https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).
- Preserve keyboard operation and focus position through loading and re-rendering;
  do not remove the focused element.

## Performance

Measure the affected path before adding memoization, virtualization, code splitting,
or other complexity; an unmeasured optimization leaves only the complexity.

For public web pages, use Core Web Vitals. "Good" means LCP at most 2.5 s, INP at
most 200 ms, and CLS at most 0.1, judged at the 75th percentile of page loads,
separately for mobile and desktop; INP replaced FID in 2024
(https://web.dev/articles/vitals). Judge with field data (CrUX or RUM). Lab INP
depends on the interactions performed; without interactions, Total Blocking Time is
a proxy but not a replacement (https://web.dev/articles/inp). Where field data is
unavailable, such as a Tauri WebView or an internal SPA, check the same aspects
(load speed, input responsiveness, layout shift) with lab runs and long-task
measurements.

- LCP: do not lazy-load the LCP image; raise its priority with
  `fetchpriority="high"` when needed (https://web.dev/articles/optimize-lcp).
  Lazy-load images outside the viewport.
- CLS: give images and video `width`/`height` or a CSS `aspect-ratio`, and reserve
  space for late embeds and ads (https://web.dev/articles/optimize-cls).
- Fonts: set `font-display` explicitly and choose its value by measurement; it
  affects LCP, FCP, and layout shift differently
  (https://web.dev/articles/font-best-practices).
- INP: split tasks longer than 50 ms and yield to the main thread; defer
  non-urgent work until after the next paint
  (https://web.dev/articles/optimize-long-tasks).
- Lazy-load by route or heavy component, virtualize long lists when measurement
  shows a benefit, and serve appropriately sized images through the framework's
  image feature when one exists.

## Testing

Cover changed executable behavior with the project's tests. Write them as in
`../best-practices/references/testing.md`; locate elements by role and accessible
name first and treat test ids as an agreed contract (its section 9). Use
`$test-design` for test allocation decisions and `$verification-loop` for execution
evidence. A passing component test in jsdom or similar does not establish browser,
device, or production behavior; check layout, focus movement, and real network
behavior with E2E or manual observation.
