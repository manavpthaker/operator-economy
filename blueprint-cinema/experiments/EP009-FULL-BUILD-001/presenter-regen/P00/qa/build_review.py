"""Private P00 QA only; never updates canonical conform, index, or review flags."""
import json, hashlib, subprocess
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parent
P=D.parent
G=P.parent
R=next(p for p in G.parents if (p/'.agents').is_dir())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
run=lambda cmd:subprocess.check_output(cmd)
read=lambda p:json.loads(p.read_text())
write=lambda p,obj:p.write_text(json.dumps(obj,indent=2)+'\n')
a=read(P/'ALIGNMENT.json');start=a['start_frame'];count=86
assert start>=0 and start+count<=int(a['probe']['nb_read_frames'])
plan=read(G/'EXECUTION-PLAN-r5.json');master=R/plan['master']['path'];assert sha(master)==plan['master']['sha256']
out=D/'opening-P00-private-review-r1.mp4'
cmd=['ffmpeg','-n','-v','error','-i',str(P/'restored.mp4'),'-i',str(master),'-filter_complex',f'[0:v]trim=start_frame={start}:end_frame={start+count},setpts=N/(24*TB),scale=1280:720:flags=lanczos,setsar=1,format=yuv420p[v];[1:a]atrim=start_sample=0:end_sample=172000,asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','16','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(out)]
run(cmd)
words=read(G/'opening-first-sentence/P00/WORDS.json')['words'];sheets=[]
for lo in range(0,count,24):
 hi=min(count,lo+24);frames=list(range(start+lo,start+hi));expr='+'.join(f'eq(n,{n})' for n in frames);sheet=D/f'mouth-frames-{lo:02d}-{hi-1:02d}.jpg'
 run(['ffmpeg','-n','-v','error','-i',str(P/'restored.mp4'),'-vf',f"select='{expr}',crop=200:160:530:160,scale=400:320,tile=4x{(len(frames)+3)//4}",'-frames:v','1','-q:v','2',str(sheet)])
 sheets.append({'image':bind(sheet),'output_frames':[lo,hi],'source_frames':frames,'narration_time_range_s':[lo/24,hi/24],'reading_order':'left to right then top to bottom, consecutive original frames; extra tiles black'})
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,sample_rate,channels','-of','json',str(out)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');assert int(v['nb_read_frames'])==count
pcm=lambda f:np.frombuffer(run(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','48000','-f','f32le','-']),'<f4')
x=pcm(P/'audio/narration.wav');y=np.frombuffer(run(['ffmpeg','-v','error','-i',str(out),'-vn','-ac','2','-ar','48000','-f','f32le','-']),'<f4').reshape(-1,2)[:,0]
write(D/'PREVIEW-BINDING.json',{'status':'private_diagnostic_only_not_conformed_for_assembly','preview':bind(out),'source':bind(P/'restored.mp4'),'alignment':bind(P/'ALIGNMENT.json'),'selected_native_offsets':bind(P/'NATIVE-OFFSETS-SELECTION.json'),'source_frames':[start,start+count],'output_frames':[0,count],'source_rate_and_output_rate':24,'padding_or_speed_change':False,'master':plan['master'],'master_sample_range':[0,172000],'command':cmd})
write(D/'VERIFY.json',{'preview':bind(out),'probe':probe,'frames_ok':True,'original_narration_samples':len(x),'decoded_AAC_samples':len(y),'zero_lag_corr':float(np.corrcoef(x,y[:len(x)])[0,1]),'rms_vs_master_db':float(20*np.log10(np.sqrt(np.mean(y[:len(x)]**2))/np.sqrt(np.mean(x**2)))),'limitation':'Frame/audio identity checks do not establish lip sync.'})
write(D/'PHONEME-FRAMES.json',{'source':bind(P/'restored.mp4'),'crop_source_xywh':[530,160,200,160],'sheets':sheets,'words':words,'word_timing_limitation':'These are approximate retained forced-alignment word boundaries, not precise phoneme timings.'})
D.joinpath('REVIEW.html').write_text('''<!doctype html><meta charset="utf-8"><title>EP009 opening P00 review</title><style>body{margin:32px;background:#eeeade;color:#202020;font:17px system-ui;max-width:1100px}video{display:block;width:100%;background:#111}button{padding:10px 16px;margin:8px 8px 8px 0;font:inherit}output{font-variant-numeric:tabular-nums}</style><h1>Opening P00 — review pending</h1><p>Exact first sentence, 86 frames / 3.5833 seconds. Original narration; no picture retiming, padding or freeze. Private diagnostic preview, not an assembly select.</p><video id="v" controls preload="auto" src="opening-P00-private-review-r1.mp4"></video><button onclick="v.currentTime=0;v.playbackRate=1;v.play()">Play opening at 1×</button><button onclick="v.pause()">Pause</button><output id="state"></output><p>“An innkeeper with twenty rooms is closing out a reservation.” Review the first audible syllable, innkeeper, rooms, and the final word. Passing audio identity does not certify lip sync.</p><script>const v=document.getElementById('v');function tick(){document.getElementById('state').value=`${v.currentTime.toFixed(3)} / ${v.duration?.toFixed(3)} s · ${v.playbackRate}× · ${v.paused?'paused':'playing'} · ended=${v.ended}`;requestAnimationFrame(tick)}tick()</script>''')
print(json.dumps({'preview':bind(out),'frames':count,'source_frames':[start,start+count],'sheets':len(sheets)}))
