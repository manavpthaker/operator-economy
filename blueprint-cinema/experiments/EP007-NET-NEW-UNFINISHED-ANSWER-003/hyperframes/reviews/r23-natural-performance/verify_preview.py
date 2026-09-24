"""Verify private R23 continuity, baseline preservation and runtime manifest."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'r22-continuous-closeups'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((ROOT/'BASELINE-PINS.json').read_text())
for rel,digest in pins.items():
    assert sha(OLD/rel)==digest,('baseline changed',rel)
excluded={'index.html','public/media/post-title-a.mp4','public/media/post-title-b.mp4'}
retained={rel:digest for rel,digest in pins.items() if rel not in excluded}
for rel,digest in retained.items():assert sha(ROOT/rel)==digest,('retained file changed',rel)

class Clips(HTMLParser):
    def __init__(self,s):
        super().__init__();self.tags=[];self.feed(s)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'data-start' in d:self.tags.append((tag,d))
old=Clips((OLD/'index.html').read_text()).tags
new=Clips((ROOT/'index.html').read_text()).tags
old_unchanged=[t for t in old if t[1].get('id') not in {'root','post-title-definition','post-title-promise'}]
new_unchanged=[t for t in new if t[1].get('id') not in {'root','post-title-continuous'}]
assert old_unchanged==new_unchanged,'prior clips or narration declarations changed'
post=[d for t,d in new if d.get('id')=='post-title-continuous']
assert len(post)==1
assert tuple(post[0][k] for k in ['data-start','data-duration','data-media-start'])==('56.5','15','0')
assert 'post-title-a.mp4' not in (ROOT/'index.html').read_text()
assert 'post-title-b.mp4' not in (ROOT/'index.html').read_text()
assert all(k not in dict(post[0]) for k in ('loop','autoplay'))
root=[d for t,d in new if d.get('id')=='root'][0]
assert root['data-duration']=='71.5' and root['data-fps']=='24'
asset=ROOT/post[0]['src'];assert asset.is_file()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(asset)]))
video=[s for s in probe['streams'] if s['codec_type']=='video']
assert len(video)==1 and not any(s['codec_type']=='audio' for s in probe['streams'])
v=video[0]
assert int(v['nb_read_frames'])==375 and v['avg_frame_rate']=='25/1'
assert abs(float(v['duration'])-15)<.001
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(asset),'-map','0:v:0','-f','null','-'],check=True,capture_output=True)
files={**retained,'index.html':sha(ROOT/'index.html'),post[0]['src']:sha(asset)}
report={'ok':True,'baseline_files_unchanged':len(pins),'retained_runtime_files_byte_identical':len(retained),'runtime_files':len(files),'prior_clip_and_audio_declarations_identical':True,'duration_seconds':71.5,'fps':24,'picture_frames':1716,'post_title_video_elements':1,'post_title_source_seconds':[0,15],'post_title_review_seconds':[56.5,71.5],'crop_cut_times_seconds':[62.916666666666664,67.91666666666667],'native_video_frames':375,'native_video_fps':25,'native_video_seconds':15,'generated_audio_in_preview':False,'narration_changed':False,'perceptual_lip_sync_certified':False,'scope':'isolated private presenter audition'}
(ROOT/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'RUNTIME-FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps(report))
