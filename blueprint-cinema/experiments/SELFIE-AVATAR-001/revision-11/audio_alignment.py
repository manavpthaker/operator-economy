"""Soundtrack placement and preservation only; no visual lip-sync verdict.

Usage in Higgsfield sandbox:
  python3 audio_alignment.py REFERENCE_WAV CANDIDATE_MEDIA
Adapted from revision-09/audio_qa.py; no revision-specific durations or word times.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

RATE = 16000
MAX_OFFSET = 1.0


def samples(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
        '-map', '0:a:0', '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_entries', 'format=start_time,duration:stream=index,codec_name,codec_type,start_time,duration,width,height,r_frame_rate,nb_frames,sample_rate,channels,pix_fmt',
        '-of', 'json', str(path)]))


def correlation(a, b):
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def fft_match(x, y):
    size = 1 << (len(x) + len(y) - 2).bit_length()
    return np.fft.irfft(np.fft.rfft(y, size) * np.fft.rfft(x[::-1], size), size)


def local_offset(a, b, al, ar, global_lag):
    margin = int(.25 * RATE)
    bl, br = max(0, al + global_lag - margin), min(len(b), ar + global_lag + margin)
    x, y = a[al:ar], b[bl:br]
    if len(y) < len(x):
        return None
    conv = fft_match(x, y)
    index = int(np.argmax(conv[len(x) - 1:len(y)]))
    offset = bl + index - al
    return {'offset_seconds': offset / RATE,
        'correlation': correlation(x, y[index:index + len(x)]),
        'local_search_boundary_hit': index in (0, len(y) - len(x)),
        'window_seconds': [al / RATE, ar / RATE]}


def select_windows(a):
    # One high-energy window within each of six equal-duration reference bins.
    energy = np.concatenate(([0.0], np.cumsum(a * a)))
    threshold = max(1e-5, float(np.sqrt(np.mean(a * a))) * .05)
    windows = []
    edges = np.linspace(0, len(a), 7).astype(int)
    for index, (left, right) in enumerate(zip(edges[:-1], edges[1:]), 1):
        width = min(int(2.5 * RATE), right - left)
        starts = np.arange(left, right - width + 1, max(1, int(.05 * RATE)))
        if not width or not len(starts):
            windows.append({'index': index, 'status': 'empty_bin'}); continue
        energies = (energy[starts + width] - energy[starts]) / width
        best = int(np.argmax(energies)); start = int(starts[best])
        rms = float(np.sqrt(max(0, energies[best])))
        windows.append({'index': index, 'status': 'measured' if rms >= threshold else 'silent_bin',
            'source_samples': [start, start + width], 'reference_rms': rms})
    return windows, threshold


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: audio_alignment.py REFERENCE_WAV CANDIDATE_MEDIA')
    reference, candidate = map(Path, sys.argv[1:])
    a, b = samples(reference), samples(candidate)
    if len(a) < 2 or len(b) < 2:
        raise ValueError('Both inputs require nonempty audio')
    reference_probe, candidate_probe = probe(reference), probe(candidate)
    conv = fft_match(a, b)
    radius = int(MAX_OFFSET * RATE)
    start = max(0, len(a) - 1 - radius)
    stop = min(len(a) + len(b) - 1, len(a) - 1 + radius + 1)
    lag = int(np.argmax(conv[start:stop]) + start - (len(a) - 1))
    a_start, b_start = max(0, -lag), max(0, lag)
    count = max(0, min(len(a) - a_start, len(b) - b_start))
    windows, threshold = select_windows(a)
    for window in windows:
        if window['status'] != 'measured':
            continue
        al, ar = window['source_samples']
        bl, br = al + lag, ar + lag
        window['correlation_at_global_offset'] = correlation(a[al:ar], b[bl:br]) if bl >= 0 and br <= len(b) else None
        window['local'] = local_offset(a, b, al, ar, lag)
    local_results = [w['local'] for w in windows if w.get('local')]
    offsets = [w['offset_seconds'] for w in local_results]
    correlations = [w['correlation'] for w in local_results if w['correlation'] is not None]
    global_correlations = [w['correlation_at_global_offset'] for w in windows if w.get('correlation_at_global_offset') is not None]
    audio_stream = next(s for s in candidate_probe['streams'] if s['codec_type'] == 'audio')
    video_stream = next((s for s in candidate_probe['streams'] if s['codec_type'] == 'video'), None)
    audio_start = float(audio_stream.get('start_time', 0))
    video_start = float(video_stream.get('start_time', 0)) if video_stream else 0.0
    picture_offset = lag / RATE + audio_start - video_start
    result = {
        'reference_path': str(reference), 'candidate_path': str(candidate),
        'source_voice_sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
        'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
        'analysis_sample_rate_hz': RATE, 'offset_resolution_seconds': 1 / RATE,
        'reference_decoded_samples': len(a), 'candidate_decoded_samples': len(b),
        'reference_duration_seconds': len(a) / RATE, 'candidate_audio_duration_seconds': len(b) / RATE,
        'audio_insertion_offset_seconds': lag / RATE,
        'source_to_picture_offset_seconds': picture_offset,
        'candidate_audio_start_seconds': audio_start, 'candidate_video_start_seconds': video_start,
        'offset_search_range_seconds': [-MAX_OFFSET, MAX_OFFSET],
        'offset_at_search_boundary': abs(lag) == radius,
        'aligned_overlap_seconds': count / RATE,
        'aligned_reference_range_seconds': [a_start / RATE, (a_start + count) / RATE],
        'aligned_candidate_range_seconds': [b_start / RATE, (b_start + count) / RATE],
        'aligned_audio_correlation': correlation(a[a_start:a_start + count], b[b_start:b_start + count]),
        'zero_offset_correlation': correlation(a[:min(len(a), len(b))], b[:min(len(a), len(b))]),
        'window_selection': 'Highest-RMS window of up to 2.5 seconds in each of six equal-duration source bins; 50 ms selection grid.',
        'window_nonsilence_rms_threshold': threshold,
        'windows': windows, 'measured_window_count': len(local_results),
        'minimum_window_correlation': min(correlations) if correlations else None,
        'minimum_window_correlation_at_global_offset': min(global_correlations) if global_correlations else None,
        'window_offset_spread_seconds': max(offsets) - min(offsets) if offsets else None,
        'maximum_local_offset_difference_seconds': max(abs(x - lag / RATE) for x in offsets) if offsets else None,
        'source_end_in_decoded_output_seconds': (len(a) + lag) / RATE,
        'source_end_in_picture_seconds': len(a) / RATE + picture_offset,
        'full_source_sample_extent_covered': a_start == 0 and count == len(a),
        'missing_source_head_seconds': a_start / RATE,
        'missing_source_tail_seconds': max(0, len(a) - a_start - count) / RATE,
        'candidate_trailing_audio_after_source_seconds': max(0, len(b) - len(a) - lag) / RATE,
        'reference_probe': reference_probe, 'candidate_probe': candidate_probe,
        'lag_sign': 'Positive means candidate audio occurs later. For captions relative to video frame zero, use source_to_picture_offset_seconds only when strong full and local correlations support a stable clock.',
        'interpretation': 'Waveform similarity and placement only. Strong full and six-window correlations, stable offsets and full sample coverage support soundtrack preservation through encoding. Low correlations cannot establish source identity or a reliable offset. Full coverage alone does not establish preserved content. No visual lip-sync or perceptual listening claim.'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
