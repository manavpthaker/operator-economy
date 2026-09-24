import sys,json,subprocess,numpy as np
sys.path.insert(0,'_tools'); import pres
def act(x,thr_db=-40):
    e=pres.env(x); db=20*np.log10(e+1e-9); pk=np.percentile(db,99); a=db>pk-30
    # speech runs: smooth
    idx=np.where(a)[0]; return idx
out={}
for tid in sys.argv[1:]:
    t=pres.TAKES[tid]; d=pres.td(tid)
    nar=pres.pcm(d/'audio/narration.wav'); nv=pres.pcm(d/'native.mp4')
    a=act(nar); b=act(nv)
    # word-based narration onset/offset in excerpt time
    on_n=a[0]/100; off_n=a[-1]/100; on_v=b[0]/100; off_v=b[-1]/100
    # sentence-level: pauses >250ms in narration and native
    def runs(idx):
        r=[];s=idx[0];p=idx[0]
        for i in idx[1:]:
            if i-p>25: r.append((s/100,p/100)); s=i
            p=i
        r.append((s/100,p/100)); return r
    rn=runs(a); rv=runs(b)
    out[tid]={'narration_onset':on_n,'native_onset':on_v,'onset_diff':round(on_v-on_n,2),'narration_end':off_n,'native_end':off_v,'end_diff':round(off_v-off_n,2),'narr_phrases':len(rn),'native_phrases':len(rv),'narr_runs':[(round(x,2),round(y,2)) for x,y in rn],'native_runs':[(round(x,2),round(y,2)) for x,y in rv]}
    print(tid, out[tid]['onset_diff'], out[tid]['end_diff'], 'speech span narr',round(off_n-on_n,2),'native',round(off_v-on_v,2), 'phrases',len(rn),len(rv))
json.dump(out,open('_tools/onsets-out.json','w'),indent=1)
