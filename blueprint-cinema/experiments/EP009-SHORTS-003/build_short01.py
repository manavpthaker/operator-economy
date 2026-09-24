#!/usr/bin/env python3
from pathlib import Path
import hashlib, html, json, shutil, subprocess
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[2]; OUT=ROOT/'01-second-commission'; FULL=REPO/'blueprint-cinema/experiments/EP009-FULL-BUILD-001'
VOICE=FULL/'assembly/r3/narration-master-r3.wav'; WORDS=FULL/'assembly/r3/word-transcript-r3.json'; NATIVE=FULL/'presenter-look-transfer/room-r1/seg009/native.mp4'; LOCK=FULL/'assembly/r8-tool-clarity/FINAL-EPISODE-LOCK-r8.json'
CUTS=[(1328,1427,'W000151','W000165','presenter'),(780,870,'W000089','W000101','proof'),(1220,1300,'W000140','W000149','presenter')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):subprocess.run(args,check=True)
assert sha(VOICE)=='0f0d5d326262813cb5ff5392fb263f15f6a8e871ad22e54c1274ff974037ca85'
assert sha(WORDS)=='0b5175dea2cbb1ac7682cd69b9ab032bc8c544131aae82575140e90ae0d76709'
for p in ['assets/fonts','assets/vendor','compositions','qa']: (OUT/p).mkdir(parents=True,exist_ok=True)
for f in ['supreme-500.woff2','zodiak-700.woff2']:shutil.copy2(REPO/'design-system/boundary-ledger/fonts'/f,OUT/'assets/fonts'/f)
shutil.copy2(ROOT.parent/'EP009-SHORTS-002/03-guest-book/assets/vendor/gsap.min.js',OUT/'assets/vendor/gsap.min.js')
words=json.loads(WORDS.read_text())['words']; wi={w['w_id']:i for i,w in enumerate(words)}
edl=[]; caps=[]; videos=[]; cursor=0; filters=[]
for i,(a,b,w0,w1,kind) in enumerate(CUTS):
    start=cursor/24; dur=(b-a)/24; subset=words[wi[w0]:wi[w1]+1]
    edl.append({'id':i,'source_in_frame':a,'source_out_frame_exclusive':b,'timeline_in_frame':cursor,'duration_frames':b-a,'first_word':w0,'last_word':w1,'text':' '.join(w['token'] for w in subset),'visual':kind,'picture_audio_mode':'presenter_address' if kind=='presenter' else 'silent_graphic'})
    filters.append(f'[0:a]atrim=start={a/24:.9f}:end={b/24:.9f},asetpts=PTS-STARTPTS[a{i}]')
    if kind=='presenter':
        local=a-1207
        # Crop around the face and complete hand action, keeping full native vertical frame.
        vf=f'trim=start_frame={local}:end_frame={b-1207},setpts=PTS-STARTPTS,crop=760:1080:570:0,scale=1080:1534,pad=1080:1920:0:180:color=0x173530,setsar=1'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(NATIVE),'-an','-vf',vf,'-r','24','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/f'assets/presenter-{i}.mp4')])
        edl[-1]['native']={'path':str(NATIVE.relative_to(REPO)),'sha256':sha(NATIVE),'in_frame':local,'out_frame_exclusive':b-1207,'transform':vf}
        videos.append(f'<video id="presenter-{i}" class="clip presenter" src="assets/presenter-{i}.mp4" data-start="{start:.9f}" data-duration="{dur:.9f}" data-media-start="0" data-track-index="1" muted playsinline></video>')
    group=[]
    for j,w in enumerate(subset):
        group.append(w)
        if len(group)>=5 or w['token'].endswith(('.', '?','!')) or j==len(subset)-1:
            t0=start+max(0,group[0]['start']-a/24-.025)
            nxt=subset[j+1]['start'] if j+1<len(subset) else b/24
            t1=min(start+dur,start+(group[-1]['end']+nxt)/2-a/24)
            caps.append({'start':t0,'end':t1,'text':' '.join(x['token'] for x in group),'words':[x['w_id'] for x in group]}); group=[]
    cursor+=b-a
