既定モデルが Opus 5.5 に。Pro でも標準で Opus が動く

1. Opus 5.5 が既定の Opus に。1M コンテキストで大きな作業も一度に読める
2. Pro と Team Standard の既定モデルも Sonnet から Opus に変わった
3. ダイアログの y / n は効かなくなった。確定は Enter、取り消しは Esc

今日やること
- ダイアログを y / n で操作していた人 → keybindings.json で割り当て直す
- PermissionRequest フックに agent を使っている人 → command か http に移す
- Pro / Team Standard の人 → 既定が Opus になるので /model を確認する
