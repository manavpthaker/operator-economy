import json, subprocess, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

B = '/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP009-FULL-BUILD-001'
A = B + '/assembly'
SRC = A + '/qa/ep009-full.mp4'
rows = json.load(open(A + '/_tools/sources.json'))
fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 14)
os.makedirs(A + '/qa/contact', exist_ok=True)
scenes = []
for r in rows:
    if not scenes or scenes[-1]['scene'] != r['scene']:
        scenes.append({'scene': r['scene'], 'f0': r['out'][0], 'segs': []})
    scenes[-1]['f1'] = r['out'][1]
    scenes[-1]['segs'].append(r)
TW, TH, COLS = 256, 144, 8
out = []
ALLRAW = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', SRC, '-map', '0:v:0', '-vf', f"select='not(mod(n\\,24))',scale={TW}:{TH}", '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
ALL = np.frombuffer(ALLRAW, dtype=np.uint8).reshape(-1, TH, TW, 3)
for s in scenes:
    t0 = math.ceil(s['f0'] / 24)
    t1 = (s['f1'] - 1) / 24
    times = list(range(t0, int(math.floor(t1)) + 1))
    frames = [t * 24 for t in times]
    imgs = ALL[t0:t0 + len(times)]
    n = min(len(imgs), len(frames))
    rws = math.ceil(n / COLS)
    sheet = Image.new('RGB', (COLS * TW, rws * (TH + 18) + 22), (16, 16, 16))
    dr = ImageDraw.Draw(sheet)
    dr.text((4, 3), f"EP009 {s['scene']}  {s['segs'][0]['id']}-{s['segs'][-1]['id']}  frames {s['f0']}-{s['f1']}  1 fps", fill=(255, 220, 80), font=fnt)
    for k in range(n):
        f = frames[k]
        seg = [x for x in s['segs'] if x['out'][0] <= f < x['out'][1]][0]
        x, y = (k % COLS) * TW, 22 + (k // COLS) * (TH + 18)
        sheet.paste(Image.fromarray(imgs[k]), (x, y))
        dr.text((x + 3, y + TH + 1), f"{int(times[k] // 60)}:{times[k] % 60:02d} {seg['id']} {seg['lane']}", fill=(230, 230, 230), font=fnt)
    p = f"{A}/qa/contact/{s['scene']}.png"
    sheet.save(p)
    out.append((s['scene'], n, len(frames)))
print(out)
