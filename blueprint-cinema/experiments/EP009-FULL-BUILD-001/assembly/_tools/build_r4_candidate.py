#!/usr/bin/env python3
"""Build only the specifically authorized, flagged P00 opening review candidate.

This separate path cannot select other presenter clips, clear a flag, update the
index or activate a plan. It preserves the normal r4 builder's eligibility rules.
"""
import argparse
import copy
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from build_r3 import A, B, R, bound, probe, read, rel, sha, verify_bound, write
from build_r4 import BASE, BASE_SHA, frame_map, graph_for, nested_bindings

INSTRUCTION = A/'r4/P00-CANDIDATE-INSTRUCTION.json'
INSTRUCTION_SHA = '51b26118ce507b6ed25c95610e1637e8c47acf2f2eacd6866388499be77b6b2e'
CANDIDATE = B/'presenter-regen/P00/qa/opening-P00-private-review-r1.mp4'
CANDIDATE_SHA = 'f1618fcf58cb9924656e226ce1a0d494fc545ca944890366e5de910fadb24307'
DECISION = B/'direction/r3-owner-revisions/P00-CANDIDATE-DECISION.json'
DECISION_SHA = 'bdd2693ed60aeae2e00330666509ed1741e62e1012247cafe7b2fb3c2342c516'
PROTECTED = [
    B/'presenter-regen/_tools/regen.py', B/'presenter-regen/_tools/regen_r5.py',
    B/'presenter-regen/EXECUTION-PLAN-r5.json', B/'presenter-regen/ACTIVE-PLAN.json',
    B/'presenter-regen/final-r5/INDEX.json', B/'presenter-regen/P00/NOTES.json',
    B/'presenter-regen/P00/SYNC-GATE.json', A/'_tools/build_r4.py', A/'_tools/verify_r4.py',
]


