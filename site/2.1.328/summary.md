Claude Code v2.1.328、Code Mode が高速化、他社クラウドは auto mode 既定に。

1. Bedrock・Agent Platform・Foundry の Opus/Sonnet 4.6 で auto mode が既定に
2. Code Mode はスクリプト後の待ちが消え、実行中の出力も見えるように
3. /code-review はバグと CLAUDE.md 違反に集中。整理提案は /simplify へ

今日やること
- Bedrock 等で Opus/Sonnet 4.6 を使う人 → auto mode が不要なら disableAutoMode を設定
- Code Mode 出力を UserPromptSubmit hook で伏せている人 → PostToolUse hook に移す
- /code-review で整理提案も見ていた人 → /simplify を併用する
