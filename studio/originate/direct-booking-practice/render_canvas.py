"""
render_canvas.py: EP009 locked Operator Canvas -> public "Operator Canvas" print edition (PDF).

Adapted from EP007's renderer, which the owner approved for No. 001. Same structure, same
Boundary Ledger tokens, same headless-Chrome print; only the episode's own constants differ.

Source: operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/operator-canvas.md
(Status: locked, 2026-09-03). The Canvas text is transcribed, not rewritten. This script only:

  * omits the Canvas's internal-only material (header metadata, the pitch-deck and episode
    coverage map, the E3 readiness check, the Canvas lock block);
  * withholds nothing. EP009's "DO NOT STATE" list in content-os/facts.md forbids no figure
    outright: it requires every modeled figure to carry its hedge in the same breath. So the
    hedges are placed on the page with the figures instead (see NOTE_AFTER), which is the
    stronger reading of that rule for a document the reader keeps;
  * adds derivation-authored glue: cover, reading key, source notes with the facts.md hedges,
    disclosures and provenance.

Replaces render_blueprint_bl.py (which rendered the derived worksheet content/blueprint.md, not
the Canvas). Boundary Ledger 2.0 tokens and vendored fonts, printed with headless Chrome.

Usage (from studio/):
    python3 originate/direct-booking-practice/render_canvas.py [--number 002] [--rev A]

Writes originate/direct-booking-practice/canvas.html and Operator-Canvas-<NNN>.pdf.
Does not copy to site/public (see launch/UPLOAD-PLAN.md).
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

# render_blueprint_bl is the shared Boundary Ledger print layer, kept in one place rather than
# copied per episode. It still lives beside No. 001's renderer, where it was written.
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "exit-readiness-prep"))
from render_blueprint_bl import CHROME, REPO, font_face, tokens  # noqa: E402

EP = Path(__file__).resolve().parent
CANVAS = (REPO / "operator-blueprint-v2" / "episodes" / "EP009-direct-booking-recovery"
          / "01-editorial" / "operator-canvas.md")

TITLE_PRE = "Operator Canvas №{num}:"
TITLE_NAME = "a direct-booking practice"
EPISODE_TITLE = "The One-Person Business That Gets Small Hotels Booking Direct"
DISCLOSURE = "Modeled scenario, not observed performance or an earnings forecast."
# site/app/lib/brand.ts AI_DISCLOSURE (owner-approved, verbatim) + facts.md EP009 host authority.
AI_DISCLOSURE = ("Episodes are presented by an AI avatar of the host, with narration in a clone of "
                 "his voice. The research and the arguments are his.")
HOST_NOTE = ("The host spent his first decade in hospitality, including Ace Hotel and Standard "
             "Hotels, and has managed hospitality operations. He has not sold this particular "
             "service. Nothing in this Canvas describes a delivered client engagement, and what a "
             "property will pay for it is untested.")

# Canvas sections that stay internal (not public): omitted whole.
OMIT = {"Pitch-deck and episode coverage map", "E3 readiness check", "Canvas lock"}

# EP009 withholds no figure. Its "DO NOT STATE" list requires each modelled figure to carry its
# hedge in the same breath rather than be removed, which NOTE_AFTER does. Kept as an empty hook so
# a later ruling can withhold something without restructuring the build.
W = '<span class="withheld">[{}]</span>'
WITHHOLD: list[tuple[str, str]] = []

# Hedges from content-os/facts.md EP009, placed on the same page as the figures they qualify.
# EP009's do-not-state list forbids no figure outright; it requires each to carry its hedge in the
# same breath. In a document the reader keeps, that means the hedge sits with the number.
NOTE_AFTER = {
    "3. Costly problem": ("Read the hedges before the numbers",
                          "The share of independent-hotel bookings running through the sites is "
                          "Cloudbeds' own reporting, worldwide, from about ninety million bookings. "
                          "Cloudbeds sells to independents. The European counterweight is HOTREC's "
                          "study, and it is Europe, not the US. Commission bands come from trade "
                          "reporting, not from the sites, which publish no base rate. Treat all of "
                          "them as directional."),
    "10. Economics model": ("Everything here is arithmetic on an invented inn",
                            "The inn is illustrative: it is made up, and every input is one you would replace with "
                            "the owner's own. The mix shift the recoverable amount turns on is a "
                            "hypothesis nobody has measured. The low end of the direct-cost band is "
                            "one vendor's own figure. The recoverable amount is a ceiling your fee "
                            "sits under, not commission this service saves, and not earnings."),
    "11. Risks and failure modes": ("Guest data",
                                    "Guest contact details are used only inside each site's partner "
                                    "terms, the American email law, and European rules for European "
                                    "guests. This is not legal advice. Check your own jurisdiction "
                                    "before you collect anything."),
}

SOURCES = [
    ("CLM-001", "OBSERVED", "Cloudbeds, 2026 State of Independent Hotels (about 90 million bookings)",
     "https://www.globenewswire.com/news-release/2026/03/25/3262232/0/en/",
     "Vendor-published. Cloudbeds sells to independent hotels. Worldwide, not US. Directional."),
    ("CLM-002", "OBSERVED", "HOTREC / HES-SO, European hotel distribution study (3,000+ hotels, 2023)",
     "https://www.hotrec.eu/en/news_digital-trends-in-accommodation-hotels-booking-com-and-dma_C2_A0_C2_A0.html",
     "Europe only. Do not read it as US behaviour; it is the counterweight to CLM-001, not a match."),
    ("CLM-003", "OBSERVED", "Booking Holdings FY2025 10-K, gross bookings",
     "https://www.stocktitan.net/sec-filings/BKNG/10-k-booking-holdings-inc-files-annual-report-7fb6c3d1394a.html",
     "Blended across everything the company sells, not a hotel commission rate. Read via a filing summary."),
    ("CLM-004", "OBSERVED", "Expedia Group FY2025 results, gross bookings",
     "https://ir.expediagroup.com/news-and-events/news/news-details/2026/Expedia-Group-Reports-Fourth-Quarter-and-Full-Year-",
     "Blended, as above. Never add the two companies together."),
    ("CLM-005", "SECONDARY", "Trade reporting on Booking.com commission mechanics",
     "https://kimisuite.com/en/blog/booking-com-commissions-explained",
     "Secondary. Booking.com publishes no base rate. Most European markets, not a US figure."),
    ("CLM-007", "OBSERVED", "HOTREC, collective damages action over parity clauses",
     "https://www.hotrec.eu/en/news_collective-action-against-booking-com-over-15-000-hotels-participating.html",
     "Europe, not here. Registration is not a finding of damages."),
    ("CLM-008", "OBSERVED", "Booking.com Partner Help, contacting your guests",
     "https://partner.booking.com/en-gb/help/reservations/contact-extranet/contacting-your-guests",
     "Primary, the site's own help. The messaging-window durations come from trade press, not the site."),
    ("CLM-009", "OBSERVED", "Google Hotel Center Help, free booking links",
     "https://support.google.com/hotelprices/answer/10472394?hl=en",
     "Primary. Eligibility runs through a Hotel Center account or an integration partner; not every "
     "small property qualifies on its own."),
    ("CLM-010", "PUBLIC PRICING", "Booking-engine pricing (Little Hotelier via Roommaster; Cloudbeds)",
     "https://www.cloudbeds.com/pricing/",
     "Public tool pricing. Secondary for Little Hotelier. Open the vendor page before you quote it."),
    ("CLM-011", "OBSERVED", "Egochi, hotel marketing agency published entry price",
     "https://www.egochi.com/hotel-marketing-agency/",
     "Self-published, for its own price only. It is not evidence that agencies serve the 20 to 40 "
     "room band, and it carries no outcome claim."),
    ("CLM-012", "OBSERVED", "AHLA industry pages and the AHLA / Hireology staffing survey (282 hoteliers)",
     "https://www.ahla.com/news/65-surveyed-hotels-report-staffing-shortages",
     "Association data, member-skewed, not size-specific. AHLA counts small-business properties, "
     "not a room band; nobody has counted the 20 to 40 band."),
    ("CLM-014", "MODELED", "D-EDGE direct distribution cost reporting",
     "https://www.d-edge.com/2025-hotel-direct-distribution-report/",
     "Vendor-reported, and it is the low end of the direct-cost band the model uses. The band is a "
     "modelling assumption, not a measured cost for any property."),
]

LABELS = {"OBSERVED": "obs", "PARALLEL": "par", "MODELED": "mod", "UNKNOWN": "unk",
          "PARALLEL/MODELED": "par",
          # EP009 carries two classes No. 001 did not: trade reporting that is not the source
          # itself, and published tool pricing. Both are weaker than OBSERVED and the reader
          # should see which is which.
          "SECONDARY": "sec", "PUBLIC PRICING": "pub"}


# ------------------------------------------------------------------ markdown -> html

def inline(s: str) -> str:
    keep: list[str] = []

    def stash(m: re.Match) -> str:
        keep.append(m.group(0))
        return f"\x00{len(keep) - 1}\x00"

    s = re.sub(r'<span class="withheld">[^<]*</span>', stash, s.strip())
    s = html.escape(s, quote=False)

    def code(m: re.Match) -> str:
        t = m.group(1)
        if t in LABELS:
            return f'<span class="chip chip-{LABELS[t]}">{t}</span>'
        return f'<span class="verbatim">{t}</span>'

    s = re.sub(r"`([^`]+)`", code, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], s)
    return s


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(lines: list[str]) -> str:
    head = cells(lines[0])
    align = ["num" if c.endswith(":") and not c.startswith(":") else "" for c in cells(lines[1])]
    out = ["<table><thead><tr>"]
    out += [f'<th class="{align[i]}">{inline(h)}</th>' for i, h in enumerate(head)]
    out.append("</tr></thead><tbody>")
    for line in lines[2:]:
        r = cells(line)
        out.append("<tr>" + "".join(
            f'<td class="{align[i] if i < len(align) else ""}">{inline(c)}</td>' for i, c in enumerate(r))
            + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_body(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("### "):
            out.append(f'<h3>{inline(s[4:])}</h3>')
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            while not lines[j].strip().startswith("```"):
                j += 1
            out.append(f'<pre class="calc">{html.escape(chr(10).join(lines[i + 1:j]), quote=False)}</pre>')
            i = j + 1
            continue
        if s.startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(table(lines[i:j]))
            i = j
            continue
        if s.startswith("- "):
            items, j = [], i
            while j < len(lines) and lines[j].strip().startswith("- "):
                items.append(lines[j].strip()[2:])
                j += 1
            out.append('<ul class="bullets">' + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ul>")
            i = j
            continue
        m = re.match(r"(\d+)\. ", s)
        if m:
            items, j = [], i
            while j < len(lines) and re.match(r"\d+\. ", lines[j].strip()):
                items.append(re.sub(r"^\d+\. ", "", lines[j].strip()))
                j += 1
            out.append(f'<ol start="{m.group(1)}">' + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ol>")
            i = j
            continue
        j, buf = i, []
        while j < len(lines) and lines[j].strip() and not re.match(r"\s*(\||```|- |### |\d+\. )", lines[j]):
            buf.append(lines[j].strip())
            j += 1
        text = " ".join(buf)
        if text.startswith("Required public disclosure:"):
            out.append(f'<div class="disclosure"><span>Required public disclosure</span>'
                       f'<strong>{html.escape(DISCLOSURE)}</strong></div>')
        else:
            out.append(f"<p>{inline(text)}</p>")
        i = j
    return "".join(out)


def public_layer(body: str) -> str:
    rows = []
    for line in body.strip().splitlines():
        if not line.strip():
            continue
        k, _, v = line.partition(":")
        rows.append(f"<dt>{html.escape(k.strip())}</dt><dd>{inline(v)}</dd>")
    return f'<dl class="layer">{"".join(rows)}</dl>'


def parse(md: str) -> tuple[str, list[tuple[str, str]]]:
    for old, new in WITHHOLD:
        if old not in md:
            sys.exit(f"locked Canvas text changed; withheld figure not found: {old[:60]}…")
        md = md.replace(old, new)
    parts = re.split(r"^##\s+", md, flags=re.M)
    secs = []
    for p in parts[1:]:
        name, _, body = p.partition("\n")
        secs.append((name.strip(), body))
    return parts[0], secs


CSS = """
@page{size:Letter;margin:.62in .7in .72in;background:#f5f0e6;
  @bottom-left{content:"THE OPERATOR ECONOMY  ·  OPERATOR CANVAS №{num}  ·  REV {rev}";
    font:500 7.5px/1 var(--bl-font-body);letter-spacing:.16em;color:#566461}
  @bottom-right{content:counter(page) " / " counter(pages);
    font:7.5px/1 var(--bl-font-data);letter-spacing:.08em;color:#566461}}
@page:first{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact;background:var(--bl-paper)}
body{background:var(--bl-paper);color:var(--bl-ink-soft);font:400 10pt/1.5 var(--bl-font-body)}
a{color:var(--bl-mineral);text-decoration:none;word-break:break-all}
strong{color:var(--bl-ink);font-weight:500}

.cover{height:11in;padding:.62in .7in .6in;display:flex;flex-direction:column;background:var(--bl-paper);break-after:page}
.mast{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--bl-ink);padding-bottom:10px}
.mast .brand{font:700 15pt/1 var(--bl-font-heading);color:var(--bl-ink)}
.mast .brand small{display:block;font:500 6.5pt/1 var(--bl-font-body);letter-spacing:.3em;color:var(--bl-ink-muted);margin-bottom:5px}
.mast .no{font:7.5pt/1 var(--bl-font-data);letter-spacing:.14em;color:var(--bl-ink-muted);text-align:right}
.kicker{margin-top:.9in;font:500 7.5pt/1 var(--bl-font-body);letter-spacing:.26em;color:var(--bl-steel-dark);text-transform:uppercase}
h1{font:700 40pt/1 var(--bl-font-display);color:var(--bl-ink);margin:.16in 0 .18in;max-width:6.4in;letter-spacing:-.005em}
h1 .pre{display:block;font:700 17pt/1.2 var(--bl-font-heading);color:var(--bl-mineral);margin-bottom:.08in}
.sub{font:400 13pt/1.45 var(--bl-font-body);color:var(--bl-ink-soft);max-width:5.6in}
.docket{margin-top:auto;border:1px solid var(--bl-rule-strong);background:var(--bl-paper-raised)}
.docket .dh{display:flex;justify-content:space-between;background:var(--bl-mineral);color:var(--bl-paper-on-mineral);
  font:500 7pt/1 var(--bl-font-body);letter-spacing:.2em;padding:9px 14px;text-transform:uppercase}
.docket dl{display:grid;grid-template-columns:1.35in 1fr}
.docket dt,.docket dd{padding:8px 14px;border-top:1px solid var(--bl-rule)}
.docket dt{font:500 7pt/1.6 var(--bl-font-body);letter-spacing:.18em;color:var(--bl-ink-muted);text-transform:uppercase}
.docket dd{font-size:9.4pt;color:var(--bl-ink)}
.docket dd.fail{color:var(--bl-oxide-dark);font-weight:500}
.cover .disclosure{margin-top:12px}
.cover .fine{margin-top:10px;font-size:7.8pt;line-height:1.45;color:var(--bl-ink-muted)}
.cover .fine strong{color:var(--bl-ink-soft)}

section{break-before:auto}
section.newpage{break-before:page}
.sh{display:flex;align-items:baseline;gap:14px;border-top:1.5px solid var(--bl-ink);padding-top:9px;margin:.26in 0 .12in;break-after:avoid}
section.newpage > .sh{margin-top:0}
.sh .n{font:8pt/1 var(--bl-font-data);color:var(--bl-steel);letter-spacing:.1em;min-width:.34in}
h2{font:700 18pt/1.1 var(--bl-font-heading);color:var(--bl-ink)}
h3{font:700 10.5pt/1.25 var(--bl-font-heading);color:var(--bl-mineral);margin:.12in 0 .04in;break-after:avoid}
p{margin:0 0 .085in;max-width:6.9in}
ul.bullets{margin:0 0 .1in;list-style:none}
ul.bullets li{position:relative;padding-left:16px;margin-bottom:4px}
ul.bullets li::before{content:"";position:absolute;left:2px;top:.62em;width:7px;height:1px;background:var(--bl-steel)}
ol{margin:0 0 .1in 2em}
ol li{margin-bottom:4px;padding-left:4px}
ol li::marker{font:8.5pt var(--bl-font-data);color:var(--bl-steel-dark)}

table{break-inside:avoid;width:100%;border-collapse:collapse;margin:.06in 0 .14in;font-size:8.4pt;line-height:1.36;background:var(--bl-paper-raised);border:1px solid var(--bl-rule-strong)}
thead{display:table-header-group}
tr{break-inside:avoid}
th{text-align:left;font:500 6.5pt/1.3 var(--bl-font-body);letter-spacing:.12em;text-transform:uppercase;color:var(--bl-paper-on-mineral);
  background:var(--bl-mineral);padding:7px 8px;vertical-align:bottom}
td{padding:6px 8px;border-top:1px solid var(--bl-rule);vertical-align:top}
td+td,th+th{border-left:1px solid var(--bl-rule)}
td:first-child{color:var(--bl-ink);font-weight:500}
td.num,th.num{text-align:right;font-family:var(--bl-font-data)}

.chip{display:inline-block;font:500 6.3pt/1.25 var(--bl-font-body);letter-spacing:.1em;padding:1.5px 5px;border:1px solid;
  vertical-align:1px;white-space:nowrap;background:var(--bl-paper-raised)}
.chip-obs{color:var(--bl-mineral);border-color:var(--bl-mineral)}
.chip-par{color:var(--bl-steel-dark);border-color:var(--bl-steel)}
.chip-mod{color:var(--bl-steel-dark);border-color:var(--bl-steel);border-style:dashed}
.chip-unk{color:var(--bl-oxide-dark);border-color:var(--bl-oxide)}
.chip-sec{color:var(--bl-steel-dark);border-color:var(--bl-steel);border-style:dotted}
.chip-pub{color:var(--bl-mineral);border-color:var(--bl-steel)}
.verbatim{font-weight:500;color:var(--bl-ink)}
.withheld{font:8pt var(--bl-font-data);color:var(--bl-oxide-dark);background:var(--bl-paper-inset);padding:0 3px}

pre.calc{font:8.2pt/1.6 var(--bl-font-data);background:var(--bl-mineral);color:var(--bl-paper-on-mineral);padding:11px 14px;margin:.04in 0 .13in;
  white-space:pre;break-inside:avoid;border-radius:2px}
.disclosure{border:1.5px solid var(--bl-oxide);background:var(--bl-paper-raised);padding:10px 14px;margin:.08in 0 .14in;break-inside:avoid}
.disclosure span{display:block;font:500 6.6pt/1 var(--bl-font-body);letter-spacing:.18em;text-transform:uppercase;color:var(--bl-oxide-dark);margin-bottom:6px}
.disclosure strong{font:700 11pt/1.35 var(--bl-font-heading);color:var(--bl-ink)}
.note{border-left:3px solid var(--bl-steel);background:var(--bl-paper-inset);padding:9px 14px;margin:.06in 0 .14in;font-size:8.8pt;break-inside:avoid}
.note b{display:block;font:500 6.6pt/1 var(--bl-font-body);letter-spacing:.16em;text-transform:uppercase;color:var(--bl-steel-dark);margin-bottom:5px}

dl.layer{display:grid;grid-template-columns:1.9in 1fr;border:1px solid var(--bl-rule-strong);background:var(--bl-paper-raised);font-size:8.8pt;line-height:1.42}
dl.layer dt,dl.layer dd{padding:6px 10px;border-top:1px solid var(--bl-rule);break-inside:avoid}
dl.layer dt:first-of-type,dl.layer dt:first-of-type + dd{border-top:0}
dl.layer dt{font:500 6.8pt/1.5 var(--bl-font-body);letter-spacing:.12em;text-transform:uppercase;color:var(--bl-ink-muted);background:var(--bl-paper-inset)}
dl.layer dd{color:var(--bl-ink)}
.key{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:.04in 0 .16in}
.key div{border:1px solid var(--bl-rule-strong);background:var(--bl-paper-raised);padding:8px 10px;font-size:8.2pt;line-height:1.35}
.key .chip{margin-bottom:5px}
section.sources li{font-size:8.5pt;margin-bottom:7px}
section.sources .src-id{font:8pt var(--bl-font-data);color:var(--bl-ink)}
section.sources .hedge{display:block;color:var(--bl-ink-muted)}
.colophon{margin-top:.24in;border-top:1px solid var(--bl-rule-strong);padding-top:10px;font-size:7.8pt;line-height:1.5;color:var(--bl-ink-muted);break-inside:avoid}
.colophon code{font:7.2pt var(--bl-font-data);word-break:break-all;color:var(--bl-ink-soft)}
.colophon .sign{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px}
.colophon .motto{font:700 14pt/1 var(--bl-font-heading);color:var(--bl-ink)}
.colophon .site{font:8pt/1 var(--bl-font-data);color:var(--bl-mineral);letter-spacing:.06em}
"""

NEWPAGE = {"10"}


def build(num: str, rev: str) -> tuple[str, str]:
    raw = CANVAS.read_text()
    if "Status: **locked**" not in raw:
        sys.exit("operator-canvas.md is not locked; refusing to render a public edition")
    canvas_sha = hashlib.sha256(raw.encode()).hexdigest()
    _, secs = parse(raw)
    by_name = dict(secs)
    missing = OMIT - by_name.keys()
    if missing:
        sys.exit(f"expected internal sections not found: {missing}")

    body: list[str] = []
    # Reading key + Public Canvas layer (the one-screen summary) first.
    key = "".join(
        f'<div><span class="chip chip-{LABELS[k]}">{k}</span><br>{html.escape(v)}</div>'
        for k, v in [("OBSERVED", "Sourced fact. Every one carries a claim ID resolved in Source notes."),
                     ("PARALLEL", "Transferred from an adjacent model that already exists."),
                     ("MODELED", "An assumption, with its arithmetic stated."),
                     ("UNKNOWN", "An open question, carried rather than hidden.")])
    body.append(
        '<section class="newpage"><div class="sh"><span class="n">KEY</span><h2>How to read this Canvas</h2></div>'
        "<p>Overall evidence class: <strong>adjacent synthesis</strong>. Every material statement "
        "carries one of four evidence labels. The overall class and the per-statement labels are "
        "different things.</p>"
        f'<div class="key">{key}</div>'
        '<div class="sh"><span class="n">00</span><h2>Public Canvas layer</h2></div>'
        f'{public_layer(by_name["Public Canvas layer"])}</section>')

    for name, text in secs:
        if name in OMIT or name == "Public Canvas layer":
            continue
        m = re.match(r"(\d+A?)\. (.+)$", name)
        n, h = (m.group(1), m.group(2)) if m else ("·", name)
        cls = "newpage" if n in NEWPAGE else ""
        content = render_body(text)
        if name in NOTE_AFTER:
            t, v = NOTE_AFTER[name]
            content += f'<div class="note"><b>{html.escape(t)}</b>{html.escape(v)}</div>'
        body.append(f'<section class="{cls}"><div class="sh"><span class="n">§{n.zfill(2) if n != "7A" else "07A"}'
                    f'</span><h2>{html.escape(h)}</h2></div>{content}</section>')

    src = "".join(
        f'<li><span class="src-id">{i}</span> <span class="chip chip-{LABELS[c]}">{c}</span> '
        f"{html.escape(t)}{'. <a href=\"' + u + '\">' + html.escape(u) + '</a>' if u else ''}"
        f'<span class="hedge">{html.escape(hd)}</span></li>'
        for i, c, t, u, hd in SOURCES)
    body.append(
        '<section class="sources newpage"><div class="sh"><span class="n">SRC</span><h2>Source notes and disclosures</h2></div>'
        f'<ul class="bullets">{src}</ul>'
        "<p>All fees, hours, property counts and costs are the Canvas's own §10 assumptions, "
        "labeled <strong>MODELED</strong>, computed on an illustrative inn that does not exist. "
        "Nobody has built this practice and published what it earns.</p>"
        f'<div class="disclosure"><span>Economics disclosure</span><strong>{html.escape(DISCLOSURE)}</strong></div>'
        '<div class="note"><b>Scope boundary</b>The three recurring jobs only: findable, bookable, '
        "remembered. Rates and revenue management stay outside, and so does anything that touches "
        "what a room should cost. The guest list belongs to the property, never to the operator. "
        "Guest contact details are used only inside each booking site's own partner terms, the "
        "American email law, and European rules for European guests; no marketing to a relay "
        "address, ever. Nothing in this Canvas is legal advice, and the recoverable amount it "
        "models is a ceiling a fee sits under, not commission this service saves.</div>"
        f'<div class="note"><b>AI and host disclosure</b>{html.escape(AI_DISCLOSURE)} {html.escape(HOST_NOTE)}</div>'
        '<div class="colophon">'
        "<p>Public print edition of the locked EP009 Operator Canvas (locked 2026-09-03, header "
        "reconciled 2026-10-12, template operator-blueprint-v2-step1-v1.5). Text is transcribed from "
        "the lock. Omitted as internal: the pitch-deck and episode coverage map, the E3 readiness "
        "check and the lock record. No figure is withheld: EP009's publication rules require every "
        "modelled figure to carry its hedge rather than be removed, and those hedges sit on the page "
        "with the figures they qualify.</p>"
        f"<p>Source Canvas SHA-256: <code>{canvas_sha}</code></p>"
        '<div class="sign"><span class="motto">Build. Own. Operate.</span>'
        '<span class="site">theoperatoreconomy.com</span></div></div></section>')

    fonts = "".join([
        font_face("BL Boska", "boska-700.woff2", 700),
        font_face("BL Zodiak", "zodiak-700.woff2", 700),
        font_face("BL Supreme", "supreme-400.woff2", 400),
        font_face("BL Supreme", "supreme-400-italic.woff2", 400, "italic"),
        font_face("BL Supreme", "supreme-500.woff2", 500),
    ])
    css = fonts + tokens() + CSS.replace("{num}", num).replace("{rev}", rev)
    pre = TITLE_PRE.format(num=num)
    cover = f"""<div class="cover">
  <div class="mast"><div class="brand"><small>THE</small>Operator Economy</div>
    <div class="no">OPERATOR CANVAS №{num} · REV {rev}<br>LOCKED 2026-09-01 · EDITION {date.today().isoformat()}</div></div>
  <div class="kicker">Exit readiness · Operator Canvas</div>
  <h1><span class="pre">{html.escape(pre)}</span>{html.escape(TITLE_NAME)}</h1>
  <p class="sub">It makes a small business able to survive a buyer's inspection.</p>
  <div class="docket"><div class="dh"><span>Episode companion</span><span>Adjacent synthesis</span></div>
    <dl>
      <dt>Episode</dt><dd>{html.escape(EPISODE_TITLE)}</dd>
      <dt>Buyer</dt><dd>An owner-operated business with real profit, exiting in one to five years.</dd>
      <dt>Offer</dt><dd>One fixed-scope readiness engagement.</dd>
      <dt>Result</dt><dd>A business that survives inspection, and a signed record of what was resolved.</dd>
      <dt>Economics</dt><dd class="fail">The base case does not clear the modeled livelihood requirement.</dd>
      <dt>First step</dt><dd>Build and publish the checklist, then run one diagnostic unpaid and record the hours.</dd>
    </dl></div>
  <div class="disclosure"><span>Economics disclosure</span><strong>{html.escape(DISCLOSURE)}</strong></div>
  <p class="fine"><strong>Scope boundary.</strong> Preparation only: never paid on a transaction, never advises on
  one. Not legal, tax or financial advice. <strong>AI and host.</strong> {html.escape(AI_DISCLOSURE)}
  {html.escape(HOST_NOTE)}</p>
</div>"""
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f"<title>{html.escape(pre)} {TITLE_NAME}</title>"
           f"<style>{css}</style></head><body>{cover}{''.join(body)}</body></html>")
    return doc, canvas_sha


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--number", default="001")
    ap.add_argument("--rev", default="A")
    a = ap.parse_args()
    doc, sha = build(a.number, a.rev)
    html_path = EP / "canvas.html"
    html_path.write_text(doc)
    pdf = EP / f"Operator-Canvas-{a.number}.pdf"
    pdf.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        try:
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={tmp}",
                            "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                            "--virtual-time-budget=5000", html_path.as_uri()],
                           capture_output=True, text=True, timeout=90)
        except subprocess.TimeoutExpired:
            pass
    if not pdf.exists():
        sys.exit("PDF not written")
    print(f"canvas sha256 {sha}\nhtml -> {html_path}\npdf  -> {pdf}")


if __name__ == "__main__":
    main()
