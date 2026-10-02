Claude Code v2.1.288、Ctrl+C で消した入力が↑で戻る。途中切れにも強くなった

1. Ctrl+C で消したプロンプトも、空欄で↑を押せば貼った画像ごと戻る
2. 応答途中で API が切れても、-p 実行やサブエージェントは続きから再開
3. --resume で文脈や最後の返答が欠ける不具合をまとめて修正

今日やること
- スクリプトで claude project purge を使う人 → claude purge に書き換える
- /autocompact を変えている人 → モデル切替後に設定を確認する
- Mantle やゲートウェイ経由で不調な人 → CLAUDE_CODE_DISABLE_STRUCTURED_OUTPUTS を試す
