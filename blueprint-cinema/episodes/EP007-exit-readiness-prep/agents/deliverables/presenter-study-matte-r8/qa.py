"""Bounded, local, read-only source QA. Outputs only beside this script."""
import hashlib
import io
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4')
EXPECTED = '6bfc0bd9190448e4a41d7ea694797ee48135d6ece85467a90bfb3e11926c749f'
W, H = 608, 1080

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for data in iter(lambda: f.read(1024*1024), b''):
            h.update(data)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))

def frame(path, n, vf):
    data = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{n}),'+vf,'-frames:v','1','-c:v','png','-f','image2pipe','-'])
    return Image.open(io.BytesIO(data))

assert sha(SOURCE) == EXPECTED
report = {'source_sha256': EXPECTED, 'files': {}, 'limits': [
    'Pixel preservation is verified against FFmpeg-decoded RGB, not compressed source YUV byte identity.',
    'Adjacent-mask differences include actual subject motion; they do not independently prove absence of edge chatter.',
    'Contact sheets are sampled visual evidence, not a full continuous playback approval.',
    'Source shoulder and torso beyond the portrait boundaries remain unavailable.',
]}
for name in ['diagnostic-mask-100f.mkv','diagnostic-alpha-100f.mkv','full-mask-765f.mkv']:
    path = ROOT/'media'/name
    p = probe(path)
    result = subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'], capture_output=True)
    report['files'][name] = {'sha256':sha(path),'size_bytes':path.stat().st_size,'probe':p,'full_decode_exit':result.returncode,'full_decode_errors':result.stderr.decode()}
    assert result.returncode == 0
    stream = p['streams'][0]
    assert (stream['width'],stream['height']) == (W,H)
    assert int(stream['nb_read_frames']) == (765 if name.startswith('full') else 100)
    assert stream['r_frame_rate'] == '25/1'

raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'media/full-mask-765f.mkv'),'-pix_fmt','gray','-f','rawvideo','-'])
masks = np.frombuffer(raw,dtype=np.uint8).reshape(765,H,W)
changes = []
coverage = []
for n in range(765):
    coverage.append(float((masks[n] > 127).mean()))
    if n:
        d = np.abs(masks[n].astype(np.int16)-masks[n-1].astype(np.int16))
        changes.append(float(d.mean()/255))
order = np.argsort(changes)[-5:][::-1]
report['temporal_mask_metrics'] = {
    'whole_mask_adjacent_mae_normalized_median':float(np.median(changes)),
    'whole_mask_adjacent_mae_normalized_p95':float(np.percentile(changes,95)),
    'largest_changes':[{'frame':int(i+1),'time_seconds':float((i+1)/25),'mae_normalized':changes[i]} for i in order],
    'opaque_coverage_fraction_min':min(coverage),'opaque_coverage_fraction_max':max(coverage),
    'empty_frames':int(sum(v == 0 for v in coverage)),
    'solid_frames':int(sum(v == 1 for v in coverage)),
}
# Compare separately generated diagnostic mask sequence with full-run first 100.
diag = subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'media/diagnostic-mask-100f.mkv'),'-pix_fmt','gray','-f','rawvideo','-'])
diagnostic_masks=np.frombuffer(diag,dtype=np.uint8).reshape(100,H,W)
report['diagnostic_vs_full_first_100_masks_equal'] = bool(np.array_equal(diagnostic_masks,masks[:100]))

samples = [10,85,400,490,580,764]
sheet = Image.new('RGB',(912,6*570),(20,20,20))
rgb_checks=[]
for row,n in enumerate(samples):
    rgb = frame(SOURCE,n,'crop=608:1080:656:0,format=rgb24').convert('RGB')
    mask = Image.fromarray(masks[n])
    alpha = rgb.copy(); alpha.putalpha(mask)
    alpha.save(ROOT/'media'/f'full-alpha-f{n:03d}.png')
    bg = Image.new('RGB',(W,H),(42,50,58)); bg.paste(rgb,(0,0),mask)
    draw=ImageDraw.Draw(sheet)
    for col,(im,label) in enumerate([(rgb,'SOURCE RGB'),(mask.convert('RGB'),'VISION MASK'),(bg,'QA DARK BACKGROUND')]):
        sheet.paste(im.resize((304,540)),(col*304,row*570+30))
        draw.text((col*304+8,row*570+8),f'{n/25:.2f}s  {label}',fill='white')
    if n < 100:
        got=np.asarray(frame(ROOT/'media/diagnostic-alpha-100f.mkv',n,'format=rgba').convert('RGBA'))
        rgb_exact=bool(np.array_equal(got[:,:,:3],np.asarray(rgb)))
        alpha_exact=bool(np.array_equal(got[:,:,3],diagnostic_masks[n]))
        rgb_checks.append({'frame':n,'all_rgb_samples_equal':rgb_exact,'alpha_samples_equal':alpha_exact})
        assert rgb_exact and alpha_exact
sheet.save(ROOT/'media/full-contact-sheet.jpg',quality=92)
report['diagnostic_alpha_pixel_checks']=rgb_checks
(ROOT/'qa-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