filters.append(''.join(f'[a{i}]' for i in range(3))+'concat=n=3:v=0:a=1[out]')
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(VOICE),'-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s16le',str(OUT/'assets/voice.wav')])
spoken=cursor/24; total=(cursor+54)/24
CSS='''@font-face{font-family:Supreme;src:url(assets/fonts/supreme-500.woff2);font-weight:500}@font-face{font-family:Zodiak;src:url(assets/fonts/zodiak-700.woff2);font-weight:700}*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#173530}#root{position:relative;width:1080px;height:1920px;overflow:hidden;color:#F5F0E6;font:500 40px/1.1 Supreme,sans-serif}.clip{position:absolute}.presenter{inset:0;width:1080px;height:1920px}.context{left:70px;top:76px;width:900px;font-size:47px;z-index:8}.caption{left:70px;top:1260px;width:865px;text-align:center;font-size:62px;line-height:1.12;letter-spacing:-.02em;z-index:20}.caption span{display:inline-block;background:#173530;padding:17px 25px 22px;border-radius:6px}.brand{left:70px;top:1768px;font-size:25px;letter-spacing:.06em;z-index:9}.proof{inset:0;width:1080px;height:1920px;background:#F5F0E6;color:#173530;padding:290px 75px 0;z-index:2}.proof h1{font:700 96px/1.03 Zodiak,serif;letter-spacing:-.035em;margin-bottom:85px}.row{border-top:3px solid #586D74;padding:28px 0 40px}.row small{font-size:28px;letter-spacing:.06em;color:#586D74}.row p{font-size:74px;margin-top:25px}.row.second{border-color:#B5482F}.same{color:#B5482F;font-size:42px;margin-top:28px}.fixture{position:absolute;left:75px;top:1740px;color:#586D74;font-size:26px}.end{inset:0;background:#173530;color:#F5F0E6;z-index:30;padding:365px 78px 0}.end small{font-size:27px;letter-spacing:.06em}.end h1{font:700 103px/1.02 Zodiak,serif;letter-spacing:-.04em;margin-top:65px}.end p{font-size:42px;margin-top:78px;line-height:1.2}.end .action{display:inline-block;background:#F5F0E6;color:#173530;padding:22px 26px;font-size:34px;margin-top:42px}.line{height:8px;width:180px;background:#B5482F;margin-top:45px;transform-origin:0 50%}'''
proof='''<div class="proof"><h1>Same guest.<br>Second commission.</h1><div class="row"><small>FIRST STAY</small><p>Commission paid</p></div><div id="repeat" class="row second"><small>RETURN VISIT</small><p>Commission paid</p><div class="same">SAME CHARGE. AGAIN.</div></div><div class="fixture">Illustrative small-inn story</div></div>'''
end='''<div class="end"><small>THE OPERATOR ECONOMY · EP009</small><h1>What could<br>the inn<br>actually pay?</h1><div class="line"></div><p>The calculation in EP009</p><div class="action">TAP THE RELATED VIDEO →</div></div>'''
# Three authored beats plus a concluding card; proof and close are true subcompositions.
for ident,body,d,anim in [('proof',proof,90/24,"tl.fromTo('#repeat',{y:30,opacity:0},{y:0,opacity:1,duration:.25,ease:'power2.out'},1.1);"),('close',end,54/24,"tl.fromTo('.line',{scaleX:0},{scaleX:1,duration:.25,ease:'power2.out'},0);")]:
    subcss=CSS
    (OUT/f'compositions/{ident}.html').write_text(f'<html><body><template><style>{subcss}#{ident}{{position:absolute;inset:0;width:1080px;height:1920px}}</style><div id="{ident}" data-composition-id="{ident}" data-start="0" data-duration="{d:.9f}" data-width="1080" data-height="1920">{body}</div><script>const tl=gsap.timeline({{paused:true}});{anim}window.__timelines=window.__timelines||{{}};window.__timelines.{ident}=tl;</script></template></body></html>')
