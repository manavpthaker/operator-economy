"""Replace only the R10 picture from frame 902; retain its full audio timeline.

Run only in the Higgsfield sandbox beside inputs.json, render.py, and the
unchanged R10 audio_alignment.py. Upload URLs stay in runtime inputs and are
never printed or archived. Frame/audio checks are not visual lip-sync approval.
"""
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import urllib.request
import wave
import zipfile

from PIL import Image, ImageDraw, ImageFont


FPS = 24
PREFIX_FRAMES = 902
TAIL_FRAMES = 420
TOTAL_FRAMES = PREFIX_FRAMES + TAIL_FRAMES
TAIL_START_SAMPLE = 1804000
SCRIPT_SHA256 = '242ab0bedea72a8fc5d303191f9dc61569614dc70cfdbef759891a7fa94affd6'
VOICE_SHA256 = 'ebda957ffd92f944ce180ffab455da84e48cfffd9ae775936be6cff3d085ba0f'
SRT_SHA256 = '215b5b7e397604ed51d12cd9da4f5a16d6b34506217d2277088b6a12674d7364'


def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def capture(args):
    return run(args, capture_output=True, text=True).stdout


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def probe(path):
    return json.loads(capture(['ffprobe', '-v', 'error', '-show_streams',
                               '-show_format', '-of', 'json', str(path)]))


def stream(info, kind):
    return next(item for item in info['streams'] if item['codec_type'] == kind)


def check_picture(info, frames):
    video = stream(info, 'video')
    assert (video['width'], video['height']) == (720, 1280)
    assert video['r_frame_rate'] == '24/1'
    assert video['pix_fmt'] == 'yuv420p'
    assert int(video['nb_frames']) == frames, video
    assert abs(float(video.get('start_time', 0))) < 1e-5
    assert abs(float(video['duration']) - frames / FPS) < 1e-5


def audio_hash(path, compressed=False):
    args = ['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0']
    if compressed:
        args += ['-c:a', 'copy']
    args += ['-f', 'hash', '-hash', 'sha256', '-']
    return capture(args).strip().split('=')[-1]


def audio_clock(info):
    audio = stream(info, 'audio')
    return {key: audio.get(key) for key in ('codec_name', 'sample_rate',
        'channels', 'time_base', 'start_pts', 'start_time', 'duration_ts',
        'duration', 'nb_frames')}


def picture_hashes(path, first_frame=0, last_frame=PREFIX_FRAMES):
    output = capture(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
        '-vf', f'trim=start_frame={first_frame}:end_frame={last_frame}',
        '-fps_mode', 'passthrough', '-f', 'framemd5', '-'])
    hashes = [line.rsplit(',', 1)[-1].strip() for line in output.splitlines()
              if line and not line.startswith('#')]
    assert len(hashes) == last_frame - first_frame
    return hashes


cfg = json.loads(Path('inputs.json').read_text())
assert hashlib.sha256(cfg['script'].encode()).hexdigest() == SCRIPT_SHA256
assert cfg['voice_sha256'] == VOICE_SHA256
assert cfg['srt_sha256'] == SRT_SHA256
assert hashlib.sha256(cfg['srt'].encode()).hexdigest() == SRT_SHA256
sources = [('prior_clean', 'prior-clean.mp4'), ('prior_final', 'prior-final.mp4'),
           ('tail', 'tail.mp4'), ('voice', 'voice.wav')]
source_receipts = {}
for key, path in sources:
    urllib.request.urlretrieve(cfg[key + '_url'], path)
    assert sha(path) == cfg[key + '_sha256'], key
    source_receipts[key] = {'sha256': sha(path), 'bytes': Path(path).stat().st_size,
                            'probe': probe(path)}
check_picture(source_receipts['prior_clean']['probe'], TOTAL_FRAMES)
check_picture(source_receipts['prior_final']['probe'], TOTAL_FRAMES)
check_picture(source_receipts['tail']['probe'], TAIL_FRAMES)

