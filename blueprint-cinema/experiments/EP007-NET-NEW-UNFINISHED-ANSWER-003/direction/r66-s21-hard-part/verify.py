#!/usr/bin/env python3
"""Reproduce the bounded local S21 encode/source checks using FFmpeg and stdlib."""
from pathlib import Path
import array
import hashlib
import json
import math
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[5]
EXP = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
SCENE = EXP / 'hyperframes/reviews/r66-s21-hard-part'
CONTEXT = EXP / 'hyperframes/reviews/r66-s21-context'
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'

def run(cmd):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def audio(path, start, duration):
    raw = run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(path), '-t', str(duration), '-vn', '-af', 'pan=mono|c0=c0', '-ar', '8000', '-f', 'f32le', '-'])
    a = array.array('f'); a.frombytes(raw)
    return a

def correlate(a, b):
    n = min(len(a), len(b)); a = a[:n]; b = b[:n]
    aa = sum(x*x for x in a); bb = sum(x*x for x in b)
    ab = sum(x*y for x,y in zip(a,b))
    return {'samples': n, 'correlation_zero_lag': ab/math.sqrt(aa*bb), 'level_db_vs_master': 10*math.log10(aa/bb)}

def inspect(path, start, duration, frames):
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels', '-of', 'json', str(path)]))
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames'])) == (1280,720,'24/1',frames)
    assert abs(float(video['duration'])-duration)<1e-5
    raw = run(['ffmpeg','-v','error','-xerror','-i',str(path),'-an','-vf','scale=64:36,format=gray','-f','rawvideo','-'])
    size = 64*36; assert len(raw)//size == frames
    sd = []
    for pos in range(0,len(raw),size):
        row=raw[pos:pos+size]; mean=sum(row)/size
        sd.append(math.sqrt(max(0,sum(x*x for x in row)/size-mean*mean)))
    alignment = correlate(audio(path,0,duration),audio(MASTER,start,duration))
    assert alignment['correlation_zero_lag']>.999
    assert abs(alignment['level_db_vs_master'])<.1
    assert not any(x<1 for x in sd)
    return {'path':str(path.relative_to(ROOT)),'sha256':sha(path),'probe':probe,'decoded_frames':frames,'uniform_frames':sum(x<1 for x in sd),'near_uniform_frames_below_sd3':sum(x<3 for x in sd),'minimum_frame_sd':min(sd),'audio':alignment}

with wave.open(str(MASTER),'rb') as f:
    f.setpos(47316000); expected=f.readframes(1472*2000)
with wave.open(str(SCENE/'public/audio/narration.wav'),'rb') as f:
    actual=f.readframes(f.getnframes())
assert expected == actual
check=json.loads((SCENE/'qa/check.json').read_text());assert check['ok'] is True
report={'status':'technical_pass_owner_review_pending','master_sha256':sha(MASTER),'pcm_carve_bit_exact':True,'strict_check':True,'scene':inspect(SCENE/'qa/s21.mp4',985.75,61.33333333333333,1472),'context':inspect(CONTEXT/'qa/context.mp4',977.75,69.33333333333333,1664),'source_sha256':sha(SCENE/'index.html'),'limitations':['No owner acceptance; no audience comprehension claim.','Audio checks establish source alignment and level, not a human listening verdict.','Render and checks are local review output, not canonical picture lock or release.'],'runtime':{'version':'0.8.46','previous_copy_pin':'0.8.46','scope':'new S21 review only','strict_check_passed':True}}
(SCENE/'qa/VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['scene','context']},indent=2))
for key in ['scene','context']:
    x=report[key];print(key,json.dumps({k:v for k,v in x.items() if k!='probe'}))
