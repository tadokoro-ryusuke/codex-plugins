---
name: continuous-learning
description: "Continuous improvement workflow for extracting lessons from failures, review comments, repeated mistakes, test issues, and debugging sessions. Use to turn a mistake into durable prevention in AGENTS.md, tests, linters, scripts, or docs."
---

# Continuous Learning

Mitchell Hashimotoの原則: **「エージェントがミスを犯すたびに、そのミスを二度と起こさない仕組みを作る」**

## 学習ループ

### 1. ミスの検出

セッション中に発生した問題を特定:
- ビルドエラー、テスト失敗、lint違反
- レビューで指摘された設計上の問題
- 繰り返し発生するパターン（同じ種類のバグ、同じ修正手順）

### 2. 根本原因の分析

問題の原因を分類:
- **ルール不足**: 既存のルール/スキルにガイダンスがない
- **ルール無視**: ルールがあるが遵守されなかった → Hook化を検討
- **知識不足**: プロジェクト固有の制約が記録されていない
- **ツール不足**: 自動検出できるべきエラーが手動チェックに依存

### 3. 防止メカニズムの構築

原因に応じた対策:

| 原因 | 対策 | 保存先 |
|------|------|--------|
| ルール不足 | ルール/スキルに追記 | rules/*.md or skills/*/SKILL.md |
| ルール無視 | Hook化（100%強制） | hooks/hooks.json |
| 知識不足 | プロジェクト固有設定に記録 | `AGENTS.md` or project docs |
| ツール不足 | lint ルール/テスト追加 | eslintrc, テストファイル |

### 4. 検証

対策が機能するか確認:
- 同じ操作を試みてブロックされるか（Hook）
- 同じコードを書いた場合にlintで検出されるか
- 次回セッションでルールが参照されるか

## 複利的改善

各セッションがハーネスを改善し、改善されたハーネスが次のセッションの信頼性を向上させる。

```
セッション1: バグ発見 → ルール追加
セッション2: ルールが防止 → 新しいバグ発見 → Hook追加
セッション3: Hook+ルールが防止 → より高度な問題に集中
```

## Stopフックとの連携

Codex の Stop フックや検証スクリプトで以下を自動検出:
- 未コミットの変更
- console.log/debugger残存
- 新規TODO/FIXMEコメント

これらの検出パターンに新しいチェック項目を追加し続けることで、Stopフック自体が学習する。
