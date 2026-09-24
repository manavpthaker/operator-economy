"""Read-only R9 diagnosis of the R8 native soundtrack against approved R7 voice."""
import hashlib,io,json,subprocess,urllib.request,wave
from pathlib import Path
import numpy as np

RATE=16000
SOURCE_URL='https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/0e152b63-7636-4413-b31a-28002e35ef88.mp3'
SOURCE_SHA='ca8d664b1e2e9bac50eadc4e9efd6d03d7de02d87cbc0511c7aa97d52c6a7f3d'
NATIVE_URL='https://d8j0ntlcm91z4.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/hf_20260913_021450_d40c526d-a4af-4d48-a988-d95247163d63.mp4'
NATIVE_SHA='f94c6bfd027c80498c65c133b0d6858987ee0739ce7283fcad78b7335aa3f858'
WINDOWS=[('opening',.20,3.50),('admission',3.75,5.45),('With_AI',5.5,6.6),('GTM_explanation',11.2,16.72),('research_ending',17.12,20.83)]
paths={}
for name,url,digest in [('reference',SOURCE_URL,SOURCE_SHA),('native',NATIVE_URL,NATIVE_SHA)]:
 p=Path('/home/user/r9-diagnosis-'+name+('.wav' if name=='reference' else '.mp4'))
 urllib.request.urlretrieve(url,p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
 paths[name]=p
with wave.open(str(paths['reference'])) as wav:
 assert (wav.getframerate(),wav.getnchannels(),wav.getsampwidth(),wav.getnframes())==(48000,1,2,1020000)

def samples(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar',str(RATE),'-f','f32le','pipe:1'])
 return np.frombuffer(raw,dtype='<f4').astype(np.float64)

def corr(a,b):
 return float(np.corrcoef(a,b)[0,1]) if len(a)>1 and len(a)==len(b) and np.std(a)>0 and np.std(b)>0 else None

def rms(x):
 return float(np.sqrt(np.mean(x*x))) if len(x) else None

def lag_window(a,b,left,right,lag):
 al,ar=round(left*RATE),round(right*RATE)
 margin=round(.50*RATE)
 bl,br=max(0,al+lag-margin),min(len(b),ar+lag+margin)
 x,y=a[al:ar],b[bl:br]
 assert len(y)>=len(x)
 size=1<<(len(x)+len(y)-2).bit_length()
 cv=np.fft.irfft(np.fft.rfft(y,size)*np.fft.rfft(x[::-1],size),size)
 start,stop=len(x)-1,len(y)
 index=int(np.argmax(cv[start:stop]))
 offset=bl+index-al
 matched=y[index:index+len(x)]
 gain=float(np.dot(x,matched)/np.dot(x,x))
 return {'source_window_seconds':[left,right],'offset_seconds':offset/RATE,
   'correlation':corr(x,matched),'linear_gain':gain,
   'normalized_residual_rms':rms(matched-gain*x)/rms(matched),
   'search_boundary_hit':index in (0,len(y)-len(x))}

a,b=map(samples,[paths['reference'],paths['native']])
size=1<<(len(a)+len(b)-2).bit_length()
cv=np.fft.irfft(np.fft.rfft(b,size)*np.fft.rfft(a[::-1],size),size)
start=max(0,len(a)-1-RATE);stop=min(len(a)+len(b)-1,len(a)+RATE)
lag=int(np.argmax(cv[start:stop])+start-(len(a)-1))
aa,bb=max(0,-lag),max(0,lag)
n=min(len(a)-aa,len(b)-bb)
matched_ref,matched_native=a[aa:aa+n],b[bb:bb+n]
gain=float(np.dot(matched_ref,matched_native)/np.dot(matched_ref,matched_ref))
windows={name:lag_window(a,b,left,right,lag) for name,left,right in WINDOWS}
offsets=[w['offset_seconds'] for w in windows.values()]
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
 'format=duration,start_time:stream=index,codec_type,codec_name,width,height,r_frame_rate,nb_frames,start_time,duration,sample_rate,channels',
 '-of','json',str(paths['native'])]))
source_available_end=(len(b)-lag)/RATE
tail=a[max(0,round(source_available_end*RATE)):]
tail_stats={'source_range_seconds':[source_available_end,len(a)/RATE],'duration_seconds':len(tail)/RATE,
 'rms':rms(tail),'peak':float(np.max(np.abs(tail))) if len(tail) else None}
last_word_end=20.7718
result={
 'scope':'R9 diagnosis only: R8 native video_edit audio compared with approved R7 waveform',
 'source':{'url':SOURCE_URL,'sha256':SOURCE_SHA,'duration_seconds':len(a)/RATE,'samples_48000':1020000},
 'native':{'url':NATIVE_URL,'sha256':NATIVE_SHA,'decoded_audio_duration_seconds':len(b)/RATE,'probe':probe},
 'analysis_sample_rate_hz':RATE,'global_lag_seconds':lag/RATE,
 'global_lag_at_search_boundary':abs(lag)==RATE,
 'aligned_overlap_seconds':n/RATE,'global_correlation':corr(matched_ref,matched_native),
 'linear_gain':gain,'normalized_residual_rms':rms(matched_native-gain*matched_ref)/rms(matched_native),
 'windows':windows,'maximum_local_offset_spread_seconds':max(offsets)-min(offsets),
 'maximum_local_deviation_from_global_seconds':max(abs(x-lag/RATE) for x in offsets),
 'minimum_window_correlation':min(w['correlation'] for w in windows.values()),
 'uncovered_reference_tail':tail_stats,
 'final_word_source_end_seconds':last_word_end,
 'final_word_end_in_native_clock_if_uniform_lag_seconds':last_word_end+lag/RATE,
 'decoded_audio_margin_after_final_word_seconds':len(b)/RATE-(last_word_end+lag/RATE),
 'interpretation_limit':'Signal timing and similarity only. No audible/perceptual voice or mouth-sync match is claimed. Shorter native audio may omit source tail; remux viability requires consistent high waveform correlation across speech windows.'
}
print(json.dumps(result,indent=2))

