#!/usr/bin/env python3
"""EP009 S17 part d (seg060): 40-room row, six properties not a share, the route you can drive.
Fix round 1: frame 0 is seg058's revised last frame (replayed from scenes/seg057__seg058/tools/build.py).
The six inns and the route to You are already on screen from S17a, so the route is re-inked rather than drawn new.
Generates ../index.html; scene() is imported by seg061__seg062."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa
from r1lib import TL2, page2, load_scene

MI, MO = 982.875, 1008.333333
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)


def scene():
    prev = load_scene('seg057__seg058')
    c = lambda w, o=0.0: cue(w, MI, o)
    r = Rough(6060)
    X = []
    X.append(label(r, 'row40', 660, 372, 580, 92,
                   [('6 × 40-room properties × $1,250 × 12', 'small', 20, 32), ('$90,000 a year of retainer', 'fig', 20, 76)], ear=16)
             .replace('class="fig"', 'class="fig" style="font-size:34px"')
             .replace('</g>', '<text class="label" x="1068" y="448" style="font-size:22px">before costs</text></g>'))
    X.append('<text id="sixl" class="hide label" x="715" y="340" text-anchor="middle">six properties</text>')
    EX, EY, EW, EH = 300, 372, 680, 216
    X.append(f'<g id="ev" class="hide"><path d="M{EX} {EY}L{EX+EW} {EY}L{EX+EW} {EY+EH}L{EX} {EY+EH}Z" fill="{SHEET}"/>'
             f'<path d="{r.rect(EX,EY,EW,EH)}" class="steel"/>'
             f'<text class="kicker" x="{EX+28}" y="{EY+40}">OBSERVED · AMERICAN HOTEL &amp; LODGING ASSOCIATION</text>'
             f'<path d="M{EX+28} {EY+54}L{EX+EW-28} {EY+54}" class="light"/></g>')
    X.append(f'<text id="evfig" class="hide fig" x="{EX+28}" y="{EY+120}" style="font-size:60px">33,200+</text>')
    X.append(f'<text id="evline" class="hide label" x="{EX+270}" y="{EY+112}" style="font-size:25px">small-business lodging properties</text>')
    X.append(f'<text id="evq" class="hide small" x="{EX+28}" y="{EY+176}">AHLA definition, not a room band</text>')
    X.append(f'<g id="nc" class="hide"><path d="{r.rect(EX,606,EW,58)}" class="dash"/>'
             f'<text class="label" x="{EX+EW/2}" y="644" text-anchor="middle" style="font-size:24px">in this band: not counted</text></g>')
    X.append('<text id="rcpt" class="hide tiny" x="640" y="700" text-anchor="middle" style="font-size:15px">AHLA "Our industry", 64,000-plus properties, 33,200-plus small-business properties, undated, C015</text>')
    X.append(f'<path id="route2" class="hide" d="M170 292C420 289 800 295 1180 292" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    X.append('<text id="illus" class="hide small" x="170" y="340">a route you can drive · illustrative</text>')

    C = {k: c(w) for k, w in dict(six='W002733', ninety='W002741', six2='W002749', props='W002750', not_='W002751',
                                  the='W002755', thirty='W002760', nobody='W002771', you='W002780', route='W002789').items()}
    tl = TL2()
    tl.slide('#row40', C['six'], x=0)
    tl.js("t.set('#row40 .fig, #row40 .label',{autoAlpha:0},0);")
    tl.fade('#row40 .fig', C['ninety']); tl.fade('#row40 .label', C['ninety'] + .6)
    # everything except the six inns on their route recedes
    gone = ['colb', 'cols', 'sul', 'hb', 'bars', 'figb', 'figs', 'row20', 'row40', 'foot']
    tl.js("t.to('" + ','.join('#' + g for g in gone) + f"',{{autoAlpha:0,duration:.5,ease:'power1.inOut'}},{C['six2']});")
    tl.fade('#sixl', C['props'] + .2)
    # the observed count, marked as observed so it does not read as part of the model
    tl.appear('#ev', C['the'])
    tl.fade('#evfig', C['thirty'])
    tl.fade('#evline', C['thirty'] + .8)
    tl.fade('#evq', C['thirty'] + 1.6)
    tl.appear('#rcpt', C['the'])
    tl.fade('#nc', C['nobody'])
    # six owners who say yes, on a route you can drive
    tl.js(f"t.to('#youl2',{{scale:1.15,svgOrigin:'110 222',duration:.3,yoyo:true,repeat:1,ease:'power1.inOut'}},{C['you']});")
    tl.out('#sixl', C['route'] - .4, .3)
    tl.draw('#route2', C['route'] - .3, 1.1)
    tl.fade('#illus', C['route'] + .3)
    body = prev['body'] + '\n' + '\n'.join(X)
    return dict(body=body, lines=tl.lines, cues=C, css=prev['css'], defs_ids=prev['defs_ids'], dur=DUR, tl=tl,
                prev_lines=[prev['lines']])


if __name__ == '__main__':
    sc = scene()
    html = page2("S17 the operator's arithmetic, part d", 's17d-root', 'ep009-s17d', DUR, sc['body'],
                 kit_defs(sc['defs_ids']), sc['tl'], sc['cues'], prev_lines=sc['prev_lines'], css=sc['css'])
    (HERE.parent / 'index.html').write_text(html)
    print('wrote', DUR)
