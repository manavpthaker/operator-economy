"""Clarify the preserved R16 source in an isolated review candidate."""
from pathlib import Path
import hashlib, json, os, re, shutil

root = Path(__file__).resolve().parent
baseline = root.parent / 'r16-customer-handover'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
files = [p for p in baseline.rglob('*') if p.is_file() and (p.relative_to(baseline).parts[0] in ('public', 'compositions') or p.name == 'index.html')]
pins = {str(p.relative_to(baseline)): sha(p) for p in files}
assert pins['index.html'] == '1007c19ffcc2cce0496573479bc8d9f690bccf14acb65305f5cc3eddacc31348'
assert pins['compositions/handoff.html'] == 'e162310d02fd193cd06658afe768ef3ed5a4f40ff42fb14c1a1b4719fa6e7e98'
for p in files:
    rel = p.relative_to(baseline)
    if str(rel) in ('index.html', 'compositions/handoff.html'): continue
    out = root / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists(): assert sha(out) == sha(p)
    elif rel.parts[0] == 'public': os.link(p, out)
    else: shutil.copy2(p, out)

index = (baseline / 'index.html').read_text().replace('EP007 R16 — customer relationship test', 'EP007 R17 — clear customer orders').replace('ep007-r16', 'ep007-r17').replace('r16-handoff', 'r17-handoff')
(root / 'index.html').write_text(index)
html = (baseline / 'compositions/handoff.html').read_text().replace('r16-', 'r17-')
html = html.replace('<title>The customer relationship test</title>', '<title>Customers order through her</title>')
html = html.replace("@font-face{font-family:Supreme;src:url('public/fonts/supreme-400.woff2');font-weight:400}", "@font-face{font-family:Supreme;src:url('public/fonts/supreme-400.woff2');font-weight:400}\n@font-face{font-family:Supreme;src:url('public/fonts/supreme-500.woff2');font-weight:500}")
html = html.replace('#r17-away-label,#r17-request-two,#r17-open-question{', '#r17-heading-after,#r17-away-label,#r17-request-two,#r17-open-question{')
html = html.replace('<h1 class="r17-heading">Will customers stay?</h1>', '<h1 id="r17-heading-before" class="r17-heading">Customers order through her.</h1><h1 id="r17-heading-after" class="r17-heading">Will they order without her?</h1>')
html = html.replace('A customer request reaches the team through the owner.', 'A customer order reaches the team through the owner.').replace('whether a new request reaches them directly', 'whether the customer will order without her')

def order(gid, accent=False):
    ink = '#B5482F' if accent else '#173530'
    return f'''<g id="{gid}" class="sketch{' accent' if accent else ''}">
<path fill="#F5F0E6" stroke="none" d="M169 505 L293 502 L316 525 L316 591 L172 595 Z" />
<path d="M171 506 L228 504 M238 504 L291 503 L315 525 L315 586 M315 591 L246 593 M235 593 L173 595 L171 560 M171 550 L170 511 M292 505 L290 527 L312 526" />
<path class="light" d="M167 515 L168 548 M169 565 L170 583 M179 598 L230 596 M255 596 L302 594 M319 535 L318 581 M292 530 L309 529" />
<text x="242" y="563" fill="{ink}" stroke="none" text-anchor="middle" font-family="Supreme,sans-serif" font-size="32" font-weight="500">ORDER</text>
</g>'''
html, count = re.subn(r'<g id="r17-request-one".*?</g>', order('r17-request-one'), html, count=1, flags=re.S)
assert count == 1
html, count = re.subn(r'<g id="r17-request-two".*?</g>', order('r17-request-two', True), html, count=1, flags=re.S)
assert count == 1
html = html.replace('Each request is a tangible blank work sheet; no invented customer record.', 'Each ORDER is a labeled model object; it contains no invented customer record.')
html = html.replace("tl.set(['#r17-owner','#r17-owner-label','#r17-owner-link'],{autoAlpha:0},56/24);", "tl.set(['#r17-owner','#r17-owner-label','#r17-owner-link','#r17-heading-before'],{autoAlpha:0},56/24);")
html = html.replace("tl.set(['#r17-away-label','#r17-request-two'],{autoAlpha:1},56/24);", "tl.set(['#r17-away-label','#r17-request-two','#r17-heading-after'],{autoAlpha:1},56/24);")
html = html.replace('{x:294,y:-100,duration:16/24', '{x:258,y:-100,duration:16/24') # Preserve a clear gap around the larger order and question mark.
(root / 'compositions/handoff.html').write_text(html)
package = json.loads((baseline / 'package.json').read_text())
package['name'] = 'ep007-r17-clear-customer-orders'
(root / 'package.json').write_text(json.dumps(package, indent=2)+'\n')
(root / 'BASELINE-PINS.json').write_text(json.dumps({'baseline': str(baseline), 'sha256': pins}, indent=2)+'\n')
verify = (baseline / 'verify-r16.py').read_text().replace("base=root.parent/'r15-post-title'", "base=root.parent/'r16-customer-handover'").replace("'r16-handoff'", "'r17-handoff'")
(root / 'verify-r17.py').write_text(verify)
assert all(sha(baseline / rel) == h for rel, h in pins.items())
print(f'R17 created; {len(pins)} R16 runtime source files unchanged.')
