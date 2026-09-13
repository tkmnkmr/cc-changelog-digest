# スケジュールタスク登録内容（記録用）

- taskId: `cc-changelog-digest`
- cron: `7 * * * *`（毎時 7 分、ローカル時刻）
- 想定モデル/effort: Opus 5 / medium

## プロンプト本文

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
