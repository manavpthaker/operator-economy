"""Probe, decode, sample and measure original-waveform placement; never infer visual lip sync."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parent
ROOT = next(p for p in BASE.parents if (p / '.agents').is_dir())
RATE = 16000


def audio(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1',
        '-ar', str(RATE), '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(data, dtype='<f4').astype(np.float64)


def corr(a, b):
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def compare(reference, candidate):
    a, b = audio(reference), audio(candidate)
    size = 1 << (len(a) + len(b) - 2).bit_length()
    convolution = np.fft.irfft(np.fft.rfft(b, size) * np.fft.rfft(a[::-1], size), size)
    bound = 2 * RATE
    start = max(0, len(a) - 1 - bound)
    stop = min(len(a) + len(b) - 1, len(a) - 1 + bound + 1)
    lag = int(np.argmax(convolution[start:stop]) + start - len(a) + 1)
    left_a, left_b = max(0, -lag), max(0, lag)
    count = min(len(a) - left_a, len(b) - left_b)
    windows = {}
    duration = len(a) / RATE
    for name, fraction in [('early', .16), ('middle', .5), ('late', .84)]:
        center = int(duration * fraction * RATE)
        half = int(min(1, duration * .12) * RATE)
        al, ar = max(0, center - half), min(len(a), center + half)
        bl, br = al + lag, ar + lag
        windows[name] = corr(a[al:ar], b[bl:br]) if bl >= 0 and br <= len(b) else None
    return {'audio_insertion_offset_seconds': lag / RATE,
        'aligned_audio_correlation': corr(a[left_a:left_a + count], b[left_b:left_b + count]),
        'segment_correlations': windows, 'offset_at_search_boundary': abs(lag) == bound,
        'reference_duration_seconds': duration, 'candidate_audio_duration_seconds': len(b) / RATE,
        'aligned_overlap_seconds': count / RATE,
        'interpretation': 'Waveform placement only. Not a measured audiovisual lip-sync offset.'}


def inspect(take, stage):
    folder = BASE / take
    media = folder / f'{stage}.mp4'
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
        '-show_format', '-of', 'json', str(media)]))
    (folder / f'{stage}-probe.json').write_text(json.dumps(probe, indent=2) + '\n')
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(media), '-f', 'null', '-'], check=True)
    duration = float(video.get('duration', probe['format']['duration']))
    times = [0.2, duration * .25, duration * .5, duration * .75, max(0, duration - .12)]
    sheet = Image.new('RGB', (1600, 204), '#202020')
    draw = ImageDraw.Draw(sheet)
    for i, at in enumerate(times):
        data = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(at), '-i', str(media),
            '-frames:v', '1', '-vf', 'scale=320:180', '-f', 'image2pipe', '-vcodec', 'png', 'pipe:1'])
        sheet.paste(Image.open(io.BytesIO(data)), (i * 320, 0))
        draw.text((i * 320 + 8, 184), f'{take} {at:.3f}s', fill='white')
    sheet.save(folder / f'{stage}-contact.png')
    result = {'take': take, 'stage': stage, 'sha256': hashlib.sha256(media.read_bytes()).hexdigest(),
        'width': video['width'], 'height': video['height'], 'fps': video['r_frame_rate'],
        'pixel_format': video['pix_fmt'], 'frames': video.get('nb_frames'),
        'duration_seconds': duration, 'full_decode': 'pass', 'sample_times': times}
    if stage == 'restored':
        reference = ROOT / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/avatar-v5-current-cut-preparation/audio' / f'{take}.wav'
        result['audio'] = compare(reference, media)
    (folder / f'{stage}-qa.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    print(json.dumps(inspect(sys.argv[1], sys.argv[2])))
