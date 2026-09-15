"""Verify Test J geometry, complete decode, and exact preservation of G's audio."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4'
OUTPUT = ROOT / 'media/repair-r10/test-j-landscape-study-blended-1080p.mp4'

def run(*args):
    return subprocess.check_output(args)

def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def audio(path, encoded):
    options = ['-c:a', 'copy', '-f', 'adts'] if encoded else ['-f', 's16le', '-acodec', 'pcm_s16le']
    return run('ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', *options, '-')

pcm = audio(OUTPUT, False)
aac = audio(OUTPUT, True)
assert pcm == audio(SOURCE, False)
assert aac == audio(SOURCE, True)
probe = json.loads(run('ffprobe', '-v', 'error', '-count_frames', '-show_streams',
                      '-show_format', '-of', 'json', str(OUTPUT)))
video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
sound = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
assert int(video['nb_read_frames']) == 765
assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '25/1')
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(OUTPUT), '-f', 'null', '-'], check=True)
foreground = json.loads((ROOT / 'repair-r10/foreground-qa.json').read_text())
assert foreground['rgb24_frame_hashes_and_timestamps_equal_g_crop']
report = {
    'status': 'technical_pass_owner_playback_pending',
    'output': str(OUTPUT.relative_to(ROOT)), 'sha256': sha(OUTPUT),
    'bytes': OUTPUT.stat().st_size, 'source_g_sha256': sha(SOURCE),
    'picture': {'width': 1920, 'height': 1080, 'fps': '25/1', 'frames': 765,
                'duration_seconds': float(video['duration'])},
    'audio': {'duration_seconds': float(sound['duration']), 'sample_rate': sound['sample_rate'],
              'channels': sound['channels'], 'aac_bitstream_equals_g': True,
              'decoded_pcm_equals_g': True, 'pcm_sha256': hashlib.sha256(pcm).hexdigest(),
              'aac_sha256': hashlib.sha256(aac).hexdigest(),
              'preserved_source_lag_to_locked_wav_ms': 23.020833},
    'container_duration_seconds': float(probe['format']['duration']),
    'full_decode_pass': True, 'foreground_qa': 'foreground-qa.json',
    'composition_sha256': sha(ROOT / 'study-composite-r10/index.html'),
    'motion_asset_sha256': sha(ROOT / 'study-composite-r10/assets/shirt-motion.js'),
    'limits': ['Full composite is resized and H264 encoded, not pixel-identical to G.',
               'Study and outer shoulders are synthetic; outer shoulders follow measured shirt motion.',
               'A rigid outer-shirt transform cannot reproduce all fabric deformation.',
               'This technical pass does not approve acting, full composite naturalness, or episode placement.'],
    'canonical_gates_changed': []}
(ROOT / 'repair-r10/technical-review.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
