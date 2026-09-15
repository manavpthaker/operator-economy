from pathlib import Path
import hashlib, json, re
from html.parser import HTMLParser

root=Path(__file__).resolve().parent
base=root.parent/'r17-clear-customer-orders'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((root/'BASELINE-PINS.json').read_text())['sha256']
for rel,h in pins.items(): assert sha(base/rel)==h, 'baseline changed: '+rel
retained=[]
for p in root.rglob('*'):
    if p.is_file() and str(p.relative_to(root)) in pins and str(p.relative_to(root)) not in ['index.html','compositions/handoff.html']:
        assert sha(p)==pins[str(p.relative_to(root))]
        retained.append(str(p.relative_to(root)))

class Clips(HTMLParser):
    def __init__(self): super().__init__(); self.clips=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-track-index' in a:self.clips.append({'tag':tag,**a})

a,b=Clips(),Clips()
a.feed((base/'index.html').read_text()); b.feed((root/'index.html').read_text())
assert len(a.clips)==len(b.clips)==18
for old,new in zip(a.clips,b.clips):
    if old.get('id')=='handoff-host':
        old={**old,'data-composition-id':'r18-handoff'}
    assert old==new, 'unexpected clip change: '+str(old)

pictures=[c for c in b.clips if c['data-track-index']=='1']
cursor=0
for c in pictures:
    start,dur=float(c['data-start']),float(c['data-duration'])
    assert abs(start-cursor)<1e-7
    assert abs(start*24-round(start*24))<1e-7
    assert abs(dur*24-round(dur*24))<1e-7
    cursor=start+dur
assert cursor==71.5
transcript=root.parents[5]/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/word-transcript.json'
assert sha(transcript)=='f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7'
result={'ok':True,'baseline_files_unchanged':len(pins),'retained_files_identical':len(retained),'all_18_clip_declarations_preserved_except_graphic_identity':True,'picture_frames':1716,'fps':24,'duration_seconds':71.5,'original_audio_assets_and_placements_identical':True,'graphic_slot':[725,842],'counterfactual_frame':781,'counterfactual_master_time':781/24,'word_not_time':32.56,'authored':{p:sha(root/p) for p in ['index.html','compositions/handoff.html','BRIEF.md','DIRECTION.md','frame.md','STORYBOARD.md']},'scope':'isolated preview candidate; no creative acceptance or encoded delivery claim'}
(root/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
