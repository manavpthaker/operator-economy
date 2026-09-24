"""Independent parent alpha-asset verification; all writes stay in this packet."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
EXP = Path('/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001')
SOURCE = EXP/'media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4'
ALPHA = EXP/'study-composite-r8/assets/performance-alpha.webm'
SNAPSHOTS = [EXP/'study-composite-r8/snapshots'/n for n in ['frame-00-at-0.4s.png','frame-01-at-23.2s.png']]

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def hashes(which, fmt):
    path=SOURCE if which=='source' else ALPHA
    command=['ffmpeg','-v','error','-xerror']
    if which=='alpha': command+=['-c:v','libvpx-vp9']
    command+=['-i',str(path),'-map','0:v:0','-an']
    vf=[]
    if which=='source': vf.append('crop=608:1080:656:0')
    vf.append('format='+fmt)
    command+=['-vf',','.join(vf),'-f','framemd5','-']
    run=subprocess.run(command,capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    rows=[line.strip() for line in run.stdout.splitlines() if line and not line.startswith('#')]
    values=[]
    for row in rows:
        parts=[x.strip() for x in row.split(',')]
        values.append({'dts':int(parts[1]),'pts':int(parts[2]),'duration':int(parts[3]),'size_bytes':int(parts[4]),'md5':parts[5]})
    return {'frame_count':len(values),'rows':values,'command':command,'decode_exit':run.returncode,
            'ordered_frame_record_sha256':hashlib.sha256(json.dumps(values,sort_keys=True).encode()).hexdigest()}

assert sha(SOURCE)=='6bfc0bd9190448e4a41d7ea694797ee48135d6ece85467a90bfb3e11926c749f'
specs=[('source','yuv420p'),('alpha','yuv420p'),('source','rgb24'),('alpha','rgb24')]
with ThreadPoolExecutor(max_workers=4) as pool:
    results=dict(zip(specs,pool.map(lambda pair:hashes(*pair),specs)))
comparisons={}
for fmt in ['yuv420p','rgb24']:
    a=results[('source',fmt)];b=results[('alpha',fmt)]
    differences=[i for i,(x,y) in enumerate(zip(a['rows'],b['rows'])) if x!=y]
    comparisons[fmt]={
        'source_frames':a['frame_count'],'alpha_frames':b['frame_count'],
        'both_765_frames':a['frame_count']==b['frame_count']==765,
        'source_pts_are_0_through_764':all(row['pts']==i for i,row in enumerate(a['rows'])),
        'alpha_pts_are_0_through_764':all(row['pts']==i for i,row in enumerate(b['rows'])),
        'matching_frame_records':sum(x==y for x,y in zip(a['rows'],b['rows'])),
        'different_frame_indices_first_20':differences[:20],
        'all_decoded_pixels_and_frame_order_identical':a['rows']==b['rows'],
        'source_ordered_frame_record_sha256':a['ordered_frame_record_sha256'],
        'alpha_ordered_frame_record_sha256':b['ordered_frame_record_sha256'],
        'source_command':a['command'],'alpha_command':b['command']}

# Force the alpha-aware decoder and decode the alpha plane, proving more than a container tag.
alpha_decode=subprocess.run(['ffmpeg','-v','error','-xerror','-c:v','libvpx-vp9','-i',str(ALPHA),'-vf','alphaextract','-f','null','-'],capture_output=True,text=True)
assert alpha_decode.returncode==0,alpha_decode.stderr
report={
    'review_status':'candidate_review_not_approval',
    'inputs':[{'path':str(p),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in [SOURCE,ALPHA,*SNAPSHOTS]],
    'source_crop':{'x':656,'y':0,'width':608,'height':1080},
    'alpha_decoder':'libvpx-vp9','comparisons':comparisons,
    'alpha_plane_full_decode_exit':alpha_decode.returncode,
    'snapshot_findings':[
        {'severity':'observation','snapshots':'both, latest 21:41 revision','location':'upper shoulders','finding':'The earlier pointed triangular joins are removed in the revised snapshots.'},
        {'severity':'observation','snapshots':'both, latest 21:41 revision','location':'center shirt to static outer shoulders and chest','finding':'A softer texture and clarity mismatch remains across the blend; continuous playback is needed to assess whether static clothing motion is conspicuous.'},
        {'severity':'observation','snapshots':'both, latest 21:41 revision','location':'head and glasses','finding':'No obvious duplicate face visible in these two stills. Fine hair/glasses edge fringe remains.'}
    ],
    'limits':[
        'This tests the alpha video and two static scene snapshots, not the subsequent encoded full composite.',
        'Lossless content verification does not approve lip sync, expressions, clothing seam, or continuous playback.',
        'Alpha-edge feathering is expected to differ from the original Vision mask; this report verifies underlying image content and frame order.'
    ],
    'external_writes':False,'production_state_changed':False,'approval_claimed':False}
(ROOT/'parent-alpha-independent-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'comparisons':comparisons,'alpha_plane_full_decode_exit':alpha_decode.returncode},indent=2))
