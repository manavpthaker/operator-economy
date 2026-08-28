#!/usr/bin/env python3
"""Render the Operator Economy evidence and signals report to a designed PDF."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    LongTable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name("report-source.md")
OUTPUT = ROOT / "output" / "pdf" / "operator-economy-emergence-evidence-signals-2026.pdf"

PAPER = colors.HexColor("#F5F0E6")
PAPER_LIGHT = colors.HexColor("#FBF8F1")
PAPER_DARK = colors.HexColor("#EDE7D8")
RULE = colors.HexColor("#D8CFB9")
RULE_STRONG = colors.HexColor("#C4B99E")
INK = colors.HexColor("#1A1A1A")
INK_BODY = colors.HexColor("#3C3A36")
INK_MUTED = colors.HexColor("#6B675E")
BLUE = colors.HexColor("#1F3A5F")
BLUE_DARK = colors.HexColor("#14263E")
BLUE_LIGHT = colors.HexColor("#E4E9F0")
GOLD = colors.HexColor("#C4A45F")
NEGATIVE = colors.HexColor("#9B3E2E")

PAGE_W, PAGE_H = letter
LEFT = 0.72 * inch
RIGHT = 0.66 * inch
TOP = 0.82 * inch
BOTTOM = 0.68 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT
CONTENT_H = PAGE_H - TOP - BOTTOM


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("OEArial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("OEArial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("OEArial-Italic", str(font_dir / "Arial Italic.ttf")))
    pdfmetrics.registerFont(
        TTFont("OEArial-BoldItalic", str(font_dir / "Arial Bold Italic.ttf"))
    )
    pdfmetrics.registerFontFamily(
        "OEArial",
        normal="OEArial",
        bold="OEArial-Bold",
        italic="OEArial-Italic",
        boldItalic="OEArial-BoldItalic",
    )
    pdfmetrics.registerFont(TTFont("OEMono", "/System/Library/Fonts/SFNSMono.ttf"))


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "OE-H1",
            parent=base["Heading1"],
            fontName="OEArial-Bold",
            fontSize=24,
            leading=27,
            textColor=BLUE_DARK,
            spaceBefore=2,
            spaceAfter=15,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "OE-H2",
            parent=base["Heading2"],
            fontName="OEArial-Bold",
            fontSize=15.5,
            leading=19,
            textColor=BLUE,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "OE-H3",
            parent=base["Heading3"],
            fontName="OEArial-Bold",
            fontSize=11.5,
            leading=14,
            textColor=INK,
            spaceBefore=9,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "OE-Body",
            parent=base["BodyText"],
            fontName="OEArial",
            fontSize=9.35,
            leading=13.3,
            textColor=INK_BODY,
            spaceAfter=7,
            allowWidows=0,
            allowOrphans=0,
            splitLongWords=True,
        ),
        "small": ParagraphStyle(
            "OE-Small",
            parent=base["BodyText"],
            fontName="OEArial",
            fontSize=7.4,
            leading=9.7,
            textColor=INK_BODY,
            splitLongWords=True,
        ),
        "quote": ParagraphStyle(
            "OE-Quote",
            parent=base["BodyText"],
            fontName="OEArial-Bold",
            fontSize=12,
            leading=16,
            textColor=BLUE_DARK,
            leftIndent=17,
            rightIndent=10,
            borderColor=BLUE,
            borderWidth=0,
            borderPadding=(8, 12, 8, 14),
            backColor=BLUE_LIGHT,
            spaceBefore=5,
            spaceAfter=10,
        ),
        "bullet": ParagraphStyle(
            "OE-Bullet",
            parent=base["BodyText"],
            fontName="OEArial",
            fontSize=9.05,
            leading=12.3,
            textColor=INK_BODY,
            leftIndent=0,
            firstLineIndent=0,
            spaceAfter=2,
            splitLongWords=True,
        ),
        "caption": ParagraphStyle(
            "OE-Caption",
            parent=base["BodyText"],
            fontName="OEMono",
            fontSize=6.7,
            leading=8.8,
            textColor=INK_MUTED,
            spaceBefore=3,
            spaceAfter=5,
        ),
        "table": ParagraphStyle(
            "OE-Table",
            parent=base["BodyText"],
            fontName="OEArial",
            fontSize=7.15,
            leading=9.25,
            textColor=INK_BODY,
            splitLongWords=True,
        ),
        "table_header": ParagraphStyle(
            "OE-TableHeader",
            parent=base["BodyText"],
            fontName="OEArial-Bold",
            fontSize=7.2,
            leading=9.1,
            textColor=PAPER_LIGHT,
            splitLongWords=True,
        ),
    }


def safe_url_display(url: str) -> str:
    parsed = urlparse(url)
    text = parsed.netloc + parsed.path
    if parsed.query:
        text += "?" + parsed.query
    escaped = html.escape(text, quote=False)
    for separator in ("/", "-", "_", "?", "&amp;", "="):
        escaped = escaped.replace(separator, separator + "&#8203;")
    return escaped


def inline_markup(text: str) -> str:
    escaped = html.escape(text.strip(), quote=False)

    link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    escaped = link_pattern.sub(
        lambda m: (
            f'<link href="{html.escape(html.unescape(m.group(2)), quote=True)}" '
            f'color="#1F3A5F"><u>{m.group(1)}</u></link>'
        ),
        escaped,
    )

    bare_url = re.compile(r"(?<![\"'=])(https?://[^\s<]+)")

    def bare_repl(match: re.Match[str]) -> str:
        raw_url = match.group(1)
        url = html.unescape(raw_url).rstrip(".,;")
        suffix = raw_url[len(raw_url.rstrip(".,;")) :]
        href = html.escape(url, quote=True)
        return (
            f'<link href="{href}" color="#1F3A5F"><u>{safe_url_display(url)}</u></link>'
            + suffix
        )

    escaped = bare_url.sub(bare_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", escaped)
    return escaped


class ThesisDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs) -> None:
        super().__init__(filename, **kwargs)
        frame = Frame(
            LEFT,
            BOTTOM,
            CONTENT_W,
            CONTENT_H,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="content",
        )
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=draw_page)])
        self._bookmark_counter = 0

    def afterFlowable(self, flowable: Flowable) -> None:
        if not isinstance(flowable, Paragraph):
            return
        if flowable.style.name not in {"OE-H1", "OE-H2"}:
            return
        self._bookmark_counter += 1
        key = f"section-{self._bookmark_counter}"
        level = 0 if flowable.style.name == "OE-H1" else 1
        title = re.sub(r"<[^>]+>", "", flowable.getPlainText())
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(title, key, level=level, closed=level == 0)


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    canvas.setTitle("The Operator Economy — Evidence Base and 18-Month Signal System")
    canvas.setAuthor("Manav Thaker / The Operator Economy")
    canvas.setSubject(
        "What the evidence supports now, what remains a forecast, and what would falsify the thesis"
    )

    if doc.page == 1:
        canvas.setFillColor(BLUE_DARK)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

        canvas.setFillColor(GOLD)
        canvas.rect(0.74 * inch, PAGE_H - 1.13 * inch, 0.62 * inch, 0.055 * inch, stroke=0, fill=1)

        canvas.setFont("OEMono", 7.5)
        canvas.setFillColor(colors.Color(245 / 255, 240 / 255, 230 / 255, alpha=0.64))
        canvas.drawString(0.74 * inch, PAGE_H - 0.82 * inch, "THE OPERATOR ECONOMY  /  EVIDENCE BASE 01")

        canvas.setFillColor(PAPER)
        canvas.setFont("OEArial-Bold", 35)
        canvas.drawString(0.74 * inch, PAGE_H - 2.25 * inch, "THE OPERATOR")
        canvas.drawString(0.74 * inch, PAGE_H - 2.78 * inch, "ECONOMY")

        canvas.setFillColor(GOLD)
        canvas.setFont("OEArial-Bold", 15)
        canvas.drawString(0.76 * inch, PAGE_H - 3.32 * inch, "EVIDENCE BASE + 18-MONTH SIGNAL SYSTEM")

        subtitle = Paragraph(
            "What the evidence supports now, what remains a forecast, "
            "and what would falsify the thesis",
            ParagraphStyle(
                "cover-subtitle",
                fontName="OEArial",
                fontSize=15,
                leading=20,
                textColor=PAPER,
            ),
        )
        subtitle.wrapOn(canvas, 5.75 * inch, 1.2 * inch)
        subtitle.drawOn(canvas, 0.76 * inch, PAGE_H - 4.48 * inch)

        canvas.setStrokeColor(colors.Color(245 / 255, 240 / 255, 230 / 255, alpha=0.20))
        canvas.line(0.76 * inch, 1.42 * inch, PAGE_W - 0.76 * inch, 1.42 * inch)
        canvas.setFont("OEMono", 7.2)
        canvas.setFillColor(colors.Color(245 / 255, 240 / 255, 230 / 255, alpha=0.62))
        canvas.drawString(0.76 * inch, 1.13 * inch, "RESEARCH REPORT  /  24 AUGUST 2026")
        cover_credit = "MANAV THAKER  /  THEOPERATORECONOMY.COM"
        cover_right = PAGE_W - 0.76 * inch
        cover_y = 1.13 * inch
        canvas.drawRightString(cover_right, cover_y, cover_credit)
        domain = "THEOPERATORECONOMY.COM"
        domain_width = pdfmetrics.stringWidth(domain, "OEMono", 7.2)
        canvas.linkURL(
            "https://theoperatoreconomy.com",
            (cover_right - domain_width, cover_y - 2, cover_right, cover_y + 8),
            relative=0,
            thickness=0,
        )
    else:
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.45)
        canvas.line(LEFT, PAGE_H - 0.49 * inch, PAGE_W - RIGHT, PAGE_H - 0.49 * inch)
        canvas.line(LEFT, 0.42 * inch, PAGE_W - RIGHT, 0.42 * inch)

        canvas.setFont("OEMono", 6.4)
        canvas.setFillColor(INK_MUTED)
        canvas.drawString(LEFT, PAGE_H - 0.36 * inch, "THE OPERATOR ECONOMY  /  EVIDENCE BASE 01")
        canvas.drawRightString(
            PAGE_W - RIGHT,
            PAGE_H - 0.36 * inch,
            "EVIDENCE-LED THESIS  /  VERSION 1.0",
        )
        canvas.drawString(LEFT, 0.25 * inch, "24 AUG 2026")
        canvas.drawRightString(PAGE_W - RIGHT, 0.25 * inch, f"{doc.page:02d}")
    canvas.restoreState()


class Diagram(Flowable):
    def __init__(self, kind: str, width: float = CONTENT_W) -> None:
        heights = {
            "verdict": 122,
            "boundary": 240,
            "causal": 188,
            "evidence": 145,
            "ledgers": 215,
            "sufficiency": 185,
            "originality": 185,
            "two-bet": 214,
            "claim-ladder": 218,
            "cadence": 210,
            "category-test": 220,
        }
        super().__init__()
        self.kind = kind
        self.width = width
        self.height = heights.get(kind, 150)

    def draw_label(
        self,
        c,
        x,
        y,
        w,
        h,
        title,
        body="",
        fill=PAPER_LIGHT,
        stroke=RULE_STRONG,
        title_color=BLUE_DARK,
        body_color=INK_BODY,
    ):
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(0.7)
        c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
        title_p = Paragraph(
            f"<b>{html.escape(title)}</b>",
            ParagraphStyle(
                "diagram-title",
                fontName="OEArial",
                fontSize=8.1,
                leading=9.5,
                textColor=title_color,
                alignment=TA_CENTER,
            ),
        )
        title_p.wrapOn(c, w - 10, h - 8)
        title_p.drawOn(c, x + 5, y + h - 15)
        if body:
            body_p = Paragraph(
                html.escape(body),
                ParagraphStyle(
                    "diagram-body",
                    fontName="OEArial",
                    fontSize=6.8,
                    leading=8.1,
                    textColor=body_color,
                    alignment=TA_CENTER,
                ),
            )
            bw, bh = body_p.wrap(w - 12, h - 24)
            body_p.drawOn(c, x + 6, y + 7)

    def draw(self) -> None:
        c = self.canv
        c.saveState()
        if self.kind == "verdict":
            self.draw_verdict(c)
        elif self.kind == "boundary":
            self.draw_boundary(c)
        elif self.kind == "causal":
            self.draw_causal(c)
        elif self.kind == "evidence":
            self.draw_evidence(c)
        elif self.kind == "ledgers":
            self.draw_ledgers(c)
        elif self.kind == "sufficiency":
            self.draw_sufficiency(c)
        elif self.kind == "originality":
            self.draw_originality(c)
        elif self.kind == "two-bet":
            self.draw_two_bet(c)
        elif self.kind == "claim-ladder":
            self.draw_claim_ladder(c)
        elif self.kind == "cadence":
            self.draw_cadence(c)
        elif self.kind == "category-test":
            self.draw_category_test(c)
        c.restoreState()

    def arrow(self, c, x1, y1, x2, y2) -> None:
        c.setStrokeColor(BLUE)
        c.setFillColor(BLUE)
        c.setLineWidth(1.1)
        c.line(x1, y1, x2, y2)
        angle = 5
        if abs(x2 - x1) >= abs(y2 - y1):
            direction = 1 if x2 > x1 else -1
            c.line(x2, y2, x2 - direction * angle, y2 + 3)
            c.line(x2, y2, x2 - direction * angle, y2 - 3)
        else:
            direction = 1 if y2 > y1 else -1
            c.line(x2, y2, x2 + 3, y2 - direction * angle)
            c.line(x2, y2, x2 - 3, y2 - direction * angle)

    def draw_verdict(self, c) -> None:
        gap = 13
        w = (self.width - 2 * gap) / 3
        y = 21
        h = 83
        boxes = [
            ("THEORY", "Ideas, mechanisms, predictions. Cannot be owned by trademark."),
            ("SOURCE", "A consistent publication, product, or service can identify origin."),
            ("MOAT", "Evidence, data, adoption, correction, and useful instruments."),
        ]
        for i, (title, body) in enumerate(boxes):
            self.draw_label(c, i * (w + gap), y, w, h, title, body, fill=BLUE_LIGHT if i == 1 else PAPER_LIGHT)
            if i < 2:
                self.arrow(c, (i + 1) * w + i * gap + 3, y + h / 2, (i + 1) * (w + gap) - 3, y + h / 2)
        c.setFont("OEMono", 6.6)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 4, "A FILING DOES NOT TURN THE LEFT-HAND BOX INTO THE RIGHT-HAND BOX")

    def draw_boundary(self, c) -> None:
        cx = self.width / 2
        cy = 117
        core_w, core_h = 188, 86

        # Connect the perimeter to the edge of the core before drawing any
        # nodes. This keeps the relationship visible without running lines
        # through the core label.
        core_left = cx - core_w / 2
        core_right = cx + core_w / 2
        core_top = cy + core_h / 2
        core_bottom = cy - core_h / 2
        connectors = [
            (146, 174, cx - 58, core_top),
            (self.width - 146, 174, cx + 58, core_top),
            (133, 101, core_left, cy),
            (self.width - 133, 101, core_right, cy),
            (cx, 53, cx, core_bottom),
        ]
        for x1, y1, x2, y2 in connectors:
            self.arrow(c, x1, y1, x2, y2)

        c.setFillColor(BLUE)
        c.setStrokeColor(BLUE_DARK)
        c.roundRect(cx - core_w / 2, cy - core_h / 2, core_w, core_h, 7, stroke=1, fill=1)
        p = Paragraph(
            "<b>OPERATOR CORE</b><br/>promise · price · judgment<br/>cash · acceptance · accountability",
            ParagraphStyle(
                "core",
                fontName="OEArial",
                fontSize=9.4,
                leading=13,
                textColor=PAPER_LIGHT,
                alignment=TA_CENTER,
            ),
        )
        p.wrapOn(c, core_w - 18, core_h - 14)
        p.drawOn(c, cx - core_w / 2 + 9, cy - 22)

        items = [
            ("AI + SOFTWARE", 8, 174, 138, 42),
            ("SPECIALISTS", self.width - 146, 174, 138, 42),
            ("PLATFORMS", 8, 80, 125, 42),
            ("INSTITUTIONS", self.width - 133, 80, 125, 42),
            ("PAYMENTS · CLOUD · LOGISTICS · CAPITAL · LICENSED CAPACITY", 82, 13, self.width - 164, 40),
        ]
        for title, x, y, w, h in items:
            self.draw_label(c, x, y, w, h, title, fill=PAPER_LIGHT)
        c.setFont("OEMono", 6.5)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(cx, 226, "CAPACITY SITS ACROSS THE PERIMETER. CONSEQUENCE STAYS AT THE CORE.")

    def draw_causal(self, c) -> None:
        labels = [
            ("1", "GRANULAR CAPABILITY", "smaller purchasable units"),
            ("2", "VARIABLE COMMITMENT", "some fixed cost becomes metered"),
            ("3", "BOUNDARY CONTRACTS", "fewer functions stay permanent"),
            ("4", "VERIFY + COORDINATE", "core work changes"),
            ("5", "BOTTLENECK MOVES", "demand · trust · judgment"),
            ("6", "DEPENDENCY TRANSFERS", "vendor · platform · key person"),
            ("7", "VALUE CAPTURE CONTESTED", "rights · power · contracts"),
        ]
        top_y, bottom_y = 106, 18
        w, h, gap = 105, 60, 10
        x0 = 0
        positions = []
        for i in range(4):
            x = x0 + i * (w + gap)
            positions.append((x, top_y))
        for i in range(3):
            x = 57 + (2 - i) * (w + gap)
            positions.append((x, bottom_y))
        for i, ((num, title, body), (x, y)) in enumerate(zip(labels, positions)):
            self.draw_label(c, x, y, w, h, f"{num}  {title}", body, fill=BLUE_LIGHT if i in {2, 4} else PAPER_LIGHT)
            if i < len(labels) - 1:
                x2, y2 = positions[i + 1]
                if y == y2:
                    self.arrow(c, x + w + 2, y + h / 2, x2 - 2, y2 + h / 2)
                else:
                    self.arrow(c, x + w / 2, y - 2, x + w / 2, y2 + h + 2)

    def draw_evidence(self, c) -> None:
        data = [
            ("SUPPORTED", "Capabilities can lower minimum efficient scale in compatible tasks.", 0.74),
            ("SUPPORTED", "AI adoption and benefits are uneven; large firms often lead.", 0.82),
            ("PROVISIONAL", "AI-compatible industries may see higher post-ChatGPT entry.", 0.48),
            ("NOT SHOWN", "Most operator firms are solo, durable, or AI-created.", 0.12),
        ]
        y = 112
        for status, label, value in data:
            c.setFont("OEMono", 6.6)
            c.setFillColor(BLUE if status == "SUPPORTED" else (INK_MUTED if status == "PROVISIONAL" else NEGATIVE))
            c.drawString(0, y + 6, status)
            c.setFillColor(RULE)
            c.roundRect(74, y, self.width - 74, 17, 3, stroke=0, fill=1)
            c.setFillColor(BLUE if status != "NOT SHOWN" else NEGATIVE)
            c.roundRect(74, y, (self.width - 74) * value, 17, 3, stroke=0, fill=1)
            p = Paragraph(
                html.escape(label),
                ParagraphStyle(
                    "evidence-label",
                    fontName="OEArial",
                    fontSize=7.2,
                    leading=8.5,
                    textColor=INK_BODY,
                ),
            )
            p.wrapOn(c, self.width - 84, 24)
            p.drawOn(c, 79, y - 16)
            y -= 32

    def draw_ledgers(self, c) -> None:
        gap = 10
        top_w = (self.width - 2 * gap) / 3
        bottom_w = (self.width - gap) / 2
        h = 79
        entries = [
            ("ECONOMICS", "Normalized surplus\nMinimum viable customers\nCash, capital, reserves"),
            ("CONTROL", "Offer and price\nCustomer/data portability\nCash authority"),
            ("RESILIENCE", "Dependency blast radius\nReplacement time\nKey-person exposure"),
            ("POSITION", "Retention and workflow depth\nAccumulated learning\nEntrant threat map"),
            ("INCIDENCE", "Supplier labor conditions\nBenefits and volatility\nRisk shifted downstream"),
        ]
        positions = [
            (0, 106, top_w),
            (top_w + gap, 106, top_w),
            (2 * (top_w + gap), 106, top_w),
            (0, 17, bottom_w),
            (bottom_w + gap, 17, bottom_w),
        ]
        for i, ((title, body), (x, y, w)) in enumerate(zip(entries, positions)):
            self.draw_label(c, x, y, w, h, title, body.replace("\n", " · "), fill=BLUE_LIGHT if i in {1, 2, 4} else PAPER_LIGHT)
        c.setFont("OEMono", 6.6)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 4, "LEDGER FIRST. WEIGHTS ONLY AFTER OUTCOME CALIBRATION.")

    def draw_sufficiency(self, c) -> None:
        y = 88
        x1, x2 = 34, self.width - 28
        c.setStrokeColor(RULE_STRONG)
        c.setLineWidth(4)
        c.line(x1, y, x2, y)
        v = x1 + 115
        end = x2 - 98
        c.setStrokeColor(BLUE)
        c.setLineWidth(9)
        c.line(v, y, end, y)
        for x, label, sub in [
            (v, "V", "viability floor"),
            (end, "min(R, C)", "reachable demand or capacity"),
        ]:
            c.setStrokeColor(BLUE_DARK)
            c.setLineWidth(1.2)
            c.line(x, y - 15, x, y + 18)
            c.setFont("OEArial-Bold", 9)
            c.setFillColor(BLUE_DARK)
            c.drawCentredString(x, y + 24, label)
            c.setFont("OEArial", 6.8)
            c.setFillColor(INK_MUTED)
            c.drawCentredString(x, y - 28, sub)
        c.setFont("OEArial-Bold", 9.5)
        c.setFillColor(BLUE)
        c.drawCentredString((v + end) / 2, y + 3, "VIABILITY GATE")

        self.draw_label(c, 16, 124, 150, 43, "ECONOMIC TEST", "Can this pay for labor, risk, and reserves?", fill=PAPER_LIGHT)
        self.draw_label(c, self.width - 166, 124, 150, 43, "DESIGN TEST", "Can the chosen core serve it without breaking?", fill=PAPER_LIGHT)
        c.setFont("OEMono", 6.5)
        c.setFillColor(NEGATIVE)
        c.drawCentredString(self.width / 2, 28, "DEFENSIBILITY IS A SEPARATE THREAT SCREEN — SMALLNESS IS NOT A MOAT")

    def draw_originality(self, c) -> None:
        layers = [
            ("PROTECTABLE SOURCE ASSETS", "cleared mark · copyrighted expression · trade dress", 0.72),
            ("DISTINCTIVE SYNTHESIS", "boundary chain · dependency-adjusted independence · viability test", 0.84),
            ("PROPRIETARY EVIDENCE", "longitudinal data · calibrated instrument · case corpus", 0.94),
            ("ESTABLISHED LINEAGE", "firm boundaries · solo work · platforms · niches · switching costs", 1.0),
        ]
        y = 139
        for i, (title, body, ratio) in enumerate(layers):
            w = self.width * ratio
            x = (self.width - w) / 2
            fill = BLUE if i == 0 else (BLUE_LIGHT if i in {1, 2} else PAPER_DARK)
            title_color = PAPER_LIGHT if i == 0 else BLUE_DARK
            self.draw_label(c, x, y, w, 38, title, body, fill=fill, title_color=title_color)
            y -= 43
        c.setFont("OEMono", 6.4)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 2, "THE BOTTOM LAYER MUST BE CREDITED. THE TOP LAYERS MUST BE EARNED.")

    def draw_two_bet(self, c) -> None:
        gap = 12
        w = (self.width - 3 * gap) / 4
        y = 119
        h = 72
        nodes = [
            ("ENABLERS", "Cheaper, more divisible software, AI, infrastructure, and specialist capacity"),
            ("BET 1", "Comparable output with a smaller permanent core after all labor is counted"),
            ("BET 2", "The operator retains customer access, decision rights, recourse, and residual economics"),
            ("OUTCOME", "A durable, owner-controlled firm configuration becomes measurably more common"),
        ]
        for i, (title, body) in enumerate(nodes):
            x = i * (w + gap)
            fill = BLUE_LIGHT if i in {1, 2} else PAPER_LIGHT
            self.draw_label(c, x, y, w, h, title, body, fill=fill)
            if i < len(nodes) - 1:
                self.arrow(c, x + w + 2, y + h / 2, x + w + gap - 2, y + h / 2)

        fail_w = (self.width - gap) / 2
        self.draw_label(
            c,
            0,
            24,
            fail_w,
            58,
            "IF BET 1 FAILS",
            "Useful tools, but no durable boundary compression after contractors, owner time, and rework are counted",
            fill=PAPER_DARK,
            title_color=NEGATIVE,
        )
        self.draw_label(
            c,
            fail_w + gap,
            24,
            fail_w,
            58,
            "IF BET 2 FAILS",
            "A platform economy with fragmented labor: the operator carries accountability while suppliers capture the margin and control",
            fill=PAPER_DARK,
            title_color=NEGATIVE,
        )
        c.setFont("OEMono", 6.5)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 5, "TOOL CAPABILITY IS NECESSARY. OPERATOR CAPTURE IS THE DISCRIMINATING TEST.")

    def draw_claim_ladder(self, c) -> None:
        layers = [
            ("FACT", "Directly observed in a named source; method and limits travel with the claim", BLUE, PAPER_LIGHT),
            ("INFERENCE", "Best explanation that fits several facts; credible alternatives remain", BLUE_LIGHT, BLUE_DARK),
            ("FORECAST", "A dated prediction about what should become observable next", PAPER_DARK, BLUE_DARK),
            ("UNKNOWN", "Material question with no adequate current evidence", PAPER_LIGHT, NEGATIVE),
        ]
        y = 157
        widths = [1.0, 0.88, 0.76, 0.64]
        for (title, body, fill, title_color), ratio in zip(layers, widths):
            w = self.width * ratio
            x = (self.width - w) / 2
            self.draw_label(
                c,
                x,
                y,
                w,
                44,
                title,
                body,
                fill=fill,
                title_color=title_color,
                body_color=PAPER_LIGHT if title == "FACT" else INK_BODY,
            )
            y -= 49
        c.setFont("OEMono", 6.5)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 3, "CONVICTION COMES FROM NEVER SMUGGLING A FORECAST INTO THE FACT LAYER.")

    def draw_cadence(self, c) -> None:
        gap = 12
        w = (self.width - 2 * gap) / 3
        blocks = [
            ("MONTHLY", "Business applications\nEarly-career hiring\nProvider price and policy changes\nOperator-panel pulse"),
            ("QUARTERLY", "Core and total labor\nVerified workflow reliability\nDirect demand and dependency\nNormalized operator surplus"),
            ("SEMIANNUAL / ANNUAL", "Official firm adoption\nNonemployer counts and receipts\nSurvival and first-hire cohorts\nIndependent replication"),
        ]
        for i, (title, body) in enumerate(blocks):
            x = i * (w + gap)
            self.draw_label(c, x, 58, w, 126, title, body.replace("\n", " · "), fill=BLUE_LIGHT if i == 1 else PAPER_LIGHT)
            if i < 2:
                self.arrow(c, x + w + 2, 121, x + w + gap - 2, 121)
        c.setFont("OEMono", 6.5)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 34, "EVERY RELEASE UPDATES THE CLAIM LEDGER: SUPPORT · CONTRADICT · NO CHANGE · METHOD BREAK")
        c.drawCentredString(self.width / 2, 17, "NO SINGLE VENDOR SURVEY OR HERO CASE PROMOTES THE THESIS.")

    def draw_category_test(self, c) -> None:
        gap = 9
        w = (self.width - 2 * gap) / 3
        h = 78
        items = [
            ("1  BOUNDARY", "A crisp inclusion rule and explicit exclusions"),
            ("2  UNIT", "A countable actor, firm, transaction, or resource flow"),
            ("3  MECHANISM", "A causal account that differs from adjacent categories"),
            ("4  MEASUREMENT", "Repeated data, denominators, and uncertainty"),
            ("5  INSTITUTION", "Products, research, cases, and a correction cadence"),
            ("6  FALSIFIERS", "Conditions under which the category must narrow or die"),
        ]
        for i, (title, body) in enumerate(items):
            row = 1 - (i // 3)
            col = i % 3
            x = col * (w + gap)
            y = 25 + row * (h + 10)
            self.draw_label(c, x, y, w, h, title, body, fill=BLUE_LIGHT if i in {2, 3, 5} else PAPER_LIGHT)
        c.setFont("OEMono", 6.5)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(self.width / 2, 4, "A MEMORABLE NAME IS NOT ON THE LIST.")


def parse_table(lines: list[str], styles: dict[str, ParagraphStyle]) -> LongTable:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
            continue
        rows.append(cells)
    ncols = max(len(row) for row in rows)
    rows = [row + [""] * (ncols - len(row)) for row in rows]

    rendered = []
    for r_idx, row in enumerate(rows):
        style = styles["table_header"] if r_idx == 0 else styles["table"]
        rendered.append([Paragraph(inline_markup(cell), style) for cell in row])

    weights = {
        2: [0.29, 0.71],
        3: [0.22, 0.39, 0.39],
        4: [0.19, 0.27, 0.28, 0.26],
        5: [0.15, 0.20, 0.22, 0.22, 0.21],
    }.get(ncols, [1 / ncols] * ncols)
    col_widths = [CONTENT_W * value for value in weights]
    table = LongTable(
        rendered,
        colWidths=col_widths,
        repeatRows=1,
        splitByRow=1,
        hAlign="LEFT",
    )
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), PAPER_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE_STRONG),
    ]
    for r_idx in range(1, len(rendered)):
        commands.append(
            ("BACKGROUND", (0, r_idx), (-1, r_idx), PAPER_LIGHT if r_idx % 2 else PAPER_DARK)
        )
    table.setStyle(TableStyle(commands))
    return table


def parse_markdown(source: str, styles: dict[str, ParagraphStyle]) -> list[Flowable]:
    lines = source.splitlines()

    # Skip front matter and the cover-source block through the first page break.
    if lines and lines[0].strip() == "---":
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        lines = lines[end + 1 :]
    first_break = next(
        (i for i, line in enumerate(lines) if line.strip() == "<!-- pagebreak -->"),
        None,
    )
    if first_break is not None:
        lines = lines[first_break + 1 :]

    story: list[Flowable] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped:
            i += 1
            continue

        if stripped == "<!-- pagebreak -->":
            story.append(PageBreak())
            i += 1
            continue

        diagram_match = re.fullmatch(r"<!-- diagram:([a-z-]+) -->", stripped)
        if diagram_match:
            story.extend([Spacer(1, 5), Diagram(diagram_match.group(1)), Spacer(1, 10)])
            i += 1
            continue

        if stripped == "---":
            story.extend(
                [
                    Spacer(1, 3),
                    HRFlowable(width="100%", thickness=0.6, color=RULE_STRONG),
                    Spacer(1, 6),
                ]
            )
            i += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            style = styles["h1"] if level == 1 else (styles["h2"] if level == 2 else styles["h3"])
            story.append(Paragraph(inline_markup(title), style))
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            story.extend([Spacer(1, 3), parse_table(table_lines, styles), Spacer(1, 9)])
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            story.append(Paragraph(inline_markup(" ".join(quote_lines)), styles["quote"]))
            continue

        if re.match(r"^[-*]\s+", stripped):
            items = []
            item_texts = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item_text = re.sub(r"^\s*[-*]\s+", "", lines[i]).strip()
                item_texts.append(item_text)
                items.append(
                    ListItem(
                        Paragraph(inline_markup(item_text), styles["bullet"]),
                        leftIndent=11,
                    )
                )
                i += 1
            bullet_list = ListFlowable(
                items,
                bulletType="bullet",
                start="circle",
                leftIndent=17,
                bulletFontName="OEArial",
                bulletFontSize=7,
                bulletColor=BLUE,
                spaceAfter=7,
            )
            if len(items) <= 8 and sum(map(len, item_texts)) <= 750:
                story.append(KeepTogether([bullet_list]))
            else:
                story.append(bullet_list)
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            item_texts = []
            start = int(stripped.split(".", 1)[0])
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                item_text = re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip()
                item_texts.append(item_text)
                items.append(
                    ListItem(
                        Paragraph(inline_markup(item_text), styles["bullet"]),
                        leftIndent=13,
                    )
                )
                i += 1
            numbered_list = ListFlowable(
                items,
                bulletType="1",
                start=start,
                leftIndent=21,
                bulletFontName="OEMono",
                bulletFontSize=7,
                bulletColor=BLUE,
                spaceAfter=7,
            )
            if len(items) <= 8 and sum(map(len, item_texts)) <= 750:
                story.append(KeepTogether([numbered_list]))
            else:
                story.append(numbered_list)
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith("#")
                or nxt.startswith("|")
                or nxt.startswith(">")
                or nxt == "---"
                or nxt.startswith("<!--")
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
            ):
                break
            paragraph_lines.append(nxt)
            i += 1
        text = " ".join(paragraph_lines)
        style = styles["caption"] if text.startswith("Source:") else styles["body"]
        story.append(Paragraph(inline_markup(text), style))

    return story


def build() -> None:
    register_fonts()
    styles = build_styles()
    source = SOURCE.read_text(encoding="utf-8")
    story = [Spacer(1, CONTENT_H - 1), PageBreak()]
    story.extend(parse_markdown(source, styles))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = ThesisDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="The Operator Economy — Evidence Base and 18-Month Signal System",
        author="Manav Thaker / The Operator Economy",
    )
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:
        print(f"PDF build failed: {exc}", file=sys.stderr)
        raise
