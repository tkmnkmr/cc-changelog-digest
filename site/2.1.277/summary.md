Claude Code v2.1.277、AGENTS.md 対応とクラッシュの大量修正。

1. CLAUDE.md が無いプロジェクトでは AGENTS.md がそのまま指示として読まれる
2. 起動・再開時のクラッシュや固まりが多数直り、設定が壊れていても落ちない
3. TaskOutput ツールは廃止。taskOutputMaxChars などの設定はもう効かない

今日やること
- TaskOutput の出力上限を設定している人 → 設定を外し Read 前提に直す
- sandbox.excludedCommands を使っている人 → 複合コマンドの除外条件を再確認
- CLAUDE.md の無いリポジトリで作業する人 → AGENTS.md が読まれるか確認
