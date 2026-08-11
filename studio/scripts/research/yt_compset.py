#!/usr/bin/env python3
"""
Research: build the comp-set thumbnail dataset and the contact sheet to read it.

Why this exists (2026-08-11). Every thumbnail rule we have was inferred — the
weights in `thumbnail_spec.py` say so in their own comment ("a belief about what
makes someone click, inferred from what YouTube surfaces on a cold feed"), and
the rules in `docs/thumbnail-rubric.md` came from a general-audience creator
checklist that had to be half-overturned by amendments A1-A6 within a month.
Nobody had ever looked at what the comp set actually does, at scale, against
performance. This does that.

Two stages:

  1. dataset     parse saved YouTube channel pulls -> compset.json
  2. contact     emit an HTML contact sheet grouped by channel, banded by
                 within-channel performance, each tile shown BOTH at reading
                 size and at 120px (the shrink-test width `check_thumbnail.py`
                 measures, per rubric amendment A6)

Getting the raw pulls: YouTube is not reachable from the sandbox (egress policy
blocks youtube.com and i.ytimg.com), so the channel pages are fetched through
the Nimble MCP scraper, which saves oversized results to disk:

    nimble_extract(url="https://www.youtube.com/@<handle>/videos",
                   output_format="plain_text", country="US", wait=4000)

Pass `country="US"`: without it a share of requests land on the EU consent
interstitial and return no video data at all. Point --from-pulls at the
directory those .txt files land in.

The contact sheet loads thumbnails from i.ytimg.com, so it must be opened on a
machine with normal internet access. That is the point of emitting a file rather
than analysing pixels here: the sandbox cannot see the images, a human can.

    yt_compset.py --from-pulls <dir> --out research/thumbnails
    yt_compset.py --out research/thumbnails          # rebuild sheet from json
"""

from __future__ import annotations

import argparse
import glob
import html
import json
import os
import re
import statistics as st
import sys
from pathlib import Path

# Lane assignments come from research/comp-synthesis.md, not from this script.
LANES = {
    "ModernMBA":           ("Modern MBA",        "register benchmark"),
    "HowMoneyWorks":       ("How Money Works",   "register benchmark"),
    "MagnatesMedia":       ("MagnatesMedia",     "documentary craft"),
    "Wendoverproductions": ("Wendover",          "documentary craft"),
    "Companyman":          ("Company Man",       "documentary craft"),
    "StarterStory":        ("Starter Story",     "direct comp"),
    "UpFlip":              ("UpFlip",            "direct comp"),
    "CodieSanchez":        ("Codie Sanchez",     "direct comp"),
    "GregIsenberg":        ("Greg Isenberg",     "AI-idea lane"),
    "GrowthinReverse":     ("Growth in Reverse", "design reference"),
}

MIN_AGE = 21   # days. Below this, early view velocity has not settled.


# ── parsing YouTube's embedded data ─────────────────────────────────────────
def carve(content: str, marker: str = "ytInitialData = "):
    """Pull the ytInitialData object out of a page by brace-matching."""
    i = content.find(marker)
    if i < 0:
        return None
    s = content[i + len(marker):]
    depth = 0; instr = False; esc = False
    for n, ch in enumerate(s):
        if esc: esc = False; continue
        if ch == "\\": esc = True; continue
        if ch == '"': instr = not instr; continue
        if instr: continue
        if ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(s[:n + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _views(s):
    if not s or "view" not in s:
        return None
    m = re.match(r"([\d.,]+)\s*([KMB]?)", s.replace(",", ""))
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2)]) if m else None


def _age_days(s):
    m = re.match(r"(\d+)\s+(second|minute|hour|day|week|month|year)", s or "")
    if not m:
        return None
    return int(m.group(1)) * {"second": 0, "minute": 0, "hour": 0,
                              "day": 1, "week": 7, "month": 30, "year": 365}[m.group(2)]


def videos(data) -> list[dict]:
    """Walk ytInitialData for video tiles.

    Modern YouTube renders each tile as `lockupViewModel`; the older
    `videoRenderer` shape is gone from the channel grid, so parsers written
    against it silently return nothing.
    """
    out = []
    def walk(o):
        if isinstance(o, dict):
            if "lockupViewModel" in o:
                lv = o["lockupViewModel"]
                md = lv.get("metadata", {}).get("lockupMetadataViewModel", {})
                rows = (md.get("metadata", {}).get("contentMetadataViewModel", {})
                          .get("metadataRows", []))
                parts = [p.get("text", {}).get("content")
                         for r in rows for p in r.get("metadataParts", [])]
                v = {"id": lv.get("contentId"), "title": md.get("title", {}).get("content")}
                for p in parts:
                    if p and "view" in p:
                        v["views"] = _views(p)
                    elif p and "ago" in p:
                        v["age_days"], v["age"] = _age_days(p), p
                if v["id"] and v.get("title"):
                    out.append(v)
            for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(data)
    seen, uniq = set(), []
    for v in out:
        if v["id"] not in seen:
            seen.add(v["id"]); uniq.append(v)
    return uniq


