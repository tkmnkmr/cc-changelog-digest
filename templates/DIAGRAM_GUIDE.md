# 図・執筆規約（LLM 向け）

report.html / card.html / post.md を埋めるときに必ず守ること。ここに書かれた SVG スニペットは
コピーしてテキストだけ差し替えて使う。**構造（タグ・座標・class）は変えない**。テキストが
上限を超えそうな場合は文言を削って収める（フォントサイズを変えて逃げない）。

## 共通ルール

- ラベル（図中の短い語句）: **20字以内**
- 説明文（図中・本文の一文）: **50字以内**
- CHANGELOG の文をそのまま貼らない。必ず自分の言葉で「何が嬉しいか」を書く。主語はユーザー。
  - 悪い例: 「Bash tool の read-only git コマンド判定を修正」（CHANGELOGそのまま）
  - 良い例: 「長時間セッションでも git status 確認が止まらなくなった」（ユーザー視点）
- 色は下表のカテゴリ色を厳守する（report.html の CSS 変数と同じ値）。

| カテゴリ | 用途 | 色 |
|---|---|---|
| breaking | 破壊的変更 | `#E5484D`（赤） |
| major | 大幅アップデート | `#A78BFA`（紫） |
| model | 新モデル | `#5B9DF9`（青） |
| new | 新規 | `#34D399`（緑） |
| update | 更新 | `#F0B429`（琥珀） |
| deprecated | 廃止 | `#8A8F98`（灰） |

- SVG は `viewBox` のみ指定し、`width`/`height` は付けない（親要素で拡縮させる）。
- フォントは SVG 内では `font-family="ui-monospace, monospace"` か
  `font-family="Hiragino Kaku Gothic ProN, sans-serif"` を明示する（親のCSSが継承されない場合があるため）。

---

## 型1: Before/After 対比図

左右2ペインで「アップデート前」「アップデート後」を対比する。矢印は中央に1本のみ。

```svg
<svg viewBox="0 0 900 220" xmlns="http://www.w3.org/2000/svg" font-family="Hiragino Kaku Gothic ProN, sans-serif">
  <!-- Before pane -->
  <rect x="0" y="0" width="400" height="200" rx="12" fill="#1C1F27" stroke="#2A2E38"/>
  <text x="24" y="34" font-size="12" fill="#8A8F98" letter-spacing="1">BEFORE</text>
  <text x="24" y="70" font-size="16" fill="#E8EAED" font-weight="700">{{20字以内のラベル}}</text>
  <text x="24" y="98" font-size="13" fill="#9AA1AC">{{50字以内の説明（複数行は</text>
  <text x="24" y="118" font-size="13" fill="#9AA1AC">tspanで改行、1行20字目安）}}</text>

  <!-- Arrow -->
  <line x1="410" y1="100" x2="480" y2="100" stroke="#F5A623" stroke-width="3"/>
  <polygon points="480,92 498,100 480,108" fill="#F5A623"/>

  <!-- After pane -->
  <rect x="500" y="0" width="400" height="200" rx="12" fill="#1C1F27" stroke="#34D399"/>
  <text x="524" y="34" font-size="12" fill="#34D399" letter-spacing="1">AFTER</text>
  <text x="524" y="70" font-size="16" fill="#E8EAED" font-weight="700">{{20字以内のラベル}}</text>
  <text x="524" y="98" font-size="13" fill="#9AA1AC">{{50字以内の説明}}</text>
</svg>
```

- 各ペインの説明は 2 行までに収め、1 行あたり全角 20 字目安で `tspan` か `text` を分けて改行する。
- 「嬉しさ」が伝わる語（例: 「待たされない」「確認が要らなくなった」）を AFTER 側に必ず入れる。

---

## 型2: フロー図（横方向のステップ）

3〜5 ステップの処理の流れを示す。ステップ数が変わっても構造の繰り返しパターンは同じ。

```svg
<svg viewBox="0 0 900 140" xmlns="http://www.w3.org/2000/svg" font-family="Hiragino Kaku Gothic ProN, sans-serif">
  <!-- Step 1 -->
  <rect x="0" y="20" width="180" height="80" rx="10" fill="#1C1F27" stroke="#2A2E38"/>
  <text x="90" y="55" font-size="13" fill="#E8EAED" text-anchor="middle" font-weight="700">{{20字以内}}</text>
  <text x="90" y="76" font-size="11" fill="#9AA1AC" text-anchor="middle">{{補足12字程度}}</text>

  <line x1="180" y1="60" x2="220" y2="60" stroke="#5B6270" stroke-width="2"/>
  <polygon points="220,54 234,60 220,66" fill="#5B6270"/>

  <!-- Step 2 -->
  <rect x="234" y="20" width="180" height="80" rx="10" fill="#1C1F27" stroke="#2A2E38"/>
  <text x="324" y="55" font-size="13" fill="#E8EAED" text-anchor="middle" font-weight="700">{{20字以内}}</text>
  <text x="324" y="76" font-size="11" fill="#9AA1AC" text-anchor="middle">{{補足12字程度}}</text>

  <line x1="414" y1="60" x2="454" y2="60" stroke="#5B6270" stroke-width="2"/>
  <polygon points="454,54 468,60 454,66" fill="#5B6270"/>

  <!-- Step 3 (最終ステップは強調色にしてよい) -->
  <rect x="468" y="20" width="180" height="80" rx="10" fill="#1C1F27" stroke="#F5A623"/>
  <text x="558" y="55" font-size="13" fill="#E8EAED" text-anchor="middle" font-weight="700">{{20字以内}}</text>
  <text x="558" y="76" font-size="11" fill="#F5A623" text-anchor="middle">{{補足12字程度}}</text>
</svg>
```

