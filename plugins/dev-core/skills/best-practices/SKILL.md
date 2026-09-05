---
name: best-practices
description: "Dev-core coding standards: TDD cycle, SOLID, naming, hardcoding bans, Feature-Sliced Design, Clean Architecture, DDD, OWASP security checklist, and refactoring rules. Reference skill loaded by dev-core workflow skills; invoke explicitly with $best-practices when planning, implementing, reviewing, or refactoring code against these standards."
---

# Dev Core Best Practices

Use these defaults when the target repository has no more specific convention.
Preserve the user's scope and established architecture; do not impose a framework
or expand a focused fix into a structural migration.

## 1. TDD Cycle (t-wada style)

Red → Green → Refactor → Evidence:

1. **Red**: Write one failing test for a single behavior. Confirm failure because the required behavior is missing or incorrect, not because of unrelated setup.
2. **Green**: Write the minimum code that makes the test pass. Add nothing speculative.
3. **Refactor**: Improve quality while keeping tests green — remove duplication, improve names, reduce complexity.
4. **Evidence**: Run focused verification and record the result. Commit a meaningful unit only when the user or delivery workflow explicitly authorizes commits.

## 2. SOLID

Use these design heuristics when they solve a concrete coupling or change problem:

- **SRP**: One module/class/function = one reason to change.
- **DIP**: Keep domain policy independent of volatile infrastructure; introduce an abstraction when the boundary benefits from substitution or isolation.

OCP, LSP, and ISP apply as usual; flag violations in review rather than re-deriving theory.

## 3. Coding Conventions

### Hardcoding bans

- Magic numbers: extract to named constants (`const MAX_RETRY = 3`).
- Config values (API keys, URLs, paths): environment variables or config files.
- UI strings: constants or locale files.

### Naming

Follow the target repository's naming and formatter configuration. Use language
conventions as a fallback; the table is illustrative, not a mandate to rename files.

| Language | Variables/functions | Classes/types | Constants | Files |
|---|---|---|---|---|
| TypeScript/JS | camelCase | PascalCase | UPPER_SNAKE_CASE | kebab-case (`user-service.ts`) |
| Rust | snake_case | PascalCase | SCREAMING_SNAKE_CASE | snake_case (`user_service.rs`) |
| Python (PEP 8) | snake_case | PascalCase | UPPER_SNAKE_CASE | snake_case (`user_service.py`) |
| Go | camelCase (exported: leading capital) | same | MixedCaps | lowercase (`userservice.go`) |

Universal across languages: intention-revealing names, no cryptic abbreviations, `is`/`has`/`can` prefixes for booleans.

### Style

- Extract repeated domain knowledge when it has a stable shared meaning; tolerate similar-looking code when an abstraction would couple unrelated behavior.
- Early returns / guard clauses over deep nesting.
- Immutability: don't mutate shared data in place — produce updated values (JS: `[...array, item]`; Python: new comprehensions / `dataclasses.replace`; Rust: ownership and `&mut` already enforce this — follow the borrow rules).
- Treat size as a review signal. Split for cohesion, testability, or an enforced repository limit; do not flag a bug solely because a function crosses a line count.
- Ternaries only for simple cases; nested ternaries are banned.

### Type strictness (per language)

Prefer types and explicit validation at boundaries. Follow configured strictness;
document necessary escape hatches and keep their scope narrow. Resolve routine
implementation choices without a new approval; escalate a material contract or
security change outside existing authority.

- **TypeScript**: `strict` on; `any` banned — use `unknown` plus type guards. Explicit return types on exported functions. Import order: external → internal absolute → relative.
- **Rust**: `cargo clippy -- -D warnings` must pass. `unwrap()`/`expect()` only in main, tests, or documented invariants. Every `unsafe` block needs a reason comment.
- **Python**: mypy or pyright as a CI gate. `Any` / `type: ignore` only with a reason. Type annotations required on new code; strict-mode existing code module by module.
- **Go**: `go vet` + golangci-lint must pass. No gratuitous `interface{}`/`any`.

