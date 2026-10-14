Claude Code v2.1.300、OTelでキャッシュ費用が丸見えに。hooks入力の検証も厳格化。

1. OTelにGenAI標準属性と、キャッシュ書込みの5分/1時間内訳。費用分析が楽に
2. hooksが返すupdatedInputを厳格に検証。不正な入力ならツール呼び出しを拒否
3. remote-controlの--sandboxフラグは廃止しエラーに。新モデルはなし

今日やること
- remote-controlで--sandboxを使う人 → sandbox.enabledへ移行
- hooksでupdatedInputを返している人 → 未知キーや不正な値がないか確認する
- トランスクリプトを共有する人 → システムプロンプト等も含まれる点に注意する
