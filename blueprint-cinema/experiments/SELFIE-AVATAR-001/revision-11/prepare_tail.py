import json,hashlib,subprocess,urllib.request,wave,base64
from pathlib import Path
from PIL import Image,ImageDraw
cfg=json.loads(Path('inputs.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(a):return subprocess.run(a,check=True,capture_output=True)
sources=[
('https://d8j0ntlcm91z4.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/hf_20260913_034355_f87bdc83-e65f-47ce-b64f-0fff26c29fbd.mp4','native.mp4','49bb223abf01ff1bc47cbeef5899e5610b848180d3d2ff35a63b37ffabf78ca5'),
('https://v3b.fal.media/files/b/0aaa367e/r3nr-VMhYG-ZGt4U42rK7_Cvtl8lCC.mp4','r10-sync.mp4','2df6df7561ad9986e997d78d7fd31801917c4f9b78c7272c64770df94672252f'),
('https://v3b.fal.media/files/b/0aaa35ee/-L-OSg2Vri4DStxgrcFHO_selfie-r10-final-ebda957ffd92f944.wav','voice.wav','ebda957ffd92f944ce180ffab455da84e48cfffd9ae775936be6cff3d085ba0f')]
for u,p,h in sources:
 urllib.request.urlretrieve(u,p)
 if sha(p)!=h:raise ValueError('source hash mismatch')
with wave.open('voice.wav') as w:
 if (w.getframerate(),w.getnchannels(),w.getsampwidth(),w.getnframes())!=(48000,1,2,2643731):raise ValueError('voice shape mismatch')
 w.setpos(1804000);pcm=w.readframes(839731)
with wave.open('tail.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(pcm)
run(['ffmpeg','-v','error','-i','native.mp4','-i','tail.wav','-map','0:v:0','-map','1:a:0','-vf','trim=start_frame=0:end_frame=420,setpts=PTS-STARTPTS','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart','tail.mp4'])
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json','tail.mp4']).stdout)
v=next(x for x in probe['streams'] if x['codec_type']=='video')
if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=(720,1280,'24/1',420):raise ValueError('tail video shape')
run(['ffmpeg','-v','error','-xerror','-i','tail.mp4','-f','null','-'])
times=[.4583333333,1.2,5.5,9.5,13.5,17.0]
sheet=Image.new('RGB',(1440,900),'#202426');draw=ImageDraw.Draw(sheet)
for row,path in enumerate(['native.mp4','r10-sync.mp4']):
 for col,t in enumerate(times):
  timestamp=t+(902/24 if row else 0)
  file=f'frame-{row}-{col}.png'
  run(['ffmpeg','-v','error','-ss',str(timestamp),'-i',path,'-frames:v','1',file])
  frame=Image.open(file).convert('RGB').resize((240,427))
  sheet.paste(frame,(col*240,row*450+23))
  draw.text((col*240+5,row*450+4),f'{"native" if row==0 else "R10 sync"} {t+902/24:.3f}s',fill='white')
sheet.save('diagnostic.jpg',quality=93)
report={'status':'tail_prepared_from_immutable_native_and_source_voice','source_inputs':[{'url':u,'sha256':h}for u,p,h in sources],'start_frame':902,'start_seconds':902/24,'end_frame_exclusive':1322,'frame_count':420,'width':720,'height':1280,'fps':24,'duration_seconds':17.5,'source_audio_start_sample':1804000,'audio_sample_count':839731,'audio_sample_rate_hz':48000,'audio_channels':1,'audio_sample_width_bytes':2,'audio_duration_seconds':839731/48000,'audio_pcm_sha256':hashlib.sha256(pcm).hexdigest(),'video_sha256':sha('tail.mp4'),'audio_sha256':sha('tail.wav'),'diagnostic_sha256':sha('diagnostic.jpg'),'video_url':cfg['uploads'][0]['url'],'audio_url':cfg['uploads'][1]['url'],'diagnostic_url':cfg['uploads'][2]['url'],'strict_decode_passed':True,'method':'First 420 native clip3 frames; original source voice exact sample slice; single clip without preceding joins. No mouth regeneration in this preparation.'}
Path('INPUT-REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
for p,slot in zip(['tail.mp4','tail.wav','diagnostic.jpg'],cfg['uploads']):
 request=urllib.request.Request(slot['upload_url'],data=Path(p).read_bytes(),method='PUT',headers={'Content-Type':slot['content_type']})
 with urllib.request.urlopen(request,timeout=60) as response:
  if response.status!=200:raise ValueError('upload failed')
 print('PUT_OK '+slot['media_id'],flush=True)
print('REPORT_BASE64='+base64.b64encode(Path('INPUT-REPORT.json').read_bytes()).decode(),flush=True)

