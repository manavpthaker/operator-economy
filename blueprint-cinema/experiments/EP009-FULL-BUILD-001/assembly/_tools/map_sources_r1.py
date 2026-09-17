import json, hashlib, subprocess, os, sys
ROOT='/Users/brownmanbrain/GitHub/operator-economy'
B=ROOT+'/blueprint-cinema/experiments/EP009-FULL-BUILD-001'
plan=json.load(open(B+'/direction/SHOT-PLAN.json'))
def load(f): return json.load(open(B+'/'+f))['segments']
pres=load('presenter/INDEX.json'); film=load('film/INDEX.json')
acts={}
for n in range(1,5):
    for k,v in load(f'scenes/act{n}-models-INDEX.json').items(): acts[k]=(f'scenes/act{n}-models-INDEX.json',v)
rows=[]; problems=[]
for s in plan['segments']:
    sid=s['id']; f0,f1=s['frames']; n=f1-f0
    if sid in acts:
        idxf,e=acts[sid]; path=e['mp4']; start=(e.get('frame_range_in_mp4') or e.get('frame_range'))[0]; nf=e['frames']
    elif sid in pres:
        idxf,e='presenter/INDEX.json',pres[sid]; path=e['path']; start=0; nf=e['frames']
    elif sid in film and film[sid].get('path'):
        idxf,e='film/INDEX.json',film[sid]; path=e['path']; start=0; nf=e['frames']
    else:
        problems.append(f'{sid}: no source'); continue
    if nf!=n: problems.append(f'{sid}: index frames {nf} != plan {n}')
    rows.append(dict(id=sid,scene=s['scene'],lane=s['lane'],index=idxf,take_id=e.get('take_id') or s.get('take_id'),path=path,sha256=e['sha256'],src_start=start,frames=n,out=[f0,f1],master_in=s['master_in'],master_out=s['master_out'],index_status=e.get('status')))
# verify sha + probe
cache={}
for r in rows:
    p=r['path']
    if p not in cache:
        h=hashlib.sha256(open(ROOT+'/'+p,'rb').read()).hexdigest()
        pr=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_packets','-show_entries','stream=width,height,r_frame_rate,nb_read_packets,sample_aspect_ratio,pix_fmt','-of','json',ROOT+'/'+p]))['streams'][0]
        cache[p]=(h,pr)
    h,pr=cache[p]
    r['sha_ok']=(h==r['sha256']); r['probe']=pr
    if not r['sha_ok']: problems.append(f"{r['id']}: SHA MISMATCH {p} actual {h}")
    if r['src_start']+r['frames']>int(pr['nb_read_packets']): problems.append(f"{r['id']}: source shortfall need {r['src_start']+r['frames']} have {pr['nb_read_packets']}")
    if (pr['width'],pr['height'],pr['r_frame_rate'])!=(1280,720,'24/1'): problems.append(f"{r['id']}: format {pr}")
# contiguity check within shared mp4s
by={}
for r in rows: by.setdefault(r['path'],[]).append(r)
notes=[]
for p,rs in by.items():
    for a,b in zip(rs,rs[1:]):
        if a['out'][1]==b['out'][0] and a['src_start']+a['frames']!=b['src_start']:
            problems.append(f"{a['id']}->{b['id']}: shared source not contiguous")
    notes.append((p.split('/')[-1],rs[0]['src_start'],sum(x['frames'] for x in rs),cache[p][1]['nb_read_packets']))
# plan contiguity
for a,b in zip(rows,rows[1:]):
    if a['out'][1]!=b['out'][0]: problems.append(f"gap {a['id']} {b['id']}")
json.dump(rows,open(B+'/assembly/_tools/sources-r1.json','w'),indent=1)
print(len(rows),'rows; total frames',rows[-1]['out'][1])
for n in notes: print(n)
print('PROBLEMS', problems)
