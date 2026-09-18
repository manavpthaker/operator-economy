#!/usr/bin/env python3
"""Prepare separate r5-look-transfer review outputs; never update current plans.

check/prepare/render require a hash-bound selection manifest. Full mode requires
all 14 moving presenter clips plus corrected P08. Pilot mode is a separate
side-by-side excerpt and can never write a full episode with missing selections.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[1]
B = T.parent
A = B/'assembly'
sys.path.insert(0, str(A/'_tools'))
from build_r3 import R, bound, read, rel, sha, verify_bound, write, probe
from build_r4 import frame_map, graph_for, nested_bindings

BASE = A/'r4/ep009-full-r4-opening-candidate-BUILD.json'
BASE_SHA = 'fad999994483aa029f045a4b1ac6286ca42e7aef91b43fcb454822e5363bec02'
AUDIT = T/'SOURCE-AUDIT.json'
AUDIT_SHA = '77d1300b3f52841209013af3523124bbca9568061f6cac35fb6026de0184224d'
REQUIRED = ('seg009','seg012','seg019','seg021','seg028','seg035','seg037','seg044',
            'seg055','seg059','seg071','seg072','seg073','seg074','seg075')
D = A/'r5-look-transfer'
Q = A/'qa/r5-look-transfer'
PERFORMANCE_FIELDS = ('hands','facial_expressions','head_and_body','camera_and_crops','timing')


def audio_digest(master, frames):
    """Hash exact mono PCM16 program samples, including only required end zeros."""
    a,z = (f*2000 for f in frames)
    h=hashlib.sha256()
    with wave.open(str(master),'rb') as w:
        if (w.getframerate(),w.getnchannels(),w.getsampwidth(),w.getcomptype()) != (48000,1,2,'NONE'):
            raise ValueError('Master must be mono 48kHz PCM16')
        n=w.getnframes()
        if a>=n or z>n+1080:raise ValueError('Unexpected master range or padding')
        w.setpos(a);left=min(z,n)-a
        while left:
            raw=w.readframes(min(left,240000))
            if not raw:raise ValueError('Master PCM shortfall')
            h.update(raw);left-=len(raw)//2
        h.update(b'\0\0'*max(0,z-n))
    return h.hexdigest()


def video_hashes(path, expected_frames):
    """Hash every decoded yuv420p frame; this binds pixels, not motion quality."""
    cmd=['ffmpeg','-v','error','-threads','1','-i',str(path),'-map','0:v:0','-an',
         '-vf','format=yuv420p','-fps_mode','passthrough','-f','framehash','-hash','sha256','-']
    text=subprocess.check_output(cmd,text=True)
    lines=[line for line in text.splitlines() if line and not line.startswith('#')]
    hashes=[line.rsplit(',',1)[-1].strip() for line in lines]
    if len(hashes)!=expected_frames or any(not re.fullmatch('[0-9a-f]{64}',h) for h in hashes):
        raise ValueError('Decoded frame hash count/format mismatch: '+str(path))
    timebase=next((line.split(':',1)[1].strip() for line in text.splitlines() if line.startswith('#tb 0:')),None)
    timestamps=[tuple(int(x.strip()) for x in line.split(',')[1:4]) for line in lines]
    if timebase!='1/24' or timestamps!=[(i,i,1) for i in range(expected_frames)]:
        raise ValueError('Replacement/reference must have exact consecutive 24fps timing from frame zero')
    return {'algorithm':'sha256_decoded_yuv420p_frames_in_order','frames':len(hashes),
            'sequence_sha256':hashlib.sha256(('\n'.join(hashes)+'\n').encode()).hexdigest(),
            'hashes':hashes}


def checked_base():
    base=read(verify_bound({'path':rel(BASE),'sha256':BASE_SHA}))
    audit=read(verify_bound({'path':rel(AUDIT),'sha256':AUDIT_SHA}))
    if audit['current_build']!=bound(BASE):raise ValueError('Inventory/base mismatch')
    for k in ('master','timemap','transcript','revision','owner_scoped_lock','film_selections'):
        verify_bound(base[k])
    lock=read(verify_bound(base['owner_scoped_lock']))
    for k in ('source','brand_preview','hospitality_preview','selected_paragraph_audio','selected_script','time_map','master_carrier'):
        verify_bound(lock[k])
    if lock['master_carrier']!=base['master'] or lock['time_map']!=base['timemap']:
        raise ValueError('Owner lock/master/timemap mismatch')
    if len(base['all_75_rows'])!=75 or len(frame_map(base['all_75_rows']))!=29323:
        raise ValueError('Expected the unchanged 75-cue, 29323-frame r4')
    for s in {s['source']['path']:s for r in base['all_75_rows'] for s in r['spans']}.values():
        verify_bound(s['source'])
    return base,audit


def validate_inventory(manifest, base, mode, segment):
    if manifest.get('record_type')!='ep009_look_transfer_review_selections' or manifest.get('status')!='selected_for_review':
        raise ValueError('Explicit review-selection manifest required')
    if manifest.get('base_build')!=bound(BASE) or manifest.get('source_audit')!=bound(AUDIT) or manifest.get('master')!=base['master']:
        raise ValueError('Manifest must bind exact current base, inventory and unchanged master')
    if manifest.get('look_reference')!=read(AUDIT)['target_appearance']['L3_image']:
        raise ValueError('Manifest must bind the exact P00/L3 target appearance')
    entries=manifest.get('replacements',[])
    ids=[e.get('segment') for e in entries]
    if len(ids)!=len(set(ids)) or not set(ids).issubset(REQUIRED):
        raise ValueError('Duplicate or unknown selection; P00/film replacements are prohibited')
    if mode=='full':
        if segment or set(ids)!=set(REQUIRED):raise ValueError('Full mode requires exactly all 15 replacements; no fallback')
        return {e['segment']:e for e in entries}
    if segment not in REQUIRED or segment=='seg044' or ids!=[segment]:
        raise ValueError('Pilot requires exactly one existing moving presenter selection')
    return {segment:entries[0]}


def validated_entry(e, row, audit_entry, base, mode):
    sid=row['id'];lo,hi=row['output_frames'];n=hi-lo
    if e.get('output_frames')!=[lo,hi] or e.get('frames')!=n or e.get('source_start_frame')!=0:
        raise ValueError(sid+': exact whole-slot frames and zero source start required')
    source=verify_bound(e['source'])
    if not source.is_relative_to(T) or source.suffix.lower()!='.mp4':
        raise ValueError(sid+': replacement must be a new MP4 under presenter-look-transfer')
    if e['source']['sha256']==audit_entry['selected_source']['sha256']:
        raise ValueError(sid+': original source is not a replacement')
    evidence=read(verify_bound(e['verification']))
    if evidence.get('record_type')!='ep009_look_transfer_replacement_verification' or evidence.get('status')!='verified':
        raise ValueError(sid+': verified replacement evidence required')
    expected={'segment':sid,'replacement':e['source'],'original_source':audit_entry['selected_source'],
              'output_frames':[lo,hi],'master':base['master'],
              'look_reference':read(AUDIT)['target_appearance']['L3_image']}
    if any(evidence.get(k)!=v for k,v in expected.items()):raise ValueError(sid+': stale/wrong verification binding')
    if evidence.get('errors')!=[] or evidence.get('technical_complete') is not True:
        raise ValueError(sid+': unresolved mechanical errors')
    info=probe(source);v=next(x for x in info['streams'] if x['codec_type']=='video')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))!=(1280,720,'24/1',n):
        raise ValueError(sid+': exact decoded 1280x720, 24fps frame count required')
    if abs(float(v.get('duration',n/24))-n/24)>.002:raise ValueError(sid+': changed video duration')
    digest=audio_digest(verify_bound(base['master']),[lo,hi])
    if evidence.get('master_sample_range')!=[lo*2000,hi*2000] or evidence.get('master_pcm_sha256')!=digest:
        raise ValueError(sid+': exact unchanged master PCM binding required')
    replacement_hashes=video_hashes(source,n)
    if evidence.get('replacement_frame_sequence_sha256')!=replacement_hashes['sequence_sha256']:
        raise ValueError(sid+': changed decoded replacement frames')
    original_hashes=None
    if sid!='seg044':
        original_hashes=video_hashes(verify_bound(audit_entry['selected_source']),n)
        if evidence.get('original_frame_sequence_sha256')!=original_hashes['sequence_sha256']:
            raise ValueError(sid+': changed decoded original performance reference')
        if e.get('kind')!='look_only_existing_performance':raise ValueError(sid+': existing-performance look transfer required')
    else:
        if e.get('kind')!='corrected_P08_performance_exception':raise ValueError('P08 requires explicit corrected-performance exception')
        script=bound(B/'narration-revisions/r3-hospitality/paragraph.txt')
        if evidence.get('corrected_script')!=script or evidence.get('old_P08_speaking_picture_used') is not False:
            raise ValueError('P08 must bind corrected script and exclude old speaking picture')
    review=evidence.get('scoped_review',{})
    if mode=='full':
        if review.get('status')!='complete' or review.get('flagged') is not False or not review.get('reviewer') or not review.get('method') or not review.get('limits'):
            raise ValueError(sid+': complete unflagged scoped review with explicit limits required')
        if review.get('target_appearance_matches') is not True:raise ValueError(sid+': appearance review unresolved')
        if review.get('identity_preserved') is not True:raise ValueError(sid+': presenter identity review unresolved')
        if sid!='seg044' and any(review.get('preserved',{}).get(k) is not True for k in PERFORMANCE_FIELDS):
            raise ValueError(sid+': performance preservation unresolved')
        if sid!='seg044' and review.get('change_scope_confirmed')!='outfit_and_environment_only':
            raise ValueError(sid+': look-only edit scope unresolved')
        if sid=='seg044' and review.get('corrected_dialogue_reviewed') is not True:
            raise ValueError('P08 corrected-dialogue review unresolved')
        if not review.get('evidence'):raise ValueError(sid+': scoped review evidence missing')
    nested_bindings(review.get('evidence',[]))
    return {'segment':sid,'source':e['source'],'verification':e['verification'],'kind':e['kind'],
            'output_frames':[lo,hi],'frames':n,'source_start_frame':0,'master_pcm_sha256':digest,
            'original_frame_hashes':original_hashes,'replacement_frame_hashes':replacement_hashes,
            'scoped_review':review,'provider_audio_discarded':True,'owner_accepted':False}


def prepare(path, mode, segment):
    base,audit=checked_base();manifest=read(path)
    entries=validate_inventory(manifest,base,mode,segment)
    original=base['all_75_rows'];rows=copy.deepcopy(original);byid={x['segment']:x for x in audit['appearances']}
    replacements=[]
    for row in rows:
        sid=row['id']
        if sid not in entries:continue
        e=validated_entry(entries[sid],row,byid[sid],base,mode);replacements.append(e)
        row['spans']=[{'kind':'video','source':e['source'],'source_start_frame':0,
            'original_frames':row['original_frames'],'output_frames':row['output_frames'],'frames':row['frames'],
            'look_transfer_segment':sid,'verification':e['verification']}]
        if sid=='seg044':row['output_cues']['picture']='Corrected locked narration delivered by revised presenter; review candidate.'
    old,new=frame_map(original),frame_map(rows)
    expected={f for e in replacements for f in range(*e['output_frames'])}
    changed={i for i,(x,y) in enumerate(zip(old,new)) if x!=y}
    if len(new)!=29323 or changed!=expected:raise ValueError('Unexpected picture change or timeline shift')
    if new[:86]!=old[:86]:raise ValueError('Current P00 must remain untouched')
    for before,after in zip(original,rows):
        b,a=copy.deepcopy(before),copy.deepcopy(after);b.pop('spans');a.pop('spans')
        if a['id']=='seg044' and 'seg044' in entries:a['output_cues']['picture']=b['output_cues']['picture']
        if a!=b:raise ValueError('Cue/row metadata changed outside P08 picture description')
    return {'record_type':'ep009_r5_look_transfer_review_build','status':'prepared_not_rendered','version':'r5-look-transfer',
        'mode':mode,'pilot_segment':segment,'base_build':bound(BASE),'source_audit':bound(AUDIT),'selections':bound(path),
        'master':base['master'],'timemap':base['timemap'],'transcript':base['transcript'],'revision':base['revision'],
        'owner_scoped_lock':base['owner_scoped_lock'],'film_selections':base['film_selections'],
        'retained_P00':copy.deepcopy(base['candidate']),'all_75_rows':rows,'total_frames':29323,
        'output_master_frames':[0,29323],'replacements':replacements,
        'mapping_checks':{'compared_frames':29323,'changed_frames':len(changed),'allowed_output_ranges':[e['output_frames'] for e in replacements],
            'unchanged_other_assignments':29323-len(changed),'P00_retained':True,'all_row_times_and_word_cues_retained':True},
        'builder':bound(Path(__file__).resolve()),'graph_helper':bound(A/'_tools/build_r4.py'),
        'owner_accepted':False,'release_cleared':False,
        'limits':['Review output only; preparation does not confer owner, sync, bulk or release acceptance.',
                  'Decoded frame hashes bind the reviewed pixels but do not prove preserved performance.',
                  'P00 retains its existing review flags. Provider audio is never used.']}


def pilot_graph(data):
    e=data['replacements'][0];sid=e['segment'];audit=read(AUDIT);old=next(x for x in audit['appearances'] if x['segment']==sid)
    n=e['frames'];a,z=e['output_frames'];master=verify_bound(data['master'])
    inputs=['-threads','1','-i',str(verify_bound(old['selected_source'])),'-threads','1','-i',str(verify_bound(e['source'])),'-i',str(master)]
    video=f'trim=start_frame=0:end_frame={n},setpts=N/(24*TB),setsar=1,format=yuv420p'
    graph=f'[0:v]{video}[old];[1:v]{video}[new];[old][new]hstack=inputs=2[vout];\n'
    graph+=f'[2:a]atrim=start_sample={a*2000}:end_sample={z*2000},apad=whole_len={n*2000},atrim=end_sample={n*2000},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[aout]\n'
    data.update(total_frames=n,output_master_frames=[a,z],comparison_layout='Original left; replacement right. Performance review may remain pending; no full-episode eligibility implied.')
    return graph,inputs


def save_or_render(data, action, name):
    if not re.fullmatch('[A-Za-z0-9_-]+',name):raise ValueError('Use a simple new output name')
    if data['mode']=='full' and not name.startswith('ep009-r5-look-transfer-'):raise ValueError('Full filename must identify r5-look-transfer')
    if data['mode']=='pilot' and not name.startswith('pilot-'+data['pilot_segment']+'-'):raise ValueError('Pilot filename must identify its segment')
    directory=D if data['mode']=='full' else D/'pilots';q=Q if data['mode']=='full' else Q/'pilots'
    paths=[directory/(name+'-BUILD.json'),directory/(name+'-graph.txt'),directory/(name+'-encode.log'),q/(name+'.mp4')]
    if any(p.exists() for p in paths):raise FileExistsError('Preserve existing output/version')
    graph,inputs=graph_for(data) if data['mode']=='full' else pilot_graph(data)
    directory.mkdir(parents=True,exist_ok=True);q.mkdir(parents=True,exist_ok=True)
    manifest,gpath,log,output=paths
    with gpath.open('x') as f:f.write(graph)
    cmd=['ffmpeg','-n','-v','error','-stats','-filter_complex_threads','2',*inputs,'-/filter_complex',str(gpath),
        '-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','16','-threads','2','-pix_fmt','yuv420p','-r','24',
        '-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',str(output)]
    data.update(output=rel(output),graph=bound(gpath),command=cmd,encode_log=rel(log),status='rendering_unaccepted_review' if action=='render' else 'prepared_not_rendered')
    write(manifest,data)
    if action=='render':
        with log.open('x') as f:result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
        data.update(encode_exit_code=result.returncode,status='encoded_unverified_review_only' if result.returncode==0 else 'failed_partial_preserved')
        if not result.returncode:data['output_sha256']=sha(output)
        manifest.write_text(json.dumps(data,indent=2)+'\n')
        if result.returncode:raise RuntimeError('Encode failed; partial artifacts preserved')
    print(json.dumps({'status':data['status'],'build':str(manifest),'output':str(output)},indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['check','prepare','render'])
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--mode',choices=['full','pilot'],default='full')
    p.add_argument('--segment',choices=REQUIRED)
    p.add_argument('--name',help='New versioned filename, required for prepare/render')
    a=p.parse_args()
    if a.action!='check' and not a.name:p.error('--name required for prepare/render')
    data=prepare(a.manifest.resolve(),a.mode,a.segment)
    if a.action=='check':
        print(json.dumps({'status':'inputs_verified_not_rendered','mode':a.mode,'selected':[e['segment'] for e in data['replacements']],
            'mapping_checks':data['mapping_checks']},indent=2))
    else:save_or_render(data,a.action,a.name)


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,subprocess.CalledProcessError,RuntimeError) as e:
        print('ERROR: '+str(e),file=sys.stderr);raise SystemExit(2)
