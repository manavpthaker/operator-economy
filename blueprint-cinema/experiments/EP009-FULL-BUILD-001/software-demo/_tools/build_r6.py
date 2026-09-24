#!/usr/bin/env python3
"""Prepare an isolated S13 picture-only revision of frozen r5; no capture/providers.

inspect checks baseline only. check/prepare/render require explicit reviewed
source selections. Existing files are never overwritten. Audio stays unchanged.
"""
import argparse,copy,datetime,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
S=Path(__file__).resolve().parents[1];B=S.parent;A=B/'assembly'
sys.path[:0]=[str(B/'presenter-look-transfer/_tools'),str(A/'_tools')]
from build_r3 import R,bound,read,rel,sha,verify_bound,write,probe
from build_r4 import frame_map,graph_for,nested_bindings
from build_review import video_hashes
BASE=A/'r5-look-transfer/ep009-r5-look-transfer-review-r1-BUILD.json'
BASE_SHA='1e6148a71302c5b1d7cf553d1fb7664576c481b661d3f2d1d072a29197d9e298'
BASE_VERIFY=BASE.with_name(BASE.name.replace('-BUILD.json','-VERIFICATION.json'))
BASE_VERIFY_SHA='4e090b0e38895830aa34250875465c75358cfaaa334bc5efc165467961ad797c'
CONTRACT=S/'TIMING-CONTRACT.json'
CONTRACT_SHA='59f284bdf9de77bcf021eabca2e6f146d842da74d88dea24013e819880334db4'
SCOPE=[16704,17458];TOTAL=29323
D=A/'r6-software-demo';Q=A/'qa/r6-software-demo'
PROTECTED=('master','timemap','transcript','revision','owner_scoped_lock','film_selections')

def checked_base():
 base=read(verify_bound({'path':rel(BASE),'sha256':BASE_SHA}))
 ev=read(verify_bound({'path':rel(BASE_VERIFY),'sha256':BASE_VERIFY_SHA}))
 contract=read(verify_bound({'path':rel(CONTRACT),'sha256':CONTRACT_SHA}))
 if ev['build']!=bound(BASE) or ev['errors'] or ev['status']!='technical_checks_passed_private_review_candidate':raise ValueError('Wrong verified r5 base')
 verify_bound(ev['output'])
 if contract['base_build']!=bound(BASE) or contract['allowed_output_frames']!=SCOPE:raise ValueError('Wrong timing contract')
 for k in PROTECTED:verify_bound(base[k])
 nested_bindings(read(verify_bound(base['owner_scoped_lock'])))
 nested_bindings(base['retained_P00']);nested_bindings(base['replacements'])
 if len(base['all_75_rows'])!=75 or len(frame_map(base['all_75_rows']))!=TOTAL:raise ValueError('Wrong baseline clock')
 if [(r['id'],r['output_frames'])for r in base['all_75_rows']if r['scene']=='S13']!=[('seg046',[16609,16987]),('seg047',[16987,17523])]:raise ValueError('S13 bounds changed')
 for source in {s['source']['path']:s['source']for r in base['all_75_rows']for s in r['spans']}.values():verify_bound(source)
 return base

def ranges(entries):
 prior=SCOPE[0];ids=[]
 for e in entries:
  lo,hi=e['output_frames']
  if type(lo)is not int or type(hi)is not int or not SCOPE[0]<=lo<hi<=SCOPE[1] or lo<prior:raise ValueError('Unordered, overlapping or out-of-S13 insertion')
  if hi-lo<2:raise ValueError('At least two frames per insert required')
  if not re.fullmatch('[A-Za-z0-9_-]+',e['id']):raise ValueError('Simple unique insert ID required')
  ids.append(e['id']);prior=hi
 if not ids or len(set(ids))!=len(ids):raise ValueError('No inserts or duplicate IDs')
 if entries[0]['output_frames'][0]!=SCOPE[0] or prior!=SCOPE[1] or any(a['output_frames'][1]!=b['output_frames'][0]for a,b in zip(entries,entries[1:])):raise ValueError('All754 selected frames must be covered without fallback')

