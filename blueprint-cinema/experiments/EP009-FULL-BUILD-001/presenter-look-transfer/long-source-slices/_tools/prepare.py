#!/usr/bin/env python3
"""Five fixed lossless inputs only. No upload, generation or current-plan edits."""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
D=Path(__file__).resolve().parents[1]
B=D.parents[1]
R=B.parents[2]
helper=B/'presenter-look-transfer/_tools/build_review.py'
s=importlib.util.spec_from_file_location('review',helper)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(R))
bound=lambda p:{'path':rel(p),'sha256':sha(p)}
save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
sources={
 'seg019':{'path':B/'presenter/P03/final/seg019.mp4','sha256':'9a9f1e27faf7e2b421f37065ec4f7d05d8af9d461874d48ff3349a0f4cc411df','frames':394,'output_start':4450,'crop_cuts':[38,333]},
 'seg071':{'path':B/'presenter/P11/final/seg071.mp4','sha256':'b8afa8379f3505004cfa0928dca2caa6efe2bf237add0813e7d89fda09a09fb8','frames':514,'output_start':27917,'crop_cuts':[30,97,449]},
}
specs=[('seg019a','seg019',0,333,0,333),('seg019b','seg019',288,394,45,106),
       ('seg071a','seg071',0,120,0,97),('seg071b','seg071',97,449,0,352),('seg071c','seg071',418,514,31,96)]
def run(cmd):return subprocess.check_output(cmd)
def pcm(path):return run(['ffmpeg','-v','error','-threads','1','-i',str(path),'-map','0:a:0','-vn','-c:a','pcm_f32le','-f','f32le','-'])
def main():
 if (D/'MANIFEST.json').exists():raise RuntimeError('Immutable preparation already exists')
 original={};video={}
 for sid,row in sources.items():
  assert sha(row['path'])==row['sha256']
  video[sid]=m.video_hashes(row['path'],row['frames'])
  original[sid]=pcm(row['path'])
  assert len(original[sid])>=row['frames']*2000*8
  save(D/(sid+'-original-FRAME-HASHES.json'),video[sid])
 entries=[]
 for name,sid,a,z,p,q in specs:
  row=sources[sid];assert 72<=z-a<=360 and 0<=p<q<=z-a
  out=D/(name+'.mov');wav=D/(name+'-source-audio.wav')
  if out.exists() or wav.exists():raise RuntimeError('Refuse overwrite '+name)
  cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(row['path']),
   '-filter_complex',f'[0:v:0]trim=start_frame={a}:end_frame={z},setpts=PTS-STARTPTS[v];[0:a:0]atrim=start_sample={a*2000}:end_sample={z*2000},asetpts=PTS-STARTPTS[a]',
   '-map','[v]','-map','[a]','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p',
   '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-r','24','-fps_mode','cfr',
   '-c:a','pcm_f32le','-movflags','+faststart','-map_metadata','-1',str(out)]
  run(cmd)
  run(['ffmpeg','-nostdin','-v','error','-i',str(out),'-map','0:a:0','-vn','-c:a','copy',str(wav)])
  frames=m.video_hashes(out,z-a);expected=video[sid]['hashes'][a:z]
  assert frames['hashes']==expected,'Decoded video mismatch '+name
  raw=pcm(out);raw_wav=pcm(wav);expected_audio=original[sid][a*2000*8:z*2000*8]
  assert raw==raw_wav==expected_audio,'Decoded source audio mismatch '+name
  assert out.stat().st_size<200_000_000
  probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
  vs=next(x for x in probe['streams'] if x['codec_type']=='video')
  aus=next(x for x in probe['streams'] if x['codec_type']=='audio')
  assert (vs['width'],vs['height'],vs['r_frame_rate'],int(vs['nb_frames']))==(1280,720,'24/1',z-a)
  assert (aus['codec_name'],int(aus['sample_rate']),aus['channels'])==('pcm_f32le',48000,2)
  fh=D/(name+'-FRAME-HASHES.json');save(fh,frames)
  pg=D/(name+'-PROBE.json');save(pg,probe)
  e={'id':name,'segment':sid,'source':bound(row['path']),'source_total_frames':row['frames'],
   'source_input_frames':[a,z],'source_input_audio_samples':[a*2000,z*2000],
   'input':bound(out),'input_bytes':out.stat().st_size,'input_frames':z-a,'input_duration_seconds':(z-a)/24,
   'select_local_frames':[p,q],'select_original_frames':[a+p,a+q],
   'select_output_frames':[row['output_start']+a+p,row['output_start']+a+q],
   'selected_frames':q-p,'source_audio':bound(wav),'source_audio_format':'stereo 48000Hz float32 little-endian PCM',
   'decoded_source_audio_sha256':hashlib.sha256(raw).hexdigest(),'decoded_source_audio_samples':len(raw)//8,
   'frame_hashes':bound(fh),'decoded_frame_sequence_sha256':frames['sequence_sha256'],
   'exact_original_decoded_frames':True,'exact_original_decoded_audio':True,'probe':bound(pg),
   'video_encoding':'libx264 CRF 0 yuv420p, no resize/crop/retime','audio_encoding':'pcm_f32le from original AAC decode; no resample or audio processing',
   'encode_command':cmd,'upload_status':'not_uploaded','provider_generation_status':'not_submitted'}
  entries.append(e);print(json.dumps({k:e[k] for k in ('id','input_frames','input_bytes','exact_original_decoded_frames','exact_original_decoded_audio')}),flush=True)
 for sid,row in sources.items():
  selected=[f for e in entries if e['segment']==sid for f in range(*e['select_original_frames'])]
  assert selected==list(range(row['frames']))
  new_cuts=[e['select_original_frames'][0] for e in entries if e['segment']==sid][1:]
  assert all(c in row['crop_cuts'] for c in new_cuts)
  assert sha(row['path'])==row['sha256']
 save(D/'MANIFEST.json',{'record_type':'ep009_exact_source_slices','status':'verified_ready_for_storage_upload',
  'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fps':24,'sample_rate':48000,
  'base_build':bound(B/'assembly/r4/ep009-full-r4-opening-candidate-BUILD.json'),
  'source_audit':bound(B/'presenter-look-transfer/SOURCE-AUDIT.json'),'preparation_helper':bound(Path(__file__)),
  'official_schema':{'url':'https://fal.ai/models/fal-ai/kling-video/o3/pro/video-to-video/edit/api','formats':['mp4','mov'],'duration_seconds':[3,15],'resolution_px':[720,3840],'max_bytes':200_000_000,'source_prompt_reference':'@Video1','look_prompt_reference':'@Image1'},
  'constraints':['No generated frames, retime, crop changes or added edit seams.','Selections reproduce every original frame exactly once in original order.','Only storage upload authorized here; no generation or active plan change.','Original decoded audio retained for provider input; locked episode master remains assembly authority.'],
  'errors':[],'slices':entries})
if __name__=='__main__':main()
