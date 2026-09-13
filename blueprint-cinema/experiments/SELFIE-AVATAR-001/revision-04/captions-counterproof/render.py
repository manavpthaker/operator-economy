"""Experiment-local Counterproof burn using the installed Higgsfield burner.

Runs in the Higgsfield media sandbox. Inputs and upload destinations are supplied
in inputs.json; upload signatures are never written to the retained report.
"""
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
import zipfile
import zlib


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def download(url, dest):
    urllib.request.urlretrieve(url, dest)


def upload(path, url):
    mime = 'video/mp4' if path.endswith('.mp4') else 'image/jpeg'
    result = run(['curl', '-f', '-sS', '-X', 'PUT', '-H', 'Content-Type: ' + mime, '--upload-file', path,
                  '-o', '/dev/null', '-w', '%{http_code}', url],
                 capture_output=True, text=True)
    assert result.stdout == '200', result.stdout
    print('UPLOAD_OK', path, '200', flush=True)


cfg = json.loads(Path('inputs.json').read_text())
download(cfg['font_url'], 'Atkinson.ttf')
assert sha('Atkinson.ttf') == cfg['font_sha256']
download(cfg['video_url'], 'clean.mp4')
assert sha('clean.mp4') == cfg['video_sha256']
Path('script.json').write_text(json.dumps({'blocks': [{'vo_line': cfg['script']}]}, ensure_ascii=False))
workflows = Path(os.environ['HF_WORKFLOWS'])
subtitles = workflows / 'subtitles' / 'scripts'
run(['bash', str(subtitles / 'fetch_fonts.sh')], stdout=subprocess.DEVNULL)

# Independently check Whisper against the finished video's own speech. The prior
# exact-script word clock is also retained and compared at start/middle/end.
with open('transcription.log', 'w') as log:
    run([sys.executable, str(subtitles / 'audio_to_captions.py'), 'clean.mp4',
         '--srt', 'verification.srt', '--json', 'verification.json', '--script',
         'script.json', '--language', 'en', '--mixed', '--max-words', '5',
         '--max-chars', '32', '--minimum-similarity', '0.90'], stdout=log, stderr=log)
transcription = json.loads(Path('verification.json').read_text())
assert transcription['similarity'] >= 0.90
assert transcription['caption_words'] == transcription['timed_words'] == len(cfg['words'])
print('TRANSCRIPT_OK', transcription['similarity'], transcription['caption_words'], flush=True)

words = cfg['words']
assert ' '.join(w['text'] for w in words) == ' '.join(cfg['script'].split())
assert ' '.join(cfg['phrases']) == ' '.join(cfg['script'].split())
offset = cfg['audio_offset_seconds']
def stamp(t):
    total = round(t * 1000)
    return f'{total//3600000:02}:{total//60000%60:02}:{total//1000%60:02},{total%1000:03}'

cues = []
cursor = 0
for phrase in cfg['phrases']:
    count = len(phrase.split())
    assert count <= 5 and len(phrase) <= 32, phrase
    selected = words[cursor:cursor+count]
    assert phrase == ' '.join(w['text'] for w in selected)
    cues.append({'text': phrase, 'start': selected[0]['start'] + offset,
                 'end': selected[-1]['end'] + offset,
                 'source_first_word': cursor + 1, 'source_last_word': cursor + count})
    cursor += count
assert cursor == len(words)
Path('caps.srt').write_text('\n\n'.join(
    f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}"
    for i, c in enumerate(cues)) + '\n', encoding='utf-8')

