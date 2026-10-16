claude -p の権限既定が変更。fork型サブエージェントも既定ON

1. Bedrock・Vertex経由の -p やSDKは、権限モード未指定だと default で起動する
2. fork型サブエージェントが -p・SDK・デスクトップ・VS Codeでも既定で使える
3. 単体版Claude Designは12/14終了の告知。新モデルの追加はなし

今日やること
- Bedrock等で -p・SDKを無人実行する人 → --permission-mode auto を明示する
- fork型サブエージェントを避けたい人 → CLAUDE_CODE_FORK_SUBAGENT=0 を設定する
- 単体版Claude Designを使う人 → 12/14の終了までに移行先を確認する
