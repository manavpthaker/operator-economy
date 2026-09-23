"""Measure each new source independently. Native envelopes are diagnostic only."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
D=Path(__file__).resolve().parent;E=D.parents[1]
P=E/'hyperframes/reviews/r76-s17-presenter/provider'
rate=16000
def decode(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-']),dtype='<f4').astype(float)
ref=decode(P/'audio/c.wav')
mode=sys.argv[1];source=P/('native.mp4' if mode=='native' else 'restoration/restored.mp4')
actual=decode(source)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(source)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert video['r_frame_rate']=='24/1'
windows=[(.4,1.8),(3.,4.5),(5.8,7.3)]
rows=[]
if mode=='native':
    block=160
    def envelope(x):
        x=x[:len(x)//block*block].reshape(-1,block)
        return np.sqrt(np.mean(x*x,axis=1))
    rr=envelope(ref);aa=envelope(actual)
    for lo,hi in windows:
        start=round(lo*100);stop=round(hi*100);target=rr[start:stop]
        candidates=[]
        for shift in range(-100,151):
            a=start+shift;b=stop+shift
            if a<0 or b>len(aa):continue
            score=float(np.corrcoef(target,aa[a:b])[0,1]);candidates.append((score,shift))
        score,shift=max(candidates)
        rows.append({'reference_window_seconds':[lo,hi],'offset_seconds':shift/100,'envelope_correlation':score})
    report={'native_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'probe':probe,'windows':rows,'limits':'Generated native speech may differ; envelope peaks are diagnostic, not perceptual sync or a sufficient trim decision.'}
    target=P/'NATIVE-ANALYSIS.json'
else:
    for lo,hi in windows:
        start,stop=round(lo*rate),round(hi*rate);target=ref[start:stop]
        n=len(actual)+len(target)-1;fftn=1<<(n-1).bit_length()
        corr=np.fft.irfft(np.fft.rfft(actual,fftn)*np.fft.rfft(target[::-1],fftn),fftn)[:n]
        conv=corr[len(target)-1:len(actual)]
        power=np.r_[0,np.cumsum(actual*actual)];target_power=np.dot(target,target)
        window_power=np.maximum(power[len(target):]-power[:-len(target)],0)
        scores=conv/np.sqrt(np.maximum(window_power,1e-12)*target_power)
        scores[window_power<target_power*.001]=-1
        idx=int(np.argmax(scores))
        rows.append({'reference_window_seconds':[lo,hi],'offset_seconds':(idx-start)/rate,'correlation':float(scores[idx])})
    assert min(r['correlation'] for r in rows)>.97,rows
    assert max(r['offset_seconds'] for r in rows)-min(r['offset_seconds'] for r in rows)<=.01,rows
    offset=float(np.median([r['offset_seconds'] for r in rows]));frame=round(offset*24)
    assert frame>=0 and frame+192<=int(video['nb_read_frames']),(frame,video)
    report={'windows':rows,'selected_source_in_frame':frame,'selected_source_in_seconds':frame/24,'measured_offset_seconds':offset,'frame_rounding_error_seconds':frame/24-offset,'output_frames':192,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_audio_sha256':hashlib.sha256((P/'audio/c.wav').read_bytes()).hexdigest(),'probe':probe,'limits':'Source audio alignment and frame rounding only. Normal-speed owner review still establishes perceived lips, identity and gesture.'}
    target=P/'ALIGNMENT.json'
target.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='probe'},indent=2))
