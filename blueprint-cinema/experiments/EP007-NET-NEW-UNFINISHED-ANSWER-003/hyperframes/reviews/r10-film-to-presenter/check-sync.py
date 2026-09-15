"""Measure exact audio provenance, not visual lip-sync quality."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np

def pcm(p, rate=16000):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar',str(rate),'-f','f32le','pipe:1']),dtype='<f4').astype(np.float64)

x=pcm('public/audio/presenter-introduction.wav')
y=pcm('public/media/presenter-introduction-q.mp4')
checks=[]
for start,end in [(1,7),(10,16),(19,25)]:
    a=x[int(start*16000):int(end*16000)];a=a-a.mean()
    scores=[]
    for lag in range(-1600,1601):
        b=y[int(start*16000)+lag:int(end*16000)+lag]
        if len(b)!=len(a):continue
        b=b-b.mean();score=float(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)))
        scores.append((score,lag))
    score,lag=max(scores)
    checks.append({'inputWindow':[start,end],'delaySeconds':lag/16000,'correlation':score})
assert min(c['correlation'] for c in checks)>.98, checks
assert max(c['delaySeconds'] for c in checks)-min(c['delaySeconds'] for c in checks)<.002,checks
result={'status':'audio-provenance-and-timing-passed','checks':checks,'medianDelaySeconds':float(np.median([c['delaySeconds'] for c in checks])),'visualLipSyncApproved':False,'note':'Positive delay means provider audio occurs later than input. Advance muted picture source by this offset when using continuous master audio.'}
Path('renders/intro-audio-sync.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
