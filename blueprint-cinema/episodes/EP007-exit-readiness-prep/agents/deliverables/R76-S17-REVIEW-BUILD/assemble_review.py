#!/usr/bin/env python3
"""Root-run R76 review assembly. No provider calls, redesign, or canonical edits.

Prepared without execution. Run only after provider/ALIGNMENT.json and the exact
restored source exist. Outputs are limited to the two new R76 review folders.
Existing outputs are never overwritten. Uses Python standard library + ffmpeg.
"""
from pathlib import Path
import array
import hashlib
import json
import math
import subprocess
import sys
import wave


ROOT = next(p for p in Path(__file__).resolve().parents if (p / '.agents').is_dir())
EXP = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
H = EXP / 'hyperframes/reviews/r76-s17-presenter'
C = EXP / 'hyperframes/reviews/r76-s17-context'
RESTORED = H / 'provider/restoration/restored.mp4'
ALIGNMENT = H / 'provider/ALIGNMENT.json'
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
TAIL = EXP / 'hyperframes/reviews/r62-s17-animation-context/qa/context.mp4'
P1 = EXP / 'hyperframes/reviews/r62-s17-p1/qa/r62-s17-p1.mp4'
P2 = EXP / 'hyperframes/reviews/r62-s17-p2/qa/r62-s17-p2.mp4'
REFERENCE = H / 'provider/audio/c.wav'
FIXED_PINS = {
    MASTER: 'd8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9',
    TAIL: '11a907ec3de4c701ad3c5e61c44b23f2f8e9bf02c6b66b82b11418c47df8a39c',
    P1: '71c969e9d9af2d05c997316de104d6ec137d79f84486690e27d523954f748e04',
    P2: '439cd6cca8bc34a4b9abb18b208bb79ad893b48864be044f34ff68701f533555',
    REFERENCE: 'd3912f9d313f463df0836025fbaec6e74ad8cc51bd4bb0072c581d8e4c458724',
}
FPS = 24
SAMPLE_RATE = 48000
SCENE_FRAMES = 192
CONTEXT_FRAMES = 1803
SCENE_MASTER_SAMPLE = 37176000
CONTEXT_MASTER_SAMPLE = 35370000
PRESENTER_CONTEXT_START_FRAME = 903
PRESENTER_CONTEXT_END_FRAME = 1095
COMMANDS = []


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def run(command):
    COMMANDS.append(command)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError('Command failed: ' + repr(command) + '\n' +
                           result.stderr.decode(errors='replace')[-12000:])
    return result.stdout


def fresh_write(path, value):
    with path.open('x', encoding='utf-8') as handle:
        handle.write(value)


def save(path, value):
    fresh_write(path, json.dumps(value, indent=2) + '\n')


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                          '-show_format', '-of', 'json', str(path)]))


def video_stream(info):
    return next(s for s in info['streams'] if s['codec_type'] == 'video')


def require_video(path, frames=None, size=None):
    info = probe(path)
    video = video_stream(info)
    assert video['r_frame_rate'] == '24/1', (path, video)
    assert video.get('avg_frame_rate') == '24/1', (path, video)
    assert 'nb_frames' in video, 'Require explicit video frame count: ' + str(path)
    if frames is not None:
        assert int(video['nb_frames']) == frames, (path, video)
    if size is not None:
        assert (video['width'], video['height']) == size, (path, video)
    return info


def read_master_pcm(start_sample, sample_count):
    with wave.open(str(MASTER), 'rb') as source:
        assert (source.getframerate(), source.getnchannels(), source.getsampwidth()) == (48000, 1, 2)
        source.setpos(start_sample)
        pcm = source.readframes(sample_count)
        assert len(pcm) == sample_count * 2
    return pcm


def verify_pcm(path, expected):
    with wave.open(str(path), 'rb') as source:
        assert (source.getframerate(), source.getnchannels(), source.getsampwidth()) == (48000, 1, 2)
        actual = source.readframes(source.getnframes())
    assert actual == expected, 'Source PCM differs: ' + str(path)
    return {'path': relative(path), 'sha256': sha(path),
            'pcm_sha256': hashlib.sha256(actual).hexdigest(),
            'samples': len(actual) // 2, 'sample_rate': 48000,
            'channels': 1, 'sample_width_bytes': 2, 'bit_exact_master_slice': True}


def write_pcm(path, pcm):
    assert not path.exists(), 'Output already exists: ' + str(path)
    with wave.open(str(path), 'wb') as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(48000)
        target.writeframes(pcm)
    return verify_pcm(path, pcm)


