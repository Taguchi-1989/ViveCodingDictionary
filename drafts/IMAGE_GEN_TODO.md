# 画像生成 TODO — 前付け 7 見開き ＋ 巻末あとがき

HTML たたき台に置いた「イラスト枠」「サムネ枠」を、最終的に画像生成（または手描き）で差し替えるための一覧です。各枠について「どこに置くか」「何を描くか」「プロンプト案」をまとめてあります。

著者がレビュー → プロンプト調整 → 画像生成 → HTML 内の該当 div を `<img>` に置換、という流れを想定しています。

## トーン共通方針

全枠で揃えるトーン：

- **白地・濃紺（#123E82）・薄青（#EAF1FB）** の 3 色基調
- **線画主体**、塗りは最小限。余白多め
- **抽象人物**: 性別・職種・年齢が出ない、シンプルな線で描いた人物
- **装飾より構造**: 図表・余白で品よく見せる
- **吹き出しは最小限**、文字情報は本文側に逃がす
- 印刷想定: ビジネス書〜技術書の落ち着いたトーン

参考: [drafts/opening_spread_brief.md](opening_spread_brief.md) §「最終的に絵へ落とすときのプロンプト方針」

## チェックリスト

| 進捗 | スプレッド | 枠数 | ファイル |
|:-:|:--|:-:|:--|
| ☑ | 0. 扉 | 4 | [front_section/0_concept_spread.html](front_section/0_concept_spread.html) |
| ☑ | 1. まえがき | 1 | [front_section/1_a1_preface.html](front_section/1_a1_preface.html) |
| ☑ | 2. 見開き分解図 | 1（下地） | [front_section/2_a2_anatomy.html](front_section/2_a2_anatomy.html) |
| ☑ | 3. 図鑑の歩き方＋索引 | 1 | [front_section/3_a3_a9_map_index.html](front_section/3_a3_a9_map_index.html) |
| ☐ | 4. 注意マーク凡例 | 0（記号のみ） | [front_section/4_a4_a5_a6_legend_marks.html](front_section/4_a4_a5_a6_legend_marks.html) |
| ✕ | 5. 図と色の見本帳 | 0（枠廃止） | [front_section/5_a7_a8_swatch.html](front_section/5_a7_a8_swatch.html) |
| ☐ | 6. 更新履歴と略称 | 0（タイムライン CSS） | [front_section/6_a10_a11_log_glossary.html](front_section/6_a10_a11_log_glossary.html) |
| ☑ | 7. あとがき | 1 | [back_section/afterword.html](back_section/afterword.html) |

**合計画像枠: 13 枠 → 実装 8 枠**（本気イラスト 6 / 大判下地 1 / 見開きミニチュア 1）。**ミニサムネ 5 枠は枠ごと廃止**（A-7「図のタイプ」が v2 で廃止されたため。生成済みの `5-1`〜`5-5_thumb_*.png` は未使用のまま `assets/front_section/generated/` に残しています）

**2026-09-07 時点で 8 枠すべて HTML に差し込み済み**です。

---

## 0. 扉「知らないことばで、止まらない。」

### 枠 0-1: 左ページ 3 コマ「困る → 引く → 戻る」（コマ 1）

- **場所**: 左ページ下段の 3 グリッド・1 枚目
- **描く内容**: 抽象人物が会話の輪の中で「？」を浮かべて止まっている。横に「知らない語」のシルエット
- **構図**: 正方形フレーム、人物バストアップ、背景に淡い線で会話の波形
- **プロンプト案**:
  ```
  Abstract minimalist line drawing, single human figure (no gender/age),
  navy ink on white background, head slightly tilted with a question mark
  above. Faint wave lines suggesting conversation in the background.
  Soft pale blue (#EAF1FB) accent. Square frame. Business book illustration
  style. Lots of whitespace.
  ```

### 枠 0-2: 左ページ 3 コマ・2 枚目「引く」

- **場所**: 同上、2 枚目
- **描く内容**: 同じ人物が本（この図鑑）を手に取って開いている瞬間
- **プロンプト案**:
  ```
  Same abstract figure as previous, navy ink on white, now holding an open
  book. Lines from the book pages suggesting words. Soft pale blue accent.
  Square frame. Whitespace dominant.
  ```

### 枠 0-3: 左ページ 3 コマ・3 枚目「会話に戻る」

- **場所**: 同上、3 枚目
- **描く内容**: 同じ人物が会話の輪に戻り、相手に向かって話しかけている
- **プロンプト案**:
  ```
  Same abstract figure, navy ink on white, now facing another figure
  (also abstract), speech bubble with simple geometric shapes (no text).
  Confident posture. Soft pale blue accent. Square frame.
  ```

