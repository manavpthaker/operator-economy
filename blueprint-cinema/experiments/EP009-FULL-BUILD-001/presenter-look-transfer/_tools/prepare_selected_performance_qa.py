#!/usr/bin/env python3
"""Lossless selected-interval diagnostics, then descriptive comparison; no approval."""
import argparse,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
T=Path(__file__).resolve().parents[1];R=next(p for p in T.parents if (p/'.agents').is_dir())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
read=lambda p:json.loads(p.read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('--stage',default='wardrobe-guarded-r2',choices=['wardrobe-guarded-r2']);p.add_argument('--qa-name',default='qa-selected-r1');args=p.parse_args()
 if not args.id.startswith('seg') or not args.id[3:].isalnum() or '/' in args.qa_name:raise ValueError('Invalid path component')
 deliveries=[T/'long-source-slices/guarded-r1/DELIVERY.json',T/'guarded-sources/DELIVERY.json',T/'guarded-sources/addendum-r1/DELIVERY.json',T/'guarded-sources/addendum-r2/DELIVERY.json']
 matches=[(f,e)for f in deliveries if f.exists()for e in read(f)['slices']if e['id']==args.id]
 if len(matches)!=1:raise ValueError('Expected exactly one guarded source record')
 delivery,e=matches[0];d=T/args.stage/args.id;receipt=d/'DOWNLOAD.json';c=read(receipt);candidate=d/'native.mp4';source=R/e['input']['path']
 assert sha(source)==e['input']['sha256'] and sha(candidate)==c['sha256']
 a,z=e['select_local_frames'];n=int(c['probe']['streams'][0]['nb_frames']);assert n>=z
 q=d/args.qa_name
 if q.exists():raise FileExistsError('Preserve prior QA')
 q.mkdir();spec=importlib.util.spec_from_file_location('review',T/'_tools/build_review.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 entries=[]
 for label,path,total in [('source',source,e['input_frames']),('candidate',candidate,n)]:
  before=m.video_hashes(path,total);out=q/(label+'-selected-lossless.mp4')
  cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(path),'-vf',f'trim=start_frame={a}:end_frame={z},setpts=PTS-STARTPTS','-an','-c:v','libx264','-crf','0','-preset','medium','-threads','2','-pix_fmt','yuv420p','-fps_mode','passthrough',str(out)]
  subprocess.run(cmd,check=True);after=m.video_hashes(out,z-a);assert after['hashes']==before['hashes'][a:z]
  entries.append({'role':label,'original':bind(path),'selected':bind(out),'source_frames':[a,z],'selected_frames':z-a,'exact_decoded_pixel_match':True,'frame_sequence_sha256':after['sequence_sha256'],'command':cmd})
 record={'id':args.id,'delivery':bind(delivery),'download':bind(receipt),'helper':bind(Path(__file__).resolve()),'select_original_segment_frames':e['select_original_frames'],'selected_provider_input_frames':[a,z],'guard_frames_excluded':True,'candidate_total_frames':n,'candidate_tail_after_selection':n-z,'inputs':entries,'method':'Lossless diagnostic trims only. No speed change, alignment, resize or crop. Original/provider files preserved.'}
 (q/'INPUTS.json').write_text(json.dumps(record,indent=2)+'\n')
 subprocess.run([sys.executable,str(T/'_tools/compare_performance_r2.py'),'--source',str(q/'source-selected-lossless.mp4'),'--candidate',str(q/'candidate-selected-lossless.mp4'),'--out',str(q/'metrics'),'--source-sha256',entries[0]['selected']['sha256'],'--candidate-sha256',entries[1]['selected']['sha256'],'--contact-count','24'],check=True)
if __name__=='__main__':main()
