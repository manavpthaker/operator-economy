"""Build a broader business-dependence model while preserving R17."""
from pathlib import Path
import hashlib, json, os, re, shutil

root=Path(__file__).resolve().parent
base=root.parent/'r17-clear-customer-orders'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for p in base.rglob('*') if p.is_file() and (p.relative_to(base).parts[0] in ('public','compositions') or p.name=='index.html')]
pins={str(p.relative_to(base)):sha(p) for p in files}
assert pins['index.html']=='c5f9aebaae02414e73987959d8a75beb751bb0da2c1fa4979796adfda5bbf83c'
assert pins['compositions/handoff.html']=='0aa44671c3b48abc9123c3c843a5ff3807e8331daa9136f8fecb24aaae306881'
for p in files:
    rel=p.relative_to(base)
    if str(rel) in ('index.html','compositions/handoff.html'):continue
    out=root/rel;out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():assert sha(out)==sha(p)
    elif rel.parts[0]=='public':os.link(p,out)
    else:shutil.copy2(p,out)
index=(base/'index.html').read_text().replace('EP007 R17 — clear customer orders','EP007 R18 — business dependence').replace('ep007-r17','ep007-r18').replace('r17-handoff','r18-handoff')
(root/'index.html').write_text(index)
source=(base/'compositions/handoff.html').read_text()
def group(name):
    match=re.search(r'<g id="r17-'+name+r'".*?</g>',source,re.S)
    assert match,name
    return match.group().replace('r17-','r18-')
owner,worker,bench=group('owner'),group('worker'),group('bench')

