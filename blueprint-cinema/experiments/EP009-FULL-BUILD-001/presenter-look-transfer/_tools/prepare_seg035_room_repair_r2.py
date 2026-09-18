"""Lossless close-only input with disposable guard. No generation."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, subprocess, sys
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];R=T.parents[3];D=T/'room-repair-seg035-r2'
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def b(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
def pcm(p):return subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(p),'-map','0:a:0','-f','f32le','-c:a','pcm_f32le','-'])
D.mkdir(exist_ok=False)
m=module('review',T/'_tools/build_review.py');source=T/'wardrobe-guarded-r2/seg035/native.mp4'
assert sha(source)=='0175794b9654093c243801c1501e00ba4696a367f579ec9df0b682d40e9c2f3e'
before=m.video_hashes(source,265);out=D/'seg035-close-guard8.mov'
cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(source),'-filter_complex','[0:v]trim=end_frame=100,setpts=N/(24*TB),tpad=stop_mode=clone:stop=8[v];[0:a]atrim=end_sample=200000,asetpts=N/SR/TB,apad=whole_len=216000[a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
subprocess.check_call(cmd);after=m.video_hashes(out,108)
assert after['hashes']==before['hashes'][:100]+[before['hashes'][99]]*8
original_audio=pcm(source);actual_audio=pcm(out)
assert len(original_audio)>=200000*8 and actual_audio==original_audio[:200000*8]+bytes(16000*8)
save(D/'FRAME-HASHES.json',after)
plan={'record_type':'ep009_seg035_close_only_room_repair','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'verified_prepared_source_only','owner_accepted':False,'authority':'Root instruction: room output lost original close shot; prepare guarded wardrobe first100frames plus8repeats of frame99, selectonly100. No subsequent wide context and no paid generation.', 'source':b(source),'source_download':b(source.parent/'DOWNLOAD.json'),'source_audit':b(T/'SOURCE-AUDIT.json'),'wardrobe_review':b(source.parent/'qa-selected-r1/REVIEW.json'),'input':b(out),'input_frames':108,'duration_seconds':4.5,'source_frames':[0,100],'select_local_frames':[0,100],'guard_frames':[100,108],'guard_derivation':'Eight repeats of exact decoded source frame99;16000zero audio samples.','original_segment_frames':[0,100],'retime':False,'resize':False,'frame_hashes':b(D/'FRAME-HASHES.json'),'decoded_frames_exact':True,'decoded_source_audio_exact':True,'conditioning_audio_f32le_sha256':hashlib.sha256(actual_audio).hexdigest(),'conditioning_audio_samples':216000,'helper':b(Path(__file__)),'encode_command':cmd,'limits':['Only first100provider frames eligible; all guards excluded.','Locked master audio unchanged; provider input audio never replaces it.','Root owns separately bound failed room and retained-wide review.']}
save(D/'PLAN.json',plan)
tr=module('storage',R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py');receipt=D/'storage';receipt.mkdir();url=tr.upload(out,receipt,'video/quicktime')
save(D/'DELIVERY.json',{'id':'seg035-close','plan':b(D/'PLAN.json'),'input':b(out),'fal_url':url,'upload_receipt':b(receipt/'UPLOAD.json'),'status':'verified_storage_only'})
print(json.dumps({'plan':b(D/'PLAN.json'),'input':b(out),'fal_url':url}),flush=True)
