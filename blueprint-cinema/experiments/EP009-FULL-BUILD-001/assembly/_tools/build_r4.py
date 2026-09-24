#!/usr/bin/env python3
"""EP009 presenter picture revision over the frozen full r3 timeline.

Default is read-only readiness. --write-plan preserves a new review BUILD and
filter graph; --render also encodes. Full-review requires all 15 revised segment
clips and the separate 86-frame opening. Partial-review requires repeatable
--select IDs and changes only those selections. Flagged clips remain held.
Neither mode is owner acceptance or a release master.
"""
import argparse
import copy
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from build_r3 import A, B, R, FPS, SPF, bound, probe, read, rel, sha, verify_bound, write

BASE = A / 'r3/ep009-full-r3-review-draft-BUILD.json'
BASE_SHA = '806ec203069d994fb5928c61aaa1350c788b2faf5fa3e9d2663e593ab962aa12'
OPENING = B / 'presenter-regen/opening-first-sentence/PLAN.json'
OPENING_SHA = 'e0025906240d879a5223c23fb002b576210f81c8515534153e3af8ca0aeb27a1'
INDEX = B / 'presenter-regen/final-r5/INDEX.json'
D = A / 'r4'
ELIGIBLE = ('review-ready',)


def nested_bindings(value):
    """Check hashes in per-part review provenance without inferring verdicts."""
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            verify_bound(value)
        for child in value.values():
            nested_bindings(child)
    elif isinstance(value, list):
        for child in value:
            nested_bindings(child)


def patch_row(row, interval, entry, selection):
    lo, hi = interval
    a, z = row['output_frames']
    if not a <= lo < hi <= z or entry['frames'] != hi - lo:
        raise ValueError('Replacement outside its exact mapped interval')
    replacement = {'kind': 'video', 'source': {'path': entry['path'], 'sha256': entry['sha256']},
                   'source_start_frame': 0, 'output_frames': [lo, hi], 'frames': hi-lo,
                   'presenter_selection_id': selection, 'presenter_review': copy.deepcopy(entry)}
    if [lo, hi] == [a, z]:
        replacement['original_frames'] = row['original_frames']
        row['spans'] = [replacement]
    else:
        # The only partial replacement is the newly approved opening. Its time
        # coordinates are identical in the original and frozen r3 timeline.
        if row['id'] != 'seg001' or [lo, hi] != [0, 86] or len(row['spans']) != 1:
            raise ValueError('Only the approved opening may replace a partial row')
        old = copy.deepcopy(row['spans'][0])
        if old['output_frames'] != [0, 135] or old['source_start_frame'] != 0:
            raise ValueError('F01 source mapping changed')
        replacement['original_frames'] = [0, 86]
        old.update(original_frames=[86, 135], output_frames=[86, 135],
                   source_start_frame=86, frames=49)
        row['spans'] = [replacement, old]
    row['presenter_review'] = copy.deepcopy(entry)
    if row['id'] == 'seg044':
        row['output_cues']['picture'] = 'Corrected locked paragraph delivered by revised P08 presenter; pending owner review.'


def frame_map(rows):
    out = []
    for row in rows:
        for s in row['spans']:
            if s['output_frames'] != [len(out), len(out)+s['frames']]:
                raise ValueError('Gap, overlap or wrong frame count in picture mapping')
            out.extend((s['kind'], s['source']['path'], s['source']['sha256'], s['source_start_frame']+i)
                       for i in range(s['frames']))
    return out