# Derive precisely the unchanged 48 kHz PCM source slice used for this repair.
with wave.open('voice.wav', 'rb') as source:
    assert (source.getnchannels(), source.getsampwidth(), source.getframerate()) == (1, 2, 48000)
    assert source.getnframes() == 2643731
    source.setpos(TAIL_START_SAMPLE)
    tail_pcm = source.readframes(source.getnframes() - TAIL_START_SAMPLE)
with wave.open('source-tail.wav', 'wb') as output:
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(48000)
    output.writeframes(tail_pcm)
if cfg.get('tail_source_voice_sha256'):
    assert sha('source-tail.wav') == cfg['tail_source_voice_sha256']

qa_text = capture(['python3', 'audio_alignment.py', 'source-tail.wav', 'tail.mp4'])
tail_qa = json.loads(qa_text)
Path('TAIL-AUDIO-QA.json').write_text(qa_text)
assert tail_qa['measured_window_count'] == 6
assert tail_qa['aligned_audio_correlation'] >= .99
assert tail_qa['minimum_window_correlation'] >= .99
assert tail_qa['minimum_window_correlation_at_global_offset'] >= .99
assert tail_qa['window_offset_spread_seconds'] <= .002
assert abs(tail_qa['source_to_picture_offset_seconds']) <= .002
assert not tail_qa['offset_at_search_boundary']
assert tail_qa['full_source_sample_extent_covered']

# Lossless encoding lets us prove the decoded prefix survives the splice.
# The retained soundtrack is copied from the exact previously delivered file.
filters = (f'[0:v]trim=end_frame={PREFIX_FRAMES},setpts=PTS-STARTPTS[p];'
           f'[1:v]trim=end_frame={TAIL_FRAMES},setpts=PTS-STARTPTS[t];'
           '[p][t]concat=n=2:v=1:a=0[v]')
run(['ffmpeg', '-y', '-v', 'error', '-i', 'prior-clean.mp4', '-i', 'tail.mp4',
     '-filter_complex_threads', '1',
     '-filter_complex', filters, '-map', '[v]', '-an',
     '-c:v', 'libx264', '-preset', 'fast', '-crf', '0', '-pix_fmt', 'yuv420p',
     '-r', str(FPS), '-frames:v', str(TOTAL_FRAMES),
     '-movflags', '+faststart', 'picture.mp4'])
# Mux separately: a video frame limit in the encoding command otherwise stops
# AAC packet copying early while the video encoder is still buffering frames.
run(['ffmpeg', '-y', '-v', 'error', '-i', 'picture.mp4', '-i', 'prior-final.mp4',
     '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart', 'clean.mp4'])
clean_probe = probe('clean.mp4')
check_picture(clean_probe, TOTAL_FRAMES)
prefix_before = picture_hashes('prior-clean.mp4')
prefix_after = picture_hashes('clean.mp4')
assert prefix_before == prefix_after
tail_before = picture_hashes('tail.mp4', 0, TAIL_FRAMES)
tail_after = picture_hashes('clean.mp4', PREFIX_FRAMES, TOTAL_FRAMES)
assert tail_before == tail_after
prior_audio_decoded = audio_hash('prior-final.mp4')
prior_audio_compressed = audio_hash('prior-final.mp4', compressed=True)
assert audio_hash('clean.mp4') == prior_audio_decoded
assert audio_hash('clean.mp4', compressed=True) == prior_audio_compressed
assert audio_clock(clean_probe) == audio_clock(source_receipts['prior_final']['probe'])

full_qa_text = capture(['python3', 'audio_alignment.py', 'voice.wav', 'clean.mp4'])
full_qa = json.loads(full_qa_text)
Path('AUDIO-QA.json').write_text(full_qa_text)
assert full_qa['full_source_sample_extent_covered']
assert full_qa['measured_window_count'] == 6
assert full_qa['aligned_audio_correlation'] >= .99
assert full_qa['minimum_window_correlation'] >= .99
assert full_qa['minimum_window_correlation_at_global_offset'] >= .99
assert full_qa['window_offset_spread_seconds'] <= .002
assert abs(full_qa['source_to_picture_offset_seconds']) <= .002

