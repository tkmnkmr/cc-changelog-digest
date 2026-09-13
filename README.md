# cc-changelog-digest

Claude Code の CHANGELOG 更新を検知し、図付きメールで配信する。

## 1. 全体フロー

```mermaid
flowchart LR
    A[feed.xml] --> B[check_update]
    B --> C[Claudeが執筆]
    C --> D[render_png]
    D --> E["publish(site/→Pages)"]
    E --> F[Gmail送信]
    F --> G[mark_seen]
```

新着リリースを検知し、執筆・画像化・公開・送信・既読化までを自動で行う。

## 2. 届くもの

```mermaid
flowchart TD
    A["結論一文"] --> B["まとめ画像"]
    B --> C["3行でわかる"]
    C --> D["注目トピック"]
    D --> E["今日やること"]
    E --> F["資料リンク"]
```

結論から入り、画像・要点・注目トピック・行動・詳細リンクの順で読める。

サンプル画像（架空データ、実際のリリース内容ではありません）:

![サンプルカード](examples/sample/card.png)

## 3. 動作の仕組み

```mermaid
sequenceDiagram
    participant S as スケジュールタスク
    participant C as check_update
    participant Claude
    S->>C: 毎時7分に実行
    alt NO_UPDATE
        C-->>S: 更新なしで終了
    else NEW_UPDATE
        C-->>Claude: pending/<version>.json
        Claude->>Claude: 執筆〜render〜publish
        Claude->>Claude: Gmail送信
        Claude->>Claude: mark_seen（送信成功時のみ）
    end
```

更新が無ければ何もせず終わる。あるときだけ執筆から送信まで一気通貫で進む。

## 4. 状態管理

```mermaid
stateDiagram-v2
    [*] --> 未読
    未読 --> pending: check_update
    pending --> 公開済み: publish
    公開済み --> 既読: 送信成功
    公開済み --> pending: 送信失敗（再送）
```

送信に失敗した版は既読化されず、次回また自動で再送が試みられる。

## 5. ディレクトリ構成

```
scripts/
  check_update.py   feed.xmlを取得し新着バージョンを検知、state/pending/<ver>.jsonを書く
  classify.py       キーワード辞書によるプレ分類（breaking/major/model/added/changed/removed/fixed/other）
  render_png.py     out/<ver>/card.html・report.htmlをplaywrightでPNG化
  publish.py        out/<ver>をsite/<ver>にコピーし、index.html更新、git commit & push
  mark_seen.py      state/last_seen.jsonに既読バージョンを追記、pending JSONを削除
  session_link.py   実行中セッションIDの推定（best-effort）
templates/          report.html/card.html/email.htmlなどのテンプレと執筆規約
state/
  last_seen.json    既読バージョン一覧と最終チェック時刻
  pending/          未処理の新着バージョンJSON（.gitignore対象）
out/                生成物（report.html, card.html, *.png, summary.md）バージョンごと
site/               GitHub Pages公開先（index.html + <ver>/）
tests/              unittest一式、フィクスチャはtests/fixtures/
docs/               詳細ドキュメント（setup/operations/scripts/writing-guide/design-decisions）
```

## 6. はじめ方

1. `pip install -r requirements.txt` で依存関係を入れる。
2. Claude デスクトップで Gmail 連携とスケジュールタスクを設定する。
3. `python3 scripts/check_update.py` で動作確認する。

詳細手順は [docs/setup.md](docs/setup.md) を参照。

## 7. 詳細ドキュメント

- [docs/setup.md](docs/setup.md) — セットアップ・Pages設定・スケジュールタスク登録
- [docs/operations.md](docs/operations.md) — 日々の運用・手動実行・失敗時の挙動
- [docs/scripts.md](docs/scripts.md) — 各スクリプトの引数・出力・終了コード
- [docs/writing-guide.md](docs/writing-guide.md) — 執筆の考え方の概要
- [docs/design-decisions.md](docs/design-decisions.md) — 設計判断とその理由

テストの実行:

```bash
python3 -m unittest discover -s tests
```
