# スクリプト詳細

`scripts/` 配下の各スクリプトの引数・出力・終了コード一覧。

## check_update.py

feed.xml をポーリングして新着バージョンを検知する。

- **引数**
  - `--feed-file <path>` — ネットワーク取得の代わりにローカルファイルを読む
  - `--force <VERSION>` — 既読済みでも強制的に pending に出す（ドライラン用）
- **出力（stdout）**
  - `NEW_UPDATE\n<ver1>\n<ver2>...` — 新着あり。`state/pending/<version>.json` を書く
  - `NO_UPDATE` — 新着なし
- **終了コード**
  - `0` — 成功
  - `2` — フィードの取得・解析エラー（メッセージは stderr）

## classify.py

CHANGELOG の各行をキーワード辞書でカテゴリ分類する（breaking / major / model / added /
changed / removed / fixed / other）。`~/code/rss-changelog-monitor/changelog_parser.py` の
方式を参考に、このプロジェクト向けに再構成したもの（コピペではなく自作コード）。

- **使い方（ライブラリとして）**: `from classify import classify_line, classify_lines`
- **使い方（CLI として）**:
  ```bash
  cat lines.txt | python3 scripts/classify.py > classified.json
  ```
- **入力**: 標準入力から改行区切りのテキスト
- **出力（stdout）**: `{"text", "category", "confidence", "tags"}` のリスト（JSON）
- **終了コード**: 常に `0`（分類できない行は `category: "other"` になるだけでエラーにはならない）

## render_png.py

`out/<version>/card.html` と `report.html` を Playwright で PNG 化する。

- **引数**: `<version>`（位置引数、必須）
- **出力**
  - `out/<version>/card.png`（1200x675、device_scale_factor=2）
  - `out/<version>/report.png`（幅 1000、full page）
- **終了コード**
  - `0` — 成功（どちらか一方でも生成できれば成功。存在しないファイルは警告のみで続行）
  - `1` — 引数不正、`out/<version>` が存在しない、playwright が import できない、
    または card.html/report.html のどちらも存在しない

## publish.py

`out/<version>/` を `site/<version>/` にコピーし、`site/index.html` を更新して commit・push する。

- **引数**
  - `<version>`（位置引数、必須）
  - `--no-push` — commit まで行い、push はスキップ
- **出力（stdout、成功時）**: JSON `{"report_url", "card_url", "index_url"}`
- **終了コード**
  - `0` — 成功
  - `1` — 使用法エラー、または必須ファイル（`out/<version>` や `report.html`）が見つからない
  - `3` — commit は成功したが push 失敗、またはリモート未設定
    （呼び出し側は画像なしメールにフォールバックし、push は後で再試行する）

## mark_seen.py

指定したバージョンを既読として記録し、対応する pending JSON を削除する。

- **引数**: `<version> [<version> ...]`（1 つ以上必須）
- **動作**: `state/last_seen.json` の `seen_versions` に追記し、`last_checked` を更新。
  `state/pending/<version>.json` が存在すれば削除する
- **終了コード**
  - `0` — 成功
  - `1` — 引数なし（usage エラー）

## session_link.py

現在の Claude セッション ID を推定する（best-effort）。

- **推定順序**
  1. 環境変数 `CLAUDE_SESSION_ID`
  2. `~/.claude/sessions/` 配下の最新ファイル（ファイル名 → 内容の順で UUID を探す）
- **出力（stdout）**: `{"session_id": "..."}`、見つからなければ `{}`
- **終了コード**: 常に `0`
- **注意**: この ID は CLI 側のセッションファイルに由来し、`get_session self` が返す ID とは
  異なる場合がある。信頼すべきは `get_session self` の方（詳細は
  [design-decisions.md](./design-decisions.md)）。
