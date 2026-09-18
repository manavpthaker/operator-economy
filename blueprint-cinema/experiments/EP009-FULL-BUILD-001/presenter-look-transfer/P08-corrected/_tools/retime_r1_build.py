import datetime, hashlib, importlib.util, json, subprocess, shutil, wave
from pathlib import Path
import numpy as np
import cv2
R=Path('/Users/brownmanbrain/GitHub/operator-economy');D=R/'blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/P08-corrected';O=D/'retime-r1';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
bind=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
def write(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
plan=json.loads((D/'PLAN.json').read_text())
for p in plan['parts']:
 pid=p['part_id'];src=D/pid;out=O/pid;out.mkdir(exist_ok=True);(out/'audio').mkdir(exist_ok=True)
 for name in ['narration.wav','narration.mp3','AUDIO.json']:shutil.copy2(src/'audio'/name,out/'audio'/name)
 review=json.loads((src/'NATIVE-REVIEW.json').read_text());anchors=review['token_lag_comparison'];fit=[v for v in anchors if not(pid=='P08r3a' and v['token']=='in')]
 x=np.array([v['narration_anchor_s'] for v in fit]);y=np.array([v['native_anchor_s'] for v in fit]);rate,offset=np.polyfit(x,y,1);assert 1<=rate<=1.3
 nframes=p['master_frames'][1]-p['master_frames'][0]+6
 frame_map=[max(0,min(216,int(np.floor(rate*n+offset*24+.5)))) for n in range(nframes)]
 origpcm=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(src/'native.mp4'),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1'],capture_output=True,check=True).stdout,dtype='<f4')
 positions=(np.arange(nframes*2000)/48000*rate+offset)*48000
 pcm=np.interp(positions,np.arange(len(origpcm)),origpcm,left=0,right=0)
 diag=out/'diagnostic-retimed-guide.wav'
 with wave.open(str(diag),'wb') as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(np.clip(pcm*32768,-32768,32767).astype('<i2').tobytes())
 edl={'record_type':'P08_new_performance_picture_retime','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'part':pid,'source_native':bind(src/'native.mp4'),'source_failed_offsets':bind(src/'NATIVE-OFFSETS.json'),'locked_narration':bind(src/'audio/narration.wav'),'source_plan':bind(D/'PLAN.json'),'authority':'Root delegated corrective production 2026-09-17: only new never-locked P08 pictures; maximum local rate1.3; unchanged native drift gate; one Fal restoration per part within existing$3 cap. No existing14performance retime.','fit':{'model':'native_seconds = rate * locked_narration_seconds + intercept','rate':float(rate),'intercept_seconds':float(offset),'max_local_rate':float(rate),'anchors':fit,'excluded':[v for v in anchors if v not in fit],'excluded_reason':'P08r3a in shares an imprecise narration DTW anchor with hospitality; independently documented before fit.','source_review':bind(src/'NATIVE-REVIEW.json'),'residual_seconds':list(((y-offset)/rate-x).astype(float))},'output_fps':24,'output_frames':nframes,'source_fps':24,'source_frame_count':217,'frame_selection':'nearest source frame at affine mapped output frame timestamp, clamped to actual first/last sourceframe; no optical flow, no speed transitions','source_frame_for_each_output_frame':frame_map,'guide':{'diagnostic_only':True,'method':'Decoded native audio sampled by exact same affine continuous map; zero outside native audio; pitch changes only in disposable diagnostic guide. Locked narration never resampled.','artifact':bind(diag)},'owner_accepted':False}
 write(out/'EDIT-DECISION.json',edl)
 cap=cv2.VideoCapture(str(src/'native.mp4'));frames=[]
 while True:
  ok,im=cap.read()
  if not ok:break
  frames.append(im)
 cap.release();assert len(frames)==217
 cmd=['ffmpeg','-n','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1920x1080','-r','24','-i','pipe:0','-i',str(diag),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','12','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(out/'native.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for idx in frame_map:proc.stdin.write(frames[idx].tobytes())
 proc.stdin.close();assert proc.wait()==0
 write(out/'RETIME.json',{'edit_decision':bind(out/'EDIT-DECISION.json'),'picture_with_diagnostic_guide':bind(out/'native.mp4'),'locked_audio':bind(out/'audio/narration.wav'),'source_original_unchanged':sha(src/'native.mp4')==review['native']['sha256'],'status':'rendered_pending_native_gate_and_motion_review'})
 print(json.dumps({'part':pid,'rate':rate,'intercept':offset,'frames':nframes,'sha256':sha(out/'native.mp4')}),flush=True)
