#!/usr/bin/env python3
"""Assemble S25 context and preserve the complete S26 source-audio endpoint."""
from pathlib import Path
import array, hashlib, json, math, subprocess, wave
ROOT=Path(__file__).resolve().parents[5]
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
H=EXP/'hyperframes/reviews/r75-s26-boundary-close'; C=EXP/'hyperframes/reviews/r75-s26-context'
MASTER=ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
def run(cmd): return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
cmd=['ffmpeg','-y','-v','error','-i',str(EXP/'hyperframes/reviews/r72-s25-first-action/qa/s25.mp4'),'-i',str(H/'qa/s26.mp4'),'-i',str(MASTER),
 '-filter_complex','[0:v]trim=start_frame=570:end_frame=726,setpts=PTS-STARTPTS[v0];[1:v]trim=start_frame=0:end_frame=149,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v];[2:a]atrim=start_sample=54012000:end_sample=54620519,asetpts=PTS-STARTPTS,apad=pad_len=1481,pan=stereo|c0=c0|c1=c0[a]',
 '-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart',str(C/'qa/context.mp4')]
(C/'qa/assembly-command.json').write_text(json.dumps(cmd,indent=2)+'\n');run(cmd)
def audio(p,start,dur):
 a=array.array('f'); a.frombytes(run(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(dur),'-vn','-af','pan=mono|c0=c0','-ar','8000','-f','f32le','-']));return a
def inspect(p,start,frames):
 pr=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels','-of','json',str(p)]))
 v=next(s for s in pr['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'24/1',frames)
 raw=run(['ffmpeg','-v','error','-xerror','-i',str(p),'-an','-vf','scale=64:36,format=gray','-f','rawvideo','-'])
 size=64*36;assert len(raw)==frames*size;sd=[]
 for n in range(frames):
  row=raw[n*size:(n+1)*size];mean=sum(row)/size
  sd.append(math.sqrt(max(0,sum(x*x for x in row)/size-mean*mean)))
 assert min(sd)>3
 a=audio(p,0,frames/24); b=audio(MASTER,start,frames/24);n=min(len(a),len(b));a=a[:n];b=b[:n]
 aa=sum(x*x for x in a);bb=sum(x*x for x in b);ab=sum(x*y for x,y in zip(a,b));corr=ab/math.sqrt(aa*bb);db=10*math.log10(aa/bb)
 assert corr>.999 and abs(db)<.1
 return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'frames':frames,'duration':frames/24,'near_uniform_frames':sum(s<3 for s in sd),'minimum_frame_sd':min(sd),'audio_comparison':'Decoded source prefix only; appended frame-alignment silence checked separately in PCM.','compared_audio_samples_at_8khz':n,'audio_zero_lag_correlation':corr,'audio_level_db_vs_master':db,'probe':pr}
with wave.open(str(MASTER),'rb') as src:
 assert src.getnframes()==54620519 and src.getframerate()==48000
 src.setpos(54324000); expected=src.readframes(296519)
with wave.open(str(H/'public/audio/narration.wav'),'rb') as src:
 assert src.getframerate()==48000 and src.getnchannels()==1 and src.getsampwidth()==2 and src.getnframes()==298000
 actual=src.readframes(src.getnframes())
assert actual[:len(expected)]==expected and actual[len(expected):]==b'\0'*(1481*2)
assert json.loads((H/'qa/check.json').read_text())['ok']
report={'status':'technical_pass_owner_review_pending','source_prefix_pcm_bit_exact':True,'preserved_source_samples':296519,'appended_zero_samples':1481,'padding_seconds':1481/48000,'strict_check':True,'runtime':'0.8.46','source_sha256':sha(H/'index.html'),
 'scene':inspect(H/'qa/s26.mp4',1131.75,149),'context':inspect(C/'qa/context.mp4',1125.25,305),
 'limits':['No owner acceptance, canonical conform or release.','Audio metrics are not a human listening verdict.','Static closing card is intentional.','Encoded AAC is not lossless; bit-exact assertion applies to staged PCM source prefix.']}
(H/'qa/VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
frames=[0,96,155,156,175,230,290,304];s='+'.join('eq(n\\,%s)'%n for n in frames)
run(['ffmpeg','-y','-v','error','-i',str(C/'qa/context.mp4'),'-vf',f'select={s},scale=640:360,tile=2x4','-frames:v','1','-update','1',str(H/'qa/encoded-contact.png')])
for n in [0,148]:
 run(['ffmpeg','-y','-v','error','-i',str(H/'qa/s26.mp4'),'-vf',f'select=eq(n\\,{n})','-frames:v','1','-update','1',str(H/f'qa/encoded-{n}.png')])
print(json.dumps({k:({a:b for a,b in v.items() if a!='probe'} if k in ['scene','context'] else v) for k,v in report.items()},indent=2))