def decode_audio(path, start_seconds, duration_seconds, channel=0):
    audio_filter = (f'atrim=start={start_seconds:.9f}:duration={duration_seconds:.9f},'
                    f'asetpts=PTS-STARTPTS,pan=mono|c0=c{channel}')
    raw = run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-vn',
               '-af', audio_filter, '-ar', '8000', '-f', 'f32le', '-'])
    samples = array.array('f')
    samples.frombytes(raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    expected = round(duration_seconds * 8000)
    assert len(samples) == expected, (path, start_seconds, len(samples), expected)
    return samples


def audio_metrics(actual, expected):
    assert len(actual) == len(expected) and len(actual) > 0
    aa = sum(x * x for x in actual)
    bb = sum(x * x for x in expected)
    ab = sum(x * y for x, y in zip(actual, expected))
    assert aa > 0 and bb > 0, 'Audio comparison window is silent'
    correlation = ab / math.sqrt(aa * bb)
    db = 10 * math.log10(aa / bb)
    assert correlation > .999 and abs(db) < .1, (correlation, db)
    return {'audio_zero_lag_correlation': correlation,
            'audio_level_db_vs_master': db,
            'actual_rms': math.sqrt(aa / len(actual)),
            'master_rms': math.sqrt(bb / len(expected)),
            'compared_audio_samples_at_8khz': len(actual)}


def compare_audio(path, media_start, master_start, duration):
    expected = decode_audio(MASTER, master_start, duration)
    channels = [audio_metrics(decode_audio(path, media_start, duration, channel), expected)
                for channel in (0, 1)]
    return {'media_start_seconds': media_start,
            'master_start_seconds': master_start, 'duration_seconds': duration,
            **channels[0], 'channel_metrics': {'left': channels[0], 'right': channels[1]},
            'method': '8 kHz decoded per-channel zero-lag normalized correlation and RMS; original mono duplicated to stereo at unity.'}


def inspect(path, master_start, frames):
    info = require_video(path, frames, (1280, 720))
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    assert (int(audio['sample_rate']), audio['channels']) == (48000, 2), audio
    duration = frames / FPS
    assert abs(float(video_stream(info)['duration']) - duration) < 1 / 24000
    raw = run(['ffmpeg', '-v', 'error', '-xerror', '-err_detect', 'explode',
               '-i', str(path), '-an', '-vf', 'scale=64:36,format=gray',
               '-f', 'rawvideo', '-'])
    frame_size = 64 * 36
    assert len(raw) == frames * frame_size, (path, len(raw), frames)
    deviations = []
    for n in range(frames):
        row = raw[n * frame_size:(n + 1) * frame_size]
        mean = sum(row) / frame_size
        deviations.append(math.sqrt(max(0, sum(x * x for x in row) / frame_size - mean * mean)))
    near_uniform = [n for n, value in enumerate(deviations) if value <= 3]
    assert not near_uniform, ('Near-uniform frames', str(path), near_uniform)
    return {'path': relative(path), 'sha256': sha(path), 'frames': frames,
            'duration': duration, 'full_decode_pass': True,
            'near_uniform_frames': len(near_uniform),
            'near_uniform_frame_indices': near_uniform,
            'minimum_frame_sd': min(deviations),
            'blank_scan': 'Every decoded frame, 64x36 gray spatial standard deviation; fail at <=3.',
            **compare_audio(path, 0, master_start, duration), 'probe': info}


def contact(path, frames, target, columns):
    selected = '+'.join('eq(n\\,%d)' % frame for frame in frames)
    rows = math.ceil(len(frames) / columns)
    run(['ffmpeg', '-n', '-v', 'error', '-i', str(path), '-vf',
         f'select={selected},scale=640:360,tile={columns}x{rows}',
         '-frames:v', '1', '-update', '1', str(target)])
    return {'path': relative(target), 'sha256': sha(target),
            'source_path': relative(path), 'frames': frames,
            'tile_columns': columns, 'tile_rows': rows}


def main():
    for path, expected in FIXED_PINS.items():
        assert sha(path) == expected, 'Pinned input changed: ' + str(path)
    alignment_sha = sha(ALIGNMENT)
    alignment = json.loads(ALIGNMENT.read_text())
    frame = alignment['selected_source_in_frame']
    assert type(frame) is int and frame >= 0, frame
    restored_sha = sha(RESTORED)
    if 'source_sha256' in alignment:
        assert alignment['source_sha256'] == restored_sha, 'Alignment refers to a different restored source'
    if 'original_audio_sha256' in alignment:
        assert alignment['original_audio_sha256'] == FIXED_PINS[REFERENCE]
    restored_probe = require_video(RESTORED)
    restored_video = video_stream(restored_probe)
    assert restored_video['width'] * 9 == restored_video['height'] * 16, 'Unexpected aspect ratio; no crop/stretch authorized'
    assert frame + SCENE_FRAMES <= int(restored_video['nb_frames']), 'Insufficient real source picture; no freeze/pad/retime'
    require_video(TAIL, 1611, (1280, 720))
    require_video(P1, 711, (1280, 720))
    require_video(P2, 708, (1280, 720))
    scene_pcm = read_master_pcm(SCENE_MASTER_SAMPLE, SCENE_FRAMES * 2000)
    context_pcm = read_master_pcm(CONTEXT_MASTER_SAMPLE, CONTEXT_FRAMES * 2000)
    reference_pcm = verify_pcm(REFERENCE, scene_pcm)
    assert context_pcm[37 * 48000 * 2 + 30000 * 2:45 * 48000 * 2 + 30000 * 2] == scene_pcm

    hqa, cqa = H / 'qa', C / 'qa'
    hqa.mkdir(parents=True, exist_ok=True)
    cqa.mkdir(parents=True, exist_ok=True)
    output_paths = [hqa / 's17-c.mp4', cqa / 'context.mp4', hqa / 'VERIFICATION.json',
                    cqa / 'VERIFICATION.json', hqa / 'assembly-command.json',
                    cqa / 'assembly-command.json', hqa / 's17-c-source.wav',
                    cqa / 'context-source.wav', C / 'index.html',
                    hqa / 'encoded-contact.png', hqa / 'seam-contact.png',
                    hqa / 'encoded-0.png', hqa / 'encoded-96.png', hqa / 'encoded-191.png']
    assert not [str(p) for p in output_paths if p.exists()], 'Refuse to overwrite existing R76 outputs; inspect or move them explicitly'
    staged_scene = write_pcm(hqa / 's17-c-source.wav', scene_pcm)
    staged_context = write_pcm(cqa / 'context-source.wav', context_pcm)
    scene = hqa / 's17-c.mp4'
    context = cqa / 'context.mp4'
    encoding = ['-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-r', '24', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart']
    scene_command = ['ffmpeg', '-n', '-v', 'error', '-i', str(RESTORED),
                     '-i', str(hqa / 's17-c-source.wav'), '-filter_complex',
                     f'[0:v]trim=start_frame={frame}:end_frame={frame + SCENE_FRAMES},setpts=PTS-STARTPTS,scale=1280:720,setsar=1[v];'
                     '[1:a]pan=stereo|c0=c0|c1=c0[a]', '-map', '[v]', '-map', '[a]',
                     *encoding, str(scene)]
    save(hqa / 'assembly-command.json', scene_command)
    run(scene_command)
    context_command = ['ffmpeg', '-n', '-v', 'error', '-i', str(TAIL), '-i', str(P1),
                       '-i', str(scene), '-i', str(P2), '-i', str(cqa / 'context-source.wav'),
                       '-filter_complex',
                       '[0:v]trim=start_frame=0:end_frame=192,setpts=PTS-STARTPTS,setsar=1[v0];'
                       '[1:v]trim=start_frame=0:end_frame=711,setpts=PTS-STARTPTS,setsar=1[v1];'
                       '[2:v]trim=start_frame=0:end_frame=192,setpts=PTS-STARTPTS,setsar=1[v2];'
                       '[3:v]trim=start_frame=0:end_frame=708,setpts=PTS-STARTPTS,setsar=1[v3];'
                       '[v0][v1][v2][v3]concat=n=4:v=1:a=0[v];'
                       '[4:a]pan=stereo|c0=c0|c1=c0[a]',
                       '-map', '[v]', '-map', '[a]', *encoding, str(context)]
    save(cqa / 'assembly-command.json', context_command)
    run(context_command)

    scene_report = inspect(scene, 774.5, SCENE_FRAMES)
    context_report = inspect(context, 736.875, CONTEXT_FRAMES)
    context_presenter = compare_audio(context, 37.625, 774.5, 8.0)
    sheets = [contact(context, [0, 191, 192, 804, 901, 902, 903, 904,
                               951, 999, 1047, 1093, 1094, 1095, 1096, 1802],
                      hqa / 'encoded-contact.png', 2),
              contact(context, [902, 903, 904, 1094, 1095, 1096],
                      hqa / 'seam-contact.png', 3)]
    for n in [0, 96, 191]:
        target = hqa / f'encoded-{n}.png'
        run(['ffmpeg', '-n', '-v', 'error', '-i', str(scene), '-vf',
             f'select=eq(n\\,{n})', '-frames:v', '1', '-update', '1', str(target)])
        sheets.append({'path': relative(target), 'sha256': sha(target),
                       'source_path': relative(scene), 'frames': [n], 'native_resolution': [1280, 720]})
    player = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>EP007 — S17 presenter review</title>
<style>body{margin:0;background:#173530;color:#F5F0E6;font:17px/1.5 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:20px}h1{font-size:25px;margin:0 0 8px}video{display:block;width:100%;background:#000;margin:18px 0}nav{display:flex;flex-wrap:wrap;gap:10px}button,a{font:inherit}button{padding:9px 14px;background:#F5F0E6;color:#173530;border:0;cursor:pointer}a{color:#F5F0E6}blockquote{margin:18px 0;padding-left:18px;border-left:2px solid #71868D}.note{color:#F5F0E6;opacity:.85}</style></head><body><main>
<h1>EP007 — S17 presenter review</h1>
<p>The full review is 1:15.125. It opens at 0:33.500 so the preceding clause is audible.</p>
<video id="review" controls playsinline preload="metadata" src="qa/context.mp4"></video>
<nav aria-label="Review moments"><button data-time="33.5">Lead-in · 0:33.500</button><button data-time="37.625">Presenter · 0:37.625</button><button data-time="45.625">Return · 0:45.625</button></nav>
<blockquote>I am not going to name states, because the line moves and I am not your lawyer. That is a real piece of homework for wherever you are.</blockquote>
<p>The new eight-second take runs from 0:37.625 to 0:45.625. Review the delivery, mouth timing and the hand movement on “homework for wherever you are,” then the return to the fixed-fee explanation.</p>
<p class="note">Review candidate. Original recorded narration. <a href="qa/context.mp4">Open the full review video</a>.</p>
<script>const v=document.getElementById('review');v.addEventListener('loadedmetadata',()=>{v.currentTime=33.5;},{once:true});document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{v.currentTime=Number(b.dataset.time);v.play().catch(()=>{});}));</script>
</main></body></html>'''
    fresh_write(C / 'index.html', player)
    assert sha(RESTORED) == restored_sha and sha(ALIGNMENT) == alignment_sha, 'Dynamic input changed during assembly'
    for path, expected in FIXED_PINS.items():
        assert sha(path) == expected, 'Pinned input changed during assembly: ' + str(path)
    report = {
        'status': 'technical_pass_owner_review_pending',
        'source_pcm_bit_exact': True, 'source_prefix_pcm_bit_exact': True,
        'preserved_source_samples': 384000, 'context_source_samples': 3606000,
        'appended_zero_samples': 0, 'padding_seconds': 0,
        'strict_check': None, 'strict_check_note': 'FFmpeg assembly only; no HyperFrames source was authored or rendered.',
        'runtime': 'ffmpeg review assembly', 'source_sha256': restored_sha,
        'selected_source_in_frame': frame, 'selected_source_out_frame_exclusive': frame + 192,
        'alignment': {'path': relative(ALIGNMENT), 'sha256': alignment_sha,
                      'source_hash_explicit_in_alignment': 'source_sha256' in alignment},
        'fixed_inputs': [{'path': relative(p), 'sha256': digest} for p, digest in FIXED_PINS.items()],
        'source_pcm': {'provider_reference': reference_pcm, 'scene': staged_scene, 'context': staged_context},
        'scene': scene_report, 'context': context_report,
        'context_presenter_audio': context_presenter,
        'seams': {'s17_start_frame': 192, 'presenter_start_frame': 903,
                  'presenter_end_frame_exclusive': 1095, 'review_initial_time_seconds': 33.5},
        'contact_sheets_and_native_stills': sheets,
        'review_player': {'path': relative(C / 'index.html'), 'sha256': sha(C / 'index.html')},
        'assembler': {'path': relative(Path(__file__).resolve()), 'sha256': sha(Path(__file__).resolve())},
        'commands': COMMANDS,
        'limits': ['No owner acceptance, canonical conform or release.',
                   'Audio metrics do not establish perceptual lip sync or performance quality.',
                   'Source PCM checks apply to staged WAV inputs; encoded AAC is lossy.',
                   'Near-uniform-frame scan detects technical blanks, not every visual defect.',
                   'Review assembly re-encodes accepted picture without changing cuts or timing.']}
    save(hqa / 'VERIFICATION.json', report)
    save(cqa / 'VERIFICATION.json', report)
    print(json.dumps({'status': report['status'], 'scene': scene_report['path'],
                      'context': context_report['path'], 'scene_frames': 192,
                      'context_frames': 1803, 'review_player': relative(C / 'index.html'),
                      'verification': relative(hqa / 'VERIFICATION.json')}, indent=2))


if __name__ == '__main__':
    main()