## 4. Feature-Sliced Design (FSD) — frontend only

**Scope**: FSD is a **SPA/web-frontend methodology** (`widgets` = page building blocks). Do not apply it to backends, CLIs, batch jobs, Cloudflare Workers, or a Tauri Rust core — use the Clean Architecture layering below there. The universal rule is "dependencies point inward (toward the domain)"; directory naming follows the target platform.

Layers depend strictly downward; no cross-dependencies within a layer; `shared` is usable from anywhere.

```
src/
├── app/       # pages, global config
├── widgets/   # page-level building blocks
├── features/  # user-facing features
├── entities/  # business entities
└── shared/    # UI kit, utils, config
```

Slice layout: `features/<name>/{api,model,ui,index.ts}` — `index.ts` is the only public API.

## 5. Clean Architecture

Business logic owns the interfaces; infrastructure implements them. The abstraction mechanism is per language: TS `interface` / Rust trait / Python `typing.Protocol` or ABC / Go interface.

Typical non-frontend layout (directory names follow language conventions):

```
src/
├── domain/          # entities, value objects, repository interfaces (zero external deps)
├── application/     # use cases (depend on domain only)
├── infrastructure/  # concrete DB / external API implementations
└── presentation/    # HTTP handlers / CLI / Tauri commands (keep as thin adapters)
```

In Tauri, `#[tauri::command]` functions are thin presentation-layer adapters; domain logic lives in a Tauri-independent crate testable with plain `cargo test`. In Cloudflare Workers, keep Hono handlers equally thin and inject Env bindings at the infrastructure layer.

TypeScript example of the dependency inversion:

```typescript
// Domain (entities) — interface definition
interface ClientRepository {
  findById(id: string): Promise<Client>;
}

// Application (features) — use case depends on the abstraction
class GetClientUseCase {
  constructor(private repo: ClientRepository) {}
  async execute(id: string) { return this.repo.findById(id); }
}

// Infrastructure (features/api) — concrete implementation
class DBClientRepository implements ClientRepository {
  async findById(id: string) { /* DB access */ }
}
```

## 6. DDD

- Entities carry identity; value objects are immutable and self-validating:

```typescript
class ClientName {
  constructor(private readonly value: string) {
    if (value.length < 2) throw new Error("Client name must be at least 2 characters");
  }
}
```

- Access aggregates only through their root; keep transaction boundaries aligned with aggregates; persist via repositories.

## 7. Security review

Use the applicable OWASP edition when a numbered standard is required; the
following are risk areas, not a claim of compliance or a versioned Top 10 mapping.

- **Access control**: authorization at protected boundaries; CORS is not authorization.
- **Cryptography**: protect sensitive data in transit and at rest.
- **Injection**: parameterized queries, output escaping, argument-safe process calls.
- **Design/configuration**: inspect changed trust boundaries and unsafe defaults.
- **Supply chain/integrity**: audit project dependencies and CI inputs; inspect untrusted agent input and output before privileged use.
- **Authentication**: preserve session and identity guarantees.
- **Logging**: retain useful security evidence without leaking sensitive data.
- **SSRF**: validate outbound destinations and constrain internal access.
- **Exceptional conditions**: handle partial failure, retries, resource exhaustion, and recovery without silently reporting success.

Always:

- Schema-based input validation (zod, Laravel Validation, etc.) on the server side — client-side validation is UX only.
- Secrets live in environment files excluded from git; commit `.env.example` as the template; scan diffs for secrets before committing.
- Financial systems additionally require: ACID transaction atomicity, double-spend prevention, audit logs, rate limiting; Web3 requires wallet signature verification and MEV protection.

## 8. Refactoring Moves

Prefer these named, behavior-preserving moves: extract method, rename for clarity, replace magic number with constant, simplify conditional, extract class/module, delete dead code.
