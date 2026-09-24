#!/usr/bin/env python3
"""Conform isolated room repairs at four original crop boundaries; no generation or retiming.
All writes are confined to presenter-look-transfer/final-r1. P00/P08 are prohibited.
"""
import argparse,copy,hashlib,json,subprocess,sys,wave
from pathlib import Path
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];F=T/'final-r1'
sys.path.insert(0,str(T/'_tools'))
import build_review as br
R=br.R
read,sha,bound,verify_bound,write,rel,probe=br.read,br.sha,br.bound,br.verify_bound,br.write,br.rel,br.probe
CROP_PLAN=T/'CROP-REPAIR-PLAN.json'
CROP_PLAN_SHA='6880da86781810bc44cdfcb782f2e247b6bc129e8c48d4d94a49cd97cab78634'
EXPECTED_CROP={
 'seg012':[('seg012-close-r2',[0,152],[0,152]),('seg012-wide-r1',[152,343],[152,343])],
 'seg019':[('seg019-close-r2',[0,38],[0,38]),('seg019a',[38,333],[38,333]),('seg019b',[333,394],[45,106])],
 'seg035':[('seg035-close-r2',[0,100],[0,100]),('seg035-wide-r1',[100,258],[100,258])],
 'seg059':[('seg059-wide-r2',[0,33],[0,33]),('seg059-close-r2',[33,152],[0,119])]}
REQUIRED=tuple(EXPECTED_CROP)

def valid_range(v):
 return isinstance(v,list) and len(v)==2 and all(type(x)is int for x in v) and 0<=v[0]<v[1]

def checked_manifest(path):
 path=path.resolve();path.relative_to(T)
 verify_bound({'path':rel(CROP_PLAN),'sha256':CROP_PLAN_SHA})
 a=read(verify_bound({'path':rel(br.AUDIT),'sha256':br.AUDIT_SHA}))
 base=read(verify_bound({'path':rel(br.BASE),'sha256':br.BASE_SHA}))
 m=read(path)
 if m.get('record_type')!='ep009_existing_performance_room_selections':raise ValueError('Wrong selection manifest type')
 for k,want in [('base_build',bound(br.BASE)),('source_audit',bound(br.AUDIT)),('master',base['master']),('look_reference',a['target_appearance']['L3_image'])]:
  if m.get(k)!=want:raise ValueError('Manifest binding mismatch: '+k)
 for k in ('master','timemap','owner_scoped_lock'):verify_bound(base[k])
 entries=m.get('selections',[]);ids=[e.get('segment')for e in entries]
 if len(ids)!=len(set(ids)) or not ids or not set(ids).issubset(REQUIRED):raise ValueError('Duplicate/unknown segments; P00/P08 prohibited')
 return m,a,base

