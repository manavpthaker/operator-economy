#!/usr/bin/env python3
"""EP009 S17 parts a+b (seg057, seg058): the operator's arithmetic. Fix round 1 (B-11, B-24).
Frame 0 is act 3's revised seg056 last frame (end_state_for_act4). S16's You, route and small inn carry into S17:
the inn becomes the first of six on the route; nothing clears to blank paper. Each step replaces the last:
rail cards swap, ledger lines collapse, the equal base and stress columns take the lower frame.
Generates ../index.html; scene() is imported by seg060."""
import hashlib
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa
from r1lib import TL2, page2

MI, MO = 903.333333, 976.541667
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
A3 = HERE.parents[1] / 'seg056/index.html'

INN0 = (770, 362, .55)           # S16 inn
YOU0 = (330, 440, .7)            # S16 You
YOU1 = (110, 300, .5)            # S17 row
INNX = [250 + 160 * i for i in range(6)]
INNY, INNS = 214, .42            # inn-mini 240x152 -> 101x64
ROUTE_Y = 292
BAND_TXT = 'Modeled scenario, not observed performance or an earnings forecast.'


def a3_css():
    return ('.a3-cardw{stroke:#173530;stroke-width:3;fill:#F5F0E6}'
            '.a3-blk{font-family:Supreme,sans-serif;fill:#173530;font-size:25px;font-weight:500}'
            '.a3-kicker{font-family:Supreme,sans-serif;fill:#33464C;font-size:18px;font-weight:500;letter-spacing:2px}'
            '.a3-small{font-family:Supreme,sans-serif;fill:#33464C;font-size:22px;font-weight:400}'
            '.a3-tiny{font-family:Supreme,sans-serif;fill:#33464C;font-size:18px;font-weight:400}'
            '.a3-gap{stroke:#586D74;stroke-width:2;stroke-dasharray:6 5;fill:none;stroke-linecap:round}'
            '.head2{font-family:Boska,serif;fill:#173530;font-size:36px;font-weight:700}')