splice = {
    'sources': source_receipts, 'clean_sha256': sha('clean.mp4'),
    'clean_bytes': Path('clean.mp4').stat().st_size, 'clean_probe': clean_probe,
    'prefix_frames': PREFIX_FRAMES, 'tail_frames': TAIL_FRAMES,
    'total_frames': TOTAL_FRAMES, 'fps': FPS,
    'splice_seconds': PREFIX_FRAMES / FPS, 'tail_source_start_sample': TAIL_START_SAMPLE,
    'source_tail_sha256': sha('source-tail.wav'),
    'decoded_prefix_identical_to_r10_clean': True,
    'decoded_tail_identical_to_repair_output': True,
    'prefix_frame_md5_list_sha256': hashlib.sha256('\n'.join(prefix_before).encode()).hexdigest(),
    'tail_frame_md5_list_sha256': hashlib.sha256('\n'.join(tail_before).encode()).hexdigest(),
    'full_audio_copied_from_prior_final': True,
    'compressed_audio_payload_sha256': prior_audio_compressed,
    'decoded_audio_sha256': prior_audio_decoded,
    'audio_timeline_identical_to_prior_final': True,
    'audio_clock': audio_clock(clean_probe),
    'tail_audio_qa_sha256': sha('TAIL-AUDIO-QA.json'),
    'full_audio_qa_sha256': sha('AUDIO-QA.json'),
    'limits': 'Decoded picture preservation and soundtrack placement only; no visual lip-sync verdict.'}
write_json('SPLICE-QA.json', splice)

binding = {
    'video_sha256': sha('clean.mp4'), 'script_sha256': SCRIPT_SHA256,
    'source_voice_sha256': VOICE_SHA256, 'srt_sha256': SRT_SHA256,
    'source_srt_sha256': SRT_SHA256, 'source_word_map_sha256': cfg['source_word_map_sha256'],
    'source_caption_receipt_sha256': cfg['source_caption_receipt_sha256'],
    'prior_final_sha256': cfg['prior_final_sha256'],
    'word_count': len(cfg['script'].split()), 'similarity': 1.0,
    'source_to_picture_offset_seconds': full_qa['source_to_picture_offset_seconds'],
    'splice_qa_sha256': sha('SPLICE-QA.json'), 'audio_qa_sha256': sha('AUDIO-QA.json'),
    'method': 'Reuse the verified R10 full-source Whisper SRT because compressed audio payloads, decoded audio, and the complete audio clock match the previously delivered file exactly. Bind unchanged caption bytes to this new clean picture.',
    'limits': 'This verifies caption text and timeline continuity; it is not visual lip-sync acceptance.'}
assert binding['word_count'] == 193
write_json('CAPTION-BINDING.json', binding)
cfg['video_local_path'] = 'clean.mp4'
cfg['video_sha256'] = binding['video_sha256']
cfg['transcription'] = {key: binding[key] for key in
    ('video_sha256', 'script_sha256', 'srt_sha256', 'word_count', 'similarity')}
cfg['transcription']['evidence_sha256'] = sha('CAPTION-BINDING.json')
cfg['audio_binding'] = {'video_sha256': binding['video_sha256'],
    'source_audio_sha256': VOICE_SHA256, 'video_audio_decoded_sha256': prior_audio_decoded,
    'full_source_audio_preserved': True, 'evidence_sha256': sha('SPLICE-QA.json')}
cfg['contact_times_seconds'] = [38.2, 44.0, 49.0, 54.5]
cfg['finish_manages_delivery'] = True
Path('inputs.json').write_text(json.dumps(cfg))
run(['python3', 'render.py'])

# Final video and still contact are already strictly decoded by the renderer.
# These paired stills aid inspection, without establishing motion accuracy.
diagnostic_samples = [('Maybe', 38.15), ('hobby', 49.20), ('business', 54.60)]
diagnostic = Image.new('RGB', (1080, 1360), '#202426')
draw = ImageDraw.Draw(diagnostic)
label_font = ImageFont.truetype('Archivo.ttf', 23)
for column, (word, at) in enumerate(diagnostic_samples):
    for row, (source, label) in enumerate([('prior-clean.mp4', 'R10 before'),
                                           ('clean.mp4', 'R11 repair')]):
        filename = f'diagnostic-{column}-{row}.jpg'
        run(['ffmpeg', '-v', 'error', '-ss', str(at), '-i', source,
             '-frames:v', '1', '-q:v', '2', filename])
        x, y = column * 360, row * 680
        draw.text((x + 12, y + 8), f'{label} | {word} {at:.2f}s',
                  font=label_font, fill='#F3F6F5')
        diagnostic.paste(Image.open(filename).resize((360, 640)), (x, y + 40))
