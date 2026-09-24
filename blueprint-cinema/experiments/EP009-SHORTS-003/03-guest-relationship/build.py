from pathlib import Path
import json, subprocess, shutil, hashlib, html

P=Path(__file__).resolve().parent
REPO=P.parents[3]
B=REPO/'blueprint-cinema/experiments/EP009-FULL-BUILD-001'
FPS=24; IN=4510; OUT=4844; FRAMES=388
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(c): subprocess.run(c,check=True)
def save(n,v): (P/n).write_text(json.dumps(v,indent=2)+'\n')
for d in ['assets/fonts','assets/vendor','qa','review','review/frames']:(P/d).mkdir(parents=True,exist_ok=True)
for font in ['supreme-500.woff2','zodiak-700.woff2']:
 shutil.copyfile(REPO/'blueprint-cinema/experiments/EP009-SHORTS-002/01-second-commission/assets/fonts'/font,P/'assets/fonts'/font)
shutil.copyfile(REPO/'.agents/skills/talking-head-recut/assets/vendor/gsap.min.js',P/'assets/vendor/gsap.min.js')
wide=B/'presenter-look-transfer/room-r1/seg019a/native.mp4'
close=B/'presenter-look-transfer/room-r1/seg019b/native.mp4'
master=B/'assembly/r3/narration-master-r3.wav'
sources=[{'id':'wide','path':str(wide.relative_to(REPO)),'sha256':sha(wide),'global_frames':[4510,4783],'native_frames':[60,333],'timeline_frames':[0,273]}, {'id':'close','path':str(close.relative_to(REPO)),'sha256':sha(close),'global_frames':[4783,4844],'native_frames':[45,106],'timeline_frames':[273,334]}]
if not (P/'assets/avatar-wide-r4.mp4').exists():
 # Retain the existing 960px crop and 1216px height exactly.
 # Plain pine framing replaces the rejected stretched edge extensions.
 # No duplicated/blurred face, synthesized room, speed change or frame hold.
 f='[0:v]trim=start_frame=60:end_frame=333,setpts=PTS-STARTPTS,crop=960:1080:360:0,scale=1080:1216,pad=1080:1920:0:200:color=0x173530,setsar=1[v]'
 run(['ffmpeg','-v','error','-i',str(wide),'-filter_complex',f,'-map','[v]','-an','-c:v','libx264','-crf','17','-preset','fast','-threads','1','-r','24','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'assets/avatar-wide-r4.mp4')])
if not (P/'assets/avatar-close.mp4').exists():
 run(['ffmpeg','-v','error','-i',str(close),'-vf','trim=start_frame=45:end_frame=106,setpts=PTS-STARTPTS,crop=608:1080:640:0,scale=1080:1920,setsar=1','-an','-c:v','libx264','-crf','17','-preset','fast','-threads','1','-r','24','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'assets/avatar-close.mp4')])
if not (P/'assets/voice-r2.wav').exists():
 run(['ffmpeg','-v','error','-i',str(master),'-af',f'atrim=start_sample={IN*2000}:end_sample={OUT*2000},asetpts=PTS-STARTPTS','-c:a','pcm_s16le',str(P/'assets/voice-r2.wav')])
words=json.loads((B/'assembly/r3/word-transcript-r3.json').read_text())['words']
wi={w['w_id']:w for w in words}
groups=[(538,542),(543,547),(548,552),(553,558),(559,562),(563,568),(569,574),(575,578),(579,583)]
caps=[]
for i,(a,z) in enumerate(groups):
 ww=[wi[f'W{x:06d}'] for x in range(a,z+1)]
 start=max(0,ww[0]['start']-IN/FPS)
 end=min((OUT-IN)/FPS,ww[-1]['end']-IN/FPS+.07)
 if i<len(groups)-1:end=min(end,wi[f'W{groups[i+1][0]:06d}']['start']-IN/FPS)
 caps.append({'id':f'cap-{i}','start':start,'end':end,'text':' '.join(w['token'] for w in ww)})
save('captions.json',caps)
save('source-contract.json',{'schema':'ep009-avatar-forward-short-v1','status':'private_review','fps':24,'frame_count':FRAMES,'duration':FRAMES/FPS,'spoken_frames':[0,334],'audio':{'path':str(master.relative_to(REPO)),'sha256':sha(master),'frames':[IN,OUT],'sample_range':[IN*2000,OUT*2000]},'presenter_sources':sources,'picture_tail':None,'cta_frames':[334,388],'next_word_excluded':{'word_id':'W000584','token':'Nobody','starts':wi['W000584']['start'],'cut':OUT/FPS},'performance':'Exact selected native timing; no re-time, loop, interpolation, regeneration or provider audio. Only spatial reframing. Wide gesture view has solid #173530 upper/lower framing, with crop 960x1080 at source x360,y0 scaled to 1080x1216 and placed at output x0,y200. No extension, blur or duplicate imagery.','related_video':{'target':'EP009 r8','attached':False,'publication_dependency':True},'publication_approved':False})
(P/'BRIEF.md').write_text('''---
workflow: general-video
flow: automation
storyboard: no
aspect: 1080x1920
language: en
message: Who at the inn owns the returning guest relationship?
---

## Intent
Owner requested “avatar forward like cleo abrams.” Existing EP009 presenter leads every spoken thought with exact existing gestures and facial expressions. This short is a hook to the full episode, not a complete explanation.

## Assets
Selected 1920×1080 look-transfer seg019a/seg019b frames and authoritative r3 PCM narration. EDL in source-contract.json.

## Customizations
Dominant gesture-wide presenter view followed by existing closer performance for the final question. Native portrait canvas. Small timed relationship cues; short exact-word captions. Local review MP4 explicitly authorized; no publication.

## Notes
Total 16.166667 seconds. Cut precedes next word Nobody. No added speech or synthetic performance. Related Video is a publication dependency. Upgraded scaffold pin 0.8.51 to 0.8.53; final check validates current composition.
''')
(P/'DESIGN.md').write_text('''# Design
The presenter asks who owns the second booking; the room and the human performance carry the story.
Boundary Ledger-compatible Supreme 500, Zodiak 700; cream #F5F0E6, pine #173530, warm signal #FB8B69. One primary focal point: face and hands. No full-screen explanatory paper deck or face window.
The gesture-wide shot retains the visible pointing hand and both hands. Solid #173530 upper/lower framing surrounds the dominant 1080x1216 performance crop at y200; no stretched room/table edges, decorative blur or duplicate face. Closing shot is a portrait reframe of the already-closer selected native performance. No color treatment: source appearance remains the accepted look.
Brand anchors at top left. Relationship cues sit above the face, captions below the hands. Typography is sparse and large enough for a phone. Existing source camera cut is retained. Final graphic follows the selected presenter and a safe silent source tail; no new word begins.
''')
(P/'STORYBOARD.md').write_text('''---
mode: autonomous
---
## Frame 1
status: built
src: index.html
0–11.375s: exact presenter wide view, small booking-site/email and return-route cues only when those relationships are spoken. Native body performance owns motion. SVG path draw clarifies the route.
## Frame 2
status: built
src: index.html
11.375–13.916667s: existing closer presenter camera cut; no new motion processing. Final outside-service question.
## Frame 3
status: built
src: index.html
13.916667–16.166667s: cut to “Who owns the second booking?” The question has completed before this 54-frame handoff. Rule: svg-path-draw plus explicit opacity/reveal, no decorative drift.
''')
caphtml=''.join(f'<p id="{c["id"]}" class="clip caption" data-start="{c["start"]:.9f}" data-duration="{c["end"]-c["start"]:.9f}" data-track-index="20">{html.escape(c["text"])}</p>' for c in caps)
doc='''<!doctype html><html><head><meta charset="utf-8"><title>EP009 · Who owns the second booking?</title><script src="assets/vendor/gsap.min.js"></script><style>
@font-face{font-family:Supreme;src:url('assets/fonts/supreme-500.woff2');font-weight:500}
@font-face{font-family:Zodiak;src:url('assets/fonts/zodiak-700.woff2');font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#173530}#root{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Supreme,Arial,sans-serif;color:#F5F0E6}.fill{position:absolute;inset:0;background:#173530}.avatar{position:absolute;inset:0;width:1080px;height:1920px;object-fit:fill}.brand{position:absolute;top:65px;left:64px;width:500px;font-size:26px;letter-spacing:.12em;padding:16px 20px;background:#173530;color:#F5F0E6;z-index:60}.caption{position:absolute;left:78px;top:1470px;width:836px;padding:22px 28px;text-align:center;background:#173530;color:#F5F0E6;font:500 68px/1.12 Supreme,Arial,sans-serif;letter-spacing:-.02em;z-index:30}.cue{position:absolute;top:143px;left:64px;width:850px;height:123px;z-index:20}.cue-inner{width:850px;height:123px;background:#F5F0E6;color:#173530;display:flex;align-items:center;justify-content:space-between;padding:25px 30px;gap:24px;font-size:40px}.cue-inner b{font-weight:500}.cue-inner svg{width:92px;height:42px;flex-shrink:0}.cue-inner path{fill:none;stroke:#B5482F;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}.end{position:absolute;inset:0;width:1080px;height:1920px;z-index:25}.end-fill{position:absolute;inset:0;background:#173530}.question{position:absolute;left:78px;top:410px;width:830px;font:700 112px/1.08 Zodiak,Georgia,serif;letter-spacing:-.03em;color:#F5F0E6}.end-copy{position:absolute;left:78px;top:1190px;width:830px;font:500 47px/1.2 Supreme,Arial,sans-serif;color:#F5F0E6}.end-copy span{display:block;margin-top:34px;color:#FB8B69;font-size:47px}.end-line{position:absolute;left:78px;top:1112px;width:830px;height:4px;background:#FB8B69;transform-origin:0 50%}
</style></head><body><main id="root" data-composition-id="main" data-start="0" data-duration="16.166666667" data-width="1080" data-height="1920" data-fps="24"><div class="fill"></div>
<video id="wide-video" class="clip avatar" src="assets/avatar-wide-r4.mp4" data-start="0" data-duration="11.375" data-media-start="0" data-track-index="1" muted playsinline></video>
<video id="close-video" class="clip avatar" src="assets/avatar-close.mp4" data-start="11.375" data-duration="2.541666667" data-media-start="0" data-track-index="1" muted playsinline></video>
<div class="clip cue" id="site-cue" data-start="0.083333333" data-duration="3.5" data-track-index="4"><div id="site-inner" class="cue-inner"><b>Booking site</b><svg viewBox="0 0 92 42"><path id="site-route" d="M4 21 H82 M68 6 L84 21 L68 36"/></svg><b>Guest’s email</b></div></div>
<div class="clip cue" id="return-cue" data-start="5.25" data-duration="4.1" data-track-index="4"><div id="return-inner" class="cue-inner"><b>Returning guest</b><svg viewBox="0 0 92 42"><path id="return-route" d="M4 21 H82 M68 6 L84 21 L68 36"/></svg><b>The inn?</b></div></div>
<div id="end" class="clip end" data-start="13.916666667" data-duration="2.25" data-track-index="5"><div class="end-fill"></div><h1 class="question">Who owns the second booking?</h1><div id="end-line" class="end-line"></div><p id="end-copy" class="end-copy">Full episode · EP009<span>Tap the related video →</span></p></div>
CAPTIONS
<p id="brand" class="clip brand" data-start="0" data-duration="16.166666667" data-track-index="40">THE OPERATOR ECONOMY</p>
<audio id="voice" src="assets/voice-r2.wav" data-start="0" data-duration="13.916666667" data-media-start="0" data-track-index="50" data-volume="1"></audio>
</main><script>const tl=gsap.timeline({paused:true});window.__timelines={main:tl};tl.fromTo('#site-inner',{opacity:0,y:14},{opacity:1,y:0,duration:.18,ease:'power2.out'},.083333333);tl.fromTo('#return-inner',{opacity:0,y:14},{opacity:1,y:0,duration:.18,ease:'power2.out'},5.25);document.querySelectorAll('.cue path').forEach(p=>{const len=p.getTotalLength();p.style.strokeDasharray=len;p.style.strokeDashoffset=len;});tl.to('#site-route',{strokeDashoffset:0,duration:.45,ease:'power2.out'},.25);tl.to('#return-route',{strokeDashoffset:0,duration:.45,ease:'power2.out'},5.4);tl.fromTo('#end-line',{scaleX:0},{scaleX:1,duration:.32,ease:'power2.out'},13.916666667);tl.fromTo('#end-copy',{opacity:0,y:12},{opacity:1,y:0,duration:.2,ease:'power2.out'},13.916666667);</script></body></html>'''
(P/'index.html').write_text(doc.replace('CAPTIONS',caphtml))
save('index.motion.json',{'duration':16.166666667,'assertions':[{'kind':'appearsBy','selector':'#wide-video','bySec':.1},{'kind':'appearsBy','selector':'#site-inner','bySec':.5},{'kind':'appearsBy','selector':'#return-inner','bySec':5.7},{'kind':'appearsBy','selector':'#close-video','bySec':11.5},{'kind':'appearsBy','selector':'#end','bySec':14.05},*({'kind':'staysInFrame','selector':'#'+c['id']} for c in caps),{'kind':'staysInFrame','selector':'#site-cue'},{'kind':'staysInFrame','selector':'#return-cue'}]})
print('Built Short03, 388 frames / 16.166667s; narration excludes next Nobody.')
