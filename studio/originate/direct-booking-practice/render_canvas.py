"""
render_canvas.py: EP009 locked Operator Canvas -> public "Operator Canvas" print edition (PDF).

Adapted from originate/exit-readiness-prep/render_canvas.py (EP007, Operator Canvas №001).
Internal EP009 publishes as public No. 002 under the publication slug direct-booking-practice
(content-os/facts.md "EP009 research"); its internal folders keep the EP009-direct-booking-recovery
name.

Source: operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/operator-canvas.md
(approved and locked by the owner 2026-09-03; its SHA-256 is recorded in 01-editorial/editorial-lock.md
and the build refuses to render any other bytes). The Canvas text is transcribed, not rewritten.
This script only:

  * omits the Canvas's internal-only material (header metadata, the pitch-deck and episode
    coverage map, the E3 readiness check, the Canvas lock block, and two pointers to the internal
    operating description held in the editorial contract);
  * drops, cleanly, the one modeled figure the Canvas states in three places without a model label,
    which content-os/facts.md "DO NOT STATE — EP009" forbids (see WITHHOLD; EP007 owner ruling
    2026-09-23: dropped cleanly, no withheld markers);
  * adds derivation-authored glue: cover, reading key, "illustrative, in the model" notes on the
    §10 arithmetic, source notes with the facts.md hedges, "not legal advice", disclosures and
    provenance.

Boundary Ledger 2.0 tokens and vendored fonts (helpers reused from EP007's render_blueprint_bl.py),
printed with headless Chrome or Playwright's Chromium.

Usage (from studio/):
    python originate/direct-booking-practice/render_canvas.py [--number 002] [--rev A]

Writes originate/direct-booking-practice/canvas.html and Operator-Canvas-<NNN>.pdf.
Does not copy to site/public.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import html
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent / "exit-readiness-prep"))
from render_blueprint_bl import CHROME as MAC_CHROME, REPO, font_face, tokens  # noqa: E402


def chrome() -> str:
    """$CHROME, else the macOS Chrome EP007 used, else Playwright's Chromium (Linux)."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    if Path(MAC_CHROME).exists():
        return MAC_CHROME
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    hits = sorted(glob.glob(f"{root}/chromium-*/chrome-linux/chrome"))
    if not hits:
        sys.exit("no Chrome found; set CHROME")
    return hits[-1]


EPDIR = REPO / "operator-blueprint-v2" / "episodes" / "EP009-direct-booking-recovery" / "01-editorial"
CANVAS = EPDIR / "operator-canvas.md"
LOCK = EPDIR / "editorial-lock.md"
LOCK_DATE = "2026-09-03"

TITLE_PRE = "Operator Canvas №{num}:"
TITLE_NAME = "a direct-booking practice"
# Owner-selected title, studio/originate/direct-booking-practice/launch/thumbnail-note.md (T1).
EPISODE_TITLE = "The One-Person Business That Gets Small Hotels Booking Direct"
DISCLOSURE = "Modeled scenario, not observed performance or an earnings forecast."
# site/app/lib/brand.ts AI_DISCLOSURE (owner-approved, verbatim), as in EP007.
AI_DISCLOSURE = ("Episodes are presented by an AI avatar of the host, with narration in a clone of "
                 "his voice. The research and the arguments are his.")
# facts.md EP009: nobody has built this and published what it earns (C022). No biography here:
# the Canvas carries none, and the narrated hospitality line is an episode-scoped owner exception.
HOST_NOTE = ("Nothing in this Canvas describes a delivered client engagement, and nobody has built "
             "this practice and published what it earns.")

# Canvas sections that stay internal (not public): omitted whole.
OMIT = {"Pitch-deck and episode coverage map", "E3 readiness check", "Canvas lock"}

