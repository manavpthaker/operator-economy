import json
ROOT='/Users/brownmanbrain/GitHub/operator-economy'
B=ROOT+'/blueprint-cinema/experiments/EP009-FULL-BUILD-001'
MASTER=ROOT+'/operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
rows=json.load(open(B+'/assembly/_tools/sources-r1.json'))
paths=[]
for r in rows:
    if r['path'] not in paths: paths.append(r['path'])
uses={p:[r for r in rows if r['path']==p] for p in paths}
total=rows[-1]['out'][1]
lines=[]
for i,p in enumerate(paths):
    n=len(uses[p])
    if n>1: lines.append(f"[{i}:v:0]split={n}"+''.join(f"[s{i}_{k}]" for k in range(n)))
lbl={}
cnt={}
for j,r in enumerate(rows):
    i=paths.index(r['path']); k=cnt.get(i,0); cnt[i]=k+1
    src=f"[s{i}_{k}]" if len(uses[r['path']])>1 else f"[{i}:v:0]"
    a=r['src_start']; b=a+r['frames']
    lines.append(f"{src}trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,scale=1280:720,setsar=1,format=yuv420p[v{j}]")
lines.append(''.join(f"[v{j}]" for j in range(len(rows)))+f"concat=n={len(rows)}:v=1:a=0,fps=24[vout]")
mi=len(paths)
lines.append(f"[{mi}:a:0]pan=stereo|c0=c0|c1=c0,apad=whole_len={total*2000},atrim=end_sample={total*2000},asetpts=N/SR/TB[aout]")
open(B+'/assembly/_tools/graph-r1.txt','w').write(';\n'.join(lines))
args=[]
for p in paths: args+=['-i',ROOT+'/'+p]
args+=['-i',MASTER]
json.dump(args,open(B+'/assembly/_tools/inputs-r1.json','w'))
print(len(paths),'inputs', total,'frames', total*2000,'samples')
