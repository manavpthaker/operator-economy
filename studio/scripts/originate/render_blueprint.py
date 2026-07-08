"""
render_blueprint.py — content/blueprint.md → the designed Operator Blueprint PDF.

The blueprint PDF is what email signups actually receive; it must match the
Claude-Design reference (Operator Blueprint №001, Rev A) — Working Schematic
direction, Rev C tokens. Colors/fonts are derived from design-system/tokens/
(_source_of_truth: colors.css, fonts.css — Boska/Zodiak/Supreme via Fontshare,
Fragment Mono via Google Fonts).

Usage (from studio/):
    python scripts/originate/render_blueprint.py originate/<slug>/script.json
    ... [--number 002] [--rev A] [--difficulty Med]
    ... [--hero "$5.9B → $2K" --hero-caption "..."]

Reads  originate/<slug>/content/blueprint.md   (stable H2 sections from derive_content.py)
Writes originate/<slug>/blueprint.html
       originate/<slug>/Operator-Blueprint-<NNN>.pdf
       ../site/public/blueprints/<slug>.pdf     (if site/public exists)

PDF engine: Chrome headless if found (mac path or PATH), else WeasyPrint.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

STUDIO = Path(__file__).parent.parent.parent
SITE_BLUEPRINTS = STUDIO.parent / "site" / "public" / "blueprints"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


# ---------------------------------------------------------------- md parsing

def _inline(s: str) -> str:
    s = html.escape(s.strip())
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for ln in lines:
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def parse_blueprint(md: str) -> dict:
    d: dict = {"sections": {}}
    m = re.search(r"^#\s+(.+)$", md, re.M)
    title = m.group(1) if m else "Operator Blueprint"
    tm = re.match(r"Operator Blueprint #?(\d+)\s*[—–-]\s*(.+)", title)
    d["number"] = tm.group(1).zfill(3) if tm else "000"
    d["title"] = tm.group(2) if tm else title
    lead = re.search(r"^\*(.+?)\*\s*$", md, re.M)
    d["lead"] = _inline(lead.group(1)) if lead else ""

    parts = re.split(r"^##\s+", md, flags=re.M)[1:]
    for p in parts:
        name, _, body = p.partition("\n")
        d["sections"][name.strip().lower().rstrip(")").split(" (")[0]] = \
            (name.strip(), body.strip())
    return d


# ---------------------------------------------------------------- rendering

def conf_chip(text: str) -> str:
    t = re.sub(r"\*", "", text).strip()
    up = t.upper()
    if up.startswith("HIGH"):
        return '<span class="chip chip-high">● HIGH</span>'
    tag = "REPORTED" if "REPORTED" in up else ("MEDIUM" if "MEDIUM" in up else up[:12])
    note = re.sub(r"^(REPORTED|MEDIUM)[,\s—–-]*", "", t, flags=re.I).strip()
    extra = f'<div class="chip-note">{html.escape(note.lower())}</div>' if note else ""
    return f'<span class="chip chip-box">{tag}</span>{extra}'


def render_evidence(body: str) -> str:
    rows = parse_table(body.splitlines())
    if not rows:
        return f"<p>{_inline(body)}</p>"
    out = ['<table><thead><tr>' + "".join(
        f"<th>{html.escape(h.upper())}</th>" for h in rows[0]) + "</tr></thead><tbody>"]
    for r in rows[1:]:
        r += [""] * (4 - len(r))
        scale = re.sub(r"\((.+?)\)", r'<div class="sub">\1</div>', _inline(r[0]))
        out.append(f"<tr><td class='k'>{scale}</td><td class='mono'>{_inline(r[1])}</td>"
                   f"<td class='src'>{_inline(r[2])}</td><td>{conf_chip(r[3])}</td></tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_stack(body: str) -> tuple[str, str]:
    """Returns (table html, cover rail html)."""
    rows = parse_table(body.splitlines())
    table = ['<table><thead><tr>' + "".join(
        f"<th>{html.escape(h.upper())}</th>" for h in rows[0]) + "</tr></thead><tbody>"]
    rail = []
    for r in rows[1:]:
        r += [""] * (4 - len(r))
        table.append(f"<tr><td class='k'>{_inline(r[0])}</td><td>{_inline(r[1])}</td>"
                     f"<td class='mono nowrap'>{_inline(r[2])}</td><td class='src'>{_inline(r[3])}</td></tr>")
        label = re.split(r"[-\s]", r[0])[0].upper()  # "Client-facing" → "CLIENT"
        rail.append(f'<div class="node"><div class="node-l">{html.escape(label)}'
                    f'</div><div class="node-v">{html.escape(re.sub(r"[*]", "", r[2]).upper())}</div></div>')
    table.append("</tbody></table>")
    return "".join(table), "".join(rail)


def render_playbook(body: str) -> list[str]:
    items = re.findall(r"^\d+\.\s+(.+?)(?=^\d+\.|\Z)", body, re.M | re.S)
    out = []
    for i, it in enumerate(items, 1):
        it = " ".join(it.split())
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", it)
        head, rest = (m.group(1), m.group(2)) if m else (it, "")
        hm = re.match(r"(?:(Week[s]?\s*[\d–\-]+)\s*[—–-]\s*)?(.+)", head, re.I)
        label, htext = (hm.group(1) or ""), hm.group(2)
        htext = htext[:1].upper() + htext[1:]
        out.append(
            f'<div class="step"><div class="step-n">{i:02d}</div>'
            f'<div class="step-l">{html.escape(label.upper())}</div>'
            f'<div class="step-b"><h4>{_inline(htext.rstrip("."))}</h4>'
            f'<p>{_inline(rest)}</p></div></div>')
    return out


def render_math(body: str) -> str:
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    big = ""
    # prefer the year-one range (e.g. $2–8K/mo) over incidental $/mo figures
    bm = re.search(r"(\$[\d.]+\s*[–\-]\s*[\d.]+K/mo)", body) or \
         re.search(r"[Yy]ear one:?\s*\*{0,2}(\$[^\s*]+/mo)", body)
    if bm:
        big = (f'<div class="bignum-row"><span class="bignum">{html.escape(bm.group(1))}</span>'
               f'<span class="chip chip-box">OUR ESTIMATE</span></div>')
    out = [big]
    for p in paras:
        if p.lower().startswith("**failure modes"):
            body_f = re.sub(r"\*\*Failure modes:\*\*", "", p, flags=re.I)
            # split the trailing standalone rule (e.g. "Stay SMB — ...") off the last mode
            tail = ""
            tm2 = re.search(r"(?<=[.;])\s+(Stay [A-Z].+|[A-Z][^.]*kill[^.]*\.)\s*$", body_f)
            if tm2:
                tail, body_f = tm2.group(1).strip(), body_f[: tm2.start()]
            modes = [x.strip(" ;.") for x in re.split(r"\(\d\)", body_f) if x.strip(" ;.")]
            items = "".join(
                f'<div class="fm"><span class="fm-x">×{i}</span>'
                f"{_inline(m[:1].upper() + m[1:])}.</div>"
                for i, m in enumerate(modes, 1))
            out.append(f'<div class="fm-label">FAILURE MODES</div>{items}')
            if tail:
                out.append(f'<p style="margin-top:.18in"><strong>{_inline(tail)}</strong></p>')
        else:
            out.append(f"<p>{_inline(p)}</p>")
    return "".join(out)


def render_sources(body: str) -> str:
    body = re.split(r"\n-{3,}", body)[0]  # drop the trailing footer block
    parts = [s.strip() for s in re.split(r"\s+·\s+", body.replace("\n", " ")) if s.strip()]
    return "".join(f'<div class="srcline"><span class="mono">[{i:02d}]</span> {_inline(s.rstrip("."))}</div>'
                   for i, s in enumerate(parts, 1))


CSS = """
/* Derived from design-system/tokens (Rev C). _source_of_truth: colors.css, fonts.css */
@import url('https://api.fontshare.com/v2/css?f[]=boska@700&f[]=zodiak@700&f[]=supreme@400,500,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Fragment+Mono&display=swap');
:root{--ink:#1A1A1A;--ink-700:#3C3A36;--ink-500:#6B675E;--paper:#F5F0E6;--paper-0:#FBF8F1;
--paper-200:#EDE7D8;--rule:#D8CFB9;--rule-strong:#C4B99E;--blue:#1F3A5F;--gold:#7A5E24;
--gold-500:#B08D3E;--sage:#5E7F6A;
--disp:'Boska',Georgia,serif;--head:'Zodiak',Georgia,serif;
--sans:'Supreme',system-ui,sans-serif;--mono:'Fragment Mono',Menlo,monospace}
@page{size:letter;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--paper);color:var(--ink-700);font:14px/1.65 var(--sans);
-webkit-print-color-adjust:exact;print-color-adjust:exact}
/* Deliberate pagination: every .sheet is one designed page (like the Rev A reference). */
.sheet{padding:0.85in 0.95in 1.2in;page-break-after:always;position:relative;
height:11in;overflow:hidden;display:flex;flex-direction:column}
.sheet:last-child{page-break-after:auto}
.foot{position:fixed;bottom:0;left:0;right:0;display:flex;justify-content:space-between;
padding:0.26in 0.95in;border-top:1px solid var(--gold-500);
font:8px/1 var(--mono);letter-spacing:.16em;color:var(--ink-500);background:var(--paper)}
/* ---- cover ---- */
.mast{display:flex;align-items:flex-start;justify-content:space-between}
.mast .the{font:8px/1 var(--mono);letter-spacing:.32em;color:var(--ink-500);margin-bottom:4px}
.mast .name{font:700 23px/1.1 var(--head);color:var(--ink)}
.badge{border:1px solid var(--gold-500);color:var(--gold);
font:9px/1 var(--mono);letter-spacing:.2em;padding:8px 14px;margin-top:4px}
h1{font:700 49px/1.06 var(--disp);color:var(--ink);margin:.6in 0 .2in;letter-spacing:.005em}
.lead{font-size:15.5px;line-height:1.7;max-width:5.2in;color:var(--ink-700)}
.rail{display:flex;align-items:stretch;gap:10px;margin:.48in 0 .1in}
.node{border:1px solid var(--blue);background:var(--paper-0);padding:10px 13px;min-width:.9in}
.node.out{border-color:var(--gold-500)}
.node-l{font:8px/1 var(--mono);letter-spacing:.16em;color:var(--blue);margin-bottom:6px}
.node.out .node-l{color:var(--gold)}
.nowrap{white-space:nowrap}
.node-v{font:12.5px/1 var(--mono);color:var(--ink)}
.rail-cap{border-left:2px solid var(--gold-500);border-bottom:2px solid var(--gold-500);
border-right:2px solid var(--gold-500);height:8px;margin:0 0 7px}
.rail-lbl{text-align:center;font:8px/1 var(--mono);letter-spacing:.22em;color:var(--gold)}
.meta{display:grid;grid-template-columns:1fr 1fr 1fr;border:1.5px solid var(--ink);margin-top:.42in}
.meta div{padding:14px 18px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.meta div:nth-child(3n){border-right:none}.meta div:nth-last-child(-n+3){border-bottom:none}
.meta .l{font:8px/1 var(--mono);letter-spacing:.18em;color:var(--ink-500);display:block;margin-bottom:8px}
.meta .v{font:15px/1 var(--mono);color:var(--ink)}
/* ---- sections ---- */
.sec{margin-top:.5in}
.sec.first{margin-top:0}
.sec.ruled{border-top:2px solid var(--ink);padding-top:.26in}
.sec-h{display:flex;align-items:baseline;gap:15px;margin-bottom:.24in}
.sec-h .n{font:10px/1 var(--mono);color:var(--gold)}
.sec-h h2{font:700 29px/1.1 var(--head);color:var(--ink)}
.sec-h .tag{margin-left:auto;font:9px/1 var(--mono);letter-spacing:.16em;color:var(--gold)}
/* ---- tables ---- */
table{width:100%;border-collapse:collapse;border:1px solid var(--rule-strong);font-size:12.5px}
thead th{background:var(--paper-200);font:600 8.5px/1 var(--mono);letter-spacing:.16em;
color:var(--ink-500);text-align:left;padding:11px 14px}
td{padding:13px 14px;border-top:1px solid var(--rule);vertical-align:top;line-height:1.55}
td.k{font-weight:700;color:var(--ink);width:1.2in}td.k .sub{font-weight:400;font-size:11px;color:var(--ink-500);margin-top:2px}
td.mono{font:12px/1.6 var(--mono);color:var(--ink)}td.src{color:var(--ink-500);font-size:12px}
.chip{font:9px/1 var(--mono);letter-spacing:.1em;white-space:nowrap}
.chip-high{color:var(--sage)}
.chip-box{border:1px solid var(--rule-strong);padding:4px 8px;color:var(--ink-700);background:var(--paper-0)}
.chip-note{font:9px/1.5 var(--mono);color:var(--ink-500);margin-top:7px;max-width:1in}
/* ---- evidence hero ---- */
.hero{font:700 50px/1 var(--mono);color:var(--ink);margin:.22in 0 .14in;letter-spacing:-.01em}
.hero .gold{color:var(--gold-500)}
.hero-cap{max-width:4.8in;color:var(--ink-500);font-size:13px;line-height:1.6;margin-bottom:14px}
.srcflag{display:inline-block;background:var(--paper-200);border-left:3px solid var(--blue);
font:9px/1 var(--mono);letter-spacing:.14em;color:var(--blue);padding:8px 12px;margin:2px 0 .26in}
/* ---- playbook ---- */
.step{display:grid;grid-template-columns:.6in 1.05in 1fr;gap:14px;padding:.21in 0;
border-bottom:1px solid var(--rule)}
.step:last-child{border-bottom:none}
.step-n{font:700 22px/1 var(--mono);color:var(--blue)}
.step-l{font:8px/1.5 var(--mono);letter-spacing:.16em;color:var(--ink-500);padding-top:7px}
.step-b h4{font:700 18px/1.25 var(--head);color:var(--ink);margin-bottom:6px}
.step-b p{font-size:13.5px;margin:0}
.cont{font:8px/1 var(--mono);letter-spacing:.18em;color:var(--ink-500);
border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:4px}
/* ---- honest math ---- */
.bignum{font:700 48px/1 var(--mono);color:var(--ink);margin:.2in 0 .06in;
display:inline-block;border-bottom:4px dotted var(--gold-500);padding-bottom:10px}
.bignum-row{display:flex;align-items:center;gap:14px}
.bignum-row .chip{margin-top:.14in}
.fm-label{font:8px/1 var(--mono);letter-spacing:.18em;color:var(--ink-500);margin:.26in 0 4px}
.fm{padding:8px 0;font-size:13.5px;border-bottom:1px solid var(--paper-200)}
.fm:last-of-type{border-bottom:none}
.fm-x{font:11px/1 var(--mono);color:#9B3E2E;margin-right:11px}
/* ---- sources + colophon ---- */
.srcline{font:12px/2.3 var(--mono);color:var(--ink-700)}.srcline .mono{color:var(--gold);margin-right:8px}
.colophon{margin-top:auto;border-top:1.5px solid var(--ink);padding-top:.35in}
.colophon p{max-width:4.9in;font-size:14px;line-height:1.7}
.boo-row{display:flex;align-items:baseline;justify-content:space-between;margin-top:.3in;max-width:6.2in}
.boo{font:700 26px/1 var(--head);color:var(--ink)}
.site{font:11px/1 var(--mono);color:var(--gold)}
p{margin-bottom:.15in}
"""

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="foot"><span>THE OPERATOR ECONOMY · OPERATOR BLUEPRINT №{num}</span>
<span>REV {rev} · {date}</span></div>

<!-- p1 · cover + the idea -->
<div class="sheet">
  <div class="mast"><div><div class="the">THE</div><div class="name">Operator Economy</div></div>
    <span class="badge">OPERATOR BLUEPRINT №{num}</span></div>
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
  <div class="rail">{rail}</div><div class="rail-cap"></div>
  <div class="rail-lbl">THE STACK · {budget}</div>
  <div class="meta">
    <div><span class="l">BLUEPRINT</span><span class="v">№{num}</span></div>
    <div><span class="l">REV</span><span class="v">{rev}</span></div>
    <div><span class="l">DATE</span><span class="v">{date}</span></div>
    <div><span class="l">SOURCES</span><span class="v">{nsources:02d}</span></div>
    <div><span class="l">DIFFICULTY</span><span class="v">{difficulty}</span></div>
    <div><span class="l">SECTIONS</span><span class="v">{nsections:02d}</span></div>
  </div>
  <div class="sec ruled"><div class="sec-h"><span class="n">01</span><h2>The idea</h2></div>{idea}</div>
</div>

<!-- p2 · evidence -->
<div class="sheet">
  <div class="sec first"><div class="sec-h"><span class="n">02</span><h2>The evidence</h2></div>
    {hero}{evidence}</div>
</div>

<!-- p3 · stack + playbook 01–03 -->
<div class="sheet">
  <div class="sec first"><div class="sec-h"><span class="n">03</span><h2>The stack</h2>
    <span class="tag">{budget} TOTAL</span></div>
    {stack}<div class="srcflag">SOURCE: PUBLIC VENDOR LIST PRICING · {pricing_date}</div></div>
  <div class="sec ruled"><div class="sec-h"><span class="n">04</span><h2>The playbook</h2></div>{playbook_a}</div>
</div>

<!-- p4 · playbook 04–05 + honest math -->
<div class="sheet">
  <div class="sec first"><div class="cont">04 · THE PLAYBOOK — CONTINUED</div>{playbook_b}</div>
  <div class="sec ruled"><div class="sec-h"><span class="n">05</span><h2>The honest math</h2></div>{math}</div>
</div>

<!-- p5 · sources + colophon -->
<div class="sheet">
  <div class="sec first"><div class="sec-h"><span class="n">06</span><h2>Sources</h2></div>{sources}</div>
  <div class="colophon"><p>The Operator Economy — evidence-first breakdowns of businesses one
  person can build. No income promises. Receipts. The next blueprint ships in the Monday
  newsletter.</p>
  <div class="boo-row"><span class="boo">Build. Own. Operate.</span>
  <span class="site">theoperatoreconomy.com</span></div></div>
</div>
</body></html>"""


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    return None


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome = find_chrome()
    if chrome:
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([chrome, "--headless=new", "--disable-gpu",
                                f"--user-data-dir={tmp}", "--no-pdf-header-footer",
                                f"--print-to-pdf={pdf_path}", "--virtual-time-budget=8000",
                                html_path.as_uri()],
                               capture_output=True, text=True, timeout=120)
        if pdf_path.exists():
            return
        print(f"chrome failed ({r.returncode}): {r.stderr[-300:]}", file=sys.stderr)
    try:
        from weasyprint import HTML  # fallback
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    except ImportError:
        sys.exit("No Chrome found and weasyprint not installed. "
                 "brew install --cask google-chrome, or pip install weasyprint.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script_json")
    ap.add_argument("--number", help="blueprint number (default: parsed from blueprint.md)")
    ap.add_argument("--rev", default="A")
    ap.add_argument("--difficulty", default="Med")
    ap.add_argument("--hero", help='evidence hero, e.g. "$5.9B → $2K"')
    ap.add_argument("--rail-out", help='gold OUT node on the cover rail, e.g. "$2–5K" '
                    "(default: first-project price parsed from the evidence table)")
    ap.add_argument("--hero-caption", default="")
    ap.add_argument("--hero-source", default="")
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args()

    ep_dir = Path(args.script_json).parent
    slug = ep_dir.name
    md = (ep_dir / "content" / "blueprint.md").read_text()
    d = parse_blueprint(md)
    num = args.number or d["number"]

    S = d["sections"]
    idea = "".join(f"<p>{_inline(p)}</p>" for p in
                   S.get("the idea", ("", ""))[1].split("\n\n") if p.strip())
    evidence = render_evidence(S.get("the evidence", ("", ""))[1])
    stack_name, stack_body = S.get("the stack", ("The stack", ""))
    bm = re.search(r"[<≤]\s*\$?\d+/mo", stack_name + " " + stack_body)
    budget = ("≤ " + bm.group(0).lstrip("<≤ ")) if bm else "≤ $100/MO"
    budget = budget.upper()
    stack_tbl, rail = render_stack(stack_body)
    ev_body = S.get("the evidence", ("", ""))[1]
    out_val = args.rail_out or next(
        iter(re.findall(r"(\$[\d]+[–\-][\d]+K) first project", ev_body)), None)
    if out_val:
        rail += (f'<div class="node out"><div class="node-l">OUT</div>'
                 f'<div class="node-v">{html.escape(out_val.upper())}</div></div>')
    steps = render_playbook(S.get("the playbook", ("", ""))[1])
    split = 3 if len(steps) > 3 else len(steps)  # p3 gets 01–03, p4 the rest
    playbook_a, playbook_b = "".join(steps[:split]), "".join(steps[split:])
    math_html = render_math(S.get("the honest math", ("", ""))[1])
    sources_html = render_sources(S.get("sources", ("", ""))[1])
    nsources = len(re.findall(r'class="srcline"', sources_html))

    hero = ""
    if args.hero:
        left, _, right = args.hero.partition("→")
        hero = (f'<div class="hero">{html.escape(left.strip())} '
                f'<span class="gold">→ {html.escape(right.strip())}</span></div>'
                f'<p class="hero-cap">{html.escape(args.hero_caption)}</p>')
        if args.hero_source:
            hero += f'<div class="srcflag">SOURCE: {html.escape(args.hero_source.upper())}</div>'

    today = date.today()
    out_html = PAGE.format(
        css=CSS, num=num, rev=args.rev, date=today.isoformat(),
        title=html.escape(d["title"]), lead=d["lead"], rail=rail, budget=budget,
        nsources=nsources or 6, difficulty=args.difficulty, nsections=6,
        idea=idea, hero=hero, evidence=evidence, stack=stack_tbl,
        pricing_date=today.strftime("%b %Y").upper(),
        playbook_a=playbook_a, playbook_b=playbook_b,
        math=math_html, sources=sources_html)

    html_path = ep_dir / "blueprint.html"
    html_path.write_text(out_html)
    print(f"html → {html_path}")
    if args.html_only:
        return

    pdf_path = ep_dir / f"Operator-Blueprint-{num}.pdf"
    html_to_pdf(html_path, pdf_path)
    print(f"pdf  → {pdf_path}")

    # LinkedIn sampler: first 4 pages (cover, evidence, playbook 01–03,
    # then whatever page 4 is) — the excerpt IS the ad for the email gate
    # (publishing-flow "sampler play"). Full blueprint never posts publicly.
    sampler = ep_dir / f"Operator-Blueprint-{num}-sampler.pdf"
    try:
        subprocess.run(["qpdf", str(pdf_path), "--pages", str(pdf_path), "1-4", "--",
                        str(sampler)], check=True, capture_output=True, timeout=60)
        print(f"sampler → {sampler} (4 pages, for the LinkedIn document post)")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠ sampler skipped (qpdf: {e}) — cut pages 1-4 manually if needed",
              file=sys.stderr)
    if SITE_BLUEPRINTS.parent.exists():
        SITE_BLUEPRINTS.mkdir(exist_ok=True)
        shutil.copy(pdf_path, SITE_BLUEPRINTS / f"{slug}.pdf")
        print(f"site → {SITE_BLUEPRINTS / (slug + '.pdf')}")


if __name__ == "__main__":
    main()