html='''<!DOCTYPE html><html><head><meta charset="utf-8"><title>The business without its owner</title></head><body><template>
<style>
@font-face{font-family:Zodiak;src:url('public/fonts/zodiak-700.woff2');font-weight:700}
@font-face{font-family:Supreme;src:url('public/fonts/supreme-400.woff2');font-weight:400}
@font-face{font-family:Supreme;src:url('public/fonts/supreme-500.woff2');font-weight:500}
#r18-handoff-root{position:absolute;inset:0;width:1280px;height:720px;color:#173530;background:#F5F0E6}
.r18-heading{position:absolute;left:88px;top:63px;margin:0;font:700 48px/1.2 Zodiak,Georgia,serif;letter-spacing:-.025em}
.r18-stage{position:absolute;inset:0;width:1280px;height:720px}
.r18-stage .sketch{fill:none;stroke:#173530;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.r18-stage .light{stroke:#586D74;stroke-width:1.1;opacity:.72}
.r18-stage .route{fill:none;stroke:#586D74;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.r18-stage .route-retrace{stroke:#586D74;stroke-width:1.2;opacity:.72}
.r18-stage .accent{stroke:#B5482F;stroke-width:2.8}
.r18-label{position:absolute;top:218px;margin:0;width:280px;text-align:center;font:400 29px/1.25 Supreme,sans-serif}
#r18-owner-label,#r18-away-label{left:494px}#r18-team-label{left:892px}
.r18-area{position:absolute;left:104px;width:229px;text-align:center;margin:0;font:500 32px/1.2 Supreme,sans-serif}
#r18-customers-label{top:231px}#r18-decisions-label{top:381px}#r18-operations-label{top:531px}
#r18-heading-after,#r18-away-label,#r18-open-question,.r18-reveal{opacity:0;visibility:hidden}
</style>
<div id="r18-handoff-root" data-composition-id="r18-handoff" data-start="0" data-duration="4.875" data-width="1280" data-height="720" data-fps="24">
<h1 id="r18-heading-before" class="r18-heading">What depends on her?</h1>
<h1 id="r18-heading-after" class="r18-heading">What still works without her?</h1>
<svg class="r18-stage" viewBox="0 0 1280 720" role="img" aria-label="Illustrative business-dependence test. Customers, decisions and operations connect through the owner to the team. When the owner is absent for a month, the business areas and team remain, while her connections are left as an open question. No failure outcome is established.">
<!-- Finite hand-drawn label tabs, not fabricated operational records. -->
<g class="sketch">
<path d="M101 211 L195 209 M205 209 L331 211 L335 272 M331 291 L230 293 M219 293 L99 290 L100 236 M98 230 L101 214" />
<path class="light" d="M96 218 L95 268 M106 295 L184 295 M245 295 L319 294 M337 218 L337 259" />
<path d="M99 360 L171 359 M185 360 L333 358 L335 422 M335 431 L249 441 M237 441 L101 438 L102 389 M100 381 L99 365" />
<path class="light" d="M95 367 L97 404 M98 414 L99 433 M109 444 L191 444 M277 443 L327 435 M338 366 L339 419" />
<path d="M102 508 L219 510 M229 510 L331 507 L334 555 M334 565 L333 589 L265 591 M253 591 L99 590 L101 541 M101 533 L102 513" />
<path class="light" d="M97 517 L96 557 M107 595 L198 595 M243 594 L312 593 M338 518 L337 550 M337 566 L336 583" />
</g>
<!-- Outer branches and team-side route persist when the owner is withdrawn. -->
<g id="r18-outer-routes" class="route">
<g class="r18-reveal r18-inbound"><path d="M337 250 C399 249 457 278 520 340" /><path class="route-retrace" d="M345 254 C393 254 424 263 457 287 M474 303 L514 339" /></g>
<g class="r18-reveal r18-inbound"><path d="M336 400 C404 399 463 414 520 428" /><path class="route-retrace" d="M347 405 C396 403 437 413 468 421 M483 425 L515 433" /></g>
<g class="r18-reveal r18-inbound"><path d="M336 550 C408 551 466 539 520 518" /><path class="route-retrace" d="M347 554 C402 556 449 548 481 536 M490 533 L515 523" /></g>
<g class="r18-reveal r18-outbound"><path d="M760 486 C851 488 949 508 1037 520 M1022 509 L1039 520 L1022 527" /><path class="route-retrace" d="M773 491 L839 494 M851 495 L928 507 M943 510 L1013 519" /></g>
</g>
<!-- Only these central relationship pieces disappear, leaving an unresolved junction. -->
<g id="r18-owner-connections" class="route">
<g class="r18-reveal r18-central"><path d="M520 340 C559 376 590 444 633 485" /><path class="route-retrace" d="M529 356 L560 394 M574 418 L623 478" /></g>
<g class="r18-reveal r18-central"><path d="M520 428 C558 439 592 470 633 485" /><path class="route-retrace" d="M529 434 L565 451 M575 458 L623 483" /></g>
<g class="r18-reveal r18-central"><path d="M520 518 C561 502 594 492 633 485" /><path class="route-retrace" d="M531 519 L567 504 M579 501 L624 489" /></g>
<g class="r18-reveal r18-outbound"><path d="M633 485 L760 486" /><path class="route-retrace" d="M645 490 L709 489 M719 490 L754 491" /></g>
</g>
<g transform="translate(170 250) scale(.78)">OWNER_SOURCE</g>
<g transform="translate(826 195) scale(.62)">WORKER_SOURCE</g>
<g transform="translate(0 75)">
<g class="sketch"><path d="M1065 327 L1097 349 L1084 394 L1074 404 M1057 340 L1080 355 L1070 389 L1064 399 L1074 404 M1071 392 L1080 397" /><path class="light" d="M1076 343 L1090 352 M1085 369 L1077 389 M1068 398 L1074 399" /></g>
BENCH_SOURCE
</g>
<g id="r18-open-question" class="sketch accent">
<path id="r18-question-curve" d="M606 401 Q607 372 633 369 M640 369 Q669 371 673 396 M673 403 Q669 420 650 428 M646 435 L643 458" />
<path id="r18-question-retrace" class="light" d="M602 398 Q601 378 619 370 M648 372 Q668 376 676 392 M654 427 L648 449" />
<path id="r18-question-dot" d="M641 474 L647 474 L647 481 L640 481 M638 485 L649 483" />
</g>
</svg>
<p id="r18-customers-label" class="r18-area">Customers</p><p id="r18-decisions-label" class="r18-area">Decisions</p><p id="r18-operations-label" class="r18-area">Operations</p>
<p id="r18-owner-label" class="r18-label">Owner</p><p id="r18-away-label" class="r18-label">Absent for a month</p><p id="r18-team-label" class="r18-label">Team</p>
</div>
<script>(()=>{
const tl=gsap.timeline({paused:true});
function trace(selector,start,duration){
  const groups=Array.from(document.querySelectorAll(selector));
  tl.set(groups,{autoAlpha:1},start);
  groups.forEach(g=>g.querySelectorAll('path').forEach(p=>{
    const len=p.getTotalLength();
    tl.fromTo(p,{strokeDasharray:len+' '+len,strokeDashoffset:len},{strokeDashoffset:0,duration,ease:'none'},start);
  }));
}
trace('.r18-inbound',6/24,19/24);
trace('.r18-central',16/24,19/24);
trace('.r18-outbound',28/24,14/24);
tl.set(['#r18-owner','#r18-owner-label','#r18-owner-connections','#r18-heading-before'],{autoAlpha:0},56/24);
tl.set(['#r18-away-label','#r18-heading-after'],{autoAlpha:1},56/24);
trace('#r18-open-question',60/24,14/24);
window.__timelines=window.__timelines||{};window.__timelines['r18-handoff']=tl;
})();</script></template></body></html>
'''.replace('OWNER_SOURCE',owner).replace('WORKER_SOURCE',worker).replace('BENCH_SOURCE',bench)
(root/'compositions/handoff.html').write_text(html)
pkg=json.loads((base/'package.json').read_text());pkg['name']='ep007-r18-business-dependence'
(root/'package.json').write_text(json.dumps(pkg,indent=2)+'\n')
(root/'BASELINE-PINS.json').write_text(json.dumps({'baseline':str(base),'sha256':pins},indent=2)+'\n')
verify=(base/'verify-r17.py').read_text().replace("base=root.parent/'r16-customer-handover'","base=root.parent/'r17-clear-customer-orders'").replace("'r17-handoff'","'r18-handoff'")
(root/'verify-r18.py').write_text(verify)
assert all(sha(base/rel)==h for rel,h in pins.items())
print(f'R18 created; {len(pins)} R17 runtime files unchanged.')