def prepare(index_path, mode, selected=None):
    base = read(verify_bound({'path': rel(BASE), 'sha256': BASE_SHA}))
    evidence = read(BASE.with_name(BASE.name.replace('-BUILD.json', '-VERIFICATION.json')))
    if evidence['build'] != bound(BASE) or evidence['status'] != 'technical_checks_passed_review_required':
        raise ValueError('Frozen r3 base lacks current technical verification')
    revision = read(verify_bound(base['revision']))
    for key in ('master', 'timemap', 'transcript', 'sources'):
        verify_bound(revision[key])
    lock = read(verify_bound(base['owner_scoped_lock']))
    if lock.get('status') != 'locked_by_owner':
        raise ValueError('Scoped owner lock missing')
    for key in ('source', 'brand_preview', 'hospitality_preview', 'selected_paragraph_audio',
                'selected_script', 'time_map', 'master_carrier'):
        verify_bound(lock[key])
    if lock['master_carrier'] != revision['master'] or lock['time_map'] != revision['timemap']:
        raise ValueError('r3 audio or timing differs from scoped owner lock')
    verify_bound(base['film_selections'])
    opening = read(verify_bound({'path': rel(OPENING), 'sha256': OPENING_SHA}))
    if opening['master'] != base['master'] or opening['master_frames'] != [0, 86]:
        raise ValueError('P00 plan does not bind the unchanged r3 opening')
    verify_bound(opening['owner_direction'])
    original = base['all_75_rows']
    rows = copy.deepcopy(original)
    if len(rows) != 75 or base['total_frames'] != 29323:
        raise ValueError('Expected frozen 75-row 29,323-frame r3 base')
    expected = {r['id']: r['output_frames'] for r in rows if r['lane'] == 'presenter'}
    if len(expected) != 15 or expected['seg044'] != [15920, 16263]:
        raise ValueError('Presenter segment contract changed')
    expected = {'P00': [0, 86], **expected}
    if mode == 'full-review' and selected:
        raise ValueError('--select is only for explicit partial-review builds')
    if mode == 'partial-review' and not selected:
        raise ValueError('Partial-review requires explicit --select IDs, for example --select P00')
    requested = list(expected) if mode == 'full-review' else list(dict.fromkeys(selected))
    if not set(requested).issubset(expected):
        raise ValueError('Unknown presenter selection ID')
    errors, pending, used, flagged, replacements = [], [], [], [], []
    index = read(index_path) if index_path.exists() else {'segments': {}}
    if index_path.exists():
        plan = read(verify_bound(index['plan']))
        if index['master'] != base['master']:
            raise ValueError('Presenter index must explicitly bind the current r3 master')
        verify_bound(index['master'])
        expected_part_ids = {p['part_id'] for p in plan['parts']}
        if not {'P00', 'P08r3a', 'P08r3b'}.issubset(expected_part_ids) or expected_part_ids.intersection({'P08a','P08b','P08c'}):
            raise ValueError('Selected plan omits revised parts or still includes obsolete P08')
    else:
        expected_part_ids = set()
    for sid, interval in expected.items():
        if sid not in requested:
            pending.append({'selection': sid, 'output_frames': interval, 'retained_r3': True,
                            'reasons': ['Not selected for this explicit partial review']})
            continue
        e = index.get('opening_insert', {}) if sid == 'P00' else index.get('segments', {}).get(sid, {})
        reasons = []
        if e.get('status') not in ELIGIBLE or e.get('technical_complete') is not True or e.get('owner_accepted') is not False:
            reasons.append('No explicit technically complete, unaccepted review-ready selection')
        if e.get('status') == 'review-ready-flagged' or e.get('flagged_parts'):
            reasons.append('Flagged presenter held; this builder does not clear review flags')
            flagged.append({'selection':sid,'status':e.get('status'),'flagged_parts':e.get('flagged_parts',[]),
                            'part_reviews':e.get('part_reviews',{})})
        if e.get('output_frames') != interval or e.get('frames') != interval[1]-interval[0]:
            reasons.append('Exact r3 output range/frame count missing or incorrect')
        parts = e.get('parts_used', [])
        if not parts or not set(parts).issubset(expected_part_ids):
            reasons.append('Parts are absent or outside the selected plan')
        if sid == 'P00' and parts != ['P00']:
            reasons.append('Opening must use only P00')
        if sid == 'seg044' and parts != ['P08r3a', 'P08r3b']:
            reasons.append('Corrected P08 must use only the two revised parts in order')
        reviews = e.get('part_reviews', {})
        if any(not reviews.get(p) for p in parts):
            reasons.append('Per-part review provenance missing')
        if not reasons:
            try:
                video = verify_bound({'path': e['path'], 'sha256': e['sha256']})
                if not video.is_relative_to(B/'presenter-regen/final-r5'):
                    raise ValueError('Use the separate final-r5 clip directory')
                nested_bindings(reviews)
                v = next(s for s in probe(video)['streams'] if s['codec_type'] == 'video')
                if (v['width'], v['height'], v['r_frame_rate'], int(v['nb_read_frames'])) != (1280,720,'24/1',e['frames']):
                    raise ValueError('Replacement must be exact-length 1280x720 24fps')
            except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
                reasons.append(str(exc))
        if reasons:
            pending.append({'selection': sid, 'output_frames': interval, 'reasons': reasons})
            continue
        row = next(r for r in rows if r['id'] == ('seg001' if sid == 'P00' else sid))
        patch_row(row, interval, e, sid)
        used.append(sid)
        replacements.append({'selection':sid, 'output_frames':interval, 'entry':copy.deepcopy(e)})
    missing_requested = [x for x in pending if x['selection'] in requested]
    if missing_requested:
        errors.append(f'{len(missing_requested)} requested presenter selections pending or flagged; render held')
    oldmap, newmap = frame_map(original), frame_map(rows)
    allowed = {f for e in replacements for f in range(*e['output_frames'])}
    if len(newmap) != 29323 or any(x != y and f not in allowed for f,(x,y) in enumerate(zip(oldmap,newmap))):
        raise ValueError('An unapproved picture frame changed or timeline length shifted')
    # Retained movie sources are hash-bound; never flatten/reencode the full r3.
    for s in {s['source']['path']:s for r in rows for s in r['spans']}.values():
        verify_bound(s['source'])
    return {'record_type':'ep009_r4_review_build', 'status':'blocked' if errors else 'ready_to_render_review_candidate',
            'scope':'full', 'mode':mode, 'owner_accepted':False, 'delivery_master':False,
            'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'base_build':bound(BASE), 'base_verification':bound(BASE.with_name(BASE.name.replace('-BUILD.json','-VERIFICATION.json'))),
            'revision':base['revision'], 'master':base['master'], 'timemap':revision['timemap'],
            'transcript':revision['transcript'], 'owner_scoped_lock':base['owner_scoped_lock'],
            'film_selections':base['film_selections'], 'opening_plan':bound(OPENING),
            'presenter_index':bound(index_path) if index_path.exists() else None,
            'presenter_plan':index.get('plan'), 'output_master_frames':[0,29323], 'total_frames':29323,
            'all_75_rows':rows, 'presenter_replacements':{'expected':16,'requested':requested,'used':used,'pending':pending,'flagged':flagged,'entries':replacements},
            'mapping_checks':{'all_29323_frame_assignments_compared':True,'only_selected_presenter_intervals_change':True,
                              'all_75_row_bounds_preserved':True,'r3_master_and_timing_unchanged':True,'F01_remainder_source_start_frame':86 if 'P00' in used else 0},
            'errors':errors, 'limitations':['Technical review candidate only; flagged parts remain flagged.',
                'No normal-speed audiovisual, mouth-sync, owner or release acceptance.',
                'Pending selections retain their exact r3 source pictures in explicit partial-review mode.']}


