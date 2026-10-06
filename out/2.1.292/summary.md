Claude Code v2.1.292、サブエージェントの思考量を指定可能に。セキュリティ修正も多数。

1. Agent ツールに effort 指定が追加。サブエージェントを軽く・深く使い分けられる
2. ネットワークパス読み取りの許可すり抜けなど、セキュリティ修正が多数入った
3. /resume 後の予約タスク不発や plan mode の戻り忘れなど、日常の不具合も解消

今日やること
- claude plugin test を使っている人 → テストを再実行し、新たな失敗がないか確認する
- 古い stdio MCP サーバーで不調な人 → MCP_PROTOCOL_NEGOTIATION=legacy を試す
