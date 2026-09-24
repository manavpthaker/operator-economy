"""Measure source preservation; does not establish perceptual lip-sync quality.

Run with Python + numpy + ffmpeg, e.g. the Higgsfield media sandbox.
Usage: compare_audio.py REFERENCE_WAV CANDIDATE_MEDIA [SECTION_INDEX]
Omit SECTION_INDEX for the final continuous full R4 waveform comparison.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

RATE = 16000
MAX_OFFSET = 1.0
GLOBAL_WINDOWS = [('opening', 0.2, 10.5), ('section_2', 20.3, 35.4), ('section_3', 36.3, 47.2), ('final_question', 47.9, 52.5)]
SECTION_CONTENT_ENDS = {1: 968000 / 48000, 2: 756000 / 48000, 3: 812734 / 48000}


def samples(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
        '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def correlation(a, b):
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def local_offset(a, b, left, right, global_lag):
    al, ar = int(left * RATE), int(right * RATE)
    margin = int(.25 * RATE)
    bl, br = max(0, al + global_lag - margin), min(len(b), ar + global_lag + margin)
    x, y = a[al:ar], b[bl:br]
    if len(y) < len(x):
        return None
    size = 1 << (len(x) + len(y) - 2).bit_length()
    conv = np.fft.irfft(np.fft.rfft(y, size) * np.fft.rfft(x[::-1], size), size)
    start, stop = len(x) - 1, len(y)
    index = int(np.argmax(conv[start:stop]))
    offset = bl + index - al
    return {'offset_seconds': offset / RATE,
        'correlation': correlation(x, y[index:index + len(x)]),
        'window_seconds': [left, right]}


def main():
    reference, candidate = map(Path, sys.argv[1:3])
    section = int(sys.argv[3]) if len(sys.argv) > 3 else None
    assert section in (None, 1, 2, 3)
    a, b = samples(reference), samples(candidate)
    duration = len(a) / RATE
    if section is None:
        windows_to_check = GLOBAL_WINDOWS
        content_end = 52.848625
    else:
        content_end = SECTION_CONTENT_ENDS[section]
        third = content_end / 3
        windows_to_check = [('early', .1, third), ('middle', third, third * 2), ('late', third * 2, content_end - .1)]
    size = 1 << (len(a) + len(b) - 2).bit_length()
    conv = np.fft.irfft(np.fft.rfft(b, size) * np.fft.rfft(a[::-1], size), size)
    radius = int(MAX_OFFSET * RATE)
    start = max(0, len(a) - 1 - radius)
    stop = min(len(a) + len(b) - 1, len(a) - 1 + radius + 1)
    lag = int(np.argmax(conv[start:stop]) + start - (len(a) - 1))
    a_start, b_start = max(0, -lag), max(0, lag)
    count = min(len(a) - a_start, len(b) - b_start)
    windows = {}
    local_offsets = {}
    for name, left, right in windows_to_check:
        al, ar = int(left * RATE), int(right * RATE)
        bl, br = al + lag, ar + lag
        windows[name] = correlation(a[al:ar], b[bl:br]) if ar <= len(a) and bl >= 0 and br <= len(b) else None
        local_offsets[name] = local_offset(a, b, left, right, lag)
    measured_offsets = [value['offset_seconds'] for value in local_offsets.values() if value]
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_entries', 'format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels,pix_fmt',
        '-of', 'json', str(candidate)]))
    result = {
        'reference_path': str(reference), 'candidate_path': str(candidate), 'section': section,
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
        'window_local_offsets': local_offsets,
        'window_offset_spread_seconds': max(measured_offsets) - min(measured_offsets) if measured_offsets else None,
        'source_end_in_output_seconds': (len(a) + lag) / RATE,
        'original_content_end_in_output_seconds': content_end + lag / RATE,
        'original_final_word_output_estimate_seconds': ([52.30 + lag / RATE, 52.50 + lag / RATE] if section is None else ([52.30 - 862 / 24 + lag / RATE, 52.50 - 862 / 24 + lag / RATE] if section == 3 else None)),
        'final_half_second_rms': float(np.sqrt(np.mean(b[-RATE // 2:] ** 2))),
        'probe': probe,
        'interpretation': 'Similarity and audio placement only. A high stable correlation supports soundtrack preservation through encoding; a low correlation cannot establish preserved voice or timing. Offset is not measured audiovisual lip sync. No perceptual listening performed.'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

