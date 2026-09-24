import json,wave,numpy as np,sys
def load(p,a=0,b=None):
    w=wave.open(p);r=w.getframerate();w.setpos(int(a*r));n=w.getnframes()-int(a*r) if b is None else int((b-a)*r)
    return np.frombuffer(w.readframes(n),np.int16).astype(float),r
def env(x,win=480): return 20*np.log10(np.sqrt(np.convolve(x**2,np.ones(win)/win,'same'))/32768+1e-9)
def sil(x,th=-45,minlen=.05):
    q=env(x)<th;d=np.diff(np.r_[0,q.astype(int),0]);s=np.where(d==1)[0];e=np.where(d==-1)[0]
    return [(round(a/48000,3),round(b/48000,3)) for a,b in zip(s,e) if (b-a)/48000>minlen]
d=json.load(open('asr.json'))
print(' '.join(f"{s['text'].strip()}@{s['offsets']['from']/1000:.2f}" for s in d['transcription'] if s['text'].strip()))
x,_=load('context-original-c.wav')
print('pickup silences',sil(x))
def lvl(v): return 20*np.log10(np.sqrt((v**2).mean())/32768)
print('pickup rms(active)',lvl(x[env(x)>-40]))
M='/Users/brownmanbrain/GitHub/operator-economy/operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
m,_=load(M,453.9,461.6)
print('master silences (from 453.9)',[(round(a+453.9,3),round(b+453.9,3)) for a,b in sil(m)])
print('master rms(active)',lvl(m[env(m)>-40]))
