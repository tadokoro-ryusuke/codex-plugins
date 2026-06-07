---
name: frontend-patterns
description: "Frontend architecture patterns for component design, state management, forms, API boundaries, accessibility, and framework-agnostic UI implementation. Use when building or reviewing frontend code."
---

# Frontend Patterns

フレームワーク非依存のフロントエンド設計パターン。フレームワーク固有の API（React hooks, Vue Composition API など）は、プロジェクトの `AGENTS.md`、公式ドキュメント、または利用可能な MCP/connector から確認してください。

## コンポーネント設計

### コンポジションパターン

小さく再利用可能なコンポーネントを組み合わせて構築する。1コンポーネント = 1責任。

```
Card
├── CardHeader  # タイトル表示
├── CardBody    # コンテンツ
└── CardFooter  # アクション
```

### Props 設計

- 型安全な Props 定義（TypeScript / PropType）
- `variant`, `size` 等はユニオン型で制限
- オプショナルな Props にはデフォルト値
- children / slots で合成可能に

### コンポーネントサイズ

- 200行以下を推奨
- 300行超で分割を検討
- ロジックはカスタムフック/Composableに抽出

## 状態管理

### 原則

- **ローカルステート優先**: コンポーネント内で完結する状態はローカルで管理
- **リフトアップは最小限**: 共有が必要な場合のみ親に移動
- **グローバルストアは慎重に**: 認証状態、テーマ等の本当にグローバルなもののみ

### 推奨ライブラリ

- **Vue 3**: Pinia（公式推奨）
- **React**: Zustand（軽量）、Jotai（アトミック）
- 選定はプロジェクトの `AGENTS.md`、README、package metadata を確認

## フォーム実装

### バリデーション戦略

- **スキーマベース**: zod / yup でバリデーションスキーマを定義
- **サーバーサイドバリデーション**: 必ず実施（クライアントのみに頼らない）
- **エラー表示**: フィールドごとにインラインエラー表示

```typescript
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  password: z.string().min(8),
});
```

### フォームライブラリ

- **Vue 3**: VeeValidate + zod
- **React**: react-hook-form + zod
- 選定はプロジェクトの `AGENTS.md`、README、package metadata を確認

## データフェッチ

### 原則

- **ローディング/エラー/データ** の3状態を常に管理
- **キャッシュ**: SWR / TanStack Query / Vue Query でキャッシュ + 再検証
- **楽観的更新**: UX向上のため、サーバー応答前にUIを更新

### サーバーサイドレンダリング（SSR）

- データフェッチはサーバーサイドで実行（SEO、初期表示速度）
- クライアントサイドでの再フェッチはキャッシュライブラリに委任

## パフォーマンス最適化

- **メモ化**: 計算コストの高い処理のみ（過剰なメモ化は避ける）
- **遅延読み込み**: ルート単位、重いコンポーネント単位
- **仮想スクロール**: 大量リスト表示時
- **画像最適化**: 遅延読み込み、適切なサイズ、next/image 等のフレームワーク機能活用
