#!/usr/bin/env python3
"""Read final R69 files; write independent QC evidence only inside this directory."""
from pathlib import Path
import array, hashlib, json, math, subprocess, statistics, wave
from html.parser import HTMLParser
ROOT=Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT=Path(__file__).resolve().parent
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
D=EXP/'direction/r69-s22-written-record-retry'
H=EXP/'hyperframes/reviews/r69-s22-film'; C=EXP/'hyperframes/reviews/r69-s22-context'
MASTER=ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
def run(args):return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,sample_rate,channels','-of','json',str(p)]))
def frames(p):
 data=run(['ffmpeg','-v','error','-xerror','-i',str(p),'-an','-vf','scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,scale=64:36,format=gray','-fps_mode','passthrough','-f','rawvideo','-'])
 assert len(data)%2304==0
 return [data[i:i+2304] for i in range(0,len(data),2304)]
def rmse(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b))/len(a))
def stats(rows):
 return {'min':min(rows),'median':statistics.median(rows),'max':max(rows),'mean':statistics.mean(rows)}
def audio(p,start,duration,channel=0):
 raw=run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(duration),'-vn','-af',f'pan=mono|c0=c{channel}','-ar','8000','-f','f32le','-'])
 return array.array('f',raw)
def audio_compare(p,master_start,frame_count):
 a=audio(p,0,frame_count/24);b=audio(MASTER,master_start,frame_count/24);n=min(len(a),len(b));a=a[:n];b=b[:n]
 aa=sum(x*x for x in a);bb=sum(x*x for x in b);ab=sum(x*y for x,y in zip(a,b))
 return {'samples_compared_at_8khz':n,'zero_lag_correlation':ab/math.sqrt(aa*bb),'level_db_vs_master':10*math.log10(aa/bb),'rmse':math.sqrt(sum((x-y)**2 for x,y in zip(a,b))/n)}
scene=H/'qa/s22.mp4';context=C/'qa/context.mp4';selection=json.loads((D/'SELECTION.json').read_text())
result={'review_scope':'Independent technical timing/audio/mapping checks; human comprehension and source claims reviewed separately.','hashes':{str(p.relative_to(ROOT)):sha(p) for p in [D/'build.py',D/'finish.py',D/'SELECTION.json',H/'index.html',scene,context,MASTER]},'scene_probe':probe(scene),'context_probe':probe(context)}
scene_frames=frames(scene);context_frames=frames(context)
result['decoded_frames']={'scene':len(scene_frames),'context':len(context_frames)}
for name,fs in [('scene',scene_frames),('context',context_frames)]:
 deviations=[]
 for f in fs:
  mean=sum(f)/len(f);deviations.append(math.sqrt(max(0,sum(x*x for x in f)/len(f)-mean*mean)))
 result[name+'_frame_variation']={'sd_summary':stats(deviations),'near_uniform_frames_below_sd3':[i for i,x in enumerate(deviations) if x<3]}
 delta=[rmse(fs[i-1],fs[i]) for i in range(1,len(fs))]
 result[name+'_adjacent_frame_changes']={'rmse_summary':stats(delta),'near_identical_pairs_below_rmse0_05':[i+1 for i,x in enumerate(delta) if x<.05]}
class Videos(HTMLParser):
 def __init__(self):super().__init__();self.items=[]
 def handle_starttag(self,tag,attrs):
  if tag=='video':self.items.append(dict(attrs))
parser=Videos();parser.feed((H/'index.html').read_text())
sources=sorted([(a['id'],H/a['src'],round(float(a['data-start'])*24),round(float(a['data-duration'])*24),round(float(a['data-media-start'])*24)) for a in parser.items],key=lambda row:row[2])
assert sources[0][2]==0 and sources[-1][2]+sources[-1][3]==524
assert all(a[2]+a[3]==b[2] for a,b in zip(sources,sources[1:]))
result['html_video_ranges']=[{'id':n,'scene_start_frame':o,'frames':c,'source_start_frame':ss} for n,p,o,c,ss in sources]

