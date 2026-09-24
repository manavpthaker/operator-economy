"""Compare the approved opening with a local clip; never alters source media."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
REFERENCE = BASE / 'approved-opening-00m00s-00m20.9s.wav'
RATE = 16000
MAX_OFFSET_SECONDS = 2
WINDOWS = [('early', 0.5, 4.5), ('middle', 8.5, 12.5), ('late', 16.5, 20.5)]


def audio(path):
    data = subprocess.check_output([
        '/opt/homebrew/bin/ffmpeg', '-v', 'error', '-i', str(path),
        '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'
    ])
    samples = np.frombuffer(data, dtype='<f4').astype(np.float64)
    if len(samples) < 2:
        raise ValueError(f'No usable audio samples: {path}')
    return samples


def correlation(a, b):
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def compare(path):
    a, b = audio(REFERENCE), audio(path)
    size = 1 << (len(a) + len(b) - 2).bit_length()
    conv = np.fft.irfft(np.fft.rfft(b, size) * np.fft.rfft(a[::-1], size), size)
    max_offset = MAX_OFFSET_SECONDS * RATE
    start = max(0, len(a) - 1 - max_offset)
    stop = min(len(a) + len(b) - 1, len(a) - 1 + max_offset + 1)
    lag = int(np.argmax(conv[start:stop]) + start - (len(a) - 1))
    a_start, b_start = max(0, -lag), max(0, lag)
    count = min(len(a) - a_start, len(b) - b_start)
    windows = {}
    for name, left, right in WINDOWS:
        al, ar = int(left * RATE), int(right * RATE)
        bl, br = al + lag, ar + lag
        windows[name] = (
            correlation(a[al:ar], b[bl:br])
            if ar <= len(a) and bl >= 0 and br <= len(b) else None
        )
    return {
        'reference': str(REFERENCE), 'candidate': str(path),
        'reference_master_range_seconds': [0.0, 20.9],
        'reference_duration_seconds': len(a) / RATE,
        'candidate_audio_duration_seconds': len(b) / RATE,
        'audio_insertion_offset_seconds': lag / RATE,
        'offset_search_range_seconds': [-MAX_OFFSET_SECONDS, MAX_OFFSET_SECONDS],
        'offset_at_search_boundary': abs(lag) == max_offset,
        'audio_insertion_offset_convention': (
            'Positive means reference audio is placed later in the candidate; '
            'negative means the candidate begins partway into the reference.'
        ),
        'aligned_overlap_seconds': max(0, count) / RATE,
        'aligned_audio_correlation': correlation(
            a[a_start:a_start + count], b[b_start:b_start + count]
        ) if count > 0 else None,
        'segment_windows_reference_seconds': {
            name: [left, right] for name, left, right in WINDOWS
        },
        'segment_correlations': windows,
        'final_half_second_rms': float(np.sqrt(np.mean(b[-RATE // 2:] ** 2))),
        'interpretation': (
            'Waveform placement and similarity only; the insertion offset is not '
            'a measured audiovisual lip-sync offset. Low correlation or a search-boundary '
            'result does not establish reliable audio placement. Segment windows use '
            'reference time and the same fitted offset; unavailable windows are null.'
        )
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: audio_qa.py CANDIDATE_MEDIA REPORT_FILENAME.json')
    output = (BASE / sys.argv[2]).resolve()
    if output.parent != BASE:
        raise ValueError('Report must remain in the test directory')
    result = compare(Path(sys.argv[1]).resolve())
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
