#!/usr/bin/env python3
"""Read a supplied presenter video; write bounded technical QA in this packet only."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
EXP = REPO / 'blueprint-cinema/experiments/EP007-PRESENTER-001'
OWNED = REPO / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-restored-look-r12'
RATE = 48000
INPUTS = {
    'locked_audio': (EXP / 'media/repair-r2/scope-two-sentences.wav', 'c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566'),
    'appearance_reference': (EXP / 'media/study-look-candidate-03.webp', '59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754'),
    'preferred_performance_reference': (EXP / 'media/repair-r6/test-f-original-footage-avatar-iii-1080p.mp4', 'd5c590fb00f9d5fda21af2d175048b94de64fb96413aa87ef215148d89727bcb'),
}
REVIEW_TIMES = [0.75, 1.05, 2.5, 3.2, 3.4, 3.6, 4.45, 5.2]


def run(*args):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')[-6000:])
    return result.stdout


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def audio(path):
    raw = run('ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
              '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-')
    return np.frombuffer(raw, dtype='<f4').astype(np.float64)


def pearson(x, y):
    if len(x) != len(y) or len(x) < 2:
        return None
    x = x - x.mean()
    y = y - y.mean()
    denominator = np.linalg.norm(x) * np.linalg.norm(y)
    return float(np.dot(x, y) / denominator) if denominator > 0 else None


def lag_for_window(reference, returned, start, end, search_seconds=0.25):
    """Positive lag means returned PCM contains the source later. Fixed-length NCC."""
    a, b = round(start * RATE), round(end * RATE)
    lo = max(-round(search_seconds * RATE), -a)
    hi = min(round(search_seconds * RATE), len(returned) - b)
    if hi < lo:
        raise ValueError('Returned audio is too short for the selected alignment window')
    x = reference[a:b]
    y = returned[a + lo:b + hi]
    centered = x - x.mean()
    n = len(x)
    fft_size = 1 << (len(y) + n - 2).bit_length()
    convolution = np.fft.irfft(np.fft.rfft(y, fft_size) *
                              np.fft.rfft(centered[::-1], fft_size), fft_size)
    numerator = convolution[n - 1:n - 1 + hi - lo + 1]
    sums = np.concatenate(([0.0], np.cumsum(y)))
    squares = np.concatenate(([0.0], np.cumsum(y * y)))
    sum_y = sums[n:] - sums[:-n]
    energy_y = np.maximum(0.0, squares[n:] - squares[:-n] - sum_y * sum_y / n)
    denominator = np.sqrt(energy_y * np.dot(centered, centered))
    scores = np.divide(numerator, denominator, out=np.full_like(numerator, -np.inf),
                       where=denominator > 1e-18)
    index = int(np.argmax(scores))
    lag = lo + index
    return {
        'source_window_seconds': [start, end], 'lag_samples': lag,
        'lag_ms': lag * 1000 / RATE,
        'aligned_pearson': pearson(x, returned[a + lag:b + lag]),
        'search_lag_samples': [lo, hi],
        'best_lag_at_search_boundary': lag in (lo, hi),
    }


def aligned_overlap(reference, returned, lag):
    source_start = max(0, -lag)
    source_end = min(len(reference), len(returned) - lag)
    if source_end <= source_start:
        raise ValueError('No source/returned overlap after alignment')
    return reference[source_start:source_end], returned[source_start + lag:source_end + lag], source_start, source_end


def levels(samples):
    if not len(samples):
        return {'samples': 0, 'rms_dbfs': None, 'peak_dbfs': None}
    rms = np.sqrt(np.mean(samples * samples))
    peak = np.max(np.abs(samples))
    return {'samples': len(samples),
            'rms_dbfs': float(20 * np.log10(max(rms, 1e-12))),
            'peak_dbfs': float(20 * np.log10(max(peak, 1e-12)))}


def window(samples, start, end):
    return samples[max(0, round(start * RATE)):min(len(samples), round(end * RATE))]


def contact_sheet(video, output, video_stream, video_start):
    frame_info = json.loads(run('ffprobe', '-v', 'error', '-select_streams', 'v:0',
                               '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time',
                               '-of', 'json', str(video)))['frames']
    if any('best_effort_timestamp_time' not in frame for frame in frame_info):
        raise ValueError('Missing video frame timestamp; cannot bind review frames')
    times = np.array([float(frame['best_effort_timestamp_time']) - video_start for frame in frame_info])
    chosen = [int(np.argmin(np.abs(times - t))) for t in REVIEW_TIMES]
    unique = sorted(set(chosen))
    expression = '+'.join('eq(n\\,%d)' % n for n in unique)
    raw = run('ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0',
              '-vf', 'select=' + expression + ',format=rgb24', '-an',
              '-fps_mode', 'passthrough', '-f', 'rawvideo', '-')
    width, height = video_stream['width'], video_stream['height']
    frames = np.frombuffer(raw, np.uint8).reshape(len(unique), height, width, 3)
    images = dict(zip(unique, frames))
    crop = (round(width * 0.25), round(height * 0.02),
            round(width * 0.75), round(height * 0.91))
    tile_width, tile_height, label_height = 360, 400, 40
    sheet = Image.new('RGB', (4 * tile_width, 2 * (tile_height + label_height)), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    records = []
    for i, (requested, n) in enumerate(zip(REVIEW_TIMES, chosen)):
        picture = Image.fromarray(images[n]).crop(crop)
        picture.thumbnail((tile_width, tile_height), Image.Resampling.LANCZOS)
        col, row = i % 4, i // 4
        left = col * tile_width + (tile_width - picture.width) // 2
        top = row * (tile_height + label_height) + label_height
        sheet.paste(picture, (left, top))
        draw.text((col * tile_width + 8, top - label_height + 6),
                  f'Asked {requested:.2f}s | frame {n} @ {times[n]:.3f}s', fill='white')
        records.append({'requested_video_local_seconds': requested, 'frame_index': n,
                        'actual_video_local_seconds': float(times[n]),
                        'selection_error_ms': float((times[n] - requested) * 1000),
                        'decoded_rgb_sha256': hashlib.sha256(images[n].tobytes()).hexdigest()})
    target = output / 'face-contact-sheet.jpg'
    sheet.save(target, quality=95)
    return {'path': str(target), 'sha256': sha(target), 'frames': records,
            'crop_ltrb_pixels': list(crop),
            'method': 'Fixed broad central head/upper-chest crop; RGB otherwise unchanged; scaled only for diagnostic display',
            'times_are': 'Requested local video times, not source-audio times shifted by measured lag'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--run-name', default='test-k')
    args = parser.parse_args()
    if Path(__file__).resolve().parent != OWNED.resolve():
        raise ValueError('This checker must run from its owned deliverable packet')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', args.run_name):
        raise ValueError('Invalid run name')
    video = args.video.expanduser().resolve(strict=True)
    provenance = {}
    for key, (path, expected) in INPUTS.items():
        digest = sha(path)
        if digest != expected:
            raise ValueError('Input hash mismatch: ' + str(path))
        provenance[key] = {'path': str(path), 'sha256': digest, 'expected_hash_verified': True}
    probe = json.loads(run('ffprobe', '-v', 'error', '-count_frames', '-show_streams',
                          '-show_format', '-of', 'json', str(video)))
    vs = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    aus = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
    decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(video), '-f', 'null', '-'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    reference, returned = audio(INPUTS['locked_audio'][0]), audio(video)
    if len(reference) != 268800:
        raise ValueError('Locked WAV must contain exactly 268800 samples at 48 kHz')
    overall = lag_for_window(reference, returned, 0.25, 5.35)
    sentences = [lag_for_window(reference, returned, a, b) for a, b in [(0.25, 2.85), (3.87, 5.35)]]
    lag = overall['lag_samples']
    x, y, a, b = aligned_overlap(reference, returned, lag)
    video_start, audio_start = float(vs.get('start_time', 0)), float(aus.get('start_time', 0))
    local_offset = audio_start - video_start + lag / RATE
    quiet = []
    for start, end in [(2.85, 3.05), (3.05, 3.25), (3.25, 3.45), (3.45, 3.65), (3.65, 3.85), (3.2, 3.6)]:
        quiet.append({'source_seconds': [start, end],
                      'video_local_seconds': [start + local_offset, end + local_offset],
                      'source': levels(window(reference, start, end)),
                      'returned': levels(window(returned, start + lag / RATE, end + lag / RATE))})
    voiced = levels(window(returned, 4.31 + lag / RATE, 4.61 + lag / RATE))
    last_start, last_end = round(4.95 * RATE), round(5.35 * RATE)
    last_has_audio = last_start + lag >= 0 and last_end + lag <= len(returned)
    video_duration = float(vs.get('duration', probe['format']['duration']))
    last_video_end = 5.35 + local_offset
    output = (OWNED / 'runs' / args.run_name).resolve()
    if not output.is_relative_to(OWNED.resolve()):
        raise ValueError('Output escapes owned packet')
    output.mkdir(parents=True, exist_ok=True)
    sheet = contact_sheet(video, output, vs, video_start)
    report = {
        'status': 'technical_measurements_complete_performance_review_pending',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'video': {'path': str(video), 'sha256': sha(video), 'bytes': video.stat().st_size},
        'verified_inputs': provenance,
        'tools': {'python': sys.executable, 'numpy': np.__version__,
                  'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe'),
                  'ffmpeg_version': run('ffmpeg', '-version').decode().splitlines()[0]},
        'probe': probe,
        'picture': {'width': vs['width'], 'height': vs['height'],
                    'fps': float(Fraction(vs['avg_frame_rate'])),
                    'decoded_frames': int(vs['nb_read_frames']), 'duration_seconds': video_duration},
        'full_decode': {'passed': decode.returncode == 0, 'exit_code': decode.returncode,
                        'stderr': decode.stderr.decode(errors='replace')},
        'audio': {'decode_format': 'mono float PCM 48000 Hz', 'source_samples': len(reference),
                  'returned_samples': len(returned), 'returned_decoded_duration_seconds': len(returned) / RATE,
                  'lag_method': 'NumPy FFT fixed-window normalized correlation; independent integer-sample maximum within +/-250ms',
                  'lag_estimation': overall, 'sentence_estimates': sentences,
                  'sentence_lag_difference_samples': sentences[1]['lag_samples'] - sentences[0]['lag_samples'],
                  'sentence_lag_difference_ms': (sentences[1]['lag_samples'] - sentences[0]['lag_samples']) * 1000 / RATE,
                  'whole_available_overlap_source_samples': [a, b],
                  'whole_available_overlap_pearson': pearson(x, y),
                  'source_to_video_local_offset_seconds': local_offset,
                  'quiet_source_gap_seconds': [2.85, 3.87], 'quiet_windows': quiet,
                  'raw_video_3p2_to_3p6_levels': levels(window(returned, 3.2 + video_start - audio_start, 3.6 + video_start - audio_start)),
                  'adjacent_never_word_levels': voiced,
                  'dbfs_floor': -240.0,
                  'last_word': {'text': 'business', 'source_seconds': [4.95, 5.35],
                                'aligned_audio_coverage_complete': last_has_audio,
                                'aligned_pearson': pearson(reference[last_start:last_end], returned[last_start + lag:last_end + lag]) if last_has_audio else None,
                                'expected_end_video_local_seconds': last_video_end,
                                'picture_covers_expected_end': video_duration >= last_video_end,
                                'picture_margin_seconds': video_duration - last_video_end}},
        'contact_sheet': sheet,
        'limits': [
            'Audio correspondence is not a perceptual lip-sync or acting verdict.',
            'Sentence lag difference tests only this short excerpt; it does not establish long-form drift behavior.',
            'Quiet windows are transcript-derived and measured acoustically; RMS is not a speech classifier.',
            'Last-word coverage uses transcript timing plus measured audio lag; it does not prove visible articulation completes.',
            'Contact sheet samples cannot reveal all intervening motion or temporal artifacts.',
            'Different face framing makes raw mouth-pixel size misleading; compare relative opening and moving delivery with F.',
            'Appearance comparison belongs against unchanged candidate 03; preferred mouth performance belongs against F.',
            'No production approval or gate changes are made.'
        ],
        'canonical_gates_changed': [],
    }
    target = output / 'technical-review.json'
    target.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'report': str(target), 'sha256': sha(target), 'contact_sheet': sheet['path'],
                      'lag_ms': overall['lag_ms'], 'overlap_correlation': pearson(x, y),
                      'full_decode_pass': decode.returncode == 0}, indent=2))
    return 0 if decode.returncode == 0 else 2


if __name__ == '__main__':
    raise SystemExit(main())
