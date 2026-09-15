#!/usr/bin/env python3
"""Read-only R25 media audit; diagnostic writes stay beside this script.

Run only after root supplies a completed output path and SHA-256.
No network, provider, runtime, approval, or canonical mutations.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
OWNED = Path(__file__).resolve().parent
INPUTS = OWNED.parent / 'r24-subtle-articulation-audit/inputs'
PINS = {
    'original': ('performance-b-original.mp4', 'dae03d667c44b7faf29d3d8b13317a3939ef6997885b05c0efb5dbc66eb58cf4'),
    'audio': ('pickup-b-original.wav', 'e37976fde23e50265e7e6dde1a034d873d8b39f87d89f074d4da19ae7ac49072'),
    'r22': ('r22-post-title-b.mp4', '6bebb793f25e39b4c5577559f7e25b91a39270f904755bc6872586579935147a'),
}
SR = 48000
SAMPLES = 412000
DURATION = SAMPLES / SR
TIMES = [0.5, 2.5, 4.666667, 5.083333, 5.458333, 8.5]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run(args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(path)]).stdout)


def pcm(path):
    data = run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']).stdout
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def align(provider, reference, max_lag=12000):
    # Positive lag means output audio is later than the reference. No correction is applied.
    if min(len(provider), len(reference)) < 100:
        return {'status': 'too_short'}
    n = 1 << (len(provider) + len(reference) - 1).bit_length()
    cross = np.fft.irfft(np.fft.rfft(provider, n) * np.conj(np.fft.rfft(reference, n)), n)
    lags = np.arange(-max_lag, max_lag + 1)
    lag = int(lags[np.argmax(cross[lags % n])])
    a, b = (provider[lag:], reference) if lag >= 0 else (provider, reference[-lag:])
    length = min(len(a), len(b))
    a, b = a[:length], b[:length]
    if min(np.std(a), np.std(b)) < 1e-9:
        return {'status': 'insufficient_signal', 'lag_samples': lag}
    gain = float(np.dot(a, b) / np.dot(b, b))
    return {'status': 'measured', 'output_minus_reference_samples': lag,
            'output_minus_reference_ms': lag * 1000 / SR,
            'pearson_after_lag': float(np.corrcoef(a, b)[0, 1]),
            'linear_gain': gain, 'comparison_samples': length,
            'residual_rms': float(np.sqrt(np.mean((a - gain * b) ** 2)))}


def frame_hashes(path):
    lines = run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-an', '-f', 'framemd5', '-']).stdout.decode().splitlines()
    hashes = [line.split(',')[-1].strip() for line in lines if line and not line.startswith('#')]
    repeats = [i for i in range(1, len(hashes)) if hashes[i] == hashes[i - 1]]
    return {'decoded_frames': len(hashes), 'unique_decoded_frames': len(set(hashes)),
            'exact_adjacent_repeated_frame_indices': repeats,
            'exact_duplicate_frames_total': len(hashes) - len(set(hashes)),
            'limit': 'Distinct frames do not prove natural motion or exclude semantically repeated gestures.'}


def frame_at(path, time, duration):
    time = min(time, max(0, duration - 1 / 24))
    data = run(['ffmpeg', '-v', 'error', '-ss', f'{time:.9f}', '-i', str(path), '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-']).stdout
    return Image.open(io.BytesIO(data)).convert('RGB'), time


def make_sheets(paths, durations):
    names = ['original', 'r22', 'output']
    width, height, label = 384, 216, 30
    full = Image.new('RGB', (width * 3, (height + label) * len(TIMES)), '#eeeae2')
    face = Image.new('RGB', (width * 3, (height + label) * len(TIMES)), '#eeeae2')
    full_draw, face_draw = ImageDraw.Draw(full), ImageDraw.Draw(face)
    continuity = []
    for row, time in enumerate(TIMES):
        sampled = {}
        for col, name in enumerate(names):
            image, actual_time = frame_at(paths[name], time, durations[name])
            sampled[name] = np.asarray(image.resize((384, 216))).astype(np.float32)
            fit = image.copy()
            fit.thumbnail((width, height))
            x, y = col * width, row * (height + label)
            full.paste(fit, (x + (width - fit.width) // 2, y + (height - fit.height) // 2))
            w, h = image.size
            # Fixed central face-context crop, not a detected face or a semantic mask.
            crop = image.crop((int(w * .34), int(h * .08), int(w * .66), int(h * .65)))
            crop.thumbnail((width, height))
            face.paste(crop, (x + (width - crop.width) // 2, y + (height - crop.height) // 2))
            text = f'{name} | B {actual_time:.3f}s'
            full_draw.text((x + 6, y + height + 7), text, fill='black')
            face_draw.text((x + 6, y + height + 7), text, fill='black')
        for reference in ['original', 'r22']:
            output, ref = sampled['output'], sampled[reference]
            # Broad torso/background patch only. Compression differences remain included.
            torso_output, torso_ref = output[145:216], ref[145:216]
            continuity.append({'time_seconds': time, 'reference': reference,
                               'full_frame_mae_8bit': float(np.mean(np.abs(output - ref))),
                               'lower_frame_patch_mae_8bit': float(np.mean(np.abs(torso_output - torso_ref))),
                               'lower_frame_patch_pearson': float(np.corrcoef(torso_output.ravel(), torso_ref.ravel())[0, 1])})
    artifacts = []
    for name, image in [('full-comparison.jpg', full), ('face-comparison.jpg', face)]:
        path = OWNED / name
        image.save(path, quality=95)
        artifacts.append({'path': str(path.relative_to(REPO)), 'sha256': sha(path)})
    return {'artifacts': artifacts, 'sample_times_seconds': TIMES,
            'comparison_metrics': continuity,
            'limit': 'Fixed normalized crops and point samples only; no landmark tracking, exact pixel-preservation claim, or full-motion approval.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    raw = args.output.resolve()
    if not raw.is_file():
        print(json.dumps({'status': 'output_missing_no_poll', 'path': str(raw)}))
        return 2
    if sha(raw) != args.sha256:
        raise ValueError('Provided output SHA-256 does not match; stop')
    paths = {name: INPUTS / pin[0] for name, pin in PINS.items()}
    for name, path in paths.items():
        if sha(path) != PINS[name][1]:
            raise ValueError(f'Input hash mismatch: {name}')
    with wave.open(str(paths['audio'])) as f:
        assert (f.getframerate(), f.getnchannels(), f.getsampwidth(), f.getnframes()) == (SR, 1, 2, SAMPLES)
    paths['output'] = raw
    info = probe(raw)
    video = next(x for x in info['streams'] if x['codec_type'] == 'video')
    rate = video['avg_frame_rate'].split('/')
    fps = int(rate[0]) / int(rate[1])
    duration = float(video.get('duration', info['format']['duration']))
    frame_count = int(video.get('nb_read_frames') or video['nb_frames'])
    decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(raw), '-map', '0', '-f', 'null', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    metadata = {'width': video['width'], 'height': video['height'], 'fps': fps,
                'frame_count': frame_count, 'duration_seconds': duration,
                'duration_delta_from_input_ms': (duration - DURATION) * 1000,
                'video_start_time': video.get('start_time'),
                'expected_206_frames_24fps': frame_count == 206 and abs(fps - 24) < 1e-9,
                'exact_input_duration_within_1ms': abs(duration - DURATION) < .001,
                'full_decode_exit_code': decode.returncode,
                'full_decode_stderr': decode.stderr.decode(errors='replace')}
    frame_info = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(raw)]).stdout)
    pts = [float(x['best_effort_timestamp_time']) for x in frame_info['frames'] if 'best_effort_timestamp_time' in x]
    metadata['pts_first_last'] = [pts[0], pts[-1]] if pts else []
    metadata['pts_strictly_increasing'] = all(b > a for a, b in zip(pts, pts[1:]))
    metadata['pts_delta_min_max'] = [min(np.diff(pts)), max(np.diff(pts))] if len(pts) > 1 else []
    audio_streams = [x for x in info['streams'] if x['codec_type'] == 'audio']
    alignment = {'status': 'no_output_audio; original source remains authoritative'}
    if audio_streams:
        output_audio, reference = pcm(raw), pcm(paths['audio'])
        results = []
        for start, end in [(0, 2.5), (2.5, 5), (4.75, 6), (6, DURATION)]:
            a, b = round(start * SR), round(end * SR)
            results.append({'range_seconds': [start, end], **align(output_audio[a:b], reference[a:b])})
        lags = [r['output_minus_reference_ms'] for r in results if r.get('status') == 'measured']
        alignment = {'status': 'measured', 'decoded_output_samples': len(output_audio),
                     'exact_first_412000_decoded_samples': bool(len(output_audio) >= SAMPLES and np.array_equal(output_audio[:SAMPLES], reference)),
                     'audio_stream_start_time': audio_streams[0].get('start_time'),
                     'full': align(output_audio[:SAMPLES], reference), 'windows': results,
                     'window_lag_spread_ms': max(lags) - min(lags) if lags else None,
                     'limit': 'Codec changes can prevent sample equality. Audio correlation does not establish mouth sync, articulation quality, or permission to replace original narration.'}
    results = {'status': 'technical_measurements_complete_visual_review_pending',
               'input_hashes': [{'path': str(p.relative_to(REPO)), 'sha256': sha(p)} for p in paths.values()],
               'output_expected_sha256': args.sha256, 'metadata': metadata,
               'audio_alignment': alignment,
               'frame_uniqueness': {name: frame_hashes(paths[name]) for name in ['original', 'r22', 'output']},
               'sampled_comparison': make_sheets(paths, {'original': DURATION, 'r22': DURATION, 'output': duration}),
               'limits': ['No source media, runtime, narration, or approval state was changed.',
                          'No upload, paid call, retime, synthetic frame generation, or replacement audio was produced.',
                          'Full-motion owner acceptance remains outside this audit.']}
    path = OWNED / 'metrics.json'
    path.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'metrics': str(path), 'metadata': metadata, 'audio_alignment': alignment,
                      'frame_uniqueness': results['frame_uniqueness']}, indent=2))
    return 0 if decode.returncode == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
