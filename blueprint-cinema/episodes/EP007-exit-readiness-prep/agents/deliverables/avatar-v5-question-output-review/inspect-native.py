#!/usr/bin/env python3
"""Local native-performance samples only; no audio restoration or runtime writes."""
from pathlib import Path
import hashlib
import io
import json
import math
import subprocess

from PIL import Image, ImageDraw

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).resolve().parent
WORK = REPO / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/avatar-v5-question-output-review.json'
work = json.loads(WORK.read_text())
for pin in work['inputs']:
    assert hashlib.sha256((REPO / pin['path']).read_bytes()).hexdigest() == pin['sha256'], pin['path']
baseline = REPO / work['inputs'][1]['path']
native = REPO / work['inputs'][2]['path']

def frame(path, t):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(path), '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', '-'])
    return Image.open(io.BytesIO(data)).convert('RGB')

def sheet(path, times, name, crop=None):
    width, height, caption = 480, 270, 24
    image = Image.new('RGB', (width * 3, (height + caption) * math.ceil(len(times) / 3)), '#eeeae2')
    for i, t in enumerate(times):
        current = frame(path, t)
        if crop:
            w, h = current.size
            current = current.crop(tuple(int(value * size) for value, size in zip(crop, [w,h,w,h])))
        current.thumbnail((width, height))
        x, y = (i % 3) * width, (i // 3) * (height + caption)
        image.paste(current, (x + (width-current.width)//2, y + (height-current.height)//2))
        ImageDraw.Draw(image).text((x+8,y+height+6), f'{name}: local {t:.3f}s', fill='black')
    target = OUT / f'{name}.jpg'
    image.save(target, quality=95)
    return {'path':str(target.relative_to(REPO)), 'sha256':hashlib.sha256(target.read_bytes()).hexdigest(), 'times_seconds':times, 'crop_fraction':crop}

probes = {}
for label, path in [('accepted_v5',baseline),('question_native',native)]:
    probes[label] = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
decode = subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(native),'-map','0','-f','null','-'],capture_output=True)
contacts = [
    sheet(baseline,[0,3,6,9,12,15,18,20,20.9],'accepted-v5-overview'),
    sheet(native,[0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7],'question-early-middle'),
    sheet(native,[7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.25,12.5,12.75,13],'question-late-ending'),
    sheet(native,[0,1,2,3,4,5,6,7,8,9,10,11,12,12.5,13],'question-hand-detail',(.20,.43,.82,1)),
]
result={'input_hashes':work['inputs'],'probes':probes,'native_full_decode':{'exit_code':decode.returncode,'stderr':decode.stderr.decode()},'contacts':contacts,'native_speech_is_regenerated':True,'final_lip_sync_review':'not_run; original narration restoration belongs to root','owner_acceptance_claimed':False}
(OUT/'evidence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'decode':result['native_full_decode'],'contacts':[x['path'] for x in contacts]}))
