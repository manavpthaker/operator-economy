#!/usr/bin/env python3
"""Bounded-memory verification of an r3 review render, never creative acceptance."""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from build_r3 import R, A, SR, SPF, FPS, bound, read, verify_bound, write, probe
from verify_r2 import video_check, loudness


def audio_check(output, master, interval):
    start, end = interval
    expected = (end - start) * SPF
    command = ['ffmpeg', '-v', 'error', '-i', str(master), '-af',
               f'atrim=start_sample={start*SPF}:end_sample={end*SPF},apad=whole_len={expected},atrim=end_sample={expected}',
               '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    m = subprocess.Popen(command, stdout=subprocess.PIPE)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(output), '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], stdout=subprocess.PIPE)
    count = decoded = 0
    energy = 0.0; pe = np.zeros(2); cross = np.zeros(2); windows = []; tail = 0.0
    try:
        while True:
            raw = m.stdout.read(SR * 5 * 4)
            if not raw:
                break
            x = np.frombuffer(raw, dtype='<f4').astype(float)
            rawp = p.stdout.read(len(x) * 8)
            y = np.frombuffer(rawp, dtype='<f4').reshape(-1, 2).astype(float)
            if len(y) != len(x):
                raise ValueError('Program audio shorter than mapped master')
            xx = float(np.dot(x, x)); yy = (y*y).sum(0); xy = (y*x[:, None]).sum(0)
            if xx / len(x) > 1e-8:
                windows.append({'start_seconds': count / SR, 'samples': len(x),
                    'corr': (xy / np.sqrt(xx*yy)).tolist(), 'rms_delta_db': (10*np.log10(yy/xx)).tolist()})
            energy += xx; pe += yy; cross += xy; count += len(x); decoded += len(y)
        while True:
            rawp = p.stdout.read(SR * 5 * 8)
            if not rawp:
                break
            y = np.frombuffer(rawp, dtype='<f4').reshape(-1, 2)
            decoded += len(y); tail = max(tail, float(np.abs(y).max()))
        exits = [m.wait(), p.wait()]
    finally:
        for process in (m, p):
            process.stdout.close()
            if process.poll() is None:
                process.terminate(); process.wait()
    return {'method': 'Complete mapped master excerpt, including planned final zero padding; channelwise unity comparison in5secondblocks.',
            'expected_samples': expected, 'compared_samples': count, 'decoded_samples': decoded,
            'aac_padding_samples': decoded - expected, 'padding_peak_abs': tail, 'decode_exit_codes': exits,
            'full_corr': (cross / np.sqrt(energy * pe)).tolist(), 'full_rms_delta_db': (10*np.log10(pe/energy)).tolist(),
            'min_voiced_window_corr': min(min(w['corr']) for w in windows),
            'max_abs_voiced_window_rms_db': max(max(abs(v) for v in w['rms_delta_db']) for w in windows), 'windows': windows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--report', type=Path, help='New report path when preserving an earlier diagnostic')
    args = parser.parse_args()
    path = args.manifest.resolve(); path.relative_to(A)
    data = read(path)
    if data.get('record_type') != 'ep009_r3_review_build' or data.get('status') != 'encoded_unverified_review_only':
        raise ValueError('Expected a completed, unverified r3 build')
    verify_bound(data['revision'])
    if data.get('owner_scoped_lock'):
        lock = read(verify_bound(data['owner_scoped_lock']))
        for key in ('source', 'brand_preview', 'hospitality_preview', 'selected_paragraph_audio', 'selected_script', 'time_map', 'master_carrier'):
            verify_bound(lock[key])
    for b in data['sources']:
        verify_bound(b)
    if data.get('review_label'):
        verify_bound(data['review_label'])
    if data['film_selections']:
        verify_bound(data['film_selections'])
    master = verify_bound(data['master'])
    output = verify_bound({'path': data['output'], 'sha256': data['output_sha256']})
    report = args.report.resolve() if args.report else path.with_name(path.name.replace('-BUILD.json', '-VERIFICATION.json'))
    report.relative_to(A)
    if report.exists():
        raise FileExistsError('Preserve existing verification')
    info, errors = probe(output), []
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v['width'], v['height'], v['r_frame_rate'], int(v['nb_read_frames'])) != (1280, 720, '24/1', data['total_frames']):
        errors.append('Video format or decoded frame count mismatch')
    if (a['sample_rate'], a['channels']) != ('48000', 2):
        errors.append('Audio format mismatch')
    if abs(float(info['format']['duration']) - data['total_frames'] / FPS) > .002:
        errors.append('Container duration mismatch')
    video = video_check(output, data['total_frames'])
    start, end = data['output_master_frames']
    allowed = [1427-start] if start <= 1427 < end else []
    video['planned_uniform_frames'] = allowed
    video.pop('planned_exception', None)
    video['unplanned_uniform_frames'] = [f for f in video['uniform_frames'] if f not in allowed]
    if video['unplanned_uniform_frames'] or video['decode_exit_code'] or video['decoded_frames'] != data['total_frames']:
        errors.append('Video decode or unplanned blank frame')
    audio = audio_check(output, master, data['output_master_frames'])
    if audio['compared_samples'] != audio['expected_samples'] or any(audio['decode_exit_codes']):
        errors.append('Audio decode or mapped sample count mismatch')
    if audio['min_voiced_window_corr'] < .999 or audio['max_abs_voiced_window_rms_db'] > .1:
        errors.append('Audio mapping or unity level mismatch')
    if not 0 <= audio['aac_padding_samples'] <= 1024 or (data['scope'] == 'full' and audio['padding_peak_abs'] > 1e-5):
        errors.append('Unexpected audio beyond planned picture')
    audio['padding_policy'] = ('Full episode requires silent decoded padding.' if data['scope'] == 'full'
                               else 'At most one AAC frame of decoded encoder padding; an excerpt can end during source speech, so decoded padding may ring. Container duration remains exact.')
    result = {'record_type': 'ep009_r3_technical_verification', 'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'technical_checks_failed' if errors else 'technical_checks_passed_review_required',
              'owner_accepted': False, 'owner_scoped_lock': data.get('owner_scoped_lock'), 'build': bound(path), 'output': bound(output), 'probe': info,
              'video': video, 'audio': audio, 'loudness': loudness(output), 'errors': errors,
              'limitations': ['No normal-speed audiovisual watch-through, mouth-sync or final creative judgment.', 'Corrected P08 is an explicitly labeled still;14otherpresentersegments still use r1.']}
    write(report, result)
    print(json.dumps({'status': result['status'], 'errors': errors, 'report': str(report)}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        raise SystemExit(2)
