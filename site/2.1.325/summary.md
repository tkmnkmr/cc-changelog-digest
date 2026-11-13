Claude Code v2.1.325、サンドボックスBashも確認制に、権限まわりを大幅強化。

1. サンドボックス内の Bash も既定で確認が出る。設定1行で従来どおりに戻せる
2. 定期タスクや /loop は、権限付きスキルの実行前に確認待ちになる
3. 許可ルールのすり抜けやサブエージェントのモデル取り違えを多数修正

今日やること
- サンドボックスで Bash を無確認で回す人 → sandbox.autoAllowBashIfSandboxed: true を設定する
- 定期タスクや /loop でスキルを使う人 → permissions.allow に Skill(名前) を追加する
- プロジェクト外のリポジトリで git を読ませる人 → --add-dir で指定する
