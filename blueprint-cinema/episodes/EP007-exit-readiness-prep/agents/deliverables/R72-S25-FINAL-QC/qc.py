from pathlib import Path
import array,hashlib,json,math,subprocess,wave
R=Path('/Users/brownmanbrain/GitHub/operator-economy');E=R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
H=E/'hyperframes/reviews/r72-s25-first-action';C=E/'hyperframes/reviews/r72-s25-context';P=E/'hyperframes/reviews/r71-s24-verdict'
O=R/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R72-S25-FINAL-QC';M=R/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
def run(c):return subprocess.run(c,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=[]
for p,expected in [(H/'index.html','999d7ed1762ef62692a4cf527a4bbed75176c807a1b867bf72bb77d8690390f8'),(H/'qa/s25.mp4','c3a4a467b08743c99b98837b484c14e0895608fe2070ad25908d7a2159076233'),(C/'qa/context.mp4','bd45de303216563dd180e8a854277513ecd1618ea578b8e05fabbe03cb87c364'),(P/'index.html','a7727975f424cd0f4ef26eae363d4b55b16cedd1262ab3f869032c8ed9c94f05'),(P/'qa/s24.mp4','c9945847aa4e4b281379e7331bb1fe097d3397530c08e97eea7c8551ae84a0a8')]:
 a=sha(p);assert a==expected;pins.append({'path':str(p.relative_to(R)),'sha256':a})
for p in [E/'direction/r72-s25-first-action/finish.py',H/'public/audio/narration.wav',M]:pins.append({'path':str(p.relative_to(R)),'sha256':sha(p)})
probes={}
for name,p,count in [('scene',H/'qa/s25.mp4',726),('context',C/'qa/context.mp4',926)]:
 pr=json.loads(run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration,sample_rate,channels','-of','json',str(p)]));v=next(s for s in pr['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',count)
 assert abs(float(v['duration'])-count/24)<.00001;probes[name]=pr
with wave.open(str(M),'rb') as w:
 fmt=(w.getnchannels(),w.getsampwidth(),w.getframerate());w.setpos(52872000);expected=w.readframes(1452000)
with wave.open(str(H/'public/audio/narration.wav'),'rb') as w:
 sfmt=(w.getnchannels(),w.getsampwidth(),w.getframerate());actual=w.readframes(w.getnframes())
assert fmt==sfmt==(1,2,48000) and actual==expected

def mono(p,start,dur):
 a=array.array('f');a.frombytes(run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(dur),'-vn','-af','pan=mono|c0=c0','-ar','48000','-f','f32le','-']));return a

def stats(x,y):
 n=min(len(x),len(y));x=x[:n];y=y[:n];aa=sum(v*v for v in x);bb=sum(v*v for v in y);ab=sum(a*b for a,b in zip(x,y));err=sum((a-b)**2 for a,b in zip(x,y));return {'compared_samples':n,'zero_lag_correlation':ab/math.sqrt(aa*bb),'level_difference_db':10*math.log10(aa/bb),'source_rms_dbfs':10*math.log10(bb/n),'residual_rms_dbfs':10*math.log10(err/n) if err else None}
seam=stats(mono(C/'qa/context.mp4',200/24-.5,1.25),mono(M,1101,1.25));seam['context_window']=[200/24-.5,200/24+.75];seam['master_window']=[1101,1102.25]
pause=stats(mono(H/'qa/s25.mp4',26.14,4.11),mono(M,1127.64,4.11));pause['scene_window']=[26.14,30.25];pause['master_window']=[1127.64,1131.75]

def gray(p,fs,extra='scale=32:18',size=576):
 s='+'.join('eq(n\\,%d)'%n for n in fs);raw=run(['ffmpeg','-v','error','-i',str(p),'-an','-vf',f'select={s},{extra},format=gray','-fps_mode','passthrough','-f','rawvideo','-']);assert len(raw)==len(fs)*size;return [raw[i*size:(i+1)*size] for i in range(len(fs))]
def mae(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
frames=[0,123,145,194,217,257,278,379,385,388,391,471,508,516,628,672,725]
a=gray(H/'qa/s25.mp4',frames);b=gray(C/'qa/context.mp4',[f+200 for f in frames]);matches=[{'scene_frame':f,'context_frame':f+200,'mean_absolute_gray_difference':mae(x,y)} for f,x,y in zip(frames,a,b)];assert max(d['mean_absolute_gray_difference'] for d in matches)<2
x=gray(P/'qa/s24.mp4',[352,551]);y=gray(C/'qa/context.mp4',[0,199]);lead=[{'s24_frame':f,'context_frame':f-352,'mean_absolute_gray_difference':mae(a,b)} for f,a,b in zip([352,551],x,y)];assert max(d['mean_absolute_gray_difference'] for d in lead)<2
button=gray(H/'qa/s25.mp4',[385,388,391],extra='crop=100:72:940:202',size=7200)
buttonmetric={'start_to_pressed_mae':mae(button[0],button[1]),'start_to_returned_mae':mae(button[0],button[2]),'frames':[385,388,391]}
end=gray(H/'qa/s25.mp4',[516,628,672,725]);hold={'settled516_to_pause628_mae':mae(end[0],end[1]),'pause628_to_final725_mae':mae(end[1],end[3]),'frames':[516,628,672,725]}
result={'status':'scoped_independent_checks_complete','input_hashes_used':pins,'probes':probes,'pcm_format':fmt,'staged_samples':len(actual)//2,'pcm_bit_exact':True,'seam_audio':seam,'end_pause_audio':pause,'cue_frame_matches':matches,'lead_frame_matches':lead,'button_press_roi':buttonmetric,'end_hold':hold,'limits':['Audio metrics are measurements, not a listening verdict or a universal correlation pass rule.','Full-frame blank scan was performed by root, not repeated by this scoped reviewer.','No owner acceptance or release is claimed.']}
(O/'technical-qc.json').write_text(json.dumps(result,indent=2)+'\n')
select=[199,200,345,478,579,588,716,925];s='+'.join('eq(n\\,%d)'%n for n in select);run(['ffmpeg','-y','-v','error','-i',str(C/'qa/context.mp4'),'-vf',f'select={s},scale=640:360,tile=2x4','-frames:v','1',str(O/'seam-cues-and-ending.png')]);(O/'seam-cues-and-ending-index.json').write_text(json.dumps(select)+'\n')
print(json.dumps({'seam_audio':seam,'end_pause_audio':pause,'button_press_roi':buttonmetric,'end_hold':hold,'max_selected_context_frame_mae':max(d['mean_absolute_gray_difference'] for d in matches+lead)},indent=2))
