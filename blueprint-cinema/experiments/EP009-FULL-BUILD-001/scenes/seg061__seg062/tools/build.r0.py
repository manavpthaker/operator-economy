#!/usr/bin/env python3
"""EP009 S18 (seg061, seg062): the hard parts, three slots on one world. Generates ../index.html.
Frame 0 restores seg060's last frame by re-running the seg060 layout with its end state in CSS."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa

MI, MO = 1008.333333, 1064.333333
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
c = lambda w, o=0.0: cue(w, MI, o)

# ---------- inherited S17d end state ----------
src_path = HERE.parent.parent / 'seg060/tools/build.py'
src = src_path.read_text().split("defs = kit_defs")[0]
ns = {'__file__': str(src_path), '__name__': 's17d_layout'}
exec(compile(src, str(src_path), 'exec'), ns)
prev = ns['body']
PREV_VISIBLE = ['band', 'ul1', 'ul2', 'head', 'inns', 'sixl', 'ev', 'evfig', 'evline', 'evq', 'rcpt', 'nc', 'you', 'route', 'illus']
css = ('<style>' + ''.join(f'#{i}{{visibility:visible;opacity:1}}' for i in PREV_VISIBLE)
       + '#s16{visibility:hidden;opacity:0}#inns{transform:translate(-270px,110px)}</style>')
PREV_IDS = [i for i in PREV_VISIBLE if i != 'you']

r = Rough(1861)
S = [f'<g id="prev">{prev}</g>'.replace('<g id="you"', '<g id="you-old"')]
# the You figure is lifted out of the S17 group so it can carry into S18
S.append('<g id="you2"><use href="#kit-practice-figure" transform="translate(350,622) scale(.6)"/></g>')
S.append('<text id="youl" class="lab" x="350" y="700" text-anchor="middle">You</text>')

S.append('<text id="h18" class="hide fig" x="640" y="70" text-anchor="middle" style="font-size:50px">What\'s genuinely hard</text>')
SL = [(40, 'slot1'), (450, 'slot2'), (860, 'slot3')]
for x, gid in SL:
    S.append(f'<path id="{gid}" class="hide" d="{r.rect(x,100,380,300)}" stroke="{STEEL}" stroke-width="1.6" stroke-dasharray="8 7" fill="none"/>')
S.append('<text id="t1" class="hide lab" x="62" y="136">The ceiling</text>')
S.append('<text id="t2" class="hide lab" x="472" y="136">Renewal</text>')
S.append('<text id="t3" class="hide lab" x="882" y="136">Access</text>')

# slot 1: a low ceiling the retainer cannot fit under
S.append('<g id="s1inn" class="hide"><use href="#kit-inn-mini" transform="translate(70,300) scale(.45)"/></g>')
S.append(f'<g id="s1line" class="hide"><path d="M64 282L150 281.5M156 282L240 281.5M64 275L64 289M240 274L240 288" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
S.append('<g id="s1tag" class="hide"><use href="#kit-retainer-tag" transform="translate(110,232) scale(.8)"/></g>')
S.append('<text id="s1few" class="hide small" x="252" y="276"><tspan x="252">a few hundred</tspan><tspan x="252" dy="24">a month</tspan></text>')

# slot 2: renewal, a good summer is not a result; the baseline is kept
S.append('<g id="cal" class="hide"><use href="#kit-calendar-leaf" transform="translate(480,170)"/></g>')
S.append('<text id="summer" class="hide small" x="540" y="332" text-anchor="middle">a good summer</text>')
S.append('<text id="slow" class="hide tiny" x="540" y="362" text-anchor="middle">first slow month</text>')
S.append(f'<g id="folder" class="hide"><path d="M650 212L700 212L712 224L806 224L806 312L650 312Z" fill="{CARD}"/>'
         f'<path d="{r.seg(650,212,700,212,False)}{r.seg(712,224,806,224,False)}{r.seg(806,226,806,312,False)}{r.seg(804,312,650,312)}{r.seg(650,310,650,213,False)}M700 212L712 224" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>')
S.append('<g id="base"><g id="basein" class="hide"><use href="#kit-sheet" transform="translate(664,236) scale(.4)"/>'
         '<text class="tiny" x="680" y="266">baseline</text></g></g>')
S.append('<text id="keep" class="hide small" x="728" y="346" text-anchor="middle">kept</text>')

# slot 3: access, at the owner's desk, holding the accounts
S.append('<g id="desk3" class="hide"><use href="#kit-table" transform="translate(890,330) scale(.8)"/>'
         '<use href="#kit-person" transform="translate(986,284) scale(.8)"/>'
         '<use href="#kit-sheet" transform="translate(1030,292) scale(.26)"/>'
         '<text class="tiny" x="986" y="385" text-anchor="middle">owner</text></g>')
S.append('<text id="acct" class="hide tiny" x="1066" y="318" text-anchor="middle" style="font-size:14px">accounts</text>')
S.append('<text id="guest" class="hide small" x="1170" y="428" text-anchor="middle">You\'re a guest</text>')

# the room-count axis (S11), the viable window, agencies
S.append(f'<g id="axis" class="hide"><path d="{r.seg(80,620,860,620)}" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
         f'<path d="M260 612L260 628M620 612L620 628" stroke="{INK}" stroke-width="2" fill="none"/>'
         '<text class="tiny" x="260" y="650" text-anchor="middle">20</text><text class="tiny" x="620" y="650" text-anchor="middle">40</text>'
         '<text class="tiny" x="40" y="626" text-anchor="middle">rooms</text></g>')
S.append(f'<path id="wl" class="hide" d="M330 560L330 640" stroke="{STEEL}" stroke-width="2.5" stroke-dasharray="8 6" fill="none"/>')
S.append('<text id="small" class="hide small" x="190" y="596" text-anchor="middle">too small</text>')
S.append(f'<path id="wr" class="hide" d="M560 560L560 640" stroke="{STEEL}" stroke-width="2.5" stroke-dasharray="8 6" fill="none"/>')
S.append('<g id="agy" class="hide"><use href="#kit-person" transform="translate(700,578) scale(.34)"/><use href="#kit-person" transform="translate(770,578) scale(.34)"/>'
         '<text class="small" x="735" y="532" text-anchor="middle">already served by an agency</text></g>')
S.append(f'<g id="unk" class="hide"><path d="M340 672L550 672" stroke="{STEEL}" stroke-width="1.6" stroke-dasharray="6 5" fill="none"/>'
         f'<path d="M348 666L340 672L348 678M542 666L550 672L542 678" stroke="{STEEL}" stroke-width="1.6" fill="none"/>'
         '<text class="small" x="445" y="700" text-anchor="middle">width unknown</text></g>')

# the fork: stop, or move up the band (rightward along the axis, never a rising arrow)
S.append(label(r, 'f1', 40, 424, 330, 52, [('no owner funds $600 a month', 'small', 16, 33)]))
S.append(label(r, 'f2', 390, 424, 270, 52, [('agencies own the band', 'small', 16, 33)]))
S.append(f'<g id="stop" class="hide"><path d="M672 450L760 450M762 436L762 464" stroke="{STEEL}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
         '<text class="lab" x="776" y="459">stop</text></g>')
S.append(f'<g id="up" class="hide"><path d="M876 450L1030 450M1020 441L1031 450L1020 459" stroke="{STEEL}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
         '<text class="small" x="852" y="458" text-anchor="middle">or</text>'
         '<text class="lab" x="1042" y="459">move up</text></g>')
S.append(f'<g id="ext"><path id="extl" class="hide" d="M866 620L1230 620" stroke="{INK}" stroke-width="2.6" stroke-dasharray="12 8" fill="none"/>'
         f'<g id="extt" class="hide"><path d="M1180 612L1180 628" stroke="{INK}" stroke-width="2" fill="none"/>'
         '<text class="tiny" x="1180" y="650" text-anchor="middle">80</text>'
         '<text class="small" x="925" y="700" text-anchor="middle">40 to 80 rooms: the redesign</text></g></g>')
S.append(f'<g id="ground" class="hide"><path d="M640 604L1230 604" stroke="{STEEL}" stroke-width="1.3" fill="none"/>'
         '<text class="tiny" x="1230" y="596" text-anchor="end">their ground</text></g>')

body = '\n'.join(S)
defs = kit_defs(['kit-phone', 'kit-practice-figure', 'kit-inn-mini', 'kit-person', 'kit-retainer-tag',
                 'kit-calendar-leaf', 'kit-sheet', 'kit-table'])
C = {k: c(w) for k, w in dict(six='W002793', whats='W002798', genuinely='W002799', three='W002803', ceiling='W002806',
                              few='W002824', walk='W002830', viable='W002834', too='W002839', served='W002845',
                              how='W002855', renewal='W002860', good='W002862', keep='W002876', first='W002884',
                              access='W002887', owners='W002894', youre='W002900', if_='W002903', already='W002918',
                              stop='W002922', move='W002924', forty='W002926', their='W002942').items()}
tl = TL()
# S17 clears on "What's"; the You figure stays and carries the three hard parts
tl.out('#prev', C['whats'] - .1, .45)
tl.out('#youl', C['whats'] - .1, .45)
tl.fade('#h18', C['genuinely'])
tl.js(f"t.fromTo('#slot1,#slot2,#slot3',{{autoAlpha:0}},{{autoAlpha:1,duration:.35,stagger:.12}},{C['three']});")
# 1. the ceiling can say no
tl.fade('#t1', C['ceiling'])
tl.to('#you2', C['ceiling'], 'x:-70,y:-262', .9)
tl.appear('#s1inn', C['ceiling'] + .5)
tl.appear('#s1line', C['ceiling'] + .9)
tl.fade('#s1tag', C['ceiling'] + 1.3, y=-8)
tl.fade('#s1few', C['few'])
tl.to('#you2', C['walk'], 'x:-10,y:-262,opacity:.4', 1.0, 'power1.inOut')
# the viable band, edges uncertain
tl.appear('#axis', C['viable'])
tl.appear('#wl', C['too']); tl.fade('#small', C['too'])
tl.appear('#wr', C['served']); tl.fade('#agy', C['served'])
tl.fade('#unk', C['how'])
# 2. renewal
tl.fade('#t2', C['renewal'])
tl.appear('#cal', C['good']); tl.fade('#summer', C['good'] + .3)
tl.appear('#folder', C['keep'] - .2)
tl.js(f"t.fromTo('#basein',{{autoAlpha:0,y:-40}},{{autoAlpha:1,y:0,duration:.6,ease:'power2.out'}},{C['keep']});")
tl.fade('#keep', C['keep'] + .5)
tl.fade('#slow', C['first'])
# 3. access
tl.fade('#t3', C['access'])
tl.appear('#desk3', C['owners'] - .2); tl.fade('#acct', C['owners'] + .2)
tl.to('#you2', C['owners'] - .2, 'x:820,y:-252,opacity:1', 1.0, 'power1.inOut')
tl.fade('#guest', C['youre'])
# stop or move up
tl.slide('#f1', C['if_'], x=0)
tl.slide('#f2', C['already'], x=0)
tl.appear('#stop', C['stop'])
tl.appear('#up', C['move'])
tl.appear('#extl', C['forty'], .5)
tl.appear('#extt', C['forty'] + .4)
tl.appear('#ground', C['their'])

html = page('S18 the hard parts', 's18-root', 'ep009-s18', DUR, body, defs, tl, C)
html = html.replace('</head>', css + '</head>', 1)
(HERE.parent / 'index.html').write_text(html)
print('wrote', DUR)
