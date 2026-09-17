#!/usr/bin/env python3
"""EP009 S17 parts a+b (seg057, seg058): the operator's arithmetic. Generates ../index.html."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from act4lib import *  # noqa

MI, MO = 903.333333, 976.541667
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
c = lambda w, o=0.0: cue(w, MI, o)
r = Rough(5717)
S = []  # svg body
tl = TL()

# ---------- inherited S16 end state (seg056), reconstructed from DIRECTION-PLAN.md ----------
S.append('<g id="s16">')
S.append('<text class="fig" x="640" y="104" text-anchor="middle" style="font-size:50px">Kill condition</text>')
S.append('<use href="#kit-phone" transform="translate(96,180)"/>')
S.append(f'<g><path d="{r.rect(230,160,520,150)}" class="steel"/>'
         '<text class="lab" x="254" y="212">agencies already retain 30-room inns</text>'
         '<text class="lab" x="254" y="244">at $1,500 a month</text>'
         '<text class="small" x="254" y="286">owners prefer it</text></g>')
S.append('<use href="#kit-practice-figure" transform="translate(150,520) scale(.6)"/>')
S.append('<path class="kit-route-dashed" d="M205 520C260 500 300 470 330 452"/>')
S.append('<use href="#kit-inn-mini" transform="translate(330,380) scale(.6)"/>')
S.append(f'<rect x="398" y="430" width="22" height="41" fill="{SHEET}" stroke="{STEEL}" stroke-width="2" stroke-dasharray="6 5"/>')
S.append('<text class="small" x="402" y="500" text-anchor="middle">no front door at this size</text>')
S.append('<path class="kit-route" d="M150 318C400 390 760 380 918 350M162 312C520 360 960 300 1080 350"/>')
S.append('<use href="#kit-person" transform="translate(930,400) scale(.5)"/><use href="#kit-person" transform="translate(1090,400) scale(.5)"/>')
S.append('<text class="small" x="1010" y="460" text-anchor="middle">two agencies</text>')
S.append(f'<g><path d="{r.rect(780,500,440,70)}" class="steel"/><text class="small" x="802" y="544">smallest retained property:</text>'
         f'<path d="M1060 548L1196 548" class="light"/></g>')
S.append('</g>')

# ---------- persistent top band: modeled scenario, every frame ----------
S.append(f'<g id="band"><rect x="0" y="0" width="1280" height="40" fill="{CARD}"/>'
         f'<path d="M0 40.5L1280 40.5" stroke="{STEEL}" stroke-width="1.3"/>'
         '<text x="640" y="27" text-anchor="middle"><tspan class="kicker">MODELED SCENARIO</tspan>'
         '<tspan class="small" style="font-size:19px"> · Modeled scenario, not observed performance or an earnings forecast.</tspan></text></g>')
S.append('<path id="ul1" class="hide" d="M242 34L614 34" stroke="#173530" stroke-width="2" fill="none" stroke-linecap="round"/><path id="ul2" class="hide" d="M622 34L1040 34" stroke="#173530" stroke-width="2" fill="none" stroke-linecap="round"/>')
S.append('<text id="foot" class="hide tiny" x="1252" y="711" text-anchor="end" style="font-size:15px">C024, C028 to C033 · Canvas section 10</text>')
S.append('<text id="head" class="hide fig" x="640" y="94" text-anchor="middle" style="font-size:44px">Your side of the arithmetic</text>')

# ---------- price rail ----------
rail = [
    ('p1', 128, 46, [('Audit $1,200', 'lab', 16, 31)]),
    ('p2', 186, 60, [('Retainer $600 a month', 'lab', 16, 27), ('20 rooms', 'tiny', 16, 50)]),
    ('p3', 258, 60, [('$1,000 or $1,250', 'lab', 16, 27), ('40 rooms', 'tiny', 16, 50)]),
    ('p4', 330, 46, [('Blend $800', 'lab', 16, 31)]),
    ('p5', 398, 60, [('Your time: $60 an hour', 'lab', 16, 27)]),
]
for gid, y, h, lines in rail:
    S.append(label(r, gid, 30, y, 290, h, lines))
S.append('<text id="p5n" class="hide tiny" x="46" y="448">the model\'s number</text>')
S.append('<path id="p23" class="hide light" d="M44 246L44 258"/>')

# ---------- six inns under their small ceilings ----------
CX = [400 + 78 * i for i in range(6)]
S.append('<g id="inns" class="hide">')
for i, cx in enumerate(CX):
    S.append(f'<g class="inn"><path d="M{cx-36} 172L{cx-2} 171.5M{cx+3} 172L{cx+36} 171.5M{cx-36} 166L{cx-36} 178M{cx+36} 165L{cx+36} 177" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<use href="#kit-retainer-tag" transform="translate({cx-36},182) scale(.75)"/>'
             f'<text class="tiny" x="{cx-4}" y="202" text-anchor="middle" style="font-weight:500;fill:{INK}">$800</text>'
             f'<use href="#kit-inn-mini" transform="translate({cx-36},232) scale(.3)"/></g>')
S.append('</g>')
S.append('<g id="hrs8" class="hide">' + ''.join(f'<text class="small" x="{cx}" y="306" text-anchor="middle">8 h</text>' for cx in CX) + '</g>')
S.append('<text id="cap8" class="hide small" x="598" y="340" text-anchor="end">a month each</text>')
S.append('<text id="capa" class="hide small" x="604" y="340">· audit 12 h each</text>')

# ---------- ledger strip ----------
LX = 884
led = [('l1', 176, '6 × $800 × 12 = $57,600 a year'),
       ('l2', 216, '+ 6 audits at $1,200: $64,800 gross'),
       ('l3', 256, '− tools and overhead, about $6,000'),
       ('l4', 304, '= $58,800 before you pay yourself'),
       ('l5', 352, '650 h × $60 = about $39,000')]
for gid, y, s in led:
    S.append(f'<text id="{gid}" class="hide lab" x="{LX}" y="{y}" style="font-size:21px">{s}</text>')
S.append(f'<path id="l4rule" class="hide" d="M{LX} 274L{LX+170} 273.5M{LX+176} 274L{LX+350} 273.5" stroke="{INK}" stroke-width="1.6" fill="none"/>')

# ---------- base and stress columns (equal) ----------
BX, SX, CW, CY, CH = 360, 830, 420, 404, 188
S.append(f'<g id="colb" class="hide"><path d="{r.rect(BX,CY,CW,CH)}" class="steel"/>'
         f'<text class="lab" x="{BX+20}" y="{CY+36}">Base: 8 h a property</text></g>')
S.append(f'<g id="cols" class="hide"><path id="cols-dash" d="{r.rect(SX,CY,CW,CH)}" class="dash"/><path id="cols-solid" d="{r.rect(SX,CY,CW,CH)}" class="steel" style="opacity:0"/>'
         f'<text class="lab" x="{SX+20}" y="{CY+36}">Stress: 12 h a property</text></g>')
S.append(f'<text id="stag" class="hide tiny" x="{SX+CW-18}" y="{CY+34}" text-anchor="end">the stress case</text>')
S.append(f'<path id="barb" class="hide" d="M{BX+20} {CY+70}L{BX+280} {CY+70}" stroke="{INK}" stroke-width="12" fill="none"/>')
S.append(f'<text id="barbl" class="hide small" x="{BX+20}" y="{CY+104}">about 650 hours</text>')
S.append(f'<path id="bars" class="hide" d="M{SX+20} {CY+70}L{SX+20+376} {CY+70}" stroke="{INK}" stroke-width="12" fill="none"/>')
S.append(f'<text id="figb" class="hide fig" x="{BX+20}" y="{CY+152}">about $20,000 left</text>')
S.append(f'<text id="figbx" class="hide tiny" x="{BX+20}" y="{CY+176}">in the model: $19,920</text>')
S.append(f'<text id="figs" class="hide fig" x="{SX+20}" y="{CY+152}">about $2,500 left</text>')
S.append(f'<text id="figsx" class="hide tiny" x="{SX+20}" y="{CY+176}">in the model: $2,640</text>')

# ---------- 20-room row ----------
S.append(label(r, 'row20', 30, 606, 600, 84,
               [('6 × 20-room inns × $600 × 12', 'small', 20, 30), ('$43,200 a year of retainer', 'fig', 20, 70)], ear=16)
         .replace('class="fig"', 'class="fig" style="font-size:32px"'))

body = '\n'.join(S)
defs = kit_defs(['kit-phone', 'kit-practice-figure', 'kit-inn-mini', 'kit-person', 'kit-retainer-tag'])

C = {k: c(w) for k, w in dict(
    say='W002508', door_open_end='W002511', your='W002512', modeled='W002523', not1='W002525', not2='W002528',
    audit='W002532', retainer='W002536', rising='W002547', call='W002557', six='W002562', eight='W002566',
    twelve='W002572', l1='W002576', add='W002591', take='W002605', and_='W002615', now='W002627',
    models='W002633', six2='W002638', about650='W002647', at60='W002653', so='W002661', about20='W002670',
    and2='W002674', twelve2='W002679', the_stress='W002686', that='W002689', about25='W002693',
    six20='W002699', forty='W002709').items()}

# S16 tail holds through "Say the door's open." then clears; band stays from frame 0.
tl.out('#s16', round(C['your'] - .5, 3), .4)
tl.fade('#head', C['your'])
tl.draw('#ul1', C['modeled'], .7)
tl.draw('#ul2', C['not1'], C['not2'] - C['not1'] + .9)
tl.appear('#foot', C['your'])
# price rail on its words
tl.slide('#p1', C['audit'])
tl.slide('#p2', C['retainer'])
tl.slide('#p3', C['rising']); tl.appear('#p23', C['rising'])
tl.slide('#p4', C['call'])
# six inns carry the blend under their ceilings
tl.js(f"t.fromTo('#inns .inn',{{autoAlpha:0,y:10}},{{autoAlpha:1,y:0,duration:.4,ease:'power2.out',stagger:.12}},{C['six']});")
tl.set('#inns', C['six'], 'autoAlpha:1')
tl.appear('#hrs8', C['eight']); tl.appear('#cap8', C['eight'])
tl.appear('#capa', C['twelve'])
# ledger, one operation per sentence (receipt order, top down)
tl.fade('#l1', C['l1'])
tl.fade('#l2', C['add'])
tl.fade('#l3', C['take'])
tl.appear('#l4rule', C['and_']); tl.fade('#l4', C['and_'])
# seg058: your time priced
tl.slide('#p5', C['now'])
tl.appear('#p5n', C['models'])
tl.draw('#barb', C['six2'], .8)
tl.appear('#barbl', C['about650'])
tl.fade('#l5', C['at60'])
# equal columns
for s in ('#p1', '#p2', '#p3', '#p23', '#p4', '#l1', '#l2', '#l3', '#hrs8', '#cap8', '#capa'):
    tl.to(s, C['so'], 'opacity:.45', .5)
tl.appear('#colb', C['so']); tl.appear('#cols', C['so'])
tl.fade('#figb', C['about20']); tl.appear('#figbx', C['about20'] + .2)
tl.set('#cols-dash', C['and2'], 'opacity:0'); tl.set('#cols-solid', C['and2'], 'opacity:1')
tl.js(f"t.set('#bars',{{autoAlpha:1,scaleX:{260/376:.4f},transformOrigin:'0% 50%'}},{C['and2']});")
tl.js(f"t.to('#bars',{{scaleX:1,duration:.7,ease:'power2.inOut'}},{C['twelve2']});")
tl.appear('#stag', C['the_stress'])
tl.fade('#figs', C['about25']); tl.appear('#figsx', C['about25'] + .2)
# both recede equally; the 20-room row arrives
for s in ('#colb', '#cols', '#stag', '#barb', '#barbl', '#bars', '#figb', '#figbx', '#figs', '#figsx', '#l4', '#l4rule', '#l5', '#p5', '#p5n'):
    tl.to(s, C['six20'], 'opacity:.5', .5)
tl.fade('#row20', C['forty'] - .25)

html = page('S17 the operator\'s arithmetic, parts a and b', 's17ab-root', 'ep009-s17ab', DUR, body, defs, tl, C)
(Path(__file__).parent.parent / 'index.html').write_text(html)
print('wrote', DUR)
