"""Exact first-shot inputs with nonselected repeat guards; storage only."""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];R=T.parents[3];D=T/'short-room-repairs-r3'
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def b(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')
def pcm(p):return subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(p),'-map','0:a:0','-f','f32le','-c:a','pcm_f32le','-'])
D.mkdir(exist_ok=False);m=module('review',T/'_tools/build_review.py');rows=[]
for sid,seg,n,total,expected in [('seg059-wide','seg059',33,161,'ed8f11aba7404bd38a0f128d17d74890099f3a050fdc8c4031fef0a10b2d171f'),('seg019-close','seg019a',38,337,'e196d23e88fe15fd66ea1e96950896f2c5c6f165634ac8f410bfd13e3bf86a67')]:
 source=T/'wardrobe-guarded-r2'/seg/'native.mp4';assert sha(source)==expected
 before=m.video_hashes(source,total);out=D/(sid+'-guarded.mov');guard=80-n
 cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(source),'-filter_complex',f'[0:v]trim=end_frame={n},setpts=N/(24*TB),tpad=stop_mode=clone:stop={guard}[v];[0:a]atrim=end_sample={n*2000},asetpts=N/SR/TB,apad=whole_len=160000[a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
 subprocess.check_call(cmd);after=m.video_hashes(out,80);assert after['hashes']==before['hashes'][:n]+[before['hashes'][n-1]]*guard
 original_audio=pcm(source);actual_audio=pcm(out);assert len(original_audio)>=n*2000*8 and actual_audio==original_audio[:n*2000*8]+bytes(guard*2000*8)
 fp=D/(sid+'-FRAME-HASHES.json');save(fp,after)
 rows.append({'id':sid,'source':b(source),'source_download':b(source.parent/'DOWNLOAD.json'),'input':b(out),'input_frames':80,'input_seconds':80/24,'source_frames':[0,n],'select_local_frames':[0,n],'original_segment_frames':[0,n],'guard_frames':[n,80],'guard_derivation':f'{guard} exact repeats of sourceframe{n-1};{guard*2000}zero audio samples.','retime':False,'resize':False,'decoded_frames_exact':True,'decoded_source_audio_exact':True,'conditioning_audio_f32le_sha256':hashlib.sha256(actual_audio).hexdigest(),'frame_hashes':b(fp),'encode_command':cmd})
 print(json.dumps({'id':sid,'input':b(out),'verified':True}),flush=True)
save(D/'PLAN.json',{'record_type':'ep009_isolated_short_shot_room_repairs','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'verified_sources_only_no_generation','authority':'Root revised059wide strategy to first33+47repeats; added019close first38+42repeats. Preserve prior contextual source unused. Upload only; no paid calls.','helper':b(Path(__file__)),'source_audit':b(T/'SOURCE-AUDIT.json'),'superseded_059_wide_context_plan':b(T/'room-repair-seg059-r2/PLAN.json'),'master':b(T.parent/'assembly/r3/narration-master-r3.wav'),'slices':rows,'limits':['Guards exist only to meet provider minimum3seconds and protect terminal selected frames. Never select the guards.','No later crop context; preserve original camera transition at33/38 using separately reviewed following pieces.','All failed outputs and prior sources remain immutable.','Provider audio is conditioning only; use locked master in final conform.']})
tr=module('storage',R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py');deliveries=[]
for row in rows:
 folder=D/row['id'];folder.mkdir();url=tr.upload(R/row['input']['path'],folder,'video/quicktime')
 deliveries.append(dict(row,fal_url=url,upload_receipt=b(folder/'UPLOAD.json')));print(json.dumps({'id':row['id'],'fal_url':url}),flush=True)
save(D/'DELIVERY.json',{'status':'verified_storage_only','plan':b(D/'PLAN.json'),'slices':deliveries})
