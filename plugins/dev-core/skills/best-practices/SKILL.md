---
name: best-practices
description: "Dev-core coding standards: TDD cycle, SOLID, naming, hardcoding bans, Feature-Sliced Design, Clean Architecture, DDD, OWASP security checklist, and refactoring rules. Reference skill loaded by dev-core workflow skills; invoke explicitly with $best-practices when planning, implementing, reviewing, or refactoring code against these standards."
---

# Dev Core Best Practices

Single source of truth for the coding standards that all dev-core workflow skills assume. These are the project conventions to enforce, not general explanations.

## 1. TDD Cycle (t-wada style)

Red → Green → Refactor → Commit:

1. **Red**: Write one failing test for a single behavior. It must fail because the implementation does not exist yet.
2. **Green**: Write the minimum code that makes the test pass. Add nothing speculative.
3. **Refactor**: Improve quality while keeping tests green — remove duplication, improve names, reduce complexity.
4. **Commit**: Commit each meaningful unit of work.

## 2. SOLID

Enforce all five; the two most often violated in review:

- **SRP**: One module/class/function = one reason to change.
- **DIP**: High-level modules depend on abstractions, never on concrete infrastructure.

OCP, LSP, and ISP apply as usual; flag violations in review rather than re-deriving theory.

## 3. Coding Conventions

### Hardcoding bans

- Magic numbers: extract to named constants (`const MAX_RETRY = 3`).
- Config values (API keys, URLs, paths): environment variables or config files.
- UI strings: constants or locale files.

### Naming

- `camelCase`: variables, functions, methods (`getUserById`, `isActive`)
- `PascalCase`: classes, types, interfaces, components (`UserService`, `ButtonProps`)
- `UPPER_SNAKE_CASE`: constants (`MAX_RETRY_COUNT`, `API_BASE_URL`)
- `kebab-case`: file and directory names (`user-service.ts`)

### Style

- DRY: remove duplication as soon as it appears.
- Early returns / guard clauses over deep nesting.
- Immutability: `[...array, item]`, `{ ...obj, key: val }`; never mutate in place.
- File size: aim for 200–400 lines, split above 500. Functions ≤ 50 lines.
- Ternaries only for simple cases; nested ternaries are banned.

### TypeScript

- `strict` mode on; `any` is banned — use `unknown` plus type guards.
- Explicit return types on exported functions.
- Import order: external libraries → internal absolute imports → relative imports.

## 4. Feature-Sliced Design (FSD)

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

Business logic owns the interfaces; infrastructure implements them:

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

## 7. Security (OWASP Top 10 checklist)

- **A01 Access control**: authorization on every endpoint, no horizontal privilege escalation, correct CORS.
- **A02 Cryptography**: encrypt sensitive data, force HTTPS, modern algorithms only.
- **A03 Injection**: ORM/parameterized queries, auto-escaping output, no shell string interpolation.
- **A04 Insecure design**: threat-model new surfaces; defense in depth.
- **A05 Misconfiguration**: no default credentials, disable unused features.
- **A06 Vulnerable components**: dependencies current; `npm audit` (or ecosystem equivalent) clean.
- **A07 Authentication**: strong password policy, MFA where available, secure session management.
- **A08 Integrity**: CI/CD pipeline safety, dependency integrity checks.
- **A09 Logging**: log security events, protect logs from tampering.
- **A10 SSRF**: validate URLs, restrict internal network access.

Always:

- Schema-based input validation (zod, Laravel Validation, etc.) on the server side — client-side validation is UX only.
- Secrets live in environment files excluded from git; commit `.env.example` as the template; scan diffs for secrets before committing.
- Financial systems additionally require: ACID transaction atomicity, double-spend prevention, audit logs, rate limiting; Web3 requires wallet signature verification and MEV protection.

## 8. Refactoring Moves

Prefer these named, behavior-preserving moves: extract method, rename for clarity, replace magic number with constant, simplify conditional, extract class/module, delete dead code.