caphtml=''.join(f'<div id="caption-{i}" class="clip caption" data-caption-layer="fg" data-start="{c["start"]:.9f}" data-duration="{c["end"]-c["start"]:.9f}" data-track-index="20"><span>{html.escape(c["text"])}</span></div>' for i,c in enumerate(caps))
body=''.join(videos)+f'<div id="proof-host" class="clip" data-composition-id="proof" data-composition-src="compositions/proof.html" data-start="4.125" data-duration="3.75" data-track-index="2"></div><div id="close-host" class="clip" data-composition-id="close" data-composition-src="compositions/close.html" data-start="{spoken:.9f}" data-duration="2.25" data-track-index="30"></div>'+caphtml+f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{spoken:.9f}" data-track-index="10"></audio><div id="context" class="clip context" data-start="0" data-duration="4.125" data-track-index="8">Same guest. Second commission.</div><div id="return-context" class="clip context" data-start="7.875" data-duration="3.333333333" data-track-index="8">The missing arithmetic.</div><div id="opening-brand" class="clip brand" data-start="0" data-duration="4.125" data-track-index="9">THE OPERATOR ECONOMY · EP009</div><div id="return-brand" class="clip brand" data-start="7.875" data-duration="3.333333333" data-track-index="9">THE OPERATOR ECONOMY · EP009</div>'
(OUT/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>EP009 · Second commission · Avatar R3</title><script src="assets/vendor/gsap.min.js"></script><style>{CSS}</style></head><body><main id="root" data-composition-id="main" data-start="0" data-duration="{total:.9f}" data-width="1080" data-height="1920" data-fps="24">{body}</main><script>window.__timelines={{main:gsap.timeline({{paused:true}})}};</script></body></html>')
(OUT/'package.json').write_text(json.dumps({'name':'ep009-short01-avatar-r3','private':True,'type':'module','scripts':{'check':'npx --yes hyperframes@0.8.53 check','render':'npx --yes hyperframes@0.8.53 render'}},indent=2))
(OUT/'hyperframes.json').write_text('{"skill":"general-video"}\n')
(OUT/'index.motion.json').write_text(json.dumps({'duration':total,'assertions':[{'kind':'appearsBy','selector':'#presenter-0','bySec':.1},{'kind':'appearsBy','selector':'#proof-host','bySec':4.25},{'kind':'appearsBy','selector':'#presenter-2','bySec':8},{'kind':'appearsBy','selector':'#close-host','bySec':11.35}]},indent=2))
(OUT/'captions.json').write_text(json.dumps(caps,indent=2))
contract={'status':'private_review_candidate','fps':24,'frame_count':cursor+54,'duration':total,'spoken_duration':spoken,'avatar_spoken_fraction':179/269,'edl':edl,'voice':{'path':str(VOICE.relative_to(REPO)),'sha256':sha(VOICE)},'transcript':{'path':str(WORDS.relative_to(REPO)),'sha256':sha(WORDS)},'lock':{'path':str(LOCK.relative_to(REPO)),'sha256':sha(LOCK)},'related_video':{'required':True,'attached':False,'target_episode':'EP009 r8','url':None},'owner_approved':False,'published':False}
(OUT/'source-contract.json').write_text(json.dumps(contract,indent=2))
(OUT/'BRIEF.md').write_text(f'''---
workflow: general-video
flow: automation
storyboard: no
destination: youtube-shorts
aspect: 1080x1920
length: {total}s
---
Avatar-forward revision of the owner's approved direction. Native synchronized presenter owns opening and return. Exact locked voice only. One3.75s explanatory proof cut demonstrates repeated commission in the illustrative small-inn story. All economics withheld for EP009. Private review render authorized by current rework request. No publication approval.
''')
(OUT/'STORYBOARD.md').write_text('# Avatar-led repeat commission\n\n'+ '\n\n'.join(f'{e["timeline_in_frame"]/24:.3f}s: {e["text"]} Picture: {e["visual"]}.' for e in edl)+'\n\nClose: What could the inn actually pay? Full calculation in EP009. Original gestures/expressions and exact matched speech survive. Full portrait crop preserves hands with quiet mineral head/footer framing. Proof operation establish then trace repeated commission; oxide identifies the repeated charge. No ambient animation. Caption rail clears face. QA must inspect lip sync, hand bounds, original gesture continuity and audible joins.\n')
print(json.dumps({'frames':cursor+54,'duration':total,'edl':edl},indent=2))
