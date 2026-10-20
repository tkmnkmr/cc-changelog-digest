2.1.304で全リクエスト失敗した不具合を修正。MCP許可リストに仕様変更

1. Vertex・Bedrock 等で全リクエストが失敗した前版の不具合が直った
2. allowedMcpServers の変更で、除外していた MCP が読み込まれ得る
3. /usage の警告が1行の修正案になり、f キーでまとめて直せる

今日やること
- allowedMcpServers で MCP を絞っている管理者 → 止めたいものを deniedMcpServers に書く
- Vertex・Bedrock・ゲートウェイ経由で使っている人 → すぐ 2.1.305 に更新する
- Linux で sandbox.allowNestedUserNamespaces を使う人 → ファイル保護を迂回できる点を理解して有効化する
