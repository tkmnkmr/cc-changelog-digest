# セットアップ

このリポジトリを新しいマシンで動かす、またはスケジュールタスクを再登録するための手順。

## 前提条件

- **Claude デスクトップアプリ**（スケジュールタスク実行基盤。Gmail 連携とセッションリンクが追加設定なしで使える）
- **Gmail 連携**（Claude デスクトップの Connectors で接続済みで、`send_message` ツールが使えること）
- **Python 3**（標準ライブラリのみで `check_update.py` / `classify.py` / `publish.py` / `mark_seen.py` / `session_link.py` は動作）
- **playwright + Chromium**（`render_png.py` のみ必要）
  ```bash
  pip install -r requirements.txt
  python3 -m playwright install chromium
  ```
- **`gh` CLI 認証済み**（GitHub Pages 設定変更やリポジトリ操作に使う場合。日常の commit/push は素の `git` で行う）

## GitHub リポジトリ / Pages 設定

- 公開リポジトリ `tkmnkmr/cc-changelog-digest` を作成し、`main` に push する。
- Pages は **GitHub Actions 方式**（`.github/workflows/pages.yml`）で `site/` をデプロイする。
  従来方式（legacy）は公開元に `/` か `/docs` しか選べないため、`site/` を使うにはこの方式が必須。
  ```bash
  gh api repos/tkmnkmr/cc-changelog-digest/pages -X POST -f build_type=workflow   # 初回
  gh api repos/tkmnkmr/cc-changelog-digest/pages -X PUT  -f build_type=workflow   # 既存設定の切替
  ```
- `site/**` が main に push されるとワークフローが自動で走り、1〜2 分で反映される。
  手動で走らせる場合は `gh workflow run pages.yml`。

## スケジュールタスクの登録

- taskId: `cc-changelog-digest`
- cron: `7 * * * *`（毎時 7 分、ローカル時刻）
- 想定モデル/effort: Opus 5 / medium
- 起動条件: Claude デスクトップアプリ起動中のみ

登録するプロンプト本文:

```
あなたは Claude Code の CHANGELOG ダイジェスト配信担当です。
作業ディレクトリ: /Users/tkm/code/cc-changelog-digest
必ず同ディレクトリの CLAUDE.md の手順を上から順に実行してください。

最初に `python3 scripts/check_update.py` を実行し、出力が NO_UPDATE なら
「更新なし」とだけ報告して直ちに終了してください（他のツールは一切使わない）。

NEW_UPDATE の場合のみ、CLAUDE.md の 2〜6 節（執筆 → render_png → publish →
Gmail 送信 → mark_seen）を完遂してください。執筆規約は templates/DIAGRAM_GUIDE.md。
送信先は tkm603018@gmail.com。Gmail 送信には接続済みの Gmail ツール send_message を使います。
送信が成功した場合のみ mark_seen.py を実行します。

セッションリンク: get_session self でこのセッションの sessionId とタイトルを取得し、
メール本文のフッターに記載してください（取得できなければ省略）。

最後に、送った版番号・公開 URL・所要の判断（破壊的変更の有無など）を 3 行で報告してください。
```

登録後、初回実行のログ（`list_task_runs`）で以下を確認する:

- NO_UPDATE 時に早期終了しているか
- 更新検知時、Gmail / Bash ツールの承認待ちで止まっていないか（止まっている場合は「Run now」で事前承認する）
- 実際に使われたモデルがアプリ既定と一致しているか（タスク作成ツールにモデル指定は無く、アプリ既定を引き継ぐ）

## 関連ドキュメント

- 日々の運用: [operations.md](./operations.md)
- 各スクリプトの詳細: [scripts.md](./scripts.md)
