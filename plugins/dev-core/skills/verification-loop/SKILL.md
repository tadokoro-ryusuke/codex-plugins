---
name: verification-loop
description: "Evidence-based 6-step verification workflow: build, typecheck, lint, test, security, and diff review. Use when asked to verify changes, finish a coding task, prepare a PR, or prove that checks pass."
---

# Verification Loop

## 6 段階検証フロー

### Step 1: Build Check 🏗️

ビルドが成功することを確認。

```bash
pnpm build
# または
npm run build
```

**チェック項目:**

- コンパイルエラーなし
- バンドルサイズが適切
- 警告の確認

### Step 2: Type Check 📝

TypeScript の型エラーがないことを確認。

```bash
pnpm typecheck
# または
npx tsc --noEmit
```

**チェック項目:**

- 型エラーなし
- strict mode 準拠
- any 使用なし

### Step 3: Lint Check 🔍

コーディング規約に準拠していることを確認。

```bash
pnpm lint
# 自動修正
pnpm lint --fix
```

**チェック項目:**

- ESLint エラーなし
- 警告の確認と対応
- Prettier フォーマット

### Step 4: Test Check ✅

すべてのテストがパスすることを確認。

```bash
pnpm test
# カバレッジ付き
pnpm test --coverage
```

**チェック項目:**

- 全テストグリーン
- カバレッジ 80%以上
- 新機能のテストあり

### Step 5: Security Check 🔒

セキュリティ脆弱性がないことを確認。

```bash
npm audit --audit-level=moderate
```

**チェック項目:**

- 依存関係の脆弱性なし
- 機密情報のハードコードなし
- OWASP Top 10 準拠

### Step 6: Diff Check 📊

変更が適切にコミットされていることを確認。

```bash
git diff --stat HEAD~1
git diff HEAD~1 --name-only
```

**チェック項目:**

- 未コミットの変更なし
- 適切なコミットメッセージ
- 不要なファイルの除外

## 証拠ベース完了判定（Iron Law）

**検証コマンドを実行せずに「パス」を宣言することは許されない。**

各ステップの判定には、**同一ターン内で**コマンドを実行した出力が必須。過去の実行結果、キャッシュされた結果、「通るはず」という推測は証拠として認めない。

| 主張 | 必要な証拠 | 証拠にならないもの |
|------|-----------|-------------------|
| 「ビルド成功」 | 同一ターンの `pnpm build` 出力（exit code 0） | 「ビルドに影響する変更はしていない」 |
| 「型エラーなし」 | 同一ターンの `pnpm typecheck` 出力 | 「型を修正したので大丈夫」 |
| 「lintパス」 | 同一ターンの `pnpm lint` 出力 | 「前回通った」 |
| 「テスト全パス」 | 同一ターンのテスト実行出力（0 failures） | 「変更していないから通る」「should pass」 |
| 「脆弱性なし」 | 同一ターンの `npm audit` 出力 | 「依存は変更していない」 |

**Red Flags**: レポート内に以下の表現があればルール違反:
- 「〜のはず」「おそらく通る」「前回パスしている」「変更していないので影響なし」
- 実行出力を伴わない ✅ 判定

## 検証結果フォーマット

```
【6 段階検証結果】

✅ Step 1: Build    - パス
✅ Step 2: Type     - パス
⚠️  Step 3: Lint    - 警告 3 件
✅ Step 4: Test     - パス（カバレッジ: 85%）
✅ Step 5: Security - パス
✅ Step 6: Diff     - 変更 5 ファイル

【アクション必要】
- lint 警告を修正: `pnpm lint --fix`
```

## CI/CD 統合

```yaml
# GitHub Actions 例
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install
      - run: pnpm build
      - run: pnpm typecheck
      - run: pnpm lint
      - run: pnpm test --coverage
      - run: npm audit --audit-level=moderate
```
