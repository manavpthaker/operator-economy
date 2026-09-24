"""Document only native fps conversion for the single P08A LatentSync result."""
import hashlib, json, os, subprocess
from fractions import Fraction
from pathlib import Path
D=Path(__file__).resolve().parents[1];R=next(p for p in D.parents if (p/'.agents').is_dir())
G=D/'repair-latentsync-r1';A=G/'P08r3a';src=A/'restored-native.mp4';out=A/'restored.mp4'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
bind=lambda p:{'path':str(Path(p).relative_to(R)),'sha256':sha(p)}
read=lambda p:json.loads(Path(p).read_text())
def write(p,v):
 with p.open('x')as f:json.dump(v,f,indent=2);f.write('\n')
def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','stream=width,height,r_frame_rate:frame=best_effort_timestamp_time','-of','json',str(p)]))
def framehash(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-i',str(p),'-map','0:v:0','-f','framemd5','-'])
 return [x.decode().split(',')[-1].strip()for x in raw.splitlines()if not x.startswith(b'#')]
term=read(A/'fal/TERMINAL.json');assert sha(src)==term['output']['sha256']
assert not out.exists() and not(A/'FPS-CONFORM.json').exists()
pr=probe(src);fps=Fraction(pr['streams'][0]['r_frame_rate']);assert fps in [Fraction(24),Fraction(25)]
pts=[float(f['best_effort_timestamp_time'])for f in pr['frames']]
assert all(abs(t-i/float(fps))<.000002 for i,t in enumerate(pts)), 'Unexpected source timestamp discontinuity'
assert pts[-1]+1/float(fps) > 172/24, 'Insufficient native coverage of the final required target timestamp'
if fps==24:
 os.link(src,out);cmd=None
else:
 cmd=['ffmpeg','-nostdin','-n','-v','error','-threads','1','-i',str(src),'-map','0:v:0','-map','0:a:0','-vf','fps=24:round=near','-c:v','libx264','-qp','0','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)]
 subprocess.run(cmd,check=True)
op=probe(out);opts=[float(f['best_effort_timestamp_time'])for f in op['frames']]
assert len(opts)>=173 and all(abs(t-i/24)<.000002 for i,t in enumerate(opts))
h0,h1=framehash(src),framehash(out);mapping=[]
for j,h in enumerate(h1):
 candidates=[i for i,x in enumerate(h0)if x==h];assert candidates,'Conform changed decoded picture pixels'
 i=min(candidates,key=lambda k:abs(pts[k]-j/24));assert abs(pts[i]-j/24)<=1/float(fps)+.000002
 mapping.append(i)
assert all(b>=a for a,b in zip(mapping,mapping[1:])), 'Reversal/loop not permitted in fps conform'
record={'record_type':'native_frame_rate_sampling_only','plan':bind(G/'PLAN.json'),'helper':bind(Path(__file__)),'raw_provider_output':bind(src),'conformed':bind(out),'source_fps':str(fps),'source_frames':len(h0),'output_fps':24,'output_frames':len(h1),'output_to_native_frame_map':mapping,'all_decoded_output_frames_match_native':True,'maximum_native_timestamp_sampling_error_seconds':max(abs(pts[i]-j/24)for j,i in enumerate(mapping)),'audio_stream_copied_without_retime':True,'speed_change':False,'manual_hold':False,'source_frame_md5':h0,'output_frame_md5':h1,'command':cmd,'status':'clock_conformed_not_sync_accepted','owner_accepted':False}
write(A/'FPS-CONFORM.json',record);print(json.dumps({k:record[k]for k in ['source_fps','source_frames','output_frames','maximum_native_timestamp_sampling_error_seconds','status']}))
