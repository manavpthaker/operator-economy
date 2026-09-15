#!/usr/bin/env python3
"""Local-only R31 question diagnostic; all outputs stay beside this script."""
from pathlib import Path
import hashlib, io, json, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).resolve().parent
WORK = REPO / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/r32-question-sync-diagnosis.json'
W = json.loads(WORK.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args): return subprocess.check_output(args)
def probe(p): return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
for pin in W['inputs']:
    assert sha(REPO/pin['path']) == pin['sha256'], pin['path']
restored, selected, master, transcript = [REPO/W['inputs'][i]['path'] for i in [2,4,5,6]]
project = selected.parents[2]
market = project/'public/audio/seller-market-narration.wav'
RATE=48000
def wave_slice(path, start, count):
    with wave.open(str(path),'rb') as f:
        assert (f.getnchannels(),f.getsampwidth(),f.getframerate()) == (1,2,RATE)
        f.setpos(start); return f.readframes(count)
pcm = wave_slice(master,134*RATE,614000)
assert pcm == wave_slice(market,int(59.5*RATE),614000), 'Actual R31 narration differs'
wav=OUT/'question-original-exact.wav'
with wave.open(str(wav),'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE); f.writeframes(pcm)
print('All input pins and actual R31 audio PCM mapping match.',flush=True)

video=OUT/'question-local-r31-original-audio.mp4'
filters=('[0:v]split=2[a][b];'
 '[a]trim=start_frame=8:end_frame=223,setpts=PTS-STARTPTS,scale=1280:720:flags=lanczos,setsar=1[w];'
 '[b]trim=start_frame=223:end_frame=315,setpts=PTS-STARTPTS,scale=1818:1022:flags=lanczos,crop=1280:720:269:22:exact=1,setsar=1[c];'
 '[w][c]concat=n=2:v=1:a=0[v]')
cmd=['ffmpeg','-v','error','-n','-i',str(selected),'-i',str(wav),'-filter_complex',filters,
 '-map','[v]','-map','1:a:0','-c:v','libx264','-crf','19','-preset','fast','-pix_fmt','yuv420p',
 '-fps_mode','passthrough','-c:a','alac','-movflags','+faststart',str(video)]
subprocess.run(cmd,check=True)
decoded_pcm=run(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-f','s16le','-acodec','pcm_s16le','-'])
assert decoded_pcm==pcm, 'Lossless standalone audio mismatch'
print('Standalone MP4 created; decoded ALAC exactly equals original PCM.',flush=True)

def decoded_audio(p):
    return np.frombuffer(run(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype='<f4').astype(np.float64)
ref=decoded_audio(wav); candidate=decoded_audio(restored); rate=16000
audio_windows=[]
for lo,hi in [(0.1,2.5),(4.2,7.2),(9.1,11.9)]:
    a=ref[round(lo*rate):round(hi*rate)]
    first=max(0,round((lo-.15)*rate)); last=min(len(candidate),round((hi+.8)*rate))
    b=candidate[first:last]
    size=1<<(len(a)+len(b)-2).bit_length()
    conv=np.fft.irfft(np.fft.rfft(b,size)*np.fft.rfft(a[::-1],size),size)
    begin=len(a)-1;end=len(b)
    offset=int(np.argmax(conv[begin:end]))
    lag=(first+offset)/rate-lo
    corr=float(np.corrcoef(a,b[offset:offset+len(a)])[0,1])
    audio_windows.append({'reference_window':[lo,hi],'restored_insertion_seconds':lag,'aligned_correlation':corr})

def frame_audit(p):
    raw=run(['ffmpeg','-v','error','-i',str(p),'-an','-vf','scale=320:180,format=gray','-f','rawvideo','-'])
    frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,180,320)
    mad=np.mean(np.abs(frames[1:].astype(np.int16)-frames[:-1].astype(np.int16)),axis=(1,2))
    pts=json.loads(run(['ffprobe','-v','error','-select_streams','v','-show_frames','-show_entries','frame=best_effort_timestamp_time,pkt_duration_time','-of','json',str(p)]))['frames']
    times=np.array([float(f['best_effort_timestamp_time']) for f in pts])
    digest=run(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-f','framemd5','-']).decode()
    hashes=[line.split(',')[-1].strip() for line in digest.splitlines() if line and not line.startswith('#')]
    repeats=[i for i in range(1,len(hashes)) if hashes[i]==hashes[i-1]]
    return frames,{'frames':len(frames),'exact_adjacent_repeat_frame_indices':repeats,
      'near_static_adjacent_frame_indices_gray_MAD_under_0_02':[int(i+1) for i in np.where(mad<.02)[0]],
      'frame_pts_first':float(times[0]),'frame_pts_last':float(times[-1]),
      'frame_interval_min':float(np.min(np.diff(times))),'frame_interval_max':float(np.max(np.diff(times))),
      'frame_interval_deviations_over_2_microseconds':int(np.count_nonzero(np.abs(np.diff(times)-1/24)>.000002)),
      'frame_hashes':hashes,'adjacent_gray_MAD':mad.tolist()}

fa={};arrays={};probes={};decodes={}
for name,p in [('restored',restored),('selected_with_pause',selected),('standalone',video)]:
    probes[name]=probe(p)
    d=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],capture_output=True)
    decodes[name]={'exit_code':d.returncode,'stderr':d.stderr.decode()}
    arrays[name],fa[name]=frame_audit(p)
    print(name+' frame/decode audit finished.',flush=True)
frame_map=[]
for delta in range(-2,3):
    a=arrays['restored'];b=arrays['selected_with_pause'];start=max(8,8-delta);end=min(297,297-delta)
    error=float(np.mean(np.abs(a[start:end].astype(np.int16)-b[start+delta:end+delta].astype(np.int16))))
    frame_map.append({'selected_minus_restored_frames':delta,'gray_MAD':error})

words=json.loads(transcript.read_text())['words']
question_words=[w for w in words if 134<=w['start']<146.792]
def picture(t):
    frame_number=round(t*24)
    seek=max(0,frame_number/24-0.00001)
    b=run(['ffmpeg','-v','error','-ss',f'{seek:.9f}','-i',str(selected),'-frames:v','1','-f','image2pipe','-c:v','png','-'])
    return Image.open(io.BytesIO(b)).convert('RGB')
contacts=[]
for name,times,crop in [
 ('question-viseme-early',[4.125,4.208333,4.291667,4.375,4.458333,6.583333,6.666667,6.75,6.833333,6.916667],(760,110,1150,390)),
 ('question-viseme-late',[9.958333,10.041667,10.125,10.208333,10.291667,10.666667,10.75,10.833333,10.916667,11],(760,110,1150,390)),
 ('question-pause-end',[0,2.375,2.75,3.125,8.916667,8.958333,9,11.75,12,12.041667,12.375,12.75],None)]:
    width,height,caption=390,280,34
    sheet=Image.new('RGB',(5*width,math.ceil(len(times)/5)*(height+caption)),'#eeeae2')
    for i,t in enumerate(times):
        im=picture(t+8/24)
        if crop: im=im.crop(crop)
        im.thumbnail((width,height))
        x=i%5*width;y=i//5*(height+caption)
        sheet.paste(im,(x+(width-im.width)//2,y+(height-im.height)//2))
        ImageDraw.Draw(sheet).text((x+5,y+height+4),f'local {t:.3f}  master {t+134:.3f}',fill='black')
    path=OUT/(name+'.jpg');sheet.save(path,quality=95)
    contacts.append({'path':str(path.relative_to(REPO)),'sha256':sha(path),'selected_timeline_sample_seconds':times,'source_frame_indices':[round(t*24)+8 for t in times],'source_offset_seconds':8/24,'crop_pixels':crop})

result={'issued_inputs':W['inputs'],'additional_inputs':[{'path':str(market.relative_to(REPO)),'sha256':sha(market)}],
 'mapping':{'review_in':131,'master_in':134,'source_in_frames':8,'fps':24,'selected_frames':307,
 'close_crop_local_seconds':215/24,'close_scale':1.42,'close_translation_xy':[-268.8,-22],
 'standalone_crop_approximation':'1818x1022 scale then exact pixel crop x269,y22 to1280x720; CSS equivalent within1 output pixel',
 'hold_local_begin':289/24,'hold_frames':18,'master_out':134+307/24},
 'audio':{'reference_sample_range':[6432000,7046000],'reference_pcm_sha256':hashlib.sha256(pcm).hexdigest(),
 'actual_R31_market_PCM_identical':True,'standalone_decoded_ALAC_PCM_identical':True,
 'restored_waveform_independent_windows':audio_windows,'interpretation':'Waveform placement is not a visual lip-sync measurement.'},
 'probes':probes,'full_decodes':decodes,'frame_audits':fa,'source_picture_alignment_candidates':frame_map,
 'question_words':question_words,'contacts':contacts,'standalone_command':cmd,
 'standalone_sha256':sha(video),'standalone_bytes':video.stat().st_size,
 'final_perceptual_sync_verdict':'not established; sampled visemes only','owner_acceptance_claimed':False}
(OUT/'evidence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'audio_windows':audio_windows,'mapping':result['mapping'],'frame_alignment':frame_map,'standalone':str(video)}),flush=True)
