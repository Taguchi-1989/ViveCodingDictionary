# 著者記入欄キュー（author fill queue）

*自動生成: 2026-09-07 11:14 / `scripts/update_author_fill_queue.py`。手で編集しないでください。*

「非エンジニアのつまずき」「私のコメント」は**著者本人しか書けない欄**です。AI は空スケルトンを置くだけで、中身には触りません。

## 内訳

- **完了**（つまずき 1 件以上 ＋ コメント 4 ラベル全部）: 452 件
- **途中**（書きかけで止まっている）: 0 件
- **手つかず**（両方まるごと空）: 6 件
- **合計**: 458 件

---

## ✍️ 途中（あと少しで終わる。ここから手を付けるのが早い）（0 件）

_なし_

---

## ⬜ 手つかず（両方まるごと空）（6 件）

letter 別: H 6件

| ID | title | status | reader_level | path |
| :-- | :-- | :-- | :-- | :-- |
| H-57 | Gemini の命名史 | needs_review | 2-3 | `content/entries/history/H-57_gemini_naming_history[人書].md` |
| H-60 | Codex → GitHub Copilot の系譜 | needs_review | 2-3 | `content/entries/history/H-60_codex_to_copilot[人書].md` |
| H-61 | Preview 版という文化 | needs_review | 2 | `content/entries/history/H-61_preview_culture[人書].md` |
| H-62 | Anthropic 創業の流れ | needs_review | 2-3 | `content/entries/history/H-62_anthropic_founding[人書].md` |
| H-63 | Vibe Coding 命名 | needs_review | 1-2 | `content/entries/history/H-63_vibe_coding_naming[人書].md` |
| H-64 | DeepSeek ショック | needs_review | 2-3 | `content/entries/history/H-64_deepseek_shock[人書].md` |

---

## 使い方

1. 上の「途中」から埋める。第一印象だけ書いて止まっているものが多く、残りの 1〜3 欄を足すだけで完了になります
2. スマホからは RepoEdit で `user-input` ブロックを直接編集できます（[docs/mobile_repoedit_setup.md](../docs/mobile_repoedit_setup.md)）
3. 書き終えたら `status: needs_review → ready` を**手で**上げてください。自動昇格は既定で無効です（CLAUDE.md の運用に合わせています）。一括で上げたいときは `VCD_AUTOPROMOTE_READY=1 python3 scripts/update_review_queue.py`

字数の目安は [docs/entry_schema.yaml](../docs/entry_schema.yaml) を参照してください（つまずき: 1 項目 15〜60 字 / コメント: 1 項目 10〜45 字）。
