"""Blocked-by-default P08 candidate: approved LatentSync A tail exception + unchanged B."""
import hashlib, importlib.util, json, subprocess, sys, wave
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1];R=next(p for p in D.parents if (p/'.agents').is_dir())
F=D/'final-r2';PLAN=F/'PLAN.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
bind=lambda p:{'path':str(Path(p).relative_to(R)),'sha256':sha(p)}
def write(p,v):
 with p.open('x')as f:json.dump(v,f,indent=2);f.write('\n')
def run(cmd):return subprocess.check_output(cmd)
def hashes(p):
 raw=run(['ffmpeg','-v','error','-threads','1','-i',str(p),'-map','0:v:0','-f','framemd5','-'])
 return [x.decode().split(',')[-1].strip()for x in raw.splitlines()if not x.startswith(b'#')]
def pcm(p,ch=1):
 return np.frombuffer(run(['ffmpeg','-v','error','-i',str(p),'-vn','-ac',str(ch),'-ar','48000','-f','f32le','-']),dtype='<f4').reshape(-1,ch).astype(float)

plan=read(PLAN)
assert plan['master_frames']==[15920,16263] and plan['master_samples']==[31840000,32526000]
assert plan['A']['target_frames']==173 and plan['A']['native_frames']==176 and plan['A']['native_fps']==25
assert plan['A']['added_target_hold_frames']==4 and plan['B']['source_frames']==[2,172]
for name,v in plan['bindings'].items():assert sha(R/v['path'])==v['sha256'],name
master=R/plan['bindings']['master']['path'];native=R/plan['bindings']['A_native']['path'];bsource=R/plan['bindings']['B_restored']['path']
with wave.open(str(master),'rb')as w:
 assert(w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,1,2);w.setpos(31840000);raw=w.readframes(686000)
assert len(raw)==1372000
for name,a,z in [('A_audio',0,346000),('B_audio',346000,686000)]:
 with wave.open(str(R/plan['bindings'][name]['path']),'rb')as w:assert w.readframes(w.getnframes())==raw[a*2:z*2]
if sys.argv[1:] == ['check']:
 print(json.dumps({'status':'inputs_verified_prepared_only','frames':343,'samples':686000,'clearance_exists':(F/'TAIL-EXCEPTION-DECISION.json').exists()}));sys.exit(0)
assert sys.argv[1:] == ['render'],'Use check or render'
clearance=F/'TAIL-EXCEPTION-DECISION.json'
if not clearance.exists():raise SystemExit('Held: missing explicit root tail-exception decision; no media created')
decision=read(clearance)
assert decision['status']=='approved_for_review_candidate' and decision['tail_extension_approved_for_review'] is True
assert decision['owner_accepted'] is False and decision.get('reason')
assert decision['plan']==bind(PLAN)
review=decision['independent_sync_review'];assert sha(R/review['path'])==review['sha256']
assert not(F/'seg044.mp4').exists() and not(F/'A-clock-with-approved-tail.mp4').exists()
write(F/'CONFORM-INTENT.json',{'status':'rendering_explicit_tail_exception','plan':bind(PLAN),'decision':bind(clearance),'independent_sync_review':review,'helper':bind(Path(__file__)),'owner_accepted':False})

