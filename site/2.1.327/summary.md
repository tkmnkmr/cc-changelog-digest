Claude Code v2.1.327、権限確認が増え、ファイル消失系の不具合を一掃。

1. /status で壊れた agent・skill・hook 設定を一覧表示。設定ミスにすぐ気づける
2. auto mode や作業フォルダ外の読み取りで、確認・拒否される操作が増える
3. .env や .mcp.json が消える、/export が無断で上書きする等の事故を修正

今日やること
- auto mode で pnpm dlx 等を許可ルールで通している人 → 止まらないか確認する
- 入れ子の claude に OAuth スコープが要る人 → CLAUDE_CODE_OAUTH_SCOPES を明示する
- 承認前のシェル起動を避けたい人 → CLAUDE_CODE_DISABLE_SHELL_HEAD_START=1 を設定
