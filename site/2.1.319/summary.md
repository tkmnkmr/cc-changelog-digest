Claude Code v2.1.319、auto mode の判定方式が変更、MCP の長い処理は自動で裏へ。

1. テレメトリ等を切った環境の auto mode は、旧判定に戻らず確認か拒否になる
2. MCP の長いツール呼び出しが自動で裏に回り、待たずに作業を続けられる
3. Bash の権限すり抜けや worktree のサンドボックス脱出など、安全面の修正が多数

今日やること
- LLM ゲートウェイ等で auto mode を使う人 → 確認が増えたら AUTO_MODE_SERVER=0 を検討
- self-paced /loop を使う人 → 旧挙動が必要なら CLAUDE_CODE_LOOP_KEEPALIVE=1 を設定
- MCP の結果を同期で待ちたい人 → CLAUDE_CODE_DISABLE_MCP_TASK_BACKGROUND を設定
