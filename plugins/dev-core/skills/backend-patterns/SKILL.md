---
name: backend-patterns
description: "Backend architecture patterns for API design, Repository, service layer, caching, error handling, Clean Architecture, and DDD. Use when implementing or reviewing backend code, API boundaries, data access, or domain logic."
---

# Backend Patterns

フレームワーク非依存のバックエンド設計パターン。ORM 固有の API（Eloquent, Prisma など）は、プロジェクトの `AGENTS.md`、公式ドキュメント、または利用可能な MCP/connector から確認してください。

## API 設計

### RESTful エンドポイント

```
GET    /api/users          # 一覧取得
GET    /api/users/:id      # 詳細取得
POST   /api/users          # 作成
PUT    /api/users/:id      # 更新
DELETE /api/users/:id      # 削除
```

### レスポンス形式

```typescript
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: { code: string; message: string } };
```

### HTTP ステータスコード

200: 成功 | 201: 作成 | 400: バリデーションエラー | 401: 認証 | 403: 認可 | 404: 未発見 | 500: サーバーエラー

## Repository パターン

```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}
```

具象実装はORM/フレームワークに依存（Eloquent, Prisma, TypeORM等）。インターフェースで抽象化し、依存性逆転を実現。

## サービス層（ユースケース）

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

## Result パターン

```typescript
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

function ok<T>(value: T): Result<T, never> {
  return { success: true, value };
}

function err<E>(error: E): Result<never, E> {
  return { success: false, error };
}
```

## キャッシュ戦略

### Cache-Aside パターン

1. キャッシュ確認 → 2. ヒットしなければDB取得 → 3. キャッシュに保存
- 更新時はキャッシュを無効化
- TTL を適切に設定（ユースケースに応じて）

## トランザクション

- 複数の書き込み操作は必ずトランザクションで囲む
- 原子性（ACID）の保証
- デッドロック防止（一貫したロック順序）
- 具体的なAPI はORM/フレームワークに依存（`DB::transaction()`, `prisma.$transaction()`等）
