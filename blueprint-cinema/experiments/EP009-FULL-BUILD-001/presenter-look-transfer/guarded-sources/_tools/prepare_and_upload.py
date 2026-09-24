#!/usr/bin/env python3
"""Fixed defect repair only: original full clip plus 8 disposable end frames."""
import argparse, datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1];B=D.parents[1];R=B.parents[2]
ALLOWED={'seg009':217,'seg021':241,'seg035':257,'seg072':185,'seg073':225,'seg075':185}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(R))
bound=lambda p:{'path':rel(p),'sha256':sha(p)}
def save(p,d):
 text=json.dumps(d,indent=2)+'\n'
 if p.exists():
  assert p.read_text()==text,'Refuse evidence overwrite '+str(p)
 else:p.write_text(text)
read=lambda p:json.loads(p.read_text())
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def run(cmd):return subprocess.check_output(cmd)
def pcm(path):return run(['ffmpeg','-v','error','-threads','1','-i',str(path),'-map','0:a:0','-vn','-c:a','pcm_f32le','-f','f32le','-'])
def prepare():
 if (D/'MANIFEST.json').exists():raise RuntimeError('Refuse overwrite')
 auditpath=B/'presenter-look-transfer/SOURCE-AUDIT.json';audit=read(auditpath)
 assert sha(auditpath)=='77d1300b3f52841209013af3523124bbca9568061f6cac35fb6026de0184224d'
 entries=[];m=module('review',B/'presenter-look-transfer/_tools/build_review.py')
 for sid,reported_frames in ALLOWED.items():
  row=next(x for x in audit['appearances'] if x['segment']==sid);n=row['duration_frames'];p=R/row['selected_source']['path']
  assert sha(p)==row['selected_source']['sha256'] and 72<=n+8<=360
  out=D/(sid+'-guard8.mov');wav=D/(sid+'-guard8-source-audio.wav')
  assert out.exists()==wav.exists(),'Partial output needs inspection: '+sid
  before=m.video_hashes(p,n);beforefile=D/(sid+'-original-FRAME-HASHES.json');save(beforefile,before)
  source=pcm(p)[:n*2000*8];shortfall=n*2000-len(source)//8
  assert shortfall==0 or (sid=='seg075' and shortfall==288),'Unexpected source-audio shortfall'
  source_payload=source;source+=b'\0'*(shortfall*8)
  pad_to_picture=f'apad=whole_len={n*2000},' if shortfall else ''
  cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(p),'-filter_complex',
   f'[0:v:0]trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop=8[v];[0:a:0]atrim=start_sample=0:end_sample={n*2000},asetpts=PTS-STARTPTS,{pad_to_picture}apad=pad_len=16000[a]',
   '-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p',
   '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-r','24','-fps_mode','cfr',
   '-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
  if not out.exists():
   run(cmd);run(['ffmpeg','-nostdin','-v','error','-i',str(out),'-map','0:a:0','-vn','-c:a','copy',str(wav)])
  frames=m.video_hashes(out,n+8);assert frames['hashes']==before['hashes']+[before['hashes'][-1]]*8
  raw=pcm(out);assert raw==pcm(wav)==source+b'\0'*(16000*8)
  assert out.stat().st_size<200_000_000
  fh=D/(sid+'-FRAME-HASHES.json');save(fh,frames)
  pg=D/(sid+'-PROBE.json');save(pg,json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)])))
  assert sha(p)==row['selected_source']['sha256']
  entries.append({'id':sid,'segment':sid,'source':row['selected_source'],'source_total_frames':n,
   'source_input_frames':[0,n],'source_input_audio_samples':[0,n*2000],
   'input':bound(out),'input_bytes':out.stat().st_size,'input_frames':n+8,'input_duration_seconds':(n+8)/24,
   'select_local_frames':[0,n],'select_original_frames':[0,n],'select_output_frames':row['output_frames'],'selected_frames':n,
   'crop_parts_preserved':row['crop_parts'],'source_audio':bound(wav),'source_audio_format':'stereo 48000Hz float32 little-endian PCM',
   'decoded_original_audio_sha256':hashlib.sha256(source_payload).hexdigest(),'decoded_original_audio_samples_retained':len(source_payload)//8,
   'original_audio_shortfall_zero_padding_samples':shortfall,'decoded_source_audio_sha256':hashlib.sha256(raw).hexdigest(),
   'decoded_source_audio_samples':len(raw)//8,'original_frame_hashes':bound(beforefile),'frame_hashes':bound(fh),
   'decoded_frame_sequence_sha256':frames['sequence_sha256'],'original_payload_exact_decoded_frames':True,'original_payload_exact_decoded_audio':True,
   'probe':bound(pg),'encode_command':cmd,'video_encoding':'libx264 CRF 0 yuv420p, no resize/crop/retime','audio_encoding':'original AAC decoded to pcm_f32le, then exactly 16000 stereo zero samples',
   'reported_failed_wardrobe_frames':reported_frames,
   'guard':{'frames':[n,n+8],'count':8,'source_original_frame':n-1,'decoded_repeated_frame_sha256':before['hashes'][-1],
    'audio_samples':[n*2000,(n+8)*2000],'audio':'16000 zero stereo float32 samples','selected':False,
    'verified_all_8_repeats':True,'verified_all_audio_zeros':True,'reason':'Observed provider truncation; retain all eight guards through wardrobe/background passes; exclude guards from final selection.'},
   'upload_status':'not_uploaded','provider_generation_status':'not_submitted'})
  print(json.dumps({'id':sid,'frames':n+8,'bytes':out.stat().st_size,'exact':True}),flush=True)
 save(D/'MANIFEST.json',{'record_type':'ep009_full_source_guarded_repair','status':'verified_ready_for_storage_upload',
  'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fps':24,'sample_rate':48000,
  'base_build':audit['current_build'],'source_audit':bound(auditpath),'preparation_helper':bound(Path(__file__)),
  'authorization':'Root requested defect-specific repair of these six terminal truncated outputs only; storage upload, no generation or plan changes.',
  'official_schema':{'url':'https://fal.ai/models/fal-ai/kling-video/o3/pro/video-to-video/edit/api','formats':['mp4','mov'],'duration_seconds':[3,15],'max_bytes':200_000_000,'source_prompt_reference':'@Video1','look_prompt_reference':'@Image1'},
  'guard_frames_per_input':8,'errors':[],'slices':entries})