diagnostic.save('diagnostic.jpg', quality=94)

outputs = [('heading.mp4', 'video_upload_url', 'video/mp4'),
           ('contact.jpg', 'contact_upload_url', 'image/jpeg')]
if cfg.get('diagnostic_upload_url'):
    outputs.append(('diagnostic.jpg', 'diagnostic_upload_url', 'image/jpeg'))
excerpt_receipt = None
if cfg.get('excerpt_upload_url'):
    run(['ffmpeg', '-y', '-v', 'error', '-ss', '37', '-i', 'heading.mp4',
         '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'fast',
         '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
         '-movflags', '+faststart', 'tail-review.mp4'])
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', 'tail-review.mp4', '-f', 'null', '-'])
    excerpt_receipt = {'start_in_full_video_seconds': 37,
        'sha256': sha('tail-review.mp4'), 'bytes': Path('tail-review.mp4').stat().st_size,
        'probe': probe('tail-review.mp4'),
        'purpose': 'Playback convenience excerpt; the full delivery retains the exact copied audio.'}
    outputs.append(('tail-review.mp4', 'excerpt_upload_url', 'video/mp4'))

delivery = {'status': 'mechanically_verified_pending_visual_review',
    'full_video_sha256': sha('heading.mp4'), 'full_video_bytes': Path('heading.mp4').stat().st_size,
    'duration_seconds': TOTAL_FRAMES / FPS, 'frames': TOTAL_FRAMES,
    'caption_bytes_unchanged': sha('caps.srt') == SRT_SHA256,
    'full_audio_unchanged_from_r10': audio_hash('heading.mp4') == prior_audio_decoded,
    'compressed_audio_payload_unchanged_from_r10': audio_hash('heading.mp4', True) == prior_audio_compressed,
    'diagnostic_still_samples': [{'word': word, 'seconds': at} for word, at in diagnostic_samples],
    'diagnostic_still_sha256': sha('diagnostic.jpg'),
    'excerpt': excerpt_receipt, 'uploads': [],
    'limits': 'The repaired tail and its transitions require playback review; no technical check proves natural or accurate mouth motion.'}
assert delivery['caption_bytes_unchanged']
assert delivery['full_audio_unchanged_from_r10']
assert delivery['compressed_audio_payload_unchanged_from_r10']
for path, key, mime in outputs:
    status = capture(['curl', '-f', '-sS', '-X', 'PUT', '-H', 'Content-Type: ' + mime,
        '--upload-file', path, '-o', '/dev/null', '-w', '%{http_code}', cfg[key]])
    assert status == '200', path
    delivery['uploads'].append({'file': path, 'http_status': 200,
        'sha256': sha(path), 'bytes': Path(path).stat().st_size})
    print('UPLOAD_OK', path, 200, flush=True)
write_json('FINISH-DELIVERY.json', delivery)

records = ['TAIL-AUDIO-QA.json', 'AUDIO-QA.json', 'SPLICE-QA.json',
           'CAPTION-BINDING.json', 'REPORT.json', 'LAYOUT.json', 'caps.srt',
           'FINISH-DELIVERY.json']
buffer = io.BytesIO()
with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for name in records:
        archive.write(name)
encoded = base64.b64encode(buffer.getvalue()).decode()
# Bound each output item without failing an already uploaded delivery.
for part, start in enumerate(range(0, len(encoded), 9000), 1):
    print(f'RECORDS_ZIP_BASE64_PART_{part}=' + encoded[start:start + 9000], flush=True)
print('FINISH_COMPLETE', delivery['full_video_sha256'], delivery['full_video_bytes'], flush=True)
