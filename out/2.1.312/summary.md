巨大CLAUDE.mdの上書き事故を防止。Bedrock独自名は短いプロンプトに

1. 大きな CLAUDE.md やルールを先頭だけ読んで上書きする事故がなくなった
2. Bedrock/Vertex等の独自デプロイ名は短いプロンプトに。環境変数で戻せる
3. Entra ID の oid で利用者を識別できるように。不具合修正は22件

今日やること
- Bedrock等で独自デプロイ名を使う人 → 全文が要るなら CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT=0
- 独自デプロイ名で自動モデル切替を避けたい人 → CLAUDE_CODE_DISABLE_REFUSAL_FALLBACK=1
- OTel で claude_code.safety_event を集計している人 → 送信停止に合わせ見直す
