#!/usr/bin/env python3
"""Verify an encoded look-transfer review; never confer owner acceptance."""
import argparse, copy, datetime, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[1]
A = T.parent / 'assembly'
sys.path.insert(0, str(A / '_tools'))
from build_r3 import bound, read, verify_bound, write, probe
from build_r4 import frame_map, nested_bindings
from verify_r3 import audio_check
from verify_r2 import video_check, loudness

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    args = parser.parse_args()
    path = args.build.resolve()
    path.relative_to(A / 'r5-look-transfer')
    data = read(path)
    if data['record_type'] != 'ep009_r5_look_transfer_review_build' or data['mode'] != 'full' or data['status'] != 'encoded_unverified_review_only':
        raise ValueError('Completed full look-transfer candidate required')
    report = path.with_name(path.name.replace('-BUILD.json', '-VERIFICATION.json'))
    if report.exists():
        raise FileExistsError('Preserve existing verification')
    for key in ('base_build', 'source_audit', 'selections', 'master', 'timemap', 'transcript', 'revision', 'owner_scoped_lock', 'film_selections', 'builder', 'graph_helper', 'graph'):
        verify_bound(data[key])
    nested_bindings(data['replacements'])
    nested_bindings(data['retained_P00'])
    output = verify_bound({'path': data['output'], 'sha256': data['output_sha256']})
    master = verify_bound(data['master'])
    base = read(verify_bound(data['base_build']))
    old, new = frame_map(base['all_75_rows']), frame_map(data['all_75_rows'])
    allowed = {i for e in data['replacements'] for i in range(*e['output_frames'])}
    changed = {i for i, pair in enumerate(zip(old, new)) if pair[0] != pair[1]}
    errors = []
    required = {'seg009', 'seg012', 'seg019', 'seg021', 'seg028', 'seg035', 'seg037',
                'seg044', 'seg055', 'seg059', 'seg071', 'seg072', 'seg073', 'seg074', 'seg075'}
    ids = [e['segment'] for e in data['replacements']]
    if len(ids) != len(required) or set(ids) != required:
        errors.append('Full review does not contain exactly all 15 presenter replacements')
    if data['total_frames'] != 29323 or data['output_master_frames'] != [0, 29323]:
        errors.append('Full review timeline declaration changed')
    if len(base['all_75_rows']) != 75 or len(data['all_75_rows']) != 75:
        errors.append('Expected exactly 75 retained cue rows')
    for before, after in zip(base['all_75_rows'], data['all_75_rows']):
        b, a = copy.deepcopy(before), copy.deepcopy(after)
        b.pop('spans'); a.pop('spans')
        if a['id'] == b['id'] == 'seg044':
            a['output_cues']['picture'] = b['output_cues']['picture']
        if a != b:
            errors.append('Protected row timing or cue metadata changed: ' + before['id'])
    if len(old) != 29323 or len(new) != 29323 or changed != allowed:
        errors.append('Picture mapping differs outside selected presenter ranges')
    if old[:86] != new[:86]:
        errors.append('Owner-locked P00 changed')
    for key in ('master', 'timemap', 'transcript', 'revision', 'owner_scoped_lock', 'film_selections'):
        if data[key] != base[key]:
            errors.append('Protected binding changed: ' + key)
    for row in data['all_75_rows']:
        for span in row['spans']:
            verify_bound(span['source'])
    info = probe(output)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v['width'], v['height'], v['r_frame_rate'], int(v['nb_read_frames'])) != (1280, 720, '24/1', 29323):
        errors.append('Video format/count mismatch')
    if (a['sample_rate'], a['channels']) != ('48000', 2):
        errors.append('Audio format mismatch')
    if abs(float(info['format']['duration']) - 29323 / 24) > .002:
        errors.append('Episode duration changed')
    video = video_check(output, 29323)
    video.pop('planned_exception', None)
    video['planned_uniform_frames'] = [1427]
    video['unplanned_uniform_frames'] = [f for f in video['uniform_frames'] if f != 1427]
    if video['unplanned_uniform_frames'] or video['decode_exit_code'] or video['decoded_frames'] != 29323:
        errors.append('Video decode or unplanned uniform frame')
    audio = audio_check(output, master, [0, 29323])
    if audio['compared_samples'] != audio['expected_samples'] or any(audio['decode_exit_codes']):
        errors.append('Audio decode/sample mismatch')
    if audio['min_voiced_window_corr'] < .999 or audio['max_abs_voiced_window_rms_db'] > .1:
        errors.append('Locked master identity/level mismatch')
    if not 0 <= audio['aac_padding_samples'] <= 1024 or audio['padding_peak_abs'] > 1e-5:
        errors.append('Unexpected audio tail')
    result = {
        'record_type': 'ep009_look_transfer_full_review_technical_verification',
        'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'technical_checks_failed' if errors else 'technical_checks_passed_private_review_candidate',
        'build': bound(path), 'output': bound(output), 'master': data['master'],
        'mapping': {'frames_compared': 29323, 'changed_picture_frames': len(changed),
                    'allowed_ranges': [e['output_frames'] for e in data['replacements']],
                    'P00_retained': old[:86] == new[:86], 'other_assignments_identical': changed == allowed},
        'probe': info, 'video': video, 'audio': audio, 'loudness': loudness(output),
        'errors': errors, 'owner_accepted': False, 'release_cleared': False,
        'limits': ['Full decode, source mapping and audio identity checks do not establish continuous human audiovisual review.',
                   'Performance judgments remain in the separately bound per-clip reviews; this report cannot clear their flags.']
    }
    write(report, result)
    print(json.dumps({'status': result['status'], 'errors': errors, 'report': str(report)}, indent=2))
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
