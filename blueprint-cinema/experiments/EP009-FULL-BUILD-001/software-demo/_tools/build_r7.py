#!/usr/bin/env python3
"""Prepare an isolated native-tool-focus revision of verified r6; no capture/providers.

R7 may replace only the 706-frame real software interval. It requires one
precomposed, selected-for-review 1280x720/24fps focus plate and preserves the
r6 illustrative F03 establish. Existing files are never overwritten. Audio
stays unchanged.
"""
import argparse,copy,datetime,json,re,subprocess,sys
from pathlib import Path

sys.dont_write_bytecode=True
S=Path(__file__).resolve().parents[1];B=S.parent;A=B/'assembly'
sys.path[:0]=[str(B/'presenter-look-transfer/_tools'),str(A/'_tools')]
from build_r3 import R,bound,read,rel,sha,verify_bound,write,probe
from build_r4 import frame_map,graph_for,nested_bindings
from build_review import video_hashes

BASE=A/'r6-software-demo/ep009-r6-software-demo-review-r1-BUILD.json'
BASE_SHA='e163c43a57cfddcbd141b584c665310ac337f7c1a7adb9fcaacf6002f383b452'
BASE_VERIFY=BASE.with_name(BASE.name.replace('-BUILD.json','-VERIFICATION.json'))
BASE_VERIFY_SHA='a326f2bd6aa0de1ef739c26de4f9380959fb8928cce34b658e899fb14221ddf5'
CONTRACT=S/'TIMING-CONTRACT.json'
CONTRACT_SHA='59f284bdf9de77bcf021eabca2e6f146d842da74d88dea24013e819880334db4'
OWNER_SCOPE=B.parent.parent/'episodes/EP009-direct-booking-recovery/review/source-records/2026-09-19-owner-s13-native-tool-focus.json'
OWNER_SCOPE_SHA='817615da0a5864f8016bd1230b6dd0ab8e3d09a9b0e1d327ddbce04135192ec2'
F03_SCOPE=[16704,16752];SCOPE=[16752,17458];TOTAL=29323
R7_ROOT=S/'r7-tool-focus';R7_CAPTURE=S/'capture/node-red-editor-r7'
R7_PLATE=R7_CAPTURE/'screen-r7-tool-focus-706.mp4'
NATIVE_CAPTURE=R7_CAPTURE/'raw/native-node-red-editor-2560x1440.png'
EDIT_MANIFEST=R7_CAPTURE/'GUIDED-SCREEN-EDIT-MANIFEST.json'
SCREEN_CONFORM=R7_CAPTURE/'SCREEN-R7-CONFORM.json'
D=A/'r7-tool-focus';Q=A/'qa/r7-tool-focus'
PROTECTED=('master','timemap','transcript','revision','owner_scoped_lock','film_selections')
REQUIRED_REVIEW_FLAGS=(
 'real_software_capture','legibility_checked','workflow_sequence_checked',
 'native_tool_surface_checked','tool_focus_legibility_checked',
 'intentional_crop_or_zoom_checked','queued_draft_not_sent_checked','no_send',
)

def entry(base,entry_id):
 matches=[e for e in base['inserts'] if e.get('id')==entry_id]
 if len(matches)!=1:raise ValueError('Required r6 insert missing or duplicated: '+entry_id)
 return matches[0]

def retained_f03(base):
 e=entry(base,'f03-illustrative-establish')
 keys=('id','kind','output_frames','source','source_start_frame','source_total_frames','decoded_frame_sequence_sha256','review')
 retained={k:copy.deepcopy(e[k])for k in keys}
 if retained['kind']!='existing_film' or retained['output_frames']!=F03_SCOPE:raise ValueError('Wrong r6 F03 establish binding')
 return retained

def r6_real_capture(base):
 e=entry(base,'real-node-red-openai-workflow')
 if e.get('kind')!='real_software_capture' or e.get('output_frames')!=SCOPE:raise ValueError('Wrong r6 real-capture binding')
 return e

def raster(path):
 info=probe(path);v=next(s for s in info['streams']if s['codec_type']=='video')
 return int(v['width']),int(v['height'])

def conform_bound(path):
 return {'path':str(path.resolve().relative_to(B)),'sha256':sha(path)}

def verify_conform_bound(binding):
 path=(B/binding['path']).resolve();path.relative_to(B)
 if sha(path)!=binding['sha256']:raise ValueError('Changed conform-bound input: '+str(path))
 return path

