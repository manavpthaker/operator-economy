#!/usr/bin/env python3
"""Verify a separate r4 encode against the unchanged r3 narration master."""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from build_r3 import A, FPS, bound, probe, read, verify_bound, write
from build_r4 import nested_bindings
from verify_r3 import audio_check
from verify_r2 import video_check, loudness


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    path = args.manifest.resolve(); path.relative_to(A/'r4')
    data = read(path)
    if data.get('record_type') != 'ep009_r4_review_build' or data.get('status') != 'encoded_unverified_review_only':
        raise ValueError('Expected a completed unverified r4 build')
    for key in ('base_build','base_verification','revision','master','timemap','transcript',
                'owner_scoped_lock','film_selections','opening_plan','presenter_index','presenter_plan','graph'):
        if data.get(key):
            verify_bound(data[key])
    for key in ('sources','presenter_replacements'):
        nested_bindings(data[key])
    if data.get('review_label'):
        verify_bound(data['review_label'])
    lock = read(verify_bound(data['owner_scoped_lock']))
    for key in ('source','brand_preview','hospitality_preview','selected_paragraph_audio','selected_script','time_map','master_carrier'):
        verify_bound(lock[key])
    output = verify_bound({'path':data['output'],'sha256':data['output_sha256']})
    master = verify_bound(data['master'])
    report = args.report.resolve() if args.report else path.with_name(path.name.replace('-BUILD.json','-VERIFICATION.json'))
    report.relative_to(A/'r4')
    if report.exists():
        raise FileExistsError('Preserve the existing verification')
    info = probe(output); errors = []
    v = next(s for s in info['streams'] if s['codec_type']=='video')
    a = next(s for s in info['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames'])) != (1280,720,'24/1',29323):
        errors.append('Video format or complete frame count mismatch')
    if (a['sample_rate'],a['channels']) != ('48000',2):
        errors.append('Audio format mismatch')
    if abs(float(info['format']['duration'])-29323/FPS)>.002:
        errors.append('Container duration mismatch')
    video = video_check(output,29323)
    video.pop('planned_exception',None)
    video['planned_uniform_frames']=[1427]
    video['unplanned_uniform_frames']=[f for f in video['uniform_frames'] if f!=1427]
    if video['unplanned_uniform_frames'] or video['decode_exit_code'] or video['decoded_frames']!=29323:
        errors.append('Video decode error or unplanned uniform frame')
    audio = audio_check(output,master,[0,29323])
    if audio['compared_samples']!=audio['expected_samples'] or any(audio['decode_exit_codes']):
        errors.append('Audio decode or mapped sample count mismatch')
    if audio['min_voiced_window_corr']<.999 or audio['max_abs_voiced_window_rms_db']>.1:
        errors.append('Audio identity or unity-level mismatch')
    if not 0<=audio['aac_padding_samples']<=1024 or audio['padding_peak_abs']>1e-5:
        errors.append('Unexpected nonsilent audio beyond the unchanged program')
    replacement=data['presenter_replacements']
    if data['mode']=='full-review' and (replacement['pending'] or len(replacement['used'])!=16):
        errors.append('Full-review lacks a required presenter selection')
    result={'record_type':'ep009_r4_technical_verification','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status':'technical_checks_failed' if errors else 'technical_checks_passed_review_required',
            'owner_accepted':False,'owner_scoped_lock':data['owner_scoped_lock'],'build':bound(path),'output':bound(output),
            'probe':info,'video':video,'audio':audio,'loudness':loudness(output),'errors':errors,
            'presenter_replacements':replacement,
            'limitations':['No normal-speed audiovisual, mouth-sync, film-performance or final creative acceptance.',
                           'All explicit presenter flags and pending selections remain open. Scoped brand and experience locks remain effective.']}
    write(report,result)
    print(json.dumps({'status':result['status'],'errors':errors,'report':str(report)},indent=2))
    return bool(errors)


if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);raise SystemExit(2)
