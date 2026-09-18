"""Lossless close-only input with disposable guard. No generation."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, subprocess, sys
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];R=T.parents[3];D=T/'room-repair-seg012-r2'
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def b(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
def pcm(p):return subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(p),'-map','0:a:0','-f','f32le','-c:a','pcm_f32le','-'])
D.mkdir(exist_ok=False)
m=module('review',T/'_tools/build_review.py');source=T/'wardrobe-guarded-r2/seg012/native.mp4'
assert sha(source)=='9fd970b6cce41834a9daa498bfe41e4afcabccb4209cde44e065cf7b9d6d43dc'
before=m.video_hashes(source,345);out=D/'seg012-close-guard8.mov'
cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(source),'-filter_complex','[0:v]trim=end_frame=152,setpts=N/(24*TB),tpad=stop_mode=clone:stop=8[v];[0:a]atrim=end_sample=304000,asetpts=N/SR/TB,apad=whole_len=320000[a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
subprocess.check_call(cmd);after=m.video_hashes(out,160)
assert after['hashes']==before['hashes'][:152]+[before['hashes'][151]]*8
original_audio=pcm(source);actual_audio=pcm(out)
assert len(original_audio)>=304000*8 and actual_audio==original_audio[:304000*8]+bytes(16000*8)
save(D/'FRAME-HASHES.json',after)
plan={'record_type':'ep009_seg012_close_only_room_repair','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'verified_prepared_source_only','owner_accepted':False,'authority':'Root instruction: room output lost original close shot; prepare guarded wardrobe first152frames plus8repeats of frame151, selectonly152. No subsequent wide context and no paid generation.', 'source':b(source),'source_download':b(source.parent/'DOWNLOAD.json'),'source_audit':b(T/'SOURCE-AUDIT.json'),'wardrobe_review':b(source.parent/'qa-selected-r1/REVIEW.json'),'failed_fixed_spatial_recovery':b(T/'room-reframe-r2/seg012/REVIEW.json'),'input':b(out),'input_frames':160,'duration_seconds':160/24,'source_frames':[0,152],'select_local_frames':[0,152],'guard_frames':[152,160],'guard_derivation':'Eight repeats of exact decoded source frame151;16000zero audio samples.','original_segment_frames':[0,152],'retime':False,'resize':False,'frame_hashes':b(D/'FRAME-HASHES.json'),'decoded_frames_exact':True,'decoded_source_audio_exact':True,'conditioning_audio_f32le_sha256':hashlib.sha256(actual_audio).hexdigest(),'conditioning_audio_samples':320000,'helper':b(Path(__file__)),'encode_command':cmd,'limits':['Only first152provider frames eligible; all guards excluded.','Locked master audio unchanged; provider input audio never replaces it.','Root owns separately bound failed room and retained-wide review.']}
save(D/'PLAN.json',plan)
tr=module('storage',R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py');receipt=D/'storage';receipt.mkdir();url=tr.upload(out,receipt,'video/quicktime')
save(D/'DELIVERY.json',{'id':'seg012-close','plan':b(D/'PLAN.json'),'input':b(out),'fal_url':url,'upload_receipt':b(receipt/'UPLOAD.json'),'status':'verified_storage_only'})
print(json.dumps({'plan':b(D/'PLAN.json'),'input':b(out),'fal_url':url}),flush=True)
