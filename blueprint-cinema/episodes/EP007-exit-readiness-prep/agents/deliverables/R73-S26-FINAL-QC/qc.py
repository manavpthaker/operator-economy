from pathlib import Path
import array,hashlib,json,math,subprocess,wave
R=Path('/Users/brownmanbrain/GitHub/operator-economy');E=R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003';H=E/'hyperframes/reviews/r73-s26-close';C=E/'hyperframes/reviews/r73-s26-context';P=E/'hyperframes/reviews/r72-s25-first-action';O=R/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R73-S26-FINAL-QC';M=R/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
def run(c):return subprocess.run(c,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=[]
for p,e in [(H/'index.html','d78dfd06bf417877321adf0b9a3781d4255606c5d293dc9c2108a3d6e1c60acb'),(H/'qa/s26.mp4','a70380c107d36a626b83195c3c31ab54a62763062fb8797e30e69b4bca705341'),(C/'qa/context.mp4','5b00a3deba876218969e066886da6dda091922b8679ece98f71885d4b251783c'),(P/'index.html','999d7ed1762ef62692a4cf527a4bbed75176c807a1b867bf72bb77d8690390f8'),(P/'qa/s25.mp4','c3a4a467b08743c99b98837b484c14e0895608fe2070ad25908d7a2159076233'),(H/'public/audio/narration.wav','76ec84133baea40b7399c59a1969e50b9c1dd5f23507f4a0cbb26fc68d52120d')]:
 a=sha(p);assert a==e;pins.append({'path':str(p.relative_to(R)),'sha256':a})
for p in [M,E/'direction/r73-s26-close/finish.py',C/'qa/assembly-command.json']:pins.append({'path':str(p.relative_to(R)),'sha256':sha(p)})
probes={}
for name,p,n in [('scene',H/'qa/s26.mp4',149),('context',C/'qa/context.mp4',305)]:
 pr=json.loads(run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration,sample_rate,channels','-of','json',str(p)]));v=next(x for x in pr['streams'] if x['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',n);assert abs(float(v['duration'])-n/24)<.00001;probes[name]=pr

def mono(p,start,dur):
 a=array.array('f');a.frombytes(run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(dur),'-vn','-af','pan=mono|c0=c0','-ar','48000','-f','f32le','-']));return a

def stats(x,y):
 n=min(len(x),len(y));x=x[:n];y=y[:n];aa=sum(v*v for v in x);bb=sum(v*v for v in y);ab=sum(a*b for a,b in zip(x,y));ee=sum((a-b)**2 for a,b in zip(x,y));return {'samples':n,'correlation':ab/math.sqrt(aa*bb),'level_difference_db':10*math.log10(aa/bb),'source_rms_dbfs':10*math.log10(bb/n),'residual_rms_dbfs':10*math.log10(ee/n) if ee else None}
seam=stats(mono(C/'qa/context.mp4',6.25,1),mono(M,1131.5,1));seam.update({'context_window':[6.25,7.25],'master_window':[1131.5,1132.5]})
# Compare the final spoken word plus its complete tail/padding to the verified staged PCM.
end={}
ref=mono(H/'public/audio/narration.wav',5.4,149/24-5.4)
for name,p,start in [('scene',H/'qa/s26.mp4',5.4),('context',C/'qa/context.mp4',11.9)]:
 end[name]=stats(mono(p,start,149/24-5.4),ref)
# Codec outputs may contain a very low-level tail into the source-silent pad; measure rather than claim bit-exact AAC silence.
encoded_scene=mono(H/'qa/s26.mp4',0,149/24);encoded_context=mono(C/'qa/context.mp4',0,305/24)
def padstats(a,start,count):
 part=a[start:start+count];n=len(part);power=sum(v*v for v in part)/n;peak=max(abs(v) for v in part);return {'samples':n,'nonzero_samples':sum(v!=0 for v in part),'rms_dbfs':10*math.log10(power) if power else None,'peak_dbfs':20*math.log10(peak) if peak else None}
padding={'scene':padstats(encoded_scene,296519,1481),'context':padstats(encoded_context,608519,1481)}

def gray(p,fs):
 s='+'.join('eq(n\\,%d)'%f for f in fs);raw=run(['ffmpeg','-v','error','-i',str(p),'-an','-vf',f'select={s},scale=32:18,format=gray','-fps_mode','passthrough','-f','rawvideo','-']);assert len(raw)==len(fs)*576;return [raw[i*576:(i+1)*576] for i in range(len(fs))]
def mae(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
frames=[0,1,19,66,109,122,133,134,144,147,148];x=gray(H/'qa/s26.mp4',frames);y=gray(C/'qa/context.mp4',[f+156 for f in frames]);matches=[{'scene_frame':f,'context_frame':f+156,'mean_absolute_gray_difference':mae(a,b)} for f,a,b in zip(frames,x,y)];assert max(v['mean_absolute_gray_difference'] for v in matches)<2
leadx=gray(P/'qa/s25.mp4',[570,725]);leady=gray(C/'qa/context.mp4',[0,155]);lead=[{'s25_frame':f,'context_frame':f-570,'mean_absolute_gray_difference':mae(a,b)} for f,a,b in zip([570,725],leadx,leady)];assert max(v['mean_absolute_gray_difference'] for v in lead)<2
static={'sampled_scene_frames':frames,'first_to_last_mae':mae(x[0],x[-1]),'maximum_sampled_difference_from_first':max(mae(x[0],r) for r in x)}
report={'status':'scoped_independent_checks_complete','input_hashes_used':pins,'probes':probes,'staged_source_and_padding':'See staged-audio-qc.json; staged hash remains unchanged.','seam_audio':seam,'final_word_and_tail_audio':end,'decoded_frame_alignment_padding':padding,'scene_context_frame_matches':matches,'lead_frame_matches':lead,'static_card':static,'limits':['AAC is lossy; byte-exact preservation applies to the staged PCM prefix, not decoded compressed audio.','No continuous normal-speed subjective listening verdict.','Root full-frame blank scan was not independently repeated.','No owner acceptance or release claimed.']}
(O/'technical-qc.json').write_text(json.dumps(report,indent=2)+'\n')
fs=[155,156,175,222,265,289,300,304];s='+'.join('eq(n\\,%d)'%f for f in fs);run(['ffmpeg','-y','-v','error','-i',str(C/'qa/context.mp4'),'-vf',f'select={s},scale=640:360,tile=2x4','-frames:v','1',str(O/'seam-and-final-word.png')]);(O/'seam-and-final-word-index.json').write_text(json.dumps(fs)+'\n')
print(json.dumps({'seam_audio':seam,'final_word_and_tail_audio':end,'decoded_padding':padding,'static_card':static,'max_selected_source_context_mae':max(v['mean_absolute_gray_difference'] for v in matches+lead)},indent=2))
