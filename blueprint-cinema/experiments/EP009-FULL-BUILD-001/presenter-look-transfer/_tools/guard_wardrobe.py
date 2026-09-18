"""Prepare exact wardrobe pixels with eight disposable tail guards; storage only."""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];R=T.parents[3];D=T/'room-inputs-guarded';D.mkdir(exist_ok=True)
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,d):
 assert not p.exists(),p
 p.write_text(json.dumps(d,indent=2)+'\n')
def run(c):return subprocess.check_output(c)
m=module('review',T/'_tools/build_review.py')
tr=module('storage',R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py')
rows=[]
for sid,n in [('seg028',129),('seg055',161),('seg059',152)]:
 source=T/'wardrobe'/sid/'native.mp4';download=read(source.parent/'DOWNLOAD.json');assert sha(source)==download['sha256']
 nf=int(download['probe']['streams'][0]['nb_frames']);before=m.video_hashes(source,nf)
 out=D/(sid+'-guard8.mov');assert not out.exists()
 cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(source),'-filter_complex',f'[0:v]trim=end_frame={n},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop=8[v];[0:a]atrim=end_sample={n*2000},asetpts=PTS-STARTPTS,apad=whole_len={(n+8)*2000}[a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
 run(cmd);after=m.video_hashes(out,n+8);assert after['hashes']==before['hashes'][:n]+[before['hashes'][n-1]]*8
 assert out.stat().st_size<200_000_000
 fp=D/(sid+'-FRAME-HASHES.json');save(fp,after)
 receipt=D/sid;receipt.mkdir(exist_ok=True);url=tr.upload(out,receipt,'video/quicktime');ur=read(receipt/'UPLOAD.json');assert ur['status']=='verified' and ur['sha256']==sha(out)
 rows.append({'id':sid,'segment':sid,'source':bound(source),'source_job':download['job_id'],'input':bound(out),'input_frames':n+8,'input_duration_seconds':(n+8)/24,'select_local_frames':[0,n],'guard_frames':[n,n+8],'selected_frames':n,'input_bytes':out.stat().st_size,'frame_hashes':bound(fp),'original_payload_exact_decoded_frames':True,'fal_url':url,'upload_receipt':bound(receipt/'UPLOAD.json'),'encode_command':cmd,'master_audio':'Never changed; input audio for conditioning only.'})
 print(json.dumps({'id':sid,'frames':n+8,'verified':True}),flush=True)
save(D/'DELIVERY.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'storage_verified_only_not_generation_authority','slices':rows,'helper':bound(Path(__file__))})