# Exact-match only; the build fails if the locked text ever changes under one of these.
WITHHOLD = [
    # facts.md "DO NOT STATE — EP009": no modeled figure without "illustrative" / "in the model" in
    # the same breath. The $600 retainer is modeled (C028); these three places state it bare.
    # Dropped cleanly per the EP007 owner ruling (2026-09-23): no withheld markers.
    ("owner will not fund $600 a month, or direct share", "owner will not fund the retainer, or direct share"),
    ("| no owner in the band funds $600 a month |", "| no owner in the band funds the retainer |"),
    ("Failure signal: no owner funds $600 a month.", "Failure signal: no owner funds the retainer."),
    # facts.md C011: one agency publishes its own $1,500 entry price ("one publishes"). It is not a
    # market floor, and nothing here may state that agencies serve the 20-40 room band.
    ("Hire a hotel marketing agency from $1,500 a month (CLM-011).",
     "Hire a hotel marketing agency; one publishes an entry price of $1,500 a month (CLM-011)."),
    ("(CLM-011: the agency floor is $1,500 for a broader scope)",
     "(CLM-011: one agency publishes an entry price of $1,500, for a broader scope)"),
    ("| agencies retain 30-room inns at $1,500 |",
     "| an agency is found retaining 30-room inns at its published $1,500 entry price |"),
    # Internal-only pointers to the editorial contract (not a public document).
    ("Precise internal operating description: see the editorial contract. Held outside first-listen "
     "narration.\n\n", ""),
    ("Precise internal operating description, retained outside first-listen narration: see the "
     "editorial contract.\n", ""),
]

# Hedges from content-os/facts.md EP009, placed on the same page as the figures they qualify.
NOTE_AFTER = {
    "3. Costly problem": ("Read the source before the number",
                          "The 63.4 percent OTA share and the 21.8 versus 10.6 percent cancellation "
                          "rates are Cloudbeds' own worldwide data, published by a company that sells "
                          "the alternative. They are not US figures. The 50.9 percent direct share is "
                          "HOTREC's, for Europe. The 65 percent staffing figure is an AHLA survey of 282 "
                          "hoteliers. The roughly 15 percent base commission comes from trade reporting "
                          "for most European markets, not from a Booking.com price list."),
    "7. Capabilities and stack": ("Not legal advice",
                                  "Guest data under OTA partner terms, CAN-SPAM and GDPR is described "
                                  "here as a design boundary. This is not legal advice. Anything touching "
                                  "rate-parity terms, rate display, or EU guest data beyond consent-first "
                                  "handling goes to the owner's own counsel."),
    "10. Economics model": ("Read the filings figures as global",
                            "Booking Holdings' $186.1 billion and Expedia's $119.6 billion are 2025 gross "
                            "bookings by their own filings, worldwide and blended across products. They "
                            "are not hotel commission and not US figures, and they are not added together."),
}

# facts.md EP009: every modeled figure carries "illustrative" / "in the model" in the same breath.
# Placed directly under the §10 sub-heading, ahead of the arithmetic it qualifies.
H3_NOTE = {
    "The property's ceiling (the buyer's rational maximum)": (
        "Illustrative, in the model",
        "Every figure in this table and in the sensitivities below it is arithmetic on an invented "
        "20-room inn, from the four stated inputs. The 10-point mix shift is a hypothesis nobody has "
        "measured. Net recoverable is the ceiling a fee sits under, not commission the service saves, "
        "and its low bound rests on one vendor's own direct-cost figure."),
    "The operator's business": (
        "Illustrative, in the model",
        "Every price, hour, count and total in this part is a modeled assumption or arithmetic on one. "
        "None of it is earnings, observed or forecast."),
}

