Claude Code v2.1.282、セッション再開で思考が消える不具合を一掃。

1. --continue や --resume で再開しても、Claude が前の思考を引き継ぐようになった
2. 毎回400エラーで会話が詰む症状が直り、コンパクション失敗も自動で立て直す
3. プロジェクト設定のテレメトリ指定は無視される。skill の予約名も増えた

今日やること
- プロジェクト設定でテレメトリを有効にしていた人 → ユーザー設定か managed 設定へ移す
- anthropic-skills / claude-ai と名付けた skill や MCP サーバーがある人 → 別名に変える
- auto mode を使う人 → サーバー側の判定を避けるなら CLAUDE_CODE_AUTO_MODE_SERVER=0 を設定
