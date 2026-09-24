"""Read-only source QA; diagnostics are generated only in this packet."""
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[6]
PACKET = Path(__file__).resolve().parent
ORDER = ROOT / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/ep007-r11-avatar-qa-20260909.json'
DIAG = PACKET / 'diagnostics'
DIAG.mkdir(exist_ok=True)
order = json.loads(ORDER.read_text())
for item in order['inputs']:
    actual = hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest()
    assert actual == item['sha256'], (item['path'], actual)

def pcm(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar','16000','-f','f32le','pipe:1']),dtype='<f4').astype('float64')

source = ROOT / order['inputs'][0]['path']
reference = ROOT / order['inputs'][1]['path']
x, y = pcm(reference), pcm(source)
rate = 16000
results = []
for st, en in [(0.3,2.0),(2.0,4.041667),(4.1,6.1),(6.666667,8.6),(8.6,11.083333)]:
    start, end = round(st*rate), round(en*rate)
    a = x[start:end]; a = a - a.mean()
    pad = 1600
    region = y[start-pad:end+pad]
    score = np.correlate(region, a, mode='valid')
    sums = np.concatenate(([0],np.cumsum(region)))
    squares = np.concatenate(([0],np.cumsum(region**2)))
    n = len(a)
    centered_energy = squares[n:] - squares[:-n] - (sums[n:] - sums[:-n])**2/n
    score /= np.sqrt(np.maximum(centered_energy, 1e-15) * np.dot(a,a))
    best = int(np.argmax(score))
    results.append({'reference_seconds':[st,en], 'best_lag_samples_16000hz':best-pad,'best_lag_seconds':(best-pad)/rate,'correlation':float(score[best]),'zero_lag_correlation':float(score[pad])})
probes = []
for item in order['inputs']:
    probes.append(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(ROOT/item['path'])])))
decode = subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(source),'-f','null','-'],capture_output=True,text=True)
report = {'input_hashes_match':True, 'probes':probes, 'audio_alignment':results,'decoded_pcm_samples_at_16000hz':{'reference':len(x),'output':len(y)},'full_decode':{'returncode':decode.returncode,'stderr':decode.stderr},'note':'Audio preservation and timeline alignment only; no automated phoneme-fidelity claim.'}
(DIAG/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'alignment':results,'decode':decode.returncode},indent=2))