def build_dataset(pull_dir: Path) -> list[dict]:
    best: dict[str, list] = {}
    for f in sorted(glob.glob(str(pull_dir / "*.txt"))):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        m = re.search(r"youtube\.com/@([^/]+)/videos", d.get("url", ""))
        if not m:
            continue
        data = carve(d.get("content", ""))
        if not data:
            continue                      # consent interstitial or a 404 shell
        vs = [v for v in videos(data) if v.get("views")]
        if len(vs) > len(best.get(m.group(1), [])):
            best[m.group(1)] = vs

    rows = []
    for h, vs in sorted(best.items()):
        name, lane = LANES.get(h, (h, "unclassified"))
        for v in vs:
            rows.append({
                "channel": name, "handle": h, "lane": lane,
                "video_id": v["id"], "title": v["title"], "views": v["views"],
                "age_days": max(v.get("age_days") or 1, 1), "age": v.get("age"),
                "thumb": f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg",
                "url": f"https://www.youtube.com/watch?v={v['id']}",
            })
    return band(rows)


def band(rows: list[dict]) -> list[dict]:
    """Label each video top/mid/bottom against its OWN channel's median.

    Within-channel only: cross-channel view comparison is meaningless when
    subscriber bases differ by orders of magnitude. Raw views rather than
    views/day, because early velocity far exceeds the long-run average and the
    channels differ wildly in cadence — views/day would just rank by recency.
    """
    for h in {r["handle"] for r in rows}:
        g = sorted([r for r in rows if r["handle"] == h and r["age_days"] >= MIN_AGE],
                   key=lambda r: -r["views"])
        if len(g) < 8:
            for r in g: r["band"] = "unranked"
            continue
        med = st.median([r["views"] for r in g]) or 1
        k = max(len(g) // 4, 2)
        for i, r in enumerate(g):
            r["band"] = "top" if i < k else "bottom" if i >= len(g) - k else "mid"
            r["index"] = round(r["views"] / med, 2)
        for r in rows:
            if r["handle"] == h and "band" not in r:
                r["band"] = "too-new"
    return rows


# ── the contact sheet ───────────────────────────────────────────────────────
def sheet(rows: list[dict], exclude: set[str]) -> str:
    rows = [r for r in rows if r["handle"] not in exclude]
    secs = []
    for h in sorted({r["handle"] for r in rows},
                    key=lambda h: [r["lane"] for r in rows if r["handle"] == h][0]):
        g = [r for r in rows if r["handle"] == h]
        ch, lane = g[0]["channel"], g[0]["lane"]
        blocks = []
        for bandname, label in (("top", "TOP QUARTILE"), ("bottom", "BOTTOM QUARTILE")):
            items = sorted([r for r in g if r.get("band") == bandname],
                           key=lambda r: -r["views"])
            if not items:
                continue
            tiles = "".join(f"""
      <figure>
        <a href="{html.escape(r['url'])}" target="_blank" rel="noopener">
          <img class="big" src="{html.escape(r['thumb'])}" loading="lazy"
               onerror="this.src='https://i.ytimg.com/vi/{r['video_id']}/hqdefault.jpg'">
        </a>
        <div class="shrink">
          <img class="tiny" src="{html.escape(r['thumb'])}" loading="lazy"
               onerror="this.src='https://i.ytimg.com/vi/{r['video_id']}/hqdefault.jpg'">
          <span class="shrinklab">120px</span>
        </div>
        <figcaption>
          <b>{r['views']:,}</b> views &middot; {html.escape(r.get('age') or '')}
          &middot; <span class="idx">{r.get('index', '')}x median</span>
          <span class="t">{html.escape(r['title'])}</span>
        </figcaption>
      </figure>""" for r in items)
            blocks.append(f'<h3 class="band {bandname}">{label}</h3>'
                          f'<div class="grid">{tiles}</div>')
        secs.append(f"""<section>
  <div class="chead"><h2>{html.escape(ch)}</h2><code>{html.escape(lane)}</code></div>
  {''.join(blocks)}
</section>""")
    return PAGE.replace("{{BODY}}", "\n".join(secs)).replace(
        "{{N}}", str(len(rows))).replace(
        "{{CH}}", str(len({r["handle"] for r in rows})))


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Comp-set thumbnails — top vs bottom quartile</title>
<style>
:root{--ink:#12263F;--ink2:#41546B;--ink3:#7A889A;--ground:#F7F4EC;--panel:#fff;
 --line:#DED6C4;--gold:#9A7B2E;--win:#2E6B4F;--lose:#8C3A2B;
 --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
 --ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
 --ink:#ECE4D4;--ink2:#B3A992;--ink3:#8A8272;--ground:#141A24;--panel:#1B222E;
 --line:#2E3846;--gold:#C8A24F;--win:#6FBF95;--lose:#E0836F}}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--ui);line-height:1.5}
.wrap{max-width:1500px;margin:0 auto;padding:38px 22px 90px}
h1{font-size:28px;margin:0 0 8px;letter-spacing:-.015em}
.sub{color:var(--ink2);max-width:78ch;margin:0 0 6px}
.warn{color:var(--lose);font-size:13.5px;max-width:78ch}
section{margin-top:48px;border-top:2px solid var(--ink);padding-top:12px}
.chead{display:flex;gap:12px;align-items:baseline}
.chead h2{font-size:22px;margin:0}
.chead code{margin-left:auto;font:600 10px/1 var(--mono);letter-spacing:.12em;
 text-transform:uppercase;color:var(--gold);border:1px solid var(--line);padding:5px 8px}
.band{font:700 11px/1 var(--mono);letter-spacing:.16em;margin:26px 0 12px;
 padding-left:9px;border-left:4px solid}
.band.top{color:var(--win);border-color:var(--win)}
.band.bottom{color:var(--lose);border-color:var(--lose)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:22px}
figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:8px;
 overflow:hidden;display:flex;flex-direction:column}
img.big{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}
.shrink{display:flex;align-items:center;gap:9px;padding:8px 10px;border-top:1px solid var(--line);
 background:linear-gradient(90deg,#fff 50%,#111 50%)}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .shrink{
 background:linear-gradient(90deg,#fff 50%,#000 50%)}}
img.tiny{width:120px;aspect-ratio:16/9;object-fit:cover;display:block}
.shrinklab{font:600 9px/1 var(--mono);letter-spacing:.1em;color:#888;
 background:var(--panel);padding:3px 5px;border-radius:3px}
figcaption{padding:9px 11px 12px;font-size:12px;color:var(--ink3)}
figcaption b{color:var(--ink);font-size:13.5px}
.idx{color:var(--gold);font-family:var(--mono);font-size:11px}
.t{display:block;color:var(--ink2);margin-top:5px;font-size:13px;line-height:1.4}
a{color:inherit}
</style>
<div class="wrap">
<h1>Comp-set thumbnails — top vs bottom quartile</h1>
<p class="sub">{{N}} videos across {{CH}} channels. Bands are <b>within-channel</b>: each video
ranked against its own channel's median views, so subscriber base is controlled. Recent-30 per
channel, so this is what each channel is doing <em>now</em>. Every tile is shown at reading size and
again at 120px — the shrink-test width the rubric standardised on (A6).</p>
<p class="warn">Read down each channel, not across channels. The question is not "which is
prettier" but: what do the top-quartile tiles share that the bottom-quartile tiles of the same
channel do not?</p>
{{BODY}}
</div>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-pulls", type=Path,
                    help="directory of saved Nimble extract .txt files")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--exclude", default="Companyman",
                    help="comma-separated handles to leave out of the sheet")
    a = ap.parse_args()

    a.out.mkdir(parents=True, exist_ok=True)
    ds = a.out / "compset.json"

    if a.from_pulls:
        rows = build_dataset(a.from_pulls)
        ds.write_text(json.dumps(rows, indent=1))
        print(f"dataset → {ds}  ({len(rows)} videos, "
              f"{len({r['handle'] for r in rows})} channels)")
    else:
        if not ds.exists():
            raise SystemExit(f"no {ds}; run once with --from-pulls")
        rows = band(json.loads(ds.read_text()))

    exclude = {h.strip() for h in a.exclude.split(",") if h.strip()}
    out = a.out / "contact-sheet.html"
    out.write_text(sheet(rows, exclude), encoding="utf-8")
    print(f"contact sheet → {out}  ({out.stat().st_size/1024:.0f} KB)")
    print("\nOpen it on a machine with internet access — the tiles load from "
          "i.ytimg.com, which the sandbox cannot reach.")
    for h in sorted({r["handle"] for r in rows}):
        g = [r for r in rows if r["handle"] == h]
        t = [r for r in g if r.get("band") == "top"]
        b = [r for r in g if r.get("band") == "bottom"]
        if t and b:
            print(f"  {g[0]['channel']:<18} n={len(g):<3} top median "
                  f"{st.median([r['views'] for r in t]):>10,.0f}  "
                  f"bottom {st.median([r['views'] for r in b]):>10,.0f}  "
                  f"({st.median([r['views'] for r in t])/max(st.median([r['views'] for r in b]),1):.1f}x)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
