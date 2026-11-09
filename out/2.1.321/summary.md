Claude Code v2.1.321、新モデル Fable 5.2 が既定に。権限まわりの安全修正も多数。

1. Fable 5.2 が既定の Fable モデルに。1M コンテキストで長い作業も一度に扱える
2. MCP OAuth のトークン漏えいや、確認なしの書き込みなど安全面の穴が塞がれた
3. Gateway の Bedrock/Vertex/Foundry は環境変数の接続先を無視。base_url 指定が必要

今日やること
- Gateway で Bedrock/Vertex/Foundry を使う人 → 接続先を upstream の base_url に移す
- Fable 5.1 を使い続けたい人 → /model claude-fable-5-1 で戻す
- mods を使う管理者 → auto/bypass で確認なしに有効化される点を確認する