def prepare(scope):
    verify_bound({'path':rel(INSTRUCTION),'sha256':INSTRUCTION_SHA})
    decision=read(verify_bound({'path':rel(DECISION),'sha256':DECISION_SHA}))
    nested_bindings(decision['evidence'])
    base = read(verify_bound({'path':rel(BASE),'sha256':BASE_SHA}))
    base_verification = BASE.with_name(BASE.name.replace('-BUILD.json','-VERIFICATION.json'))
    if read(base_verification)['build'] != bound(BASE) or read(base_verification)['status'] != 'technical_checks_passed_review_required':
        raise ValueError('Frozen r3 verification changed')
    revision = read(verify_bound(base['revision']))
    for key in ('master','timemap','transcript','sources'):
        verify_bound(revision[key])
    lock = read(verify_bound(base['owner_scoped_lock']))
    if lock['status'] != 'locked_by_owner' or lock['master_carrier'] != revision['master'] or lock['time_map'] != revision['timemap']:
        raise ValueError('Scoped owner lock differs')
    for key in ('source','brand_preview','hospitality_preview','selected_paragraph_audio','selected_script','time_map','master_carrier'):
        verify_bound(lock[key])
    verify_bound(base['film_selections'])
    verify_bound({'path':rel(CANDIDATE),'sha256':CANDIDATE_SHA})
    v = next(s for s in probe(CANDIDATE)['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames'])) != (1280,720,'24/1',86):
        raise ValueError('Exact authorized candidate must be 86 frames at 1280x720 24fps')
    notes = read(B/'presenter-regen/P00/NOTES.json')
    if notes['flagged'] is not True or notes['owner_accepted'] is not False:
        raise ValueError('This narrowly scoped path requires the preserved flagged review state')
    nested_bindings(notes.get('evidence',{}))
    original = base['all_75_rows']; rows = copy.deepcopy(original)
    if len(rows)!=75 or len(frame_map(original))!=29323:
        raise ValueError('Frozen timeline shape changed')
    row = rows[0]
    if row['id']!='seg001' or row['output_frames']!=[0,135] or len(row['spans'])!=1 or row['spans'][0]['source_start_frame']!=0:
        raise ValueError('Opening F01 mapping changed')
    old = copy.deepcopy(row['spans'][0])
    old.update(original_frames=[86,135],output_frames=[86,135],source_start_frame=86,frames=49)
    row['spans']=[{'kind':'video','source':bound(CANDIDATE),'original_frames':[0,86],
                   'output_frames':[0,86],'source_start_frame':0,'frames':86,
                   'candidate_id':'P00-exact-private-review-r1','sync_status':'flagged_unresolved',
                   'owner_accepted':False},old]
    before,after=frame_map(original),frame_map(rows)
    changed=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]
    if len(after)!=29323 or changed!=list(range(86)):
        raise ValueError('Only the 86 authorized picture frames may differ')
    if [{k:v for k,v in x.items() if k!='spans'} for x in rows] != [{k:v for k,v in x.items() if k!='spans'} for x in original]:
        raise ValueError('A cue or segment field changed')
    for s in {s['source']['path']:s for r in rows for s in r['spans']}.values():
        verify_bound(s['source'])
    total=29323 if scope=='full' else 252
    if scope!='full':
        rows=rows[:2]
        if rows[-1]['output_frames'][1]!=252:raise ValueError('Opening context must end exactly at 10.5 seconds')
    return {'record_type':'ep009_exact_P00_flagged_review_candidate_build','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'prepared_candidate_lipsync_unresolved','scope':scope,'total_frames':total,'output_master_frames':[0,total],
        'all_75_rows':rows,'full_timeline_row_count':75,'candidate_instruction':bound(INSTRUCTION),'candidate_decision':bound(DECISION),
        'base_build':bound(BASE),'base_verification':bound(base_verification),'revision':base['revision'],
        'master':base['master'],'timemap':revision['timemap'],'transcript':revision['transcript'],
        'owner_scoped_lock':base['owner_scoped_lock'],'film_selections':base['film_selections'],
        'candidate':{'source':bound(CANDIDATE),'output_frames':[0,86],'source_frames':[0,86],
            'status':'flagged_lipsync_unresolved_review_candidate','notes':bound(B/'presenter-regen/P00/NOTES.json'),
            'sync_gate':bound(B/'presenter-regen/P00/SYNC-GATE.json'),'assessment':notes['assessment'],
            'diagnostic_flags':copy.deepcopy(notes['diagnostic_flags']),
            'rationale':'Root authorized a reversible review artifact after mechanical checks and dense-frame evidence established no demonstrated gross mismatch. This does not establish perceptual sync.'},
        'protected_artifacts':[bound(p) for p in PROTECTED],
        'mapping_checks':{'all_29323_assignments_compared':True,'changed_frames':[0,86],
            'unchanged_source_assignments':29237,'all_75_cues_and_row_fields_unchanged':True,
            'F01_return_source_frames':[86,135],'F02_entry_frame':135,'unchanged_master':True},
        'sync_cleared':False,'conform_readiness_cleared':False,'owner_accepted':False,
        'bulk_cleared':False,'release_cleared':False,'delivery_master':False,
        'retained_presenter_state':{'r1_segments':14,'P08':'locked L3 still with corrected narration; presenter pending'},
        'limitations':['P00 mouth-sync flags remain unresolved; this file does not promote a selection.',
            'The final-r5 index, normal builder eligibility and bulk clearance remain untouched.',
            'Technical encoding checks do not confer normal-speed audiovisual, mouth-sync, creative or release acceptance.']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scope',choices=['full','opening-context'],default='full')
    p.add_argument('--render',action='store_true')
    args=p.parse_args(); data=prepare(args.scope)
    if not args.render:
        print(json.dumps({k:data[k] for k in ('status','scope','total_frames','candidate','mapping_checks')},indent=2));return 0
    name='ep009-full-r4-opening-candidate' if args.scope=='full' else 'ep009-r4-opening-context-candidate'
    d=A/'r4';outdir=A/'qa/r4';d.mkdir(exist_ok=True);outdir.mkdir(exist_ok=True)
    manifest=d/(name+'-BUILD.json');graphpath=d/(name+'-graph.txt');log=d/(name+'-encode.log');output=outdir/(name+'.mp4')
    for path in (manifest,graphpath,log,output):
        if path.exists():raise FileExistsError('Preserve existing artifact: '+str(path))
    graph,inputs=graph_for(data)
    with graphpath.open('x') as f:f.write(graph)
    cmd=['ffmpeg','-n','-v','error','-stats','-filter_complex_threads','2',*inputs,'-/filter_complex',str(graphpath),
         '-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','16','-threads','2',
         '-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',str(output)]
    data.update(output=rel(output),graph=bound(graphpath),command=cmd,encode_log=rel(log),
                candidate_builder=bound(Path(__file__).resolve()),status='rendering_candidate_lipsync_unresolved')
    write(manifest,data)
    with log.open('x') as f:result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    data.update(encode_exit_code=result.returncode,status='encoded_candidate_lipsync_unresolved' if result.returncode==0 else 'failed_partial_preserved')
    if result.returncode==0:data['output_sha256']=sha(output)
    for b in data['protected_artifacts']:verify_bound(b)
    manifest.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'build':str(manifest),'output':str(output)},indent=2))
    return result.returncode


if __name__=='__main__':
    raise SystemExit(main())
