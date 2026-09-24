from pathlib import Path
import json,hashlib,subprocess,html,shutil
P=Path(__file__).resolve().parent
R=P.parents[3]
F=R/'blueprint-cinema/experiments/EP009-FULL-BUILD-001'
master=F/'assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4'
transcript=F/'assembly/r3/word-transcript-r3.json'
s037=F/'presenter-look-transfer/room-r1/seg037/native.mp4'
s035=F/'presenter-look-transfer/room-r1/seg035/native.mp4'
FPS=24
edits=[{'id':'correction','source_in_frame':12495,'source_out_frame_exclusive':12696,'word_in':'W001447','word_out':'W001475','timeline_in_frame':0,'picture_source':str(s037.relative_to(R)),'picture_native_frames':[83,284],'crop':[608,1080,632,0]}, {'id':'constraint','source_in_frame':11307,'source_out_frame_exclusive':11449,'word_in':'W001305','word_out':'W001322','timeline_in_frame':201,'picture_source':str(s035.relative_to(R)),'picture_native_frames':[122,258],'crop':[608,1080,664,0]}]
A=P/'assets';A.mkdir(exist_ok=True)
(A/'fonts').mkdir(exist_ok=True)
for name in ['supreme-400.woff2','supreme-500.woff2','zodiak-700.woff2']:
 shutil.copyfile(R/'design-system/boundary-ledger/fonts'/name,A/'fonts'/name)
# Native picture is sampled at the original 24 fps with no frame extension or retime.
for i,(e,source) in enumerate(zip(edits,[s037,s035])):
 out=A/f'presenter-{i+1}.mp4'
 if not out.exists():
  start,end=e['picture_native_frames'];w,h,x,y=e['crop']
  subprocess.run(['ffmpeg','-v','error','-i',str(source),'-vf',f'trim=start_frame={start}:end_frame={end},setpts=N/(24*TB),crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,setsar=1','-an','-c:v','libx264','-crf','17','-preset','fast','-threads','2','-r','24',str(out)],check=True)
# Select locked audio by exact frame boundaries, concatenate at unity level, no synthesis.
parts=[]
for i,e in enumerate(edits):
 frames=e['source_out_frame_exclusive']-e['source_in_frame'];e['duration_frames']=frames
 parts.append(f'[0:a]atrim=start={e["source_in_frame"]/24:.9f}:end={e["source_out_frame_exclusive"]/24:.9f},asetpts=PTS-STARTPTS[a{i}]')
parts.append('[a0][a1]concat=n=2:v=0:a=1[a]')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-filter_complex',';'.join(parts),'-map','[a]','-c:a','pcm_s24le',str(A/'voice.wav')],check=True)
words=json.loads(transcript.read_text())['words'];by={w['w_id']:w for w in words}
ranges=[(0,1447,1450),(0,1451,1455),(0,1456,1461),(0,1462,1465),(0,1466,1469),(0,1470,1475),(1,1305,1309),(1,1310,1313),(1,1314,1318),(1,1319,1322)]
captions=[]
for i,(ei,lo,hi) in enumerate(ranges):
 e=edits[ei];ws=[by[f'W{n:06}'] for n in range(lo,hi+1)];shift=(e['timeline_in_frame']-e['source_in_frame'])/24
 st=ws[0]['start']+shift;end=min(ws[-1]['end']+shift,(e['timeline_in_frame']+e['duration_frames'])/24)
 captions.append({'id':f'caption-{i:02}', 'start':round(st,6),'duration':round(end-st,6),'text':' '.join(w['token'] for w in ws),'word_ids':[w['w_id'] for w in ws]})
