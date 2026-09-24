import wave,json,hashlib,subprocess,zipfile
from pathlib import Path
import numpy as np
def pcm(path):
    with wave.open(path) as w:return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
a=pcm('source.wav');b=pcm('decoded.wav')
assert hashlib.sha256(Path('source.wav').read_bytes()).hexdigest()=='2fda60f4b9f61fcb2f784ae311ce13f87525a484920e5a6d0079e0033b730609'
def match(a,b,maxlag):
    size=len(a)+len(b)-1;f=1<<(size-1).bit_length()
    c=np.fft.irfft(np.fft.rfft(b,f)*np.fft.rfft(a[::-1],f),f)[:size]
    l=np.arange(size)-(len(a)-1);m=np.abs(l)<=maxlag;k=int(l[m][np.argmax(c[m])])
    aa=a[max(0,-k):];bb=b[max(0,k):];n=min(len(aa),len(bb))
    return {'lag_seconds':k/48000,'correlation':float(np.corrcoef(aa[:n],bb[:n])[0,1])}
whole=match(a,b,4800);windows=[]
for t in [.15,1.2,2.1,3.7,4.6,5.4]:
    s=int(t*48000);windows.append({'start':t,**match(a[s:s+24000],b[s:s+24000],2400)})
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json','final.mp4']))
v=next(x for x in probe['streams'] if x['codec_type']=='video')
report={'final_sha256':hashlib.sha256(Path('final.mp4').read_bytes()).hexdigest(),'final_bytes':Path('final.mp4').stat().st_size,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frame_count':v.get('nb_frames'),'duration_seconds':float(probe['format']['duration']),'audio':whole,'voice_windows':windows,'source_samples':len(a),'decoded_samples':len(b),'limits':'Audio correlation verifies the original voice clock, not visual lip sync or moving likeness.'}
assert whole['correlation']>.98 and abs(whole['lag_seconds'])<.025,report
assert min(x['correlation'] for x in windows)>.97 and max(abs(x['lag_seconds']) for x in windows)<.025,report
Path('FINAL-QA.json').write_text(json.dumps(report,indent=2)+'\n')
for i,t in enumerate([.25,1.25,2.5,3.4,4.5,5.7,6.5]):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i','final.mp4','-frames:v','1','-q:v','2',f'final-{i+1:02d}.jpg'],check=True)
with zipfile.ZipFile('/home/user/selfie-w2-test02-final-qa.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write('FINAL-QA.json')
    for p in Path('.').glob('final-*.jpg'):z.write(p)
print(json.dumps(report),flush=True)
