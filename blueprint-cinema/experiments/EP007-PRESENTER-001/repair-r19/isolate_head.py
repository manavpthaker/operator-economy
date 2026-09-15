#!/usr/bin/env python3
"""Damp Q's head motion using local person mattes and observed background pixels."""
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEG = ROOT / 'episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-head-damping-r19/segmentation'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def smooth(v):
    v = np.clip(v, 0, 1)
    return v * v * (3 - 2 * v)


def main():
    cfg = json.loads((HERE / 'damping-config.json').read_text())
    source = Path(cfg['source'])
    output = Path(cfg['output']).with_name('test-r-q-subtle-straight-head-isolated-1080p.mp4')
    if output.exists():
        raise FileExistsError(output)
    assert sha(source) == cfg['source_sha256']
    x0, y0, x1, y1 = cfg['processing_roi_xyxy']
    box = (x0, y0, x1, y1)
    cw, ch = x1-x0, y1-y0
    ax, ay, bx, by = cfg['mask']['rigid_core_xyxy']
    ox, oy, px, py = cfg['mask']['outer_bounds_xyxy']
    step = cfg['mesh_step_px']

    def weight(x, y):
        return float(smooth((x-ox)/(ax-ox)) * (1-smooth((x-bx)/(px-bx))) *
                     smooth((y-oy)/(ay-oy)) * (1-smooth((y-by)/(py-by))))

    grid = []
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            xx, yy = min(x+step,x1), min(y+step,y1)
            points = [(sx-x0,sy-y0,weight(sx,sy))
                      for sx,sy in ((x,y),(x,yy),(xx,yy),(xx,y))]
            grid.append(((x-x0,y-y0,xx-x0,yy-y0),points))

    def warp(arr, dy):
        mesh = [(rect,tuple(v for x,y,w in pts for v in (x,y-dy*w)))
                for rect,pts in grid]
        im = Image.fromarray(arr.astype(np.float32))
        return np.asarray(im.transform((cw,ch),Image.Transform.MESH,mesh,
                                      Image.Resampling.BICUBIC)).copy()

    refs = []
    bindings = []
    for path in sorted(SEG.glob('frame-*.png')):
        i = int(path.stem.split('-')[-1])
        maskpath = SEG/f'mask-full-{i:03d}.png'
        if not maskpath.exists():
            raise FileNotFoundError(maskpath)
        maskim = Image.open(maskpath)
        assert maskim.size == (1920,1080)
        rgb = np.asarray(Image.open(path).convert('RGB').crop(box),np.float32)
        alpha = np.asarray(maskim.convert('L').crop(box),np.float32)/255
        refs.append((i,rgb,alpha))
        bindings.append({'frame':i,'image_sha256':sha(path),'alpha_sha256':sha(maskpath)})
    if not refs:
        raise ValueError('No verified segmentation inputs')
    by_index = {i:(rgb,a) for i,rgb,a in refs}
    shifts = {r['frame']:r['output_dy_px'] for r in cfg['frame_shifts']}
    dec = subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-map','0:v:0',
        '-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg','-v','error','-f','rawvideo','-pix_fmt','rgb24',
        '-s','1920x1080','-r','25','-i','-','-i',str(source),'-map','0:v:0',
        '-map','1:a:0','-c:v','libx264','-preset','medium','-crf','15','-pix_fmt',
        'yuv420p','-c:a','copy','-movflags','+faststart',str(output)],stdin=subprocess.PIPE)
    facts = []
    for i in range(140):
        raw = dec.stdout.read(1920*1080*3)
        if len(raw) != 1920*1080*3:
            raise ValueError('Unexpected decoded frame length')
        dy = shifts.get(i,0)
        if abs(dy) > 1e-6:
            frame = np.frombuffer(raw,np.uint8).reshape(1080,1920,3).copy()
            rgb, alpha = by_index[i]
            # Use only observed background samples, preferring the nearest clean frame.
            score = np.full((ch,cw),np.inf,np.float32)
            background = rgb.copy()
            chosen_alpha = np.ones((ch,cw),np.float32)
            for j, ref, a in refs:
                cost = a + abs(j-i)*0.0001
                take = cost < score
                background[take] = ref[take]
                chosen_alpha[take] = a[take]
                score[take] = cost[take]
            warped_alpha = np.clip(warp(alpha,dy),0,1)
            # Matte only the foreground; shelf/wall pixels retain original Q coordinates.
            premul = np.clip(rgb - (1-alpha[...,None])*background,
                             0,255*alpha[...,None])
            shifted = np.stack([warp(premul[:,:,k],dy) for k in range(3)],axis=2)
            shifted = np.clip(shifted,0,255*warped_alpha[...,None])
            bg = np.where((alpha>0.02)[...,None],background,rgb)
            result = shifted + (1-warped_alpha[...,None])*bg
            unchanged_background = (alpha<=0.002)&(warped_alpha<=0.002)
            result[unchanged_background] = rgb[unchanged_background]
            revealed = (alpha>0.02)&(warped_alpha<0.98)
            unresolved = revealed&(chosen_alpha>0.02)
            # This count is retained for review; uncertain matte-edge pixels are not a clean plate.
            facts.append({'frame':i,'dy_px':dy,
                'revealed_or_soft_edge_pixels':int(revealed.sum()),
                'pixels_without_clean_reference':int(unresolved.sum()),
                'unchanged_background_pixels':int(unchanged_background.sum())})
            frame[y0:y1,x0:x1] = np.clip(np.rint(result),0,255).astype(np.uint8)
            if i in (20,25,29):
                Image.fromarray(frame).save(output.parent/f'isolated-frame-{i:03d}.png')
            raw = frame.tobytes()
        enc.stdin.write(raw)
    if dec.stdout.read(1):
        raise ValueError('Unexpected additional source frames')
    dec.stdout.close(); enc.stdin.close()
    if dec.wait() or enc.wait():
        raise RuntimeError('Decode/encode failure')
    report={'source':str(source),'source_sha256':sha(source),'output':str(output),
            'output_sha256':sha(output),'bytes':output.stat().st_size,
            'segmentation_inputs':bindings,'frames':facts,
            'background_method':'Observed lowest-alpha nearest-time Q pixels; source background coordinates retained',
            'audio':'Q bitstream copied','new_provider_generations':0,
            'owner_review_pending':True}
    (HERE/'isolated-render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(output),'sha256':report['output_sha256'],
        'bytes':report['bytes'],'max_unresolved_edge_pixels':max(f['pixels_without_clean_reference'] for f in facts)},indent=2))


if __name__=='__main__':
    main()
