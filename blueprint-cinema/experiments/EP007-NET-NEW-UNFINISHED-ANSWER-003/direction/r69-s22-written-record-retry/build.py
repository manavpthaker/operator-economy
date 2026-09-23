#!/usr/bin/env python3
"""Stage verified S22 sources and build the film-only review from exact selected frames."""
from pathlib import Path
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[5]
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
D=Path(__file__).resolve().parent
H=EXP/'hyperframes/reviews/r69-s22-film'
C=EXP/'hyperframes/reviews/r69-s22-context'
sel=json.loads((D/'SELECTION.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p in [H/'public/media',H/'public/audio',H/'public/vendor',H/'qa',C/'qa']:p.mkdir(parents=True,exist_ok=True)
for name in ['A','B']:
 p=H/'provider'/('take-'+name.lower())/'native.mp4'
 assert sha(p)==sel['takes'][name]['sha256']
 assert sel['takes'][name]['out_frame']-sel['takes'][name]['in_frame']==(97 if name=='A' else 264)
 shutil.copy2(p,H/'public/media'/f'take-{name.lower()}.mp4')
prior=EXP/'hyperframes/reviews/r67-s22-plan'
for name in ['establishing.mp4','question.mp4']:shutil.copy2(prior/'public/media'/name,H/'public/media'/name)
shutil.copy2(prior/'public/audio/narration.wav',H/'public/audio/narration.wav')
shutil.copy2(prior/'public/vendor/gsap.min.js',H/'public/vendor/gsap.min.js')
for name in ['package.json','hyperframes.json']:
 text=(prior/name).read_text().replace('r67-s22-plan','r69-s22-film');(H/name).write_text(text)
def video(id,file,start,duration,source,track,extra=''):
 return f'<video id="{id}" class="clip film" src="public/media/{file}" muted playsinline data-start="{start}" data-duration="{duration}" data-media-start="{source}" data-track-index="{track}" {extra}></video>'
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>EP007 S22 — Return to the table</title>
<style>*{box-sizing:border-box}html,body{margin:0;width:1280px;height:720px;overflow:hidden}
#root{position:relative;width:1280px;height:720px;overflow:hidden}.back{position:absolute;inset:0;background:#000}
.clip{position:absolute;inset:0;width:1280px;height:720px}.film{object-fit:cover}
</style><script src="public/vendor/gsap.min.js"></script></head><body>
<div id="root" data-composition-id="ep007-r69-s22" data-start="0" data-duration="21.833333333333332" data-width="1280" data-height="720" data-fps="24"><div class="back"></div>
'''
html+=video('table-return','establishing.mp4',0,55/24,4.5,1)+'\n'
html+=video('buyer-question','question.mp4',55/24,108/24,0,2)+'\n'
html+=video('owner-record','take-a.mp4',163/24,97/24,sel['takes']['A']['in_frame']/24,3)+'\n'
html+=video('buyer-response','take-b.mp4',260/24,264/24,sel['takes']['B']['in_frame']/24,4)+'\n'
html+='''<audio id="original-narration" src="public/audio/narration.wav" data-start="0" data-duration="21.833333333333332" data-media-start="0" data-track-index="100" data-volume="1"></audio>
</div><script>window.__timelines=window.__timelines||{};window.__timelines['ep007-r69-s22']=gsap.timeline({paused:true});</script></body></html>
'''
(H/'index.html').write_text(html)
(C/'.gitignore').write_text('qa/\n')
(C/'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EP007 — S22 review</title><style>body{margin:0;background:#111;color:#eee;font:16px/1.45 system-ui}video{display:block;width:100%;max-height:84vh;background:#000}main{padding:14px 20px;max-width:1100px}p{margin:7px 0}button{color:#eee;border:1px solid #777;background:#222;padding:7px 10px;border-radius:4px;cursor:pointer;margin:5px 6px 0 0}.status{color:#ccc;font-size:14px}</style></head><body><video id="v" src="qa/context.mp4" controls preload="metadata" playsinline></video><main><p><strong>S22 · Return to the table</strong></p><p>Last 8 seconds of locked S21, then S22 at 0:08. Original narration throughout.</p><div id="cues"></div><p class="status">S21 is locked. S22 awaits review. S17’s on-camera take remains open.</p></main><script>const v=document.getElementById('v');for(const [t,label] of [[8,'S22 starts'],[14.791667,'The prepared record'],[18.833333,'The buyer checks it']]){const b=document.createElement('button');b.textContent=label;b.onclick=()=>{v.currentTime=t;v.play()};document.getElementById('cues').appendChild(b)}</script></body></html>''')
print(json.dumps({'source_staged':True,'frames':524,'takes':sel['takes']}))
