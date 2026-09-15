from pathlib import Path
import subprocess, json, hashlib, datetime
import numpy as np
from PIL import Image, ImageDraw

Q=Path(__file__).resolve().parent
V=Q.parent
video=Q/'r39-full-review.mp4'
run=lambda args:subprocess.check_output(['ffmpeg','-v','error']+args)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
stream=next(s for s in probe['streams'] if s['codec_type']=='video')
assert stream['r_frame_rate']=='24/1' and int(stream['nb_frames'])==7047
assert abs(float(probe['format']['duration'])-293.625)<.001
raw=run(['-i',str(video),'-vf','select=gte(n\\,5943),scale=128:72,format=gray','-fps_mode','passthrough','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(-1,72,128)
assert len(frames)==1104
std=frames.std(axis=(1,2));blanks=np.flatnonzero(std<2).tolist()
assert not blanks, blanks
rate=48000
actual=np.frombuffer(run(['-i',str(video),'-vn','-ar',str(rate),'-ac','1','-f','f32le','-']),'<f4').astype(float)
expected=np.frombuffer(run(['-i',str(V/'public/audio/owner-dependency-his-r39.wav'),'-ar',str(rate),'-ac','1','-f','f32le','-']),'<f4').astype(float)
start=round(247.625*rate);section=actual[start:start+len(expected)]
corr=float(np.corrcoef(section,expected)[0,1]);assert corr>.995,corr
samples=[0,5942,5943,5989,5990,5991,6116,6117,6118,6201,6255,6435,6609,6843,6999]
filt='select='+ '+'.join('eq(n\\,%d)'%n for n in samples)+',scale=384:216'
raw=run(['-i',str(video),'-vf',filt,'-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-'])
selected=np.frombuffer(raw,np.uint8).reshape(-1,216,384,3)
assert len(selected)==len(samples)
contact=Image.new('RGB',(384*3,242*5),'#173530');draw=ImageDraw.Draw(contact)
for i,(n,a) in enumerate(zip(samples,selected)):
    x,y=(i%3)*384,(i//3)*242
    contact.paste(Image.fromarray(a),(x,y))
    draw.text((x+8,y+222),f'Frame {n} | {n/24:.3f}s',fill='white')
contact.save(Q/'encoded-cut-contact.jpg',quality=93)
record={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration_seconds':float(probe['format']['duration']),'fps':stream['r_frame_rate'],'frames':int(stream['nb_frames']),'sample_frames':samples,'new_scene_frames_scanned':len(frames),'uniform_blank_frames':len(blanks),'minimum_frame_luma_std':float(std.min()),'audio_correlation_versioned_s08':corr,'limits':['Uniform-blank scan does not measure semantic clarity.','Audio correlation checks source placement, not perceptual lip sync or timbre.','New performance and animation await owner review.']}
(Q/'ENCODED-VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
