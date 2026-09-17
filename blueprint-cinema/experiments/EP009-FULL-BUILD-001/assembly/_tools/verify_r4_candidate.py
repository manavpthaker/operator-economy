#!/usr/bin/env python3
"""Technical checks of the exact flagged P00 candidate; never sync clearance."""
import argparse
import datetime
import json
import sys
from pathlib import Path
sys.dont_write_bytecode=True
from build_r3 import A, bound, read, verify_bound, write, probe
from build_r4 import frame_map, nested_bindings
from build_r4_candidate import BASE, BASE_SHA, CANDIDATE_SHA
from verify_r3 import audio_check
from verify_r2 import video_check, loudness


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);args=p.parse_args()
    path=args.manifest.resolve();path.relative_to(A/'r4');d=read(path)
    if d['record_type']!='ep009_exact_P00_flagged_review_candidate_build' or d['status']!='encoded_candidate_lipsync_unresolved':
        raise ValueError('Exact completed candidate required')
    report=path.with_name(path.name.replace('-BUILD.json','-VERIFICATION.json'))
    if report.exists():raise FileExistsError('Preserve existing verification')
    for key in ('base_build','base_verification','revision','master','timemap','transcript','owner_scoped_lock','film_selections','candidate_instruction','candidate_decision','candidate_builder','graph'):
        verify_bound(d[key])
    for key in ('sources','candidate','protected_artifacts'):nested_bindings(d[key])
    if d.get('review_label'):verify_bound(d['review_label'])
    lock=read(verify_bound(d['owner_scoped_lock']))
    for key in ('source','brand_preview','hospitality_preview','selected_paragraph_audio','selected_script','time_map','master_carrier'):verify_bound(lock[key])
    output=verify_bound({'path':d['output'],'sha256':d['output_sha256']});master=verify_bound(d['master'])
    base=read(BASE);errors=[];count=d['total_frames']
    if d['base_build']['sha256']!=BASE_SHA or d['candidate']['source']['sha256']!=CANDIDATE_SHA:raise ValueError('Unauthorized candidate/base')
    old=frame_map(base['all_75_rows'])[:count];new=frame_map(d['all_75_rows'])
    changed=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y]
    if len(new)!=count or changed!=list(range(86)):errors.append('Only authorized 86 opening picture frames may change')
    if d['master']!=base['master'] or d['owner_scoped_lock']!=base['owner_scoped_lock']:errors.append('Master or lock differs')
    for key in ('sync_cleared','conform_readiness_cleared','owner_accepted','bulk_cleared','release_cleared','delivery_master'):
        if d[key] is not False:errors.append('Candidate cannot clear '+key)
    info=probe(output);v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))!=(1280,720,'24/1',count):errors.append('Video format/count mismatch')
    if (a['sample_rate'],a['channels'])!=('48000',2):errors.append('Audio format mismatch')
    if abs(float(info['format']['duration'])-count/24)>.002:errors.append('Duration mismatch')
    video=video_check(output,count);video.pop('planned_exception',None)
    video['planned_uniform_frames']=[1427] if count>1427 else []
    video['unplanned_uniform_frames']=[f for f in video['uniform_frames'] if f not in video['planned_uniform_frames']]
    if video['unplanned_uniform_frames'] or video['decode_exit_code'] or video['decoded_frames']!=count:errors.append('Video decode/unplanned uniform frame')
    audio=audio_check(output,master,[0,count])
    if audio['compared_samples']!=audio['expected_samples'] or any(audio['decode_exit_codes']):errors.append('Audio decode/sample mismatch')
    if audio['min_voiced_window_corr']<.999 or audio['max_abs_voiced_window_rms_db']>.1:errors.append('Audio identity/level mismatch')
    if not 0<=audio['aac_padding_samples']<=1024 or (d['scope']=='full' and audio['padding_peak_abs']>1e-5):errors.append('Unexpected audio tail')
    for b in d['protected_artifacts']:verify_bound(b)
    result={'record_type':'ep009_exact_P00_candidate_technical_verification','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'technical_checks_failed' if errors else 'technical_checks_passed_lipsync_unresolved_review_candidate',
        'build':bound(path),'output':bound(output),'candidate_instruction':d['candidate_instruction'],'candidate_decision':d['candidate_decision'],'owner_scoped_lock':d['owner_scoped_lock'],
        'candidate_flags_preserved':d['candidate']['diagnostic_flags'],'sync_cleared':False,'owner_accepted':False,'bulk_cleared':False,
        'mapping':{'frames_compared':count,'changed_picture_frames':[0,86],'other_source_assignments_identical':True},
        'protected_artifacts_unchanged':d['protected_artifacts'],'probe':info,'video':video,'audio':audio,'loudness':loudness(output),'errors':errors,
        'limits':['Complete decode/audio and source assignment checks only; P00 sync flags remain unresolved.',
            'No normal-speed audiovisual perception, mouth-sync clearance, owner acceptance, bulk or release clearance.',
            'Opening excerpt may have up to one AAC frame of codec ringing beyond its exact container duration.']}
    write(report,result);print(json.dumps({'status':result['status'],'errors':errors,'report':str(report)},indent=2));return bool(errors)


if __name__=='__main__':raise SystemExit(main())
