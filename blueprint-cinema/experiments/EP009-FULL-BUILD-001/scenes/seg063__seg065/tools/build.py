#!/usr/bin/env python3
"""EP009 S19 + S20a (seg063, seg064, seg065): the first 30 and 90 days on the same objects; boxes stay unchecked;
a dashed "Say" marker. Frame 0 restores seg062's last frame. Generates ../index.html."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from act4lib import *  # noqa

MI, MO = 1064.333333, 1125.791667
DUR = round((round(MO * 24) - round(MI * 24)) / 24, 6)
c = lambda w, o=0.0: cue(w, MI, o)

# ---------- inherited S18 end state ----------
src_path = HERE.parent.parent / 'seg061__seg062/tools/build.py'
src = src_path.read_text().rsplit("defs = kit_defs", 1)[0]
ns = {'__file__': str(src_path), '__name__': 's18_layout'}
exec(compile(src, str(src_path), 'exec'), ns)
prev = ns['body'].replace('<g id="prev">', '<g id="prev17">', 1)
S18_VISIBLE = ['h18', 'slot1', 'slot2', 'slot3', 't1', 't2', 't3', 's1inn', 's1line', 's1tag', 's1few', 'cal', 'summer', 'slow',
               'folder', 'basein', 'keep', 'desk3', 'acct', 'guest', 'axis', 'wl', 'small', 'wr', 'agy', 'unk', 'f1', 'f2',
               'stop', 'up', 'extl', 'extt', 'ground']
css = ('<style>#prev17{visibility:hidden;opacity:0}' + ''.join(f'#prev18 #{i}{{visibility:visible;opacity:1}}' for i in S18_VISIBLE)
       + '#prev18 #youl{visibility:hidden;opacity:0}#prev18 #you2{transform:translate(820px,-252px)}</style>')

r = Rough(1930)
S = [f'<g id="prev18">{prev}</g>']

# ---------- timeline ----------
S.append(f'<g id="tline" class="hide"><path d="{r.seg(40,120,1240,120)}" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
         f'<path d="M40 110L40 130M640 108L640 132M1240 110L1240 130" stroke="{INK}" stroke-width="2" fill="none"/>'
         '<text class="tiny" x="40" y="152">day 1</text><text class="tiny" x="640" y="152" text-anchor="middle">day 30</text>'
         '<text class="tiny" x="1240" y="152" text-anchor="end">day 90</text></g>')
S.append('<text id="d130" class="hide label" x="340" y="102" text-anchor="middle">Days 1 to 30</text>')
S.append('<text id="bnt" class="hide small" x="340" y="176" text-anchor="middle">building, not thinking</text>')
S.append('<text id="d3190" class="hide label" x="1080" y="102" text-anchor="middle">Days 31 to 90</text>')

# ---------- the audit card (S14) with its three parts ----------
AX, AY, AW, AH = 40, 192, 580, 150
S.append(f'<g id="audit" class="hide"><path d="M{AX} {AY}L{AX+AW} {AY}L{AX+AW} {AY+AH}L{AX} {AY+AH}Z" fill="{CARD}"/>'
         f'<path d="{r.rect(AX,AY,AW,AH)}" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
         f'<text class="lab" x="{AX+20}" y="{AY+36}">Build the audit</text></g>')
S.append(f'<g id="ap1" class="hide"><path d="M230 212L300 212L300 300L230 300Z" fill="{SHEET}"/><path d="{r.rect(230,212,70,88)}" class="steel"/>'
         '<path d="M242 236L288 236M242 256L288 256M242 276L276 276" class="light"/>'
         '<text class="tiny" x="265" y="326" text-anchor="middle">checklist</text></g>')
S.append('<g id="ap2" class="hide"><use href="#kit-ceiling-slip-blank" transform="translate(372,206) scale(.22)"/>'
         '<text class="tiny" x="405" y="326" text-anchor="middle">ceiling calculator</text></g>')
S.append('<g id="ap3" class="hide"><use href="#kit-phone" transform="translate(532,212) scale(.62)"/>'
         '<text class="tiny" x="555" y="326" text-anchor="middle">phone-side test</text></g>')

# ---------- three inns in the band ----------
IX = [118, 308, 498]
S.append('<g id="inn3" class="hide">' + ''.join(f'<use href="#kit-inn-mini" transform="translate({x-48},362) scale(.4)"/>' for x in IX) + '</g>')
S.append('<text id="free" class="hide tiny" x="118" y="446" text-anchor="middle">free, an owner you know</text>')
S.append(f'<g id="watch" class="hide"><circle cx="186" cy="378" r="13" fill="{SHEET}" stroke="{INK}" stroke-width="2.2"/>'
         f'<path d="M186 378L186 369M186 378L192 382M182 362L190 362M186 362L186 365" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>')
S.append('<text id="fee" class="hide tiny" x="403" y="446" text-anchor="middle">at the audit fee</text>')
S.append('<g id="ceil3" class="hide">' + ''.join(
    f'<path d="M{x-48} 470L{x-3} 469.5M{x+3} 470L{x+48} 469.5M{x-48} 463L{x-48} 477M{x+48} 462L{x+48} 476" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    f'<use href="#kit-retainer-tag" transform="translate({x-29},478) scale(.6)"/>' for x in IX) + '</g>')
S.append('<g id="ans" class="hide">' + ''.join(f'<path d="M{x-44} 528L{x+44} 528" class="steel"/>' for x in IX)
         + '<text class="tiny" x="308" y="550" text-anchor="middle">write down the answer</text></g>')

# ---------- five calls ----------
S.append('<g id="phone5" class="hide"><use href="#kit-phone" transform="translate(44,586) scale(.45)"/><text class="tiny" x="64" y="672" text-anchor="middle">five calls</text></g>')
FIG = [(150, 'c1'), (220, 'c2'), (360, 'c3'), (500, 'c4'), (570, 'c5')]
for x, gid in FIG:
    S.append(f'<g id="{gid}" class="hide"><path d="M{x-12} 603Q{x} 592 {x+12} 603M{x-19} 596Q{x} 580 {x+19} 596" class="steel"/>'
             f'<use href="#kit-person" transform="translate({x},652) scale(.3)"/></g>')
S.append('<text id="cl1" class="hide tiny" x="168" y="692" text-anchor="middle">PMS partner managers</text>')
S.append('<text id="cl2" class="hide tiny" x="384" y="692" text-anchor="middle">innkeeper association</text>')
S.append('<text id="cl3" class="hide tiny" x="535" y="692" text-anchor="middle">agencies</text>')

# ---------- success at day 30: boxes stay unchecked ----------
S.append(f'<g id="succ" class="hide"><path d="M640 160L640 196" stroke="{STEEL}" stroke-width="1.3" fill="none"/>'
         f'<path d="M660 188L1240 188L1240 346L660 346Z" fill="{SHEET}"/><path d="{r.rect(660,188,580,158)}" class="steel"/>'
         '<text class="lab" x="684" y="224">Success at day 30</text></g>')
SUC = [('sc1', 262, 'one paid audit'), ('sc2', 298, 'one yes to a retainer under the ceiling'), ('sc3', 334, 'an audit inside 15 hours')]
for gid, y, s in SUC:
    S.append(f'<g id="{gid}" class="hide"><use href="#kit-checkbox-empty" transform="translate(686,{y-20})"/>'
             f'<text class="small" x="724" y="{y}">{s}</text></g>')

# ---------- days 31 to 90 ----------
D = [('dd1', 404, 'deliver the first retainer'), ('dd2', 442, '8 h assumption → real hours'), ('dd3', 480, 'rerun the arithmetic')]
for gid, y, s in D:
    S.append(f'<g id="{gid}" class="hide"><path d="M672 {y-7}L688 {y-7}" class="steel"/><text class="small" x="700" y="{y}">{s}</text></g>')
S.append('<text id="decide" class="hide lab" x="672" y="540">decide</text>')
OPT = [('o1', 672, 'keep going'), ('o2', 862, 'move the band up'), ('o3', 1052, 'sell the audit only')]
for gid, x, s in OPT:
    S.append(label(r, gid, x, 562, 180, 52, [(s, 'small', 14, 33)]))
S.append(f'<path id="fork" class="hide" d="M700 548L1142 548M762 548L762 562M952 548L952 562M1142 548L1142 562" stroke="{STEEL}" stroke-width="1.6" fill="none"/>')

# ---------- S20a: "Say" marker, dashed = supposed ----------
S.append(f'<g id="say" class="hide"><path d="M760 116L760 70" stroke="{STEEL}" stroke-width="2.5" stroke-dasharray="6 5" fill="none"/>'
         f'<path d="M660 30L920 30L920 68L660 68Z" fill="{PAPER}"/>'
         f'<path d="M660 30L920 30L920 68L660 68Z" stroke="{STEEL}" stroke-width="2" stroke-dasharray="9 7" fill="none"/>'
         '<text class="small" x="790" y="56" text-anchor="middle">Say: first retainer running</text></g>')

body = '\n'.join(S)
defs = kit_defs(['kit-phone', 'kit-practice-figure', 'kit-inn-mini', 'kit-person', 'kit-retainer-tag', 'kit-calendar-leaf',
                 'kit-sheet', 'kit-table', 'kit-ceiling-slip-blank', 'kit-checkbox-empty'])
C = {k: c(w) for k, w in dict(before='W002944', first='W002951', building='W002955', build='W002958', checklist='W002962',
                              ceiling='W002964', phone='W002968', three='W002975', one='W002980', start='W002989',
                              two='W002992', put='W002997', write='W003011', make='W003016', two_pms='W003019',
                              innkeeper='W003027', two_agy='W003035', success='W003042', one_paid='W003047',
                              one_yes='W003050', inside='W003061', days='W003064', deliver='W003069', real='W003079',
                              rerun='W003081', decide='W003085', keep='W003086', move='W003088', sell='W003093',
                              say='W003097').items()}
tl = TL()
tl.out('#prev18', C['before'], .5)
tl.draw('#tline path:first-child', C['before'] + .7, .9)
tl.appear('#tline', C['before'] + .7, .2)
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
tl.appear('#succ', C['success'])
tl.fade('#sc1', C['one_paid']); tl.fade('#sc2', C['one_yes']); tl.fade('#sc3', C['inside'])
tl.fade('#d3190', C['days'])
tl.fade('#dd1', C['deliver']); tl.fade('#dd2', C['real']); tl.fade('#dd3', C['rerun'])
tl.fade('#decide', C['decide'])
tl.appear('#fork', C['keep'] - .1)
tl.fade('#o1', C['keep']); tl.fade('#o2', C['move']); tl.fade('#o3', C['sell'])
tl.appear('#say', C['say'], .35)

html = page('S19 the first 30 and 90 days', 's19-root', 'ep009-s19', DUR, body, defs, tl, C)
html = html.replace('</head>', css + '</head>', 1)
(HERE.parent / 'index.html').write_text(html)
print('wrote', DUR)
