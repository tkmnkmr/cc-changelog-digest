# cc-changelog-digest

Claude Code の CHANGELOG 更新を検知し、図付き HTML 資料（X の AI インフルエンサー投稿を
文体・構成の手本にした、結論先出し・短文のまとめ）を生成してメールで配信するための足場スクリプト群。

## 目的

- 公式 Atom フィード（`https://raw.githubusercontent.com/anthropics/claude-code/main/feed.xml`）
  をポーリングし、新しいバージョンのリリースノートを検知する。
- リリースノートを「ヘッドライン／3行でわかる／前後の変化／注目トピック／機能の追加・更新・廃止」
  という観点で整理し、`templates/` を使って HTML 資料（report.html）・まとめ画像
  （card.html → card.png）・summary.md（ヘッドライン＋3行でわかる＋今日やること）を作る。
- 生成物を GitHub Pages（`docs/`）に公開し、メールで配信する。

実際の文章整理・資料執筆は Claude（スケジュールタスク）が担当する。このリポジトリの
`scripts/` は検知・分類の下準備・画像化・公開・既読管理という「機械的な部分」のみを担う。

## 構成

```
scripts/
  check_update.py   feed.xml を取得し新着バージョンを検知、state/pending/<ver>.json を書く
  classify.py       キーワード辞書によるプレ分類（breaking/major/model/added/changed/removed/fixed/other）
  render_png.py     out/<ver>/card.html・report.html を playwright で PNG 化
  publish.py        out/<ver> を docs/<ver> にコピーし、index.html 更新、git commit & push
  mark_seen.py      state/last_seen.json に既読バージョンを追記、pending JSON を削除
  session_link.py   実行中セッション ID の推定（best-effort）
templates/          report.html / card.html / email.html などのテンプレ（別担当が作成）
state/
  last_seen.json    既読バージョン一覧と最終チェック時刻
  pending/          未処理の新着バージョン JSON（.gitignore 対象）
out/                生成物（report.html, card.html, *.png, summary.md）バージョンごとのディレクトリ
docs/               GitHub Pages 公開先（index.html + <ver>/）
tests/              unittest 一式、フィクスチャは tests/fixtures/
```

## 手動実行手順

```bash
# 1. 新着チェック（NEW_UPDATE / NO_UPDATE を標準出力に、新着があれば state/pending/<ver>.json を生成）
python3 scripts/check_update.py

# ローカルの feed.xml で試す場合
python3 scripts/check_update.py --feed-file tests/fixtures/feed_sample.xml

# 既読でも強制的に pending に出したい場合（ドライラン用）
python3 scripts/check_update.py --force 2.1.270

# 2. (Claude が) state/pending/<ver>.json を読み、templates/ を使って
#    out/<ver>/report.html, out/<ver>/card.html, out/<ver>/summary.md を作成する

# 3. PNG 化
python3 scripts/render_png.py 2.1.270

# 4. 公開（GitHub Pages への commit & push）
python3 scripts/publish.py 2.1.270
python3 scripts/publish.py 2.1.270 --no-push   # push せずローカル確認のみ

# 5. 配信できたら既読化
python3 scripts/mark_seen.py 2.1.270

# セッションリンクの推定（best-effort、失敗しても exit 0）
python3 scripts/session_link.py
```

## テスト

```bash
python3 -m unittest discover -s tests
```

## 分類ロジックについて

`scripts/classify.py` は `~/code/rss-changelog-monitor/changelog_parser.py` の
キーワード辞書による分類方式を参考に、このプロジェクト向けのカテゴリ
（breaking / major / model / added / changed / removed / fixed / other）で
再構成したものです（コピペではなく自作コード）。

## 依存関係

- Python 3 標準ライブラリのみで `check_update.py` / `classify.py` / `publish.py` /
  `mark_seen.py` / `session_link.py` は動作する。
- `render_png.py` のみ `playwright`（`requirements.txt` 参照）と Chromium が必要。
  開発機では playwright も chromium も既にインストール済みの前提。