def checked_selection(path,base):
 path=path.resolve();path.relative_to(S);m=read(path)
 if m.get('record_type')!='ep009_software_demo_selections' or m.get('status')!='selected_for_review':raise ValueError('Explicit selected-for-review manifest required')
 for k,v in [('base_build',bound(BASE)),('timing_contract',bound(CONTRACT)),('master',base['master'])]:
  if m.get(k)!=v:raise ValueError('Selection binding mismatch: '+k)
 direction=read(verify_bound(m['direction']))
 if direction.get('base_build')!=bound(BASE) or direction.get('allowed_output_frames')!=SCOPE:raise ValueError('Direction must bind exact r5 and S13 scope')
 if direction.get('selected_inserts')!=[{k:e[k]for k in ('id','output_frames','source','source_start_frame')}for e in m.get('inserts',[])]:raise ValueError('Exact source/range direction binding required')
 entries=m.get('inserts',[]);ranges(entries)
 if not any(e.get('kind')=='real_software_capture'for e in entries):raise ValueError('At least one real software capture required')
 actual=[]
 for e in entries:
  source=verify_bound(e['source']);kind=e.get('kind');lo,hi=e['output_frames'];start=e.get('source_start_frame');n=e.get('source_total_frames')
  if kind not in ('real_software_capture','existing_film'):raise ValueError('Unknown media provenance kind')
  if source.suffix.lower()!='.mp4' or type(start)is not int or type(n)is not int or start<0 or start+hi-lo>n:raise ValueError('Invalid exact video source range')
  if kind=='real_software_capture' and not source.is_relative_to(S):raise ValueError('Screen source must live in isolated software-demo lane')
  if kind=='existing_film' and not source.is_relative_to(B/'film'):raise ValueError('Existing film must bind preserved film source')
  v=next(s for s in probe(source)['streams']if s['codec_type']=='video')
  if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))!=(1280,720,'24/1',n):raise ValueError('Exact1280x720/24fps source count required')
  vh=video_hashes(source,n)
  if vh['sequence_sha256']!=e.get('decoded_frame_sequence_sha256'):raise ValueError('Decoded source frame sequence changed')
  review=read(verify_bound(e['review']))
  if review.get('source')!=e['source'] or review.get('source_frames')!=[start,start+hi-lo] or review.get('status')!='reviewed_for_insertion' or review.get('errors')!=[]:raise ValueError('Current exact-interval source review required')
  if not all(review.get(k)for k in ('reviewer','method','limits','evidence')):raise ValueError('Review provenance/method/limits missing')
  nested_bindings(review['evidence'])
  if kind=='real_software_capture' and (review.get('real_software_capture')is not True or review.get('legibility_checked')is not True or review.get('workflow_sequence_checked')is not True):raise ValueError('Real capture and readable workflow review missing')
  actual.append({**copy.deepcopy(e),'frames':hi-lo,'source_probe':v,'review_record':review,'provider_audio_discarded':True})
 return m,actual

def portion(s,lo,hi):
 a,z=s['output_frames'];p=copy.deepcopy(s);p.update(output_frames=[lo,hi],frames=hi-lo,source_start_frame=s['source_start_frame']+lo-a)
 if 'original_frames'in p:
  if p['original_frames'][1]-p['original_frames'][0]!=z-a:raise ValueError('Nonlinear retained original span unsupported')
  origin=p['original_frames'][0];p['original_frames']=[origin+lo-a,origin+hi-a]
 return p

def patch(rows,entries):
 rows=copy.deepcopy(rows)
 for e in entries:
  lo,hi=e['output_frames']
  for row in rows:
   new=[]
   for s in row['spans']:
    a,z=s['output_frames'];x,y=max(a,lo),min(z,hi)
    if x>=y:new.append(s);continue
    if a<x:new.append(portion(s,a,x))
    p=portion(s,x,y);p.update(kind='video',source=e['source'],source_start_frame=e['source_start_frame']+x-lo,software_demo_insert=e['id'],software_demo_review=e['review'])
    new.append(p)
    if y<z:new.append(portion(s,y,z))
   row['spans']=new
 return rows