def check_entry(e,a,base):
 sid=e['segment'];row=next(r for r in a['appearances']if r['segment']==sid);lo,hi=row['output_frames'];n=hi-lo
 original=verify_bound(row['selected_source']);pieces=e.get('pieces',[])
 if not pieces:raise ValueError(sid+': no room picture selections')
 expected=EXPECTED_CROP[sid]
 if len(pieces)!=len(expected):raise ValueError(sid+': incorrect piece count')
 if e.get('crop_repair_plan')!=bound(CROP_PLAN):raise ValueError(sid+': exact crop repair plan binding required')
 repair=read(verify_bound(e['crop_repair_plan']))
 if repair.get('record_type')!='ep009_fixed_crop_room_repair_plan' or repair.get('base_build')!=bound(br.BASE) or repair.get('source_audit')!=bound(br.AUDIT):raise ValueError('Wrong crop repair authority')
 authority=repair['segments'][sid]
 if authority['original_source']!=row['selected_source'] or authority['pieces']!=[{'id':x,'original_frames':y,'source_frames':z}for x,y,z in expected]:raise ValueError('Changed fixed original crop selections')
 br.nested_bindings(authority['evidence'])
 br.nested_bindings(authority['piece_sources'])
 actual=[];framemap=[]
 for p,(pid,original_frames,local_frames) in zip(pieces,expected):
  if p.get('id')!=pid or p.get('original_frames')!=original_frames or p.get('source_frames')!=local_frames:raise ValueError(sid+': changed existing selection/cut boundary')
  if not valid_range(p['source_frames']) or not valid_range(p['original_frames']):raise ValueError('Invalid frame range')
  source=verify_bound(p['source'])
  source_authority=authority['piece_sources'][pid]
  provenance={}
  if source_authority['kind']=='retained_reviewed_native_interval':
   if p['source']!=source_authority['source']:raise ValueError(pid+': retained room source changed')
   provenance={'retained_source_download':source_authority['download']}
  elif source_authority['kind']=='new_isolated_crop_repair':
   if source!=R/source_authority['expected_output_path']:raise ValueError(pid+': wrong repair output path')
   job=read(verify_bound(source_authority['provider_job']))
   receipt_path=R/source_authority['expected_download_path'];receipt=read(receipt_path)
   if job.get('source')!=source_authority['confirmed_input_media_id'] or job.get('segment')!=pid:raise ValueError(pid+': wrong repair job/input binding')
   if receipt.get('job_id')!=job.get('job_id') or receipt.get('sha256')!=p['source']['sha256'] or receipt.get('segment')!=pid:raise ValueError(pid+': stale or wrong repair download receipt')
   provenance={'repair_provider_job':source_authority['provider_job'],'repair_download':bound(receipt_path),'submitted_input':source_authority['submitted_input']}
  else:raise ValueError(pid+': unknown source authority')
  if not source.is_relative_to(T) or source.suffix.lower()!='.mp4' or source.is_relative_to(F):raise ValueError('Room source must be an original new provider MP4 under transfer lane')
  if p['source']['sha256']==row['selected_source']['sha256']:raise ValueError('Original performance is not a room edit')
  info=probe(source);v=next(s for s in info['streams']if s['codec_type']=='video');total=int(v['nb_read_frames'])
  if v['r_frame_rate']!='24/1' or (v['width'],v['height'])not in [(1920,1080),(1280,720)]:raise ValueError(pid+': expected24fps16:9, no retiming allowed')
  if total<local_frames[1]:raise ValueError(pid+': provider lost selected frames; no clone/respeed allowed')
  hashes=br.video_hashes(source,total)
  actual.append({**p,**provenance,'input_probe':v,'input_decoded_frame_sequence_sha256':hashes['sequence_sha256'],'frames':local_frames[1]-local_frames[0]})
  for i,(src_frame,orig_frame)in enumerate(zip(range(*local_frames),range(*original_frames))):
   framemap.append({'output_frame':orig_frame,'master_frame':lo+orig_frame,'source_piece':pid,'source_frame':src_frame,'original_performance_frame':orig_frame})
 if [x['original_performance_frame']for x in framemap]!=list(range(n)):raise ValueError('Dropped/duplicated/reordered original timeline frames')
 review=copy.deepcopy(e.get('scoped_review')or{'status':'pending','flagged':True,'reviewer':None,'method':'not supplied','limits':'No appearance or motion approval inferred from mechanical conform.','evidence':[]})
 evidence=review.get('evidence',[]);br.nested_bindings(evidence)
 if review.get('status')=='complete' and (not evidence or not review.get('reviewer')or not review.get('method')or not review.get('limits')):raise ValueError('Complete review needs explicit reviewer/method/limits and hash-bound evidence')
 # A missing/incomplete review is carried as pending; neither frame hashes nor encode success produce a motion/look pass.
 return {'segment':sid,'output_frames':[lo,hi],'frames':n,'original_source':row['selected_source'],'pieces':actual,'frame_map':framemap,'scoped_review':review,'original_hashes':br.video_hashes(original,n),'master_pcm_sha256':br.audio_digest(verify_bound(base['master']),[lo,hi])}

def pcm_bytes(master,frames):
 lo,hi=[x*2000 for x in frames]
 with wave.open(str(master),'rb')as w:
  if(w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getcomptype())!=(1,2,48000,'NONE'):raise ValueError('Unexpected master format')
  total=w.getnframes();w.setpos(lo);raw=w.readframes(min(hi,total)-lo)
 if hi>total:
  if hi-total>1080:raise ValueError('Unexpected master tail padding')
  raw+=b'\0\0'*(hi-total)
 if len(raw)!=(hi-lo)*2:raise ValueError('Master read shortfall')
 return raw

