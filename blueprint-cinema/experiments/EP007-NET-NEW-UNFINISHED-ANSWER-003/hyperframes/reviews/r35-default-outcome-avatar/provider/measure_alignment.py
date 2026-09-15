"""Measure original-narration insertion in the actual returned container."""
from pathlib import Path
import json, subprocess, hashlib
import numpy as np

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
source = BASE / 'restoration/restored.mp4'
auth = json.loads((BASE / 'GENERATION-AUTHORIZATION.json').read_text())
audio_ref = next(x for x in auth['inputs'] if x['path'].endswith('.wav'))
original = REPO / audio_ref['path']
assert hashlib.sha256(original.read_bytes()).hexdigest() == audio_ref['sha256']
rate = 16000
def decode(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-']), dtype='<f4').astype(float)
ref = decode(original)
actual = decode(source)
def compare(lo, hi):
    start, stop = round(lo*rate), round(hi*rate)
    target = ref[start:stop]
    n = len(actual)+len(target)-1
    fftn = 1 << (n-1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(actual,fftn)*np.fft.rfft(target[::-1],fftn),fftn)[:n]
    conv = corr[len(target)-1:len(actual)]
    power = np.r_[0,np.cumsum(actual*actual)]
    target_power = np.dot(target,target)
    window_power = np.maximum(power[len(target):]-power[:-len(target)],0)
    denom = np.sqrt(np.maximum(window_power,1e-12)*target_power)
    scores = conv/denom
    # FFT roundoff over digital silence must not become an apparent match.
    scores[window_power < target_power*.001] = -1
    index = int(np.argmax(scores))
    return {'reference_window_seconds':[lo,hi], 'source_window_start_seconds':index/rate,'offset_seconds':(index-start)/rate,'correlation':float(scores[index])}
rows = [compare(.3,1.3),compare(1.65,2.65),compare(3.45,4.5)]
offset = float(np.median([r['offset_seconds'] for r in rows]))
assert min(r['correlation'] for r in rows) > .97, rows
assert max(r['offset_seconds'] for r in rows)-min(r['offset_seconds'] for r in rows) <= .01, rows
frame = round(offset*24)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)]))
duration=float(probe['format']['duration'])
assert frame >= 0 and frame/24 + 5 <= duration + 1/24
result={'method':'Independent early/middle/late waveform cross-correlation at 16 kHz against exact original source. Nearest 24 fps picture frame.', 'measurements':rows,'measured_offset_seconds':offset,'selected_source_in_frame':frame,'selected_source_in_seconds':frame/24,'frame_rounding_error_seconds':frame/24-offset,'source_duration_seconds':duration,'output_frames':120,'output_duration_seconds':5,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_audio_sha256':audio_ref['sha256'],'limitations':'Container waveform alignment does not certify perceptual lip sync, facial expression, or audience comprehension. Those require visual and audiovisual review.'}
(BASE/'ALIGNMENT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
