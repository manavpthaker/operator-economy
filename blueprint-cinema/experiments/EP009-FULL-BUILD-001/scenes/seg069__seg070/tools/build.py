#!/usr/bin/env python3
"""EP009 S20e + S21 (seg069, seg070): the callback in the S00 model world, then redirect (not recap) to the service
inside the second commission and the S10 ceiling slip cleared for any property. Generates ../index.html.
S00 object placements match scenes/seg004__seg006 (act 1): inn (60,262) .8, site (856,290) 1.7, tags (1150,318|376) 1.4.
The slip matches scenes/seg036__seg039 (act 3): kit-ceiling-slip-filled with lit boxes, title, illustrative tag."""
import subprocess
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa

MI, MO = 1139.458333, 1175.041667
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
c = lambda w, o=0.0: cue(w, MI, o)
r = Rough(2021)
S = []

# ---------------- S20e: the S00 world, the following year ----------------
S.append('<text id="ill" class="kicker" x="40" y="44">ILLUSTRATIVE</text>')
S.append('<g id="w00">')
S.append('<g id="inn"><use href="#kit-inn" transform="translate(60,262) scale(.8)"/><text class="label" x="252" y="238" text-anchor="middle">The inn</text></g>')
S.append('<g id="own"><use href="#kit-inn-own-page" transform="translate(357.6,433.2) scale(.8)"/></g>')
S.append('<g id="site"><use href="#kit-booking-site-simple" transform="translate(856,290) scale(1.7)"/><text class="label" x="992" y="268" text-anchor="middle">Booking site</text></g>')
S.append('<g id="tag1"><use href="#kit-commission-tag" transform="translate(1150,318) scale(1.4)"/></g>')
S.append('<path id="intro" class="kit-route" d="M864 510C750 606 450 606 318 508"/>')
S.append(f'<path id="intro2" class="hide" d="M864 510C750 606 450 606 318 508" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
# the guest's own email field (not the relay)
S.append(f'<g id="field"><path d="M470 176L806 176L806 222L470 222Z" fill="{SHEET}"/><path d="{r.rect(470,176,336,46)}" stroke="{INK}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
         '<use href="#kit-text-own-email" transform="translate(488,207)"/></g>')
S.append('<g id="guest"><use href="#kit-guest" transform="translate(640,470) scale(.6)"/></g>')
S.append('</g>')
S.append('<g id="tag2"><use href="#kit-commission-tag" transform="translate(1150,376) scale(1.4)"/></g>')
S.append('<g id="tag2e" class="hide"><use href="#kit-commission-tag-empty" transform="translate(1150,376) scale(1.4)"/></g>')
# October note travels from the inn to the guest's own email
S.append('<g id="note" class="hide"><use href="#kit-seasonal-note" transform="translate(0,0) scale(.75)"/></g>')
S.append('<text id="oct" class="hide small" x="720" y="112" text-anchor="end">October</text>')
S.append('<path id="book" class="hide kit-route" d="M596 462C540 470 470 470 414 466"/>')
S.append('<g id="notag" class="hide"><use href="#kit-commission-tag-empty" transform="translate(478,404) scale(1.4)"/></g>')

# ---------------- S21: the service inside the second commission ----------------
S.append('<g id="big" class="hide"><g id="bigtag"><use href="#kit-commission-tag" transform="translate(150,230) scale(4)"/></g>'
         f'<path id="svc" class="hide" d="M250 274L370 270L374 354L250 358Z" fill="{SHEET}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>'
         '<g id="pcard" class="hide"><use href="#kit-practice-card" transform="translate(275,280) scale(.46)"/></g>'
         '<text id="svcl" class="hide label" x="310" y="430" text-anchor="middle">the service</text></g>')

# the S10 ceiling slip (inline copy, same geometry as seg036__seg039)
slip = subprocess.run(['python3', str(KITDEFS).replace('kit_defs.py', 'kit_defs.py'), 'inline', 'kit-ceiling-slip-filled', '--prefix', 'slip'],
                      capture_output=True, text=True, check=True).stdout
lit = ''.join(f'<rect id="lit{i}" x="24" y="{y}" width="252" height="51" fill="{CARD}" style="mix-blend-mode:multiply"/>'
              for i, y in ((1, 93), (2, 179), (3, 265), (4, 350)))
S.append('<g id="slipw" class="hide"><g id="slip" transform="translate(760,150)">' + slip + lit
         + '<text id="slip-title" class="lab" x="24" y="40" style="font-size:26px">The ceiling</text>'
         + '<text id="slip-ill" class="tiny" x="258" y="40" text-anchor="end">illustrative</text></g></g>')
S.append('<text id="four" class="hide label" x="610" y="250" text-anchor="middle">Four numbers</text>')
S.append('<g id="cline" class="hide"><use href="#kit-ceiling-line" transform="translate(430,470) scale(.9)" color="#B5482F"/>'
         '<text class="lab" x="430" y="452">Ceiling</text></g>')
S.append('<g id="rtag" class="hide"><use href="#kit-retainer-tag" transform="translate(530,486)"/></g>')
S.append('<text id="anyp" class="hide small" x="910" y="626" text-anchor="middle">any small property</text>')

body = '\n'.join(S)
defs = kit_defs(['kit-inn', 'kit-inn-own-page', 'kit-booking-site-simple', 'kit-commission-tag', 'kit-commission-tag-empty',
                 'kit-text-own-email', 'kit-guest', 'kit-seasonal-note', 'kit-practice-card', 'kit-ceiling-line', 'kit-retainer-tag'])
C = {k: c(w) for k, w in dict(in_='W003146', october='W003147', note='W003149', the='W003157', inns='W003163', no='W003167',
                              the2='W003176', still='W003178', nobody='W003183', stopped='W003189', thats='W003195',
                              service='W003197', now='W003203', rooms='W003208', rate='W003209', occ='W003210', share='W003211',
                              four='W003215', a='W003217', fit='W003225', any_='W003233', ten='W003237').items()}
tl = TL()
# In October, a note about the trail, to the guest's own email
tl.js(f"t.fromTo('#note',{{autoAlpha:0,x:230,y:250}},{{autoAlpha:1,x:230,y:250,duration:.3}},{C['in_']});")
tl.js(f"t.to('#note',{{x:726,y:92,duration:1.1,ease:'power2.inOut'}},{C['note']});")
tl.fade('#oct', C['october'] + .2)
# the next booking comes through the inn's own page, no tag attached
tl.draw('#book', C['inns'] - .4, .8)
tl.appear('#notag', C['no'], .4)
# the site still did the first introduction; nobody left it
tl.draw('#intro2', C['still'], .9)
# the inn stopped paying for the second one
tl.out('#tag2', C['stopped'], .5)
tl.appear('#tag2e', C['stopped'], .5)
# S21: redirect. The world recedes; the second tag opens onto the service.
tl.js("t.to('#w00,#note,#oct,#book,#notag,#tag2e,#ill,#intro2',{autoAlpha:0,duration:.45,ease:'power1.inOut'}," + str(C['thats'] - .2) + ");")
tl.js(f"t.fromTo('#big',{{autoAlpha:0,x:760,y:120,scale:.35,svgOrigin:'150 230'}},{{autoAlpha:1,x:0,y:0,scale:1,duration:.55,ease:'power2.inOut'}},{C['thats'] - .1});")
tl.appear('#svc', C['service'], .3)
tl.fade('#pcard', C['service'] + .15)
tl.fade('#svcl', C['service'] + .5)
# "And now you have the arithmetic": the tag slides aside, the slip comes forward
tl.js(f"t.to('#big',{{x:-110,y:120,scale:.6,svgOrigin:'150 230',opacity:.5,duration:.7,ease:'power2.inOut'}},{C['now']});")
tl.js(f"t.fromTo('#slipw',{{autoAlpha:0,x:120}},{{autoAlpha:1,x:0,duration:.6,ease:'power2.out'}},{C['now'] + .1});")
# the four inputs highlight and clear to blank, one oxide at a time
for i, k in enumerate(['rooms', 'rate', 'occ', 'share'], 1):
    at = C[k]
    tl.js(f"t.to('#slip__box{i}',{{stroke:'#B5482F',duration:.15}},{at});")
    tl.js(f"t.to('#slip__value{i},#lit{i}',{{autoAlpha:0,duration:.35,ease:'power1.in'}},{at + .2});")
    tl.js(f"t.to('#slip__box{i}',{{stroke:'#173530',duration:.2}},{at + .55});")
tl.out('#slip-ill', C['share'] + .3)
tl.fade('#four', C['four'])
tl.js(f"t.to('#big',{{autoAlpha:0,duration:.4}},{C['four']});")
tl.appear('#cline', C['a'], .4)
tl.fade('#rtag', C['fit'], y=-8)
tl.fade('#anyp', C['any_'])

html = page('S20e and S21 the callback and the payoff', 's21-root', 'ep009-s20e-s21', DUR, body, defs, tl, C)
(HERE.parent / 'index.html').write_text(html)
print('wrote', DUR)
