#!/usr/bin/env python3
"""Write world-kit/showcase/index.html: three 1280x720 held frames of kit objects.

Frame A (0-1 s): people and places. Frame B (1-2 s): paper objects and states.
Frame C (2-3 s): the kit staged in the accepted EP007 R57 S13ab layout, for the side-by-side comparison.
Kit defs are injected by kit_defs.py between the KIT markers.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOW = HERE.parent / "showcase"


def use(i, x, y, s=1.0, extra=""):
    sc = f" scale({s})" if s != 1 else ""
    return f'<use href="#{i}" transform="translate({x},{y}){sc}"{extra}/>'


def cap(x, y, t, anchor="middle"):
    return f'<text class="cap" x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'


A = [
    '<text class="kick" x="40" y="44">WORLD KIT A · PEOPLE AND PLACES</text>',
    # the inn with one lit window and its live own page
    use("kit-inn", 40, 84), use("kit-inn-window-lit", 40 + 38 + 3 * 42, 84 + 88), use("kit-inn-own-page", 40 + 372, 84 + 214),
    cap(280, 414, "kit-inn · kit-inn-window-lit · kit-inn-own-page"),
    # the booking site with listings and its audience
    use("kit-booking-site", 570, 84),
    *[use("kit-listing-card-inn" if i == 2 else "kit-listing-card", 570 + 58 + 64 * i - 17, 84 + 168) for i in range(6)],
    use("kit-crowd", 660, 392),
    cap(790, 72, "kit-booking-site · kit-listing-card(-inn)"), cap(790, 512, "kit-crowd"),
    use("kit-inn-mini", 1030, 84), cap(1150, 262, "kit-inn-mini"),
    use("kit-hotel-large", 1044, 290), cap(1154, 528, "kit-hotel-large"),
    use("kit-booking-site-simple", 1076, 560), cap(1156, 708, "kit-booking-site-simple"),
    use("kit-inn-own-page-dashed", 580, 600), cap(608, 690, "own-page-dashed"),
    # people at 0.7
    '<g transform="translate(30,466) scale(.7)">' + use("kit-desk", 0, 250) + use("kit-innkeeper", 120, 192) + '</g>',
    cap(118, 506, "kit-innkeeper · kit-desk"),
    use("kit-guest", 290, 606, .7), cap(290, 664, "kit-guest"),
    use("kit-person", 400, 606, .7), cap(400, 664, "kit-person"),
    use("kit-practice-figure", 510, 606, .7), cap(516, 664, "kit-practice-figure"),
    use("kit-table", 690, 620, .6), cap(760, 690, "kit-table"),
    use("kit-empty-place", 880, 560, .7), cap(932, 700, "kit-empty-place"),
]

B = [
    '<text class="kick" x="40" y="36">WORLD KIT B · PAPER, TAGS, STATES</text>',
    use("kit-ceiling-slip-blank", 30, 56, .6), cap(120, 340, "slip-blank"),
    use("kit-ceiling-slip-filled", 222, 56, .6), cap(312, 340, "slip-filled"),
    use("kit-ceiling-line-ghost", 430, 92), use("kit-ceiling-line", 430, 132, extra=' color="#173530"'),
    use("kit-retainer-tag", 560, 146), cap(610, 62, "kit-ceiling-line(-ghost) · kit-retainer-tag"),
    use("kit-relay-field", 430, 230, .8), cap(600, 318, "kit-relay-field"),
    '<g transform="translate(830,52) scale(.72)">' + use("kit-job-findable", 0, 0) + '</g>',
    '<g transform="translate(1030,52) scale(.72)">' + use("kit-job-bookable", 0, 0) + '</g>',
    '<g transform="translate(830,200) scale(.72)">' + use("kit-job-remembered", 0, 0) + '</g>',
    use("kit-practice-card", 1060, 196, .66), cap(1110, 330, "kit-practice-card"),
    cap(920, 42, "kit-job-findable"), cap(1120, 42, "kit-job-bookable"), cap(920, 344, "kit-job-remembered"),
    # registration cards: own email and relay
    '<g transform="translate(30,372) scale(.62)">' + use("kit-registration-card", 0, 0) + use("kit-text-own-email", 34, 164) + '</g>',
    '<g transform="translate(270,372) scale(.62)">' + use("kit-registration-card", 0, 0) + use("kit-text-relay", 34, 163) + '</g>',
    cap(250, 514, "kit-registration-card + kit-text-own-email / kit-text-relay"),
    use("kit-reservation-record", 510, 350, .42), cap(636, 500, "kit-reservation-record"),
    use("kit-report-slip", 780, 372, .5), use("kit-report-slip-before-after", 990, 372, .5),
    cap(875, 490, "kit-report-slip"), cap(1085, 490, "report-slip-before-after"),
    use("kit-card-small", 1196, 380, .38),
    # row 3
    use("kit-guest-book-closed", 30, 552, .8), cap(84, 660, "book-closed"),
    use("kit-guest-book-open", 150, 540, .9), use("kit-guest-book-entries", 150, 540, .9), use("kit-signature", 150, 540, .9),
    cap(240, 670, "book-open + entries + signature"),
    use("kit-guest-book-open-dashed", 350, 540, .9), cap(440, 670, "book-open-dashed"),
    use("kit-commission-tag", 572, 548), use("kit-commission-tag", 650, 548), use("kit-commission-tag-empty", 728, 548),
    use("kit-commission-tag", 806, 548), use("kit-tag-service", 806, 548),
    cap(700, 610, "commission-tag · empty · + service"),
    use("kit-commission-tag-layers", 560, 626, .36), cap(690, 690, "tag-layers"),
    use("kit-rate-tag", 880, 552), cap(908, 610, "rate-tag"),
    use("kit-checkbox-empty", 752, 648), use("kit-checkbox-checked", 790, 648, extra=' color="#173530"'),
    cap(790, 700, "checkboxes"),
    use("kit-thank-you-note", 960, 540, .7), use("kit-seasonal-note", 1060, 540, .7),
    use("kit-envelope", 960, 616, .8), use("kit-leaf", 1010, 612, .9),
    use("kit-phone", 1160, 530, .62), use("kit-calendar-leaf", 1048, 610, .5), use("kit-wifi-sign", 1116, 624, .5),
    use("kit-wall-hook", 1220, 640), use("kit-boundary", 1250, 520, .6, extra=' color="#B5482F"'),
    cap(1060, 712, "notes · envelope · leaf · phone · calendar · wifi · hook · boundary"),
    use("kit-sheet", 880, 628, .22), use("kit-timeline-line", 30, 700, .5), use("kit-tick", 255, 700, .6),
    use("kit-route-solid", 480, 706, .5), use("kit-route-dashed", 590, 706, .5),
]

C = [
    '<path class="light" d="M92 128L736 124L740 664L90 668Z"/><text class="kicker" x="112" y="160">THE FRONT DESK</text>',
    use("kit-desk", 130, 450), use("kit-innkeeper", 250, 392),
    '<text class="label" x="250" y="270" text-anchor="middle">Innkeeper</text>',
    use("kit-guest", 600, 236, .6), '<text class="label" x="530" y="232" text-anchor="end">Guest</text>',
    use("kit-person", 600, 360, .6), '<text class="label" x="530" y="356" text-anchor="end">A traveller</text>',
    use("kit-practice-figure", 600, 484, .6), '<text class="label" x="530" y="480" text-anchor="end">A practice</text>',
    use("kit-guest-book-closed", 180, 560, .7),
    use("kit-inn", 820, 330, .625), '<text class="label" x="970" y="560" text-anchor="middle">The inn</text>',
    use("kit-booking-site-simple", 1090, 100, .9), '<text class="label" x="1162" y="90" text-anchor="middle">Booking site</text>',
    '<path class="steel" stroke-dasharray="10 8" d="M1100 222C1060 262 1030 300 1010 334"/>',
    '<path class="ink" d="M650 500C700 520 760 470 812 432"/>',
]


def panel(pid, body, label):
    return (f'<div class="panel" id="{pid}"><svg viewBox="0 0 1280 720" role="img" aria-label="{label}">\n'
            + "\n".join(body) + "\n</svg></div>")


HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>EP009 world kit showcase</title>
<style>
@font-face{font-family:Boska;src:url('public/fonts/boska-700.woff2');font-weight:700}
@font-face{font-family:Supreme;src:url('public/fonts/supreme-400.woff2');font-weight:400}
@font-face{font-family:Supreme;src:url('public/fonts/supreme-500.woff2');font-weight:500}
*{box-sizing:border-box}html,body{margin:0;width:1280px;height:720px;overflow:hidden}
#wk-root{position:relative;width:1280px;height:720px;overflow:hidden;background:#F5F0E6;color:#173530}
svg{position:absolute;inset:0;width:1280px;height:720px;overflow:visible}
#wk-defs{width:0;height:0}
.panel{position:absolute;inset:0;visibility:hidden;opacity:0}
.ink{stroke:#173530;stroke-width:3;fill:none;stroke-linecap:round;stroke-linejoin:round}
.steel{stroke:#586D74;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round}
.light{stroke:#586D74;stroke-width:1.3;fill:none;stroke-linecap:round;stroke-linejoin:round}
.label{font-family:Supreme,sans-serif;fill:#173530;font-size:27px;font-weight:500}
.kicker{font-family:Supreme,sans-serif;fill:#33464C;font-size:21px;font-weight:500;letter-spacing:2px}
.kick{font-family:Supreme,sans-serif;fill:#33464C;font-size:16px;font-weight:500;letter-spacing:2px}
.cap{font-family:Supreme,sans-serif;fill:#586D74;font-size:14px;font-weight:400}
</style><script src="public/vendor/gsap.min.js"></script></head><body>
<div id="wk-root" data-composition-id="ep009-world-kit-showcase" data-start="0" data-duration="3" data-width="1280" data-height="720" data-fps="24">
<svg id="wk-defs" aria-hidden="true"><defs>
<!-- KIT:DEFS:BEGIN -->
<!-- KIT:DEFS:END -->
</defs></svg>
%PANELS%
</div>
<script>
const t=gsap.timeline({paused:true});
// Three held frames, one second each.
t.set('#wk-a',{autoAlpha:1},0);
t.set('#wk-a',{autoAlpha:0},1); t.set('#wk-b',{autoAlpha:1},1);
t.set('#wk-b',{autoAlpha:0},2); t.set('#wk-c',{autoAlpha:1},2);
t.set('#wk-c',{autoAlpha:1},2.99);
window.__timelines['ep009-world-kit-showcase']=t;
</script></body></html>
"""


def main():
    panels = "\n".join([
        panel("wk-a", A, "World kit A: people and places."),
        panel("wk-b", B, "World kit B: paper objects, tags and states."),
        panel("wk-c", C, "World kit C: the kit staged in the accepted EP007 R57 S13ab layout."),
    ])
    out = SHOW / "index.html"
    out.write_text(HTML.replace("%PANELS%", panels))
    subprocess.run([sys.executable, str(HERE / "kit_defs.py"), "inject", str(out)], check=True)


if __name__ == "__main__":
    main()
