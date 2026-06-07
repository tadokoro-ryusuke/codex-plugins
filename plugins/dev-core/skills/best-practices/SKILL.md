---
name: best-practices
description: "Development best practices for TDD, Feature-Sliced Design, Clean Architecture, DDD, SOLID, coding conventions, refactoring, TypeScript, and security. Use when planning, implementing, reviewing, or refactoring code."
---

# Dev Core Best Practices

全エージェントの共通基盤。コーディング規約・原則・パターンの **Single Source of Truth**。

## 1. TDD サイクル（t-wada 式）

### Red→Green→Refactor→Commit

1. **Red 🔴**: 単一機能の失敗するテストを1つ作成。実装は存在しないため必ず失敗する
2. **Green 🟢**: テストをパスさせる**最小限のコード**を記述。余分な機能は追加しない
3. **Refactor 🔨**: テストをグリーンに保ちながら品質向上。重複排除、命名改善、複雑さの解消
4. **Commit ✅**: 意味のあるまとまりとしてコミット

## 2. SOLID 原則

- **SRP**: 1モジュール/クラス/関数 = 1つの責任。変更理由は1つだけ
- **OCP**: 拡張に開き、修正に閉じる。新機能は既存コード変更なしで追加
- **LSP**: 派生型は基底型と置換可能
- **ISP**: 使わないメソッドへの依存を強制しない
- **DIP**: 高レベルモジュールは低レベルに依存しない。抽象に依存する

## 3. コーディング規約

### ハードコーディング禁止

- **マジックナンバー**: `const MAX_RETRY = 3;` — 数値リテラル直接記述禁止
- **設定値**: 環境変数または設定ファイル（API Key, URL, パス）
- **UI文字列**: 定数や言語ファイルで管理

### 命名規約

- **camelCase**: 変数、関数、メソッド（`getUserById`, `isActive`）
- **PascalCase**: クラス、型、インターフェース、コンポーネント（`UserService`, `ButtonProps`）
- **UPPER_SNAKE_CASE**: 定数（`MAX_RETRY_COUNT`, `API_BASE_URL`）
- **kebab-case**: ファイル名、ディレクトリ名（`user-service.ts`）

### コードスタイル

- **DRY**: コード重複は即座に排除
- **早期リターン/ガード節**: 深いネストを避ける
- **イミュータビリティ**: `[...array, item]`, `{ ...obj, key: val }` — 直接変更しない
- **ファイルサイズ**: 200-400行推奨、500行超で分割検討。関数は50行以下
- **三項演算子**: 単純な場合のみ。ネストした三項演算子は使用禁止

### TypeScript

- **strict mode** 有効
- **any 禁止**: `unknown` + 型ガードを使用
- **明示的な戻り値の型**: 公開関数には必ず型を指定
- **インポート順序**: 外部ライブラリ → 内部モジュール（絶対パス）→ 相対パス

## 4. Feature-Sliced Design (FSD)

### レイヤー構造（上から下へ依存）

```
src/
├── app/       # アプリケーション層（ページ、グローバル設定）
├── widgets/   # ウィジェット層（ページ構成要素）
├── features/  # フィーチャー層（ユーザー向け機能）
├── entities/  # エンティティ層（ビジネスエンティティ）
└── shared/    # 共有層（UI、ユーティリティ、設定）
```

### 依存関係ルール

- 上位層は下位層のみに依存可能
- 同一層内での相互依存は禁止
- shared 層はどこからでも使用可能

### スライス構成

```
features/[feature-name]/
├── api/      # APIクライアント、サーバーアクション
├── model/    # ストア、型、ビジネスロジック
├── ui/       # UIコンポーネント
└── index.ts  # パブリックAPI
```

## 5. Clean Architecture

### 依存性の逆転

- ビジネスロジックは外部依存を持たない
- インターフェースを通じた疎結合
- 詳細（UI、DB）はビジネスルールに依存

```typescript
// Domain層（entities）— インターフェース定義
interface ClientRepository {
  findById(id: string): Promise<Client>;
}

// Application層（features）— ユースケース
class GetClientUseCase {
  constructor(private repo: ClientRepository) {}
  async execute(id: string) { return this.repo.findById(id); }
}

// Infrastructure層（features/api）— 具象実装
class DBClientRepository implements ClientRepository {
  async findById(id: string) { /* DB操作 */ }
}
```

## 6. DDD（ドメイン駆動設計）

### エンティティとバリューオブジェクト

```typescript
// エンティティ（識別子を持つ）
class Client {
  constructor(
    private readonly id: ClientId,
    private name: ClientName,
    private tags: Tag[],
  ) {}
}

// バリューオブジェクト（不変、自己検証）
class ClientName {
  constructor(private readonly value: string) {
    if (value.length < 2) throw new Error("クライアント名は2文字以上必要です");
  }
}
```

### 集約とリポジトリ

- 集約ルートを通じたアクセス
- トランザクション境界の明確化
- リポジトリパターンの実装

## 7. セキュリティ（OWASP Top 10）

### チェックリスト

- **A01 Access Control**: 認可チェックが全エンドポイントに実装、水平権限昇格防止、CORS設定
- **A02 Cryptographic**: 機密データ暗号化、HTTPS強制、安全な暗号アルゴリズム
- **A03 Injection**: SQL/XSS/コマンドインジェクション対策（ORM使用、自動エスケープ）
- **A04 Insecure Design**: 脅威モデリング、防御の深さ
- **A05 Misconfiguration**: デフォルト資格情報変更、不要機能無効化
- **A06 Vulnerable Components**: 依存関係最新、`npm audit` クリーン
- **A07 Authentication**: 強力なパスワードポリシー、MFA、安全なセッション管理
- **A08 Integrity**: CI/CD安全性、依存関係整合性チェック
- **A09 Logging**: セキュリティイベントのログ記録、改ざん防止
- **A10 SSRF**: URL検証、内部ネットワークアクセス制限

### 入力検証

- スキーマベースのバリデーション（zod, Laravel Validation等）
- サーバーサイドバリデーション必須（クライアントのみに頼らない）

### 機密情報保護

- 環境変数の使用（.env.local / .env、.gitignore に追加）
- コミット前の機密情報チェック
- .env.example をコミット可能なテンプレートとして管理

### 金融システム追加チェック

- トランザクション原子性（ACID）、二重支払い防止
- 監査ログ、レート制限
- Web3: ウォレット署名検証、MEV保護

## 8. リファクタリング技法

- メソッドの抽出: 複雑な関数を分割
- 変数/関数の名前変更: 明確性の向上
- マジックナンバーを定数に置き換え
- 条件式の簡略化
- クラス/モジュールの抽出
- デッドコードの排除
