"""Measure source preservation; does not establish perceptual lip-sync quality.

Run with Python + numpy + ffmpeg, e.g. the Higgsfield media sandbox.
Usage: compare_audio.py REFERENCE_WAV CANDIDATE_MEDIA
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

RATE = 16000
MAX_OFFSET = 1.0
WINDOWS = [('early', 0.25, 3.0), ('middle', 3.2, 5.3), ('last_sentence', 6.2, 7.1)]


def samples(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
        '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def correlation(a, b):
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def main():
    reference, candidate = map(Path, sys.argv[1:3])
    a, b = samples(reference), samples(candidate)
    size = 1 << (len(a) + len(b) - 2).bit_length()
    conv = np.fft.irfft(np.fft.rfft(b, size) * np.fft.rfft(a[::-1], size), size)
    radius = int(MAX_OFFSET * RATE)
    start = max(0, len(a) - 1 - radius)
    stop = min(len(a) + len(b) - 1, len(a) - 1 + radius + 1)
    lag = int(np.argmax(conv[start:stop]) + start - (len(a) - 1))
    a_start, b_start = max(0, -lag), max(0, lag)
    count = min(len(a) - a_start, len(b) - b_start)
    windows = {}
    for name, left, right in WINDOWS:
        al, ar = int(left * RATE), int(right * RATE)
        bl, br = al + lag, ar + lag
        windows[name] = correlation(a[al:ar], b[bl:br]) if ar <= len(a) and bl >= 0 and br <= len(b) else None
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_entries', 'format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels,pix_fmt',
        '-of', 'json', str(candidate)]))
    result = {
        'reference_path': str(reference), 'candidate_path': str(candidate),
        'reference_sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
        'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
        'reference_duration_seconds': len(a) / RATE,
        'candidate_audio_duration_seconds': len(b) / RATE,
        'audio_insertion_offset_seconds': lag / RATE,
        'offset_search_range_seconds': [-MAX_OFFSET, MAX_OFFSET],
        'offset_at_search_boundary': abs(lag) == radius,
        'aligned_overlap_seconds': max(0, count) / RATE,
        'aligned_audio_correlation': correlation(a[a_start:a_start+count], b[b_start:b_start+count]),
        'segment_correlations': windows,
        'final_half_second_rms': float(np.sqrt(np.mean(b[-RATE // 2:] ** 2))),
        'probe': probe,
        'interpretation': 'Similarity and audio placement only. A high stable correlation supports soundtrack preservation through encoding; a low correlation cannot establish preserved voice or timing. Offset is not measured audiovisual lip sync. No perceptual listening performed.'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
