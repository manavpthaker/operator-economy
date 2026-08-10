#!/usr/bin/env python3
"""
Originate: build a YouTube-surface mockup for judging thumbnails in context.

Why this exists (2026-08-10). Thumbnails were being judged as full-size PNGs
opened on their own. That is not where anyone sees them. In the feed they are
roughly 360px wide, sitting next to a title, under a duration chip that covers
the lower-right corner, in a grid of competitors, and in dark mode about as
often as light. A file that looks decisive at 1280px can vanish at 360.

This renders a self-contained HTML harness with four rigs:

  1. browse grid   — the set at real feed size with real metadata
  2. size ladder   — one thumbnail at 360/210/168/120 to find where it dies
  3. before/after  — the current live thumbnail against its replacement
  4. channel page  — the set together, which is the series-consistency read

The emulated YouTube surface has its own light/dark switch, independent of the
viewer's own theme, because that is the whole point: every OE thumbnail is dark
navy and the contrast rule in thumbnail-rubric.md assumes YouTube's white UI.

    build_thumbnail_mockup.py --out mockup.html

Images are downscaled and inlined as data URIs, so the file works offline and
inside a strict CSP. Nothing is fetched at view time.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]      # studio/
REPO = ROOT.parent                              # repo root
THUMB_W = 640                                   # 2x the largest display size


@dataclass
class Item:
    label: str
    title: str
    image: Path
    meta: str = ""
    duration: str = ""
    note: str = ""
    before: Path | None = None
    before_note: str = ""
    flatten: str | None = None   # composite alpha over this colour first
    extra: dict = field(default_factory=dict)


def data_uri(src: Path, flatten: str | None = None) -> str:
    """Downscale to THUMB_W and inline as a JPEG data URI."""
    if not src.exists():
        raise SystemExit(f"missing image: {src}")
    with tempfile.TemporaryDirectory() as td:
        stage = Path(td) / "stage.png"
        if flatten:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
                capture_output=True, text=True, check=True).stdout.strip()
            w, h = probe.split(",")[:2]
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error",
                 "-f", "lavfi", "-i", f"color={flatten}:s={w}x{h}",
                 "-i", str(src), "-filter_complex", "[0][1]overlay",
                 "-frames:v", "1", "-update", "1", str(stage)], check=True)
            src = stage
        out = Path(td) / "out.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(src),
             "-vf", f"scale={THUMB_W}:-2", "-q:v", "4", str(out)], check=True)
        return "data:image/jpeg;base64," + base64.b64encode(out.read_bytes()).decode()


def card(it: Item, uri: str, cls: str = "") -> str:
    dur = (f'<span class="dur">{html.escape(it.duration)}</span>'
           if it.duration else '<span class="dur dur-none" title="position and size accurate; '
                               'value not asserted">&nbsp;&nbsp;&nbsp;</span>')
    meta = f'<div class="meta">{html.escape(it.meta)}</div>' if it.meta else ""
    return f"""<article class="card {cls}">
  <div class="thumb"><img src="{uri}" alt="{html.escape(it.title)}" loading="lazy">{dur}</div>
  <h3 class="vtitle">{html.escape(it.title)}</h3>
  <div class="chan">The Operator Economy</div>
  {meta}
</article>"""


def build(items: list[Item], ladder_of: str) -> str:
    uris = {it.label: data_uri(it.image, it.flatten) for it in items}
    before_uris = {it.label: data_uri(it.before) for it in items if it.before}

    grid = "\n".join(card(it, uris[it.label]) for it in items)

    lad = next(it for it in items if it.label == ladder_of)
    ladder = "\n".join(
        f'<figure class="rung"><img src="{uris[lad.label]}" style="width:{w}px" alt="">'
        f'<figcaption>{w}px<span>{note}</span></figcaption></figure>'
        for w, note in [(360, "desktop grid"), (210, "sidebar"),
                        (168, "mobile feed"), (120, "browse strip")])

    pairs = "\n".join(f"""<div class="pair">
  <div class="pair-head">{html.escape(it.title)}</div>
  <div class="pair-body">
    <figure><div class="thumb sm"><img src="{before_uris[it.label]}" alt=""></div>
      <figcaption><b>live</b> {html.escape(it.before_note)}</figcaption></figure>
    <figure><div class="thumb sm"><img src="{uris[it.label]}" alt=""></div>
      <figcaption><b>proposed</b> {html.escape(it.note)}</figcaption></figure>
  </div>
