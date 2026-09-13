"""Read-only native soundtrack diagnosis in the Higgsfield media sandbox.

Usage: python3 diagnose_native.py inputs.json
Required config: native_url, native_sha, voice_url, voice_sha.
Prints one JSON report. No upload, generation, repair or perceptual pass claim.
"""
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path

import numpy as np

RATE = 16000
WINDOWS = [
    ('opening', .20, 3.50),
    ('admission', 3.75, 5.45),
    ('With_AI', 5.50, 6.60),
    ('GTM_broad', 11.20, 16.72),
    ('GTM_entry', 10.70, 11.70),
    ('GTM_name_early', 11.70, 12.70),
    ('GTM_name_late', 12.70, 13.70),
    ('GTM_after_name', 13.70, 14.70),
    ('GTM_code', 14.70, 16.72),
    ('research_ending', 17.12, 20.83),
]


def download(url, digest, destination):
    with urllib.request.urlopen(url, timeout=45) as response:
        data = response.read()
    assert hashlib.sha256(data).hexdigest() == digest, destination.name
    destination.write_bytes(data)
    return data


def samples(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
        '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def correlation(a, b):
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def convolution(a, b):
    size = 1 << (len(a) + len(b) - 2).bit_length()
    return np.fft.irfft(np.fft.rfft(b, size) * np.fft.rfft(a[::-1], size), size)


def measure_window(a, b, left, right, global_lag):
    al, ar = round(left * RATE), round(right * RATE)
    margin = RATE // 2
    bl = max(0, al + global_lag - margin)
    br = min(len(b), ar + global_lag + margin)
    x, y = a[al:ar], b[bl:br]
    window = {'source_window_seconds': [left, right]}
    if ar > len(a) or len(y) < len(x):
        return {**window, 'lag_seconds': None, 'correlation': None,
            'availability': 'Insufficient source or candidate duration for complete window'}
    cv = convolution(x, y)
    index = int(np.argmax(cv[len(x)-1:len(y)]))
    lag = bl + index - al
    return {**window, 'lag_seconds': lag / RATE,
        'correlation': correlation(x, y[index:index+len(x)]),
        'search_boundary_hit': index in (0, len(y)-len(x))}


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    voice = Path('/home/user/r9-current-voice.wav')
    native = Path('/home/user/r9-current-native.mp4')
    voice_bytes = download(cfg['voice_url'], cfg['voice_sha'], voice)
    download(cfg['native_url'], cfg['native_sha'], native)
    with wave.open(io.BytesIO(voice_bytes)) as wav:
        assert (wav.getframerate(), wav.getnchannels(), wav.getsampwidth(),
                wav.getnframes()) == (48000, 1, 2, 1020000), 'Expected approved R7 WAV'

    a, b = samples(voice), samples(native)
    cv = convolution(a, b)
    start = max(0, len(a)-1-RATE)
    stop = min(len(a)+len(b)-1, len(a)+RATE)
    lag = int(np.argmax(cv[start:stop]) + start - (len(a)-1))
    aa, bb = max(0, -lag), max(0, lag)
    overlap = min(len(a)-aa, len(b)-bb)
    windows = {name: measure_window(a, b, left, right, lag)
        for name, left, right in WINDOWS}
    valid = [w for w in windows.values() if w['correlation'] is not None]
    lags = [w['lag_seconds'] for w in valid]
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_entries', 'format=duration,start_time:stream=index,codec_type,codec_name,width,height,r_frame_rate,nb_frames,start_time,duration,sample_rate,channels',
        '-of', 'json', str(native)]))
    report = {
        'scope': 'Read-only comparison of new native audio with approved R7 source',
        'voice_url': cfg['voice_url'], 'voice_sha256': cfg['voice_sha'],
        'native_url': cfg['native_url'], 'native_sha256': cfg['native_sha'],
        'source_duration_seconds': len(a) / RATE,
        'decoded_native_audio_duration_seconds': len(b) / RATE,
        'analysis_sample_rate_hz': RATE,
        'global_lag_seconds': lag / RATE,
        'global_correlation': correlation(a[aa:aa+overlap], b[bb:bb+overlap]),
        'global_search_boundary_hit': abs(lag) == RATE,
        'aligned_overlap_seconds': overlap / RATE,
        'windows': windows,
        'local_lag_spread_seconds': max(lags)-min(lags) if lags else None,
        'minimum_window_correlation': min(w['correlation'] for w in valid) if valid else None,
        'native_probe': probe,
        'lag_sign': 'Negative means the matching native audio occurs earlier than the R7 source.',
        'limits': 'Correlation and lag only. No audible identity, complete-word, visual lip-sync or remux acceptance claim. Broad-window correlation can drop when it contains different local lags.',
    }
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()