# Keep native speech timing. Only normal25->24fps sampling plus the separately approved end hold.
apic=F/'A-clock-with-approved-tail.mp4'
acmd=['ffmpeg','-nostdin','-n','-v','error','-threads','1','-i',str(native),'-an','-vf','fps=24:round=near,tpad=stop_mode=clone:stop=4,setpts=N/(24*TB)',
      '-c:v','libx264','-qp','0','-preset','fast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(apic)]
subprocess.run(acmd,check=True)
h0,h1=hashes(native),hashes(apic);assert len(h0)==176 and len(h1)==173
mapping=[]
for j,h in enumerate(h1):
 candidates=[i for i,v in enumerate(h0)if v==h];assert candidates,'Clock carrier altered decoded picture pixels'
 i=min(candidates,key=lambda k:abs(k/25-j/24));mapping.append(i)
 if j<169:assert abs(i/25-j/24)<=.040001
assert all(b>=a for a,b in zip(mapping,mapping[1:]))
assert all(h==h0[-1]for h in h1[168:]) and mapping[169:]==[175]*4
frame_record={'native':bind(native),'carrier':bind(apic),'native_fps':25,'native_frames':176,'output_fps':24,'output_frames':173,'output_to_native_frame_map':mapping,
 'source_frame_md5':h0,'output_frame_md5':h1,'all_decoded_frames_match_selected_native':True,'native_duration_seconds':176/25,'target_duration_seconds':173/24,
 'ordinary_fps_conform_frames':169,'ordinary_fps_rounding_extension_seconds':169/24-176/25,'explicit_added_hold_frames':4,'explicit_hold_target_range':[169,173],
 'held_native_frame':175,'total_extension_seconds':173/24-176/25,'speech_speed_changed':False,'locked_audio_changed':False,'decision':bind(clearance),'command':acmd}
write(F/'A-FRAME-MAP.json',frame_record)

al=read(R/plan['bindings']['B_alignment']['path']);assert al['start_frame']==2 and int(al['probe']['nb_read_frames'])>=172
brect=plan['B']['crop_rect'];cw,ch,x,y=brect
graph=f'[0:v]trim=start_frame=0:end_frame=173,setpts=N/(24*TB),scale=1280:720:flags=lanczos,setsar=1,format=yuv420p[v0];[1:v]trim=start_frame=2:end_frame=172,setpts=N/(24*TB),crop={cw}:{ch}:{x}:{y},scale=1280:720:flags=lanczos,setsar=1,format=yuv420p[v1];[v0][v1]concat=n=2:v=1:a=0[vo];[2:a]atrim=start_sample=31840000:end_sample=32526000,asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[ao]'
out=F/'seg044.mp4'
cmd=['ffmpeg','-nostdin','-n','-v','error','-threads','1','-i',str(apic),'-i',str(bsource),'-i',str(master),'-filter_complex',graph,'-map','[vo]','-map','[ao]',
     '-c:v','libx264','-crf','16','-preset','slow','-threads','2','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(out)]
subprocess.run(cmd,check=True)
with wave.open(str(F/'narration-exact-master.wav'),'wb')as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(raw)
conform={'record_type':'corrected_P08_LatentSync_A_approved_tail_plus_unchanged_B','status':'rendered_pending_whole_candidate_review','output':bind(out),'plan':bind(PLAN),'decision':bind(clearance),
 'independent_A_sync_review':review,'master':plan['bindings']['master'],'output_frames':[15920,16263],'frames':343,'master_sample_range':[31840000,32526000],
 'exact_narration':bind(F/'narration-exact-master.wav'),'A_frame_map':bind(F/'A-FRAME-MAP.json'),'pieces':[{'part':'P08r3a','frames':173,'local_range':[0,173],'crop':'W','source':bind(apic)},
 {'part':'P08r3b','frames':170,'local_range':[173,343],'crop':'M','source':plan['bindings']['B_restored'],'source_frames':[2,172],'crop_rect':brect,'nose':plan['bindings']['B_nose'],'gate':plan['bindings']['B_gate']}],
 'prior_failed_A_diagnostics_preserved':plan['prior_A_failed_evidence'],'owner_accepted':False,'existing14performances_modified':False,'diagnostic_guide_in_final':False,'helper':bind(Path(__file__)),'command':cmd}
write(F/'CONFORM.json',conform)
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,channels,sample_rate','-of','json',str(out)]))['streams']
v=next(s for s in probe if s['codec_type']=='video');assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',343)
ref=np.frombuffer(raw,dtype='<i2').astype(float)/32768;o=pcm(out,2);corr=[];gain=[]
for a in range(0,len(ref),48000):
 xx=ref[a:min(a+96000,len(ref))]
 if len(xx)<2400 or np.sqrt(np.mean(xx*xx))<1e-4:continue
 for c in [0,1]:
  yy=o[a:a+len(xx),c];corr.append(float(np.dot(xx,yy)/(np.linalg.norm(xx)*np.linalg.norm(yy)+1e-12)));gain.append(float(20*np.log10((np.linalg.norm(yy)+1e-12)/(np.linalg.norm(xx)+1e-12))))
errors=[]
if min(corr)<.995:errors.append('master_audio_correlation')
if max(abs(x)for x in gain)>.25:errors.append('master_audio_gain')
if not 686000<=len(o)<=688048:errors.append('audio_length')
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True,capture_output=True)
verify={'status':'technical_pass_pending_perceptual_review'if not errors else'fail','errors':errors,'output':bind(out),'conform':bind(F/'CONFORM.json'),'frames':343,'master_sample_range':[31840000,32526000],
 'program_samples':686000,'decoded_samples':len(o),'minimum_voiced_window_correlation':min(corr),'maximum_absolute_gain_db':max(abs(x)for x in gain),'tail_extension_disclosed':True,'owner_accepted':False}
write(F/'VERIFY.json',verify);print(json.dumps(verify));assert not errors