### 枠 0-4: 右ページ 見開きミニチュア

- **場所**: 右ページ中央
- **描く内容**: 本書 1 見開き（左右ページ）のミニチュア俯瞰図。左ページに「タグ帯・図・ポンチ絵」、右ページに「6 視点・フロー・関連語ピル」が小さく並ぶ
- **HTML 内に既に CSS でラフ実装あり**。画像化する場合は精度高めに
- **プロンプト案**:
  ```
  Two-page book spread isometric view, navy ink line drawing on white.
  Left page has: blue tagline bar at top, main figure box in middle,
  small character icon at bottom. Right page has: 2x3 grid of icons,
  horizontal step flow, row of pill-shaped tags. Pale blue (#EAF1FB)
  for accent areas. Clean editorial style.
  ```

---

## 1. まえがき (A-1)

### 枠 1-1: 大判の「ことばの橋」イラスト

- **場所**: 左ページ中央〜下段（最大ボリューム）
- **描く内容**: 抽象人物 2 名が短い橋を挟んで向かい合う。橋の上に「ことば」と書かれた短冊。性別・職種が出ない
- **構図**: 横長フレーム、橋が中央、人物は左右、文字（短冊）は中央上方
- **既存資産**: 旧 A-1 サンプル p.02「はじめに」の構図を参照
- **プロンプト案**:
  ```
  Abstract conceptual line drawing, two simplified human figures facing each
  other across a small wooden bridge. A vertical paper banner reading
  "ことば" (Japanese for "words") hangs above the bridge. Navy ink
  (#123E82) on white. No gender, no profession indicators. Minimal lines.
  Generous whitespace. Horizontal landscape composition. Business-essay
  book frontispiece.
  ```

---

## 2. 見開きの読み方 (A-2)

### 枠 2-1: 中央下地の「本編エントリ見開き」（半透明）

- **場所**: 見開き中央に薄く敷く（13 個のコールアウト矢印が指す対象）
- **描く内容**: 本編 F-2 TypeScript の実物見開きを 60% 縮小・半透明 42%
- **代替案**: 実際の F-2 を Playwright スクショ → グレーアウト処理して埋め込み
- **HTML 内に既にラフ実装あり**。最終版は実物スクショ推奨
- **プロンプト不要**（撮影ベース）

---

## 3. 図鑑の歩き方＋索引 (A-3 + A-9)

### 枠 3-1: 左ページ A〜J 地図 + 3 ルート

- **場所**: 左ページ中央
- **描く内容**: A〜J の 10 ノードが円環または横並びで配置。各ノードに章ラベル。3 本の色違いの線（薄青／緑／橙）が異なるルートを示す
- **HTML 内に既に CSS グリッドでラフ実装あり**。画像化する場合は地図感を強める
- **プロンプト案**:
  ```
  Editorial infographic, 10 labeled nodes A through J arranged in a circle
  or horizontal row, each with a Japanese theme label. Three colored lines
  (light blue, green, orange) connecting different paths through the nodes.
  Navy ink (#123E82) on white background. Minimal line work. Legend in
  bottom right corner. Clean technical book style.
  ```

---

## 4. 注意マーク凡例 (A-4 + A-5 + A-6)

イラスト枠なし（記号・タグ・カードのみ）。HTML の現状で完成度高い。

---

## 5. 図と色の見本帳 (A-7 + A-8)

> **2026-09-07: この 5 枠は廃止しました。** A-7「図のタイプ」自体が v2 で廃止され、
> 5_a7_a8_swatch.html は「色と記号の凡例」2 ページに組み替わっています。生成済みの
> `5-1`〜`5-5_thumb_*.png` は未使用のまま残置。以下は経緯の記録です。

### 枠 5-1〜5-5: 5 種類の図タイプ ミニサムネ（廃止）

各サムネは本編エントリのメイン図を模した小さな代表図。

- **5-1 structure**（概念図）: 中心ノードと周辺ノードを矢印で結ぶ
- **5-2 timeline**（時系列）: 横線に 4 つのドット
- **5-3 comparison**（対比）: 2 つの箱を並べる
- **5-4 before_after**（前後）: BEFORE / AFTER ラベル付きの 2 枠
- **5-5 workflow**（手順）: 矢印で繋がった 3〜4 ステップ

HTML 内に純 CSS のラフ実装あり。最終版は本編から実物の代表図を抽出してくる方が説得力が出る。

