"""Create isolated source candidate, preserving the inspected R15 baseline."""
from pathlib import Path
import re, shutil, json, hashlib, os

root = Path(__file__).resolve().parent
baseline = root.parent / 'r15-post-title'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
baseline_files = [p for p in baseline.rglob('*') if p.is_file() and (p.relative_to(baseline).parts[0] in ('public','compositions') or p.name == 'index.html')]
pins = {str(p.relative_to(baseline)): sha(p) for p in baseline_files}
assert pins['index.html'] == '1e5f8f725927268741ef8f624a8f865a62f5cfba0dccd90d6e02d727bfd181ae'
assert pins['compositions/handoff.html'] == 'ddaaa423c0f8ba8c852063688caf727d1a3ba9dd82ed6f9d5bb12b4ffbcaea14'
(root / 'compositions').mkdir(exist_ok=True)
for p in baseline_files:
    rel = p.relative_to(baseline)
    if rel.parts[0] != 'public' and str(rel) not in ['compositions/question.html','compositions/sting.html','compositions/title.html']:
        continue
    out = root / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        assert sha(out) == sha(p)
    elif rel.parts[0] == 'public':
        os.link(p, out) # Immutable local media, no duplicate large-file storage.
    else:
        shutil.copy2(p, out)

index = (baseline / 'index.html').read_text().replace('EP007 R15 — post-title explanation', 'EP007 R16 — customer relationship test').replace('ep007-r15','ep007-r16').replace('r13-handoff','r16-handoff')
(root / 'index.html').write_text(index)
pkg = {'name':'ep007-r16-customer-handover','private':True,'type':'module','scripts':{k:f'npx hyperframes@0.8.33 {k}' for k in ['check','preview','snapshot']}}
(root / 'package.json').write_text(json.dumps(pkg,indent=2)+'\n')

source = (baseline / 'compositions/handoff.html').read_text()
def group(gid):
    start = source.index('<g ', source.index('id="'+gid+'"')-40)
    # These two retained actor groups contain no nested g element.
    end = source.index('</g>',start)+4
    s = source[start:end]
    s = re.sub(r' data-hf-id="[^"]*"','',s)
    s = re.sub(r' transform="[^"]*"','',s)
    return s.replace('r13-','r16-')
owner = group('r13-owner')
worker = group('r13-worker')

html = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>The customer relationship test</title></head><body><template>
<style>
@font-face{font-family:Zodiak;src:url('public/fonts/zodiak-700.woff2');font-weight:700}
@font-face{font-family:Supreme;src:url('public/fonts/supreme-400.woff2');font-weight:400}
#r16-handoff-root{position:absolute;inset:0;width:1280px;height:720px;color:#173530}
.r16-field{position:absolute;inset:0;background:#F5F0E6}
.r16-heading{position:absolute;left:88px;top:63px;margin:0;font:700 48px/1.2 Zodiak,Georgia,serif;letter-spacing:-.025em}
.r16-stage{position:absolute;inset:0;width:1280px;height:720px}
.r16-stage .sketch{fill:none;stroke:#173530;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.r16-stage .light{stroke:#586D74;stroke-width:1.1;opacity:.72}
.r16-stage .route{fill:none;stroke:#586D74;stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round}
.r16-stage .accent{stroke:#B5482F;stroke-width:2.4}
.r16-label{position:absolute;top:175px;margin:0;width:240px;text-align:center;font:400 29px/1.25 Supreme,sans-serif}
#r16-customer-label{left:118px}#r16-owner-label,#r16-away-label{left:514px}#r16-team-label{left:912px}
#r16-away-label,#r16-request-two,#r16-open-question{opacity:0;visibility:hidden}
</style>
<div id="r16-handoff-root" data-composition-id="r16-handoff" data-start="0" data-duration="4.875" data-width="1280" data-height="720" data-fps="24">
<div class="r16-field"></div><h1 class="r16-heading">Will customers stay?</h1>
<svg class="r16-stage" viewBox="0 0 1280 720" role="img" aria-label="Illustrative relationship test. A customer request reaches the team through the owner. If the owner leaves, the customer and team remain; whether a new request reaches them directly is an open question, not a shown rejection.">
<!-- New customer study: finite individually authored contours, open corners and uneven retraces. -->
<g id="r16-customer" class="sketch">
<path d="M207 264 Q195 243 207 225 M211 220 Q232 205 252 215 M256 219 Q271 232 267 249 L273 265 L262 272 M258 276 Q250 290 235 290 L216 279 L208 266" />
<path class="light" d="M204 253 Q197 230 215 218 M213 218 L229 211 M235 211 Q258 210 267 231 M269 239 L271 256 M213 270 L219 283 M224 287 L240 293 M251 286 L260 278" />
<path d="M212 252 Q219 244 222 258 L216 265 M247 249 L257 248 M258 258 L260 262 M247 277 L257 275 M225 287 L223 305 M253 287 L255 304 M220 305 L199 317 Q188 325 184 350 M258 306 L280 319 L294 345" />
<path class="light" d="M218 305 L213 314 M235 311 L247 318 M196 322 L190 336 M281 325 L291 347 M202 342 L199 369 M274 340 L277 373" />
<path d="M199 317 L226 346 L242 324 L267 344 L281 321 M203 345 L201 392 M201 400 L200 443 L271 447 M273 351 L273 390 M275 404 L278 444 M186 350 L181 398 L199 420 M292 346 L309 382 L294 407 L274 408 M304 381 L288 394 L272 396" />
<path class="light" d="M179 363 L178 397 M185 402 L196 416 M205 373 L207 398 M204 410 L203 438 M214 419 L226 435 M220 413 L235 435 M252 414 L268 433 M277 368 L281 391 M294 365 L302 382" />
<path d="M200 443 L197 476 L218 478 L235 451 M242 450 L251 479 L278 478 L276 447 M198 479 L186 487 L216 489 M254 481 L257 490 L291 489 L280 479" />
<path class="light" d="M205 449 L202 469 M212 449 L209 472 M254 451 L263 473 M197 485 L212 485 M263 486 L279 485 M175 498 L221 502 M235 501 L297 499" />
</g>
<g transform="translate(170 175) scale(.78)">OWNER</g>
<g transform="translate(826 120) scale(.62)">WORKER</g>
<g class="sketch"><path d="M1065 327 L1097 349 L1084 394 L1074 404 M1057 340 L1080 355 L1070 389 L1064 399 L1074 404 M1071 392 L1080 397" /><path class="light" d="M1076 343 L1090 352 M1085 369 L1077 389 M1068 398 L1074 399" /></g>
<!-- The team bench and prior work remain available in both states. -->
<g id="r16-bench" class="sketch">
<path d="M946 435 L1117 431 L1161 447 L979 453 L948 439 M982 457 L1158 451 M989 457 L988 497 M997 458 L996 493 M1139 454 L1146 496" />
<path class="light" d="M958 438 L1027 436 M1042 436 L1116 434 M989 463 L991 486 M1143 462 L1146 482 M982 502 L1050 505 M1081 503 L1158 501" />
</g>
<g id="r16-route" class="route">
<path d="M250 548 L377 502 M385 499 L549 441 M257 551 L351 519 M414 492 L526 451" />
<g id="r16-owner-link"><path d="M551 440 L630 410 L730 418 M566 439 L611 423 M658 417 L717 422" /></g>
<path d="M733 418 L882 430 M891 431 L1027 440 M749 423 L846 431 M927 438 L1009 444 M1015 431 L1030 440 L1015 448" />
</g>
<!-- Each request is a tangible blank work sheet; no invented customer record. -->
<g id="r16-request-one" class="sketch">
<path fill="#F5F0E6" stroke="none" d="M210 520 L259 517 L274 531 L274 573 L212 576 Z" />
<path d="M212 521 L241 519 M247 519 L259 518 L273 531 L273 571 L245 574 M237 574 L213 576 L212 549 M212 542 L212 525 M259 519 L258 534 L271 533 M222 541 L258 539 M223 549 L251 548 M223 560 L245 559" />
<path class="light" d="M209 528 L209 552 M218 579 L248 577 M278 537 L277 563 M226 544 L248 543" />
</g>
<g id="r16-request-two" class="sketch accent">
<path fill="#F5F0E6" stroke="none" d="M210 520 L259 517 L274 531 L274 573 L212 576 Z" />
<path d="M212 521 L241 519 M247 519 L259 518 L273 531 L273 571 L245 574 M237 574 L213 576 L212 549 M212 542 L212 525 M259 519 L258 534 L271 533" />
<path class="light" d="M209 528 L209 552 M218 579 L248 577 M278 537 L277 563 M223 541 L258 539 M223 550 L252 548 M223 560 L245 559" />
</g>
<g id="r16-open-question" transform="translate(0 -100)" class="sketch accent">
<path d="M611 522 Q612 501 631 498 M636 498 Q657 499 660 517 M660 522 Q657 534 644 540 M641 544 L639 559" />
<path class="light" d="M608 520 Q608 505 621 499 M642 500 Q657 501 662 514 M647 539 L642 553" />
<path d="M638 572 L642 572 L642 577 L637 577 M636 580 L644 579" />
</g>
</svg>
<p id="r16-customer-label" class="r16-label">Customer</p><p id="r16-owner-label" class="r16-label">Owner</p><p id="r16-away-label" class="r16-label">If she leaves</p><p id="r16-team-label" class="r16-label">Team</p>
</div><script>(()=>{
const tl=gsap.timeline({paused:true});
tl.set(['#r16-owner','#r16-owner-label','#r16-owner-link'],{autoAlpha:1},0);
tl.fromTo('#r16-request-one',{x:0,y:0},{x:390,y:-138,duration:13/24,ease:'power1.inOut'},6/24);
tl.to('#r16-request-one',{x:790,y:-108,duration:14/24,ease:'power1.inOut'},28/24);
// Counterfactual on nearest 24fps frame to W000090 'not', master32.56.
tl.set(['#r16-owner','#r16-owner-label','#r16-owner-link'],{autoAlpha:0},56/24);
tl.set(['#r16-away-label','#r16-request-two'],{autoAlpha:1},56/24);
tl.fromTo('#r16-request-two',{x:0,y:0},{x:294,y:-100,duration:16/24,ease:'power1.inOut',immediateRender:false},60/24);
const marks=Array.from(document.querySelectorAll('#r16-open-question path'));
tl.set('#r16-open-question',{autoAlpha:1},66/24);
marks.forEach((p,i)=>{const len=p.getTotalLength();tl.fromTo(p,{strokeDasharray:len+' '+len,strokeDashoffset:len},{strokeDashoffset:0,duration:10/24,ease:'none'},66/24+i/24);});
window.__timelines=window.__timelines||{};window.__timelines['r16-handoff']=tl;
})();</script></template></body></html>
'''.replace('OWNER',owner).replace('WORKER',worker)
(root / 'compositions/handoff.html').write_text(html)
(root / 'BASELINE-PINS.json').write_text(json.dumps({'baseline':str(baseline.relative_to(root.parents[6])), 'sha256':pins},indent=2)+'\n')
assert all(sha(baseline / rel)==h for rel,h in pins.items())
print(f'R16 created; {len(pins)} R15 input files unchanged.')