def graph_for(data):
    spans = [{**copy.deepcopy(s),'segment_id':r['id']} for r in data['all_75_rows'] for s in r['spans']]
    groups = []
    for s in spans:
        rng = [s['source_start_frame'],s['source_start_frame']+s['frames']]
        if groups and groups[-1]['source'] == s['source'] and groups[-1]['kind'] == s['kind'] and rng[0] >= groups[-1]['ranges'][-1][1]:
            groups[-1]['ranges'].append(rng); groups[-1]['frames'] += s['frames']
        else:
            groups.append({'source':s['source'],'kind':s['kind'],'ranges':[rng],'frames':s['frames']})
    if any(g['frames'] < 2 for g in groups):
        raise ValueError('Isolated one-frame concat branch prohibited')
    sources = {g['source']['path']:g['source'] for g in groups}; paths = list(sources)
    graph, inputs, counts = [], [], {}
    for i,p in enumerate(paths):
        matches = [g for g in groups if g['source']['path'] == p]
        inputs += (['-loop','1','-framerate','24'] if matches[0]['kind']=='still' else ['-threads','1'])+['-i',str(R/p)]
        if len(matches)>1:
            graph.append(f'[{i}:v]split={len(matches)}'+''.join(f'[src{i}_{j}]' for j in range(len(matches))))
    label = None
    if any(g['kind']=='still' for g in groups):
        label_record = read(A/'r3/presenter-pending-label.json'); label = verify_bound(label_record['image'])
        inputs += ['-loop','1','-framerate','24','-i',str(label)]
    for j,g in enumerate(groups):
        i = paths.index(g['source']['path']); k=counts.get(i,0); counts[i]=k+1
        src = f'[src{i}_{k}]' if sum(x['source']==g['source'] for x in groups)>1 else f'[{i}:v]'
        a,z = g['ranges'][0][0],g['ranges'][-1][1]
        select = f'trim=start_frame={a}:end_frame={z}' if z-a==g['frames'] else f'trim=end_frame={z},select=\''+'+'.join(f'between(n,{x},{y-1})' for x,y in g['ranges'])+'\''
        scale = 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720' if g['kind']=='still' else 'scale=1280:720'
        filt = f'{select},setpts=N/(24*TB),{scale},setsar=1,format=yuv420p'
        if g['kind']=='still':
            graph += [src+filt+f'[still{j}]',f'[still{j}][{len(paths)}:v]overlay=shortest=1:eof_action=repeat[v{j}]']
        else:
            graph.append(src+filt+f'[v{j}]')
    graph.append(''.join(f'[v{j}]' for j in range(len(groups)))+f'concat=n={len(groups)}:v=1:a=0,fps=24[vout]')
    inputs += ['-threads','1','-i',str(verify_bound(data['master']))]
    audio_index=len(paths)+(1 if label else 0); samples=data['total_frames']*SPF
    graph.append(f'[{audio_index}:a]pan=stereo|c0=c0|c1=c0,apad=whole_len={samples},atrim=end_sample={samples},asetpts=N/SR/TB[aout]')
    data.update(source_spans=spans,render_groups=groups,sources=list(sources.values()),review_label=bound(label) if label else None)
    return ';\n'.join(graph)+'\n',inputs


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--index',type=Path,default=INDEX)
    p.add_argument('--mode',choices=['full-review','partial-review'],default='full-review')
    p.add_argument('--select',action='append',help='Explicit partial-review selection: P00 or a presenter segment ID; repeat for each')
    p.add_argument('--name',default='ep009-full-r4-review-draft')
    p.add_argument('--write-plan',action='store_true')
    p.add_argument('--render',action='store_true')
    args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.name):
        raise ValueError('Use a new simple artifact name')
    data=prepare(args.index.resolve(),args.mode,args.select)
    if data['errors'] or not (args.write_plan or args.render):
        print(json.dumps({k:data[k] for k in ('status','mode','presenter_replacements','errors')},indent=2))
        return 2 if data['errors'] else 0
    graph,inputs=graph_for(data)
    D.mkdir(exist_ok=True); (A/'qa/r4').mkdir(exist_ok=True)
    manifest=D/(args.name+'-BUILD.json'); graphpath=D/(args.name+'-graph.txt'); log=D/(args.name+'-encode.log'); output=A/'qa/r4'/(args.name+'.mp4')
    for path in (manifest,graphpath,log,output):
        if path.exists():raise FileExistsError(f'Preserve existing artifact: {path}')
    with graphpath.open('x') as f:f.write(graph)
    cmd=['ffmpeg','-n','-v','error','-stats','-filter_complex_threads','2',*inputs,'-/filter_complex',str(graphpath),
         '-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','16','-threads','2',
         '-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',str(output)]
    data.update(output=rel(output),graph=bound(graphpath),command=cmd,encode_log=rel(log),
                status='rendering' if args.render else 'prepared_not_rendered')
    write(manifest,data)
    if args.render:
        with log.open('x') as f:result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
        data['status']='encoded_unverified_review_only' if result.returncode==0 else 'failed_partial_preserved'
        data['encode_exit_code']=result.returncode
        if result.returncode==0:data['output_sha256']=sha(output)
        manifest.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'build':str(manifest),'output':str(output)},indent=2))
    return data.get('encode_exit_code',0)


if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);raise SystemExit(2)