def conform(path,m,a,base,item):
 sid=item['segment'];n=item['frames'];prefix=F/sid
 endings=['.mp4','-CONFORM-INTENT.json','-CONFORM.json','-FRAME-MAP.json','-FRAME-HASHES.json','-MASTER.wav','-VERIFICATION.json','-SELECTION.json','-graph.txt','-encode.log']
 if any(Path(str(prefix)+s).exists()for s in endings):raise FileExistsError('Preserve prior final-r1 output for '+sid)
 F.mkdir(parents=True,exist_ok=True);F.resolve().relative_to(T.resolve());out=Path(str(prefix)+'.mp4');master=verify_bound(base['master']);raw=pcm_bytes(master,item['output_frames'])
 if hashlib.sha256(raw).hexdigest()!=item['master_pcm_sha256']:raise ValueError('Master PCM digest mismatch')
 inputs=[];chains=[];labels=[]
 for i,p in enumerate(item['pieces']):
  inputs+=['-threads','1','-i',str(verify_bound(p['source']))];start,end=p['source_frames']
  chains.append(f'[{i}:v:0]trim=start_frame={start}:end_frame={end},setpts=N/(24*TB),scale=1280:720:flags=lanczos,setsar=1,format=yuv420p[v{i}]');labels.append(f'[v{i}]')
 if len(labels)==1:chains.append(labels[0]+'null[vo]')
 else:chains.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=0,setpts=N/(24*TB)[vo]')
 lo,hi=[x*2000 for x in item['output_frames']];j=len(labels)
 chains.append(f'[{j}:a:0]atrim=start_sample={lo}:end_sample={hi},asetpts=N/SR/TB,apad=whole_len={n*2000},atrim=end_sample={n*2000},pan=stereo|c0=c0|c1=c0[ao]')
 graph=Path(str(prefix)+'-graph.txt')
 with graph.open('x') as h:h.write(';\n'.join(chains)+'\n')
 cmd=['ffmpeg','-nostdin','-n','-v','error','-filter_complex_threads','2',*inputs,'-i',str(master),'-/filter_complex',str(graph),'-map','[vo]','-map','[ao]','-c:v','libx264','-crf','16','-preset','medium','-threads','2','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(out)]
 intent={'record_type':'ep009_existing_performance_final_conform','status':'rendering','segment':sid,'selection_manifest':bound(path),'base_build':bound(br.BASE),'source_audit':bound(br.AUDIT),'master':base['master'],'look_reference':m['look_reference'],'output_frames':item['output_frames'],'frames':n,'pieces':item['pieces'],'provider_audio_discarded':True,'no_retime_clone_or_frame_interpolation':True,'scoped_review':item['scoped_review'],'crop_repair_plan':bound(CROP_PLAN),'helper':bound(Path(__file__).resolve()),'carrier_helper':bound(Path(br.__file__).resolve()),'graph':bound(graph),'command':cmd,'owner_accepted':False}
 write(Path(str(prefix)+'-CONFORM-INTENT.json'),intent)
 with Path(str(prefix)+'-encode.log').open('x')as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
 sidecar=Path(str(prefix)+'-MASTER.wav')
 with wave.open(str(sidecar),'wb')as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(raw)
 mapfile=Path(str(prefix)+'-FRAME-MAP.json');write(mapfile,{'segment':sid,'original_source':item['original_source'],'pieces':item['pieces'],'frames':item['frame_map'],'method':'Each original segment frame appears once, in order. Source intervals are fixed; no retime or selected guard frames.'})
 vh=br.video_hashes(out,n);hashfile=Path(str(prefix)+'-FRAME-HASHES.json');write(hashfile,{'replacement':vh,'original':item['original_hashes']})
 v=next(s for s in probe(out)['streams']if s['codec_type']=='video')
 if(v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))!=(1280,720,'24/1',n):raise ValueError('Incorrect output format/frame count')
 # Verify encoded audio against the exact sidecar. AAC padding is never part of the program.
 import numpy as np
 decoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-vn','-ac','2','-ar','48000','-f','f32le','pipe:1']),dtype='<f4').reshape(-1,2).astype(float)
 ref=np.frombuffer(raw,dtype='<i2').astype(float)/32768;corr=[];gain=[];errors=[]
 if not len(ref)<=len(decoded)<=len(ref)+2048:errors.append('audio_length')
 for start in range(0,len(ref),48000):
  x=ref[start:min(start+96000,len(ref))]
  if len(x)<2400 or np.sqrt(np.mean(x*x))<1e-4:continue
  for ch in (0,1):
   y=decoded[start:start+len(x),ch]
   if len(y)!=len(x):errors.append('audio_shortfall');continue
   corr.append(float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12)));gain.append(float(20*np.log10((np.linalg.norm(y)+1e-12)/(np.linalg.norm(x)+1e-12))))
 if not corr or min(corr)<.995:errors.append('audio_content_mismatch')
 if not gain or max(abs(x)for x in gain)>.25:errors.append('audio_gain_mismatch')
 # Cut excerpts may carry AAC tail ringing; record it without treating it as selected narration.
 tail=decoded[len(ref):];tailpeak=float(np.max(np.abs(tail)))if len(tail)else 0.0
 conform={**intent,'status':'conformed','output':bound(out),'pcm_sidecar':bound(sidecar),'frame_map':bound(mapfile),'decoded_frame_hashes':bound(hashfile)};conformfile=Path(str(prefix)+'-CONFORM.json');write(conformfile,conform)
 verification={'record_type':'ep009_look_transfer_replacement_verification','status':'verified'if not errors else'failed','segment':sid,'replacement':bound(out),'original_source':item['original_source'],'output_frames':item['output_frames'],'master':base['master'],'look_reference':m['look_reference'],'errors':errors,'technical_complete':not errors,'master_sample_range':[lo,hi],'master_pcm_sha256':item['master_pcm_sha256'],'master_pcm_sidecar':bound(sidecar),'replacement_frame_sequence_sha256':vh['sequence_sha256'],'original_frame_sequence_sha256':item['original_hashes']['sequence_sha256'],'frame_hashes':bound(hashfile),'source_frame_map':bound(mapfile),'conform':bound(conformfile),'scoped_review':item['scoped_review'],'owner_accepted':False,'minimum_audio_window_correlation':min(corr)if corr else None,'maximum_absolute_gain_db':max(abs(x)for x in gain)if gain else None,'decoded_audio_samples':len(decoded),'aac_surplus_samples':len(tail),'aac_surplus_peak':tailpeak,'limits':'Mechanical verification only. Preserved timing is not proof that provider preserved performance. Look/motion judgments come only from explicit scoped review evidence.'}
 verificationfile=Path(str(prefix)+'-VERIFICATION.json');write(verificationfile,verification)
 carrier={'segment':sid,'source':bound(out),'verification':bound(verificationfile),'kind':'look_only_existing_performance','output_frames':item['output_frames'],'frames':n,'source_start_frame':0,'owner_accepted':False};write(Path(str(prefix)+'-SELECTION.json'),carrier)
 print(json.dumps({'segment':sid,'output':bound(out),'technical_complete':not errors,'scoped_review_status':item['scoped_review'].get('status'),'selection':bound(Path(str(prefix)+'-SELECTION.json'))}))
 if errors:raise ValueError('Encoded verification errors: '+','.join(errors))

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['check','render']);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--segment',choices=REQUIRED);args=p.parse_args();path=args.manifest.resolve();m,a,base=checked_manifest(path)
 entries=[e for e in m['selections']if not args.segment or e['segment']==args.segment]
 if not entries:raise ValueError('Requested segment absent from manifest')
 checked=[check_entry(e,a,base)for e in entries]
 if args.action=='check':print(json.dumps({'status':'checked_not_rendered','segments':[x['segment']for x in checked],'frames':sum(x['frames']for x in checked),'output_directory':str(F),'review_states':{x['segment']:x['scoped_review'].get('status')for x in checked}}));return
 for item in checked:conform(path,m,a,base,item)

if __name__=='__main__':
 try:main()
 except(ValueError,KeyError,OSError,subprocess.CalledProcessError,RuntimeError)as e:print('ERROR: '+str(e),file=sys.stderr);raise SystemExit(2)