SOURCES = [
    ("CLM-001", "OBSERVED", "Cloudbeds, 2026 State of Independent Hotels (press release)",
     "https://www.globenewswire.com/news-release/2026/03/25/3262232/0/en/",
     "Reported, vendor-published research on its own dataset. Cloudbeds sells the alternative. "
     "Worldwide, not US and not specific to small properties."),
    ("CLM-002", "OBSERVED", "HOTREC and HES-SO, European hotel distribution study, reference year 2023",
     "https://www.hotrec.eu/en/news_digital-trends-in-accommodation-hotels-booking-com-and-dma_C2_A0_C2_A0.html",
     "Europe, not the US, all property sizes. Shows dependence is high but lower than the "
     "Cloudbeds global figure."),
    ("CLM-003", "OBSERVED", "Booking Holdings, 2025 annual report (10-K), via filing summary",
     "https://www.stocktitan.net/sec-filings/BKNG/10-k-booking-holdings-inc-files-annual-report-7fb6c3d1394a.html",
     "Gross bookings blended across products, worldwide. Not the hotel commission rate."),
    ("CLM-004", "OBSERVED", "Expedia Group, full-year 2025 results",
     "https://ir.expediagroup.com/news-and-events/news/news-details/2026/Expedia-Group-Reports-Fourth-"
     "Quarter-and-Full-Year-2025-Results/default.aspx",
     "Gross bookings blended across products, worldwide. Not the lodging commission and not a US figure."),
    ("CLM-005", "OBSERVED", "Booking.com for Partners, \"Understanding your commission\"; trade reporting",
     "https://partner.booking.com/en-gb/help/commission-invoices-tax/commission/understanding-our-commission",
     "Mechanics opened at source. The roughly 15 percent base band for most European markets and "
     "the 2026 Genius change are secondary, from trade reporting."),
    ("CLM-008", "OBSERVED", "Booking.com for Partners, \"Contacting your guests\"",
     "https://partner.booking.com/en-gb/help/reservations/contact-extranet/contacting-your-guests",
     "Alias and on-platform policy opened at source. Messaging-window durations are from the trade "
     "press, secondary."),
    ("CLM-009", "OBSERVED", "Google Hotel Center Help, free booking links",
     "https://support.google.com/hotelprices/answer/10472394?hl=en",
     "No fee. A small property connects through a Hotel Center account or an integration partner."),
    ("CLM-010", "OBSERVED", "Little Hotelier pricing (via secondary); Cloudbeds pricing",
     "https://www.cloudbeds.com/pricing/",
     "Public tool pricing, which changes. Tool price is not service demand."),
    ("CLM-011", "OBSERVED", "One agency's published entry price; revenue managers quote privately",
     "https://www.egochi.com/hotel-marketing-agency/",
     "Verifies one agency's own price only. Agency outcome claims and revenue-management uplift "
     "claims are excluded."),
    ("CLM-012", "OBSERVED", "AHLA, industry statistics and staffing survey of 282 hoteliers",
     "https://www.ahla.com/news/65-surveyed-hotels-report-staffing-shortages",
     "\"Small business\" is AHLA's definition, not a room band. Nobody has counted the 20 to 40 "
     "room band."),
    ("CLM-014", "OBSERVED", "D-EDGE, 2025 hotel direct distribution report",
     "https://www.d-edge.com/2025-hotel-direct-distribution-report/",
     "Vendor-published, its own client base. Used only as the low bound for direct cost in the model."),
    ("CLM-016", "OBSERVED", "The host's own hospitality background, content-os facts ledger", None,
     "Bounded vantage on buyer-side judgment only. Not a property owner or revenue manager, and no "
     "client outcome for this service."),
    ("ANA-002", "PARALLEL", "Step 0 analogy map: outsourced hotel revenue management", None,
     "Adjacent parallel. An outside specialist on retainer for a property too small to hire. Does "
     "not show what a 20 to 40 room property will pay."),
    ("ANA-003", "PARALLEL", "Step 0 analogy map: independent-hotel marketing agencies", None,
     "Adjacent parallel. The buyer already funds outside help and accepts direct share as the "
     "reported outcome. Does not show that agencies serve the band."),
    ("ANA-009", None, "Step 0 analogy map: vendor uplift claims (rejected)", None,
     "Rejected. Seller-published outcome claims about the service being sold. Not used anywhere in "
     "this Canvas."),
]

LABELS = {"OBSERVED": "obs", "PARALLEL": "par", "MODELED": "mod", "UNKNOWN": "unk",
          "PARALLEL/MODELED": "par"}


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
            if s[4:] in H3_NOTE:
                t, v = H3_NOTE[s[4:]]
                out.append(f'<div class="note"><b>{html.escape(t)}</b>{html.escape(v)}</div>')
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

