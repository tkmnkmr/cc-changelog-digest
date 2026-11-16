Claude Code v2.1.326、サンドボックスと権限がさらに厳格に、修正は200件超。

1. サンドボックスは機密フォルダへの書込みを既定で禁止。必要なら allowWrite で許可
2. hook の block 判定や auto mode の許可ルール判定が厳しくなり、止まる操作が増える
3. 画面のちらつき・入力消失・再開時の履歴欠落など200件超の不具合を修正

今日やること
- サンドボックスでホーム配下に書かせている人 → sandbox.filesystem.allowWrite で許可する
- 常に decision: block を出す hook がある人 → 意図せず止めないか確認する
- worktree で git の filter や helper を使う人 → フルパス指定に直す