def checked_edit_basis(basis,old,plate):
 """Validate the actual static-native/r2 source map used by the preconformed plate."""
 if not isinstance(basis,dict):raise ValueError('R7 source basis missing')
 if verify_bound(basis.get('native_current_configuration_capture',{}))!=NATIVE_CAPTURE:raise ValueError('R7 must bind the clean native Node-RED capture')
 if basis.get('retained_real_test_run')!=old['source'] or basis.get('r7_focus_plate')!=plate:raise ValueError('R7 source-role binding mismatch')
 edit_path=verify_bound(basis.get('guided_edit_manifest',{}));conform_path=verify_bound(basis.get('screen_conform',{}))
 if edit_path!=EDIT_MANIFEST or conform_path!=SCREEN_CONFORM:raise ValueError('R7 must bind current edit and conform records')
 edit=read(edit_path);conform=read(conform_path)
 if edit.get('record_type')!='ep009_r7_guided_screen_edit_manifest' or edit.get('output_frames')!=[0,706]:raise ValueError('Wrong r7 guided-edit manifest')
 if conform.get('output')!=conform_bound(R7_PLATE) or conform.get('source_edit_manifest')!=conform_bound(EDIT_MANIFEST):raise ValueError('Conform/edit/output binding mismatch')
 segments=edit.get('segments',[]);prior=0;r2_starts=[]
 for segment in segments:
  out=segment.get('output_frames');source=verify_conform_bound(segment.get('source',{}));src_frames=segment.get('source_frames')
  if not(isinstance(out,list)and len(out)==2 and isinstance(src_frames,list)and len(src_frames)==2 and out[0]==prior and out[0]<out[1]<=706):raise ValueError('R7 guided edit has gap, overlap or invalid range')
  prior=out[1]
  if source not in (NATIVE_CAPTURE,verify_bound(old['source'])):raise ValueError('R7 guided edit uses an unbound source')
  width,height=raster(source);transform=str(segment.get('transform',''))
  crop=re.search(r'crop \[(\d+),(\d+),(\d+),(\d+)\]',transform)
  if crop:
   x,y,w,h=(int(value)for value in crop.groups())
   if w<2 or h<2 or x+w>width or y+h>height:raise ValueError('R7 crop exceeds source raster')
  if source==NATIVE_CAPTURE:
   if src_frames!=[0,1] or segment.get('kind')!='native_node_red_current_configuration':raise ValueError('Native static source semantics missing')
  else:
   if not(0<=src_frames[0]<src_frames[1]<=706) or segment.get('kind')!='retained_r2_test_recording':raise ValueError('Retained r2 source range invalid')
   r2_starts.append(src_frames[0])
 if prior!=706 or r2_starts!=sorted(r2_starts):raise ValueError('R7 source sequence is not contiguous/causal')
 if basis.get('no_causal_state_reordered') is not True:raise ValueError('R7 causal sequence declaration missing')
 return basis

def checked_base():
 base=read(verify_bound({'path':rel(BASE),'sha256':BASE_SHA}))
 ev=read(verify_bound({'path':rel(BASE_VERIFY),'sha256':BASE_VERIFY_SHA}))
 contract=read(verify_bound({'path':rel(CONTRACT),'sha256':CONTRACT_SHA}))
 owner=read(verify_bound({'path':rel(OWNER_SCOPE),'sha256':OWNER_SCOPE_SHA}))
 if base.get('record_type')!='ep009_r6_software_demo_review_build' or base.get('status')!='encoded_unverified_review_only':raise ValueError('Wrong r6 baseline')
 if ev.get('build')!=bound(BASE) or ev.get('errors') or ev.get('status')!='technical_checks_passed_private_review_candidate':raise ValueError('Wrong verified r6 base')
 if ev.get('output')!={'path':base.get('output'),'sha256':base.get('output_sha256')}:raise ValueError('R6 output binding mismatch')
 verify_bound(ev['output'])
 if contract.get('base_build')!=base.get('base_build') or contract.get('allowed_output_frames')!=[F03_SCOPE[0],SCOPE[1]]:raise ValueError('Wrong inherited timing contract')
 reviewed=owner.get('reviewed_candidate',{})
 if owner.get('episode')!='EP009-direct-booking-recovery' or {k:reviewed.get(k)for k in ('path','sha256')}!=ev['output']:raise ValueError('Wrong owner tool-focus scope')
 for k in PROTECTED:verify_bound(base[k])
 verify_bound(base['selections']);verify_bound(base['direction'])
 nested_bindings(read(verify_bound(base['owner_scoped_lock'])))
 nested_bindings(base['retained_P00']);nested_bindings(base['retained_r5_presenters'])
 if len(base['all_75_rows'])!=75 or len(frame_map(base['all_75_rows']))!=TOTAL:raise ValueError('Wrong baseline clock')
 if [(r['id'],r['output_frames'])for r in base['all_75_rows']if r['scene']=='S13']!=[('seg046',[16609,16987]),('seg047',[16987,17523])]:raise ValueError('S13 bounds changed')
 for source in {s['source']['path']:s['source']for r in base['all_75_rows']for s in r['spans']}.values():verify_bound(source)
 retained_f03(base);r6_real_capture(base)
 return base

