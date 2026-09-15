"""Freeze read-only input evidence and a technical contact sheet in this packet."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
EXP=Path('/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001')
VIDEO=EXP/'media/repair-r9/test-i-landscape-study-refined-1080p.mp4'
IMAGES=[EXP/'media/repair-r9'/n for n in ['rendered-frame-0.png','rendered-frame-23p2.png','rendered-frame-final.png']]
ROOM=EXP/'study-composite-r9/assets/study.png'
INDEX=EXP/'study-composite-r9/index.html'

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

assert sha(VIDEO)=='b0e1f20c78091a61453a43c28aec1a9df0f6a04297912fdd6fdbcb5dd348d4f1'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vf','select=eq(n\\,0)+eq(n\\,580)+eq(n\\,764),format=rgb24','-an','-fps_mode','passthrough','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(3,1080,1920,3)
checks=[]
for n,path,frame in zip([0,580,764],IMAGES,frames):
    rgb=np.asarray(Image.open(path).convert('RGB'))
    checks.append({'frame':n,'time_seconds':n/25,'path':str(path),'matches_decoded_test_i_rgb':bool(np.array_equal(rgb,frame))})
assert all(x['matches_decoded_test_i_rgb'] for x in checks)
(ROOT/'media').mkdir(exist_ok=True)
sheet=Image.new('RGB',(960,1710),(20,20,20));draw=ImageDraw.Draw(sheet)
for i,(n,frame) in enumerate(zip([0,580,764],frames)):
    sheet.paste(Image.fromarray(frame).resize((960,540)),(0,i*570+30))
    draw.text((14,i*570+9),f'Test I encoded frame {n} / {n/25:.2f} seconds',fill='white')
sheet.save(ROOT/'media/test-i-contact-sheet.jpg',quality=94)
inputs=[{'path':str(p),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in [VIDEO,*IMAGES,ROOM,INDEX]]
report={'inputs':inputs,'source_frame_checks':checks,'source_rgb_edited':False,
        'provenance':'Three supplied PNG frames are exactly equal to the corresponding decoded RGB frames of hash-pinned Test I. Contact sheet is a resized diagnostic only. No source raster was edited.',
        'measurement_limits':'No skin-to-wall exposure ratio or unmatched-surface sharpness score is used; material, content and lighting differ.'}
(ROOT/'input-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
