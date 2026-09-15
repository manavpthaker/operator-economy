#!/usr/bin/env python3
"""Read-only R23 media QA. Writes diagnostic artifacts only beside this script.

Run once after root reports the output ready. No network/provider operations.
Metrics verify media conformity; they cannot certify visual lip sync or acting.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw


REPO = pathlib.Path('/Users/brownmanbrain/GitHub/operator-economy')
PROVIDER = REPO / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r23-natural-performance/provider'
OWNED = pathlib.Path(__file__).resolve().parent
RAW = PROVIDER / 'presenter-generated-raw.mp4'
PROPOSAL = PROVIDER / 'PROPOSED-REQUEST.json'
SR = 48000


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run(args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(path)]).stdout)


def pcm(path):
    data = run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']).stdout
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def align(provider, reference, max_lag_samples=24000):
    # Positive lag means provider audio is later than the submitted reference.
    if min(len(provider), len(reference)) < 100:
        return {'status': 'too_short'}
    n = 1 << (len(provider) + len(reference) - 1).bit_length()
    correlation = np.fft.irfft(np.fft.rfft(provider, n) * np.conj(np.fft.rfft(reference, n)), n)
    lags = np.arange(-max_lag_samples, max_lag_samples + 1)
    lag = int(lags[np.argmax(correlation[lags % n])])
    if lag >= 0:
        a, b = provider[lag:], reference
    else:
        a, b = provider, reference[-lag:]
    length = min(len(a), len(b))
    a, b = a[:length], b[:length]
    if min(np.std(a), np.std(b)) < 1e-9:
        return {'status': 'insufficient_signal', 'lag_samples': lag}
    gain = float(np.dot(a, b) / np.dot(b, b))
    residual = a - gain * b
    return {
        'status': 'measured',
        'provider_minus_reference_samples': lag,
        'provider_minus_reference_ms': lag * 1000 / SR,
        'pearson_after_lag': float(np.corrcoef(a, b)[0, 1]),
        'linear_gain': gain,
        'residual_rms': float(np.sqrt(np.mean(residual ** 2))),
        'reference_rms': float(np.sqrt(np.mean(b ** 2))),
    }


def contact_sheet(path, duration):
    times = [0, .5, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 11.44, 12.11, 13, 14, 14.8, 15.0]
    times = [min(t, max(0, duration - .04)) for t in times]
    width, height, label = 384, 216, 25
    sheet = Image.new('RGB', (width * 5, (height + label) * 3), '#eeeae2')
    draw = ImageDraw.Draw(sheet)
    for i, t in enumerate(times):
        result = run(['ffmpeg', '-v', 'error', '-ss', f'{t:.6f}', '-i', str(path), '-frames:v', '1', '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2', '-f', 'image2pipe', '-vcodec', 'png', '-'])
        frame = Image.open(io.BytesIO(result.stdout)).convert('RGB')
        x, y = (i % 5) * width, (i // 5) * (height + label)
        sheet.paste(frame, (x, y))
        draw.text((x + 7, y + height + 5), f'Local {t:.2f}s / Review {56.5+t:.2f}s', fill='black')
    output = OWNED / 'r23-output-contact.jpg'
    sheet.save(output, quality=94)
    return {'path': str(output), 'sha256': sha(output), 'local_times_seconds': times}


def main():
    if not RAW.is_file():
        print(json.dumps({'status': 'output_missing_no_poll', 'expected_path': str(RAW)}))
        return 2
    proposal = json.loads(PROPOSAL.read_text())
    inputs = {
        'photo': PROVIDER / proposal['image_local_path'],
        'handled_audio': PROVIDER / proposal['audio_local_path'],
        'original_audio': PROVIDER / proposal['original_audio_local_path'],
    }
    expected = {
        'photo': proposal['image_sha256'],
        'handled_audio': proposal['audio_sha256'],
        'original_audio': proposal['original_audio_sha256'],
    }
    measured_hashes = {key: sha(path) for key, path in inputs.items()}
    for key in inputs:
        if measured_hashes[key] != expected[key]:
            raise ValueError(f'Input hash mismatch: {key}')
    original, handled = pcm(inputs['original_audio']), pcm(inputs['handled_audio'])
    source_preserved = len(original) == 720000 and np.array_equal(handled[:720000], original)
    tail = handled[720000:]
    tail_valid = len(tail) == 5760 and bool(np.all(tail == 0))
    if not source_preserved or not tail_valid:
        raise ValueError('Handled input does not preserve exact15s PCM plus0.12s zero tail')
    info = probe(RAW)
    video = next(x for x in info['streams'] if x['codec_type'] == 'video')
    audio_streams = [x for x in info['streams'] if x['codec_type'] == 'audio']
    numerator, denominator = video['avg_frame_rate'].split('/')
    fps = float(numerator) / float(denominator)
    duration = float(video.get('duration', info['format']['duration']))
    frame_count = int(video.get('nb_read_frames') or video.get('nb_frames'))
    decoded = run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(RAW), '-map', '0', '-f', 'null', '-'])
    metadata = {
        'duration_seconds': duration, 'fps': fps, 'decoded_frames': frame_count,
        'width': video['width'], 'height': video['height'],
        'video_start_time': video.get('start_time'),
        'audio_streams': [{'sample_rate': x.get('sample_rate'), 'duration': x.get('duration'), 'start_time': x.get('start_time')} for x in audio_streams],
        'minimum15s_picture': duration >= 15,
        'expected377frames25fps': frame_count == 377 and math.isclose(fps, 25),
        'decoder_integrity': True,
    }
    alignment = {'status': 'no_provider_audio'}
    if audio_streams:
        provider_audio = pcm(RAW)
        windows = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15), (10.5, 12.7)]
        results = []
        for start, end in windows:
            a, b = int(start * SR), int(end * SR)
            results.append({'range_seconds': [start, end], **align(provider_audio[a:b], original[a:b])})
        lags = [x['provider_minus_reference_ms'] for x in results if x.get('status') == 'measured']
        alignment = {
            'status': 'measured', 'decoded_samples': len(provider_audio),
            'full_first15s': align(provider_audio[:720000], original),
            'windows': results,
            'measured_window_lag_spread_ms': max(lags) - min(lags) if lags else None,
            'meaning': 'Waveform alignment and drift diagnostic only; not a mouth-synchronization verdict.',
        }
    report = {
        'status': 'technical_measurements_complete_visual_review_pending',
        'proposal_sha256': sha(PROPOSAL), 'raw_path': str(RAW), 'raw_sha256': sha(RAW),
        'input_hashes': measured_hashes, 'original_pcm_preserved': source_preserved,
        'generation_only_zero_tail_valid': tail_valid,
        'metadata': metadata, 'audio_alignment': alignment,
        'contact_sheet': contact_sheet(RAW, duration),
        'limits': [
            'No source, R23 runtime, canonical narration or approval state was changed.',
            'No paid call or network operation was made.',
            'Contact sheet may expose severe visual artifacts but cannot certify complete motion, speech articulation, identity stability or lip sync.',
            'Provider audio is diagnostic; selected review must use unchanged original narration.',
        ],
    }
    output = OWNED / 'r23-output-qa.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(output), 'sha256': sha(output), 'metadata': metadata, 'audio_alignment': alignment}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