def mapping_check(base,rows,entries):
 before,after=frame_map(base['all_75_rows']),frame_map(rows)
 allowed={i for e in entries for i in range(*e['output_frames'])};changed={i for i,(a,b)in enumerate(zip(before,after))if a!=b}
 if len(after)!=TOTAL or changed!=allowed:raise ValueError('Unexpected retained/source picture assignment')
 for b,a in zip(base['all_75_rows'],rows):
  x,y=copy.deepcopy(b),copy.deepcopy(a);x.pop('spans');y.pop('spans')
  if x!=y:raise ValueError('Protected row metadata changed')
 for e in entries:
  for i in range(*e['output_frames']):
   expected=('video',e['source']['path'],e['source']['sha256'],e['source_start_frame']+i-e['output_frames'][0])
   if after[i]!=expected:raise ValueError('Wrong selected source frame')
 return {'frames_compared':TOTAL,'changed_frames':len(changed),'other_assignments_identical':True,'all75row_metadata_identical':True,'allowed_ranges':[e['output_frames']for e in entries]}

def prepare(path):
 base=checked_base();m,entries=checked_selection(path,base);rows=patch(base['all_75_rows'],entries);mapping=mapping_check(base,rows,entries)
 return {'record_type':'ep009_r6_software_demo_review_build','status':'prepared_not_rendered','version':'r6-software-demo','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_build':bound(BASE),'base_verification':bound(BASE_VERIFY),'timing_contract':bound(CONTRACT),'selections':bound(path),'direction':m['direction'],**{k:copy.deepcopy(base[k])for k in PROTECTED},'retained_P00':copy.deepcopy(base['retained_P00']),'retained_r5_presenters':copy.deepcopy(base['replacements']),'all_75_rows':rows,'total_frames':TOTAL,'output_master_frames':[0,TOTAL],'inserts':entries,'mapping_checks':mapping,'builder':bound(Path(__file__)),'graph_helper':bound(A/'_tools/build_r4.py'),'owner_accepted':False,'release_cleared':False,'limits':['Private review revision; no publication or owner acceptance inferred.','Every source audio track is discarded; locked master supplies the complete unchanged program.','The existing presenter and P00/P08 review limitations remain bound unchanged.']}

def save(data,action,name):
 if not re.fullmatch('ep009-r6-software-demo-[A-Za-z0-9_-]+',name):raise ValueError('New r6-software-demo filename required')
 manifest=D/(name+'-BUILD.json');gp=D/(name+'-graph.txt');log=D/(name+'-encode.log');out=Q/(name+'.mp4')
 if any(p.exists()for p in (manifest,gp,log,out)):raise FileExistsError('Preserve existing artifact/version')
 graph,inputs=graph_for(data);D.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
 with gp.open('x')as f:f.write(graph)
 cmd=['ffmpeg','-nostdin','-n','-v','error','-stats','-filter_complex_threads','2',*inputs,'-/filter_complex',str(gp),'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','16','-threads','2','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',str(out)]
 data.update(output=rel(out),graph=bound(gp),command=cmd,encode_log=rel(log),status='rendering_unaccepted_review'if action=='render'else'prepared_not_rendered');write(manifest,data)
 if action=='render':
  with log.open('x')as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
  data.update(encode_exit_code=r.returncode,status='encoded_unverified_review_only'if r.returncode==0 else'failed_partial_preserved')
  if r.returncode==0:data['output_sha256']=sha(out)
  manifest.write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({'status':data['status'],'build':bound(manifest),'output':rel(out)}))
 return data.get('encode_exit_code',0)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['inspect','check','prepare','render']);p.add_argument('--manifest',type=Path);p.add_argument('--name',default='ep009-r6-software-demo-review-r1');a=p.parse_args()
 if a.action=='inspect':
  checked_base();print(json.dumps({'status':'base_verified_no_selections_or_render','scope':SCOPE,'timing_contract':bound(CONTRACT)}));return 0
 if not a.manifest:p.error('--manifest is required')
 d=prepare(a.manifest.resolve())
 if a.action=='check':print(json.dumps({'status':'inputs_checked_not_rendered','mapping':d['mapping_checks']}));return 0
 return save(d,a.action,a.name)
if __name__=='__main__':
 try:raise SystemExit(main())
 except(ValueError,KeyError,OSError,subprocess.CalledProcessError)as e:print('ERROR: '+str(e),file=sys.stderr);raise SystemExit(2)
