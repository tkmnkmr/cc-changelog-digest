Claude Code v2.1.292、サブエージェントの思考量を指定可能に。セキュリティ修正も多数。

1. Agent ツールに effort 指定が加わり、サブエージェントの思考量を選べる
2. 権限プロンプトのすり抜けなど、セキュリティの穴を多数ふさいだ
3. 予約タスクや /loop が止まる・消える不具合が直った

今日やること
- auto モードや PreToolUse フックで承認している人 → 早めに更新する
- stdio の MCP サーバーを使う人 → 接続不調なら MCP_PROTOCOL_NEGOTIATION=legacy を試す
- claude plugin test を回している人 → 再実行し新たな失敗がないか確認する
