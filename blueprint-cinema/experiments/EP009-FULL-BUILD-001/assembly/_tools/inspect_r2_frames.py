#!/usr/bin/env python3
"""Extract encoded r2 cue/boundary evidence and compare it to retained sources."""
import json
import math
import subprocess
import sys
from pathlib import Path
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from build_r2 import A, B, ROOT, read, rel, sha, write_new

manifest = read(A / 'BUILD-r2-graphics-only-draft.json')
output = ROOT / manifest['output']
assert sha(output) == manifest['output_sha256']
dest = A / 'qa' / 'r2-graphics-integration'
if dest.exists() and any(p.is_file() for p in dest.rglob('*')):
    raise FileExistsError(f'Refusing to overwrite inspection evidence: {dest}')
dest.mkdir(exist_ok=True)
(dest / 'encoded').mkdir(exist_ok=True)
(dest / 'source').mkdir(exist_ok=True)
rows = manifest['sources']
points, groups = {}, {}

def add(frame, label, group):
    points.setdefault(frame, []).append(label)
    groups.setdefault(group, []).append(frame)

for scene, seed in [('seg004__seg006','seg004'), ('seg020','seg020'), ('seg057__seg058','seg057')]:
    row = next(r for r in rows if r['id'] == seed)
    verification = read(B / 'scenes' / scene / 'qa/r2/VERIFY.json')
    for cue in verification['cue_stills']:
        add(row['out'][0] + cue['frame'], scene + ':' + cue.get('key',cue.get('name')), scene)
changed = {c['segment'] for c in manifest['changes']}
for left, right in zip(rows, rows[1:]):
    if left['id'] in changed or right['id'] in changed:
        group = 'boundaries'
        add(left['out'][1]-1, left['id']+' last before '+right['id'], group)
        add(right['out'][0], right['id']+' first after '+left['id'], group)
for name, sequence in [('eight',range(520,533)), ('twelve',range(556,577))]:
    for frame in sequence:
        add(21680+frame,f'S17 {name} local frame {frame}','transition-'+name)

def extract(path, frames, directory):
    frames = sorted(set(frames))
    # A balanced sum avoids FFmpeg expression-parser recursion limits for the
    # full cue/transition inventory; a left-associated 100-term sum can fail.
    def balanced(terms):
        if len(terms)==1:
            return terms[0]
        mid=len(terms)//2
        return '('+balanced(terms[:mid])+'+'+balanced(terms[mid:])+')'
    expr = balanced([f'eq(n\\,{f})' for f in frames])
    subprocess.run(['ffmpeg','-n','-v','error','-threads','1','-i',str(path),
                    '-an','-vf',f"select='{expr}'",'-fps_mode','passthrough',
                    str(directory/'selected-%05d.png')],check=True)
    files = sorted(directory.glob('selected-*.png'))
    assert len(files)==len(frames),(path,len(files),len(frames))
    mapping = {}
    for frame, file in zip(frames,files):
        target = directory/f'f{frame:05d}.png'
        file.rename(target)
        mapping[frame]=target
    return mapping

encoded = extract(output, points, dest/'encoded')
source_uses, mapping = {}, {}
for frame in sorted(points):
    row = next(r for r in rows if r['out'][0] <= frame < r['out'][1])
    source_frame = row['src_start'] + frame-row['out'][0]
    source_uses.setdefault(row['path'],set()).add(source_frame)
    mapping[frame] = (row,source_frame)
refs={}
for index,(path,frames) in enumerate(source_uses.items()):
    directory=dest/'source'/f'asset-{index:02d}'
    directory.mkdir()
    refs[path]=extract(ROOT/path,frames,directory)

records=[]
for frame in sorted(points):
    row,sf=mapping[frame]
    source=refs[row['path']][sf]
    actual=np.asarray(Image.open(encoded[frame]).convert('RGB'),dtype=np.float32)
    expected=np.asarray(Image.open(source).convert('RGB'),dtype=np.float32)
    delta=np.abs(actual-expected)
    records.append({'output_frame':frame,'time_seconds':frame/24,'segment':row['id'],
                    'labels':points[frame],'encoded_png':rel(encoded[frame]),
                    'source_video':row['path'],'source_frame':sf,'reference_png':rel(source),
                    'mean_absolute_rgb_difference_255':float(delta.mean()),
                    'fraction_pixels_mean_difference_over_20':float((delta.mean(axis=2)>20).mean())})

font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
sheets=[]
for name,frames in groups.items():
    frames=list(dict.fromkeys(frames))
    if name.startswith('transition-'):
        width,height,cols,per_page=1050,75,1,24
    else:
        width,height,cols,per_page=640,390,2,8
    for page in range(math.ceil(len(frames)/per_page)):
        items=frames[page*per_page:(page+1)*per_page]
        sheet=Image.new('RGB',(width*cols,height*math.ceil(len(items)/cols)),(22,22,22))
        draw=ImageDraw.Draw(sheet)
        for index,frame in enumerate(items):
            picture=Image.open(encoded[frame]).convert('RGB')
            if name.startswith('transition-'):
                picture=picture.crop((225,300,1275,345))
            else:
                picture=picture.resize((640,360))
            x,y=(index%cols)*width,(index//cols)*height
            sheet.paste(picture,(x,y))
            text=f'f{frame} / {frame/24:.3f}s / '+', '.join(points[frame])
            draw.text((x+5,y+height-24),text[:86],font=font,fill=(240,240,240))
        path=dest/f'{name}-{page+1:02d}.jpg'
        sheet.save(path,quality=93)
        sheets.append(rel(path))
write_new(dest/'FRAME-COMPARISON.json',{
    'output':{'path':rel(output),'sha256':sha(output)},
    'method':'Exact frame-index selection from encoded full cut and mapped retained source; cue list from replacement VERIFY files; both frames of every boundary touching a changed segment, including following unchanged segments; every frame of the two append transitions.',
    'frames':records,'contact_sheets':sheets,
    'max_mean_absolute_rgb_difference_255':max(r['mean_absolute_rgb_difference_255'] for r in records),
    'max_fraction_pixels_difference_over_20':max(r['fraction_pixels_mean_difference_over_20'] for r in records),
    'limitation':'Comparison detects frame mapping/image changes. No audiovisual, lip-sync, or normal-speed judgment.'})
print(json.dumps({'directory':str(dest),'frames':len(records),'sheets':sheets,
                  'max_mean_absolute_rgb_difference_255':max(r['mean_absolute_rgb_difference_255'] for r in records)},indent=2))
