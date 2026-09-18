"""Exact343frame review candidate from separately restored, corrected new P08 pictures."""
import hashlib,importlib.util,json,subprocess,wave
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parents[1];R=next(p for p in D.parents if (p/'.agents').is_dir());G=D/'retime-r1';F=D/'final-r1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text());bind=lambda p:{'path':str(Path(p).relative_to(R)),'sha256':sha(p)}
def write(p,d):
 with p.open('x')as f:json.dump(d,f,indent=2);f.write('\n')
assert sha(G/'PLAN.json')=='1de5d83a8b73bdc9faffb120c697e024bd39999fd7b6e07a978beb206214be19'
plan=read(G/'PLAN.json');master=R/plan['master']['path'];assert sha(master)==plan['master']['sha256']
s=importlib.util.spec_from_file_location('p08_r1',D/'_tools/p08_retime_r1.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);r=m.r
F.mkdir(exist_ok=True);assert not(F/'seg044.mp4').exists()
inputs=[];chains=[];pieces=[]
for i,p in enumerate(plan['parts']):
 pid=p['part_id'];d=G/pid;al=read(d/'ALIGNMENT.json');gate=read(d/'SYNC-GATE.json');assert sha(d/'restored.mp4')==al['restored']['sha256']
 for name,b in gate['artifacts'].items():assert sha(d/name)==b['sha256']
 n=p['master_frames'][1]-p['master_frames'][0];a=al['start_frame'];z=a+n;assert 0<=a<z<=int(al['probe']['nb_read_frames'])
 size='W' if i==0 else 'M';rect=r.rect_for(pid,size)
 inputs+=['-i',str(d/'restored.mp4')];chains.append(f'[{i}:v]trim=start_frame={a}:end_frame={z},setpts=N/(24*TB),{r.crop_filter(rect)},setsar=1,format=yuv420p[v{i}]')
 pieces.append({'part':pid,'output_frames':p['master_frames'],'frames':n,'source_frames':[a,z],'crop_size':size,'crop_rect':rect,'restored':bind(d/'restored.mp4'),'alignment':bind(d/'ALIGNMENT.json'),'crop_measurement':bind(d/'NOSE.json'),'sync_diagnostics':bind(d/'SYNC-GATE.json'),'picture_edit':bind(d/'EDIT-DECISION.json'),'flags':{k:v for k,v in gate['pass_signals'].items() if not v}})
chains+=['[v0][v1]concat=n=2:v=1:a=0[vo]','[2:a]atrim=start_sample=31840000:end_sample=32526000,asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[ao]']
cmd=['ffmpeg','-n','-v','error',*inputs,'-i',str(master),'-filter_complex',';'.join(chains),'-map','[vo]','-map','[ao]','-c:v','libx264','-crf','16','-preset','slow','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(F/'seg044.mp4')]
record={'record_type':'corrected_P08_retimed_new_performance_review_conform','status':'rendering','conform_helper':bind(Path(__file__)), 'processing_helpers':[bind(D/'_tools/p08_retime_r1.py'),bind(D/'_tools/p08_retime_r1_lexical.py')], 'plan':bind(G/'PLAN.json'),'master':plan['master'],'output_frames':[15920,16263],'frames':343,'pieces':pieces,'command':cmd,'owner_accepted':False,'existing14performances_modified':False,'diagnostic_guide_in_final':False}
write(F/'CONFORM-INTENT.json',record);subprocess.run(cmd,check=True)
with wave.open(str(master),'rb')as w:
 assert(w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,1,2);w.setpos(31840000);raw=w.readframes(686000)
with wave.open(str(F/'narration-exact-master.wav'),'wb')as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(raw)
record.update(status='rendered_pending_review',output=bind(F/'seg044.mp4'),exact_narration=bind(F/'narration-exact-master.wav'));write(F/'CONFORM.json',record)
probe=json.loads(r.run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,channels,sample_rate','-of','json',str(F/'seg044.mp4')]))['streams'];v=next(s for s in probe if s['codec_type']=='video');assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',343)
ref=np.frombuffer(raw,dtype='<i2').astype(float)/32768;out=r.pcm(F/'seg044.mp4',2);corr=[];gain=[]
for start in range(0,len(ref),48000):
 x=ref[start:min(start+96000,len(ref))]
 if len(x)<2400 or np.sqrt(np.mean(x*x))<1e-4:continue
 for ch in [0,1]:
  y=out[start:start+len(x),ch];corr.append(float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12)));gain.append(float(20*np.log10((np.linalg.norm(y)+1e-12)/(np.linalg.norm(x)+1e-12))))
errors=[]
if min(corr)<.995:errors.append('master_audio_correlation')
if max(abs(x)for x in gain)>.25:errors.append('master_audio_gain')
if not 686000<=len(out)<=688048:errors.append('audio_length')
subprocess.run(['ffmpeg','-v','error','-i',str(F/'seg044.mp4'),'-f','null','-'],check=True,capture_output=True)
verify={'status':'technical_pass'if not errors else'fail','errors':errors,'output':bind(F/'seg044.mp4'),'conform':bind(F/'CONFORM.json'),'frames':343,'master_sample_range':[31840000,32526000],'program_samples':686000,'decoded_samples':len(out),'minimum_voiced_window_correlation':min(corr),'maximum_absolute_gain_db':max(abs(x)for x in gain),'owner_accepted':False,'sync_flags':{p['part']:p['flags']for p in pieces}}
write(F/'VERIFY.json',verify);print(json.dumps(verify));assert not errors
