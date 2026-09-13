"""Check returned audio against the approved seven-second voice, without altering it."""
import hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
source = BASE.parent / 'media/test-01/test01-original-c.wav'
video = Path(sys.argv[1]).resolve()
assert BASE in video.parents

def decoded(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']), dtype='<f4').astype(float)

def match(ref, output, maxlag=6400):
    n=min(len(ref),len(output)); ref=ref[:n]; output=output[:n]
    size=1 << (2*n-1).bit_length()
    x=np.fft.irfft(np.fft.rfft(output,size)*np.conj(np.fft.rfft(ref,size)),size)
    lags=np.arange(-min(maxlag,n-1),min(maxlag,n-1)+1)
    lag=int(lags[np.argmax(x[lags % size])])
    if lag >= 0: a,b=ref[:n-lag],output[lag:n]
    else: a,b=ref[-lag:n],output[:n+lag]
    return {'lag_seconds':lag/16000,'correlation':float(np.corrcoef(a,b)[0,1])}

a,b=decoded(source),decoded(video)
windows=[]
for start,end in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6.07)]:
    windows.append({'start':start,'end':end,**match(a[round(start*16000):round(end*16000)],b[round(start*16000):round(end*16000)],1600)})
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'source_audio_seconds':len(a)/16000,'output_audio_seconds':len(b)/16000,'global_audio':match(a,b),'speech_windows':windows,'probe':probe,'limits':'Audio correlation measures preservation of the supplied voice clock. It does not establish visual lip sync, moving likeness, or owner acceptance.'}
((video.parent.parent if video.parent.name=='media' else video.parent)/'AUDIO-QA.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='probe'},indent=2))
