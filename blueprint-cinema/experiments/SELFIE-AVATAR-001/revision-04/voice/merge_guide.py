import wave,urllib.request,hashlib,json,numpy as np
from pathlib import Path
inputs=[
('original','https://v3b.fal.media/files/b/0aaa2fb4/vxKcTdYdF6jGcYVvUwB_i_selfie-r4-guide-56c013dbff2dd0e1.wav','56c013dbff2dd0e11b59408b5d0e4006cd31ae5ca3d05b847b21e8b17661271f'),
('pickup','https://v3b.fal.media/files/b/0aaa2fcd/sMKc65sHQOYmWWeirMKHl_selfie-r4-pickup-25c5e6b5c9614a9e.wav','25c5e6b5c9614a9e61cea512e24e44d13e943b1e17ee76c89805e7eeb551839d')]
data={}
for label,url,expected in inputs:
 p=Path('/home/user/'+label+'.wav')
 with urllib.request.urlopen(url) as r: p.write_bytes(r.read())
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
 with wave.open(str(p)) as w:
  assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(24000,1,2)
  pcm=w.readframes(w.getnframes())
 data[label]=pcm
def quiet_cut(pcm,preferred):
 a=np.frombuffer(pcm,dtype='<i2'); goal=round(preferred*24000)
 choices=range(goal-240,goal+241)
 pos=min(choices,key=lambda i:(abs(int(a[i]))+abs(int(a[i-1])),abs(i-goal)))
 win=a[pos-480:pos+480].astype(float)/32768.
 return pos,{'sample':pos,'seconds':pos/24000,'adjacent_samples':[int(a[pos-1]),int(a[pos])],'window_40ms_rms':float(np.sqrt(np.mean(win*win)))}
a,ca=quiet_cut(data['original'],47.5)
b,cb=quiet_cut(data['pickup'],5.8)
merged=data['original'][:2*a]+data['pickup'][2*b:]
out=Path('/home/user/r4-corrected-guide.wav')
with wave.open(str(out),'wb') as w:
 w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(merged)
with wave.open(str(out)) as w: check=w.readframes(w.getnframes())
assert check[:2*a]==data['original'][:2*a]
assert check[2*a:]==data['pickup'][2*b:]
print(json.dumps({'merged_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'duration_seconds':len(merged)/48000,
'frame_count':len(merged)//2,'sample_rate_hz':24000,'original_prefix':{'source_start_sample':0,'source_end_sample_exclusive':a,'record_start_sample':0,**ca},
'pickup_suffix':{'source_start_sample':b,'source_end_sample_exclusive':len(data['pickup'])//2,'record_start_sample':a,**cb},
'pcm_prefix_identical':True,'pcm_pickup_suffix_identical':True,'boundary_processing':'None; concatenated near-zero sample boundaries only. Raw pickup endpoint retained.',
'first_new_sentence_record_estimate':a/24000+6.14-b/24000}))

