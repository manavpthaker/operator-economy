#!/usr/bin/env python3
"""Reduce head motion without retiming or regenerating the facial performance."""
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def smooth(v):
    v = np.clip(v,0,1)
    return v*v*(3-2*v)


def main():
    cfg=json.loads((HERE/'stabilization-config.json').read_text())
    source,output,seg=map(Path,(cfg['source'],cfg['output'],cfg['segmentation_path']))
    if output.exists():
        raise FileExistsError(output)
    if sha(source)!=cfg['source_sha256']:
        raise ValueError('Source changed')
    output.parent.mkdir(parents=True,exist_ok=True)
    x0,y0,x1,y1=cfg['roi_xyxy'];box=(x0,y0,x1,y1);cw,ch=x1-x0,y1-y0
    ax,ay,bx,by=cfg['rigid_core_xyxy'];ox,oy,px,py=cfg['outer_bounds_xyxy']
    step=cfg['mesh_step_px']

    def weight(x,y):
        return float(smooth((x-ox)/(ax-ox))*(1-smooth((x-bx)/(px-bx)))*
                     smooth((y-oy)/(ay-oy))*(1-smooth((y-by)/(py-by))))

    rects=[];points=[];weights=[]
    for y in range(y0,y1,step):
        for x in range(x0,x1,step):
            xx,yy=min(x+step,x1),min(y+step,y1)
            rects.append((x-x0,y-y0,xx-x0,yy-y0))
            quad=((x,y),(x,yy),(xx,yy),(xx,y))
            points.append(quad);weights.append([weight(a,b) for a,b in quad])
    points=np.asarray(points,np.float64);weights=np.asarray(weights)[...,None]
    origin=np.array([x0,y0])

    def mesh_for(record):
        inverse=np.asarray(record['inverse_matrix_2x3'])
        mapped=points@inverse[:,:2].T+inverse[:,2]
        mapped=points+weights*(mapped-points)-origin
        return [(r,tuple(q.reshape(-1))) for r,q in zip(rects,mapped)]

    def warp(arr,mesh):
        im=Image.fromarray(arr.astype(np.float32))
        return np.asarray(im.transform((cw,ch),Image.Transform.MESH,mesh,
                                      Image.Resampling.BICUBIC)).copy()

    # A fixed plate supplies only newly exposed background; visible Q background stays original.
    best_score=np.full((ch,cw),np.inf,np.float32)
    clean_alpha=np.ones((ch,cw),np.float32)
    background=np.zeros((ch,cw,3),np.float32)
    bindings=[]
    for i in range(cfg['frames']):
        fp,mp=seg/f'frame-{i:03d}.png',seg/f'mask-full-{i:03d}.png'
        with Image.open(fp) as im:
            rgb=np.asarray(im.convert('RGB').crop(box),np.float32)
        with Image.open(mp) as im:
            if im.size!=(1920,1080):raise ValueError('Mask shape mismatch')
            alpha=np.asarray(im.convert('L').crop(box),np.float32)/255
        score=alpha+abs(i-68)*0.00001
        take=score<best_score
        background[take]=rgb[take];clean_alpha[take]=alpha[take];best_score[take]=score[take]
        bindings.append({'frame':i,'rgb_sha256':sha(fp),'alpha_sha256':sha(mp)})
    Image.fromarray(np.rint(background).astype(np.uint8)).save(output.parent/'observed-background-roi.png')

    dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-map','0:v:0',
        '-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc=subprocess.Popen(['ffmpeg','-v','error','-f','rawvideo','-pix_fmt','rgb24',
        '-s','1920x1080','-r','25','-i','-','-i',str(source),'-map','0:v:0',
        '-map','1:a:0','-c:v','libx264','-preset','medium','-crf','15','-pix_fmt',
        'yuv420p','-c:a','copy','-movflags','+faststart',str(output)],stdin=subprocess.PIPE)
    checks=[]
    for i in range(cfg['frames']):
        raw=dec.stdout.read(1920*1080*3)
        if len(raw)!=1920*1080*3:raise ValueError('Source frame count mismatch')
        frame=np.frombuffer(raw,np.uint8).reshape(1080,1920,3).copy()
        rgb=frame[y0:y1,x0:x1].astype(np.float32)
        with Image.open(seg/f'mask-full-{i:03d}.png') as im:
            alpha=np.asarray(im.convert('L').crop(box),np.float32)/255
        mesh=mesh_for(cfg['transforms'][i])
        warped_alpha=np.clip(warp(alpha,mesh),0,1)
        premul=np.clip(rgb-(1-alpha[...,None])*background,0,255*alpha[...,None])
        shifted=np.stack([warp(premul[:,:,k],mesh) for k in range(3)],axis=2)
        shifted=np.clip(shifted,0,255*warped_alpha[...,None])
        bg=np.where((alpha>0.02)[...,None],background,rgb)
        result=shifted+(1-warped_alpha[...,None])*bg
        untouched=(alpha<=0.002)&(warped_alpha<=0.002)
        result[untouched]=rgb[untouched]
        revealed=(alpha>0.02)&(warped_alpha<0.98)
        unresolved=revealed&(clean_alpha>0.02)
        frame[y0:y1,x0:x1]=np.clip(np.rint(result),0,255).astype(np.uint8)
        checks.append({'frame':i,'unresolved_edge_pixels':int(unresolved.sum()),
                       'unchanged_background_pixels':int(untouched.sum())})
        if i in (0,15,25,50,70,100,111,125,139):
            Image.fromarray(frame).save(output.parent/f'frame-{i:03d}.png')
        enc.stdin.write(frame.tobytes())
    if dec.stdout.read(1):raise ValueError('Extra source frame')
    dec.stdout.close();enc.stdin.close()
    if dec.wait() or enc.wait():raise RuntimeError('Decode or encode failed')
    report={'source_sha256':sha(source),'output':str(output),'output_sha256':sha(output),
        'bytes':output.stat().st_size,'segmentation_bindings':bindings,'edge_checks':checks,
        'audio_mode':'source AAC bitstream copy','retiming':False,'expression_generation':False,
        'face_transform':'single uniform similarity within head core; no separate feature edits',
        'background':'observed Q pixels; original visible background coordinates preserved',
        'owner_review_pending':True}
    (HERE/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(output),'sha256':report['output_sha256'],'bytes':report['bytes'],
        'max_unresolved_edge_pixels':max(x['unresolved_edge_pixels'] for x in checks)},indent=2))


if __name__=='__main__':main()
