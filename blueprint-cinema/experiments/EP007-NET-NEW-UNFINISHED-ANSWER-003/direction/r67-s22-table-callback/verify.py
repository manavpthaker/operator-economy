#!/usr/bin/env python3
"""Bounded technical checks for the S22 timing plan, not generated performance."""
from pathlib import Path
import array,hashlib,json,math,subprocess,wave
ROOT=Path(__file__).resolve().parents[5]
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
H=EXP/'hyperframes/reviews/r67-s22-plan'
C=EXP/'hyperframes/reviews/r67-s22-context'
MASTER=ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
def run(c): return subprocess.run(c,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def audio(p,start,dur):
 a=array.array('f');a.frombytes(run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(dur),'-vn','-af','pan=mono|c0=c0','-ar','8000','-f','f32le','-']))
 return a
def inspect(p,start,frames):
 probe=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels','-of','json',str(p)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'24/1',frames)
 raw=run(['ffmpeg','-v','error','-xerror','-i',str(p),'-an','-vf','scale=64:36,format=gray','-f','rawvideo','-'])
 size=64*36;assert len(raw)==frames*size
 sd=[]
 for n in range(frames):
  row=raw[n*size:(n+1)*size];m=sum(row)/size
  sd.append(math.sqrt(max(0,sum(x*x for x in row)/size-m*m)))
 assert min(sd)>3
 a=audio(p,0,frames/24);b=audio(MASTER,start,frames/24);n=min(len(a),len(b));a=a[:n];b=b[:n]
 aa=sum(x*x for x in a);bb=sum(x*x for x in b);ab=sum(x*y for x,y in zip(a,b))
 corr=ab/math.sqrt(aa*bb);db=10*math.log10(aa/bb)
 assert corr>.999 and abs(db)<.1,(corr,db)
 return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'frames':frames,'duration':frames/24,'minimum_frame_sd':min(sd),'near_uniform_frames':sum(s<3 for s in sd),'audio_zero_lag_correlation':corr,'audio_level_db_vs_master':db,'probe':probe}
with wave.open(str(MASTER),'rb') as src:
 src.setpos(25130*2000);expected=src.readframes(524*2000)
with wave.open(str(H/'public/audio/narration.wav'),'rb') as out: actual=out.readframes(out.getnframes())
assert actual==expected
check=json.loads((H/'qa/check.json').read_text());assert check['ok']
report={'status':'technical_pass_timing_animatic_only','runtime':'0.8.46','strict_check':True,'pcm_bit_exact':True,'source_sha256':sha(H/'index.html'),'master_sha256':sha(MASTER),
 'scene':inspect(H/'qa/s22-plan.mp4',25130/24,524),'context':inspect(C/'qa/context.mp4',24938/24,716),
 'paid_calls':0,'limitations':['New binder actions are labeled static references and have not been generated.',
 'Technical audio alignment is not a listening verdict.','No owner acceptance of S22 direction or footage; no release or canonical conform.']}
(H/'qa/VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['scene','context']},indent=2))
for key in ['scene','context']: print(key,json.dumps({k:v for k,v in report[key].items() if k!='probe'}))

