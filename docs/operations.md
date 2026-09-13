# 運用

## 毎時の動作

スケジュールタスク `cc-changelog-digest`（毎時 7 分）が `CLAUDE.md` の手順を実行する。

1. `check_update.py` で feed.xml を確認する。
2. `NO_UPDATE` なら何もせず終了（メール送信なし、既読化なし）。
3. `NEW_UPDATE` なら Claude が `state/pending/<version>.json` を材料に執筆し、`render_png.py` →
   `publish.py` → Gmail 送信 → `mark_seen.py` を順に実行する。
4. 複数版が同時に溜まっている場合は全部読み、1 通のメールにまとめる（版ごとのセクションを
   report 内に置く）。

## 手動実行（ドライラン）

既読済みのバージョンでも強制的に pending に出し、公開せずに確認したい場合:

```bash
python3 scripts/check_update.py --force 2.1.270
# ... 執筆 ...
python3 scripts/render_png.py 2.1.270
python3 scripts/publish.py 2.1.270 --no-push   # push せずローカル確認のみ
```

`--no-push` を付けると `site/<version>/` へのコピーと `index.html` 更新、ローカル commit まで行い、
リモートへの push はスキップする。ドライラン後は `mark_seen.py` を実行しないこと（テスト用データを
既読にしてしまうと本番配信が止まる）。

ローカルの feed.xml で試す場合:

```bash
python3 scripts/check_update.py --feed-file tests/fixtures/feed_sample.xml
```

## 失敗時の挙動

- **push 失敗フォールバック**: `publish.py` が exit code 3 で終了した場合（commit は成功したが
  push 失敗、またはリモート未設定）、画像なしのテキストのみメールにフォールバックする。本文に
  「公開に失敗したため画像は省略。ローカル: out/<version>/」と明記する。
- **送信失敗時は既読化しない**: Gmail 送信が失敗した場合 `mark_seen.py` を実行しない。
  次回実行時に同じバージョンが再度 `NEW_UPDATE` として検知され、再送を試みる。
- 判断に迷う場合は「送らない・既読にしない」を選ぶ（保守的に倒す）。

## ブランチ運用の注意

- **作業ツリーは常に `main` ブランチに置く**こと。
- `publish.py` は `git push` 時にチェックアウト中のブランチへ push する（ブランチを指定しない）。
  作業ツリーが `main` 以外のブランチにチェックアウトされていると、意図しないブランチに配信物が
  積まれてしまう。
- GitHub Pages は `main` の `site/` を GitHub Actions（`.github/workflows/pages.yml`）でデプロイして配信する（`docs/setup.md` 参照）。
  したがって配信を機能させるには、スケジュールタスク実行時に作業ツリーが `main` である必要がある。
- 開発作業でブランチを切る場合も、`publish.py` を実行する前には必ず `main` に戻す。
