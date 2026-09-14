"""Measure source-voice preservation in a restored section or the complete assembly."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
name=sys.argv[1]
assert name in ('opening','final')
if name=='final':
    source=BASE/'assembly/public/audio/original-c.wav'
    video=BASE/'assembly/renders/week2-full02-uncaptioned.mp4'
    expected='0ad39c68a67b6c0f11edcbbe952380fc616716a59788dc049e2613313e4091e0'
    report_path=BASE/'FINAL-AUDIO-QA.json'
else:
    source=BASE/'media'/'opening.wav'
    video=BASE/'media'/f'{name}-restored.mp4'
    expected='90bd248de78abdd33fc302e384bed4cc562ae652248e9379e201ca5bafe72ede'
    report_path=BASE/name/'SYNC-AUDIO-QA.json'
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
def decoded(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype='<f4').astype(float)
def match(ref,out,maxlag=6400):
    n=min(len(ref),len(out));ref=ref[:n];out=out[:n]
    size=1<<(2*n-1).bit_length()
    x=np.fft.irfft(np.fft.rfft(out,size)*np.conj(np.fft.rfft(ref,size)),size)
    lags=np.arange(-min(maxlag,n-1),min(maxlag,n-1)+1)
    lag=int(lags[np.argmax(x[lags%size])])
    if lag>=0:a,b=ref[:n-lag],out[lag:n]
    else:a,b=ref[-lag:n],out[:n+lag]
    return {'lag_seconds':lag/16000,'correlation':float(np.corrcoef(a,b)[0,1])}
a,b=decoded(source),decoded(video);windows=[]
whole=match(a,b);offset=round(whole['lag_seconds']*16000)
for start in np.arange(.1,len(a)/16000-.5,1.0):
    s=max(round(start*16000),-offset,0);e=min(s+12000,len(a),len(b)-offset)
    if e<=s:continue
    if np.sqrt(np.mean(a[s:e]**2))<.001:continue
    residual=match(a[s:e],b[s+offset:e+offset],1600)
    windows.append({'start':s/16000,'end':e/16000,'lag_seconds':whole['lag_seconds']+residual['lag_seconds'],'residual_lag_seconds':residual['lag_seconds'],'correlation':residual['correlation']})
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
report={'name':name,'source_sha256':expected,'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'source_audio_seconds':len(a)/16000,'output_audio_seconds':len(b)/16000,'global_audio':whole,'speech_windows':windows,'probe':probe,'limits':'This measures original-voice clock preservation. It cannot certify visual lip sync, moving likeness or owner acceptance.'}
aa=a[max(0,-offset):];bb=b[max(0,offset):];n=min(len(aa),len(bb));aa=aa[:n];bb=bb[:n]
report['level']={'rms_gain_db':float(20*np.log10(np.sqrt(np.mean(bb**2))/np.sqrt(np.mean(aa**2)))),'decoded_peak':float(np.max(np.abs(bb)))}
report_path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('probe','speech_windows')},indent=2))
print(json.dumps({'speech_windows':len(windows),'minimum_window_correlation':min(x['correlation'] for x in windows),'maximum_window_abs_lag':max(abs(x['lag_seconds']) for x in windows)}))
assert report['global_audio']['correlation']>.98
assert min(x['correlation'] for x in windows)>.97
if name=='final':
    assert abs(report['global_audio']['lag_seconds'])<.025
    assert max(abs(x['lag_seconds']) for x in windows)<.025
    assert abs(report['level']['rms_gain_db'])<.1
    assert report['level']['decoded_peak']<1
else:
    # A provider may insert silence. Preserve the measured offset so picture can
    # be aligned to the unchanged master; do not treat an offset as zero lag.
    assert max(abs(x['lag_seconds']-report['global_audio']['lag_seconds']) for x in windows)<.002
