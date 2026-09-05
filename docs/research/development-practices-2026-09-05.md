# 開発プラグインの更新調査・改善記録

調査日: 2026-09-05。比較元: `d17d0ab`。作業ブランチ:
`codex/development-practices-refresh`。

## 結論と範囲

`dev-core`、`github-tools`、`hotl-engineering` の開発手順・検証・委譲・
レビュー・配布テンプレートを更新した。最優先は、未実行・不完全な証拠を
成功として扱う経路の修正。そのうえで、固定の工程・数値・再承認要求を、
依頼の範囲とリスクに応じた手順へ整理した。

既存の TDD、作業ツリー保全、明示的な委譲許可、現在の証拠による完了判定は
維持した。マーケティング・UI素材、兄弟リポジトリ、実サービス、アカウント
設定、公開・インストールは対象外。言語・フレームワーク固有の全パターンを
網羅的に再監査したという意味ではない。

## 一次情報と採用判断

公式記述の要約と、このリポジトリへの採用判断を区別する。

| 一次情報（当日取得） | 確認した事項 | 採用判断 |
| --- | --- | --- |
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | 段階的に説明を読み込む方式、明確な適用範囲、スキル一覧の文脈予算 | 必要な参照だけを読み、長い HOTL 説明を短縮。既存の参照スキルの明示起動方針は維持 |
| [OpenAI: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Codex の委譲条件、読み取り中心の並列化、追加トークン、設定継承 | 入力・所有範囲・共有資源・戻す証拠・停止条件を定義。内部委譲のためにユーザー所有タスクを作らない |
| [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | 現実のタスクに合う評価、継続評価、人による採点調整 | 挙動ケースを増やし、JSONスキーマ検証と実モデルによる評価を明確に区別。特定の評価APIは導入しない |
| [OpenAI: Hooks](https://learn.chatgpt.com/docs/hooks) | `command` と `mcp_tool` をサポート。shell/unified exec は `Bash` と `tool_input.command` に正規化 | 現行ブロッカーの名前・入力形式を維持。command限定を製品仕様ではなく当リポジトリの互換性方針として説明 |
| [GitHub: Secure use](https://docs.github.com/en/actions/reference/security/secure-use) | 最小権限、ジョブごとの権限、信頼できない入力、固定SHAの推奨 | 認可と書込みジョブを分離し、モデル出力を決定的な検証に通す。プロバイダー権限・SHA固定は適用時の必須確認事項として維持 |
| [GitHub: Repository permissions API](https://docs.github.com/en/rest/collaborators/collaborators#get-repository-permissions-for-a-user) | ユーザーの実際のリポジトリ権限を取得できる | 存在しない sender の association 属性を使わず、ラベルを付けた本人の admin 権限を照会 |
| [Azure: Blue-green rollback](https://learn.microsoft.com/en-us/azure/container-apps/blue-green-deployment#roll-back-the-deployment-if-there-were-problems) | revision の有効化と実トラフィックの切替は別 | 汎用サンプルだけで復旧を完了扱いしない。実状態の保存・復元・疎通確認を行うアダプターを要求 |
| [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) | 異なる粒度のテスト、下位層中心の速いフィードバック、層の名称への過度な固執を避ける | 80%やE2E件数を普遍的な基準にせず、変更された振る舞いと重要な失敗経路を優先 |
| [DORA: Delivery metrics](https://dora.dev/guides/dora-metrics/) | 現行は5指標。従来の Four Keys から変化し、一般的な MTTR とも区別 | 現行名称に更新し、チーム・サービスの改善指標として扱う |
| [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | 分類の更新、供給網と例外条件の扱い | 古い番号対応を除去し、変更リスクを確認する観点として記載。準拠・無脆弱性を主張しない |

## 優先度付きの発見と対応

以下のパスはリポジトリルートからの相対パス。
「修正済み」はソース・ローカル検証の状態であり、配備済みを意味しない。

| ID / 優先度 | 更新前の問題・証拠 | 対応と確認範囲 |
| --- | --- | --- |
| F1 / P1 | `verification-loop/scripts/verify.sh` で、Pythonツール不足が表示されずJSの成功だけで終了0。空の検証もPASS。CLI fixtureで再現 | 各言語の不足をBLOCKED、未検証を終了2に変更。グローバルPython監査・自動コンパイラ取得・異なるPMの監査流用も解消。9 fixtureが成功 |
| F2 / P1 | `assets/workflows/ai-review.yml` が欠落・不正JSON・負の件数を0件と解釈。既存shellを用いた独立fixtureで再現 | trusted baseの `check_review_verdicts.py` で必須tier、ジョブ状態、非負整数、head SHAを検証。PR外に新規verdictを作成 |
| F3 / P1 | `assets/evals/run_evals.py` で通常ケースのAPI失敗が平均から消える。成功1件＋失敗1件でもPASSを親・レビュー担当が独立再現 | target/judge実行不全を品質点と分離して失敗判定。投票数・得点型/範囲、空suiteも確認 |
| F4 / P1 | `assets/workflows/eval-gate.yml` の共有staging結果が対象PRを評価した証拠にならない | 応答の実revisionと期待revisionを照合。PR用preview接続は適用先で必要。未接続なら成功扱いしない |
| F5 / P1 | baseline取得の通信・認証失敗まで初回扱いし、回帰比較を省略 | 通常の取得失敗・明示指定ファイル欠落を伝播。初回校正はbaselineを指定しない明示的手順に分離 |
| F6 / P1 | 評価開始前に失敗すると、PR内にあった古いPASSレポートを投稿できる | 出力を新規RUNNER_TEMPディレクトリへ移し、投稿・artifact・S3・baseline更新の参照を統一。2回の準備が異なる空ディレクトリを作るfixtureで確認 |
| F7 / P1 | `assets/workflows/agent-implement.yml` が `sender.author_association` を使い、正規承認でも始動しない | read-only認可ジョブでactor権限を確認後、書込み/OIDCジョブへ進む。admin/write/read/欠落をAPIスタブで確認 |
| F8 / P1 | `assets/workflows/deploy.yml` が最初のactive revisionを選び、有効化だけでロールバック完了を通知 | 不完全な復旧コードを撤去。capture/restoreアダプターを必須にし、未設定を本番デプロイ前に拒否。実クラウド復旧は適用先の検証事項 |
| F9 / P2 | `test-design`、`best-practices`、review roleが固定率・件数・サイズだけで処理や重大度を決める | 既存ゲートと具体的影響を基準に変更。重要な失敗/復旧経路をテスト対象へ。flakeは自動除外せず調査・期限付きの承認済み隔離 |
| F10 / P2 | 委譲の所有範囲・返却証拠、共有資源、再開時の古い証拠の扱いが不十分 | orchestration、plan template、collabを整合。ツール非搭載時は既存計画へ記録。別worktreeでもDB等の共有資源は隔離されないと明示 |
| F11 / P2 | PR準備やHOTL適用で既存承認を再確認し、ローカル下書きにもfetchを要求 | 承認を継続利用し、必要な最終判断の前に具体物を準備。未コミット作業を保全し、複数行PR本文はbody fileに変更 |
| F12 / P2 | 過去のDORA/OWASP分類、hooks仕様の過度な一般化、2週間だけでの昇格など | 現行仕様とローカル方針を区別。既存の強制ゲートを弱めず、新規のノイズのある検査だけを校正 |
| F13 / P2 | skill挙動ケースは6件で、CIはスキーマと浅いsmoke中心 | 挙動ケース15件へ拡張し、未実行を明記。27件のオフライン実行テストをCIに組込み |

## 検証記録

- **Red → Green**: verification runnerの9ケース中7件が修正前に失敗し、修正後に9件成功。既存のmixed-stack失敗伝播は維持。
- **追加回帰**: verdict、target/judge、認可、復旧preflight、baseline欠落、出力先の各失敗をテストで固定し、修正後に成功。revision照合等の追加境界ケースも実行。
- `python3 -m unittest discover -s scripts/tests -v`: **27件成功**。Python 3.12、PyYAML 6.0.2で実施。外部API、実モデル、実プロジェクトのbuildはスタブ。
- `node scripts/validate-codex-plugins.mjs`: 成功。
- `node scripts/validate-skill-evals.mjs`: **15ケースのスキーマ検証成功**。15ケースを実モデルで実行したという意味ではない。
- bundled `quick_validate.py`: 更新した **10スキル成功**。
- bundled `validate_plugin.py`: 更新した **3プラグイン成功**。
- SessionStart fixture、破壊的操作を実行しないPreToolUse deny/pass-through fixture、agent TOML、shell/Python構文: 成功。
- `actionlint` 1.7.12: このリポジトリのCIとHOTLサンプルの **7 YAML成功**。公式releaseのchecksumを検証した一時バイナリを使用。shellcheck/pyflakes連携は無効とし、別途構文検証を実施。
- 独立レビューで発見された不完全評価・古い出力・severity矛盾を修正し、親側でも根拠と該当テストを確認。
- 出力準備失敗時に空パスからルートを収集し得る異常系も回帰テスト化し、準備成功・非空パスをartifact投稿の前提に追加した。
- `git diff --check`: 成功。コミット・push・PR・実サービス変更は実行していない。

## 移行と残る適用作業

ソース版は `dev-core 5.0.0`、`github-tools 1.4.0`、
`hotl-engineering 2.0.0`。検証runnerの終了コードとHOTLの成果物・適用契約が
変わるため、前者と後者はmajor更新とした。

1. 配布時には、意図するmarketplaceのソースを公開・確認してから再インストールし、新しいタスクでversion/cacheを照合する。この作業ではインストール済みキャッシュを書き換えていない。
2. HOTLを実案件へ適用する際は `assets/ADJUST.md` に従い、trusted validator、実revisionを返すpreview、baseline、実権限、モデル/profile、固定Action SHA、通知先を設定する。
3. 本番の復旧アダプターは実環境のrevision modeとトラフィック設定に合わせて実装・リハーサルする。今回証明したのは未設定時の停止だけ。
4. issue-to-agentは、承認済みIssue本文のsnapshotと環境承認を確立してから有効化する。GitHub上の権限API/OIDC/生成PRは未実行。
5. 指示変更の品質向上を数値化するには、15シナリオを隔離fixtureで変更前後・複数回実行し、モデル/runtime、追跡ログ、成果物、禁止された副作用を採点する。現在はケース定義とオフライン回帰の段階であり、エージェント成功率の改善は未測定。

更新を続ける際は、現実の失敗を再現可能なケースにし、原因に対応する最小の
指示・テスト・ツールを変更してから同じ条件で比較する。個別の失敗を無条件の
恒久ルールへ広げない。
