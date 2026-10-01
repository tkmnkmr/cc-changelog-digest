Claude Code v2.1.287、Claude Mods 登場。MCP が繋がらない時は設定1行で回避

1. Claude Mods 追加。プラグインでより深い挙動まで変えられるようになった
2. 新しい MCP 規格のサインイン用 URL に対応。繋がらなければ設定1行で回避
3. Bedrock・Vertex 等で Opus 4.7 以降と Fable が既定で 1M コンテキストに

今日やること
- MCP サーバーを使っている人 → 繋がらなければ bareElicitationCapability: true を足す
- OpenTelemetry で prompt を隠している人 → prompt_text も同様に隠す
- Bedrock 等で 200K に留めたい人 → CLAUDE_CODE_DISABLE_1M_CONTEXT=1 を設定する
