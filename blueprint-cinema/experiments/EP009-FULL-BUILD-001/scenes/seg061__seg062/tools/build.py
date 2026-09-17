#!/usr/bin/env python3
"""EP009 S18 (seg061, seg062): the hard parts. Fix round 1 (B-13, B-14, B-24).
Frame 0 is seg060's revised last frame (replayed). No clear to blank paper: S17's six inns, route and You stay;
slot 1 is built out of the first inn. One hard part is on stage at a time; the used ones collapse to dimmed chips.
The viable window has dashed, unlabelled edges and no numbers on the axis (orchestrator ruling B-13).
Generates ../index.html; scene() is imported by seg063__seg065."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa
from r1lib import TL2, page2, load_scene

MI, MO = 1008.333333, 1064.333333
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
INN0 = (770, 362, .55)
YOU0 = (330, 440, .7)
ROW_INN = (250, 214, .42)
ROW_YOU = (110, 300, .5)


def scene():
    prev = load_scene('seg060')
    c = lambda w, o=0.0: cue(w, MI, o)
    r = Rough(1861)
    S = []
    S.append('<text id="h18" class="hide head2" x="40" y="96">What\'s genuinely hard</text>')
    CH = [(640, 'ch1', 'The ceiling'), (850, 'ch2', 'Renewal'), (1060, 'ch3', 'Access')]
    for x, gid, s in CH:
        S.append(f'<g id="{gid}" class="hide"><path class="chd" d="{r.rect(x,62,190,44)}" stroke="{STEEL}" stroke-width="1.6" stroke-dasharray="7 6" fill="none"/>'
                 f'<path class="chs" d="{r.rect(x,62,190,44)}" stroke="{INK}" stroke-width="2.4" fill="none" style="opacity:0"/>'
                 f'<text class="cht lab" x="{x+95}" y="92" text-anchor="middle" style="opacity:0">{s}</text></g>')

    # slot 1: the ceiling can say no (built from the first inn on the route)
    S.append(f'<g id="s1line" class="hide"><path d="M80 414L196 413.5M202 414L320 413.5M80 406L80 422M320 405L320 421" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    S.append('<g id="s1tag" class="hide"><use href="#kit-retainer-tag" transform="translate(152,370) scale(.8)"/></g>')
    S.append('<text id="s1few" class="hide small" x="344" y="404"><tspan x="344">a few hundred</tspan><tspan x="344" dy="25">a month</tspan></text>')

    # the viable window: no numbers, dashed unlabelled edges
    S.append(f'<g id="axis" class="hide"><path d="{r.seg(640,640,1060,640)}" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>')
    S.append('<text id="rooms" class="hide tiny" x="640" y="668">rooms</text>')
    S.append(f'<path id="wl" class="hide" d="M760 588L760 668" stroke="{STEEL}" stroke-width="2.5" stroke-dasharray="8 6" fill="none"/>')
    S.append(f'<path id="wr" class="hide" d="M900 588L900 668" stroke="{STEEL}" stroke-width="2.5" stroke-dasharray="8 6" fill="none"/>')
    S.append('<text id="small" class="hide small" x="692" y="578" text-anchor="middle">too small</text>')
    S.append('<g id="agy" class="hide"><use href="#kit-person" transform="translate(960,630) scale(.3)"/><use href="#kit-person" transform="translate(1020,630) scale(.3)"/></g>')
    S.append('<text id="served" class="hide small" x="990" y="566" text-anchor="middle">already served by an agency</text>')
    S.append('<text id="wide" class="hide small" x="830" y="700" text-anchor="middle">nobody knows how wide</text>')

    # slot 2: renewal (a good summer is not a result; the baseline is kept)
    S.append('<g id="s2" class="hide"><use href="#kit-calendar-leaf" transform="translate(80,420)"/>'
             '<text class="small" x="140" y="596" text-anchor="middle">a good summer</text></g>')
    S.append(f'<g id="folder" class="hide"><path d="M260 450L310 450L322 462L416 462L416 550L260 550Z" fill="{CARD}"/>'
             f'<path d="{r.seg(260,450,310,450,False)}{r.seg(322,462,416,462,False)}{r.seg(416,464,416,550,False)}{r.seg(414,550,260,550)}{r.seg(260,548,260,451,False)}M310 450L322 462" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>')
    S.append('<g id="basein" class="hide"><use href="#kit-sheet" transform="translate(274,474) scale(.4)"/>'
             '<text class="tiny" x="290" y="504">baseline</text></g>')
    S.append('<text id="keep" class="hide small" x="338" y="596" text-anchor="middle">kept</text>')

    # slot 3: access, at the owner's desk
    S.append('<g id="desk3" class="hide"><use href="#kit-table" transform="translate(80,580) scale(.8)"/>'
             '<use href="#kit-person" transform="translate(176,534) scale(.8)"/>'
             '<use href="#kit-sheet" transform="translate(220,542) scale(.26)"/>'
             '<text class="tiny" x="176" y="635" text-anchor="middle">owner</text>'
             '<text class="tiny" x="256" y="568" text-anchor="middle" style="font-size:14px">accounts</text></g>')
    S.append('<text id="guest" class="hide small" x="400" y="690" text-anchor="middle">You\'re a guest</text>')

    # the fork: stop, or move up (horizontal, never a rising arrow)
    S.append(label(r, 'f1', 40, 410, 350, 54, [('no owner funds $600 a month', 'small', 16, 35)]))
    S.append(label(r, 'f2', 40, 486, 350, 54, [('agencies own the band', 'small', 16, 35)]))
    S.append(f'<g id="stop" class="hide"><path d="M410 437L470 437M473 423L473 451" stroke="{STEEL}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             '<text class="label" x="488" y="447">stop</text></g>')
    S.append(f'<g id="up" class="hide"><path d="M410 513L600 513M589 504L601 513L589 522" stroke="{STEEL}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             '<text class="label" x="614" y="523">move up</text></g>')
    S.append(f'<path id="extl" class="hide" d="M1070 640L1250 640" stroke="{INK}" stroke-width="2.6" stroke-dasharray="12 8" fill="none"/>')
    S.append('<text id="extt" class="hide small" x="1250" y="700" text-anchor="end">40 to 80 rooms: the redesign</text>')
    S.append(f'<g id="ground" class="hide"><path d="M1086 654L1250 654" stroke="{STEEL}" stroke-width="1.3" fill="none"/>'
             '<text class="tiny" x="1250" y="674" text-anchor="end">their ground</text></g>')

    C = {k: c(w) for k, w in dict(whats='W002798', genuinely='W002799', three='W002803', ceiling='W002806',
                                  few='W002824', walk='W002830', viable='W002834', too='W002839', served='W002845',
                                  how='W002855', renewal='W002860', good='W002862', keep='W002876',
                                  access='W002887', owners='W002894', youre='W002900', if_='W002903', already='W002918',
                                  stop='W002922', move='W002924', forty='W002926', their='W002942').items()}
    tl = TL2()
    # S17's labels, evidence and band leave; the row, route and You stay
    tl.js("t.to('#band,#ul1,#ul2,#head,#sixl,#ev,#evfig,#evline,#evq,#rcpt,#nc,#illus',{autoAlpha:0,duration:.45,ease:'power1.inOut'}," + str(C['whats'] - .1) + ");")
    tl.fade('#h18', C['genuinely'])
    tl.js(f"t.fromTo('#ch1,#ch2,#ch3',{{autoAlpha:0}},{{autoAlpha:1,duration:.35,stagger:.12}},{C['three']});")

    def chip(n, at):
        tl.js(f"t.to('#ch{n} .cht, #ch{n} .chs',{{opacity:1,duration:.3}},{at});t.to('#ch{n} .chd',{{opacity:0,duration:.3}},{at});")

    # 1. the ceiling can say no: the first inn comes down out of the row
    chip(1, C['ceiling'])
    tl.dim('#inns5,#ceils,#route,#route2,#youl2', C['ceiling'], .25, .6)
    tl.mv('#inn0', C['ceiling'] + .1, INN0, (86, 430, .9), .9)
    tl.mv('#you', C['ceiling'] + .3, YOU0, (430, 560, .6), .9)
    tl.appear('#s1line', C['ceiling'] + 1.0)
    tl.fade('#s1tag', C['ceiling'] + 1.4, y=-8)
    tl.fade('#s1few', C['few'])
    tl.mv('#you', C['walk'], YOU0, (570, 560, .6), 1.0, 'power1.inOut'); tl.dim('#you', C['walk'], .4, 1.0)
    # the viable band: edges dashed, width unknown
    tl.appear('#axis', C['viable']); tl.appear('#rooms', C['viable'])
    tl.appear('#wl', C['too']); tl.fade('#small', C['too'])
    tl.appear('#wr', C['served']); tl.fade('#agy', C['served']); tl.fade('#served', C['served'] + .3)
    tl.fade('#wide', C['how'])
    tl.js(f"t.to('#wl',{{x:-26,duration:.7,yoyo:true,repeat:1,ease:'sine.inOut'}},{C['how']});")
    tl.js(f"t.to('#wr',{{x:26,duration:.7,yoyo:true,repeat:1,ease:'sine.inOut'}},{C['how']});")
    # 2. renewal replaces slot 1; the inn returns to the row
    chip(2, C['renewal']); tl.dim('#ch1', C['renewal'], .4)
    tl.js(f"t.to('#s1line,#s1tag,#s1few',{{autoAlpha:0,duration:.35}},{C['renewal'] - .1});")
    tl.mv('#inn0', C['renewal'], INN0, ROW_INN, .8)
    tl.dim('#inn0', C['renewal'], .25, .8)
    tl.dim('#you', C['renewal'], 0, .4)
    tl.dim('#small,#served,#wide,#rooms', C['renewal'], .4)
    tl.appear('#s2', C['good'])
    tl.appear('#folder', C['keep'] - .2)
    tl.js(f"t.fromTo('#basein',{{autoAlpha:0,y:-40}},{{autoAlpha:1,y:0,duration:.6,ease:'power2.out'}},{C['keep']});")
    tl.fade('#keep', C['keep'] + .5)
    # 3. access replaces slot 2
    chip(3, C['access']); tl.dim('#ch2', C['access'], .4)
    tl.js(f"t.to('#s2,#folder,#basein,#keep',{{autoAlpha:0,duration:.35}},{C['access'] - .1});")
    tl.appear('#desk3', C['owners'] - .2)
    tl.mv('#you', C['owners'] - .25, YOU0, (400, 610, .6), .05)
    tl.js(f"t.to('#you',{{opacity:1,duration:.6}},{C['owners'] - .1});")
    tl.fade('#guest', C['youre'])
    # the fork replaces slot 3; all three parts dim
    tl.dim('#ch3', C['if_'], .4)
    tl.js(f"t.to('#desk3,#guest,#you,#small,#served,#wide,#rooms',{{autoAlpha:0,duration:.4}},{C['if_'] - .1});")
    tl.slide('#f1', C['if_'] + .2, x=0)
    tl.slide('#f2', C['already'], x=0)
    tl.appear('#stop', C['stop'])
    tl.appear('#up', C['move'])
    tl.appear('#extl', C['forty'], .5)
    tl.fade('#extt', C['forty'] + .4)
    tl.js(f"t.to('#agy',{{x:150,duration:.8,ease:'power2.inOut'}},{C['their'] - .3});")
    tl.appear('#ground', C['their'] + .2)
    body = prev['body'] + '\n' + '\n'.join(S)
    defs_ids = prev['defs_ids'] + ['kit-calendar-leaf', 'kit-sheet', 'kit-table']
    return dict(body=body, lines=tl.lines, cues=C, css=prev['css'], defs_ids=defs_ids, dur=DUR, tl=tl,
                prev_lines=prev['prev_lines'] + [prev['lines']])


if __name__ == '__main__':
    sc = scene()
    html = page2('S18 the hard parts', 's18-root', 'ep009-s18', DUR, sc['body'], kit_defs(sc['defs_ids']), sc['tl'], sc['cues'],
                 prev_lines=sc['prev_lines'], css=sc['css'])
    (HERE.parent / 'index.html').write_text(html)
    print('wrote', DUR)
