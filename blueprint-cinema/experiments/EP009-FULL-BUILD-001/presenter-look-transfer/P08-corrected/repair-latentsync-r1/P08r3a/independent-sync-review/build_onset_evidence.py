import json,hashlib,subprocess,importlib.util
from pathlib import Path
from datetime import datetime,timezone
import cv2,numpy as np
from PIL import Image,ImageDraw
R=Path.cwd(); B=R/'blueprint-cinema/experiments/EP009-FULL-BUILD-001'; P=B/'presenter-look-transfer/P08-corrected'; D=P/'repair-latentsync-r1/P08r3a'; Q=D/'independent-sync-review'
def bind(p):return {'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
spec=importlib.util.spec_from_file_location('sa',B/'presenter/_tools/sync_audit.py');sa=importlib.util.module_from_spec(spec);spec.loader.exec_module(sa)
v=D/'restored-native.mp4';wav=D/'audio/narration.wav'; m=sa.mouth_series(str(v)); assert len(m)==176
raw=subprocess.run(['ffmpeg','-v','error','-i',str(wav),'-ac','1','-ar','48000','-f','s16le','-'],capture_output=True,check=True).stdout
a=np.frombuffer(raw,np.int16).astype(float); hop=480;e=np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0,len(a)-hop,hop)]);thr=max(np.percentile(e,20)*3,e.max()*.06);onsets=[];quiet=0
for j,active in enumerate(e>thr):
 if not active:quiet+=1
 else:
  if quiet>=25:onsets.append(j*.01)
  quiet=0
lag=50/48000; face=np.load(Q/'performance/candidate-trajectories.npz')['face'];cap=cv2.VideoCapture(str(v)); frames=[]
while True:
 ok,im=cap.read()
 if not ok:break
 frames.append(im)
cap.release();groups=[('ONSET-1',list(range(0,26))),('ONSET-2',list(range(48,76))),('PAUSE-ONSET-3',list(range(108,134))),('FINAL-WORD',list(range(154,176)))];windows=[];rows=[]
for k in range(176):
 t=k/25-lag;start=max(0,round(t*48000));end=min(len(a),round((t+.04)*48000));rms=np.sqrt(np.mean(a[start:end]**2))/e.max();rows.append({'native_frame':k,'native_time_s':k/25,'narration_time_s':t,'mouth_gap_faceheight':float(m[k]),'audio_rms_fraction_peak':float(rms)})
for name,ids in groups:
 W,H=260,274; canvas=Image.new('RGB',(W*5,H*((len(ids)+4)//5)),(12,15,18));dr=ImageDraw.Draw(canvas)
 for j,k in enumerate(ids):
  f=face[k];cx=int((f[33,0]+f[263,0])*1920/2);cy=int((f[10,1]+f[152,1])*1080/2);im=frames[k];crop=im[max(0,cy-225):min(1080,cy+225),max(0,cx-250):min(1920,cx+250)];pil=Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)).resize((260,234));x=(j%5)*W;y=(j//5)*H;canvas.paste(pil,(x,y));r=rows[k];dr.text((x+4,y+235),f'f{k} native {k/25:.3f}s / VO {r["narration_time_s"]:.3f}s',fill='white');dr.text((x+4,y+250),f'gap {m[k]:.3f}  audio {r["audio_rms_fraction_peak"]:.3f}',fill='white')
 out=Q/(name+'-FACE-FRAMES.jpg');canvas.save(out,quality=95);windows.append({'label':name,'frames':ids,**bind(out)})
report={'created_at':datetime.now(timezone.utc).isoformat(),'native':bind(v),'narration':bind(wav),'clock_binding':bind(D/'DURATION-HOLD.json'),'fps':25,'native_audio_lag_samples_at48000':50,'clock':'native frame k at narration k/25 - 50/48000 seconds. No media alteration.','method':'Existing FaceMesh mouth_series landmarks13/14 gap/faceheight and original10ms RMS onset rule; audio frame RMS integrates each actual40ms native interval. Descriptive diagnostics; no full-duration or exact phoneme pass.','audio_onsets_seconds':onsets,'audio_threshold_fraction_peak':float(thr/e.max()),'all_native_frames':rows,'images':windows,'coverage_held':True,'owner_accepted':False,'automatic_approval':False}
out=Q/'ONSET-EVIDENCE.json';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(bind(out)))
