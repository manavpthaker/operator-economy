#!/usr/bin/env python3
"""Bind the authorized continuous V4 take; generate deterministic HyperFrames HTML.
Audio insertion placement is not an AV-sync measurement. No provider calls.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, subprocess
from fractions import Fraction

BASE = Path(__file__).resolve().parent
PROJECT = BASE / 'project'
REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
EXP = REPO / 'blueprint-cinema/experiments/EP007-PRESENTER-001'
LOCKS = {
 'acceptance': (EXP/'avatar-v3-lock/ACCEPTANCE.json', '5b6fa0fb68b5aeb470e681515ec49b4dcbbb00dcfe861666187bb918662b08dc'),
 'wide_still': (EXP/'avatar-v4-wide/media/wide-study-reference.png', '5c282925447ff8227ea66dcafa60e5b9cf5913aa5cbb565037fb4e0a2d1cbb82'),
 'approved_wav': (EXP/'avatar-v3-lock/media/approved-opening-00m00s-00m20.9s.wav', 'cc7e6927c34baae9f998d65f3f9ab1274d3ab73e2acf5d3b7c18d0a2c05d529d'),
}
FPS = 24

def sha(path):
 h = hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
 return h.hexdigest()

def stage(source, destination):
 destination.parent.mkdir(parents=True, exist_ok=True)
 if source.resolve() != destination.resolve(): shutil.copy2(source, destination)
 return sha(destination)

def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

ap=argparse.ArgumentParser(description=__doc__)
g=ap.add_mutually_exclusive_group(required=True)
g.add_argument('--still-study', action='store_true')
g.add_argument('--source',type=Path,help='Final restored continuous V4 MP4, never a generated-native soundtrack.')
ap.add_argument('--audio-insertion-offset',type=float,help='Measured original WAV insertion placement in restored container; not AV sync.')
ap.add_argument('--crop-scale',type=float,default=1.30)
ap.add_argument('--wide-scale',type=float,default=1.004,help='Top-anchored 0.4 percent overscan removes corrupted source bottom rows.')
ap.add_argument('--crop-y',type=float,default=0.0,help='Pixel translation after top-anchored scaling; default preserves headroom.')
a=ap.parse_args()
if not 1.0 <= a.wide_scale <= 1.005: ap.error('Wide cleanup overscan is limited to 0.5 percent.')
if not 1.30 <= a.crop_scale <= 1.40: ap.error('Authorized crop range is 1.30 to 1.40.')
if abs(a.crop_y)>100: ap.error('Crop translation beyond 100px needs actual-frame reassessment.')
inputs={}
for key,(p,expected) in LOCKS.items():
 actual=sha(p)
 if actual!=expected: raise SystemExit(f'LOCK HASH MISMATCH: {key}')
 inputs[key]={'path':str(p),'sha256':actual}
assets=PROJECT/'assets'
assets.mkdir(parents=True,exist_ok=True)
lib=EXP/'study-composite-r10/assets/vendor/gsap.min.js'
libsha=stage(lib,assets/'vendor/gsap.min.js')
if a.still_study:
 source=LOCKS['wide_still'][0]
 stage(source,assets/'wide-study-reference.png')
 stage(LOCKS['approved_wav'][0],assets/'approved-opening.wav')
 status='STILL_STUDY_NOT_GENERATED_VIDEO'
 media='<img id="continuous-picture" src="assets/wide-study-reference.png" alt="Supplied wider reference still: composition study only" />'
 audio_src='assets/approved-opening.wav'
 offset=0.0
 frames=504
 audio_duration=20.9
 source_info={'path':str(source),'sha256':sha(source),'kind':'supplied_generated_still','actual_video_bound':False}
else:
 if a.audio_insertion_offset is None: ap.error('--audio-insertion-offset is required for actual restored video binding.')
 source=a.source.expanduser().resolve()
 p=probe(source)
 vs=[s for s in p['streams'] if s['codec_type']=='video']
 aus=[s for s in p['streams'] if s['codec_type']=='audio']
 if len(vs)!=1 or not aus: raise SystemExit('Expected one video stream and an original-narration-restored audio stream.')
 v=vs[0]
 if (v['width'],v['height'])!=(1920,1080): raise SystemExit('Expected 1920x1080 input; do not silently upscale a different result.')
 if Fraction(v['avg_frame_rate'])!=24 or Fraction(v['r_frame_rate'])!=24: raise SystemExit('Expected constant 24fps source; assess before converting.')
 frames=int(v.get('nb_frames') or round(float(v['duration'])*FPS))
 audio_duration=min(frames/FPS,float(aus[0].get('duration') or p['format']['duration']))
 offset=a.audio_insertion_offset
 if abs(offset)>2: raise SystemExit('Insertion placement outside ±2s analysis range.')
 if frames/FPS < 20.9+offset-1/FPS: raise SystemExit('Source would lose the approved audio tail; inspect before binding.')
 stage(source,assets/'source-restored.mp4')
 status='RESTORED_VIDEO_BOUND_PENDING_RENDER_QA'
 media='<video id="continuous-picture" class="clip" src="assets/source-restored.mp4" data-start="0" data-duration="DURATION" data-media-start="0" data-playback-rate="1" data-track-index="1" muted playsinline preload="auto"></video>'
 audio_src='assets/source-restored.mp4'
 source_info={'path':str(source),'sha256':sha(source),'kind':'generated_video_original_narration_restored','actual_video_bound':True,'probe':p}
duration=frames/FPS
cut_frame=math.floor((17.96+offset)*FPS)-3
cut_sec=cut_frame/FPS
if not 0 < cut_frame < frames: raise SystemExit('Question cut falls outside the source.')
media=media.replace('DURATION',str(duration))
shot_timing = f'class="clip" data-start="0" data-duration="{duration}" data-track-index="0"' if a.still_study else ''
binding={
 'status':status,'composition':{'width':1920,'height':1080,'fps':FPS,'frames':frames,'duration':duration},
 'inputs':inputs,'source':source_info,'vendor':{'source':str(lib),'staged_path':'assets/vendor/gsap.min.js','sha256':libsha},
 'crop':{'wide_scale':a.wide_scale,'wide_cleanup_reason':'Remove corrupted final rows present in the provider-restored source','scale':a.crop_scale,'transform_origin':'50% 0%','x':0,'y':a.crop_y,'cut_frame_zero_based':cut_frame,'cut_seconds':cut_sec,'gsap_set_seconds':cut_sec-0.000001,'boundary_epsilon_seconds':0.000001,'transition':'hard set, zero duration'},
 'timing':{'master_question_start':17.96,'master_question_end':20.34,'master_audio_end':20.9,'audio_insertion_offset_seconds':offset,'offset_interpretation':'Waveform insertion placement in restored container; NOT measured audiovisual sync','cut_rule':'floor((17.96 + audio_insertion_offset_seconds) * 24) - 3'},
 'continuity':{'video_elements':0 if a.still_study else 1,'audio_elements':1,'source_start':0,'source_rate':1,'audio_fades':False,'audio_processing':False,'narration_trim':False,'audio_slot_duration':audio_duration},
 'pending':['Inspect actual moving frames and crop headroom','Canonical HyperFrames render and media/audio QA'] if not a.still_study else ['Actual generated and restored V4 video','Measured audio insertion placement','Final crop review','Canonical render and final media/audio QA']
}
(PROJECT/'binding.json').write_text(json.dumps(binding,indent=2)+'\n')
html=f'''<!doctype html>
<html lang="en" data-resolution="landscape">
<head><meta charset="utf-8"><meta name="viewport" content="width=1920, height=1080">
<title>EP007 V4 wider opening review</title>
<script src="assets/vendor/gsap.min.js"></script>
<style>
* {{box-sizing:border-box;margin:0;padding:0}}
html,body,#root {{width:1920px;height:1080px;overflow:hidden;background:#000}}
.clip {{position:absolute;inset:0;width:1920px;height:1080px}}
#crop-wrapper {{position:absolute;inset:0;width:1920px;height:1080px}}
#continuous-picture {{display:block;width:1920px;height:1080px;object-fit:cover}}
</style></head>
<body>
<!-- {status}. Source and soundtrack remain continuous. Crop is visual only. -->
<div id="root" data-composition-id="ep007-avatar-v4" data-start="0" data-duration="{duration}" data-width="1920" data-height="1080" data-fps="24">
<section id="continuous-shot" {shot_timing}>
<div id="crop-wrapper" data-layout-allow-overflow>{media}</div>
</section>
<audio id="continuous-narration" src="{audio_src}" data-start="0" data-duration="{audio_duration}" data-media-start="0" data-playback-rate="1" data-track-index="10" preload="auto"></audio>
</div>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set('#crop-wrapper',{{scale:{a.wide_scale},x:0,y:0,transformOrigin:'50% 0%'}},0);
tl.addLabel('buyer-question-close',{cut_sec});
tl.set('#crop-wrapper',{{scale:{a.crop_scale},x:0,y:{a.crop_y},transformOrigin:'50% 0%'}},{cut_sec-0.000001});
window.__timelines=window.__timelines||{{}};
window.__timelines['ep007-avatar-v4']=tl;
</script>
</body></html>
'''
(PROJECT/'index.html').write_text(html)
# Pose boundaries are verified with explicit canonical snapshots and actual rendered frames.
print(json.dumps({'status':status,'source_sha256':source_info['sha256'],'duration':duration,'frames':frames,'cut_frame':cut_frame,'cut_seconds':cut_sec,'crop_scale':a.crop_scale},indent=2))