def upload():
 manifest=D/'MANIFEST.json';d=read(manifest);assert d['errors']==[] and {x['id'] for x in d['slices']}==set(ALLOWED)
 trpath=R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py';tr=module('fal_storage',trpath)
 for e in d['slices']:
  p=R/e['input']['path'];assert sha(p)==e['input']['sha256']
  receipt=D/e['id'];receipt.mkdir(exist_ok=True);url=tr.upload(p,receipt,'video/quicktime')
  assert sha(p)==e['input']['sha256'];r=read(receipt/'UPLOAD.json');assert r['status']=='verified' and r['sha256']==e['input']['sha256']
  print(json.dumps({'id':e['id'],'file_url':url,'receipt':bound(receipt/'UPLOAD.json')}),flush=True)
 if (D/'UPLOADS.json').exists():raise RuntimeError('Upload summary exists')
 save(D/'UPLOADS.json',{'record_type':'ep009_verified_fal_storage_uploads','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'manifest':bound(manifest),'transport':bound(trpath),'operation':'upload() only; storage initiate, PUT, GET hash verification; no generation',
  'uploads':[{'id':e['id'],'input':e['input'],'select_local_frames':e['select_local_frames'],'select_output_frames':e['select_output_frames'],
   'frame_hashes':e['frame_hashes'],'fal_url':read(D/e['id']/'UPLOAD.json')['file_url'],'receipt':bound(D/e['id']/'UPLOAD.json'),'status':'verified'} for e in d['slices']],
  'errors':[]})
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','upload']);x=a.parse_args();(prepare if x.mode=='prepare' else upload)()
