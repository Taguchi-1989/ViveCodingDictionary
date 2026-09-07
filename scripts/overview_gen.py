#!/usr/bin/env python3
"""全エントリ「ざっと見る」用一覧 HTML 生成

出力: drafts/prototypes/preview/overview.html

各エントリを 1 行で表示し、章・ステータス・密度で絞り込み／ソートできるシングルページ。
本文セクション合計、TS 基準比、HTML preview と PDF preview へのリンクを並べる。

Usage:
    python scripts/overview_gen.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from density_audit import (
    TARGETS, TS_BASELINE, AUTHOR_BULLET_TARGET, TSUMAZUKI_TOTAL_TARGET, COMMENT_LABELS,
    layout_of, parse, section_chars, status_of, tagline_chars,
    tsumazuki_bullets, comment_items,
)

ENTRIES = REPO / 'content' / 'entries'
PONCHI_DIR = REPO / 'drafts' / 'ponchi'
PONCHI_FINAL_DIR = REPO / 'assets' / 'ponchi' / 'final'
OUT = REPO / 'drafts' / 'prototypes' / 'preview' / 'overview.html'

CHAPTERS = {
    'A': 'はじめに・読み方',
    'B': 'サービス',
    'C': '人・会社',
    'D': 'モデル',
    'E': 'ベンチマーク',
    'F': 'ツール',
    'G': 'AI 用語（言語モデル系）',
    'H': '歴史・開発手法',
    'I': 'MCP',
    'J': '一般用語',
}


def section_cell_class(n: int, target: dict) -> str:
    if n == 0:
        return 'na'
    if n > target['max']:
        return 'over'
    if n > target['rec_max']:
        return 'near'
    if n < target['min']:
        return 'under'
    return 'ok'


def author_cell_class(n: int) -> str:
    if n > AUTHOR_BULLET_TARGET['max']:
        return 'over'
    if n > AUTHOR_BULLET_TARGET['rec_max']:
        return 'near'
    return 'ok'


def tsumazuki_total_class(n: int) -> str:
    if n > TSUMAZUKI_TOTAL_TARGET['max']:
        return 'over'
    if n > TSUMAZUKI_TOTAL_TARGET['rec_max']:
        return 'near'
    return 'ok'


def ponchi_final_ext(entry_id: str) -> str | None:
    """final ディレクトリで .webp を優先し、無ければ .png を返す。見つからなければ None。"""
    for ext in ('webp', 'png'):
        if (PONCHI_FINAL_DIR / f'{entry_id}.{ext}').exists():
            return ext
    return None


def collect():
    rows = []
    ponchi_ids = {p.stem for p in PONCHI_DIR.glob('*.svg')}
    ponchi_final_ids = {
        p.stem for p in PONCHI_FINAL_DIR.iterdir()
        if p.suffix.lower() in ('.webp', '.png')
    }
    for f in sorted(ENTRIES.rglob('*.md')):
        text = f.read_text(encoding='utf-8')
        fm, body = parse(text)
        st = status_of(fm)
        layout = layout_of(fm)
        if st == 'archived':
            continue
        em = re.match(r'([A-J]-\d+)', f.stem)
        if not em:
            continue
        eid = em.group(1)

        # extract title from YAML
        tm = re.search(r'^title:\s*[\"\']?(.+?)[\"\']?\s*$', fm, re.M)
        title = tm.group(1).strip() if tm else eid

        # category
        cm = re.search(r'^category:\s*(\S+)', fm, re.M)
        category = cm.group(1).strip() if cm else ''

        # tag from filename
        tag_m = re.search(r'\[(.+?)\]', f.stem)
        tag = tag_m.group(1) if tag_m else ''

        # density per section
        if layout.startswith('front_'):
            total = -1
            sections = {}
            tsu = []
            com = {label: '' for label in COMMENT_LABELS}
        else:
            sections = {}
            for sname in TARGETS:
                if sname == 'tagline':
                    sections[sname] = tagline_chars(fm, body)
                else:
                    sections[sname] = section_chars(body, sname)
            total = sum(sections.values())
            tsu = tsumazuki_bullets(body)
            com = comment_items(body)

        rows.append({
            'id': eid,
            'letter': eid[0],
            'num': int(eid.split('-')[1]),
            'title': title,
            'status': st,
            'layout': layout,
            'category': category,
            'tag': tag,
            'total': total,
            'sections': sections,
            'tsumazuki': tsu,
            'comment': com,
            'has_ponchi': eid in ponchi_final_ids or eid in ponchi_ids,
            'has_ponchi_final': eid in ponchi_final_ids,
        })
    rows.sort(key=lambda r: (r['letter'], r['num']))
    return rows


def gen_html(rows):
    by_letter = defaultdict(list)
    for r in rows:
        by_letter[r['letter']].append(r)

    # Stats per chapter
    chapter_stats = {}
    for letter, items in by_letter.items():
        valid = [it for it in items if it['total'] >= 0]
        chapter_stats[letter] = {
            'count': len(items),
            'ready': sum(1 for it in items if it['status'] == 'ready'),
            'needs_review': sum(1 for it in items if it['status'] == 'needs_review'),
            'avg_density': sum(it['total'] for it in valid) // len(valid) if valid else 0,
        }

    # JSON for client filter
    data_json = json.dumps(rows, ensure_ascii=False)

    parts = []
    P = parts.append
    P('<!DOCTYPE html>')
    P('<html lang="ja"><head><meta charset="UTF-8">')
    P('<meta name="viewport" content="width=device-width, initial-scale=1">')
    P('<title>バイブコーディング図鑑 — 全エントリ一覧</title>')
    P('<style>')
    P('* { box-sizing: border-box; }')
    P('body { margin:0; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic UI","Meiryo",sans-serif; color:#1a2333; background:#f3f6fb; }')
    P('header { background:#fff; border-bottom:1px solid #d8e0eb; padding:18px 24px; position:sticky; top:0; z-index:10; box-shadow:0 1px 0 rgba(0,0,0,0.03); }')
    P('h1 { font-size:20px; margin:0 0 4px; color:#0c2552; font-weight:900; }')
    P('.subtitle { font-size:12px; color:#6c7a91; }')
    P('.toolbar { display:flex; gap:8px; flex-wrap:wrap; margin-top:12px; align-items:center; }')
    P('.btn { background:#eef3fb; color:#27406b; border:1px solid #d4dded; padding:5px 11px; border-radius:6px; cursor:pointer; font-size:12px; font-weight:600; }')
    P('.btn:hover { background:#dde6f5; }')
    P('.btn.on { background:#27406b; color:#fff; border-color:#27406b; }')
    P('select { padding:5px 9px; border-radius:6px; border:1px solid #d4dded; font-size:12px; background:#fff; }')
    P('main { padding:18px 24px 60px; max-width:1400px; margin:0 auto; }')
    P('.chapter { margin:24px 0 12px; padding:6px 12px; background:#0c2552; color:#fff; border-radius:6px; font-weight:700; font-size:14px; display:flex; gap:16px; align-items:baseline; }')
    P('.chapter .stat { font-size:11px; opacity:0.7; font-weight:400; }')
    P('table { width:100%; border-collapse:collapse; background:#fff; border:1px solid #d8e0eb; border-radius:6px; overflow:hidden; }')
    P('th,td { padding:4px 5px; border-bottom:1px solid #eef0f4; font-size:11px; vertical-align:middle; white-space:nowrap; }')
    P('th { background:#fafbfd; text-align:left; font-weight:700; color:#27406b; font-size:10px; letter-spacing:0.02em; }')
    P('th .tcap { display:block; font-size:9px; opacity:0.6; font-weight:400; }')
    P('table.dense td.num { text-align:right; font-variant-numeric:tabular-nums; min-width:32px; }')
    P('td.num.over { background:#ffe2e0; color:#8b1d1d; font-weight:700; }')
    P('td.num.near { background:#fff4d6; color:#7a5500; }')
    P('td.num.under { background:#eef0f4; color:#6c7a91; }')
    P('td.num.ok { color:#1a2333; }')
    P('td.num.na { color:#aab2c0; }')
    P('td.num.total { font-weight:700; }')
    P('td.ponchi { text-align:center; font-size:14px; padding:2px 4px; }')
    P('td.ponchi.has { color:#1a6b1a; }')
    P('td.ponchi.pending { color:#aab2c0; }')
    P('.ponchi-thumb { display:inline-block; position:relative; }')
    P('.ponchi-thumb img { width:52px; height:52px; object-fit:contain; display:block; border:1px solid #d8e0eb; border-radius:3px; background:#fff; transition:transform .15s ease, box-shadow .15s ease; }')
    P('.ponchi-thumb img:hover { transform:scale(4.5); transform-origin:right center; z-index:200; position:relative; box-shadow:0 6px 24px rgba(0,0,0,0.35); border-color:#27406b; }')
    P('.ponchi-thumb.svg-only { font-size:18px; line-height:52px; width:52px; height:52px; color:#1a6b1a; border:1px dashed #b8c8db; border-radius:3px; background:#f8fbff; }')
    P('tr:last-child td { border-bottom:none; }')
    P('tr:hover td { background:#fcfdff; }')
    P('.id { font-family:"SFMono-Regular","Consolas",monospace; font-size:12px; font-weight:700; color:#0c2552; width:50px; }')
    P('.title { font-weight:600; color:#1a2333; min-width:180px; }')
    P('.tag { font-size:10px; padding:2px 6px; border-radius:3px; font-weight:600; display:inline-block; }')
    P('.tag.sumi { background:#dbeefd; color:#0c2552; }')        # 済
    P('.tag.hito { background:#fff0d4; color:#7a4f00; }')         # 人書
    P('.tag.ai_sei { background:#e3e6ec; color:#3a4254; }')       # AI整
    P('.tag.ai_choku { background:#e9e9e9; color:#444; }')         # AI直
    P('.tag.tou { background:#f0d0d0; color:#7a1818; }')           # 凍')
    P('.status { font-size:10px; color:#6c7a91; }')
    P('.density { text-align:right; font-variant-numeric:tabular-nums; font-size:12px; }')
    P('.density.high { color:#9a2727; font-weight:700; }')
    P('.density.mid { color:#3a4254; }')
    P('.density.low { color:#1a6b1a; }')
    P('.density.na { color:#aab2c0; }')
    P('.links { white-space:nowrap; }')
    P('.links a { color:#27406b; text-decoration:none; font-size:11px; padding:2px 6px; border-radius:3px; background:#eef3fb; margin-right:3px; border:1px solid #d4dded; font-weight:600; }')
    P('.links a:hover { background:#27406b; color:#fff; }')
    P('.hidden { display:none !important; }')
    P('.legend { font-size:11px; color:#6c7a91; margin-top:6px; }')
    P('.legend code { background:#eef3fb; padding:1px 4px; border-radius:3px; font-size:10px; }')
    P('</style></head><body>')

    P('<header>')
    P('<h1>バイブコーディング図鑑 — 全エントリざっと見</h1>')
    total_count = len(rows)
    total_ready = sum(1 for r in rows if r['status'] == 'ready')
    total_nr = sum(1 for r in rows if r['status'] == 'needs_review')
    valid_dens = [r['total'] for r in rows if r['total'] >= 0]
    median_d = sorted(valid_dens)[len(valid_dens) // 2] if valid_dens else 0
    ponchi_count = sum(1 for r in rows if r['has_ponchi'])
    ponchi_final_count = sum(1 for r in rows if r.get('has_ponchi_final'))
    P(f'<div class="subtitle">全 {total_count} 件 / ready {total_ready} / needs_review {total_nr} / ポンチ絵あり {ponchi_final_count} 件・画像生成待ち {total_count - ponchi_final_count} 件 / 本文密度中央値 {median_d} 字（TS 基準 {TS_BASELINE} 字 比 {median_d*100//TS_BASELINE}%）</div>')
    P('<div class="toolbar">')
    P('<span style="font-size:12px;font-weight:600;">章フィルタ:</span>')
    P('<button class="btn on" data-filter="all" onclick="filterChapter(this)">すべて</button>')
    for letter in sorted(by_letter):
        P(f'<button class="btn" data-filter="{letter}" onclick="filterChapter(this)">{letter} {CHAPTERS.get(letter,"")} ({len(by_letter[letter])})</button>')
    P('<span style="margin-left:24px;font-size:12px;font-weight:600;">状態:</span>')
    P('<button class="btn on" data-status="all" onclick="filterStatus(this)">すべて</button>')
    P('<button class="btn" data-status="ready" onclick="filterStatus(this)">ready</button>')
    P('<button class="btn" data-status="needs_review" onclick="filterStatus(this)">needs_review</button>')
    P('<button class="btn" data-status="hito" onclick="filterStatus(this)">[人書] 残</button>')
    P('<span style="margin-left:24px;font-size:12px;font-weight:600;">ポンチ絵:</span>')
    P('<button class="btn on" data-ponchi="all" onclick="filterPonchi(this)">すべて</button>')
    P('<button class="btn" data-ponchi="has" onclick="filterPonchi(this)">あり</button>')
    P('<button class="btn" data-ponchi="pending" onclick="filterPonchi(this)">画像生成待ち</button>')
    P('</div>')
    P('<div class="legend">密度色 — <span class="density high">赤</span> TS基準 +30% 超 / <span class="density mid">通常</span> +10〜30% / <span class="density low">緑</span> TS±10% 内</div>')
    P('</header>')

    P('<main>')
    for letter in sorted(by_letter):
        items = by_letter[letter]
        stat = chapter_stats[letter]
        P(f'<div class="chapter" data-chapter="{letter}">'
          f'<span>{letter}章 — {CHAPTERS.get(letter, "")}</span>'
          f'<span class="stat">{stat["count"]} 件 / ready {stat["ready"]} / needs_review {stat["needs_review"]} / 平均密度 {stat["avg_density"]} 字</span>'
          f'</div>')
        P(f'<table data-chapter="{letter}" class="dense">')
        # Header with all section columns
        sec_short = {
            'tagline': 'タグライン',
            '何をしてくれるか': '何を',
            'どこで出会うか': 'どこで',
            '会話での使い方例': '会話',
            '1. 役割': '1役割',
            '2. うれしさ': '2嬉',
            '3. 注意点': '3注',
            '4. どこで役立つか': '4役立',
            '5. はじめに': '5初',
            '6. 深掘り先': '6深',
        }
        header_cells = ['ID', 'タイトル', 'タグ', 'st']
        for sname in TARGETS:
            t = TARGETS[sname]
            header_cells.append(f'{sec_short[sname]}<span class="tcap">≤{t["max"]}</span>')
        header_cells.extend([
            '計', 'TS比',
            f'つま計<span class="tcap">≤{TSUMAZUKI_TOTAL_TARGET["max"]}</span>',
            '印象', '良', 'ダ', '誰',
            'ポンチ', 'preview',
        ])
        P('<thead><tr>')
        for h in header_cells:
            P(f'<th>{h}</th>')
        P('</tr></thead>')
        P('<tbody>')

        for r in items:
            tag_cls_map = {'済': 'sumi', '人書': 'hito', 'AI整': 'ai_sei', 'AI直': 'ai_choku', '凍': 'tou'}
            tag_cls = tag_cls_map.get(r['tag'], 'ai_choku')
            tag_label = r['tag'] if r['tag'] else '—'

            if r['total'] < 0:
                density_class = 'na'
                density_html = '<span class="density na">—</span>'
                ts_html = '—'
            else:
                ratio = r['total'] * 100 // TS_BASELINE
                density_class = 'high' if ratio > 130 else ('low' if ratio <= 110 else 'mid')
                density_html = f'<span class="density {density_class}">{r["total"]}</span>'
                ts_html = f'<span class="density {density_class}">{ratio}%</span>'

            row_cells = []
            row_cells.append(f'<td class="id">{r["id"]}</td>')
            row_cells.append(f'<td class="title">{escape(r["title"])}</td>')
            row_cells.append(f'<td><span class="tag {tag_cls}">{tag_label}</span></td>')
            row_cells.append(f'<td class="status">{r["status"][:2]}</td>')

            for sname in TARGETS:
                t = TARGETS[sname]
                n = r['sections'].get(sname, 0)
                if r['total'] < 0:
                    row_cells.append('<td class="num na">—</td>')
                else:
                    cls = section_cell_class(n, t)
                    row_cells.append(f'<td class="num {cls}">{n}</td>')

            row_cells.append(f'<td class="num total">{density_html}</td>')
            row_cells.append(f'<td class="num">{ts_html}</td>')

            # tsumazuki: total
            tsu_total = sum(len(b) for b in r['tsumazuki'])
            tsu_full = ' / '.join(r['tsumazuki']) if r['tsumazuki'] else ''
            if tsu_total == 0:
                row_cells.append('<td class="num na">—</td>')
            else:
                cls = tsumazuki_total_class(tsu_total)
                row_cells.append(f'<td class="num {cls}" title="{escape(tsu_full)}">{tsu_total}</td>')

            # comment 4 labels
            for label in COMMENT_LABELS:
                v = r['comment'].get(label, '')
                if v:
                    n = len(v)
                    cls = author_cell_class(n)
                    row_cells.append(f'<td class="num {cls}" title="{escape(v)}">{n}</td>')
                else:
                    row_cells.append('<td class="num na">—</td>')

            # ponchi indicator: 画像サムネ（webp 優先）/ SVG marker / pending
            ext = ponchi_final_ext(r['id']) if r.get('has_ponchi_final') else None
            if ext:
                img_src = f'../../../assets/ponchi/final/{r["id"]}.{ext}'
                row_cells.append(
                    f'<td class="ponchi has"><span class="ponchi-thumb">'
                    f'<img src="{img_src}" alt="{escape(r["id"])}" loading="lazy" title="{escape(r["id"])} {escape(r["title"])}"></span></td>'
                )
            elif r['has_ponchi']:
                row_cells.append('<td class="ponchi has"><span class="ponchi-thumb svg-only" title="SVG のみ（画像待ち）">◐</span></td>')
            else:
                row_cells.append('<td class="ponchi pending"><span class="ponchi-thumb svg-only" style="color:#aab2c0;border-style:dotted;" title="画像生成待ち">○</span></td>')

            hto = f'{r["id"]}.html'
            pdf = f'pdf/{r["id"]}.pdf'
            row_cells.append(f'<td class="links"><a href="{hto}" target="_blank">H</a><a href="{pdf}" target="_blank">P</a></td>')
            ponchi_attr = 'has' if r['has_ponchi'] else 'pending'
            P(f'<tr data-status="{r["status"]}" data-tag="{r["tag"]}" data-ponchi="{ponchi_attr}">{"".join(row_cells)}</tr>')
        P('</tbody></table>')
    P('</main>')

    P('<script>')
    P('let curChapter = "all"; let curStatus = "all"; let curPonchi = "all";')
    P('function apply() {')
    P('  document.querySelectorAll(".chapter, table").forEach(el => {')
    P('    const ch = el.dataset.chapter;')
    P('    el.classList.toggle("hidden", curChapter !== "all" && ch !== curChapter);')
    P('  });')
    P('  document.querySelectorAll("tbody tr").forEach(tr => {')
    P('    const st = tr.dataset.status; const tag = tr.dataset.tag; const pn = tr.dataset.ponchi;')
    P('    let show = true;')
    P('    if (curStatus === "ready") show = show && (st === "ready");')
    P('    else if (curStatus === "needs_review") show = show && (st === "needs_review");')
    P('    else if (curStatus === "hito") show = show && (tag === "人書");')
    P('    if (curPonchi !== "all") show = show && (pn === curPonchi);')
    P('    tr.classList.toggle("hidden", !show);')
    P('  });')
    P('}')
    P('function filterChapter(btn) {')
    P('  document.querySelectorAll("[data-filter]").forEach(b => b.classList.remove("on"));')
    P('  btn.classList.add("on"); curChapter = btn.dataset.filter; apply();')
    P('}')
    P('function filterStatus(btn) {')
    P('  document.querySelectorAll("[data-status]").forEach(b => b.classList.remove("on"));')
    P('  btn.classList.add("on"); curStatus = btn.dataset.status; apply();')
    P('}')
    P('function filterPonchi(btn) {')
    P('  document.querySelectorAll("[data-ponchi]").forEach(b => b.classList.remove("on"));')
    P('  btn.classList.add("on"); curPonchi = btn.dataset.ponchi; apply();')
    P('}')
    P('</script></body></html>')

    return '\n'.join(parts)


def main():
    rows = collect()
    html = gen_html(rows)
    OUT.write_text(html, encoding='utf-8')
    print(f'wrote {OUT} ({len(rows)} entries)', file=sys.stderr)


if __name__ == '__main__':
    main()
