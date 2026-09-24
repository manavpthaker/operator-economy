"""Inspect native sections against their exact source audio; no generation or mutation API."""
import hashlib,json,subprocess,urllib.request,zipfile
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
rows=json.loads(Path('INPUTS.json').read_text())
results=[];shots=[]
for row in rows:
    name=row['name']
    for kind in ['video','audio']:
        url=row[kind+'_url'];p=Path(name+('.mp4' if kind=='video' else '.wav'))
        data=urllib.request.urlopen(url,timeout=60).read();p.write_bytes(data)
        if kind=='audio': assert hashlib.sha256(data).hexdigest()==row['audio_sha256']
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',name+'.mp4']))
    def pcm(path):
        b=subprocess.check_output(['ffmpeg','-v','error','-i',path,'-vn','-ac','1','-ar','16000','-f','f32le','-'])
        return np.frombuffer(b,dtype='<f4').astype(float)
    a=pcm(name+'.wav');b=pcm(name+'.mp4');n=min(len(a),len(b))
    zero=float(np.corrcoef(a[:n],b[:n])[0,1])
    size=len(a)+len(b)-1;nfft=1<<(size-1).bit_length()
    cross=np.fft.irfft(np.fft.rfft(b,nfft)*np.fft.rfft(a[::-1],nfft),nfft)[:size]
    lags=np.arange(size)-len(a)+1;mask=np.abs(lags)<=16000
    lag=int(lags[mask][np.argmax(cross[mask])])
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    duration=float(v.get('duration',probe['format']['duration']))
    result={'name':name,'video_sha256':hashlib.sha256(Path(name+'.mp4').read_bytes()).hexdigest(),'video_url':row['video_url'],'probe':probe,'audio_zero_lag_correlation':zero,'best_lag_seconds':lag/16000,'source_audio_duration':len(a)/16000,'native_audio_duration':len(b)/16000,'limits':'Audio alignment and sampled frames do not establish visual lip sync or naturalness.'}
    results.append(result)
    for i,f in enumerate([.04,.22,.45,.68,.9]):
        t=duration*f;p=Path(name+'-'+str(i)+'.jpg')
        subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',name+'.mp4','-frames:v','1','-q:v','2',str(p)],check=True)
        im=Image.open(p).convert('RGB');im.thumbnail((288,512));cell=Image.new('RGB',(288,538),'#171717');cell.paste(im,((288-im.width)//2,26));ImageDraw.Draw(cell).text((8,7),f'{name}: {t:.2f}s',fill='white');shots.append(cell)
sheet=Image.new('RGB',(1440,1076))
for i,im in enumerate(shots):sheet.paste(im,((i%5)*288,(i//5)*538))
sheet.save('native-contact.jpg',quality=94)
Path('NATIVE-QA.json').write_text(json.dumps(results,indent=2)+'\n')
with zipfile.ZipFile('native-qa.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write('NATIVE-QA.json');z.write('native-contact.jpg')
print(json.dumps([{k:v for k,v in x.items() if k!='probe'} for x in results]))