spoken=343/24;cta_start=337/24;total=397/24
caption_html='\n'.join(f'<div class="clip caption" id="{c["id"]}" data-start="{c["start"]:.6f}" data-duration="{c["duration"]:.6f}" data-track-index="20"><span>{html.escape(c["text"])}</span></div>' for c in captions)
index='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>EP009 · What can the inn afford?</title><script src="assets/vendor/gsap.min.js"></script><style>
@font-face{font-family:Supreme;src:url(assets/fonts/supreme-400.woff2);font-weight:400}@font-face{font-family:Supreme;src:url(assets/fonts/supreme-500.woff2);font-weight:500}@font-face{font-family:Zodiak;src:url(assets/fonts/zodiak-700.woff2);font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#173530}#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Supreme,sans-serif}.clip{position:absolute}.overlay{inset:0;width:1080px;height:1920px}.presenter{left:0;top:0;width:1080px;height:1920px;object-fit:fill;z-index:0}.caption{left:72px;top:1260px;width:882px;text-align:center;z-index:30;font-size:62px;font-weight:500;line-height:1.1;letter-spacing:-.02em;color:#F5F0E6}.caption span{display:inline-block;padding:18px 25px 22px;background:#173530;border-radius:7px}.context{left:66px;top:58px;max-width:938px;z-index:10;color:#F5F0E6;font:500 31px/1.1 Supreme,sans-serif;letter-spacing:.03em;padding:16px 20px;background:#173530}.correction{position:absolute;left:74px;top:1034px;width:846px;z-index:10;color:#F5F0E6;font:500 45px/1.1 Supreme,sans-serif;background:#173530;padding:20px 24px;border-left:8px solid #B5482F}.mini{position:absolute;left:74px;top:1044px;z-index:10;background:#173530;color:#F5F0E6;font:500 43px/1.1 Supreme,sans-serif;padding:20px 24px}.end{inset:0;width:1080px;height:1920px;z-index:12;background:#173530;color:#F5F0E6;padding:390px 82px 0}.end-kicker{font:500 27px/1.15 Supreme,sans-serif;letter-spacing:.08em;margin-bottom:45px}.end h1{font:700 100px/1.0 Zodiak,serif;letter-spacing:-.04em}.end p{font:400 42px/1.15 Supreme,sans-serif;margin-top:50px}.end .action{display:inline-block;margin-top:38px;padding:20px 24px;background:#F5F0E6;color:#173530;font:500 34px/1.1 Supreme,sans-serif}.end-rule{height:9px;background:#B5482F;width:150px;margin-top:48px;transform-origin:0 50%}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="[[TOTAL]]" data-width="1080" data-height="1920" data-fps="24">
<video id="presenter-one" class="clip presenter" src="assets/presenter-1.mp4" data-start="0" data-duration="8.375" data-media-start="0" data-track-index="0" muted playsinline></video>
<video id="presenter-two" class="clip presenter" src="assets/presenter-2.mp4" data-start="8.375" data-duration="5.666666667" data-media-start="0" data-track-index="0" muted playsinline></video>
<audio id="locked-voice" class="clip" src="assets/voice.wav" data-start="0" data-duration="SPOKEN" data-track-index="10"></audio>
<div id="context" class="clip context" data-start="0" data-duration="3.625" data-track-index="11">TOTAL BOOKING-SITE COMMISSIONS</div>
<div id="correction-host" class="clip overlay" data-start="1.125" data-duration="2.5" data-track-index="12"><div id="correction" class="correction">≠ Recoverable opportunity</div></div>
<div id="question-host" class="clip overlay" data-start="5.166666667" data-duration="3.208333333" data-track-index="12"><div id="real-question" class="mini">How much can actually shift?</div></div>
CAPTIONS
<section id="end" class="clip end" data-start="CTA" data-duration="2.5" data-track-index="15"><div id="end-body"><div class="end-kicker">THE OPERATOR ECONOMY · EP009</div><h1>What can this inn actually afford?</h1><div id="end-rule" class="end-rule"></div><p>The full calculation in EP009</p><div class="action">TAP THE RELATED VIDEO →</div></div></section>
</div><script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});tl.fromTo('#correction',{y:20,opacity:0},{y:0,opacity:1,duration:.25,ease:'power2.out'},1.125);tl.fromTo('#real-question',{y:18,opacity:0},{y:0,opacity:1,duration:.25,ease:'power2.out'},5.166666667);tl.fromTo('#end-body',{y:26,opacity:.3},{y:0,opacity:1,duration:.25,ease:'power2.out'},CTA);tl.fromTo('#end-rule',{scaleX:0},{scaleX:1,duration:.3,ease:'power2.out'},CTA);window.__timelines.main=tl;</script></body></html>'''
for key,val in [('[[TOTAL]]',f'{total:.9f}'),('SPOKEN',f'{spoken:.9f}'),('CTA',f'{cta_start:.9f}'),('CAPTIONS',caption_html)]:index=index.replace(key,val)
(P/'index.html').write_text(index)
(P/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
(P/'index.motion.json').write_text(json.dumps({'duration':total,'assertions':[{'kind':'appearsBy','selector':'#context','bySec':.1},{'kind':'appearsBy','selector':'#correction','bySec':1.4},{'kind':'appearsBy','selector':'#end-body','bySec':14.4},{'kind':'staysInFrame','selector':'#context'},{'kind':'staysInFrame','selector':'#correction'},{'kind':'staysInFrame','selector':'#end-body'}]},indent=2)+'\n')
sha=lambda p:hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
contract={'status':'private_review_not_owner_accepted','candidate':'EP009-SHORTS-003-04','fps':24,'frames':397,'duration_seconds':total,'speech_frames':343,'presenter_frames':337,'presenter_share_of_speech':337/343,'sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in [master,transcript,s037,s035,F/'presenter-look-transfer/final-r1/seg035.mp4']],'edits':edits,'picture_boundary':'037 native83..284 maps master12495..12696;035 native122..258 maps master11307..11443. Last6 audio frames shown under CTA. No unselected native tail used.','audio_boundary':'Final cutoff11449 excludes next So at477.06s. Opening the from11307 removes setup Its that. Audio unchanged at unity.','claim_boundary':'No amount or percentage retained without its spoken qualifications. Text only identifies total commissions vs recoverable opportunity.','cta':['What can this inn actually afford?','The full calculation in EP009','Tap the related video'],'distribution':{'upload':False,'release':False,'related_video_target':'pending_exact_full_episode'}}
(P/'source-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
print('Built',P,'duration',total)