</div>""" for it in items if it.before)

    chan = "\n".join(card(it, uris[it.label], "compact") for it in items)

    return TEMPLATE.format(grid=grid, ladder=ladder, pairs=pairs, chan=chan,
                           ladder_title=html.escape(lad.title))


TEMPLATE = """<title>OE thumbnails, in situ</title>
<style>
/* ---- harness palette. OE's own tokens, so the tool never gets confused
       with the specimen. Light is the base; both dark paths redefine only
       tokens, never component rules. ---- */
:root {{
  --ink:#12263F; --ink-2:#41546B; --ink-3:#6C7C90;
  --ground:#F7F4EC; --panel:#FFFFFF; --line:#DED6C4;
  --gold:#9A7B2E; --brick:#9B3E2E;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --ui:Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
}}
@media (prefers-color-scheme:dark) {{
  :root:not([data-theme="light"]) {{
    --ink:#ECE4D4; --ink-2:#B3A992; --ink-3:#8A8272;
    --ground:#141A24; --panel:#1B222E; --line:#2E3846;
    --gold:#C8A24F; --brick:#C4614C;
  }}
}}
:root[data-theme="dark"] {{
  --ink:#ECE4D4; --ink-2:#B3A992; --ink-3:#8A8272;
  --ground:#141A24; --panel:#1B222E; --line:#2E3846;
  --gold:#C8A24F; --brick:#C4614C;
}}

/* ---- the emulated YouTube surface. Driven by [data-yt], NOT by the viewer's
       theme, because seeing both is the instrument. Values are YouTube's
       actual chrome colours. ---- */
