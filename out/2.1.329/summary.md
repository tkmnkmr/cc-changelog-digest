Claude Code v2.1.329、旧版の予約タスクは再登録を。/tasks で一括管理。

1. 旧版で保存した予約タスクの多くは、新しいセッションで再登録が必要に
2. /tasks に予約タスク・/loop・フォークが並び、x で確認して止められる
3. /code-review は引数なしでブランチ全体を、PR は gh pr diff で確実に読む

今日やること
- 予約タスクを使っている人 → 新しいセッションで一覧を確認し、消えたものを再登録
- ゲートウェイで出力上限が小さい人 → CLAUDE_CODE_MAX_OUTPUT_TOKENS を設定
- Code Mode で PreToolUse hook に拒否を任せる人 → "onFailure": "block" を付ける
