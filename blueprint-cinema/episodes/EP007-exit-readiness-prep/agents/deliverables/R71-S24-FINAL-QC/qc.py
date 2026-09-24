from pathlib import Path
import array,hashlib,json,math,subprocess,wave
ROOT=Path('/Users/brownmanbrain/GitHub/operator-economy'); E=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
H=E/'hyperframes/reviews/r71-s24-verdict'; C=E/'hyperframes/reviews/r71-s24-context'
O=ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R71-S24-FINAL-QC'
M=ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
def run(c): return subprocess.run(c,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=[]
for p,expected in [(H/'index.html','a7727975f424cd0f4ef26eae363d4b55b16cedd1262ab3f869032c8ed9c94f05'),(H/'qa/s24.mp4','c9945847aa4e4b281379e7331bb1fe097d3397530c08e97eea7c8551ae84a0a8'),(C/'qa/context.mp4','1d2cb8332856467934365f516178d25cca0e1f45f1ec8094b9955184366fef32')]:
 actual=sha(p);assert actual==expected; pins.append({'path':str(p.relative_to(ROOT)),'sha256':actual})
for p in [E/'direction/r71-s24-verdict/finish.py',H/'public/audio/narration.wav',M,E/'hyperframes/reviews/r70-s23-payoff/qa/s23.mp4']:
 pins.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
probe={}
for name,p,count in [('scene',H/'qa/s24.mp4',552),('context',C/'qa/context.mp4',744)]:
 pr=json.loads(run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration,sample_rate,channels','-of','json',str(p)]));v=next(s for s in pr['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',count);assert abs(float(v['duration'])-count/24)<.00001
 probe[name]=pr
with wave.open(str(M),'rb') as w:
 fm=(w.getnchannels(),w.getsampwidth(),w.getframerate());w.setpos(51768000);expected=w.readframes(1104000)
with wave.open(str(H/'public/audio/narration.wav'),'rb') as w:
 fs=(w.getnchannels(),w.getsampwidth(),w.getframerate());actual=w.readframes(w.getnframes())
assert fm==fs==(1,2,48000) and actual==expected

def mono(p,start,duration):
 a=array.array('f');a.frombytes(run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(duration),'-vn','-af','pan=mono|c0=c0','-ar','48000','-f','f32le','-']));return a
x=mono(C/'qa/context.mp4',7.5,.75);y=mono(M,1078,.75);n=min(len(x),len(y));x=x[:n];y=y[:n]
aa=sum(v*v for v in x);bb=sum(v*v for v in y);ab=sum(a*b for a,b in zip(x,y));ac={'samples':n,'sample_rate':48000,'context_window':[7.5,8.25],'master_window':[1078,1078.75],'zero_lag_correlation':ab/math.sqrt(aa*bb),'level_difference_db':10*math.log10(aa/bb)}
ac['correlation_vs_initial_generic_0_999_check']='pass' if ac['zero_lag_correlation']>.999 else 'below_threshold'
ac['master_rms_dbfs']=10*math.log10(bb/n)
ac['error_rms_dbfs']=10*math.log10(sum((a-b)**2 for a,b in zip(x,y))/n)
lags=[]
for lag in [-16,-8,-4,-2,-1,0,1,2,4,8,16]:
    xx=x[max(0,lag):n+min(0,lag)];yy=y[max(0,-lag):n-min(0,-lag)]
    m=min(len(xx),len(yy));xx=xx[:m];yy=yy[:m]
    lags.append({'lag_samples':lag,'correlation':sum(a*b for a,b in zip(xx,yy))/math.sqrt(sum(a*a for a in xx)*sum(b*b for b in yy))})
ac['lag_candidates']=lags
ac['best_tested_lag_samples']=max(lags,key=lambda z:z['correlation'])['lag_samples']
assert ac['best_tested_lag_samples']==0 and abs(ac['level_difference_db'])<.1
seam_index=24000
ac['seam_neighbor_samples_float']={'context':list(x[seam_index-4:seam_index+4]),'master':list(y[seam_index-4:seam_index+4])}

def gray(p,frames):
 s='+'.join('eq(n\\,%d)'%n for n in frames)
 raw=run(['ffmpeg','-v','error','-i',str(p),'-an','-vf',f'select={s},scale=32:18,format=gray','-fps_mode','passthrough','-f','rawvideo','-'])
 assert len(raw)==len(frames)*576;return [raw[n*576:(n+1)*576] for n in range(len(frames))]
scene_frames=[0,45,51,163,169,258,264,357,358,359,364,551]
a=gray(H/'qa/s24.mp4',scene_frames);b=gray(C/'qa/context.mp4',[n+192 for n in scene_frames]);matches=[]
for f,row,col in zip(scene_frames,a,b):
 mae=sum(abs(x-y) for x,y in zip(row,col))/576;assert mae<2;matches.append({'scene_frame':f,'context_frame':f+192,'mean_absolute_gray_difference':mae})
x=gray(E/'hyperframes/reviews/r70-s23-payoff/qa/s23.mp4',[38,229]);y=gray(C/'qa/context.mp4',[0,191]);lead=[]
for f,row,col in zip([38,229],x,y):
 mae=sum(abs(x-y) for x,y in zip(row,col))/576;assert mae<2;lead.append({'source_s23_frame':f,'context_frame':f-38,'mean_absolute_gray_difference':mae})
r={'status':'complete_with_documented_review_context_limitations','input_hashes_used':pins,'probes':probe,'pcm_format':fs,'pcm_samples':len(actual)//2,'pcm_bit_exact':True,'seam_audio':ac,'scene_context_frame_matches':matches,'lead_frame_matches':lead,'limits':['Only selected encoded frame comparisons performed; root full-frame blank scan not independently repeated.','No continuous normal-speed listening verdict.','Eight-second review lead-in starts inside aligned S23 work; final episode continuity is unaffected.']}
(O/'technical-qc.json').write_text(json.dumps(r,indent=2)+'\n')
selected=[191,192,237,243,549,550,556,743];s='+'.join('eq(n\\,%d)'%n for n in selected)
run(['ffmpeg','-y','-v','error','-i',str(C/'qa/context.mp4'),'-vf',f'select={s},scale=640:360,tile=2x4','-frames:v','1',str(O/'seam-and-cues.png')]);(O/'seam-and-cues-index.json').write_text(json.dumps(selected)+'\n')
print(json.dumps({'seam_audio':ac,'maximum_selected_frame_mae':max(v['mean_absolute_gray_difference'] for v in matches+lead),'scene_frames':552,'context_frames':744,'pcm_bit_exact':True},indent=2))
