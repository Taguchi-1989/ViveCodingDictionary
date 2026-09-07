#!/usr/bin/env python3
"""Generate drafts/index.html — a top management page linking to every HTML
preview/mockup/cover/tool under drafts/. Re-run after adding new HTML files.

Cloudflare Pages build output directory: `drafts`
"""
from __future__ import annotations

import html
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "drafts"
OUT = DRAFTS / "index.html"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)


def read_title(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return path.stem
    m = TITLE_RE.search(text)
    if not m:
        return path.stem
    title = re.sub(r"\s+", " ", m.group(1)).strip()
    for suffix in (
        " — バイブコーディング図鑑 preview",
        " — バイブコーディング図鑑",
        " - バイブコーディング図鑑 preview",
        "バイブコーディング図鑑 — ",
        "バイブコーディング図鑑 ",
    ):
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()
        if title.startswith(suffix):
            title = title[len(suffix) :].strip()
    return title or path.stem


def collect() -> list[tuple[Path, str]]:
    items = []
    for p in DRAFTS.rglob("*.html"):
        if p == OUT:
            continue
        items.append((p, read_title(p)))
    items.sort(key=lambda x: str(x[0]).lower())
    return items


SECTIONS = [
    ("本を読む（リーダー・前付け・あとがき）", "book/"),
    ("本を読む（リーダー・前付け・あとがき）", "front_section/"),
    ("本を読む（リーダー・前付け・あとがき）", "back_section/"),
    ("探す（検索・読者ルート）", "search/"),
    ("探す（検索・読者ルート）", "reading_routes/"),
    ("エントリプレビュー (A〜J)", "prototypes/preview/"),
    ("表紙・裏表紙", "covers/"),
    ("オープニング見開き", "opening/"),
    ("誌面モック / Design Philosophy v2", "prototypes/mockups/design_philosophy_v2/"),
    ("誌面モック / A・B・C 案", "prototypes/mockups/"),
    ("ツール", "tools/"),
]


def section_of(rel: str) -> str:
    for label, prefix in SECTIONS:
        if rel.startswith(prefix):
            return label
    return "その他"


def letter_of(rel: str) -> str | None:
    if not rel.startswith("prototypes/preview/"):
        return None
    name = rel.split("/")[-1]
    if name in ("index.html", "overview.html"):
        return "目次・一覧"
    if len(name) >= 1 and name[0].isalpha():
        return name[0].upper()
    return "その他"


def build_html(items: list[tuple[Path, str]]) -> str:
    groups: dict[str, dict[str, list[tuple[str, str]]]] = {}
    for path, title in items:
        rel = path.relative_to(DRAFTS).as_posix()
        sec = section_of(rel)
        sub = letter_of(rel) or ""
        groups.setdefault(sec, {}).setdefault(sub, []).append((rel, title))

    parts: list[str] = []
    parts.append("""<!doctype html>
<html lang=\"ja\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>バイブコーディング図鑑 — 管理トップ</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, \"Hiragino Sans\", \"Yu Gothic UI\", system-ui, sans-serif; margin: 0; background: #f3f6fb; color: #1a2333; }
  header { background: #0c2552; color: #fff; padding: 18px 24px; position: sticky; top: 0; z-index: 5; }
  header h1 { margin: 0; font-size: 1.05rem; font-weight: 800; }
  header .sub { font-size: 0.78rem; opacity: 0.8; margin-top: 2px; }
  main { max-width: 1100px; margin: 0 auto; padding: 24px; }
  h2 { font-size: 1rem; color: #0c2552; border-left: 5px solid #2a5db0; padding: 4px 10px; margin: 28px 0 10px; }
  h3 { font-size: 0.85rem; color: #2a5db0; margin: 14px 0 6px; }
  ul.grid { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 4px 12px; }
  ul.grid li { font-size: 0.82rem; line-height: 1.5; }
  ul.grid a { color: #1a3a6c; text-decoration: none; padding: 3px 6px; border-radius: 4px; display: flex; align-items: baseline; gap: 6px; }
  ul.grid a .label { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  ul.grid a:hover { background: #e6eef9; }
  .code { flex: 0 0 auto; min-width: 3.4em; color: #2a5db0; font-weight: 700; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.78rem; }
  .hero { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin: 4px 0 20px; }
  .hero-card { display: flex; flex-direction: column; gap: 4px; background: #fff; border: 1px solid #d4dded; border-radius: 10px; padding: 14px 16px; text-decoration: none; color: #1a2333; }
  .hero-card:hover { border-color: #2a5db0; box-shadow: 0 2px 8px rgba(12,37,82,0.08); }
  .hero-card .step { font-size: 0.72rem; font-weight: 800; color: #2a5db0; letter-spacing: 0.1em; }
  .hero-card strong { font-size: 0.95rem; color: #0c2552; }
  .hero-card .desc { font-size: 0.75rem; color: #6c7a91; line-height: 1.5; }
  .filter { margin: 8px 0 18px; }
  .filter input { width: 100%; padding: 8px 12px; border: 1px solid #d4dded; border-radius: 6px; font-size: 0.9rem; }
  footer { color: #6c7a91; font-size: 0.75rem; padding: 24px; text-align: center; }
  footer a { color: #2a5db0; }
</style>
</head>
<body>
<header>
  <h1>バイブコーディング図鑑 — 管理トップ</h1>
  <div class=\"sub\">作りかけ含め、全 HTML ページにリンクで飛べる目次です。最終更新: __UPDATED__</div>
</header>
<main>
  <div class=\"hero\">
    <a class=\"hero-card\" href=\"/front_section/0_concept_spread.html\"><span class=\"step\">1</span><strong>扉から読み始める</strong><span class=\"desc\">前付け 7 見開き（A 群）。上部ナビで順にめくれます</span></a>
    <a class=\"hero-card\" href=\"/book/index.html\"><span class=\"step\">2</span><strong>本編を読む（B〜J）</strong><span class=\"desc\">もくじ付きリーダーで全エントリを本のように</span></a>
    <a class=\"hero-card\" href=\"/back_section/afterword.html\"><span class=\"step\">3</span><strong>あとがき</strong><span class=\"desc\">この本ができるまで</span></a>
    <a class=\"hero-card\" href=\"/back_section/bk3_model_snapshot.html\"><span class=\"step\">4</span><strong>巻末付録 BK-3</strong><span class=\"desc\">モデル勢力図スナップショット（2024Q1–2026Q3）</span></a>
    <a class=\"hero-card\" href=\"/search/index.html\"><span class=\"step\">🔍</span><strong>検索</strong><span class=\"desc\">用語名・本文からエントリを探す</span></a>
  </div>
  <div class=\"filter\"><input id=\"q\" type=\"search\" placeholder=\"絞り込み（ID やタイトルで検索）...\" autofocus></div>
""")

    seen_labels: set[str] = set()
    for sec_label, _ in SECTIONS:
        if sec_label in seen_labels:
            continue
        seen_labels.add(sec_label)
        if sec_label not in groups:
            continue
        parts.append(f"  <h2>{html.escape(sec_label)}</h2>\n")
        subs = groups[sec_label]
        sub_keys = sorted(subs.keys(), key=lambda k: (k == "目次・一覧" and "0" or k))
        for sub in sub_keys:
            entries = subs[sub]

            def sort_key(e: tuple[str, str]):
                name = e[0].split("/")[-1].removesuffix(".html")
                m = re.match(r"^([A-Z])-(\d+)$", name)
                if m:
                    return (m.group(1), int(m.group(2)))
                return ("~", 0, name)

            entries.sort(key=sort_key)
            if sub:
                parts.append(f"    <h3>{html.escape(sub)}</h3>\n")
            parts.append('    <ul class="grid">\n')

            def code_of(rel: str) -> str:
                name = rel.split("/")[-1].removesuffix(".html")
                return name if re.match(r"^[A-Z]-\d+$", name) else ""

            # ID を持つ行が 1 つでもあるグループでは、持たない行にも空のバッジ枠を
            # 置いて桁を揃える。全行が ID なしのグループ（前付け・検索など）では
            # 余白が無駄になるので枠ごと省く。
            has_code = any(code_of(rel) for rel, _ in entries)
            for rel, title in entries:
                name = rel.split("/")[-1].removesuffix(".html")
                code = code_of(rel)
                parts.append(
                    f'      <li data-search="{html.escape((name + " " + title).lower())}">'
                )
                parts.append(f'<a href="/{html.escape(rel)}">')
                if has_code:
                    parts.append(f'<span class="code">{html.escape(code)}</span>')
                parts.append(
                    f'<span class="label">{html.escape(title)}</span></a></li>\n'
                )
            parts.append("    </ul>\n")

    parts.append("""</main>
<footer>
  Repo: <a href=\"https://github.com/Taguchi-1989/VibeCodingDictionary\">Taguchi-1989/VibeCodingDictionary</a>
  ／ 再生成: <code>python3 scripts/generate_site_index.py</code>
</footer>
<script>
  const q = document.getElementById('q');
  const items = document.querySelectorAll('li[data-search]');
  q.addEventListener('input', () => {
    const v = q.value.trim().toLowerCase();
    items.forEach(li => {
      li.style.display = !v || li.dataset.search.includes(v) ? '' : 'none';
    });
  });
</script>
</body>
</html>
""")
    return "".join(parts)


def main() -> None:
    items = collect()
    stamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    html_out = build_html(items).replace("__UPDATED__", html.escape(stamp))
    OUT.write_text(html_out, encoding="utf-8")
    print(f"wrote {OUT} ({len(items)} pages, updated {stamp})")


if __name__ == "__main__":
    main()
