# cc-changelog-digest — 実行手順（スケジュールタスク / 手動実行 共通）

このリポジトリは Claude Code の CHANGELOG 更新を検知し、図付き HTML 資料（X の AI インフルエンサー
投稿を文体・構成の手本にした、結論先出し・短文のまとめ）を生成してメール配信する。以下の手順を
**上から順に** 実行する。判断に迷ったら「送らない・既読にしない」を選ぶ。

## 0. 前提
- 作業ディレクトリ: `~/code/cc-changelog-digest`
- 送信先: tkm603018@gmail.com（Gmail 連携ツール `send_message` を使う）
- 公開先: https://tkmnkmr.github.io/cc-changelog-digest/
- 執筆規約: `templates/DIAGRAM_GUIDE.md`（必読）

## 1. 検知（更新がなければここで終了）
```bash
python3 scripts/check_update.py
```
- 出力が `NO_UPDATE` → **何もせず即終了**。メールも送らない。
- 出力が `NEW_UPDATE` + 版番号 → `state/pending/<version>.json` を読む。複数版ある場合は全部読み、1 通にまとめる。

## 2. 整理・執筆（Opus 推奨）
`state/pending/<version>.json` の `content_text` と `pre_classified` を材料に、次の観点で **再構成** する
（CHANGELOG の文をそのまま貼らない。主語をユーザーにして「何が嬉しいか」を書く。
文体・構成は X の AI インフルエンサー投稿を手本にする。詳細は `templates/DIAGRAM_GUIDE.md` 冒頭）。

1. ヘッドライン（結論一文、40字以内）
2. 3行でわかる（各50字以内、3行）
3. 前後の変化（Before/After 図 + 嬉しさ50字）
4. 注目トピック3枠（⚠️破壊的変更 / 🚀大幅アップデート / 🧠新モデル、無ければ「該当なし」を明記）
5. 機能4列（✨新規 / 🔧更新 / 🐛修正 / 🗑️廃止・利用不可）
6. 今日やること（「〜を使っている人 → 〜する」形式、1〜3件。無ければ「特別な対応は不要」）

`pre_classified` はキーワード分類の下書きにすぎない。文脈で判断して上書きしてよい。
「破壊的変更」の判定は保守的に（挙動が変わりユーザーの対応が必要なものだけ）。

成果物（テンプレのプレースホルダを全て埋める。未使用プレースホルダを残さない）:
- `out/<version>/report.html` ← `templates/report.html`
- `out/<version>/card.html`   ← `templates/card.html`
- `out/<version>/summary.md`  ← ヘッドライン＋3行でわかる＋今日やること
複数版をまとめる場合はディレクトリ名を `<最新版>` にし、report 内に版ごとのセクションを置く。
成果物を書き出す際は `<!-- LLM: -->` コメントを全て削除する。
`summary.md` など Markdown の成果物は Bash のヒアドキュメントで書き出す（サブエージェント実行時に
Write ツールがレポートファイルと誤検知して拒否することがある）。

## 3. 画像化
```bash
python3 scripts/render_png.py <version>
```
`out/<version>/card.png` を Read で **目視確認**。文字溢れ・重なりがあれば card.html を直して撮り直す。

## 4. 公開
```bash
python3 scripts/publish.py <version>
```
- 成功: stdout の JSON（`report_url`, `card_url`）をメールに使う。
- exit 3（push 失敗）: 画像なしメールにフォールバック。本文に「公開に失敗したため画像は省略。ローカル: out/<version>/」と書く。

## 5. メール送信
`templates/email.html` を埋めて Gmail `send_message` で送る。
- to: tkm603018@gmail.com
- subject: `[Claude Code] v<version> アップデートまとめ`（複数版なら `v<古い>〜v<新しい>`）
- htmlBody: 埋めた email.html。body: summary.md のテキスト + report_url（プレーン代替）
- セッションリンク: セッション ID/タイトルの取得元は優先順位順に試す。
  1. `get_session self`（`mcp__ccd_session_mgmt__get_session`）を第一候補とする
  2. 取得できない場合のフォールバックとして `python3 scripts/session_link.py` を使う
  どちらも取れなければ省略する。

## 6. 既読化（送信成功後のみ）
```bash
python3 scripts/mark_seen.py <version> [...]
```
送信に失敗したら実行しない（次回再送される）。

## 禁止事項
- 既読化を送信前に行わない
- feed 以外の情報源で推測して「新モデル」等を書かない（CHANGELOG に無いことは書かない）
- publish.py 以外で git push しない
