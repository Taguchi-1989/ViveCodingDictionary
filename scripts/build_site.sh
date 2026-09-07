#!/usr/bin/env bash
# Cloudflare Pages build script.
# Output directory must be set to `drafts` in Pages config.
set -euo pipefail

echo "==> generating preview HTML"
python3 scripts/preview_gen.py

echo "==> copying referenced assets into drafts/"
mkdir -p drafts/assets/ponchi/final
mkdir -p drafts/assets/covers
mkdir -p drafts/assets/opening
mkdir -p drafts/assets/figures

# Ponchi: webp only (png originals are too heavy and only used by overview thumbnails)
cp assets/ponchi/final/*.webp drafts/assets/ponchi/final/ 2>/dev/null || true

# Front-section generated art。中間データ（*_raw*, contact sheet）は出さない。
# render_* は page_count_plan.html がレンダー見本として参照するので必要（数十 KB）
mkdir -p drafts/assets/front_section/generated
for f in assets/front_section/generated/*.png; do
  case "$(basename "$f")" in
    *contact_sheet*|*_raw*) ;;
    *) cp "$f" drafts/assets/front_section/generated/ ;;
  esac
done

# v2 レイアウト凍結仕様のモックアップが参照する実験ポンチ絵
mkdir -p drafts/assets/ponchi/experiments
cp assets/ponchi/experiments/F-2-typescript-wide-v21.png drafts/assets/ponchi/experiments/ 2>/dev/null || true

# Other small asset folders (concept images, opening spread, figure prompts)
cp -r assets/covers/.   drafts/assets/covers/   2>/dev/null || true
cp -r assets/opening/.  drafts/assets/opening/  2>/dev/null || true
cp -r assets/figures/.  drafts/assets/figures/  2>/dev/null || true

echo "==> generating site index"
python3 scripts/generate_site_index.py

echo "==> done"
du -sh drafts/assets 2>/dev/null || true
