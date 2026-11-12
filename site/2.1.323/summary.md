Claude Code v2.1.323、Code Mode が試験登場、権限の穴も一斉修正。

1. Claude が JavaScript でツールを呼ぶ Code Mode を試験的にオンにできる
2. Bash 権限やサンドボックスのすり抜けが多数ふさがれ、任せても安心度が上がった
3. 未知のモデルIDは1M前提に変更。窓の小さい他社モデル利用者は設定が必要

今日やること
- 他社モデルを使う人 → CLAUDE_CODE_DISABLE_1M_CONTEXT=1 を設定する
- ALL_PROXY だけでプロキシを通している人 → HTTPS_PROXY も設定する
- サンドボックスでリンク経由の書き込み許可を使う人 → 実パスで許可し直す
