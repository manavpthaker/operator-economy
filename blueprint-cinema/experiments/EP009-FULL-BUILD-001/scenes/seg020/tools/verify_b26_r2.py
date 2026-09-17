"""Validate the two B-26 booking-site instance substitutions without changing their timing."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw

SCENES = Path(__file__).resolve().parents[2]
ROOT = SCENES.parents[3]
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(args):
    return subprocess.check_output(args)


def frame(p, n):
    raw = run(['ffmpeg','-v','error','-i',str(p),'-vf',f'select=eq(n\\,{n})','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
    return Image.fromarray(np.frombuffer(raw,np.uint8).reshape(720,1280,3))


def audio(p, filt=None):
    args=['ffmpeg','-v','error','-i',str(p)]
    if filt: args += ['-af',filt]
    return np.frombuffer(run(args+['-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32)


def site_inner(html):
    return re.search(r'<g id="site"[^>]*>(<g transform=.*?</g>)<text',html).group(1)


later_s11=(SCENES/'seg040__seg043/index.html').read_text()
later_s20=(SCENES/'seg069__seg070/index.html').read_text()
kit=(SCENES.parent/'world-kit/kit.svg').read_text()
for name in ['seg004__seg006','seg020']:
    p=SCENES/name;r=p/'qa/r2';v=r/f'{name}.r2.mp4'
    b=json.loads((p/'BUILD.r1.json').read_text());mi,mo,expected=b['master_in'],b['master_out'],b['frames']
    html=(p/'index.html').read_text();old=(p/'tools/index.r1.html').read_text()
    js=html.split('<script>\n',1)[1];oldjs=old.split('<script>\n',1)[1]
    assert js==oldjs
    source_geometry={}
    for id in ['kit-booking-site','kit-listing-card','kit-listing-card-inn']:
        current=re.search(r'<g id="'+id+r'" data-kit-desc=.*?</g>',html,re.S).group(0)
        canonical=re.search(r'<g id="'+id+r'" data-kit-desc=.*?</g>',kit,re.S).group(0).replace('\n','')
        source_geometry[id]={'exact_canonical_match':current==canonical,'sha256':hashlib.sha256(current.encode()).hexdigest()}
        assert current==canonical
    if name=='seg020':
        match=site_inner(html)==site_inner(later_s11)
        instance_check='S05 instance equals S11 instance including transform and every listing card.'
    else:
        compare=re.sub(r'<use href="#kit-guest-book-open"[^>]*/>','',site_inner(later_s20))
        match=site_inner(html)==compare
        instance_check='S00 instance equals S20 instance excluding the later guest-book overlay.'
    assert match
    probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(v)]))
    vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert int(vs['nb_read_frames'])==expected==round(mo*24)-round(mi*24)
    assert (vs['width'],vs['height'],vs['r_frame_rate'])==(1280,720,'24/1')
    assert (au['sample_rate'],au['channels'])==('48000',2)
    (r/'PROBE.json').write_text(json.dumps(probe,indent=2)+'\n')
    ref=audio(MASTER,f'atrim=start_sample={round(mi*48000)}:end_sample={round(mo*48000)},asetpts=N/SR/TB')
    excerpt=audio(p/'public/audio/narration.wav');out=audio(v)
    ref_corr=float(np.corrcoef(ref,excerpt)[0,1]);corr=float(np.corrcoef(ref,out[:len(ref)])[0,1])
    assert ref_corr>.999999 and corr>=.999
    raw=run(['ffmpeg','-v','error','-i',str(v),'-vf','scale=128:72','-an','-f','rawvideo','-pix_fmt','gray','-'])
    frames=np.frombuffer(raw,np.uint8).reshape(-1,72,128)
    uniform=np.flatnonzero(np.ptp(frames,axis=(1,2))<=2).tolist()
    assert len(frames)==expected and not uniform
    cues=json.loads(re.search(r'const C=(\{[^;]+\});',html).group(1))
    stills=[]
    for key,t in [('first',0)]+[(k,min(v+.7,(expected-1)/24)) for k,v in cues.items()]+[('last',(expected-1)/24)]:
        n=round(t*24);dest=r/'stills'/f'{n:04d}-{key}.png';frame(v,n).save(dest)
        stills.append({'key':key,'frame':n,'master_time':mi+n/24,'path':str(dest.relative_to(ROOT))})
    cols,cw,ch=3,480,295
    sheet=Image.new('RGB',(cols*cw,((len(stills)+cols-1)//cols)*ch),'white');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(stills):
        x,y=i%cols*cw,i//cols*ch
        sheet.paste(Image.open(ROOT/s['path']).resize((480,270)),(x,y+25))
        draw.text((x+6,y+6),f"{s['key']}  master {s['master_time']:.3f}",fill='black')
    sheet.save(r/'contact-r2.png')
    result={'finding':'B-26','scene':name,'video':str(v.relative_to(ROOT)),'sha256':sha(v),'frames':expected,'frames_ok':True,'duration':expected/24,'format':'1280x720 24/1; stereo 48000 Hz','source_geometry':source_geometry,'instance_check':instance_check,'instance_match':match,'timeline_javascript_unchanged':js==oldjs,'timeline_javascript_sha256':hashlib.sha256(js.encode()).hexdigest(),'audio_corr_zero_lag':corr,'source_excerpt_vs_master_corr':ref_corr,'trailing_encoder_samples':len(out)-len(ref),'uniform_frames':uniform,'cue_stills':stills,'inputs':{str(q.relative_to(ROOT)):sha(q) for q in [MASTER,p/'public/audio/narration.wav',p/'package.json',p/'index.html',SCENES.parent/'world-kit/kit.svg',SCENES/'seg040__seg043/index.html',SCENES/'seg069__seg070/index.html']},'review_limits':'Frame and geometry review with audio correlation; no normal-speed audiovisual playback or owner verdict.'}
    (r/'VERIFY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cue_stills','inputs','source_geometry']},indent=2))

# Full-size A/B/callback comparison, saved only under an owned scene path.
comparisons=[('S00 r1',SCENES/'seg004__seg006/qa/seg004__seg006.mp4',340),('S00 r2',SCENES/'seg004__seg006/qa/r2/seg004__seg006.r2.mp4',340),('S20 existing callback',SCENES/'seg069__seg070/qa/s20e-s21.mp4',24),('S05 r1',SCENES/'seg020/qa/seg020.mp4',498),('S05 r2',SCENES/'seg020/qa/r2/seg020.r2.mp4',498),('S11 existing return',SCENES/'seg040__seg043/qa/seg040__seg043.mp4',400)]
sheet=Image.new('RGB',(1920,770),'white');draw=ImageDraw.Draw(sheet)
for i,(label,p,n) in enumerate(comparisons):
    x,y=(i%3)*640,(i//3)*385
    img=frame(p,n);dest=SCENES/'seg020/qa/r2/stills'/f'comparison-{i}.png';img.save(dest)
    sheet.paste(img.resize((640,360)),(x,y+25));draw.text((x+8,y+7),label,fill='black')
sheet.save(SCENES/'seg020/qa/r2/world-continuity-comparison.png')
