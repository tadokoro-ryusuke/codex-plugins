# GPT-6 Sol / Luna とプラグインのモデル選択

調査日: 2026-09-23。調査対象は `main` の `db5b5e6`、`dev-core` 5.4.0。公開一次情報と現行ソースを確認した調査・提案であり、プラグインの実装変更、再インストール、モデル間の実装比較評価は実施していない。ユーザーの「opus 6 luna max」は文脈から `gpt-6-luna` / `max` の提案として扱った。

追記: 調査後にユーザーが推奨内容の適用を承認したため、5.5.0 の変更と検証を別の [実装記録](../plans/task-sol-luna-routing.md) に記録する。以下の現状説明・確認結果は調査時点の履歴として保持する。

## 結論

GPT-6 Luna max は、範囲の明確な実装サブエージェントの有力な第一候補。公式図では DeepSWE で Sol high を上回る点推定値と低い費用を示す一方、FrontierCode では Sol が高得点であり、評価軸で順位が変わる。Luna max を限定実装、Sol を広い実装、Astra を設計・重要レビューに割り当てる構成を提案する。実リポジトリでの最適性は比較評価で確かめる。

公式 Codex ガイドの開始点は Sol Medium / Luna High / Astra Light。Max は難問向けで、大部分の作業に Max / Ultra は不要と説明されている。Luna は Max まで対応し、Ultra は非対応。API の Sol / Luna の既定推論量はともに `medium` であり、Codex の推奨開始点と混同しない。[Codex Models](https://learn.chatgpt.com/docs/models#pick-a-reasoning-effort)、[Sol API](https://developers.openai.com/api/docs/models/gpt-6-sol)、[Luna API](https://developers.openai.com/api/docs/models/gpt-6-luna)

## 確認できた能力・評価の範囲

以下は [OpenAI 発表の埋め込み図](https://openai.com/index/introducing-gpt-6-sol-and-luna/#coding) のスコア / タスク費用。本文抽出では図が欠落するため、ブラウザーで図を読み込み、表示された各点の ARIA ラベルを別々の調査担当が確認した。

| 構成 | DeepSWE v1.1 | FrontierCode 1.1 Main |
| --- | ---: | ---: |
| Luna high | 59.3% / $0.084 | 37.3% / $0.067 |
| Luna max | 66.6% / $0.22 | 42.4% / $0.11 |
| Sol medium | 56.6% / $0.38 | 45.9% / $0.80 |
| Sol high | 65.3% / $0.64 | 47.7% / $1.08 |
| Sol xhigh | 66.6% / $1.00 | 48.4% / $1.37 |
| Sol max | 68.8% / $2.74 | 49.3% / $2.14 |

FrontierCode は正しさに加えて、テスト品質・スコープ・規約など mergeability も評価する。図点に信頼区間はなく、費用は表示上の丸め値。研究環境 / API の結果を、自リポジトリの成功率や Codex の購読消費量へ直接変換できない。

この比較から、実装用 Luna max を具体的に試す根拠は得られる。ただし、親が仕様と境界を定義し reviewer が変更品質を確かめる構成で優位性が維持されるかは、このプラグインで新たに検証する仮説である。

[DeepSWE 主催者ページ](https://deepswe.datacurve.ai/) は 113 タスク、mini-swe-agent による統一実行、2026-09-22 更新を表示する。ただし調査時に取得できた一覧には GPT-6 Sol / Luna の構成が見当たらず、発表の二つの数値を主催者一覧で独立照合できなかった。主催者ページの別モデルの最良値と、発表の指定 effort 比較を混ぜない。

公式の用途区分は Sol が複雑な coding / agentic workflow、Luna が focused coding を含む明確で反復可能な仕事、Astra が最難度の一連の仕事。[Codex Models](https://learn.chatgpt.com/docs/models#choosing-astra-sol-and-luna)

## 価格と長い作業の実コスト

API Standard、入力が 272K 以下、100 万トークン当たりの USD:

| モデル | 通常入力 | キャッシュ読取 | キャッシュ書込 | 出力 |
| --- | ---: | ---: | ---: | ---: |
| GPT-6 Sol | $2.00 | $0.20 | $2.50 | $10.00 |
| GPT-6 Luna | $0.10 | $0.01 | $0.125 | $0.50 |

同じトークン量なら Luna は Sol の 1/20。両モデルは context 1,050,000、最大出力 128,000。272K 超の入力はリクエスト全体で入力・キャッシュ単価が 2 倍、出力単価が 1.5 倍。API Fast は対象単価の 2 倍。[Sol API](https://developers.openai.com/api/docs/models/gpt-6-sol)、[Luna API](https://developers.openai.com/api/docs/models/gpt-6-luna)

推論トークンも出力として課金される。API ガイドは medium を一般的な agentic coding、high を複雑な debugging / planning、xhigh を追加時間と費用に見合う評価結果がある場合、max を最難問向けと位置づける。低い単価だけではタスク完了までの時間・費用は決まらない。[Reasoning models](https://developers.openai.com/api/docs/guides/reasoning#reasoning-effort)

Codex の ChatGPT credits は 100 万入力 / キャッシュ入力 / 出力について、Sol が 50 / 5 / 250、Luna が 2.5 / 0.25 / 12.5。こちらも表の単価比は 20 倍だが、公式は credit 単価だけで購読枠の消費量は決まらないと明記する。消費量は context、推論、ツール、検索、キャッシュ等で変わる。Codex の credit 課金には別途の cache-write 料金がなく、API キー認証は API 料金を使う。[Codex Pricing](https://learn.chatgpt.com/docs/pricing)

ChatGPT 認証時の GPT-6 Fast は credits 消費 2.5 倍。API Fast の 2 倍と区別する。現在の公式 Speed ページから Sol / Luna の実装タスクにおける絶対レイテンシや、Luna max 対 Sol high の速度比は確認できない。[Codex Speed](https://learn.chatgpt.com/docs/agent-configuration/speed)

## キャッシュの改善を設計にどう反映するか

GPT-5.6 以降のキャッシュ書込は通常入力の 1.25 倍、読取は 0.1 倍。安定した指示・共通資料を先頭に置き、会話は追記する。GPT-6 では `configuration_update` を追記して effort を変え、トップレベルの `reasoning.effort` を固定すると既存 prefix を保てる。ツール定義と順序を固定し、`allowed_tools` 等で利用可否を変える手段もある。[Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

これは API を呼ぶ実行基盤の機能であり、SKILL.md に一文書くだけで Codex 内部のキャッシュ制御が変わるとは確認していない。モデル変更をまたぐキャッシュ共有も前提にしない。実装する基盤がある場合は `cached_tokens`、`cache_write_tokens`、出力・推論量、総費用を記録する。

## 信頼性とスキル設計に関する留保

System Card の Auto-review 評価では Luna に迂回の試みが観測され、成功は観測されなかった。これは制約への対応を試す評価で、普段の失敗率ではない。モデル更新後も既存の権限境界・検証を保持する判断材料となる。[GPT-6 System Card, section 11.6.1](https://deploymentsafety.openai.com/gpt-6-astra)

GPT-6 の共通 prompting ガイドは、記載された行動傾向が Astra の観測に基づくため、選んだモデルと作業で評価するよう明記している。Astra 向けに不要になった手順を、そのまま Luna から全削除する根拠にはならない。[Model guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)

スキルの短い発火条件、必要時だけ補助資料を読む構成、矛盾した指示の削減は公式の改善方向である。モデル名の置換とあわせて、読み込む指示の量と役割の重複も見直す。[Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

## このリポジトリへの提案 — 未検証の設計判断

以下は公開結果の転載ではなく、評価するための候補。

| 仕事の性質 | 候補 | 境界・昇格条件 |
| --- | --- | --- |
| 明確な仕様、限定された編集範囲、機械検証可能な実装 | Luna max を第一候補に high と比較 | 要求解釈や依存関係の解決が増えるなら Sol に渡す |
| 複数モジュール、曖昧な仕様、難しい障害修正 | Sol medium / high を比較 | 隠れた不変条件や影響の大きい判断を含むなら Astra を比較 |
| 設計、作業分割、統合、重大リスクの独立レビュー | Sol high / Astra high を比較 | 見逃しと後戻りの損失を評価に含める |
| 単純な検索・抽出・整形 | Luna low / high を比較 | Max の一律指定を避ける |

モデルごとの新スキルを増やすより、既存の execute / review 等が共有する選択方針と役割設定に集約する。ユーザー指定と実行環境で利用可能なモデルを優先し、未対応モデル・effort を黙って別設定へ置換しない。

子エージェントの費用だけで最適化せず、親の説明・監督・再修正・統合・最終レビューを含む完了までの総量を測る。範囲指定、完了条件、ファイル所有権、検証コマンド、返却する根拠を委譲単位に持たせる。Luna が安くても、細分化しすぎた説明や重複探索で節約が消える可能性がある。

## 現行プラグインで確認した更新箇所

モデル設定の中心は [execution-profile.json](../../plugins/dev-core/skills/codex-collab/assets/execution-profile.json)。現状は親推奨・implementer・reviewer が `gpt-6-astra / high`、researcher が旧 `gpt-5.6-sol / medium`。調査時の内容であり、今回この設定は変更していない。

- [planned-execution.md](../../plugins/dev-core/skills/codex-collab/references/planned-execution.md) の 42–50 行は、明示指定・custom profile を優先し、通常と難しい実装に同じ default を使う契約。モデル名を Luna に置換するだけでは難しい実装も Luna になる。タスク別の選択を導入するには、この文書で選択条件と許可範囲を改める必要がある。
- [resolve_execution_role.py](../../plugins/dev-core/skills/codex-collab/scripts/resolve_execution_role.py) の 115–140 行は、選択された model/effort を実環境の capability と照合する。新しいモデル名・`max` 自体のための allowlist 追加は不要。既存の `--profile` と対になった `--model` / `--effort` を再利用できる。ただしツールが選択可能であることと、ワークフローが自動選択を許可していることは別。
- role は implementer / reviewer / researcher の 3 種類。最初の導入ではこの区分を維持し、タスクごとの candidate profile または明示 override を使う。独自の router agent や新しい role 群を加える必要はない。
- [dev-execute](../../plugins/dev-core/skills/dev-execute/SKILL.md) の 16–21 行と [orchestration.md](../../plugins/dev-core/skills/dev-workflow/references/orchestration.md) の 38–63 行は、委譲の便益・所有権とモデル選択を分けている。逐次・密結合の仕事は親が実装でき、子は役割を完遂して戻る。この設計を維持する。
- profile は実行中の親を切り替えない。単独の debug / TDD / review にも一律適用されない。profile の対象外では明示指定がない限り設定を継承する。モデル選択の適用範囲を README と skill で明示する。
- [code-reviewer.toml](../../plugins/dev-core/skills/codex-collab/assets/agents/code-reviewer.toml) は effort と read-only を設定するが model は指定しない。JSON profile は自動ロードされず、既に個人導入した TOML の設定も今回の source 変更だけでは変わらない。
- [skill-behavior-cases.json](../../plugins/dev-core/evals/skill-behavior-cases.json) は通常・難しい実装とも Astra high を期待するケースを持つ。新方針では該当ケースと [test_execution_roles.py](../../scripts/tests/test_execution_roles.py) の capability fixtures、README を同期する。既存の 49 ケース inventory は live 実行の証拠ではない。
- HOTL の [ai-review.yml](../../plugins/hotl-engineering/skills/hotl-engineering/assets/workflows/ai-review.yml) 等は Bedrock / Anthropic 用の provider adapter。今回の OpenAI モデル更新では provider 固有のモデル ID を一括置換しない。主な変更対象は dev-core。

## 推奨する最初の構成

公開情報と現行構成から選ぶ、実装比較前の候補。親・重要レビューの設定を固定して、worker の変更効果を先に測る。

| 責務 | 最初の候補 | 選択理由・適用範囲 |
| --- | --- | --- |
| 要件・設計・統合・受入判断 | Astra high を維持 | 現行の品質基準を保って比較する。公式の一般的な開始点は Astra low であり、high が実測最適という意味ではない |
| 一般的な実装子 | Sol medium | 公式の Codex 開始点に沿う。複雑なロジック・多数の境界条件を追う場合は、許可された方針で high を選択 |
| 仕様が固まった局所実装子 | Luna max を第一候補に試す | 公開図の coding 成績を根拠に、編集範囲・期待結果・独立した検証が明確な仕事で評価する |
| 単純な局所修正・短い定型作業 | Luna high | 公式開始点に沿う。Max の追加推論が受入率を改善しない仕事では high の時間・総消費を比較する |
| 独立レビューが必要な変更 | Astra high を維持 | セキュリティ、永続データ、並行処理、重要な公開契約などの既存 gate を維持 |
| 有限の資料からの検索・抽出・整理 | Luna high | 情報収集と設計・根因判断を分け、根拠の所在を返す。難しい比較判断は Sol または親へ戻す |
| lint / test / format 等の決定的な処理 | ツール直接実行 | コマンド実行のためだけにモデルを追加しない |

Luna の適用条件は、合意した期待動作、限定した write set、局所的な依存関係、候補が書き換えられない受入チェックを持つこと。たとえば確定した DTO 変換、既存パターンに沿う validation、原因が確定した局所的な回帰修正が候補になる。

要件矛盾、未知の根因、権限設計、migration、共有状態の設計、未計画の公開契約変更は、Max に上げて作業継続する前に親へ戻す。親が範囲を定め直し、Sol / Astra の担当を選ぶ。モデル切替時も同じ失敗経緯を引き継ぎ、既存の Three Strikes をリセットしない。

共通の完了条件とレビュー gate はモデルにかかわらず保持する。Luna には、その作業に必要な仕様・ファイル・チェック・返却条件を短く渡す。Astra 向けの設計手順を全量コピーしたり、各 skill にモデル名を重複定義したりしない。

移行は、現在の quality profile を比較基準として保存し、候補を明示して試し、成績が安定した仕事の種類から既定値へ採用する順序がよい。これは調査上の提案であり、今回の依頼から既定設定変更の承認を推定して適用してはいない。

## 変更前に行う比較評価

1. 同じコミット・同じタスク・同じツール・同じ検証条件で、Luna high / max と Sol medium / high を比較する。現行 Astra high も基準として残す。最初の比較では親・reviewer のモデル、effort、レビュー要否、並列度、speed を固定し、モデルまたは effort を一つずつ変える。
2. タスクを明確な局所修正、複数ファイル変更、仕様の曖昧な障害、レビューの見逃し検出に分ける。変更者と評価者の役割を分ける。
3. 完了率だけでなく、差分の妥当性、隠れた回帰、スコープ逸脱、親の手直し量、経過時間、推論を含む総トークン、実 credits / API 費用を記録する。
4. 実運用では再試行と上位モデルへの引き継ぎを含めて測る。少数の成功例で既定モデルを全面変更しない。難度ごとに繰り返し、実行順を入れ替え、未完了と失敗も集計する。
5. CLI / desktop / API で利用可能モデルと effort が異なる場合は、結果を別に扱う。構造検証が通ったことと、実モデルで指示どおり行動したことを区別する。

未確認: 当該ユーザー環境での実装品質、Luna max 対 Sol medium/high のタスク別優劣、同時実行時の速度、親子合計の credits 節約率、Codex 内部キャッシュの実挙動。これらは公開ベンチマークだけでは確定しない。

既存の [execution-evaluation.md](../../plugins/dev-core/skills/codex-collab/references/execution-evaluation.md) が、独立 grader、親子・手戻りの合計消費、requested と effective model の区別を定義している。これを拡張し、新しい評価基盤の作成は必要な場合に限る。構造検査、helper の offline tests、native skill の挙動、比較品質・コストを別の証拠として扱う。

実装段階の変更範囲は profile / 選択契約 / README / 関連 tests・eval。実行ロジックを変える場合は test-first で行い、plugin validator、eval schema validator、offline tests を実行する。リリースする際に version を上げ、許可された範囲で再インストールと新しいタスクでの読込みを確認する。

## 今回の確認結果

- 変更はこの調査レポートの追加のみ。plugin source、model profile、version、インストール済みキャッシュは変更していない。
- `node scripts/validate-codex-plugins.mjs`: 成功。
- 既存 offline tests: Python 3.12 と PyYAML 6.0.2 の一時環境で `python -m unittest discover -s scripts/tests -q` を実行し、66 件成功。外部サービスは fixture / mock であり、実モデルの品質比較ではない。
- 最初の macOS 標準 Python 3.9 実行は cache 書込み権限と PyYAML 不在、続く Python 3.12 単体実行は PyYAML 不在で失敗。コードを変更せず CI 指定の依存関係を一時環境に揃えて解消した。
- レポートのローカル参照 10 件と行末空白を確認。モデル比較や live skill eval は未実行。