table{break-inside:auto;width:100%;border-collapse:collapse;margin:.06in 0 .14in;font-size:8.4pt;line-height:1.36;background:var(--bl-paper-raised);border:1px solid var(--bl-rule-strong)}
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
    canvas_sha = hashlib.sha256(raw.encode()).hexdigest()
    # The EP009 Canvas header reads "approved"; the lock is the SHA-256 in editorial-lock.md.
    if "Decision: **lock.**" not in raw or f"`{canvas_sha}`" not in LOCK.read_text():
        sys.exit("operator-canvas.md does not match the locked hash in editorial-lock.md; "
                 "refusing to render a public edition")
    missing_h3 = [h for h in H3_NOTE if f"### {h}\n" not in raw]
    if missing_h3:
        sys.exit(f"expected §10 sub-headings not found: {missing_h3}")
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
        f'<li><span class="src-id">{i}</span> '
        f'{f"<span class=\"chip chip-{LABELS[c]}\">{c}</span> " if c else ""}'
        f"{html.escape(t)}{'. <a href=\"' + u + '\">' + html.escape(u) + '</a>' if u else ''}"
        f'<span class="hedge">{html.escape(hd)}</span></li>'
        for i, c, t, u, hd in SOURCES)
    body.append(
        '<section class="sources newpage"><div class="sh"><span class="n">SRC</span><h2>Source notes and disclosures</h2></div>'
        f'<ul class="bullets">{src}</ul>'
        "<p>All fees, hours, property counts and costs are the Canvas's own §10 assumptions, "
        "labeled <strong>MODELED</strong>, and illustrative: arithmetic in the model on an invented inn. "
        "No observed operator price for this practice exists.</p>"
        f'<div class="disclosure"><span>Economics disclosure</span><strong>{html.escape(DISCLOSURE)}</strong></div>'
        '<div class="note"><b>Scope boundary</b>Excluded: pricing strategy and revenue management, '
        "paid advertising and metasearch spend, any marketing to masked OTA addresses, any advice to "
        "leave the sites, and software resale. Guest data is used only with consent and inside the "
        "sites' rules. Nothing in this Canvas is legal, tax or financial advice, and nothing in it "
        "predicts what any property will save or any operator will earn.</div>"
        f'<div class="note"><b>AI and host disclosure</b>{html.escape(AI_DISCLOSURE)} {html.escape(HOST_NOTE)}</div>'
        '<div class="colophon">'
        "<p>Public print edition of the locked EP009 Operator Canvas (locked 2026-09-03, template "
        "operator-blueprint-v2-step1-v1.5). Text is transcribed from the lock. Omitted as internal: the "
        "pitch-deck and episode coverage map, the E3 readiness check, the lock record and two pointers "
        "to the internal operating description. One modeled retainer figure is omitted in the three "
        "places it appeared without its model label, under the publication rules for EP009.</p>"
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
    <div class="no">OPERATOR CANVAS №{num} · REV {rev}<br>LOCKED {LOCK_DATE} · EDITION {date.today().isoformat()}</div></div>
  <div class="kicker">Direct-booking recovery · Operator Canvas</div>
  <h1><span class="pre">{html.escape(pre)}</span>{html.escape(TITLE_NAME)}</h1>
  <p class="sub">It helps a small hotel get its returning guests to book direct, instead of paying a
  booking site to meet them again.</p>
  <div class="docket"><div class="dh"><span>Episode companion</span><span>Adjacent synthesis</span></div>
    <dl>
      <dt>Episode</dt><dd>{html.escape(EPISODE_TITLE)}</dd>
      <dt>Buyer</dt><dd>An owner-run US property of roughly 20 to 40 rooms with no marketing hire.</dd>
      <dt>Offer</dt><dd>A fixed-fee audit, then a monthly retainer for three jobs.</dd>
      <dt>Result</dt><dd>A baseline, a working direct path, a consented guest list, and one number monthly.</dd>
      <dt>Economics</dt><dd class="fail">In the model, the bottom of the band is a foothold, not a living.</dd>
      <dt>First step</dt><dd>Build the audit, run it on three properties, and put a retainer under each property's ceiling in front of its owner.</dd>
    </dl></div>
  <div class="disclosure"><span>Economics disclosure</span><strong>{html.escape(DISCLOSURE)}</strong></div>
  <p class="fine"><strong>Scope boundary.</strong> Never tells a property to leave the sites, never markets to a
  masked OTA address. Not legal, tax or financial advice. <strong>AI and host.</strong> {html.escape(AI_DISCLOSURE)}
  {html.escape(HOST_NOTE)}</p>
</div>"""
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f"<title>{html.escape(pre)} {TITLE_NAME}</title>"
           f"<style>{css}</style></head><body>{cover}{''.join(body)}</body></html>")
    return doc, canvas_sha


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--number", default="002")
    ap.add_argument("--rev", default="A")
    a = ap.parse_args()
    doc, sha = build(a.number, a.rev)
    html_path = EP / "canvas.html"
    html_path.write_text(doc)
    pdf = EP / f"Operator-Canvas-{a.number}.pdf"
    pdf.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        try:
            sandbox = ["--no-sandbox"] if hasattr(os, "geteuid") and os.geteuid() == 0 else []
            subprocess.run([chrome(), "--headless=new", "--disable-gpu", *sandbox, f"--user-data-dir={tmp}",
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
