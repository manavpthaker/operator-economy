"""Create a private comparison with the realization uninterrupted by a diagram."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, re, shutil

root = Path(__file__).resolve().parent
base = root.parent / 'r19-tagline-restored'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
files = [p for p in base.rglob('*') if p.is_file() and
         (p.relative_to(base).parts[0] in ('public', 'compositions') or p.name == 'index.html')]
pins = {str(p.relative_to(base)): sha(p) for p in files}
for source in files:
    rel = source.relative_to(base)
    if str(rel) == 'index.html':
        continue
    dest = root / rel; dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert sha(dest) == sha(source)
    elif rel.parts[0] == 'public':
        os.link(source, dest)
    else:
        shutil.copy2(source, dest)
index = (base/'index.html').read_text().replace('EP007 R19 — tagline restored', 'EP007 R20 — uninterrupted realization').replace('ep007-r19', 'ep007-r20')
line = next(s for s in index.splitlines() if 'id="owner-arithmetic-stare"' in s)
replacement = line.replace('data-duration="2.2916666666666665"', 'data-duration="7.166666666666667"').replace('A held silent realization before the model.', 'Uninterrupted realization: the owner looks toward the buyer, then lowers her gaze as she cannot finish the answer.')
index = index.replace(line, replacement)
graphic = next(s for s in index.splitlines() if 'id="handoff-host"' in s)
index = index.replace(graphic+'\n', '')
(root/'index.html').write_text(index)
pkg = json.loads((base/'package.json').read_text());pkg['name']='ep007-r20-performance-first'
(root/'package.json').write_text(json.dumps(pkg,indent=2)+'\n')
(root/'BASELINE-PINS.json').write_text(json.dumps({'baseline':str(base),'sha256':pins},indent=2)+'\n')

class Clips(HTMLParser):
    def __init__(self):super().__init__();self.clips=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-track-index' in a:self.clips.append({'tag':tag,**a})

old,new=Clips(),Clips();old.feed((base/'index.html').read_text());new.feed(index)
old_by_id={c['id']:c for c in old.clips}
assert len(old.clips)==18 and len(new.clips)==17
for c in new.clips:
    if c['id']=='owner-arithmetic-stare':
        expected={**old_by_id[c['id']],'data-duration':'7.166666666666667','aria-label': 'Uninterrupted realization: the owner looks toward the buyer, then lowers her gaze as she cannot finish the answer.'}
        assert c==expected
    else:assert c==old_by_id[c['id']]
cursor=0
for c in new.clips:
    if c['data-track-index']!='1':continue
    start,duration=float(c['data-start']),float(c['data-duration'])
    assert abs(start-cursor)<1e-7
    assert abs(start*24-round(start*24))<1e-7 and abs(duration*24-round(duration*24))<1e-7
    cursor=start+duration
assert cursor==71.5
assert all(sha(base/rel)==h for rel,h in pins.items())
result={'ok':True,'baseline_runtime_files_unchanged':len(pins),'retained_runtime_files_identical':len(pins)-1,
        'picture_frames':1716,'fps':24,'duration_seconds':71.5,
        'edit_delta':'Extend existing shot-d continuously from source frame10 through frame181 inclusive; remove handoff-host.',
        'extended_shot_review_frames':[670,842],'extended_shot_source_frames':[10,182],
        'source_available_frames':193,'source_window_within_media':True,
        'original_audio_and_sting_identical':True,'presenter_replacement_pending':True,
        'scope':'private creative comparison; no production or publication gate change'}
(root/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
