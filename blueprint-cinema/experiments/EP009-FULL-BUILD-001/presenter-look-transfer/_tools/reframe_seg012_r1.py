"""Restore exact preexisting crop after room edit normalized framing. No retime."""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];R=T.parents[3];D=T/'room-reframe-r1/seg012'
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def b(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
D.mkdir(parents=True,exist_ok=False);source=T/'room-r1/seg012/native.mp4'
assert sha(source)=='ba86217b7373a2f4dc3e6e0f79f76af3b57d8b74377298f9f3851f7e4abe5007'
out=D/'reframed.mp4';graph='[0:v]split=2[a][b];[a]trim=end_frame=152,setpts=N/(24*TB),crop=1280:720:304:0,setsar=1[c];[b]trim=start_frame=152:end_frame=345,setpts=N/(24*TB),scale=1280:720:flags=lanczos,setsar=1[w];[c][w]concat=n=2:v=1:a=0,format=yuv420p[v]'
base=['ffmpeg','-nostdin','-v','error','-threads','1','-filter_complex_threads','1','-i',str(source),'-filter_complex',graph,'-map','[v]']
cmd=base+['-map','0:a:0','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-c:a','copy','-movflags','+faststart','-map_metadata','-1',str(out)]
subprocess.check_call(cmd)
m=module('review',T/'_tools/build_review.py');after=m.video_hashes(out,345)
text=subprocess.check_output(base+['-an','-r','24','-fps_mode','cfr','-f','framehash','-hash','sha256','-'],text=True)
expected=[l.rsplit(',',1)[-1].strip() for l in text.splitlines() if l and not l.startswith('#')]
assert after['hashes']==expected
def pcm(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-f','f32le','-c:a','pcm_f32le','-'])
original_audio=pcm(source);assert pcm(out)==original_audio
save(D/'FRAME-HASHES.json',after)
save(D/'DERIVATION.json',{'record_type':'ep009_seg012_original_crop_restoration','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'mechanically_verified_not_performance_reviewed','authority':'Root authorized deterministic original crop1280x720x304x0 for first152, retaining wide152..345. No native change.','source':b(source),'source_download':b(source.parent/'DOWNLOAD.json'),'output':b(out),'source_audit':b(T/'SOURCE-AUDIT.json'),'crop_authority':b(T.parent/'presenter/P02/EDIT-R1-seg012.json'),'parts':[{'frames':[0,152],'crop_w_h_x_y':[1280,720,304,0]},{'frames':[152,345],'scale_w_h':[1280,720],'filter':'lanczos'}],'frames':345,'eligible_frames':[0,343],'discarded_guard_frames':[343,345],'fps':24,'retime':False,'decoded_frame_hashes':b(D/'FRAME-HASHES.json'),'all_transformed_frames_exact':True,'conditioning_audio_decoded_unchanged':True,'conditioning_audio_f32le_sha256':hashlib.sha256(original_audio).hexdigest(),'helper':b(Path(__file__)),'command':cmd,'limits':['Restoring original crop is mechanical, not evidence of performance preservation. Independent pixel/landmark review still required.','Original room edit remains unchanged and rejected for its lost close shot.','Final conform uses locked master, never this conditioning audio.']})
print(json.dumps({'output':b(out),'derivation':b(D/'DERIVATION.json')}),flush=True)
