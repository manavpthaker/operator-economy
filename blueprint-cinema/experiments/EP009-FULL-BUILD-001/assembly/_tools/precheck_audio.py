import json, subprocess, numpy as np
ROOT='/Users/brownmanbrain/GitHub/operator-economy'
B=ROOT+'/blueprint-cinema/experiments/EP009-FULL-BUILD-001'
MASTER=ROOT+'/operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
def dec(p, ss=None, t=None):
    cmd=['ffmpeg','-v','error']
    cmd+=['-i',p]
    af='aresample=48000'
    cmd+=['-map','0:a:0','-ac','1','-af',af,'-f','f32le','-']
    return np.frombuffer(subprocess.check_output(cmd),dtype=np.float32)
m=dec(MASTER); print('master samples',len(m))
rows=json.load(open(B+'/assembly/_tools/sources.json'))
cache={}; out=[]
for r in rows:
    p=ROOT+'/'+r['path']
    if p not in cache:
        try: cache[p]=dec(p)
        except Exception as e: cache[p]=None
    a=cache[p]
    if a is None: out.append((r['id'],'no audio')); continue
    s0=r['src_start']*2000; n=r['frames']*2000; m0=r['out'][0]*2000
    x=a[s0:s0+n]; y=m[m0:m0+n]; k=min(len(x),len(y)); x=x[:k]; y=y[:k]
    c=float(np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y)+1e-12))
    # best lag within +/-0.6 s coarse
    best=(c,0)
    if c<0.99:
        for lag in range(-28800,28801,48):
            lo=m0+lag
            if lo<0: continue
            yy=m[lo:lo+k]
            if len(yy)<k: continue
            cc=float(np.dot(x,yy)/np.sqrt(np.dot(x,x)*np.dot(yy,yy)+1e-12))
            if cc>best[0]: best=(cc,lag)
    out.append((r['id'],r['lane'],round(c,5),best[1],round(best[0],5)))
for o in out: print(o)
json.dump(out,open(B+'/assembly/_tools/precheck_audio.json','w'),indent=1)
