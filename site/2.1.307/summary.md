MCP の二重実行とスリープ後の失敗を修正。runner は30分上限に注意

1. HTTP MCP が通信途中で切れても、書き込み系ツールが二重に実行されなくなった
2. PC のスリープや鍵束ロック後も、MCP が失敗扱いのまま残らなくなった
3. self-hosted runner の checkout hook は既定30分で打ち切り。長い人は設定が必要

今日やること
- self-hosted runner で30分超の checkout hook を使う人 → --checkout-hook-timeout-min を上げる
- プロジェクト設定で axScreenReader を指定している人 → ユーザー設定へ移す
