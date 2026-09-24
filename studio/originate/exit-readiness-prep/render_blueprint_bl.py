"""
render_blueprint_bl.py: EP007 content/blueprint.md -> Boundary Ledger worksheet PDF.

Why not scripts/originate/render_blueprint.py: that renderer is a Rev C, fixed six-section
template (idea / evidence / stack / playbook / honest math / sources). EP007's approved
worksheet has thirteen sections of forms, checklists and write-in tables; the old template would
silently drop Parts 1-9. This renders the approved copy verbatim with Boundary Ledger 2.0 tokens
(design-system/boundary-ledger/tokens.css, vendored fonts embedded as data URIs).

Usage (from studio/):
    python originate/exit-readiness-prep/render_blueprint_bl.py [--number 001] [--rev A]

Writes originate/exit-readiness-prep/blueprint.html and Operator-Blueprint-<NNN>.pdf.
Does not copy to site/public (do that at site-flip time, see launch/UPLOAD-PLAN.md).
"""
from __future__ import annotations

import argparse
import base64
import html
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

EP = Path(__file__).resolve().parent
REPO = EP.parents[2]
BL = REPO / "design-system" / "boundary-ledger"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def font_face(family: str, file: str, weight: int, style: str = "normal") -> str:
    b64 = base64.b64encode((BL / "fonts" / file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64}) "
            f"format('woff2');font-weight:{weight};font-style:{style}}}")


def tokens() -> str:
    """The :where(...) token block from tokens.css, re-scoped to :root for print."""
    css = (BL / "tokens.css").read_text()
    block = css[css.rindex(":where(.bl-system"):]
    return ":root" + block[block.index("{"):]


# ------------------------------------------------------------------ markdown -> html