result['source_mapping']=[]
for name,p,offset,count,source_start in sources:
 sf=frames(p);pr=probe(p);actual=scene_frames[offset:offset+count];expected=sf[source_start:source_start+count]
 assert len(actual)==len(expected)==count
 errors=[rmse(a,b) for a,b in zip(actual,expected)]
 lags={}
 for lag in range(-3,4):
  values=[rmse(actual[i],sf[source_start+i+lag]) for i in range(0,count,5) if 0<=source_start+i+lag<len(sf)]
  lags[str(lag)]=statistics.mean(values)
 result['source_mapping'].append({'name':name,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'source_probe':pr,'scene_frame_range':[offset,offset+count],'source_frame_range':[source_start,source_start+count],'all_frame_expected_mapping_rmse':stats(errors),'sampled_lag_comparison_rmse':lags,'best_sampled_lag':min(lags,key=lags.get)})
prior=EXP/'hyperframes/reviews/r66-s21-hard-part/qa/s21.mp4';pf=frames(prior)
result['context_previous_192_mapping_rmse']=stats([rmse(a,b) for a,b in zip(context_frames[:192],pf[1280:1472])])
result['context_scene_524_mapping_rmse']=stats([rmse(a,b) for a,b in zip(context_frames[192:],scene_frames)])
with wave.open(str(MASTER),'rb') as f:f.setpos(25130*2000);expected=f.readframes(524*2000)
with wave.open(str(H/'public/audio/narration.wav'),'rb') as f:actual=f.readframes(f.getnframes())
result['staged_pcm_bit_exact']=actual==expected
result['encoded_audio']={'scene':audio_compare(scene,25130/24,524),'context':audio_compare(context,24938/24,716)}
result['stereo_channel_comparison']={}
for key,p,fc,pr in [('scene',scene,524,result['scene_probe']),('context',context,716,result['context_probe'])]:
 ast=next(x for x in pr['streams'] if x['codec_type']=='audio')
 if ast.get('channels')==2:
  left=audio(p,0,fc/24,0);right=audio(p,0,fc/24,1);n=min(len(left),len(right))
  result['stereo_channel_comparison'][key]={'sample_count':n,'left_right_rmse':math.sqrt(sum((left[i]-right[i])**2 for i in range(n))/n),'largest_difference':max(abs(left[i]-right[i]) for i in range(n))}
result['seam_audio_context_entry']={}
ca=audio(context,7.75,.5);ma=audio(MASTER,25130/24-.25,.5);n=min(len(ca),len(ma));aa=sum(x*x for x in ca[:n]);bb=sum(x*x for x in ma[:n]);ab=sum(x*y for x,y in zip(ca[:n],ma[:n]))
result['seam_audio_context_entry']={'context_range':[7.75,8.25],'samples':n,'correlation':ab/math.sqrt(aa*bb),'level_db_vs_master':10*math.log10(aa/bb)}

(OUT/'technical-qc.json').write_text(json.dumps(result,indent=2)+'\n')
cuts=[x[2] for x in sources[1:]]
seam_indices=sorted(set([0,523]+[i for cut in cuts for i in [cut-1,cut]]))
action_indices=sorted(set([i for source in sources[2:] for i in list(range(source[2],source[2]+source[3],24))+[source[2]+source[3]-1]]))
for name,p,indices in [('scene_seams',scene,seam_indices),('scene_action',scene,action_indices),('context_entry',context,[190,191,192,193])]:
 expr='+'.join('eq(n\\,%d)'%i for i in indices)
 rows=math.ceil(len(indices)/2)
 run(['ffmpeg','-y','-v','error','-i',str(p),'-vf',f'select={expr},scale=640:360,tile=2x{rows}','-frames:v','1','-update','1',str(OUT/(name+'.png'))])
 (OUT/(name+'-index.json')).write_text(json.dumps(indices)+'\n')
print(json.dumps({'decoded_frames':result['decoded_frames'],'staged_pcm_bit_exact':result['staged_pcm_bit_exact'],'encoded_audio':result['encoded_audio'],'source_best_lags':{x['name']:x['best_sampled_lag'] for x in result['source_mapping']}},indent=2))
