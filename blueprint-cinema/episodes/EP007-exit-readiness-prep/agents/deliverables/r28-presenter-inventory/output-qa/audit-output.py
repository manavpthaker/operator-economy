#!/usr/bin/env python3
"""Read-only completed R28 output audit. Writes only beside this file."""
from pathlib import Path
import importlib.util
import json
import subprocess
import wave

from PIL import Image, ImageDraw

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
OWNED = Path(__file__).resolve().parent
PROVIDER = REPO / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r28-spatial-bridge/provider'
HELPER = OWNED.parent.parent / 'r25-lips-output-qa/audit-output.py'
spec = importlib.util.spec_from_file_location('r25_read_helpers', HELPER)
qa = importlib.util.module_from_spec(spec)
# Loading source through compile avoids writing __pycache__ outside this folder.
exec(compile(HELPER.read_text(), str(HELPER), 'exec'), qa.__dict__)

raw = PROVIDER / 'presenter-generated-raw.mp4'
source = PROVIDER / 'inputs/presenter-question-source.mp4'
audio = PROVIDER / 'inputs/question-exact.wav'
proposal_path = PROVIDER / 'PROPOSED-REQUEST.json'
proposal = json.loads(proposal_path.read_text())
assert qa.sha(raw) == '754c51ee1ee904cc4bb57ca4c3d0ece45d5ac36499169f145529db38ce4d1f28'
assert qa.sha(source) == proposal['input_files']['video']['sha256']
assert qa.sha(audio) == proposal['input_files']['audio']['sha256']
master = Path(proposal['source_audio']['path'])
assert qa.sha(master) == proposal['source_audio']['sha256']
with wave.open(str(master)) as f, wave.open(str(audio)) as g:
    f.setpos(6432000)
    assert g.getnframes() == 578000
    assert f.readframes(578000) == g.readframes(578000)

info = qa.probe(raw)
video = next(s for s in info['streams'] if s['codec_type'] == 'video')
decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(raw), '-map', '0', '-f', 'null', '-'], capture_output=True)
reference, output = qa.pcm(audio), qa.pcm(raw)
windows = []
for start, end in [(0, 3), (3, 6), (6, 9), (9, 12.041666666666666)]:
    a, b = round(start * 48000), round(end * 48000)
    windows.append({'local_seconds': [start, end], **qa.align(output[a:b], reference[a:b])})
times = [0, 3, 6, 9, 11.5, 12]
sheets = {name: Image.new('RGB', (768, 246 * len(times)), '#eeeae2') for name in ['full-comparison', 'face-comparison']}
for row, time in enumerate(times):
    for col, (name, path) in enumerate([('submitted source', source), ('React output', raw)]):
        image, actual = qa.frame_at(path, time, 289 / 24)
        for kind, sheet in sheets.items():
            picture = image.copy()
            if kind == 'face-comparison':
                w, h = image.size
                picture = image.crop((int(w * .34), int(h * .08), int(w * .66), int(h * .65)))
            picture.thumbnail((384, 216))
            x, y = col * 384, row * 246
            sheet.paste(picture, (x + (384 - picture.width) // 2, y + (216 - picture.height) // 2))
            ImageDraw.Draw(sheet).text((x + 6, y + 222), f'{name} | local {actual:.3f}s', fill='black')
for name, image in sheets.items():
    image.save(OWNED / f'{name}.jpg', quality=95)
inputs = [raw, source, audio, master, proposal_path, HELPER]
result = {
    'status': 'technical_complete_sampled_visual_pending',
    'input_hashes': [{'path': str(p.relative_to(REPO)), 'sha256': qa.sha(p)} for p in inputs],
    'metadata': {k: video.get(k) for k in ['width', 'height', 'avg_frame_rate', 'start_time', 'duration', 'nb_frames', 'nb_read_frames']},
    'full_decode': {'exit_code': decode.returncode, 'stderr': decode.stderr.decode()},
    'original_pcm_exact': True,
    'audio': {'full': qa.align(output[:578000], reference), 'windows': windows, 'decoded_samples': len(output)},
    'frame_uniqueness': {'source': qa.frame_hashes(source), 'output': qa.frame_hashes(raw)},
    'contact_times_seconds': times,
    'limits': ['Numbers and stills do not prove full-motion lip sync or exact body/head preservation.',
               'No source, runtime, provider, or approval writes were performed.'],
}
(OWNED / 'metrics.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['metadata', 'full_decode', 'original_pcm_exact', 'audio', 'frame_uniqueness']}, indent=2))
