#!/usr/bin/env python3
"""EP009 S17 part d (seg060): 40-room row, six properties not a share, route to You. Generates ../index.html.
Frame 0 restores seg058's last frame by re-running the seg057__seg058 layout and applying its end opacities."""
import re
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa

MI, MO = 982.875, 1008.333333
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
c = lambda w, o=0.0: cue(w, MI, o)

# ---- inherited S17ab layout, same seed and geometry ----
src_path = HERE.parent.parent / 'seg057__seg058/tools/build.py'
src = src_path.read_text().split("body = '\\n'.join(S)")[0]
ns = {'__file__': str(src_path), '__name__': 's17ab_layout'}
exec(compile(src, str(src_path), 'exec'), ns)
S = ns['S']
body = '\n'.join(S)

END = {  # seg058 last-frame state
    1.0: ['band', 'ul1', 'ul2', 'foot', 'head', 'inns', 'row20'],
    .45: ['p1', 'p2', 'p3', 'p23', 'p4', 'l1', 'l2', 'l3', 'hrs8', 'cap8', 'capa'],
    .5: ['colb', 'cols', 'stag', 'barb', 'barbl', 'bars', 'figb', 'figbx', 'figs', 'figsx', 'l4', 'l4rule', 'l5', 'p5', 'p5n'],
}
r = Rough(6060)
X = []
# 40-room row beside the 20-room row, same size
X.append(label(r, 'row40', 650, 606, 600, 84,
               [('6 × 40-room properties × $1,250 × 12', 'small', 20, 30), ('$90,000 a year of retainer', 'fig', 20, 70)], ear=16)
         .replace('class="fig"', 'class="fig" style="font-size:32px"')
         .replace('</g>', '<text class="lab" x="1062" y="676">before costs</text></g>'))
X.append('<text id="sixl" class="hide lab" x="355" y="258" text-anchor="middle">six properties</text>')
# evidence tag (R53 card grammar, compact)
EX, EY, EW, EH = 700, 150, 550, 262
X.append(f'<g id="ev" class="hide"><path d="M{EX} {EY}L{EX+EW} {EY}L{EX+EW} {EY+EH}L{EX} {EY+EH}Z" fill="{SHEET}"/>'
         f'<path d="{r.rect(EX,EY,EW,EH)}" class="steel"/>'
         f'<text class="kicker" x="{EX+28}" y="{EY+42}">AMERICAN HOTEL &amp; LODGING ASSOCIATION</text>'
         f'<path d="M{EX+28} {EY+58}L{EX+EW-28} {EY+58}" class="light"/></g>')
X.append(f'<text id="evfig" class="hide fig" x="{EX+28}" y="{EY+132}" style="font-size:64px">33,200+</text>')
X.append(f'<text id="evline" class="hide lab" x="{EX+28}" y="{EY+178}" style="font-size:25px">small-business lodging properties</text>')
X.append(f'<text id="evq" class="hide small" x="{EX+28}" y="{EY+226}">AHLA definition, not a room band</text>')
X.append(f'<g id="nc" class="hide"><path d="{r.rect(EX,448,EW,74)}" class="dash"/>'
         f'<text class="lab" x="{EX+EW/2}" y="494" text-anchor="middle">in this band: not counted</text></g>')
X.append('<text id="rcpt" class="hide tiny" x="700" y="552" style="font-size:15px"><tspan x="700">AHLA "Our industry", 64,000-plus properties,</tspan><tspan x="700" dy="20">33,200-plus small-business properties, undated, C015</tspan></text>')
# the route you can drive: joins the six inns (after they move) to You
X.append('<path id="route" class="hide kit-route" d="M126 404C170 414 230 398 283 406C335 414 390 398 440 406C490 413 540 400 590 410C640 424 560 470 470 505C430 520 400 532 380 548"/>')
X.append('<g id="you" class="hide"><use href="#kit-practice-figure" transform="translate(350,622) scale(.6)"/>'
         '<text class="lab" x="350" y="700" text-anchor="middle">You</text></g>')
X.append('<text id="illus" class="hide small" x="420" y="612">a route you can drive · illustrative</text>')
body += '\n' + '\n'.join(X)

defs = kit_defs(['kit-phone', 'kit-practice-figure', 'kit-inn-mini', 'kit-person', 'kit-retainer-tag'])
C = {k: c(w) for k, w in dict(six='W002733', ninety='W002741', six2='W002749', props='W002750', not_='W002751',
                              the='W002755', thirty='W002760', nobody='W002771', you='W002780', route='W002789').items()}
tl = TL()
tl.slide('#row40', C['six'], x=0)
tl.js(f"t.set('#row40 .fig, #row40 .lab',{{autoAlpha:0}},0);")
tl.fade('#row40 .fig', C['ninety']); tl.fade('#row40 .lab', C['ninety'] + .6)
# everything except the six inns recedes out; the inns move left and down
gone = ['p1', 'p2', 'p3', 'p23', 'p4', 'p5', 'p5n', 'l1', 'l2', 'l3', 'l4', 'l4rule', 'l5', 'hrs8', 'cap8', 'capa', 'colb', 'cols', 'stag',
        'barb', 'barbl', 'bars', 'figb', 'figbx', 'figs', 'figsx', 'row20', 'row40', 'foot']
tl.js("t.to('" + ','.join('#' + g for g in gone) + f"',{{autoAlpha:0,duration:.5,ease:'power1.inOut'}},{C['six2']});")
tl.to('#inns', C['six2'] + .25, 'x:-270,y:110', .8)
tl.fade('#sixl', C['props'] + .45)
tl.appear('#ev', C['the'])
tl.fade('#evfig', C['thirty'])
tl.fade('#evline', C['thirty'] + .8)
tl.fade('#evq', C['thirty'] + 1.6)
tl.appear('#rcpt', C['the'])
tl.fade('#nc', C['nobody'])
tl.fade('#you', C['you'])
tl.draw('#route', C['route'] - .3, .9)
tl.appear('#illus', C['route'] + .5)
css = '<style>' + ''.join(f'#{i}{{visibility:visible;opacity:{op}}}' for op, ids in END.items() for i in ids) + '#s16{visibility:hidden;opacity:0}#cols-dash{opacity:0}#cols-solid{opacity:1 !important}</style>'
html = page("S17 the operator's arithmetic, part d", 's17d-root', 'ep009-s17d', DUR, body, defs, tl, C)
html = html.replace('</head>', css + '</head>', 1)
(HERE.parent / 'index.html').write_text(html)
print('wrote', DUR)