# Pin the previously verified continuous-narration clock, shifted by the measured
# Sync insertion. Fresh final-video Whisper is an independent drift check.
new = transcription['captions']
checks = []
for idx in [0, len(new)//2, len(new)-1]:
    cue = new[idx]
    first_word = sum(len(c['text'].split()) for c in new[:idx])
    last_word = first_word + len(cue['text'].split()) - 1
    delta_start = cue['start'] - (words[first_word]['start'] + offset)
    delta_end = cue['end'] - (words[last_word]['end'] + offset)
    assert abs(delta_start) < 0.45 and abs(delta_end) < 0.45, (idx, delta_start, delta_end)
    checks.append({'new_cue': cue, 'start_delta': delta_start, 'end_delta': delta_end})

# Use the maintained burner for all fit, placement, hold logic and encoding.
# The user's named design system overrides its white/black default colors.
source = (subtitles / 'subtitle_paper_burn.py').read_text()
replacements = {
    'fill=(255, 255, 255, 255)': 'fill=(243, 246, 245, 255)',
    'stroke_fill=(0, 0, 0, 235)': 'stroke_fill=(32, 36, 38, 255)',
    '"-filter_complex",fc': '"-filter_complex_threads","1","-filter_complex",fc',
}
for old, new_text in replacements.items():
    assert source.count(old) == 1, old
    source = source.replace(old, new_text)
module = {'__name__': 'counterproof_burner', '__file__': str(subtitles / 'subtitle_paper_burn.py')}
exec(compile(source, module['__file__'], 'exec'), module)
ImageFont = module['ImageFont']
original_truetype = ImageFont.truetype
def weighted_font(*args, **kwargs):
    font = original_truetype(*args, **kwargs)
    if str(args[0]).endswith('Atkinson.ttf'):
        font.set_variation_by_axes([600])
    return font
ImageFont.truetype = weighted_font
sys.argv = ['counterproof_burner', '--in', 'clean.mp4', '--srt', 'caps.srt',
            '--out', 'counterproof.mp4', '--style', 'bold', '--font', 'Atkinson.ttf',
            '--no-caps', '--fontsize-frac', str(42/1280), '--bottom-frac', '0.17',
            '--maxw-frac', '0.77', '--stroke-frac', '0.045', '--gap', '0.042',
            '--tail', '0.18', '--bridge', '0.35', '--min-dur', '0.30']
module['main']()

def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', path], capture_output=True, text=True).stdout)
before, after = probe('clean.mp4'), probe('counterproof.mp4')
for kind in ['video', 'audio']:
    a = next(s for s in before['streams'] if s['codec_type'] == kind)
    b = next(s for s in after['streams'] if s['codec_type'] == kind)
    assert abs(float(a['duration'])-float(b['duration'])) < 0.05
    assert a.get('start_time') == b.get('start_time')
    if kind == 'video':
        for key in ['width', 'height', 'r_frame_rate', 'nb_frames']:
            assert a[key] == b[key], key
audio_hashes = []
for path in ['clean.mp4', 'counterproof.mp4']:
    digest = run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:a:0',
                  '-f', 'streamhash', '-hash', 'sha256', '-'], capture_output=True, text=True).stdout
    audio_hashes.append(digest)
assert audio_hashes[0] == audio_hashes[1]
run(['ffmpeg', '-v', 'error', '-xerror', '-i', 'counterproof.mp4', '-f', 'null', '-'])

from PIL import Image, ImageDraw
selected = [0, 12, len(cues)//2, len(cues)-1]
contact = Image.new('RGB', (1440, 1320), '#202426')
for j, index in enumerate(selected):
    c = cues[index]
    midpoint = (c['start']+c['end']) / 2
    out = f'frame-{index:02}.jpg'
    run(['ffmpeg', '-v', 'error', '-ss', str(midpoint), '-i', 'counterproof.mp4',
         '-frames:v', '1', '-q:v', '2', out])
    img = Image.open(out).resize((360,640))
    contact.paste(img, ((j%2)*720, (j//2)*660))
    # Keep large individual crops beside the portrait, for caption readability.
    crop = Image.open(out).crop((65, 875, 655, 1100)).resize((360,137))
    contact.paste(crop, ((j%2)*720+360, (j//2)*660+300))
contact.save('contact.jpg', quality=94)

report = {'status': 'mechanically_verified_pending_visual_review',
          'source_sha256': cfg['video_sha256'], 'output_sha256': sha('counterproof.mp4'),
          'output_bytes': Path('counterproof.mp4').stat().st_size,
          'font_sha256': sha('Atkinson.ttf'), 'font_weight': 600, 'font_size_px': 42,
          'text_color': '#F3F6F5', 'outline_color': '#202426',
          'source_asr_offset_seconds': offset, 'word_count': len(words),
          'cue_count': len(cues), 'timing_spot_checks': checks,
          'transcription_similarity': transcription['similarity'],
          'audio_decoded_hash': audio_hashes[0].strip(),
          'audio_unchanged': True, 'before': before, 'after': after,
          'burner_original_sha256': sha(subtitles / 'subtitle_paper_burn.py'),
          'burner_color_adapter_sha256': hashlib.sha256(source.encode()).hexdigest()}
Path('REPORT.json').write_text(json.dumps(report, indent=2))
Path('CUES.json').write_text(json.dumps(cues, indent=2, ensure_ascii=False))
upload('counterproof.mp4', cfg['video_upload_url'])
upload('contact.jpg', cfg['contact_upload_url'])
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for name in ['caps.srt', 'CUES.json', 'REPORT.json', 'verification.srt',
                 'verification.json', 'transcription.log']:
        archive.write(name)
print('RECORDS_ZIP_BASE64=' + base64.b64encode(buf.getvalue()).decode(), flush=True)
print('RENDER_COMPLETE', report['output_sha256'], report['output_bytes'], flush=True)