- ステップを増減する場合は `x` を 234 刻みでずらし、`viewBox` の幅を `234*N + 220` 程度に調整する。
- 矢印の向きは常に左→右。逆方向のフローを表現しない。

---

## 型3: 3列カード（新規 / 更新 / 廃止）

**report.html の 06 セクションでは使わない**（`.cols3` の HTML 版カードと内容が重複するため、
06 は `.cols3` のテキストリストのみで構成する）。card.html や他セクションで3カテゴリを
図解したい場合にのみ、この型を使ってよい。

```svg
<svg viewBox="0 0 900 160" xmlns="http://www.w3.org/2000/svg" font-family="Hiragino Kaku Gothic ProN, sans-serif">
  <!-- New -->
  <rect x="0" y="0" width="280" height="160" rx="12" fill="rgba(52,211,153,0.10)" stroke="#34D399"/>
  <circle cx="24" cy="28" r="5" fill="#34D399"/>
  <text x="40" y="33" font-size="13" fill="#34D399" font-weight="700">新規</text>
  <text x="20" y="66" font-size="14" fill="#E8EAED" font-weight="700">{{20字以内}}</text>
  <text x="20" y="90" font-size="12" fill="#9AA1AC">{{50字以内の説明}}</text>

  <!-- Update -->
  <rect x="310" y="0" width="280" height="160" rx="12" fill="rgba(240,180,41,0.10)" stroke="#F0B429"/>
  <circle cx="334" cy="28" r="5" fill="#F0B429"/>
  <text x="350" y="33" font-size="13" fill="#F0B429" font-weight="700">更新</text>
  <text x="330" y="66" font-size="14" fill="#E8EAED" font-weight="700">{{20字以内}}</text>
  <text x="330" y="90" font-size="12" fill="#9AA1AC">{{50字以内の説明}}</text>

  <!-- Deprecated -->
  <rect x="620" y="0" width="280" height="160" rx="12" fill="rgba(138,143,152,0.10)" stroke="#8A8F98"/>
  <circle cx="644" cy="28" r="5" fill="#8A8F98"/>
  <text x="660" y="33" font-size="13" fill="#8A8F98" font-weight="700">廃止</text>
  <text x="640" y="66" font-size="14" fill="#E8EAED" font-weight="700">{{20字以内}}</text>
  <text x="640" y="90" font-size="12" fill="#9AA1AC">{{50字以内の説明}}</text>
</svg>
```

- 3 カテゴリいずれかが「該当なし」の場合、そのカードのテキストを「該当なし」にする（カードごと消さない）。

---

## X 投稿文（post.md）の執筆規約

- 文字数: **140〜280 字**（日本語は1文字1カウント）。
- 冒頭 1 文で結論（今回の目玉は何か）を言い切る。
- 絵文字は **3 個以内**。多用しない。
- ハッシュタグは末尾に `#ClaudeCode` を必ず入れる（他タグは任意で1〜2個まで）。
- CHANGELOG の文をそのまま引用しない。エンジニアが「へえ」と思う角度（体験の変化）で書く。
- 破壊的変更がある回は、投稿文の中でも軽く触れる（隠さない）。

### 例（型として参考にする。数値・内容はダミー）

> Claude Code v2.1.270、地味だけど効くやつが来た。長時間セッション後の Bash 権限確認が減って、read-only な git コマンドが素通りするように。ついでに新モデルも追加でコード生成がさらに速く。破壊的変更が1件あるので移行ガイドだけ要チェック。 #ClaudeCode

---

## card.html 執筆規約

- 大見出し（VERSION）以外の文字はすべて上限を超えたら**削って**収める。縮小フォントで逃げない。
- `HEADLINE` は 40 字以内、体言止めでも可。
- `POINT_1`〜`POINT_4` は各 30 字以内。絵文字は各ポイント先頭に1個まで。
- 破壊的変更が無い回は `BREAKING_BADGE` のブロックごと削除する（空バッジを表示しない）。