- **プロンプト案（共通）**:
  ```
  Minimal abstract diagram thumbnail, 110x110px, navy ink (#123E82) on
  white background, pale blue (#EAF1FB) accent areas. Geometric shapes
  only (circles, rectangles, arrows). No text. Technical book editorial
  style.
  ```

---

## 6. 更新履歴と略称 (A-10 + A-11)

イラスト枠なし。HTML の現状（CSS タイムライン + 表）で完成度高い。

---

## 7. あとがき (back)

### 枠 7-1: 大判の「著者と AI の共著」イラスト

- **場所**: 左ページ中央〜下段（まえがきの「ことばの橋」と対の構図）
- **描く内容**: 机を挟んで著者（抽象人物・左）と AI のシルエット（右）が向かい合う。著者は口元に手を当てて口述、AI は半透明の人型シルエットで同時に書いている
- **構図**: まえがきの橋イラストと対称。橋ではなく机、向かい合うのは人と AI
- **プロンプト案**:
  ```
  Abstract conceptual line drawing, one simplified human figure on the
  left speaking with hand near mouth, facing a translucent humanoid
  silhouette on the right (representing AI) with a glowing edge.
  A simple desk between them with an open notebook. Navy ink (#123E82)
  on white. Pale blue accent (#EAF1FB) for the AI silhouette glow.
  No gender, no profession indicators. Generous whitespace. Horizontal
  landscape composition. Pair with the "bridge" illustration from the
  preface — same style, complementary composition (closing the book).
  ```

---

## まとめ TODO

1. **本気イラスト 6 枠**（最優先）
   - 0-1, 0-2, 0-3（扉 3 コマ）
   - 0-4（見開きミニチュア）
   - 1-1（まえがき・ことばの橋）
   - 7-1（あとがき・AI 共著）

2. **ミニサムネ 5 枠**（中優先・既存 CSS でしのげる）
   - 5-1〜5-5（5 図タイプ）

3. **下地スクショ 1 枠**（低優先・実物撮影で代替可）
   - 2-1（A-2 分解図の下地）

4. **CSS のままで OK 2 枠**
   - 3-1（章地図、すでにグリッドで実装）
   - 6 系（タイムライン・表、純 CSS で完成）

## 本編：スコープ地図バッチ（2026-09-02 追加・5 枚まとめて発注）

「〜エンジニアリング」5 兄弟を **同じ幾何の入れ子図**で描き分けるため、この 5 枚は **必ず 1 バッチでまとめて**発注します。層の数・順序・ラベル位置が 1 枚でもずれると比較図として機能しません。仕様の正は [docs/scope_map_figure_spec.md](../docs/scope_map_figure_spec.md)、各エントリの `## 誌面ポンチ絵メモ` に個別指示があります。

- [ ] **J-106 ハーネスエンジニアリング** — スコープ地図そのものがメイン図（全層を大きく描く／新規）
- [ ] **J-103 ループエンジニアリング** — 既存のタイムライン構図＋左下隅にミニ図（新規）
- [ ] **J-118 グラフエンジニアリング** — 直線ループ vs 分岐グラフの 2 コマ＋左下隅にミニ図（新規）
- [ ] **G-10 プロンプトエンジニアリング** — 既存 `assets/ponchi/final/G-10.webp` を、ミニ図の描き込みのため**再生成**（構図は現行踏襲）
- [ ] **G-11 コンテキストエンジニアリング** — 既存 `assets/ponchi/final/G-11.webp` を同上で**再生成**

合格条件: G-10 と G-11 を並べたときに「同じ地図で、光る輪が 1 つ増えている」と読めること。

## 著者からの確認待ち

- [ ] 「基本全部書いて OK か」← 草案コミット後の方針確認
- [ ] 抽象人物のスタイル（性別/職種を出さない方針で OK か、もう少し具体的にした方が良いか）
- [ ] 画像生成エンジン選定（Midjourney / SD / Imagen / Flux など）
- [ ] 色のトーン（現状の濃紺 #123E82 ＋薄青 #EAF1FB で OK か、もう少し暖色を入れるか）

## 履歴

- 2026-05-24: 初版。前付け 7 spread + 巻末あとがき 1 spread の全画像枠を集約
- 2026-09-02: 本編「スコープ地図バッチ」5 枚を追加（docs/scope_map_figure_spec.md）
- 2026-09-07: 未反映だった 2 枠（0-4 見開きミニチュア / 3-1 章ルート地図）を HTML に差し込み。5-1〜5-5 は枠ごと廃止に整理
