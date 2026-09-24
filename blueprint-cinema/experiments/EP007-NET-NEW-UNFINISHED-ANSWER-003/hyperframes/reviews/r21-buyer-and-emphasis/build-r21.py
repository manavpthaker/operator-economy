"""Review-only buyer coverage and deliberate presenter framing."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, shutil

root=Path(__file__).resolve().parent
base=root.parent/'r20-performance-first'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for p in base.rglob('*') if p.is_file() and (p.relative_to(base).parts[0] in ('public','compositions') or p.name=='index.html')]
pins={str(p.relative_to(base)):sha(p) for p in files}
assert pins['index.html']=='631248888b66ee90e39236e2e0221af36743b9cc3616bec538f7fd1f6a331f5e'
for src in files:
    rel=src.relative_to(base)
    if str(rel)=='index.html':continue
    dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():assert sha(dest)==sha(src)
    elif rel.parts[0]=='public':os.link(src,dest)
    else:shutil.copy2(src,dest)
index=(base/'index.html').read_text().replace('EP007 R20 — uninterrupted realization','EP007 R21 — buyer reaction and emphasis').replace('ep007-r20','ep007-r21')
index=index.replace('</style>', '.avatar-promise{left:-160px;top:-24px;width:1600px;height:905px}\n.avatar-emphasis{left:-256px;top:-42px;width:1792px;height:1013.6px}\n</style>')
old=next(s for s in index.splitlines() if 'id="pause-consequence"' in s)
new='<div class="viewport" data-layout-allow-overflow="">'+old.replace('class="clip plate"','class="clip buyer-crop"').replace('Quiet consequence: the buyer waits and the owner reflects.','Buyer-focused reaction to the unfinished answer; existing silent footage and source timing preserved.')+'</div>'
index=index.replace(old,new)
old=next(s for s in index.splitlines() if 'id="post-title-promise"' in s)
new=old.replace('class="clip avatar"','class="clip avatar avatar-promise"').replace('data-duration="8.583333333333334"','data-duration="5"').replace('Synthetic presenter explains what viewers will learn, synchronized to the original narration.','A closer presenter shot begins the viewing promise.')
new+='\n<div class="viewport" data-layout-allow-overflow=""><video id="post-title-one-number" class="clip avatar avatar-emphasis" src="public/media/post-title-b.mp4" data-start="67.91666666666667" data-duration="3.5833333333333335" data-media-start="5" data-track-index="1" muted playsinline aria-label="A tighter framing emphasizes one number; original source motion and narration continue without a timing change."></video></div>'
index=index.replace(old,new)
(root/'index.html').write_text(index)
pkg=json.loads((base/'package.json').read_text());pkg['name']='ep007-r21-buyer-and-emphasis';(root/'package.json').write_text(json.dumps(pkg,indent=2)+'\n')
(root/'BASELINE-PINS.json').write_text(json.dumps({'baseline':str(base),'sha256':pins},indent=2)+'\n')

class Clips(HTMLParser):
    def __init__(self):super().__init__();self.clips=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-track-index' in a:self.clips.append({'tag':tag,**a})

a,b=Clips(),Clips();a.feed((base/'index.html').read_text());b.feed(index)
old={c['id']:c for c in a.clips};assert len(b.clips)==18
changed={'pause-consequence','post-title-promise','post-title-one-number'}
for c in b.clips:
    if c['id'] not in changed:assert c==old[c['id']]
cursor=0
for c in b.clips:
    if c['data-track-index']!='1':continue
    s,d=float(c['data-start']),float(c['data-duration'])
    assert abs(s-cursor)<1e-7 and abs(s*24-round(s*24))<1e-7 and abs(d*24-round(d*24))<1e-7
    cursor=s+d
assert cursor==71.5
assert all(sha(base/rel)==h for rel,h in pins.items())
assert all(sha(root/rel)==h for rel,h in pins.items() if rel!='index.html')
result={'ok':True,'baseline_files_unchanged':len(pins),'retained_runtime_files_byte_identical':len(pins)-1,
        'duration_seconds':71.5,'fps':24,'picture_frames':1716,'original_audio_unchanged':True,
        'buyer_reaction_review_range':[35.083333333333336,40.083333333333336],
        'buyer_source_range':[4.75,9.75],'buyer_crop':'same source; right-side close framing',
        'by_the_end_cut_review_time':62.916666666666664,'by_word_onset':63.38,
        'one_number_cut_review_time':67.91666666666667,'one_word_onset':67.94,
        'post_title_b_source_frames_contiguous':[[0,120],[120,206]],
        'vocal_stress_changed':False,'lip_sync_repaired':False,
        'scope':'private framing comparison; no media generation, narration change or gate advance'}
(root/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
