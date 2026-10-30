作業フォルダ外への書き込みを、全モードで封じる設定が登場

1. 新設定で Write/Edit が作業フォルダ外を全モードで拒否。他所を壊す事故を防げる
2. VS Code/Desktop で放置した大きな会話を自動要約。再開時の読み直しが軽くなる
3. 組織の effort 上限でも自動で下げて再試行。不具合修正は約80件

今日やること
- 作業フォルダ外を触らせたくない人 → permissions.blockWritesOutsideWorkingDirectories を有効にする
- CI で claude -p を使う人 → 起動失敗が exit 1 になるので失敗時の扱いを確認する
- FORCE_HYPERLINK=false の人 → リンクが無効になる正しい挙動に変わったので表示を確認する
