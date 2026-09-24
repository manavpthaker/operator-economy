from pathlib import Path
import json, subprocess, shutil, hashlib, html

P=Path(__file__).resolve().parent
R=P.parents[3]
F=R/'blueprint-cinema/experiments/EP009-FULL-BUILD-001'
A=P/'assets'; A.mkdir(exist_ok=True)
FPS=24
EDL=[(8790,8883,'opening','If the parts to fix this are cheap, why doesn\'t the inn just do it?'),(16775,16899,'proof','A language model drafts the thank you, the review request, the note about the trail in the fall.'),(5360,5516,'return','I think it can be sold from outside. But only for what it recovers, and what it recovers is a number.')]
D=sum(b-a for a,b,_,_ in EDL)/24
T=D+2.25
def run(args): subprocess.run(args,check=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(src,out,ss,dur,vf):
 if not out.exists() or out.stat().st_size<1000:run(['ffmpeg','-nostdin','-v','error','-y','-threads','1','-ss',str(ss),'-i',str(src),'-t',str(dur),'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','17','-threads','2','-pix_fmt','yuv420p','-r','24','-movflags','+faststart',str(out)])
native=F/'presenter-look-transfer/room-r1'
asset(native/'seg028/native.mp4',A/'opening.mp4',36/24,93/24,'crop=608:1080:680:0,scale=1080:1920:flags=lanczos,setsar=1')
asset(native/'seg021/native.mp4',A/'return.mp4',9/24,156/24,'crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1')
carrier=F/'assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4'
asset(carrier,A/'tools.mp4',16775/24,124/24,'scale=1080:608:flags=lanczos,setsar=1')
asset(carrier,A/'tool-node.mp4',16794/24,60/24,'crop=640:400:640:40,scale=1080:676:flags=lanczos,setsar=1')
master=F/'assembly/r3/narration-master-r3.wav'
if not (A/'voice.wav').exists():
 graph=';'.join(f'[0:a]atrim=start_sample={a*2000}:end_sample={b*2000},asetpts=PTS-STARTPTS[s{i}]' for i,(a,b,_,_) in enumerate(EDL))+';' + ''.join(f'[s{i}]' for i in range(3))+'concat=n=3:v=0:a=1,pan=stereo|c0=c0|c1=c0[out]'
 run(['ffmpeg','-nostdin','-v','error','-y','-i',str(master),'-filter_complex',graph,'-map','[out]','-c:a','pcm_s24le',str(A/'voice.wav')])
shutil.copy(R/'blueprint-cinema/experiments/EP009-SHORTS-002/03-guest-book/assets/vendor/gsap.min.js',A/'gsap.min.js')
shutil.copy(R/'design-system/boundary-ledger/fonts/supreme-500.woff2',A/'supreme-500.woff2')
shutil.copy(R/'design-system/boundary-ledger/fonts/supreme-400.woff2',A/'supreme-400.woff2')
shutil.copy(R/'design-system/boundary-ledger/fonts/boska-700.woff2',A/'boska-700.woff2')
(P/'hyperframes.json').write_text(json.dumps({'$schema':'https://hyperframes.heygen.com/schema/hyperframes.json','paths':{'blocks':'compositions','assets':'assets'},'authoringSkill':'general-video'},indent=2))
(P/'package.json').write_text(json.dumps({'name':'ep009-short02-avatar','private':True,'type':'module','scripts':{'check':'npx --yes hyperframes@0.8.53 check','render':'npx --yes hyperframes@0.8.53 render'}},indent=2))
words=json.loads((F/'assembly/r3/word-transcript-r3.json').read_text())['words']
groups=[['W001024','W001031'],['W001032','W001038'],['W002018','W002024'],['W002025','W002027'],['W002028','W002035'],['W000646','W000653'],['W000654','W000659'],['W000660','W000666']]
caps=[]; source=[]; offset=0
for a,b,key,text in EDL:
 ws=[w for w in words if a/24<=w['start']<b/24]
 source.append({'id':key,'source_in_frame':a,'source_out_frame_exclusive':b,'timeline_in_frame':round(offset*24),'timeline_out_frame_exclusive':round((offset+(b-a)/24)*24),'word_in':ws[0]['w_id'],'word_out':ws[-1]['w_id'],'text':text})
 for first,last in groups:
  if first not in [w['w_id'] for w in ws]:continue
  start=next(i for i,w in enumerate(ws) if w['w_id']==first); end=next(i for i,w in enumerate(ws) if w['w_id']==last)
  selected=ws[start:end+1]
  ca=max(0,offset+selected[0]['start']-a/24-.03); cb=min(offset+(b-a)/24,offset+selected[-1]['end']-a/24+.13)
  caps.append({'start':ca,'end':cb,'text':' '.join(w['token'] for w in selected),'words':[w['w_id'] for w in selected]})
 offset+=(b-a)/24
(P/'captions.json').write_text(json.dumps(caps,indent=2))
contract={'schema':'ep009-short02-avatar-r3','fps':24,'duration_frames':427,'duration_seconds':T,'spoken_duration_frames':373,'presenter_spoken_frames':249,'presenter_spoken_fraction':249/373,'master':{'path':str(master.relative_to(R)),'sha256':sha(master)},'segments':source,'presenter_sources':[{'path':str((native/'seg028/native.mp4').relative_to(R)),'sha256':sha(native/'seg028/native.mp4'),'native_in_frame':36,'native_out_frame_exclusive':129,'crop':[680,0,608,1080]},{'path':str((native/'seg021/native.mp4').relative_to(R)),'sha256':sha(native/'seg021/native.mp4'),'native_in_frame':9,'native_out_frame_exclusive':165,'crop':[656,0,608,1080]}],'tool_carrier':{'path':str(carrier.relative_to(R)),'sha256':sha(carrier)},'constraints':['No voice or performance generation.','No retime, loops, added gestures or expression changes.','Silent 54-frame designed end card.','Private review; exact Related Video target remains unbound.']}
contract['tool_visual_ranges']=[{'asset':'assets/tools.mp4','source_frames':[16775,16794],'timeline_frames':[93,112],'treatment':'Full tool overview, scaled to1080×608'},{'asset':'assets/tool-node.mp4','source_frames':[16794,16854],'timeline_frames':[112,172],'treatment':'OpenAI node crop640×400 at640,40 then1080×676'},{'asset':'assets/tools.mp4','source_frames':[16854,16899],'timeline_frames':[172,217],'treatment':'Returned-draft panel, r8 directed zoom retained'}]
(P/'source-contract.json').write_text(json.dumps(contract,indent=2))
captionhtml='\n'.join(f'<div id="caption-{i}" class="clip caption" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="{20+i}" data-layout-allow-caption-zone><span>{html.escape(c["text"])}</span></div>' for i,c in enumerate(caps))
root=f'''<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
@font-face{{font-family:Supreme;src:url('assets/supreme-500.woff2');font-weight:500}}@font-face{{font-family:Supreme;src:url('assets/supreme-400.woff2');font-weight:400}}@font-face{{font-family:Boska;src:url('assets/boska-700.woff2');font-weight:700}}
*{{box-sizing:border-box}}body{{margin:0}}#root{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Supreme,sans-serif;color:#FBF8F1}}.back{{position:absolute;inset:0;background:#204440}}.presenter{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}.proof-back{{position:absolute;inset:0;background:#204440;z-index:1}}.tool{{z-index:2;position:absolute;left:0;top:480px;width:1080px;height:608px}}.caption{{z-index:4;position:absolute;left:85px;top:1335px;width:830px;min-height:156px;display:flex;justify-content:center;align-items:center;text-align:center;font-size:60px;line-height:1.1;font-weight:500}}.caption span{{display:block;padding:20px 26px;background:#173530;border-radius:12px;color:#FBF8F1}}.hook{{position:absolute;left:85px;top:1130px;width:830px;min-height:148px;font-size:66px;line-height:1.03;font-weight:500;text-align:center}}.hook span{{background:#173530;padding:12px 23px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}.proof-heading{{z-index:3;position:absolute;left:85px;top:235px;width:820px;font-size:76px;line-height:1.04}}.proof-label{{z-index:3;position:absolute;left:85px;top:365px;width:860px;font-size:32px;color:#FBF8F1}}.truth{{z-index:3;position:absolute;left:85px;top:1190px;width:830px;font-size:35px;line-height:1.24;color:#FBF8F1}}.cta{{z-index:6;position:absolute;inset:0;padding:385px 90px 220px;background:#204440;display:flex;flex-direction:column;align-items:flex-start}}.cta h1{{font:700 116px/.98 Boska,serif;margin:0;max-width:890px}}.cta .sub{{font:500 47px/1.2 Supreme,sans-serif;margin-top:72px;max-width:840px}}.cta .link{{font:500 45px/1.15 Supreme,sans-serif;margin-top:70px;padding:24px 0;border-top:3px solid #FBF8F1;border-bottom:3px solid #FBF8F1;width:830px}}.credit{{position:absolute;left:85px;top:1720px;width:830px;font:500 28px/1.3 Supreme,sans-serif;letter-spacing:.06em}}
</style></head><body><main id="root" data-composition-id="ep009-short02-avatar" data-start="0" data-duration="{T}" data-width="1080" data-height="1920" data-fps="24">
<div class="back"></div>
<video id="opening" class="clip presenter" src="assets/opening.mp4" data-start="0" data-duration="3.875" data-track-index="0" muted playsinline></video>
<div id="hook" class="clip hook" data-start="0" data-duration="3.875" data-track-index="3"><span>Why pay for cheap tools?</span></div>
<div id="proof-back" class="clip proof-back" data-start="3.875" data-duration="5.166666666667" data-track-index="1"></div>
<video id="tool-overview" class="clip tool" src="assets/tools.mp4" data-start="3.875" data-duration="0.791666666667" data-track-index="2" muted playsinline></video>
<video id="tool-node" class="clip tool" style="height:676px" src="assets/tool-node.mp4" data-start="4.666666666667" data-duration="2.5" data-track-index="2" muted playsinline></video>
<video id="tool-draft" class="clip tool" src="assets/tools.mp4" data-start="7.166666666667" data-duration="1.875" data-media-start="3.291666666667" data-track-index="2" muted playsinline></video>
<div id="proof-heading" class="clip proof-heading" data-start="3.875" data-duration="5.166666666667" data-track-index="4">The tool can draft.</div>
<div id="proof-label" class="clip proof-label" data-start="3.875" data-duration="5.166666666667" data-track-index="5">Node-RED + OpenAI · recorded workflow</div>
<div id="truth" class="clip truth" data-start="3.875" data-duration="5.166666666667" data-track-index="6">Fictional guest. Awaiting human review. No sending available.</div>
<video id="return" class="clip presenter" src="assets/return.mp4" data-start="9.041666666667" data-duration="6.5" data-track-index="0" muted playsinline></video>
{captionhtml}
<section id="cta" class="clip cta" data-start="{D}" data-duration="2.25" data-track-index="10"><h1>What work would an inn pay for?</h1><p class="sub">The service and the calculation in the full episode.</p><p class="link">EP009 · Tap the related video →</p><p class="credit">THE OPERATOR ECONOMY</p></section>
<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{D}" data-track-index="50" data-volume="1"></audio>
</main><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl.fromTo('#cta h1',{{y:20,opacity:0}},{{y:0,opacity:1,duration:.16,ease:'power2.out',immediateRender:false}},{D});window.__timelines['ep009-short02-avatar']=tl;</script></body></html>'''
(P/'index.html').write_text(root)
(P/'index.motion.json').write_text(json.dumps({'duration':T,'assertions':[{'kind':'appearsBy','selector':'#opening','bySec':.1},{'kind':'appearsBy','selector':'#hook','bySec':.1},{'kind':'appearsBy','selector':'#proof-heading','bySec':4.05},{'kind':'appearsBy','selector':'#return','bySec':9.2},{'kind':'appearsBy','selector':'#cta','bySec':15.75},*({'kind':'staysInFrame','selector':f'#caption-{i}'} for i in range(len(caps))),{'kind':'staysInFrame','selector':'#truth'}]},indent=2))
print(json.dumps({'duration_seconds':T,'frames':427,'presenter_spoken_fraction':249/373}))
