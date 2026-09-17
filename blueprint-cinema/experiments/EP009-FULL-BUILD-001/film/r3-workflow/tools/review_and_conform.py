import pathlib,json,subprocess,hashlib,sys,urllib.request,datetime
import numpy as np

ROOT=pathlib.Path.cwd();BASE=ROOT/'blueprint-cinema/experiments/EP009-FULL-BUILD-001/film/r3-workflow'
PLAN=json.loads((BASE/'PLAN.json').read_text())
def run(args):return subprocess.run(args,check=True,capture_output=True).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def binding(p):return {'path':str(p.relative_to(ROOT)),'sha256':sha(p)}
def probe(p):
 d=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));return d
def contact(shot):
 p=BASE/shot['id'];raw=p/'raw-r1.mp4'; q=p/'qa';q.mkdir(exist_ok=True)
 d=probe(raw);write(p/'RAW-PROBE-r1.json',d)
 vf="fps=2,scale=480:270,tile=4x5:padding=2"
 run(['ffmpeg','-v','error','-y','-i',str(raw),'-vf',vf,'-frames:v','1',str(q/'contact-r1.jpg')])
 return {'id':shot['id'],'raw':binding(raw),'probe':d,'contact':str((q/'contact-r1.jpg').relative_to(ROOT))}
def conform(shot,start_frame,attempt=1):
 p=BASE/shot['id'];raw=p/f'raw-r{attempt}.mp4';info=probe(raw);v=next(x for x in info['streams'] if x['codec_type']=='video');fps=eval(v['r_frame_rate']);assert fps==24
 n=shot['target_frames'];assert start_frame+n<=int(v['nb_read_frames'])
 out=p/f'final-r{attempt}.mp4';pcm=p/f'final-r{attempt}.pcm.mov';master=ROOT/PLAN['master']['path'];a0,a1=[x*2000 for x in shot['original_frames']]
 vf=f'trim=start_frame={start_frame}:end_frame={start_frame+n},setpts=PTS-STARTPTS,scale=1280:720:flags=lanczos,setsar=1'
 af=f'atrim=start_sample={a0}:end_sample={a1},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0'
 run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(master),'-filter_complex',f'[0:v]{vf}[v];[1:a]{af}[a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-r','24','-c:a','pcm_s16le','-ar','48000','-movflags','+faststart',str(pcm)])
 run(['ffmpeg','-v','error','-y','-i',str(pcm),'-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',str(out)])
 final=probe(out);vfinfo=next(x for x in final['streams'] if x['codec_type']=='video');afinfo=next(x for x in final['streams'] if x['codec_type']=='audio')
 ref=run(['ffmpeg','-v','error','-i',str(master),'-af',f'atrim=start_sample={a0}:end_sample={a1}','-f','s16le','-ac','1','-'])
 pcmgot=run(['ffmpeg','-v','error','-i',str(pcm),'-map','0:a','-af','pan=mono|c0=c0','-f','s16le','-']);assert ref==pcmgot
 got=run(['ffmpeg','-v','error','-i',str(out),'-map','0:a','-af','pan=mono|c0=c0','-f','s16le','-']);r=np.frombuffer(ref,dtype=np.int16);g=np.frombuffer(got,dtype=np.int16)[:len(r)];corr=float(np.corrcoef(r,g)[0,1]);assert corr>=.999
 grey=run(['ffmpeg','-v','error','-i',str(out),'-vf','scale=160:90','-pix_fmt','gray','-f','rawvideo','-']);f=np.frombuffer(grey,dtype=np.uint8).reshape(-1,90,160);uniform=int((np.ptp(f,axis=(1,2))<8).sum());assert uniform==0
 assert int(vfinfo['nb_read_frames'])==n and vfinfo['width']==1280 and vfinfo['height']==720 and vfinfo['r_frame_rate']=='24/1' and int(afinfo['sample_rate'])==48000 and afinfo['channels']==2
 q=p/'qa';q.mkdir(exist_ok=True)
 for idx in [0,n//2,n-1]:run(['ffmpeg','-v','error','-y','-i',str(out),'-vf',f'select=eq(n\\,{idx})','-frames:v','1',str(q/f'final-r{attempt}-f{idx:04d}.png')])
 record={'id':shot['id'],'status':'technical_pass_creative_review_pending','source_raw':binding(raw),'source_window_frames':[start_frame,start_frame+n],'source_window_seconds':[start_frame/24,(start_frame+n)/24],'speed_change':False,'reverse':False,'freeze':False,'original_frames':shot['original_frames'],'target_frames':n,'final':binding(out),'intermediate_pcm':binding(pcm),'checks':{'frames':int(vfinfo['nb_read_frames']),'dimensions':[1280,720],'fps':24,'sample_rate':48000,'audio_channels':2,'pcm_sample_exact':True,'aac_correlation_zero_lag':corr,'audio_offset_windows':'not applicable: silent film; locked master excerpt attached without timing alteration','uniform_frames':uniform},'native_probe':info,'final_probe':final,'review_status':'pending visual review'}
 write(p/f'TAKE-r{attempt}.json',record);return record
if __name__=='__main__':
 if sys.argv[1]=='contacts':
  for s in PLAN['shots']:
   if (BASE/s['id']/'raw-r1.mp4').exists():print(json.dumps(contact(s)))
 elif sys.argv[1]=='conform':
  shot=next(x for x in PLAN['shots'] if x['id']==sys.argv[2]);print(json.dumps(conform(shot,int(sys.argv[3]))))