def scene():
    c = lambda w, o=0.0: cue(w, MI, o)
    r = Rough(5717)
    S = []
    # ---------- S16 end state (act 3 seg056 fix round 1), same markup and geometry ----------
    S.append('<g id="s16">'
             '<g id="a3-phone"><use href="#kit-phone" transform="translate(60,140)"/></g>'
             '<g id="a3-cond"><rect x="170" y="120" width="1010" height="170" rx="4" class="a3-cardw"/>'
             '<text class="a3-kicker" x="202" y="160">KILL CONDITION</text>'
             '<text class="a3-blk" x="202" y="208" font-size="27">If agencies already retain 30-room inns at $1,500 a month,</text>'
             '<text class="a3-blk" x="202" y="254" font-size="27">and owners prefer it</text>'
             '<rect x="900" y="230" width="252" height="38" rx="4" class="a3-gap"/><text class="a3-tiny" x="1026" y="255" text-anchor="middle">unknown: ask two agencies</text></g>'
             '<g id="a3-door"><path class="a3-gap" d="M706 386L748 386L748 450L706 450Z"/>'
             '<text class="a3-small" x="700" y="500" text-anchor="middle">then: no front door at this size</text></g>'
             '<path id="a3-rt" class="kit-route" d="M400 420C500 414 600 414 700 418"/>'
             '<g id="a3-call"><path class="kit-route" d="M92 280C94 400 120 520 160 584"/><path class="kit-route" d="M104 280C136 400 220 520 290 584"/>'
             '<use href="#kit-person" transform="translate(170,640) scale(.42)"/><use href="#kit-person" transform="translate(300,640) scale(.42)"/>'
             '<text class="a3-tiny" x="170" y="686" text-anchor="middle">agency</text><text class="a3-tiny" x="300" y="686" text-anchor="middle">agency</text></g>'
             '<g id="a3-ans"><text class="a3-blk" x="620" y="624" font-size="25">smallest retained property:</text>'
             '<path d="M948 594L1210 593M1211 596L1210 646M1208 648L950 648M947 645L948 598" stroke="#173530" stroke-width="2.2" fill="#FBF8F1" stroke-linecap="round"/></g>'
             '</g>')
    # carried objects: You and the inn (moved by GSAP on wrapper groups)
    S.append('<g id="you" transform="matrix(1,0,0,1,0,0)"><use href="#kit-practice-figure" transform="translate(330,440) scale(.7)"/></g>')
    S.append('<text id="youl" class="a3-small" x="330" y="352" text-anchor="middle" fill="#173530">You</text>')
    S.append('<text id="youl2" class="hide lab" x="110" y="228" text-anchor="middle">You</text>')
    S.append('<g id="inn0" transform="matrix(1,0,0,1,0,0)"><use href="#kit-inn-mini" transform="translate(770,362) scale(.55)"/></g>')
    # ---------- S17 row: six inns on a route, small ceilings with blank retainer tags ----------
    S.append(f'<path id="route" class="hide kit-route" d="M170 {ROUTE_Y}C420 {ROUTE_Y-3} 800 {ROUTE_Y+3} 1180 {ROUTE_Y}"/>')
    S.append('<g id="inns5" class="hide">' + ''.join(
        f'<use class="innx" href="#kit-inn-mini" transform="translate({x},{INNY}) scale({INNS})"/>' for x in INNX[1:]) + '</g>')
    S.append('<g id="ceils" class="hide">' + ''.join(
        f'<g class="ceil"><path d="M{x} 172L{x+48} 171.5M{x+54} 172L{x+101} 171.5M{x} 165L{x} 179M{x+101} 164L{x+101} 178" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
        f'<use href="#kit-retainer-tag" transform="translate({x+26},178) scale(.5)"/></g>' for x in INNX) + '</g>')
    # B-R1-01: retain one fixed left edge; each cue appends only its new clause.
    # One text node avoids recentering and overlapping full-string crossfades.
    S.append('<text id="each-note" class="hide small" x="250" y="332">'
             '<tspan>each: $800 a month</tspan>'
             '<tspan id="each2" class="hide"> · 8 hours a month</tspan>'
             '<tspan id="each3" class="hide"> · audit 12 hours</tspan></text>')

    # ---------- band (every S17 frame from 0.5 s), heading small top-left, receipt ----------
    S.append(f'<g id="band" class="hide"><rect x="0" y="0" width="1280" height="40" fill="{CARD}"/>'
             f'<path d="M0 40.5L1280 40.5" stroke="{STEEL}" stroke-width="1.3"/>'
             '<text x="640" y="27" text-anchor="middle"><tspan class="kicker">MODELED SCENARIO</tspan>'
             f'<tspan class="small" style="font-size:19px"> · {BAND_TXT}</tspan></text></g>')
    S.append('<path id="ul1" class="hide" d="M242 34L614 34" stroke="#173530" stroke-width="2" fill="none" stroke-linecap="round"/>'
             '<path id="ul2" class="hide" d="M622 34L1040 34" stroke="#173530" stroke-width="2" fill="none" stroke-linecap="round"/>')
    S.append('<text id="foot" class="hide tiny" x="1252" y="711" text-anchor="end" style="font-size:15px">C024, C028 to C033 · Canvas section 10</text>')
    S.append('<text id="head" class="hide head2" x="40" y="96">Your side of the arithmetic</text>')

    # ---------- price rail: one to three cards, each step replaces ----------
    RX, RW = 40, 380
    S.append(label(r, 'pA', RX, 380, RW, 54, [('Audit $1,200', 'label', 18, 37)]))
    S.append(label(r, 'pB', RX, 446, RW, 54, [('Retainer $600 a month', 'label', 18, 37)]))
    S.append('<text id="pBn" class="hide small" x="436" y="482">20 rooms</text>')
    S.append(label(r, 'pC', RX, 512, RW, 54, [('$1,000 or $1,250', 'label', 18, 37)]))
    S.append('<text id="pCn" class="hide small" x="436" y="548">40 rooms</text>')
    S.append(label(r, 'pD', RX, 446, RW, 54, [('Blend $800 a month', 'label', 18, 37)]))
    S.append(label(r, 'pE', RX, 380, RW, 84, [('Your time: $60 an hour', 'label', 18, 37), ("the model's number", 'small', 18, 68)]))

    # ---------- ledger: one operation per sentence; earlier lines collapse ----------
    LX = 470
    led = [('l1', 410, '6 × $800 × 12 = $57,600 a year'),
           ('l2', 456, '+ 6 audits at $1,200: $64,800 gross'),
           ('l3', 502, '− tools and overhead, about $6,000'),
           ('l4', 562, '= $58,800 before you pay yourself')]
    LXX = 720
    for gid, y, s in led:
        S.append(f'<text id="{gid}" class="hide label" x="{LXX}" y="{y}">{s}</text>')
    S.append(f'<path id="l4rule" class="hide" d="M{LXX} 524L{LXX+230} 523.5M{LXX+236} 524L{LXX+470} 523.5" stroke="{INK}" stroke-width="1.6" fill="none"/>')
    S.append(f'<text id="l5" class="hide label" x="{LXX}" y="456">650 h × $60 = about $39,000</text>')

    # ---------- hours bar under the row, then the equal columns ----------
    S.append(f'<g id="hb"><path id="barb" class="hide" d="M250 330L610 330" stroke="{INK}" stroke-width="12" fill="none"/>'
             '<text id="barbl" class="hide small" x="626" y="338">about 650 hours</text></g>')
    BX, SX, CW, CY, CH = 40, 660, 580, 490, 200
    S.append(f'<g id="colb" class="hide"><path d="{r.rect(BX,CY,CW,CH)}" class="steel"/>'
             f'<text class="label" x="{BX+22}" y="{CY+40}">Base case: 8 h a property</text></g>')
    S.append(f'<g id="cols" class="hide"><path id="cols-dash" d="{r.rect(SX,CY,CW,CH)}" class="dash"/><path id="cols-solid" d="{r.rect(SX,CY,CW,CH)}" class="steel" style="opacity:0"/>'
             f'<text class="label" x="{SX+22}" y="{CY+40}">Stress case: 12 h a property</text></g>')
    S.append(f'<path id="sul" class="hide" d="M{SX+22} {CY+48}L{SX+150} {CY+48}" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    S.append(f'<path id="bars" class="hide" d="M{SX+22} {CY+76}L{SX+22+518} {CY+76}" stroke="{INK}" stroke-width="12" fill="none"/>')
    S.append(f'<text id="figb" class="hide fig" x="{BX+22}" y="{CY+164}" style="font-size:46px">about $20,000 left</text>')
    S.append(f'<text id="figs" class="hide fig" x="{SX+22}" y="{CY+164}" style="font-size:46px">about $2,500 left</text>')

    # ---------- 20-room row ----------
    S.append(label(r, 'row20', 40, 372, 580, 92,
                   [('6 × 20-room inns × $600 × 12', 'small', 20, 32), ('$43,200 a year of retainer', 'fig', 20, 76)], ear=16)
             .replace('class="fig"', 'class="fig" style="font-size:34px"'))

    C = {k: c(w) for k, w in dict(
        say='W002508', your='W002512', modeled='W002523', not1='W002525', not2='W002528',
        audit='W002532', retainer='W002536', rising='W002547', call='W002557', six='W002562', eight='W002566',
        twelve='W002572', l1='W002576', add='W002591', take='W002605', and_='W002615', now='W002627',
        models='W002633', six2='W002638', about650='W002647', at60='W002653', so='W002661', about20='W002670',
        and2='W002674', twelve2='W002679', the_stress='W002686', that='W002689', about25='W002693',
        six20='W002699', forty='W002709').items()}
    tl = TL2()
    # S16 holds through "Say the door's open."; the band arrives in S16's empty top strip.
    tl.appear('#band', C['say'] + .15, .35)
    # "Your side": S16's condition, phone, calls and answer field leave; You, the route and the inn stay and move up.
    tl.js("t.to('#s16 > g, #a3-rt',{autoAlpha:0,duration:.45,ease:'power1.inOut'}," + str(C['your'] - .1) + ");")
    tl.out('#youl', C['your'] - .1, .3)
    tl.mv('#you', C['your'] + .15, YOU0, YOU1, 1.0)
    tl.mv('#inn0', C['your'] + .15, INN0, (INNX[0], INNY, INNS), 1.0)
    tl.fade('#youl2', C['your'] + .9)
    tl.fade('#head', C['your'] + .2)
    tl.appear('#foot', C['your'] + .5)
    tl.draw('#route', C['your'] + .7, 1.2)
    # "a modeled scenario": five more inns on the route, pencil-light until they are counted
    tl.draw('#ul1', C['modeled'], .7)
    tl.js(f"t.set('#inns5',{{autoAlpha:1}},{C['modeled']});")
    tl.js(f"t.fromTo('#inns5 .innx',{{autoAlpha:0}},{{autoAlpha:.3,duration:.4,stagger:.14,ease:'power1.out'}},{C['modeled']});")
    tl.draw('#ul2', C['not1'], C['not2'] - C['not1'] + .9)
    # price rail: each card replaces or dims the one it follows
    tl.slide('#pA', C['audit'])
    tl.slide('#pB', C['retainer']); tl.fade('#pBn', C['retainer'] + .5)
    tl.slide('#pC', C['rising']); tl.fade('#pCn', C['rising'] + .5)
    tl.js(f"t.to('#pB,#pBn,#pC,#pCn',{{autoAlpha:0,duration:.35}},{C['call']});")
    tl.slide('#pD', C['call'] + .2)
    # six properties on retainer: the inns turn solid with a blank retainer tag under each small ceiling
    tl.js(f"t.to('#inns5 .innx',{{opacity:1,duration:.35,stagger:.08}},{C['six']});")
    tl.js(f"t.set('#ceils',{{autoAlpha:1}},{C['six']});t.fromTo('#ceils .ceil',{{autoAlpha:0,y:-8}},{{autoAlpha:1,y:0,duration:.35,stagger:.08}},{C['six']});")
    tl.fade('#each-note', C['six'] + .6)
    tl.appear('#each2', C['eight'], .25)
    tl.appear('#each3', C['twelve'], .25)
    # ledger
    tl.fade('#l1', C['l1'])
    tl.dim('#pD', C['add'], .3); tl.fade('#l2', C['add'])
    tl.fade('#l3', C['take'])
    tl.appear('#l4rule', C['and_']); tl.fade('#l4', C['and_'])
    tl.dim('#l1,#l2,#l3,#pA', C['and_'] + .3, .3)
    # seg058: your time priced; the rail and the three collapsed lines are replaced
    tl.js(f"t.to('#pA,#pD,#l1,#l2,#l3,#l4rule',{{autoAlpha:0,duration:.4}},{C['now'] - .15});")
    tl.js(f"t.to('#l4',{{y:-152,duration:.6,ease:'power2.inOut'}},{C['now']});")
    tl.slide('#pE', C['now'] + .2)
    tl.js(f"t.set('#pE text.small',{{autoAlpha:0}},0);t.to('#pE text.small',{{autoAlpha:1,duration:.35}},{C['models']});")
    tl.out('#each-note', C['six2'] - .1, .3)
    tl.draw('#barb', C['six2'] + .1, .8)
    tl.fade('#barbl', C['about650'])
    tl.fade('#l5', C['at60'])
    # "So": two equal columns replace the rail; the hours bar moves into the base column
    tl.out('#pE', C['so'] - .1, .35)
    tl.appear('#colb', C['so']); tl.appear('#cols', C['so'])
    tl.js(f"t.to('#hb',{{x:{BX+22-250},y:{CY+76-330},duration:.8,ease:'power2.inOut'}},{C['so'] + .1});")
    tl.fade('#figb', C['about20'])
    tl.set('#cols-dash', C['and2'], 'opacity:0'); tl.set('#cols-solid', C['and2'], 'opacity:1')
    tl.js(f"t.set('#bars',{{autoAlpha:1,scaleX:{360/518:.4f},transformOrigin:'0% 50%'}},{C['and2']});")
    tl.js(f"t.to('#bars',{{scaleX:1,duration:.7,ease:'power2.inOut'}},{C['twelve2']});")
    tl.draw('#sul', C['the_stress'], .5)
    tl.fade('#figs', C['about25'])
    # both cases recede together; the ledger lines leave; the 20-room row arrives
    tl.js(f"t.to('#l4,#l5',{{autoAlpha:0,duration:.4}},{C['six20']});")
    tl.dim('#colb,#cols,#sul,#hb,#bars,#figb,#figs', C['six20'], .5)
    tl.fade('#row20', C['six20'] + .5)
    tl.js(f"t.set('#row20 .fig',{{autoAlpha:0}},0);t.to('#row20 .fig',{{autoAlpha:1,duration:.4}},{C['forty']});")

    defs_ids = ['kit-phone', 'kit-practice-figure', 'kit-inn-mini', 'kit-person', 'kit-retainer-tag']
    return dict(body='\n'.join(S), lines=tl.lines, cues=C, css=a3_css(), defs_ids=defs_ids, dur=DUR, tl=tl)


if __name__ == '__main__':
    sc = scene()
    html = page2("S17 the operator's arithmetic, parts a and b", 's17ab-root', 'ep009-s17ab', DUR, sc['body'],
                 kit_defs(sc['defs_ids']), sc['tl'], sc['cues'], css=sc['css'])
    (HERE.parent / 'index.html').write_text(html)
    print('seg056 source sha256', hashlib.sha256(A3.read_bytes()).hexdigest(), 'wrote', DUR)
