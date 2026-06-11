---
name: backend-patterns
description: "Framework-agnostic backend patterns: REST API design, response/Result shapes, Repository, use-case service layer, caching, transactions. Reference skill loaded by dev-core workflow skills; invoke explicitly with $backend-patterns when implementing or reviewing APIs, data access, or domain logic."
---

# Backend Patterns

Framework-agnostic backend conventions. For ORM- or framework-specific APIs (Eloquent, Prisma, etc.), consult the project's `AGENTS.md`, official docs, or available MCP connectors instead of guessing.

## API design

RESTful endpoints:

```
GET    /api/users          # list
GET    /api/users/:id      # detail
POST   /api/users          # create
PUT    /api/users/:id      # update
DELETE /api/users/:id      # delete
```

Response shape — discriminated union, no mixed success/error payloads:

```typescript
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: { code: string; message: string } };
```

Status codes: 200 OK | 201 created | 400 validation | 401 authentication | 403 authorization | 404 not found | 500 server error.

## Repository pattern

```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}
```

Concrete implementations depend on the ORM (Eloquent, Prisma, TypeORM, …). Domain code depends only on the interface (dependency inversion).

## Service layer (use cases)

One use case = one class with a single `execute`. Dependencies injected as abstractions:

```typescript
class CreateUserUseCase {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async execute(input: CreateUserInput): Promise<Result<User>> {
    const validated = CreateUserSchema.parse(input);
    const user = User.create(validated);
    const saved = await this.userRepository.save(user);
    await this.emailService.sendWelcome(saved.email);
    return ok(saved);
  }
}
```

## Result pattern

Return expected failures as values; reserve exceptions for the unexpected:

```typescript
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

const ok = <T>(value: T): Result<T, never> => ({ success: true, value });
const err = <E>(error: E): Result<never, E> => ({ success: false, error });
```

## Caching (cache-aside)

1. Check cache → 2. on miss, read DB → 3. populate cache.
Invalidate on writes; set TTLs per use case rather than one global value.

## Transactions

- Wrap every multi-write operation in a transaction (ACID).
- Prevent deadlocks with a consistent lock ordering.
- The concrete API is framework-specific (`DB::transaction()`, `prisma.$transaction()`, …) — check the project.
