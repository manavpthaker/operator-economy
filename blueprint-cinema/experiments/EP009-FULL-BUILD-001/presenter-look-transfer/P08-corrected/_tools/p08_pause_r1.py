"""One explicitly authorized offline picture-only pause comparison. No provider or full P08 output."""
import datetime,hashlib,json,os,subprocess,wave
from pathlib import Path
R=Path.cwd();D=R/'blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/P08-corrected'
G=D/'repair-pause-r1';A=G/'P08r3a';S=D/'repair-v2pro-r1/P08r3a';A.mkdir(parents=True,exist_ok=True);(A/'audio').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();bind=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
def write(p,v):
 with p.open('x')as f:json.dump(v,f,indent=2);f.write('\n')
source=S/'restored.mp4';audio=S/'audio/narration.wav';master=D.parents[1]/'assembly/r3/narration-master-r3.wav'
assert sha(source)=='aa3116b568c11ab29d591476cea8df1281d63000c7fce4b429aabe0b082302d2'
assert sha(audio)=='a743f1e4c218b9d75ea4d2238c9a8e2a4b9878ad949480c5fd23d755a4e2e02c'
with wave.open(str(master),'rb')as w:w.setpos(31840000);pcm=w.readframes(346000)
with wave.open(str(audio),'rb')as w:assert w.getnframes()==346000 and w.readframes(346000)==pcm
os.link(audio,A/'audio/narration.wav')
mapping=list(range(107))+[106]*4+list(range(107,169));assert len(mapping)==173
auth={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'Root current explicit bounded technical direction','instruction_exact':"LatentSync targeted sync still held; do not extend tail. Instead root authorizes ONE offline P08A v2/pro picture-only pause-repair candidate previously proposed: original[0,107)+4 copies frame106+original[107,169)=173; exact locked PCM unchanged. This is sole new P08 performance exception, never any of14preserved takes. Preserve failed artifacts/gates; document4frame quiet-pause insertion and neutral169–172discard. Do not conform fullP08 until graphic reviews dense onset and last out plus wholeA. This is comparison candidate technical authority only. No paid calls.",'owner_accepted':False,'provider_calls':0}
write(G/'AUTHORIZATION.json',auth)
graph='[0:v]split=3[s0][s1][s2];[s0]trim=start_frame=0:end_frame=107,setpts=N/(24*TB)[v0];[s1]trim=start_frame=106:end_frame=107,setpts=N/(24*TB),tpad=stop_mode=clone:stop=3[v1];[s2]trim=start_frame=107:end_frame=169,setpts=N/(24*TB)[v2];[v0][v1][v2]concat=n=3:v=1:a=0,setpts=N/(24*TB)[v]'
cmd=['ffmpeg','-nostdin','-n','-v','error','-threads','1','-i',str(source),'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-qp','0','-preset','fast','-threads','2','-pix_fmt','yuv420p','-r','24','-movflags','+faststart',str(A/'picture.mp4')]
plan={'record_type':'one_offline_P08A_pause_comparison','status':'prepared_not_accepted','authority':bind(G/'AUTHORIZATION.json'),'source':bind(source),'narration':bind(audio),'master':bind(master),'master_samples':[31840000,32186000],'master_frames':[15920,16093],
 'frames':173,'fps':24,'output_to_source_frames':mapping,'prefix':[0,107],'extra_hold_source_frame':106,'extra_hold_output_range':[107,111],'post_source_range':[107,169],'discarded_neutral_source_frames':[169,173],
 'whole_second_sentence_delay_seconds':4/24,'voice_samples_changed':False,'previous_failures':{'v2_gate':bind(S/'SYNC-GATE.json'),'v2_independent_review':bind(S/'independent-sync-review/INDEPENDENT-SYNC-REVIEW.json')},
 'speech_sync_claim':False,'existing14performances_modified':False,'full_P08_conform_allowed':False,'owner_accepted':False,'helper':bind(Path(__file__).resolve()),'command':cmd}
write(G/'PLAN.json',plan);subprocess.run(cmd,check=True)
def hashes(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-i',str(p),'-map','0:v:0','-f','framemd5','-'])
 return[line.decode().split(',')[-1].strip()for line in raw.splitlines()if not line.startswith(b'#')]
h0,h1=hashes(source),hashes(A/'picture.mp4');assert len(h0)==len(h1)==173 and [h0[i]for i in mapping]==h1
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','stream=r_frame_rate,width,height:frame=best_effort_timestamp_time','-of','json',str(A/'picture.mp4')]))
assert probe['streams'][0]['r_frame_rate']=='24/1';pts=[float(f['best_effort_timestamp_time'])for f in probe['frames']];assert len(pts)==173 and max(abs(t-i/24)for i,t in enumerate(pts))<.000002
write(A/'SOURCE-FRAME-MAP.json',{'plan':bind(G/'PLAN.json'),'source':bind(source),'picture':bind(A/'picture.mp4'),'output_to_source_frames':mapping,'source_frame_md5':h0,'output_frame_md5':h1,'decoded_frames_exactly_match_map':True,'fps':24,'frames':173,'max_pts_error_seconds':max(abs(t-i/24)for i,t in enumerate(pts))})
preview=A/'P08A-pause-r1-exact-master-review.mp4'
pcmd=['ffmpeg','-nostdin','-n','-v','error','-threads','1','-i',str(A/'picture.mp4'),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-vf','scale=1280:720:flags=lanczos','-c:v','libx264','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','256k','-movflags','+faststart',str(preview)]
subprocess.run(pcmd,check=True)
record={'record_type':'offline_pause_comparison_ready','status':'pending_independent_whole_A_and_onset_tail_review','plan':bind(G/'PLAN.json'),'picture':bind(A/'picture.mp4'),'source_frame_map':bind(A/'SOURCE-FRAME-MAP.json'),'exact_narration':bind(A/'audio/narration.wav'),'preview':bind(preview),'source_clock':'target24fpsframe0 corresponds to narration sample0; picture map explicitly modifies only the authorized new P08A performance','owner_accepted':False,'full_P08_conform':False,'provider_calls':0,'preview_command':pcmd}
write(A/'CANDIDATE.json',record);print(json.dumps({'plan':record['plan'],'picture':record['picture'],'preview':record['preview'],'frames':173,'status':record['status']}))