def checked_selection(path,base):
 path=path.resolve();path.relative_to(R7_ROOT);m=read(path)
 if m.get('record_type')!='ep009_r7_tool_focus_selections' or m.get('status')!='selected_for_review':raise ValueError('Explicit R7 selected-for-review manifest required')
 for k,v in (
  ('base_build',bound(BASE)),('base_verification',bound(BASE_VERIFY)),
  ('timing_contract',bound(CONTRACT)),('master',base['master']),
  ('r6_selections',base['selections']),('owner_tool_focus_scope',bound(OWNER_SCOPE)),
 ):
  if m.get(k)!=v:raise ValueError('R7 selection binding mismatch: '+k)
 if m.get('r7_scope')!=SCOPE or m.get('retained_f03')!=retained_f03(base):raise ValueError('R7 scope/F03 preservation binding mismatch')
 direction=read(verify_bound(m['direction']))
 for k,v in (
  ('base_build',bound(BASE)),('base_verification',bound(BASE_VERIFY)),
  ('timing_contract',bound(CONTRACT)),('owner_tool_focus_scope',bound(OWNER_SCOPE)),
  ('r7_scope',SCOPE),('retained_f03',retained_f03(base)),
 ):
  if direction.get(k)!=v:raise ValueError('R7 direction binding mismatch: '+k)
 entries=m.get('inserts',[])
 if len(entries)!=1:raise ValueError('R7 requires exactly one precomposed focus insert')
 e=entries[0]
 expected_direction=[{k:e[k]for k in ('id','output_frames','source','source_start_frame')}]
 if direction.get('selected_inserts')!=expected_direction:raise ValueError('Exact R7 source/range direction binding required')
 if e.get('kind')!='real_software_capture' or e.get('output_frames')!=SCOPE:raise ValueError('R7 may replace only the real software interval')
 if not re.fullmatch('[A-Za-z0-9_-]+',e.get('id','')):raise ValueError('Simple R7 insert ID required')
 source=verify_bound(e['source']);start=e.get('source_start_frame');n=e.get('source_total_frames')
 if source.suffix.lower()!='.mp4' or start!=0 or n!=SCOPE[1]-SCOPE[0]:raise ValueError('R7 requires one full-length 706-frame focus plate')
 if source!=R7_PLATE:raise ValueError('R7 must use the declared native-tool-focus plate')
 old=r6_real_capture(base)
 if e['source']==old['source']:raise ValueError('R7 source must differ from the un-focused r6 capture')
 v=next(s for s in probe(source)['streams']if s['codec_type']=='video')
 if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))!=(1280,720,'24/1',n):raise ValueError('Exact 1280x720/24fps/706-frame focus plate required')
 vh=video_hashes(source,n)
 if vh['sequence_sha256']!=e.get('decoded_frame_sequence_sha256'):raise ValueError('Decoded R7 source frame sequence changed')
 review=read(verify_bound(e['review']))
 if review.get('source')!=e['source'] or review.get('source_frames')!=[0,n] or review.get('status')!='reviewed_for_insertion' or review.get('errors')!=[]:raise ValueError('Current exact-interval R7 source review required')
 if review.get('owner_tool_focus_scope')!=bound(OWNER_SCOPE):raise ValueError('R7 source review must bind owner tool-focus scope')
 if not all(review.get(k)is True for k in REQUIRED_REVIEW_FLAGS):raise ValueError('R7 native-tool/legibility/no-send review evidence missing')
 if review.get('email_sending_available') is not False:raise ValueError('R7 review must establish no email sending')
 if not all(review.get(k)for k in ('reviewer','method','limits','evidence')):raise ValueError('R7 review provenance/method/limits missing')
 nested_bindings(review['evidence'])
 basis=checked_edit_basis(m.get('source_basis'),old,e['source'])
 if direction.get('source_basis')!=basis:raise ValueError('R7 direction must bind the exact source basis')
 return m,[{**copy.deepcopy(e),'frames':n,'source_probe':v,'review_record':review,'provider_audio_discarded':True}]

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
 allowed=set(range(*SCOPE));changed={i for i,(a,b)in enumerate(zip(before,after))if a!=b}
 if len(after)!=TOTAL or changed!=allowed:raise ValueError('Unexpected retained/source picture assignment')
 if before[F03_SCOPE[0]:F03_SCOPE[1]]!=after[F03_SCOPE[0]:F03_SCOPE[1]]:raise ValueError('R6 F03 illustrative establish changed')
 for b,a in zip(base['all_75_rows'],rows):
  x,y=copy.deepcopy(b),copy.deepcopy(a);x.pop('spans');y.pop('spans')
  if x!=y:raise ValueError('Protected row metadata changed')
 e=entries[0]
 for i in range(*SCOPE):
  expected=('video',e['source']['path'],e['source']['sha256'],e['source_start_frame']+i-SCOPE[0])
  if after[i]!=expected:raise ValueError('Wrong selected R7 source frame')
 return {'frames_compared':TOTAL,'changed_frames':len(changed),'other_assignments_identical':True,'all75row_metadata_identical':True,'retained_r6_f03_establish_identical':True,'allowed_ranges':[SCOPE]}

