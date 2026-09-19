#!/usr/bin/env python3
"""Full technical verification of a separate r6 demo review; no promotion."""
import argparse,copy,datetime,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
import build_r6 as b
from verify_r3 import audio_check
from verify_r2 import video_check,loudness

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('build',type=Path);args=p.parse_args();path=args.build.resolve();path.relative_to(b.D)
 data=b.read(path);report=path.with_name(path.name.replace('-BUILD.json','-VERIFICATION.json'))
 if report==path or report.exists():raise FileExistsError('Preserve existing verification/build')
 if data['record_type']!='ep009_r6_software_demo_review_build' or data['status']!='encoded_unverified_review_only':raise ValueError('Completed full r6 review required')
 base=b.checked_base();errors=[]
 for k in ('base_build','base_verification','timing_contract','selections','direction','builder','graph_helper','graph'):b.verify_bound(data[k])
 if data['base_build']!=b.bound(b.BASE) or data['base_verification']!=b.bound(b.BASE_VERIFY) or data['timing_contract']!=b.bound(b.CONTRACT):raise ValueError('Wrong bound baseline/contract')
 for k in b.PROTECTED:
  b.verify_bound(data[k])
  if data[k]!=base[k]:errors.append('Protected binding changed: '+k)
 if data['retained_P00']!=base['retained_P00'] or data['retained_r5_presenters']!=base['replacements']:errors.append('Presenter records changed')
 if data['total_frames']!=b.TOTAL or data['output_master_frames']!=[0,b.TOTAL]:errors.append('Full timeline changed')
 manifest,entries=b.checked_selection(b.verify_bound(data['selections']),base)
 if entries!=data['inserts']:errors.append('Selected source/review provenance changed')
 expected_rows=b.patch(base['all_75_rows'],entries)
 if expected_rows!=data['all_75_rows']:errors.append('Unexpected row/source map')
 mapping=b.mapping_check(base,data['all_75_rows'],entries)
 graph,inputs=b.graph_for(copy.deepcopy(data))
 if b.verify_bound(data['graph']).read_text()!=graph:errors.append('Emitted graph differs from selected sources')
 actual_inputs=[data['command'][i+1]for i,t in enumerate(data['command'][:-1])if t=='-i']
 expected_inputs=[inputs[i+1]for i,t in enumerate(inputs[:-1])if t=='-i']
 if actual_inputs!=expected_inputs:errors.append('Encoded input order differs from graph')
 output=b.verify_bound({'path':data['output'],'sha256':data['output_sha256']});output.relative_to(b.Q)
 info=b.probe(output);v=next(s for s in info['streams']if s['codec_type']=='video');a=next(s for s in info['streams']if s['codec_type']=='audio')
 if(v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))!=(1280,720,'24/1',b.TOTAL):errors.append('Video format/count')
 if(a['sample_rate'],a['channels'])!=('48000',2):errors.append('Audio format')
 if abs(float(info['format']['duration'])-b.TOTAL/24)>.002:errors.append('Duration')
 video=video_check(output,b.TOTAL);video.pop('planned_exception',None);video['planned_uniform_frames']=[1427];video['unplanned_uniform_frames']=[n for n in video['uniform_frames']if n!=1427]
 if video['decoded_frames']!=b.TOTAL or video['decode_exit_code'] or video['unplanned_uniform_frames']:errors.append('Video decode/unplanned uniform picture')
 audio=audio_check(output,b.verify_bound(data['master']),[0,b.TOTAL])
 if audio['compared_samples']!=58646000 or any(audio['decode_exit_codes']):errors.append('Audio decode/sample count')
 if audio['min_voiced_window_corr']<.999 or audio['max_abs_voiced_window_rms_db']>.1:errors.append('Locked audio identity/level')
 if not 0<=audio['aac_padding_samples']<=1024 or audio['padding_peak_abs']>1e-5:errors.append('Audio tail')
 result={'record_type':'ep009_software_demo_full_review_technical_verification','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'technical_checks_failed'if errors else'technical_checks_passed_private_review_candidate','errors':errors,'build':b.bound(path),'output':b.bound(output),'base_build':b.bound(b.BASE),'master':data['master'],'mapping':mapping,'emitted_graph_matches_selections':graph==b.verify_bound(data['graph']).read_text(),'all_presenter_records_retained':data['retained_r5_presenters']==base['replacements'],'probe':info,'video':video,'audio':audio,'loudness':loudness(output),'owner_accepted':False,'release_cleared':False,'limits':['Full decode, declared source mapping, graph/input binding and audio identity are technical checks; actual screen legibility, workflow truth and audiovisual integration require review.','Existing r5 presenter/P00/P08 limitations remain unchanged; this record does not approve them.']}
 b.write(report,result);print(json.dumps({'status':result['status'],'errors':errors,'report':b.bound(report)}));return bool(errors)
if __name__=='__main__':
 try:raise SystemExit(main())
 except(ValueError,KeyError,OSError)as e:print('ERROR: '+str(e),file=sys.stderr);raise SystemExit(2)
