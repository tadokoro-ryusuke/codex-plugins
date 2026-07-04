---
name: frontend-patterns
description: "Framework-agnostic frontend patterns: component composition, props design, state management scope, schema-based forms, data fetching, performance. Reference skill loaded by dev-core workflow skills; invoke explicitly with $frontend-patterns when building or reviewing UI code."
---

# Frontend Patterns

Framework-agnostic frontend conventions. For framework-specific APIs (React hooks, Vue Composition API, …), consult the project's `AGENTS.md`, official docs, or available MCP connectors instead of guessing.

## Component design

Compose small single-responsibility components:

```
Card
├── CardHeader  # title
├── CardBody    # content
└── CardFooter  # actions
```

Props:

- Type-safe definitions (TypeScript / prop types); constrain `variant`, `size`, etc. with union types.
- Defaults for optional props; use children/slots for composition.

Size: aim ≤ 200 lines per component, split above 300; extract logic into custom hooks / composables.

## State management

- **Local state first**: keep state inside the component when it doesn't need to be shared.
- **Lift minimally**: move to the parent only when sharing requires it.
- **Global stores sparingly**: only truly global concerns (auth, theme).
- Library choice (Pinia, Zustand, Jotai, …) follows the project — check `AGENTS.md`, README, and package metadata before introducing anything.

## Forms

- Schema-based validation (zod / yup); define the schema once and reuse it.
- Server-side validation is mandatory — client-side validation is UX only.
- Show inline errors per field.

```typescript
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  password: z.string().min(8),
});
```

Form library follows the project (VeeValidate, react-hook-form, …) — check before adding.

## Data fetching

- Always model the three states: loading / error / data.
- Cache + revalidate with the project's query library (TanStack Query, SWR, Vue Query).
- Optimistic updates where UX benefits; reconcile on server response.
- SSR: fetch on the server for SEO and first paint; let the cache library own client refetching.

### Avoid `useEffect` for data fetching (React)

Fetching in `useEffect` breeds race conditions, double fetches, and missing cleanup. Prefer, in order:

```typescript
// Bad: fetching in useEffect
useEffect(() => {
  fetchData().then(setData);
}, []);

// Good 1: Server Component (fetch on the server)
async function Component() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// Good 2: event handler when the fetch is user-initiated
function handleClick() {
  fetchData().then(setData);
}

// Good 3: data-fetching library (cache + revalidation included)
const { data } = useSWR("/api/data", fetcher);
```

## Performance

- Memoize only expensive computations — avoid reflexive memoization.
- Lazy-load by route and for heavy components.
- Virtualize long lists.
- Optimize images: lazy loading, correct sizes, framework facilities (e.g. next/image).
