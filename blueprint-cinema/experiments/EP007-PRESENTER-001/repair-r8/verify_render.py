"""Verify the review render and preservation of the source audio."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4'
OUTPUT = ROOT / 'media/repair-r8/test-h-landscape-study-1080p.mp4'

def run(*args):
    return subprocess.check_output(args)

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def pcm(path):
    return run('ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
               '-f', 's16le', '-acodec', 'pcm_s16le', '-')

def aac(path):
    return run('ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
               '-c:a', 'copy', '-f', 'adts', '-')

source_pcm, output_pcm = pcm(SOURCE), pcm(OUTPUT)
source_aac, output_aac = aac(SOURCE), aac(OUTPUT)
probe = json.loads(run('ffprobe', '-v', 'error', '-count_frames', '-show_streams',
                      '-show_format', '-of', 'json', str(OUTPUT)))
video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
audio = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(OUTPUT), '-f', 'null', '-'], check=True)
assert int(video['nb_read_frames']) == 765
assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '25/1')
assert source_pcm == output_pcm
assert source_aac == output_aac

report = {
    'status': 'technical_pass_owner_playback_pending',
    'output': str(OUTPUT.relative_to(ROOT)), 'sha256': sha(OUTPUT),
    'bytes': OUTPUT.stat().st_size,
    'source_g_sha256': sha(SOURCE),
    'picture': {'width': 1920, 'height': 1080, 'fps': '25/1', 'frames': 765,
                'duration_seconds': float(video['duration'])},
    'audio': {'duration_seconds': float(audio['duration']), 'sample_rate': audio['sample_rate'],
              'channels': audio['channels'], 'aac_bitstream_equals_g': True,
              'decoded_pcm_equals_g': True, 'pcm_sha256': hashlib.sha256(output_pcm).hexdigest(),
              'aac_sha256': hashlib.sha256(output_aac).hexdigest(),
              'preserved_source_lag_to_locked_wav_ms': 23.020833},
    'container_duration_seconds': float(probe['format']['duration']),
    'full_decode_pass': True,
    'foreground_asset_independent_qa': 'All 765 pre-composition VP9 foreground frames match G crop in RGB24 and YUV420, same order and timestamps; see worker parent-alpha-independent-qa.json.',
    'limits': ['Full composite is resized and H264 encoded, not pixel-identical to G.',
               'Study and static outer shoulders are synthetic.',
               'Small light edge fringe and moving/static shirt texture mismatch remain.',
               'This technical pass does not approve acting, full composite naturalness, or episode placement.'],
    'canonical_gates_changed': [],
}
destination = ROOT / 'repair-r8/technical-review.json'
destination.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