def inline(s: str) -> str:
    s = html.escape(s.strip(), quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', s)
    return s


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


CLASS_ROLE = {"reported": "rep", "parallel": "par", "modeled": "mod"}


def table(lines: list[str], part: str) -> str:
    head = cells(lines[0])
    align = ["num" if c.strip().endswith(":") else "" for c in cells(lines[1])]
    rows = [cells(l) for l in lines[2:]]
    blank = [r for r in rows if not any(r)]
    # A single empty template row is a write-in form: give the reader room to write.
    if blank and len(rows) == 1:
        rows = rows * 7
    writein = any(not any(r[1:]) for r in rows) or bool(blank)
    cls = "writein" if writein else ""
    if "evidence" in part:
        cls = "evidence"
    out = [f'<table class="{cls}"><thead><tr>']
    out += [f"<th>{inline(h)}</th>" for h in head]
    out.append("</tr></thead><tbody>")
    for r in rows:
        r += [""] * (len(head) - len(r))
        tds = []
        for i, c in enumerate(r):
            a = f' class="{align[i]}"' if i < len(align) and align[i] else ""
            if cls == "evidence" and head[i].lower() == "class":
                role = CLASS_ROLE.get(c.split(",")[0].strip().lower(), "rep")
                tds.append(f'<td><span class="chip chip-{role}">{inline(c)}</span></td>')
            else:
                tds.append(f"<td{a}>{inline(c)}</td>")
        total = ' class="total"' if r[0].startswith("**Total") else ""
        out.append(f"<tr{total}>" + "".join(tds) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_body(md: str, part: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            while not lines[j].strip().startswith("```"):
                j += 1
            code = html.escape("\n".join(lines[i + 1:j]), quote=False)
            out.append(f'<pre class="calc">{code}</pre>')
            i = j + 1
            continue
        if s.startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(table(lines[i:j], part))
            i = j
            continue
        if s.startswith(">"):
            j = i
            buf = []
            while j < len(lines) and lines[j].strip().startswith(">"):
                buf.append(lines[j].strip().lstrip(">").strip())
                j += 1
            out.append(f'<blockquote>{inline(" ".join(buf))}</blockquote>')
            i = j
            continue
        if s.startswith("- "):
            items = []
            j = i
            while j < len(lines) and (lines[j].strip().startswith("- ")
                                      or (lines[j].startswith("  ") and lines[j].strip())):
                if lines[j].strip().startswith("- "):
                    items.append(lines[j].strip()[2:])
                else:
                    items[-1] += " " + lines[j].strip()
                j += 1
            check = all(it.startswith("[ ]") for it in items)
            lis = []
            for it in items:
                if check:
                    lis.append(f'<li><span class="box" aria-hidden="true"></span>'
                               f"<span>{inline(it[3:])}</span></li>")
                else:
                    lis.append(f"<li>{inline(it)}</li>")
            out.append(f'<ul class="{"checklist" if check else "bullets"}">' + "".join(lis) + "</ul>")
            i = j
            continue
        # paragraph
        j = i
        buf = []
        while j < len(lines) and lines[j].strip() and not re.match(r"\s*(\||```|>|- |---)", lines[j]):
            buf.append(lines[j].strip())
            j += 1
        text = " ".join(buf)
        if re.fullmatch(r"\*\*[A-F]\. .+\*\*", text):
            out.append(f'<h3 class="group">{inline(text.strip("*"))}</h3>')
        elif re.match(r"^(Owner|Operator) signature:", text):
            for sig in [x for x in re.split(r"(?=Operator signature:)", text) if x.strip()]:
                label = sig.split(":")[0]
                out.append(f'<div class="sig"><span>{label}</span><span class="line"></span>'
                           f'<span>Date</span><span class="line short"></span></div>')
        else:
            out.append(f"<p>{inline(text)}</p>")
        i = j
    return "".join(out)


def split_sections(md: str) -> tuple[str, list[tuple[str, str]]]:
    title = re.search(r"^#\s+(.+)$", md, re.M).group(1).strip()
    parts = re.split(r"^##\s+", md, flags=re.M)
    secs = []
    for p in parts[1:]:
        name, _, body = p.partition("\n")
        secs.append((name.strip(), body))
    return title, secs


CSS = """
@page{size:Letter;margin:.62in .7in .72in;background:#f5f0e6;
  @bottom-left{content:"THE OPERATOR ECONOMY  ·  OPERATOR BLUEPRINT №{num}  ·  REV {rev}";
    font:500 7.5px/1 var(--bl-font-body);letter-spacing:.16em;color:#566461}
  @bottom-right{content:counter(page) " / " counter(pages);
    font:7.5px/1 var(--bl-font-data);letter-spacing:.08em;color:#566461}}
@page:first{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{background:var(--bl-paper);color:var(--bl-ink-soft);font:400 10.2pt/1.52 var(--bl-font-body)}
a{color:var(--bl-mineral);text-decoration:none;word-break:break-all}
strong{color:var(--bl-ink);font-weight:500}
code{font:8.5pt var(--bl-font-data)}

/* cover */
.cover{height:11in;padding:.62in .7in .6in;display:flex;flex-direction:column;background:var(--bl-paper);
  break-after:page}
.mast{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--bl-ink);padding-bottom:10px}
.mast .brand{font:700 15pt/1 var(--bl-font-heading);color:var(--bl-ink)}
.mast .brand small{display:block;font:500 6.5pt/1 var(--bl-font-body);letter-spacing:.3em;color:var(--bl-ink-muted);margin-bottom:5px}
.mast .no{font:7.5pt/1 var(--bl-font-data);letter-spacing:.18em;color:var(--bl-ink-muted)}
.kicker{margin-top:1.05in;font:500 7.5pt/1 var(--bl-font-body);letter-spacing:.26em;color:var(--bl-steel-dark)}
h1{font:700 44pt/.98 var(--bl-font-display);color:var(--bl-ink);margin:.16in 0 .18in;max-width:6in;letter-spacing:-.005em}
.sub{font:400 13pt/1.45 var(--bl-font-body);color:var(--bl-ink-soft);max-width:5.4in}
.docket{margin-top:auto;border:1px solid var(--bl-rule-strong);background:var(--bl-paper-raised)}
.docket .dh{display:flex;justify-content:space-between;background:var(--bl-mineral);color:var(--bl-paper-on-mineral);
  font:500 7pt/1 var(--bl-font-body);letter-spacing:.2em;padding:9px 14px}
.docket dl{display:grid;grid-template-columns:1.35in 1fr}
.docket dt,.docket dd{padding:9px 14px;border-top:1px solid var(--bl-rule)}
.docket dt{font:500 7pt/1.6 var(--bl-font-body);letter-spacing:.18em;color:var(--bl-ink-muted);text-transform:uppercase}
.docket dd{font-size:9.6pt;color:var(--bl-ink)}
.docket dd.commit{color:var(--bl-oxide-dark);font-weight:500}
.cover .note{margin-top:14px;font-size:8pt;color:var(--bl-ink-muted);max-width:6.4in}

/* sections */
section{break-before:auto}
section.newpage{break-before:page}
.sh{display:flex;align-items:baseline;gap:14px;border-top:1.5px solid var(--bl-ink);padding-top:9px;margin:.28in 0 .13in;
  break-after:avoid}
section.newpage .sh{margin-top:0}
.sh .n{font:8pt/1 var(--bl-font-data);color:var(--bl-steel);letter-spacing:.1em;min-width:.3in}
h2{font:700 19pt/1.08 var(--bl-font-heading);color:var(--bl-ink)}
h2 .qual{display:block;font:400 9.5pt/1.3 var(--bl-font-body);color:var(--bl-ink-muted);margin-top:5px}
h3.group{font:700 11pt/1.2 var(--bl-font-heading);color:var(--bl-mineral);margin:.12in 0 .03in;break-after:avoid}
p{margin:0 0 .09in;max-width:6.9in}
ul.bullets{margin:0 0 .1in 0;list-style:none}
ul.bullets li{position:relative;padding-left:16px;margin-bottom:4px}
ul.bullets li::before{content:"";position:absolute;left:2px;top:.62em;width:7px;height:1px;background:var(--bl-steel)}
ul.checklist{list-style:none;margin:0 0 .08in}
ul.checklist li{display:flex;gap:10px;align-items:flex-start;padding:3px 0;line-height:1.4;border-bottom:1px solid var(--bl-rule);break-inside:avoid}
.box{flex:0 0 auto;width:10px;height:10px;margin-top:3px;border:1.2px solid var(--bl-ink-soft);border-radius:1px;background:var(--bl-paper-raised)}

table{width:100%;border-collapse:collapse;margin:.06in 0 .14in;font-size:8.6pt;line-height:1.38;background:var(--bl-paper-raised);
  border:1px solid var(--bl-rule-strong)}
thead{display:table-header-group}
tr{break-inside:avoid}
th{text-align:left;font:500 6.6pt/1.3 var(--bl-font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--bl-ink-muted);
  background:var(--bl-paper-inset);padding:7px 8px;border-bottom:1px solid var(--bl-rule-strong);vertical-align:bottom}
td{padding:6px 8px;border-top:1px solid var(--bl-rule);vertical-align:top}
td+td,th+th{border-left:1px solid var(--bl-rule)}
td.num,th.num{text-align:right;font-family:var(--bl-font-data)}
table.writein td{height:.44in}
table.writein td:first-child{color:var(--bl-ink);font-weight:500}
table.writein tr.total td{height:.34in;background:var(--bl-paper-inset)}
table.evidence th{background:var(--bl-mineral);color:var(--bl-paper-on-mineral);border-bottom:none}
table.evidence td:first-child{color:var(--bl-ink);font-weight:500;width:2.05in}
table.evidence td:last-child{color:var(--bl-ink-muted)}
.chip{display:inline-block;font:500 6.4pt/1.25 var(--bl-font-body);letter-spacing:.1em;text-transform:uppercase;padding:2px 5px;border:1px solid}
.chip-rep{color:var(--bl-mineral);border-color:var(--bl-mineral)}
.chip-par{color:var(--bl-steel-dark);border-color:var(--bl-steel)}
.chip-mod{color:var(--bl-steel-dark);border-color:var(--bl-steel);border-style:dashed}

pre.calc{font:8.3pt/1.6 var(--bl-font-data);background:var(--bl-mineral);color:var(--bl-paper-on-mineral);padding:12px 14px;margin:.04in 0 .14in;
  white-space:pre;break-inside:avoid;border-radius:2px}
blockquote{margin:.08in 0 .14in;padding:12px 16px;border-left:3px solid var(--bl-steel);background:var(--bl-paper-inset);
  font:700 12pt/1.35 var(--bl-font-heading);color:var(--bl-ink)}
blockquote strong{font-weight:700}
.sig{display:flex;align-items:flex-end;gap:10px;margin:.2in 0 .04in;font:500 7pt/1 var(--bl-font-body);letter-spacing:.14em;
  text-transform:uppercase;color:var(--bl-ink-muted)}
.sig .line{flex:1;border-bottom:1px solid var(--bl-ink-soft);height:1px}
.sig .line.short{flex:0 0 1.4in}

.sig + p{margin-top:.2in}
/* the one active commitment: the first move */
section.first-move .panel{border:1.5px solid var(--bl-oxide);background:var(--bl-paper-raised);padding:14px 18px;break-inside:avoid}
section.first-move .sh{border-top-color:var(--bl-oxide)}
section.first-move .sh .n{color:var(--bl-oxide)}
section.sources ul.bullets li{font-size:8.6pt;margin-bottom:6px}
section.sources p{font-size:8.6pt;color:var(--bl-ink-muted)}
.colophon{margin-top:.3in;border-top:1px solid var(--bl-rule-strong);padding-top:12px;display:flex;justify-content:space-between;
  align-items:baseline;break-inside:avoid}
.colophon .motto{font:700 15pt/1 var(--bl-font-heading);color:var(--bl-ink)}
.colophon .site{font:8pt/1 var(--bl-font-data);color:var(--bl-mineral);letter-spacing:.06em}
"""

NEWPAGE = {"Part 1", "Part 2", "Part 3", "Part 4", "Part 5", "Part 6", "Part 7", "Part 9"}


def build(num: str, rev: str) -> str:
    md = (EP / "content" / "blueprint.md").read_text()
    title, secs = split_sections(md)
    main_title, _, kind = title.partition(":")
    body = []
    n = 0
    for name, text in secs:
        key = name.split(".")[0]
        cls = []
        if key in NEWPAGE:
            cls.append("newpage")
        if name.lower() == "the first move":
            cls.append("first-move")
        if name.lower() == "sources":
            cls.append("sources")
        m = re.match(r"(Part \d+)\. (.+?)(?: \((.+)\))?$", name)
        n += 1
        if m:
            label, h, qual = m.group(1), m.group(2), m.group(3)
            num_lbl = m.group(1).split()[1].zfill(2)
        else:
            label, h, qual, num_lbl = None, name, None, "·"
        qual_html = f'<span class="qual">{html.escape(qual)}</span>' if qual else ""
        content = render_body(text, name.lower())
        if "first-move" in cls:
            content = f'<div class="panel">{content}</div>'
        extra = ""
        if name.lower() == "sources":
            extra = ('<div class="colophon"><span class="motto">Build. Own. Operate.</span>'
                     '<span class="site">theoperatoreconomy.com</span></div>')
        body.append(f'<section class="{" ".join(cls)}"><div class="sh"><span class="n">'
                    f'{"PART " + num_lbl if label else ""}</span><h2>{html.escape(h)}{qual_html}</h2>'
                    f"</div>{content}{extra}</section>")

    fonts = "".join([
        font_face("BL Boska", "boska-700.woff2", 700),
        font_face("BL Zodiak", "zodiak-700.woff2", 700),
        font_face("BL Supreme", "supreme-400.woff2", 400),
        font_face("BL Supreme", "supreme-400-italic.woff2", 400, "italic"),
        font_face("BL Supreme", "supreme-500.woff2", 500),
    ])
    css = fonts + tokens() + CSS.replace("{num}", num).replace("{rev}", rev)
    today = date.today().isoformat()
    cover = f"""<div class="cover">
  <div class="mast"><div class="brand"><small>THE</small>Operator Economy</div>
    <div class="no">OPERATOR BLUEPRINT №{num} · REV {rev} · {today}</div></div>
  <div class="kicker">{html.escape(kind.strip().upper())}</div>
  <h1>{html.escape(main_title.strip())}</h1>
  <p class="sub">Decide whether to build a one-person, fixed-fee practice that gets owner-run
  businesses ready to be inspected by a buyer, and run the first test that tells you.</p>
  <div class="docket"><div class="dh"><span>Episode companion</span><span>Modeled, not observed</span></div>
    <dl>
      <dt>Episode</dt><dd>The One-Person Business That Gets Companies Ready for a Sale</dd>
      <dt>Business</dt><dd>A one-person, fixed-fee practice that gets owner-run businesses ready to be inspected by a buyer</dd>
      <dt>Offer</dt><dd>One engagement. One business. Fixed scope, fixed fee.</dd>
      <dt>Never</dt><dd>Valuing the business, finding a buyer, negotiating a deal, any fee tied to a sale</dd>
      <dt>First move</dt><dd class="commit">Run Part 1 for free, with Part 5 running.</dd>
    </dl></div>
  <p class="note">Nothing in this worksheet is legal, tax, or financial advice, and nothing in it
  predicts what any business will sell for.</p>
</div>"""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f"<title>Operator Blueprint №{num}: {html.escape(main_title.strip())}</title>"
            f"<style>{css}</style></head><body>{cover}{''.join(body)}</body></html>")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--number", default="001")
    ap.add_argument("--rev", default="A")
    a = ap.parse_args()
    html_path = EP / "blueprint.html"
    html_path.write_text(build(a.number, a.rev))
    pdf = EP / f"Operator-Blueprint-{a.number}.pdf"
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
    print(f"html -> {html_path}\npdf  -> {pdf}")


if __name__ == "__main__":
    main()
