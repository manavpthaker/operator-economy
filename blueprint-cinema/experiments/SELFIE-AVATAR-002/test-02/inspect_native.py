import json,hashlib,subprocess,wave,re,zipfile
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json','native.mp4']))
def pcm(p):
    with wave.open(p) as w:return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
a=pcm('source.wav');b=pcm('native.wav')
assert hashlib.sha256(Path('source.wav').read_bytes()).hexdigest()=='2fda60f4b9f61fcb2f784ae311ce13f87525a484920e5a6d0079e0033b730609'
size=len(a)+len(b)-1;nfft=1<<(size-1).bit_length()
c=np.fft.irfft(np.fft.rfft(b,nfft)*np.fft.rfft(a[::-1],nfft),nfft)[:size]
lags=np.arange(size)-(len(a)-1);mask=np.abs(lags)<=48000;best=int(lags[mask][np.argmax(c[mask])])
aa=a[max(0,-best):];bb=b[max(0,best):];n=min(len(aa),len(bb));corr=float(np.corrcoef(aa[:n],bb[:n])[0,1])
m=WhisperModel('small.en',device='cpu',compute_type='int8')
segs,info=m.transcribe('native.mp4',beam_size=5,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,language='en')
words=[];transcript=''
for s in segs:
    transcript+=s.text
    words.extend({'text':w.word.strip(),'start':w.start,'end':w.end,'probability':w.probability} for w in s.words or [])
expected="Sometimes it’s less work to just do the task. I can use AI to build something that does it for me."
norm=lambda s:re.findall(r"[a-z]+(?:'[a-z]+)?",s.lower().replace('’',"'"))
r={'native_sha256':hashlib.sha256(Path('native.mp4').read_bytes()).hexdigest(),'probe':probe,'transcript':transcript.strip(),'words':words,'exact_words':norm(expected)==norm(transcript),'source_native_best_lag_seconds':best/48000,'source_native_correlation_after_lag':corr,'limits':'Transcript and audio correlation do not prove visual lip sync or moving likeness.'}
Path('NATIVE-QA.json').write_text(json.dumps(r,indent=2)+'\n')
for i,t in enumerate([.25,1.25,2.5,3.4,4.5,5.7,6.5]):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i','native.mp4','-frames:v','1','-q:v','2',f'native-{i+1:02d}.jpg'],check=True)
with zipfile.ZipFile('/home/user/selfie-w2-test02-native-qa.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write('NATIVE-QA.json')
    for p in Path('.').glob('native-*.jpg'):z.write(p)
print(json.dumps({k:v for k,v in r.items() if k!='probe'}),flush=True)
