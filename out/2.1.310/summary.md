Bedrock・Vertex でも Monitor が使える。ゲートウェイ越しの失敗も解消

1. Bedrock・Vertex・Foundry やテレメトリ無効環境でも Monitor が使えるように
2. 一部のゲートウェイ越しでリクエストが失敗する問題を、自動リトライで解消
3. 保存期間を長くすると貼った画像が消える不具合など、細かな修正多数

今日やること
- Bedrock・Vertex・Foundry で使っている人 → 更新して長い待機を Monitor に任せる
- cleanupPeriodDays を大きくしている人 → 早めに更新して画像の消失を防ぐ
