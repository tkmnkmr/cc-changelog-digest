サンドボックスと権限の抜け穴を一斉修正。ultrareviewは信頼確認が必須に

1. サンドボックス外で起動ファイルが走る等、権限まわりの抜け穴を十数件ふさいだ
2. claude ultrareview は信頼確認が必須に。スクリプトは --trust-workspace が要る
3. sed -i は通常の Bash 確認を経て実行。/rewind では戻らなくなった

今日やること
- claude ultrareview をスクリプトで回す人 → --trust-workspace を付ける
- sed -i の編集を /rewind で戻していた人 → git で戻す運用に切り替える
