古いCLAUDE.mdを点検する新コマンド追加、一部環境は自動モード既定に

1. CLAUDE.md や skill に残った旧モデル向けの書き方を /doctor が指摘してくれる
2. 第三者プロバイダやテレメトリ無効の環境は、既定で auto mode 開始に変わった
3. MCP とプラグイン周りの不具合が大量に直り、一覧操作と起動も速くなった

今日やること
- Bedrock/Vertex などやテレメトリ無効で使う人 → permissions.defaultMode を明示する
- claude plugin eval を使う人 → git を 2.31 以上に上げる
- 組織でモデルを絞りたい管理者 → deniedModels と availableModelsMatch を設定する
