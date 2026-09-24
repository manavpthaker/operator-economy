from pathlib import Path
import array, hashlib, json, math, subprocess, wave
ROOT=Path('/Users/brownmanbrain/GitHub/operator-economy')
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
OUT=ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R70-S23-FINAL-QC'
H=EXP/'hyperframes/reviews/r70-s23-payoff'; C=EXP/'hyperframes/reviews/r70-s23-context'
EP=ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep'
M=EP/'02-narration-production/master/narration-master.v4.wav'
def run(cmd): return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={str(H/'index.html'):'04e59492d6da09c6ebc0e67446721b143379ff4515dfb4e425295135d37a15b2',str(H/'qa/s23.mp4'):'1997e7cafe1ffd05ce261b09be5950091727057093d631b9e6e8682a457178e5',str(C/'qa/context.mp4'):'bf1a79cbb756936c08a2bd579b7376fbf75a5b43ff09d5f9f4f8a5cea37da19a',str(M):'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9',str(EP/'01-editorial/script.md'):'e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0',str(EP/'02-narration-production/word-transcript.json'):'f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7'}
pins=[]
for name,e in expected.items():
 p=Path(name);actual=sha(p);assert actual==e,(name,actual);pins.append({'path':str(p.relative_to(ROOT)),'sha256':actual})
for p in [EXP/'direction/r70-s23-payoff/finish.py',EXP/'direction/r70-s23-payoff/DIRECTION.md',H/'public/audio/narration.wav',EXP/'hyperframes/reviews/r69-s22-film/qa/s22.mp4']:
 pins.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
with wave.open(str(M),'rb') as w:
 master_format=(w.getnchannels(),w.getsampwidth(),w.getframerate());w.setpos(51308000);src=w.readframes(460000)
with wave.open(str(H/'public/audio/narration.wav'),'rb') as w:
 staged_format=(w.getnchannels(),w.getsampwidth(),w.getframerate());staged=w.readframes(w.getnframes())
assert staged_format==master_format==(1,2,48000)
assert src==staged

def mono(p,start,dur,rate=8000):
 raw=run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(dur),'-vn','-af','pan=mono|c0=c0','-ar',str(rate),'-f','f32le','-'])
 a=array.array('f');a.frombytes(raw);return a

def corr(a,b):
 n=min(len(a),len(b));a=a[:n];b=b[:n];aa=sum(v*v for v in a);bb=sum(v*v for v in b);ab=sum(x*y for x,y in zip(a,b))
 return {'sample_count':n,'correlation':ab/math.sqrt(aa*bb),'level_difference_db':10*math.log10(aa/bb)}

def frames(p):
 raw=run(['ffmpeg','-v','error','-xerror','-i',str(p),'-an','-vf','scale=32:18,format=gray','-fps_mode','passthrough','-f','rawvideo','-'])
 assert len(raw)%576==0
 return [raw[i:i+576] for i in range(0,len(raw),576)]

sc=frames(H/'qa/s23.mp4');co=frames(C/'qa/context.mp4');assert len(sc)==230 and len(co)==422
metrics={}
for name,p,expectedframes,start,f in [('scene',H/'qa/s23.mp4',230,25654/24,sc),('context',C/'qa/context.mp4',422,25462/24,co)]:
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration,sample_rate,channels','-of','json',str(p)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',expectedframes)
 sd=[math.sqrt(sum((x-sum(row)/576)**2 for x in row)/576) for row in f]
 a=corr(mono(p,0,expectedframes/24),mono(M,start,expectedframes/24))
 assert a['correlation']>.999 and abs(a['level_difference_db'])<.1
 assert min(sd)>3
 metrics[name]={'probe':probe,'decoded_frames':len(f),'near_uniform_frames':sum(x<3 for x in sd),'minimum_frame_sd':min(sd),'audio':a}
seam=corr(mono(C/'qa/context.mp4',7.75,.5,48000),mono(M,25654/24-.25,.5,48000))
assert seam['correlation']>.999 and abs(seam['level_difference_db'])<.1
# First/last/transition scene frames must remain ordered and visually match the embedded context.
comparison=[]
for n in [0,1,89,90,91,95,96,97,132,193,229]:
 mae=sum(abs(x-y) for x,y in zip(sc[n],co[n+192]))/576
 comparison.append({'scene_frame':n,'context_frame':n+192,'mean_absolute_gray_difference':mae})
 assert mae<2
out={'status':'independent_technical_pass','input_hashes_used':pins,'pcm_bit_exact':True,'pcm_format':staged_format,'staged_samples':len(staged)//2,'scene':metrics['scene'],'context':metrics['context'],'seam_audio_7_75_to_8_25':seam,'scene_to_context_selected_frame_matches':comparison,'limits':['No continuous normal-speed listening verdict.','Metrics and sampled images do not establish owner acceptance.','S22 was already owner locked; this audit checks its selected lead-in and seam only.']}
(OUT/'technical-qc.json').write_text(json.dumps(out,indent=2)+'\n')
# Compact full-resolution seam/cue image for direct independent inspection.
selected=[191,192,281,282,283,287,288,421]
expr='+'.join('eq(n\\,%d)'%n for n in selected)
run(['ffmpeg','-y','-v','error','-i',str(C/'qa/context.mp4'),'-vf',f'select={expr},scale=640:360,tile=2x4','-frames:v','1',str(OUT/'seam-and-cues.png')])
(OUT/'seam-and-cues-index.json').write_text(json.dumps(selected)+'\n')
print(json.dumps({k:out[k] for k in ['status','pcm_bit_exact','staged_samples','seam_audio_7_75_to_8_25','scene_to_context_selected_frame_matches']},indent=2))
print(json.dumps({k:{'frames':v['decoded_frames'],'minimum_frame_sd':v['minimum_frame_sd'],'audio':v['audio']} for k,v in metrics.items()},indent=2))
