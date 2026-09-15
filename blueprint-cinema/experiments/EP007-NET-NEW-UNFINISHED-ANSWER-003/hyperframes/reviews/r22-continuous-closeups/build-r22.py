"""Keep R21's closeups with uninterrupted B video playback."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, shutil

root = Path(__file__).resolve().parent
base = root.parent / 'r21-buyer-and-emphasis'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
runtime = json.loads((base / '.hyperframes/phone-player.json').read_text())['files']
pins = {rel: sha(base / rel) for rel in runtime}
assert pins == runtime, 'R21 runtime drift'
for rel in runtime:
    if rel == 'index.html': continue
    src, dest = base / rel, root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists(): assert sha(dest) == sha(src)
    elif rel.startswith('public/'): os.link(src, dest)
    else: shutil.copy2(src, dest)

source = (base / 'index.html').read_text()
index = source.replace('EP007 R21 — buyer reaction and emphasis', 'EP007 R22 — continuous closeups').replace('ep007-r21', 'ep007-r22')
index = index.replace('.avatar-promise{left:-160px;top:-24px;width:1600px;height:905px}\n.avatar-emphasis{left:-256px;top:-42px;width:1792px;height:1013.6px}', '.promise-framing{position:absolute;left:0;top:0;width:1280px;height:724px;transform-origin:0 0}')
promise = next(line for line in index.splitlines() if 'id="post-title-promise"' in line)
emphasis = next(line for line in index.splitlines() if 'id="post-title-one-number"' in line)
replacement = '<div class="viewport" data-layout-allow-overflow=""><div id="promise-framing" class="promise-framing" data-layout-allow-overflow=""><video id="post-title-promise" class="clip avatar" src="public/media/post-title-b.mp4" data-start="62.916666666666664" data-duration="8.583333333333334" data-media-start="0" data-track-index="1" muted playsinline aria-label="One uninterrupted presenter take; the viewing promise and one number retain their approved closeup framing."></video></div></div>'
index = index.replace(promise, replacement).replace(emphasis+'\n', '')
old = "</div><script>window.__timelines=window.__timelines||{};window.__timelines['ep007-r22']=gsap.timeline({paused:true});</script>"
new = """</div><script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({paused:true});
tl.set('#promise-framing', {x:-160, y:-24, scale:1.25, transformOrigin:'0 0'}, 0);
tl.addLabel('one-number', 67.91666666666667);
tl.set('#promise-framing', {x:-256, y:-42, scale:1.4, transformOrigin:'0 0'}, 'one-number');
window.__timelines['ep007-r22'] = tl;
</script>"""
assert old in index
index = index.replace(old, new)
(root / 'index.html').write_text(index)
pkg=json.loads((base/'package.json').read_text());pkg['name']='ep007-r22-continuous-closeups'
(root/'package.json').write_text(json.dumps(pkg,indent=2)+'\n')
(root/'BASELINE-PINS.json').write_text(json.dumps({'baseline':str(base),'sha256':pins},indent=2)+'\n')

class Clips(HTMLParser):
    def __init__(self): super().__init__(); self.clips=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'data-track-index' in a: self.clips.append({'tag':tag,**a})
a,b=Clips(),Clips();a.feed(source);b.feed(index)
oldclips={c['id']:c for c in a.clips}
for c in b.clips:
    if c['id']!='post-title-promise': assert c==oldclips[c['id']]
cursor=0
for c in b.clips:
    if c['data-track-index']!='1': continue
    s,d=float(c['data-start']),float(c['data-duration'])
    assert abs(s-cursor)<1e-7
    assert abs(s*24-round(s*24))<1e-7 and abs(d*24-round(d*24))<1e-7
    cursor=s+d
assert cursor==71.5 and len(b.clips)==17
assert index.count('src="public/media/post-title-b.mp4"')==1
assert all(sha(base/rel)==pin for rel,pin in pins.items())
assert all(sha(root/rel)==pin for rel,pin in pins.items() if rel!='index.html')
result={'ok':True,'baseline_files_unchanged':len(pins),'retained_files_byte_identical':len(pins)-1,
        'duration_seconds':71.5,'fps':24,'picture_frames':1716,'b_video_elements':1,
        'b_source_frames':[0,206],'b_review_range':[62.916666666666664,71.5],
        'crop_cut_time':67.91666666666667,'crop_states_unchanged':True,
        'audio_clips_unchanged':True,'source_media_unchanged':True,
        'narration_changed':False,'lip_sync_generated':False,
        'scope':'private playback refinement; continuous decoder with unchanged hard closeups'}
(root/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
