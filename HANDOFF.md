# HANDOFF — 次のセッションへ（2026-09-13）

## 現状
- 仕組みは稼働開始済み。スケジュールタスク `cc-changelog-digest`（毎時 7 分、Claude デスクトップ起動中のみ）が `CLAUDE.md` の手順で動く。
- v2.1.270 をドライランで配信済み（メール送信・Pages 公開・既読化まで確認）。次は v2.1.271 以降で本番初回。
- PR #1〜#3 はマージ済み（修正列の追加、email テンプレの安全化、`.claude/` 除外、その他フォローアップ）。
- 再設計完了: Pages 公開ディレクトリを `docs/` → `site/` に変更し、README をゼロから書き直し、詳細ドキュメントを `docs/`（`setup.md` / `operations.md` / `scripts.md` / `writing-guide.md` / `design-decisions.md`）に集約した。`SCHEDULED_TASK_PROMPT.md` は `docs/setup.md` に統合して削除済み。
- **Pages のソース設定（gh api での変更）はこの再設計 PR のマージ後に別途実施する**（`docs/setup.md` に手順を記載済み）。

## 予想外だったこと
- 差分検知の「初回は最新1件のみ」を既読ゼロ判定で実装したため、既読1件になった直後に旧版19件が新規扱いになった。自動実行の26分前に発覚し、「最新既読より新しい版のみ」に修正（317a502）。詳細は `docs/design-decisions.md`。
- 公式 Atom `feed.xml` がリポジトリ直下に存在し、CHANGELOG.md/Release と同一コミットで更新される。RSS 案と定期確認案は同じ情報源だった。
- feed の content は `<li>` ではなく `<p>• …</p>` 形式。html_to_text は両対応にしてある。
- テンプレ内の LLM 向けコメントに `{{CARD_BLOCK}}` を書くと未置換プレースホルダとして本文に残る（PR で修正）。

## 判断の根拠
- 実行基盤にデスクトップのスケジュールタスクを選んだのは、セッションリンクと Gmail 連携が追加設定なしで使えるため。常時稼働が必要なら GitHub Actions + `claude -p` へ（check/render/publish は流用可能）。
- 画像は base64 添付でなく Pages の URL 参照。添付は毎回数十万トークンかかる。
- モデル Opus 5 / effort medium は 1 日 1 回程度の実行なのでコスト許容と判断。タスク作成ツールにモデル指定は無く、アプリ既定を引き継ぐ想定。**初回本番実行のログで実モデルを確認すること**（`list_task_runs` → セッションの model）。
- 詳細は `docs/design-decisions.md` に集約した（このファイルには重複させない）。

## 次回変えること・残課題
- 再設計 PR マージ後、`gh api` で GitHub Pages の Source を `main` の `/site` に設定変更する（`docs/setup.md` 参照）。設定変更前は Pages が旧 `docs/` を参照したままなので、マージ直後は公開 URL が一時的に古い内容のままになる可能性がある。
- 初回本番実行後に `list_task_runs` で NO_UPDATE 早期終了と、更新時のツール承認（Gmail / Bash）が止まっていないか確認。止まっていたら「Run now」で事前承認。
- セッションリンクはデスクトップアプリの URL 形式が不明のため、メールにはセッション ID とタイトルのみ記載している。形式が分かればリンク化する。
- `session_link.py` が返す ID と `get_session self` の ID が異なる（前者は CLI 側のセッションファイル）。信頼するのは後者。
- 複数版が同時に溜まった場合の 1 通まとめは手順に書いてあるが未検証。