.yt {{ --yt-bg:#fff; --yt-fg:#0f0f0f; --yt-meta:#606060; }}
.yt[data-yt="dark"] {{ --yt-bg:#0f0f0f; --yt-fg:#f1f1f1; --yt-meta:#aaa; }}

*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:var(--ui);line-height:1.55;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1180px;margin:0 auto;padding:40px 24px 96px}}

header{{border-bottom:2px solid var(--ink);padding-bottom:20px;margin-bottom:8px}}
h1{{font:600 30px/1.15 var(--ui);margin:0 0 6px;letter-spacing:-.015em;text-wrap:balance}}
.sub{{color:var(--ink-2);max-width:64ch;margin:0}}

.rig{{margin-top:52px}}
.rig>h2{{font:600 13px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;
  color:var(--gold);margin:0 0 4px}}
.rig>.q{{font:500 20px/1.3 var(--ui);margin:0 0 6px;letter-spacing:-.01em}}
.rig>.why{{color:var(--ink-2);margin:0 0 20px;max-width:70ch;font-size:15px}}

.bar{{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:10px;
  align-items:center;background:var(--ground);border-bottom:1px solid var(--line);
  padding:12px 0;margin-bottom:4px}}
.bar .lbl{{font:600 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3)}}
button{{font:600 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;
  padding:9px 14px;border:1px solid var(--line);border-radius:2px;
  background:var(--panel);color:var(--ink-2);cursor:pointer}}
button[aria-pressed="true"]{{background:var(--ink);color:var(--ground);border-color:var(--ink)}}
button:focus-visible{{outline:2px solid var(--gold);outline-offset:2px}}

/* ---- emulated surface ---- */
.yt{{background:var(--yt-bg);padding:22px;border:1px solid var(--line);border-radius:2px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px 16px}}
.grid.tight{{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}}
.card{{min-width:0}}
.thumb{{position:relative;aspect-ratio:16/9;border-radius:10px;overflow:hidden;
  background:#000}}
.thumb img{{width:100%;height:100%;object-fit:cover;display:block}}
.dur{{position:absolute;right:6px;bottom:6px;background:rgba(0,0,0,.8);color:#fff;
  font:500 12px/1.2 var(--ui);padding:2px 4px;border-radius:4px;
  font-variant-numeric:tabular-nums}}
.dur-none{{background:rgba(0,0,0,.55)}}
.vtitle{{font:500 14px/1.35 var(--ui);color:var(--yt-fg);margin:9px 0 3px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.chan,.meta{{font:400 12px/1.4 var(--ui);color:var(--yt-meta)}}
.compact .vtitle{{font-size:13px}}

/* ---- size ladder ---- */
.ladder{{display:flex;flex-wrap:wrap;gap:26px;align-items:flex-start}}
.rung{{margin:0}}
.rung img{{display:block;border-radius:6px;height:auto}}
.rung figcaption{{font:600 11px/1.5 var(--mono);letter-spacing:.08em;color:var(--yt-meta);
  margin-top:8px}}
.rung figcaption span{{display:block;font-weight:400;letter-spacing:0;text-transform:none;
  color:var(--yt-meta);opacity:.75}}

/* ---- before/after ---- */
.pair{{border-top:1px solid var(--line);padding:20px 0}}
.pair:first-of-type{{border-top:0}}
.pair-head{{font:500 15px/1.3 var(--ui);margin-bottom:12px}}
.pair-body{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}}
.pair-body figure{{margin:0}}
.thumb.sm{{border-radius:8px}}
.pair-body figcaption{{font:400 12.5px/1.5 var(--ui);color:var(--ink-2);margin-top:8px}}
.pair-body figcaption b{{font:600 11px/1 var(--mono);letter-spacing:.1em;
  text-transform:uppercase;color:var(--gold);display:block;margin-bottom:3px}}

.notes{{margin-top:56px;border-top:2px solid var(--ink);padding-top:22px}}
.notes h2{{font:600 13px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;
  color:var(--gold);margin:0 0 14px}}
.notes ul{{margin:0;padding-left:20px;max-width:74ch}}
.notes li{{margin-bottom:9px;color:var(--ink-2)}}
.notes b{{color:var(--ink)}}
.warn{{border-left:3px solid var(--brick);padding-left:14px;margin-top:18px;max-width:74ch}}
.warn b{{color:var(--brick)}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>

<div class="wrap">
<header>
  <h1>OE thumbnails, in situ</h1>
  <p class="sub">The same files at the size and on the surface where they are actually
  seen. Judged as 1280px PNGs they all look fine; that is not the test.</p>
</header>

<div class="bar">
  <span class="lbl">YouTube surface</span>
  <button id="lt" aria-pressed="true">Light</button>
  <button id="dk" aria-pressed="false">Dark</button>
  <span class="lbl" style="margin-left:auto">Page</span>
  <button id="pt">Flip page theme</button>
</div>

<section class="rig">
  <h2>Rig 01</h2>
  <p class="q">Does it survive the browse grid?</p>
  <p class="why">Real feed width, real titles, duration chip in its true position over the
  lower-right corner. Switch the surface to dark: every one of these is navy, and the
  rubric's contrast rule assumes YouTube's white UI.</p>
  <div class="yt" data-yt="light" id="ytA"><div class="grid">{grid}</div></div>
</section>

<section class="rig">
  <h2>Rig 02</h2>
  <p class="q">Where does it stop reading?</p>
  <p class="why">{ladder_title} at four real display widths. 120px is the browse strip
  that <code>check_thumbnail.py</code> measures.</p>
  <div class="yt" data-yt="light" id="ytB"><div class="ladder">{ladder}</div></div>
</section>

<section class="rig">
  <h2>Rig 03</h2>
  <p class="q">Is the replacement actually better?</p>
  <p class="why">Live thumbnail against its proposed replacement, both at feed size.</p>
  <div class="yt" data-yt="light" id="ytC">{pairs}</div>
</section>

<section class="rig">
  <h2>Rig 04</h2>
  <p class="q">Do they read as one channel?</p>
  <p class="why">The channel-page view. Series consistency is the thing you cannot see
  one file at a time.</p>
  <div class="yt" data-yt="light" id="ytD"><div class="grid tight">{chan}</div></div>
</section>

<div class="notes">
  <h2>Reading this honestly</h2>
  <ul>
    <li><b>View counts are real.</b> EP002 took 288 impressions to 3 views, EP003 took
    160 to 1. Those are the numbers this exercise exists to move.</li>
    <li><b>Duration chips are placeholders</b> except where a real runtime is known. The
    chip's size and position are accurate, which is the part that matters, since it
    occludes the lower-right corner your rubric reserves.</li>
    <li><b>No competitor tiles.</b> A real browse feed interleaves other channels and
    that changes the read considerably. Dropping in screenshots of an actual feed is the
    next step and the one thing this cannot fake.</li>
    <li><b>EP005 is shown flattened on black</b>, which is what YouTube's JPEG conversion
    produces from its 94%-transparent source. It is not what the design intended.</li>
  </ul>
  <div class="warn">
    <b>The thing to look for:</b> flip the surface to dark. A dark-navy thumbnail on a
    <code>#0f0f0f</code> page has no edge, so the tile stops being a tile and the gold
    figure floats on the page itself. That is most of YouTube's audience.
  </div>
</div>
</div>

<script>
(function () {{
  var surfaces = ['ytA','ytB','ytC','ytD'].map(function (i) {{ return document.getElementById(i); }});
  var lt = document.getElementById('lt'), dk = document.getElementById('dk');
  function setYt(mode) {{
    surfaces.forEach(function (s) {{ if (s) s.dataset.yt = mode; }});
    lt.setAttribute('aria-pressed', String(mode === 'light'));
    dk.setAttribute('aria-pressed', String(mode === 'dark'));
  }}
  lt.addEventListener('click', function () {{ setYt('light'); }});
  dk.addEventListener('click', function () {{ setYt('dark'); }});

  document.getElementById('pt').addEventListener('click', function () {{
    var r = document.documentElement;
    var dark = r.getAttribute('data-theme') === 'dark'
      || (!r.getAttribute('data-theme')
          && window.matchMedia('(prefers-color-scheme: dark)').matches);
    r.setAttribute('data-theme', dark ? 'light' : 'dark');
  }});
}})();
</script>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--manifest", type=Path,
                    help="JSON list of items; defaults to the back-catalogue set")
    a = ap.parse_args()

    if a.manifest:
        items = [Item(**{**d, "image": Path(d["image"]),
                         "before": Path(d["before"]) if d.get("before") else None})
                 for d in json.loads(a.manifest.read_text())]
    else:
        o, d = REPO / "studio/originate", REPO / "docs/thumbnail-drafts"
        items = [
            Item("ep001", "The $5.9 Billion Business You Can Start for $100",
                 d / "ai-implementation-consulting.png",
                 meta="82 views · the channel's best", note="$2K PER INSTALL",
                 before=o / "ai-implementation-consulting/thumbnail-ep001.jpg",
                 before_note="9-word serif title card; breaks rules 1, 2, 3, 5, 6"),
            Item("ep002", "The Phone Call Businesses Never Answer",
                 d / "voice-agent-agency.png",
                 meta="3 views · 288 impressions · 0.7% CTR", note="62% GO TO VOICEMAIL",
                 before=o / "voice-agent-agency/thumbnail-ep002.png",
                 before_note="two competing numbers, kicker, OE. mark in the chip corner"),
            Item("ep003", "The 5 Billion Dollar Business That Sounds Boring",
                 d / "boring-automation-agency.png",
                 meta="1 view · 160 impressions · 0.0% CTR", note="$500 EVERY MONTH",
                 before=None,
                 before_note=""),
            Item("ep004", "The Design Agency You Can Run Alone",
                 d / "solo-design-agency.png",
                 meta="live since 2026-08-03", note="typographic challenger, text held constant",
                 before=o / "solo-design-agency/thumbnail-004.png",
                 before_note="already satisfies one-hero-number; the strongest live asset"),
            Item("ep005", "The 400x Problem Nobody Covers",
                 o / "too-small-to-bother/launch/thumbnail.png",
                 meta="scheduled", duration="13:33", flatten="black",
                 note="", before=None),
        ]

    a.out.write_text(build(items, ladder_of="ep003"), encoding="utf-8")
    kb = a.out.stat().st_size / 1024
    print(f"wrote {a.out}  ({kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
