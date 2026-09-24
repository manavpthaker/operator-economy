#!/usr/bin/env python3
"""Verify an r2 candidate from its build manifest without promoting acceptance.

Run with the retained syncenv Python (numpy). Checks use bounded-memory streaming,
including decoding every video frame and comparing the complete program audio.
Writes a new report beside the manifest; never overwrites r1 or an earlier report.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from build_r2 import A, ROOT, MASTER, MASTER_SHA, FPS, SR, read, sha, probe, rel, write_new


def audio_check(output):
    def decoder(path, channels):
        return subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                                 '-ac', str(channels), '-ar', str(SR), '-f', 'f32le', '-'], stdout=subprocess.PIPE)
    master, program = decoder(MASTER, 1), decoder(output, 2)
    count = program_count = 0
    sum_m2 = 0.0
    sum_p2, cross = np.zeros(2), np.zeros(2)
    windows = []
    lr_max = tail_max = 0.0
    shortfall = False
    uncompared_in_block = 0
    block = SR * 10
    try:
        while True:
            raw = master.stdout.read(block * 4)
            if not raw:
                break
            m = np.frombuffer(raw, dtype='<f4').astype(np.float64)
            rawp = program.stdout.read(len(m) * 8)
            p = np.frombuffer(rawp, dtype='<f4').reshape(-1, 2).astype(np.float64)
            program_count += len(p)
            if len(p) != len(m):
                shortfall = True
                uncompared_in_block = len(m) - len(p)
                m = m[:len(p)]
            if not len(m):
                break
            mm, pp = float(np.dot(m, m)), np.sum(p * p, axis=0)
            mp = np.sum(p * m[:, None], axis=0)
            sum_m2 += mm
            sum_p2 += pp
            cross += mp
            lr_max = max(lr_max, float(np.max(np.abs(p[:, 0] - p[:, 1]))))
            if mm / len(m) > 1e-8:
                corr = mp / np.sqrt(np.maximum(mm * pp, 1e-30))
                db = 10 * np.log10(np.maximum(pp / mm, 1e-30))
                windows.append({'start_seconds': count / SR, 'samples': len(m),
                                'zero_lag_normalized_corr': corr.tolist(), 'rms_minus_master_db': db.tolist()})
            count += len(m)
            if shortfall:
                break
        while True:
            rawp = program.stdout.read(block * 8)
            if not rawp:
                break
            p = np.frombuffer(rawp, dtype='<f4').reshape(-1, 2)
            program_count += len(p)
            tail_max = max(tail_max, float(np.max(np.abs(p))))
        # Drain the master if the program was short, so no subprocess blocks.
        remainder = 0
        while True:
            raw = master.stdout.read(block * 4)
            if not raw:
                break
            remainder += len(raw) // 4
        exits = [master.wait(), program.wait()]
    finally:
        for process in (master, program):
            process.stdout.close()
            if process.poll() is None:
                process.terminate()
                process.wait()
    full_corr = cross / np.sqrt(np.maximum(sum_m2 * sum_p2, 1e-30))
    full_db = 10 * np.log10(np.maximum(sum_p2 / max(sum_m2, 1e-30), 1e-30))
    return {
        'method': 'Full decoded audio in consecutive 10 s blocks, zero-lag normalized waveform correlation (no mean subtraction); per-channel RMS against mono master.',
        'compared_master_samples': count, 'uncompared_master_samples': remainder + uncompared_in_block,
        'program_decoded_samples': program_count, 'program_shortfall': shortfall, 'decode_exit_codes': exits,
        'full_corr': full_corr.tolist(), 'full_rms_minus_master_db': full_db.tolist(),
        'min_non_silent_window_corr': min(min(w['zero_lag_normalized_corr']) for w in windows) if windows else 0,
        'max_abs_non_silent_window_rms_db': max(max(abs(x) for x in w['rms_minus_master_db']) for w in windows) if windows else None,
        'left_minus_right_max_abs': lr_max,
        'decoded_samples_after_master': program_count - count, 'tail_max_abs': tail_max,
        'windows': windows,
        'limitation': 'Correct master audio placement does not establish lip sync of the image.'}


def video_check(output, expected):
    process = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(output), '-an',
                                '-vf', 'signalstats,metadata=print:file=-', '-f', 'null', '-'],
                               stdout=subprocess.PIPE, text=True)
    frames, uniform, frame, values = 0, [], None, {}

    def finish():
        if frame is not None and all(f'{c}{edge}' in values for c in 'YUV' for edge in ('MIN', 'MAX')):
            if all(values[f'{c}MAX'] - values[f'{c}MIN'] <= 4 for c in 'YUV'):
                uniform.append(frame)

    for line in process.stdout:
        if line.startswith('frame:'):
            finish()
            frame = int(re.match(r'frame:(\d+)', line).group(1))
            frames += 1
            values = {}
        elif line.startswith('lavfi.signalstats.'):
            k, value = line.strip().split('=', 1)
            values[k.rsplit('.', 1)[-1]] = float(value)
    finish()
    process.stdout.close()
    code = process.wait()
    # Locked accepted sting has one uniform navy entry frame. This exception is
    # frame-specific, so any new blank elsewhere is still a technical failure.
    unplanned = [f for f in uniform if f != 1427]
    return {'method': 'Decode every encoded frame; uniform means full-frame Y, U, V spans each at most 4 code values.',
            'decoded_frames': frames, 'expected_frames': expected, 'decode_exit_code': code,
            'uniform_frames': uniform, 'unplanned_uniform_frames': unplanned,
            'planned_exception': {'frame': 1427, 'segment': 'seg010', 'basis': 'Existing locked one-frame navy sting entry'},
            'limitation': 'Blank-frame detection does not judge composition, legibility, motion, seams, or performance.'}


def loudness(output):
    p = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', str(output), '-vn',
                        '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True, check=True)
    summary = p.stderr[p.stderr.rfind('Summary:'):]
    def value(pattern):
        found = re.search(pattern, summary)
        return float(found.group(1)) if found else None
    return {'integrated_lufs': value(r'I:\s+(-?[\d.]+) LUFS'),
            'loudness_range_lu': value(r'LRA:\s+(-?[\d.]+) LU'),
            'true_peak_dbtp': value(r'Peak:\s+(-?[\d.]+) dBFS'),
            'note': 'Measured only; no normalization or final mix acceptance.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest', type=Path)
    ap.add_argument('--report', type=Path, help='New report path under assembly; default derives from manifest.')
    args = ap.parse_args()
    manifest = args.manifest.resolve()
    manifest.relative_to(A)
    data = read(manifest)
    if data.get('record_type') != 'ep009_r2_assembly_build' or data.get('errors'):
        raise ValueError('Expected an unblocked r2 assembly build manifest.')
    if data['mode'] == 'full-review' and (data['presenter_replacements']['pending'] or len(data['presenter_replacements']['used']) != 15):
        raise ValueError('Full-review manifest has missing presenter replacements.')
    output = ROOT / data['output']
    output.resolve().relative_to(A / 'qa')
    if sha(output) != data.get('output_sha256'):
        raise ValueError('Encoded candidate differs from its build hash.')
    report = args.report.resolve() if args.report else manifest.with_name(manifest.name.replace('BUILD-', 'VERIFICATION-', 1))
    report.relative_to(A)
    if report.exists():
        raise FileExistsError(f'Refusing to overwrite report: {report}')
    errors = []
    for r in data['sources']:
        if sha(ROOT / r['path']) != r['sha256']:
            errors.append(f"Source changed after render: {r['id']}")
    if sha(MASTER) != MASTER_SHA:
        errors.append('Locked master hash differs.')
    pr = probe(output)
    v = next(s for s in pr['streams'] if s['codec_type'] == 'video')
    a = next(s for s in pr['streams'] if s['codec_type'] == 'audio')
    if (v.get('width'), v.get('height'), v.get('r_frame_rate')) != (1280, 720, '24/1'):
        errors.append('Incorrect picture dimensions or frame rate.')
    if (a.get('sample_rate'), a.get('channels')) != ('48000', 2):
        errors.append('Incorrect audio rate or channel count.')
    if abs(float(pr['format']['duration']) - data['total_frames'] / FPS) > 0.002:
        errors.append('Container duration does not match planned picture duration.')
    video = video_check(output, data['total_frames'])
    if video['decoded_frames'] != data['total_frames'] or video['decode_exit_code'] or video['unplanned_uniform_frames']:
        errors.append('Video decode, frame count, or unplanned-uniform-frame check failed.')
    audio = audio_check(output)
    if audio['program_shortfall'] or any(audio['decode_exit_codes']) or audio['min_non_silent_window_corr'] < 0.999:
        errors.append('Audio decode, length, or zero-lag waveform check failed.')
    if audio['max_abs_non_silent_window_rms_db'] is None or audio['max_abs_non_silent_window_rms_db'] > 0.1:
        errors.append('Program audio differs from unity master level by more than 0.1 dB in a voiced window.')
    if audio['tail_max_abs'] > 1e-5:
        errors.append('Program audio has non-silent samples after the master.')
    decoded_excess = audio['program_decoded_samples'] - data['total_frames'] * (SR // FPS)
    if not 0 <= decoded_excess <= 1024:
        errors.append('Decoded audio padding differs by more than one AAC frame from planned picture sample count.')
    result = {
        'record_type': 'ep009_r2_technical_verification', 'mode': data['mode'],
        'status': 'technical_checks_failed' if errors else 'technical_checks_passed_review_required',
        'owner_accepted': False, 'delivery_master': False,
        'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'build_manifest': {'path': rel(manifest), 'sha256': sha(manifest)},
        'output': {'path': rel(output), 'sha256': sha(output), 'probe': pr},
        'video': video, 'audio': audio, 'loudness': loudness(output),
        'pending_presenter_replacements': data['presenter_replacements']['pending'],
        'flagged_presenter_parts': data['presenter_replacements']['flagged'],
        'errors': errors, 'warnings': data['warnings'],
        'limitations': data['limitations'] + ['No audiovisual watch-through or mouth-sync judgment was performed by this verifier.'],
    }
    write_new(report, result)
    print(json.dumps({'status': result['status'], 'mode': data['mode'], 'errors': errors, 'report': str(report)}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2)
