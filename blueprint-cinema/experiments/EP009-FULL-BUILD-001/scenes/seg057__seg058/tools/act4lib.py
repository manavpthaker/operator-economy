"""Shared generator helpers for EP009 act 4 model scenes (copied into each project's tools/)."""
import json
import random
import subprocess
from pathlib import Path

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
BUILD = REPO / 'blueprint-cinema/experiments/EP009-FULL-BUILD-001'
KITDEFS = BUILD / 'world-kit/tools/kit_defs.py'
WORDS = REPO / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/word-transcript.json'

INK, STEEL, MUTED, OXIDE, SHEET, CARD, PAPER = '#173530', '#586D74', '#33464C', '#B5482F', '#FBF8F1', '#EDE5D6', '#F5F0E6'

_W = None


def word(wid):
    global _W
    if _W is None:
        _W = {w['w_id']: w for w in json.load(open(WORDS))['words']}
    return _W[wid]


def cue(wid, master_in, off=0.0):
    return round(word(wid)['start'] - master_in + off, 3)


def kit_defs(ids):
    out = subprocess.run(['python3', str(KITDEFS), 'defs', *ids], capture_output=True, text=True, check=True).stdout
    # one line per object
    blocks, cur = [], []
    for line in out.splitlines():
        cur.append(line)
        if line == '</g>':
            blocks.append(''.join(cur))
            cur = []
    return '\n'.join(blocks)


class Rough:
    """Workshop construction: short partial strokes with gaps and small seeded offsets."""

    def __init__(self, seed):
        self.r = random.Random(seed)

    def j(self, a=1.2):
        return round(self.r.uniform(-a, a), 1)

    def seg(self, x1, y1, x2, y2, gap=True):
        # split long lines into two strokes with a gap, like the kit
        L = abs(x2 - x1) + abs(y2 - y1)
        if gap and L > 120:
            f = self.r.uniform(.42, .58)
            g = 6 / L
            mx1, my1 = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
            mx2, my2 = x1 + (x2 - x1) * (f + g), y1 + (y2 - y1) * (f + g)
            return (f'M{x1+self.j()} {y1+self.j()}L{mx1+self.j(.6)} {my1+self.j(.6)}'
                    f'M{mx2+self.j(.6)} {my2+self.j(.6)}L{x2+self.j()} {y2+self.j()}')
        return f'M{x1+self.j()} {y1+self.j()}L{x2+self.j()} {y2+self.j()}'

    def rect(self, x, y, w, h):
        return ''.join([self.seg(x, y, x + w, y), self.seg(x + w, y + 2, x + w, y + h),
                        self.seg(x + w - 2, y + h, x, y + h), self.seg(x, y + h - 2, x, y + 1)])

    def label_shape(self, x, y, w, h, ear=14):
        """Dog-eared label (kit-card-small grammar)."""
        fill = f'M{x} {y}L{x+w-ear} {y}L{x+w} {y+ear}L{x+w} {y+h}L{x} {y+h}Z'
        ink = ''.join([self.seg(x, y, x + w - ear, y), self.seg(x + w, y + ear, x + w, y + h),
                       self.seg(x + w - 1, y + h, x, y + h), self.seg(x, y + h - 1, x, y + 1)])
        ear_p = f'M{x+w-ear} {y}L{x+w-ear} {y+ear}L{x+w} {y+ear}'
        return fill, ink, ear_p


def label(r, gid, x, y, w, h, lines, cls='hide', stroke=STEEL, ear=14, extra=''):
    """lines: list of (text, css class, dx, dy-baseline)"""
    fill, ink, ear_p = r.label_shape(x, y, w, h, ear)
    t = ''.join(f'<text class="{c}" x="{x+dx}" y="{y+dy}">{s}</text>' for s, c, dx, dy in lines)
    return (f'<g id="{gid}" class="{cls}"{extra}><path d="{fill}" fill="{SHEET}" stroke="none"/>'
            f'<path d="{ink}" stroke="{stroke}" stroke-width="2" fill="none" stroke-linecap="round"/>'
            f'<path d="{ear_p}" class="light"/>{t}</g>')


HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
@font-face{{font-family:Boska;src:url('public/fonts/boska-700.woff2');font-weight:700}}
@font-face{{font-family:Supreme;src:url('public/fonts/supreme-400.woff2');font-weight:400}}
@font-face{{font-family:Supreme;src:url('public/fonts/supreme-500.woff2');font-weight:500}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1280px;height:720px;overflow:hidden}}
#{root}{{position:relative;width:1280px;height:720px;overflow:hidden;background:#F5F0E6}}
svg.stage{{position:absolute;inset:0;width:1280px;height:720px;overflow:hidden}}
.kit-route{{stroke:#586D74;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round}}
.kit-route-dashed{{stroke:#586D74;stroke-width:2.5;stroke-dasharray:10 8;fill:none;stroke-linecap:round}}
.kit-pay{{stroke:#173530;stroke-width:4;fill:none;stroke-linecap:round}}
.light{{stroke:#586D74;stroke-width:1.3;fill:none;stroke-linecap:round;stroke-linejoin:round}}
.inkl{{stroke:#173530;stroke-width:3;fill:none;stroke-linecap:round;stroke-linejoin:round}}
.steel{{stroke:#586D74;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}}
.dash{{stroke:#586D74;stroke-width:2;stroke-dasharray:9 7;fill:none;stroke-linecap:round}}
.label{{font-family:Supreme,sans-serif;fill:#173530;font-size:27px;font-weight:500}}
.lab{{font-family:Supreme,sans-serif;fill:#173530;font-size:22px;font-weight:500}}
.small{{font-family:Supreme,sans-serif;fill:#33464C;font-size:20px;font-weight:400}}
.tiny{{font-family:Supreme,sans-serif;fill:#33464C;font-size:17px;font-weight:400}}
.kicker{{font-family:Supreme,sans-serif;fill:#33464C;font-size:18px;font-weight:500;letter-spacing:2px}}
.fig{{font-family:Boska,serif;fill:#173530;font-size:40px;font-weight:700}}
.hide{{visibility:hidden;opacity:0}}
.head{{position:absolute;left:0;right:0;text-align:center;margin:0;font:700 50px/1.06 Boska,serif;color:#173530;visibility:hidden;opacity:0}}
</style><script src="public/vendor/gsap.min.js"></script></head><body>
"""


class TL:
    def __init__(self):
        self.lines = []

    def fade(self, sel, at, d=10 / 24, y=8):
        self.lines.append(f"t.fromTo('{sel}',{{autoAlpha:0,y:{y}}},{{autoAlpha:1,y:0,duration:{d:.3f},ease:'power1.out'}},{at});")

    def appear(self, sel, at, d=10 / 24):
        self.lines.append(f"t.fromTo('{sel}',{{autoAlpha:0}},{{autoAlpha:1,duration:{d:.3f},ease:'power1.out'}},{at});")

    def slide(self, sel, at, x=24, d=.45):
        self.lines.append(f"t.fromTo('{sel}',{{autoAlpha:0,x:{x}}},{{autoAlpha:1,x:0,duration:{d},ease:'power2.out'}},{at});")

    def out(self, sel, at, d=.35):
        self.lines.append(f"t.to('{sel}',{{autoAlpha:0,duration:{d},ease:'power1.inOut'}},{at});")

    def to(self, sel, at, props, d=.5, ease='power2.inOut'):
        self.lines.append(f"t.to('{sel}',{{{props},duration:{d},ease:'{ease}'}},{at});")

    def set(self, sel, at, props):
        self.lines.append(f"t.set('{sel}',{{{props}}},{at});")

    def draw(self, sel, at, d=.6):
        self.lines.append(f"draw('{sel}',{at},{d});")

    def js(self, s):
        self.lines.append(s)


def page(title, root, comp_id, duration, svg_body, defs, tl, cues, extra_html=''):
    js = '\n'.join(tl.lines)
    return (HEAD.format(title=title, root=root)
            + f'<div id="{root}" data-composition-id="{comp_id}" data-start="0" data-duration="{duration}" data-width="1280" data-height="720" data-fps="24">\n'
            + '<svg class="stage" viewBox="0 0 1280 720" role="img" aria-label="' + title + '">\n<defs>\n' + defs + '\n</defs>\n'
            + svg_body + '\n</svg>\n' + extra_html
            + f'<audio id="{root}-narration" src="public/audio/narration.wav" data-start="0" data-duration="{duration}" data-media-start="0" data-track-index="100" data-volume="1"></audio>\n'
            + '</div>\n<script>\nwindow.__timelines=window.__timelines||{};\nconst t=gsap.timeline({paused:true});\n'
            + 'const C=' + json.dumps(cues) + ';\n'
            + "const draw=(sel,at,d)=>{document.querySelectorAll(sel).forEach(p=>{const L=p.getTotalLength();t.set(p,{autoAlpha:1,strokeDasharray:L,strokeDashoffset:L},at);t.to(p,{strokeDashoffset:0,duration:d,ease:'power1.inOut'},at);});};\n"
            + js + f"\nt.set({{}},{{}},{duration});\nwindow.__timelines['{comp_id}']=t;\n</script></body></html>\n")