def prepare(path):
 base=checked_base();m,entries=checked_selection(path,base);rows=patch(base['all_75_rows'],entries);mapping=mapping_check(base,rows,entries)
 return {'record_type':'ep009_r7_tool_focus_review_build','status':'prepared_not_rendered','version':'r7-tool-focus','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_build':bound(BASE),'base_verification':bound(BASE_VERIFY),'timing_contract':bound(CONTRACT),'r6_selections':copy.deepcopy(base['selections']),'owner_tool_focus_scope':bound(OWNER_SCOPE),'r7_scope':SCOPE,'retained_f03':retained_f03(base),'selections':bound(path),'direction':m['direction'],'source_basis':copy.deepcopy(m['source_basis']),**{k:copy.deepcopy(base[k])for k in PROTECTED},'retained_P00':copy.deepcopy(base['retained_P00']),'retained_r5_presenters':copy.deepcopy(base['retained_r5_presenters']),'all_75_rows':rows,'total_frames':TOTAL,'output_master_frames':[0,TOTAL],'inserts':entries,'mapping_checks':mapping,'builder':bound(Path(__file__)),'graph_helper':bound(A/'_tools/build_r4.py'),'owner_accepted':False,'release_cleared':False,'limits':['Private r7 tool-focus review revision; no publication or owner acceptance inferred.','R6 is the frozen base; only the real software interval [16752,17458) may change, while the F03 illustrative establish remains separately bound and unchanged.','Every source audio track is discarded; locked master supplies the complete unchanged program.','The existing presenter and P00/P08 review limitations remain bound unchanged.']}

def save(data,action,name):
 if not re.fullmatch('ep009-r7-tool-focus-[A-Za-z0-9_-]+',name):raise ValueError('New r7-tool-focus filename required')
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
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['inspect','check','prepare','render']);p.add_argument('--manifest',type=Path);p.add_argument('--name',default='ep009-r7-tool-focus-review-r1');a=p.parse_args()
 if a.action=='inspect':
  checked_base();print(json.dumps({'status':'r6_base_verified_no_r7_selection_or_render','scope':SCOPE,'retained_f03':F03_SCOPE,'timing_contract':bound(CONTRACT),'owner_tool_focus_scope':bound(OWNER_SCOPE)}));return 0
 if not a.manifest:p.error('--manifest is required')
 d=prepare(a.manifest.resolve())
 if a.action=='check':print(json.dumps({'status':'r7_inputs_checked_not_rendered','mapping':d['mapping_checks']}));return 0
 return save(d,a.action,a.name)

if __name__=='__main__':
 try:raise SystemExit(main())
 except(ValueError,KeyError,OSError,subprocess.CalledProcessError)as e:print('ERROR: '+str(e),file=sys.stderr);raise SystemExit(2)
