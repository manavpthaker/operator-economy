#!/usr/bin/env python3
"""Append eight nonselected guards, verify exact payload, or upload storage only."""
import argparse, copy, datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1]
B=D.parents[1];R=B.parents[2];G=D/'guarded-r1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(R))
bound=lambda p:{'path':rel(p),'sha256':sha(p)}
save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
read=lambda p:json.loads(p.read_text())
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def run(cmd):return subprocess.check_output(cmd)
def pcm(path):return run(['ffmpeg','-v','error','-threads','1','-i',str(path),'-map','0:a:0','-vn','-c:a','pcm_f32le','-f','f32le','-'])
def prepare():
 if G.exists():raise RuntimeError('Refuse overwrite guarded-r1')
 original=read(D/'MANIFEST.json');assert original['errors']==[]
 G.mkdir();m=module('review',B/'presenter-look-transfer/_tools/build_review.py')
 entries=[]
 for old in original['slices']:
  p=R/old['input']['path'];assert sha(p)==old['input']['sha256']
  name=old['id'];n=old['input_frames'];out=G/(name+'-guard8.mov');wav=G/(name+'-guard8-source-audio.wav')
  cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(p),'-filter_complex',
   '[0:v:0]tpad=stop_mode=clone:stop=8[v];[0:a:0]apad=pad_len=16000[a]',
   '-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p',
   '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-r','24','-fps_mode','cfr',
   '-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
  run(cmd)
  run(['ffmpeg','-nostdin','-v','error','-i',str(out),'-map','0:a:0','-vn','-c:a','copy',str(wav)])
  frames=m.video_hashes(out,n+8);before=read(R/old['frame_hashes']['path'])
  assert frames['hashes']==before['hashes']+[before['hashes'][-1]]*8
  audio=pcm(out);source_audio=pcm(p)
  assert audio==pcm(wav)==source_audio+b'\0'*(16000*2*4)
  assert len(source_audio)//8==n*2000 and 72<=n+8<=360 and out.stat().st_size<200_000_000
  fh=G/(name+'-FRAME-HASHES.json');save(fh,frames)
  probe=G/(name+'-PROBE.json');save(probe,json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)])))
  e=copy.deepcopy(old)
  e.update({'verified_unguarded_input':old['input'],'input':bound(out),'input_frames':n+8,'input_duration_seconds':(n+8)/24,
   'input_bytes':out.stat().st_size,'source_audio':bound(wav),'decoded_source_audio_sha256':hashlib.sha256(audio).hexdigest(),
   'decoded_source_audio_samples':len(audio)//8,'frame_hashes':bound(fh),'decoded_frame_sequence_sha256':frames['sequence_sha256'],
   'probe':bound(probe),'encode_command':cmd,
   'original_payload_exact_decoded_frames':True,'original_payload_exact_decoded_audio':True,
   'guard':{'frames':[n,n+8],'count':8,'source_original_frame':old['source_input_frames'][1]-1,
    'decoded_repeated_frame_sha256':before['hashes'][-1],'audio_samples':[n*2000,(n+8)*2000],
    'audio':'16000 zero stereo float32 samples','selected':False,'verified_all_8_repeats':True,'verified_all_audio_zeros':True,
    'reason':'Observed provider temporal quantization can shorten output. Preserve these nonselected guards through every wardrobe and background pass; never add them to final selection.'}})
  entries.append(e);print(json.dumps({'id':name,'guarded_frames':n+8,'bytes':out.stat().st_size,'exact':True}),flush=True)
 result=copy.deepcopy(original)
 result.update({'status':'guarded_verified_ready_for_storage_upload','unguarded_preparation':bound(D/'MANIFEST.json'),
  'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preparation_helper':bound(Path(__file__)),
  'guard_frames_per_input':8,'guard_authority':'Root instruction: preserve eight end guards through both edit passes, never select them; original selection intervals unchanged.',
  'provider_quantization_observations':{'source_to_wardrobe_frames':[[220,217],[242,241],[129,129],[161,161],[227,225],[186,185],[288,289]],'provenance':'Root observed completed provider outputs; diagnostic observations, not a guarantee of model length.'},
  'slices':entries})
 save(G/'MANIFEST.json',result)
def upload():
 manifest=G/'MANIFEST.json';d=read(manifest);assert d['errors']==[] and len(d['slices'])==5
 transport=R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py'
 tr=module('fal_storage',transport)
 for e in d['slices']:
  p=R/e['input']['path'];assert sha(p)==e['input']['sha256'] and e['guard']['verified_all_8_repeats']
  receipts=G/e['id'];receipts.mkdir(exist_ok=True)
  url=tr.upload(p,receipts,'video/quicktime')
  assert sha(p)==e['input']['sha256']
  receipt=read(receipts/'UPLOAD.json');assert receipt['status']=='verified' and receipt['sha256']==e['input']['sha256']
  print(json.dumps({'id':e['id'],'file_url':url,'receipt':bound(receipts/'UPLOAD.json')}),flush=True)
 if (G/'UPLOADS.json').exists():raise RuntimeError('Upload summary already exists; receipts preserved')
 save(G/'UPLOADS.json',{'record_type':'ep009_verified_fal_storage_uploads','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'manifest':bound(manifest),'transport':bound(transport),'operation':'upload() only; storage initiate, PUT, GET hash verification; no generation submission',
  'uploads':[{'id':e['id'],'input':e['input'],'select_local_frames':e['select_local_frames'],'select_original_frames':e['select_original_frames'],
   'select_output_frames':e['select_output_frames'],'frame_hashes':e['frame_hashes'],'fal_url':read(G/e['id']/'UPLOAD.json')['file_url'],
   'receipt':bound(G/e['id']/'UPLOAD.json'),'status':'verified'} for e in d['slices']],'errors':[]})
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','upload']);x=a.parse_args()
 (prepare if x.mode=='prepare' else upload)()
