"""Measure original-audio insertion before selecting R47 picture frames."""
from pathlib import Path
import json, subprocess, hashlib
import numpy as np
P=Path(__file__).resolve().parent
R=next(x for x in P.parents if (x/'.agents').exists())
auth=json.loads((P/'GENERATION-AUTHORIZATION.json').read_text())
plan=json.loads((R/auth['plan']['path']).read_text())
original=P/'audio/transfer-original.wav'
source=P/'restoration/restored.mp4'
assert hashlib.sha256(original.read_bytes()).hexdigest()==plan['audio']['sha256']
rate=16000
def decode(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-']),dtype='<f4').astype(float)
ref=decode(original);actual=decode(source)
def compare(lo,hi):
    start,stop=round(lo*rate),round(hi*rate);target=ref[start:stop]
    n=len(actual)+len(target)-1;fftn=1<<(n-1).bit_length()
    corr=np.fft.irfft(np.fft.rfft(actual,fftn)*np.fft.rfft(target[::-1],fftn),fftn)[:n]
    conv=corr[len(target)-1:len(actual)]
    power=np.r_[0,np.cumsum(actual*actual)];target_power=np.dot(target,target)
    window_power=np.maximum(power[len(target):]-power[:-len(target)],0)
    scores=conv/np.sqrt(np.maximum(window_power,1e-12)*target_power)
    scores[window_power<target_power*.001]=-1
    index=int(np.argmax(scores))
    return {'reference_window_seconds':[lo,hi],'source_window_start_seconds':index/rate,'offset_seconds':(index-start)/rate,'correlation':float(scores[index])}
rows=[compare(.4,1.8),compare(3.5,5.8),compare(8.3,10.8)]
offset=float(np.median([r['offset_seconds'] for r in rows]))
assert min(r['correlation'] for r in rows)>.97,rows
assert max(r['offset_seconds'] for r in rows)-min(r['offset_seconds'] for r in rows)<=.01,rows
reference_in=plan['picture_master_range'][0]-plan['audio_master_range'][0]
fps=24;frame=round((offset+reference_in)*fps)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video');duration=float(video.get('duration',probe['format']['duration']))
assert frame>=0 and frame/fps+plan['picture_frames']/fps<=duration+1e-6,(frame,duration)
result={'method':'Early/middle/late waveform correlation at16kHz; nearest24fps picture frame','measurements':rows,'measured_offset_seconds':offset,'reference_in_seconds':reference_in,'selected_source_in_frame':frame,'selected_source_in_seconds':frame/fps,'frame_rounding_error_seconds':frame/fps-(offset+reference_in),'source_duration_seconds':duration,'output_frames':plan['picture_frames'],'output_duration_seconds':plan['picture_frames']/fps,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_audio_sha256':plan['audio']['sha256'],'limitations':'Waveform alignment locates original speech in the container; it does not establish perceptual lip sync, naturalness, likeness or gesture quality.'}
(P/'ALIGNMENT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
