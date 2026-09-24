#!/usr/bin/env python3
"""EP009 S19 + S20a (seg063, seg064, seg065): the first 30 and 90 days; boxes stay unchecked; a dashed "Say" marker.
Fix round 1 (B-15, B-24). Frame 0 is seg062's revised last frame (replayed). No blank page: on "Before" S18's room
axis lifts to the top and becomes the 90-day timeline. Days 1 to 30 use the full frame until "Success", then shrink
into the left half (drawings only) while success and days 31 to 90 take the right. "PMS" is spelled out as spoken.
Generates ../index.html."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa
from r1lib import TL2, page2, load_scene

MI, MO = 1064.333333, 1125.791667
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)


def scene():
    prev = load_scene('seg061__seg062')
    c = lambda w, o=0.0: cue(w, MI, o)
    r = Rough(1930)
    S = []
    # timeline (starts where S18's axis was)
    S.append(f'<g id="tline" class="hide" transform="matrix(.5083,0,0,1,619.67,520)"><path d="{r.seg(40,120,1240,120)}" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>')
    S.append(f'<g id="ticks" class="hide"><path d="M40 110L40 130M640 108L640 132M1240 110L1240 130" stroke="{INK}" stroke-width="2" fill="none"/>'
             '<text class="tiny" x="40" y="152">day 1</text><text class="tiny" x="640" y="152" text-anchor="middle">day 30</text>'
             '<text class="tiny" x="1240" y="152" text-anchor="end">day 90</text></g>')
    S.append('<text id="d130" class="hide label" x="340" y="102" text-anchor="middle">Days 1 to 30</text>')
    S.append('<text id="bnt" class="hide small" x="340" y="178" text-anchor="middle">building, not thinking</text>')
    S.append('<text id="d3190" class="hide label" x="940" y="102" text-anchor="middle">Days 31 to 90</text>')

    G = []  # the days 1 to 30 group (full frame)
    AX, AY, AW, AH = 40, 200, 580, 200
    G.append(f'<g id="audit" class="hide"><path d="M{AX} {AY}L{AX+AW} {AY}L{AX+AW} {AY+AH}L{AX} {AY+AH}Z" fill="{CARD}"/>'
             f'<path d="{r.rect(AX,AY,AW,AH)}" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<text class="label g30t" x="{AX+22}" y="{AY+40}">Build the audit</text></g>')
    G.append(f'<g id="ap1" class="hide"><path d="M90 262L174 262L174 368L90 368Z" fill="{SHEET}"/><path d="{r.rect(90,262,84,106)}" class="steel"/>'
             '<path d="M104 290L160 290M104 314L160 314M104 338L146 338" class="light"/>'
             '<text class="small g30t" x="132" y="392" text-anchor="middle">checklist</text></g>')
    G.append('<g id="ap2" class="hide"><use href="#kit-ceiling-slip-blank" transform="translate(290,254) scale(.26)"/>'
             '<text class="small g30t" x="330" y="392" text-anchor="middle">ceiling calculator</text></g>')
    G.append('<g id="ap3" class="hide"><use href="#kit-phone" transform="translate(504,262) scale(.76)"/>'
             '<text class="small g30t" x="533" y="392" text-anchor="middle">phone-side test</text></g>')
    IX = [770, 960, 1150]
    G.append('<g id="inn3" class="hide">' + ''.join(f'<use href="#kit-inn-mini" transform="translate({x-60},212) scale(.5)"/>' for x in IX) + '</g>')
    G.append('<text id="free" class="hide small g30t" x="770" y="318" text-anchor="middle">free, an owner you know</text>')
    G.append(f'<g id="watch" class="hide"><circle cx="846" cy="222" r="15" fill="{SHEET}" stroke="{INK}" stroke-width="2.2"/>'
             f'<path d="M846 222L846 212M846 222L853 226M841 204L851 204M846 204L846 207" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>')
    G.append('<text id="fee" class="hide small g30t" x="1055" y="318" text-anchor="middle">at the audit fee</text>')
    G.append('<g id="ceil3" class="hide">' + ''.join(
        f'<path d="M{x-56} 346L{x-3} 345.5M{x+3} 346L{x+56} 345.5M{x-56} 339L{x-56} 353M{x+56} 338L{x+56} 352" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        f'<use href="#kit-retainer-tag" transform="translate({x-34},354) scale(.7)"/>' for x in IX) + '</g>')
    G.append('<g id="ans" class="hide">' + ''.join(f'<path d="M{x-52} 408L{x+52} 408" class="steel"/>' for x in IX)
             + '<text class="small g30t" x="960" y="436" text-anchor="middle">write down the answer</text></g>')
    G.append('<g id="phone5" class="hide"><use href="#kit-phone" transform="translate(56,490) scale(.62)"/><text class="small g30t" x="80" y="616" text-anchor="middle">five calls</text></g>')
    FIG = [(260, 'c1'), (400, 'c2'), (660, 'c3'), (920, 'c4'), (1060, 'c5')]
    for x, gid in FIG:
        G.append(f'<g id="{gid}" class="hide"><path d="M{x-16} 540Q{x} 526 {x+16} 540M{x-25} 531Q{x} 510 {x+25} 531" class="steel"/>'
                 f'<use href="#kit-person" transform="translate({x},640) scale(.46)"/></g>')
    G.append('<text id="cl1" class="hide small g30t" x="330" y="690" text-anchor="middle">property management system partner managers</text>')
    G.append('<text id="cl2" class="hide small g30t" x="660" y="690" text-anchor="middle">innkeeper association</text>')
    G.append('<text id="cl3" class="hide small g30t" x="990" y="690" text-anchor="middle">agencies</text>')
    S.append('<g id="g30" transform="matrix(1,0,0,1,0,0)">' + ''.join(G) + '</g>')

    # success at day 30: boxes stay unchecked
    S.append(f'<g id="succ" class="hide"><path d="M680 188L1240 188L1240 346L680 346Z" fill="{SHEET}"/><path d="{r.rect(680,188,560,158)}" class="steel"/>'
             '<text class="label" x="704" y="228">Success at day 30</text></g>')
    SUC = [('sc1', 266, 'one paid audit'), ('sc2', 302, 'one yes to a retainer under the ceiling'), ('sc3', 338, 'an audit inside 15 hours')]
    for gid, y, s in SUC:
        S.append(f'<g id="{gid}" class="hide"><use href="#kit-checkbox-empty" transform="translate(706,{y-20})"/>'
                 f'<text class="small" x="744" y="{y}">{s}</text></g>')
    D = [('dd1', 400, 'deliver the first retainer'), ('dd2', 438, '8 h assumption → real hours'), ('dd3', 476, 'rerun the arithmetic')]
    for gid, y, s in D:
        S.append(f'<g id="{gid}" class="hide"><path d="M692 {y-7}L708 {y-7}" class="steel"/><text class="small" x="720" y="{y}">{s}</text></g>')
    S.append('<text id="decide" class="hide label" x="640" y="548" text-anchor="middle">decide</text>')
    OPT = [('o1', 130, 'keep going'), ('o2', 520, 'move the band up'), ('o3', 910, 'sell the audit only')]
    for gid, x, s in OPT:
        S.append(label(r, gid, x, 604, 240, 56, [(s, 'label', 18, 37)]).replace('class="label"', 'class="label" style="font-size:24px"'))
    S.append(f'<path id="fork" class="hide" d="M250 580L1030 580M640 562L640 580M250 580L250 604M640 580L640 604M1030 580L1030 604" stroke="{STEEL}" stroke-width="1.6" fill="none"/>')

    # S20a: "Say" marker, dashed = supposed
    S.append(f'<g id="say" class="hide"><path d="M760 116L760 70" stroke="{STEEL}" stroke-width="2.5" stroke-dasharray="6 5" fill="none"/>'
             f'<path d="M660 30L920 30L920 68L660 68Z" fill="{PAPER}"/>'
             f'<path d="M660 30L920 30L920 68L660 68Z" stroke="{STEEL}" stroke-width="2" stroke-dasharray="9 7" fill="none"/>'
             '<text class="small" x="790" y="56" text-anchor="middle">Say: first retainer running</text></g>')

    C = {k: c(w) for k, w in dict(before='W002944', first='W002951', building='W002955', build='W002958', checklist='W002962',
                                  ceiling='W002964', phone='W002968', three='W002975', one='W002980', start='W002989',
                                  two='W002992', put='W002997', write='W003011', make='W003016', two_pms='W003019',
                                  innkeeper='W003027', two_agy='W003035', success='W003042', one_paid='W003047',
                                  one_yes='W003050', inside='W003061', days='W003064', deliver='W003069', real='W003079',
                                  rerun='W003081', decide='W003085', keep='W003086', move='W003088', sell='W003093',
                                  say='W003097').items()}
    tl = TL2()
    # "Before you get anywhere near that": S18 leaves; its axis lifts and becomes the timeline
    s18 = ['h18', 'ch1', 'ch2', 'ch3', 'f1', 'f2', 'stop', 'up', 'wl', 'wr', 'agy', 'extt', 'ground', 'inn0', 'inns5', 'ceils', 'route', 'route2', 'youl2']
    tl.js("t.to('" + ','.join('#' + i for i in s18) + f"',{{autoAlpha:0,duration:1.0,ease:'power1.inOut'}},{C['before']});")
    tl.appear('#tline', C['before'] + .1, .25)
    tl.js(f"t.to('#axis,#extl',{{autoAlpha:0,duration:.25}},{C['before'] + .1});")
    tl.js(f"t.to('#tline',{{attr:{{transform:'matrix(1,0,0,1,0,0)'}},duration:1.1,ease:'power2.inOut'}},{C['before'] + .2});")
    tl.appear('#ticks', C['before'] + 1.1, .4)
    tl.fade('#d130', C['first'])
    tl.fade('#bnt', C['building'])
    tl.appear('#audit', C['build'])
    tl.fade('#ap1', C['checklist']); tl.fade('#ap2', C['ceiling']); tl.fade('#ap3', C['phone'])
    tl.appear('#inn3', C['three'])
    tl.fade('#free', C['one']); tl.appear('#watch', C['start'])
    tl.fade('#fee', C['two'])
    tl.appear('#ceil3', C['put'])
    tl.appear('#ans', C['write'])
    tl.appear('#phone5', C['make'])
    tl.appear('#c1', C['two_pms'], .2)
    tl.appear('#c2', C['two_pms'] + .25, .2)
    tl.fade('#cl1', C['two_pms'] + .6)
    tl.appear('#c3', C['innkeeper'], .2); tl.fade('#cl2', C['innkeeper'] + .4)
    tl.appear('#c4', C['two_agy'], .2)
    tl.appear('#c5', C['two_agy'] + .25, .2)
    tl.fade('#cl3', C['two_agy'] + .6)
    # "Success": days 1 to 30 shrink into the left half as drawings; success takes the right
    tl.js(f"t.to('#g30 .g30t, #bnt',{{autoAlpha:0,duration:.35}},{C['success'] - .15});")
    tl.js(f"t.to('#g30',{{attr:{{transform:'matrix(.5,0,0,.5,20,98)'}},opacity:.5,duration:.9,ease:'power2.inOut'}},{C['success']});")
    tl.slide('#succ', C['success'] + .3, x=40)
    tl.fade('#sc1', C['one_paid']); tl.fade('#sc2', C['one_yes']); tl.fade('#sc3', C['inside'])
    tl.fade('#d3190', C['days'])
    tl.fade('#dd1', C['deliver']); tl.fade('#dd2', C['real']); tl.fade('#dd3', C['rerun'])
    tl.fade('#decide', C['decide'])
    tl.appear('#fork', C['keep'] - .1)
    tl.fade('#o1', C['keep']); tl.fade('#o2', C['move']); tl.fade('#o3', C['sell'])
    tl.appear('#say', C['say'], .35)
    body = prev['body'] + '\n' + '\n'.join(S)
    defs_ids = prev['defs_ids'] + ['kit-ceiling-slip-blank', 'kit-checkbox-empty']
    return dict(body=body, lines=tl.lines, cues=C, css=prev['css'], defs_ids=defs_ids, dur=DUR, tl=tl,
                prev_lines=prev['prev_lines'] + [prev['lines']])


if __name__ == '__main__':
    sc = scene()
    html = page2('S19 the first 30 and 90 days', 's19-root', 'ep009-s19', DUR, sc['body'], kit_defs(sc['defs_ids']), sc['tl'], sc['cues'],
                 prev_lines=sc['prev_lines'], css=sc['css'])
    (HERE.parent / 'index.html').write_text(html)
    print('wrote', DUR)
