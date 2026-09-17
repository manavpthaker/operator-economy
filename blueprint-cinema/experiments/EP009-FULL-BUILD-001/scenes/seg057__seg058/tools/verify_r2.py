"""Bounded render evidence for EP009 reviewer finding B-R1-01."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent.parent
R = P / 'qa/r2'
VIDEO = R / 's17ab.r2.mp4'
OLD_VIDEO = P / 'qa/s17ab.mp4'
ROOT = P.parents[4]
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
MI, MO, FPS, FRAMES = 903.333333, 976.541667, 24, 1757


def call(args):
    return subprocess.check_output(args)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame(path, n):
    data = call(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', f'select=eq(n\\,{n})', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    return Image.fromarray(np.frombuffer(data, np.uint8).reshape(720, 1280, 3))


def audio(path, filt=None):
    args = ['ffmpeg', '-v', 'error', '-i', str(path)]
    if filt:
        args += ['-af', filt]
    return np.frombuffer(call(args + ['-vn', '-ar', '48000', '-ac', '1', '-f', 'f32le', '-']), np.float32)


probe = json.loads(call(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(VIDEO)]))
vs = next(s for s in probe['streams'] if s['codec_type'] == 'video')
au = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
assert int(vs['nb_read_frames']) == FRAMES
assert (vs['width'], vs['height'], vs['r_frame_rate']) == (1280, 720, '24/1')
assert (au['sample_rate'], au['channels']) == ('48000', 2)
(R / 'PROBE.json').write_text(json.dumps(probe, indent=2) + '\n')
reference = audio(MASTER, f'atrim=start_sample={round(MI*48000)}:end_sample={round(MO*48000)},asetpts=N/SR/TB')
excerpt = audio(P / 'public/audio/narration.wav')
rendered = audio(VIDEO)
assert len(reference) == len(excerpt)
excerpt_corr = float(np.corrcoef(reference, excerpt)[0, 1])
render_corr = float(np.corrcoef(reference, rendered[:len(reference)])[0, 1])
assert excerpt_corr > .999999 and render_corr >= .999
raw = call(['ffmpeg', '-v', 'error', '-i', str(VIDEO), '-vf', 'scale=128:72', '-an', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
small_frames = np.frombuffer(raw, np.uint8).reshape(-1, 72, 128)
uniform = np.flatnonzero(np.ptp(small_frames, axis=(1, 2)) <= 2).tolist()
assert len(small_frames) == FRAMES and not uniform

sys.path.insert(0, str(P / 'tools'))
spec = importlib.util.spec_from_file_location('build_r2', P / 'tools/build.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cues = mod.scene()['cues']
cue_stills = []
for name, at in [('start', 0)] + [(k, min(v + .7, (FRAMES-1)/FPS)) for k, v in cues.items()] + [('end', (FRAMES-1)/FPS)]:
    n = round(at * FPS)
    out = R / 'stills' / f'{n:04d}-{name}.png'
    frame(VIDEO, n).save(out)
    cue_stills.append({'name': name, 'frame': n, 'master_time': MI+n/FPS, 'path': str(out.relative_to(ROOT))})

# Read every encoded frame across both append reveals, including the reported defect interval.
windows = {'eight': range(520, 533), 'twelve': range(556, 577)}
strip_paths = []
for name, numbers in windows.items():
    numbers = list(numbers)
    sheet = Image.new('RGB', (1030, len(numbers)*62), '#ffffff')
    draw = ImageDraw.Draw(sheet)
    for row, n in enumerate(numbers):
        img = frame(VIDEO, n)
        path = R / 'stills' / f'{n:04d}-{name}-transition.png'
        img.save(path)
        sheet.paste(img.crop((230, 306, 1110, 348)), (148, row*62+16))
        draw.text((8, row*62+28), f'{MI+n/FPS:.3f}  f{n}', fill='black')
    out = R / f'{name}-all-frames.png'
    sheet.save(out)
    strip_paths.append(str(out.relative_to(ROOT)))

# Contact sheet records the entire bounded scene; full-size stills remain available.
cols, cw, ch = 4, 480, 295
sheet = Image.new('RGB', (cols*cw, ((len(cue_stills)+cols-1)//cols)*ch), '#ffffff')
draw = ImageDraw.Draw(sheet)
for i, info in enumerate(cue_stills):
    x, y = (i%cols)*cw, (i//cols)*ch
    img = Image.open(ROOT/info['path']).resize((480,270))
    sheet.paste(img,(x,y+25))
    draw.text((x+6,y+6),f"{info['name']}  master {info['master_time']:.3f}",fill='black')
sheet.save(R/'contact-r2.png')

boundaries = {}
for name, n in [('first',0), ('last',FRAMES-1)]:
    a = np.asarray(frame(OLD_VIDEO,n)).astype(np.int16)
    b = np.asarray(frame(VIDEO,n)).astype(np.int16)
    diff = np.abs(a-b)
    boundaries[name] = {'max_channel_difference': int(diff.max()), 'pixels_over_20': int((diff.max(axis=2)>20).sum()), 'mean_absolute_channel_difference': float(diff.mean())}

# Constant prefix must not move or crossfade while later clauses append.
baseline = np.asarray(frame(VIDEO,520))[311:339,248:408].astype(np.int16)
prefix_diffs = []
for n in list(windows['eight']) + list(windows['twelve']):
    sample = np.asarray(Image.open(R/'stills'/f'{n:04d}-{"eight" if n in windows["eight"] else "twelve"}-transition.png'))[311:339,248:408].astype(np.int16)
    prefix_diffs.append({'frame': n, 'max_channel_difference': int(np.abs(sample-baseline).max())})

result = {
    'finding': 'B-R1-01', 'video': str(VIDEO.relative_to(ROOT)), 'sha256': sha(VIDEO),
    'frames': FRAMES, 'expected_frames': round(MO*FPS)-round(MI*FPS), 'frames_ok': True,
    'format': '1280x720 24/1; stereo 48000 Hz', 'audio_corr_zero_lag': render_corr,
    'source_excerpt_vs_master_corr': excerpt_corr, 'trailing_encoder_samples': len(rendered)-len(reference),
    'uniform_frames': uniform, 'all_frames_scanned': len(small_frames), 'cue_stills': cue_stills,
    'transition_sheets': strip_paths, 'boundaries_vs_r1': boundaries, 'constant_prefix_pixel_differences': prefix_diffs,
    'inputs': {str(p.relative_to(ROOT)):sha(p) for p in [MASTER,P/'public/audio/narration.wav',P/'package.json',P/'index.html',P/'tools/build.py']},
    'review_limits': 'Frame evidence and waveform correlation; not an audio listening, normal-speed comprehension, whole-episode rhythm or owner acceptance verdict.'
}
(R/'VERIFY.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['cue_stills','inputs','constant_prefix_pixel_differences']},indent=2))
