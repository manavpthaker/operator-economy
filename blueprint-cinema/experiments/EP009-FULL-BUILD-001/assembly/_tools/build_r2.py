#!/usr/bin/env python3
"""Build an EP009 r2 review candidate, preserving every r1 artifact.

Default: inspect inputs and print readiness without writing or rendering.
  python build_r2.py --scene-source <new seg057__seg058 MP4>
  python build_r2.py --scene-source <new MP4> --render
  python build_r2.py --scene-source <new MP4> --mode graphics-only-draft --render

Optional --opening-source and --seg020-source replace their complete original
scene plates while retaining every segment's source-frame offset and duration.

Full-review requires all 15 regenerated presenter segments. Graphics-only-draft
uses the complete retained r1 presenter set; it never silently mixes replacements.
This is an experimental assembly reference, not a Resolve delivery master.
"""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
A = Path(__file__).resolve().parents[1]
B = A.parent
ROOT = next(p for p in B.parents if (p / '.agents').is_dir())
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
MASTER_SHA = 'e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944'
FPS, SR = 24, 48000


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def rel(path):
    return str(Path(path).resolve().relative_to(ROOT))


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-count_packets', '-show_entries',
        'stream=codec_type,width,height,r_frame_rate,nb_read_packets,duration,sample_rate,channels:format=duration',
        '-of', 'json', str(path)]))


def write_new(path, data):
    with Path(path).open('x') as f:
        f.write(json.dumps(data, indent=2) + '\n')


def graph_for(rows):
    paths = list(dict.fromkeys(r['path'] for r in rows))
    uses = {p: [r for r in rows if r['path'] == p] for p in paths}
    lines, counts = [], {}
    for i, p in enumerate(paths):
        if len(uses[p]) > 1:
            lines.append(f'[{i}:v:0]split={len(uses[p])}' + ''.join(f'[s{i}_{k}]' for k in range(len(uses[p]))))
    for j, row in enumerate(rows):
        i = paths.index(row['path'])
        k = counts.get(i, 0)
        counts[i] = k + 1
        src = f'[s{i}_{k}]' if len(uses[row['path']]) > 1 else f'[{i}:v:0]'
        start, stop = row['src_start'], row['src_start'] + row['frames']
        lines.append(f'{src}trim=start_frame={start}:end_frame={stop},setpts=PTS-STARTPTS,scale=1280:720,setsar=1,format=yuv420p[v{j}]')
    lines.append(''.join(f'[v{j}]' for j in range(len(rows))) + f'concat=n={len(rows)}:v=1:a=0,fps=24[vout]')
    samples = rows[-1]['out'][1] * (SR // FPS)
    lines.append(f'[{len(paths)}:a:0]pan=stereo|c0=c0|c1=c0,apad=whole_len={samples},atrim=end_sample={samples},asetpts=N/SR/TB[aout]')
    inputs = []
    for p in paths:
        inputs += ['-threads', '1', '-i', str(ROOT / p)]
    inputs += ['-threads', '1', '-i', str(MASTER)]
    return ';\n'.join(lines) + '\n', inputs


def prepare(mode, scene_source, opening_source=None, seg020_source=None):
    plan = read(B / 'direction/SHOT-PLAN.json')
    rows = read(A / '_tools/sources-r1.json')
    originals = {r['id']: dict(r) for r in rows}
    by_id = {r['id']: r for r in rows}
    errors, warnings, pending, available, flagged, changed = [], [], [], [], [], []
    scene_replacements, scene_expected_frames = [], {}
    if [r['id'] for r in rows] != [s['id'] for s in plan['segments']]:
        errors.append('Retained r1 source order does not match the locked plan.')
    for s in plan['segments']:
        r = by_id.get(s['id'])
        if not r or r['out'] != s['frames'] or r['frames'] != s['frames'][1] - s['frames'][0]:
            errors.append(f"{s['id']}: retained frame boundaries differ from locked plan")
    if rows[0]['out'][0] != 0 or any(a['out'][1] != b['out'][0] for a, b in zip(rows, rows[1:])):
        errors.append('Retained timeline has a gap or overlap.')
    if sha(MASTER) != MASTER_SHA or plan['master']['sha256'] != MASTER_SHA:
        errors.append('Locked narration master hash differs.')
    if rows[-1]['out'][1] != 29607:
        errors.append('Expected locked 29607-frame timeline.')

    idx_path = B / 'presenter-regen/INDEX.json'
    idx = read(idx_path).get('segments', {}) if idx_path.exists() else {}
    for r in rows:
        if r['lane'] != 'presenter':
            continue
        e = idx.get(r['id'], {})
        reasons = []
        path = ROOT / e.get('path', '__missing__')
        if e.get('status') not in ('review-ready', 'review-ready-flagged'):
            reasons.append(f"regeneration index not review-ready (status: {e.get('status', 'missing')})")
        if e.get('technical_complete') is not True:
            reasons.append('technical completion not explicitly recorded')
        if e.get('owner_accepted') is not False:
            reasons.append('explicit unaccepted review state absent or incorrect')
        if not path.is_file():
            reasons.append('regenerated clip absent')
        if e.get('frames') != r['frames']:
            reasons.append('replacement frame contract absent or incorrect')
        if path.is_file() and sha(path) != e.get('sha256'):
            reasons.append('replacement hash absent or incorrect')
        if reasons:
            pending.append({'segment': r['id'], 'reasons': reasons})
            continue
        available.append(r['id'])
        if e.get('status') == 'review-ready-flagged' or e.get('flagged_parts'):
            flagged.append({'segment': r['id'], 'status': e['status'],
                            'parts': e.get('flagged_parts', []), 'part_reviews': e.get('part_reviews', {})})
        if mode == 'full-review':
            changed.append({'segment': r['id'], 'old_path': r['path'], 'old_sha256': r['sha256'],
                            'new_path': e['path'], 'new_sha256': e['sha256']})
            r.update(path=e['path'], sha256=e['sha256'], src_start=0,
                     index=rel(idx_path), index_sha256=sha(idx_path), index_status=e['status'],
                     replacement_parts=e.get('parts_used', []), technical_complete=True,
                     owner_accepted=False, flagged_parts=e.get('flagged_parts', []),
                     part_reviews=e.get('part_reviews', {}))
    if mode == 'full-review' and pending:
        errors.append(f'{len(pending)} presenter replacements pending; full-review rendering refused.')
    if mode == 'graphics-only-draft':
        warnings.append('GRAPHICS-ONLY DRAFT: all 15 r1 presenter segments remain, regardless of replacement availability.')
    if flagged:
        warnings.append('Presenter index contains flagged parts. Technical assembly does not clear their sync or creative review.')

    def replace_scene(seed_id, source, option):
        old = originals[seed_id]
        group = [r for r in originals.values() if r['path'] == old['path']]
        expected = int(old['probe']['nb_read_packets'])
        scene = source.resolve()
        try:
            scene_rel = rel(scene)
        except ValueError:
            errors.append(f'{option}: replacement scene must be retained inside the repository.')
            return
        if not scene.is_file():
            errors.append(f'{option}: replacement scene absent: {scene}')
            return
        h = sha(scene)
        if scene_rel in {r['path'] for r in originals.values()}:
            errors.append(f'{option}: use a new path, preserving every r1 source file.')
        if h == old['sha256']:
            errors.append(f'{option}: replacement scene is byte-identical to r1.')
        if sha(ROOT / old['path']) != old['sha256']:
            errors.append(f'{option}: original r1 source no longer matches its retained hash.')
        if scene_rel in scene_expected_frames and scene_expected_frames[scene_rel] != expected:
            errors.append(f'{option}: one replacement path cannot serve different whole-source frame contracts.')
        scene_expected_frames[scene_rel] = expected
        scene_replacements.append({'option': option, 'segments': [r['id'] for r in group],
                                   'old_path': old['path'], 'new_path': scene_rel, 'sha256': h,
                                   'whole_source_frames_expected': expected})
        for original in group:
            sid = original['id']
            r = by_id[sid]
            changed.append({'segment': sid, 'old_path': original['path'], 'old_sha256': original['sha256'],
                            'new_path': scene_rel, 'new_sha256': h, 'src_start_preserved': original['src_start']})
            r.update(path=scene_rel, sha256=h, src_start=original['src_start'],
                     index=f'explicit {option}; see build manifest', index_status='replacement review candidate')

    if scene_source is None:
        errors.append('Pass --scene-source for the new 1757-frame seg057__seg058 render.')
    else:
        replace_scene('seg057', scene_source, '--scene-source')
    if opening_source is not None:
        replace_scene('seg004', opening_source, '--opening-source')
    if seg020_source is not None:
        replace_scene('seg020', seg020_source, '--seg020-source')

    cache = {}
    for r in rows:
        path = ROOT / r['path']
        if not path.is_file():
            errors.append(f"{r['id']}: source absent: {r['path']}")
            continue
        if r['path'] not in cache:
            cache[r['path']] = (sha(path), probe(path))
        h, p = cache[r['path']]
        v = next((s for s in p['streams'] if s['codec_type'] == 'video'), {})
        if h != r['sha256']:
            errors.append(f"{r['id']}: source hash mismatch")
        if (v.get('width'), v.get('height'), v.get('r_frame_rate')) != (1280, 720, '24/1'):
            errors.append(f"{r['id']}: source must be 1280x720 at 24 fps")
        frames = int(v.get('nb_read_packets', 0))
        if r['src_start'] + r['frames'] > frames:
            errors.append(f"{r['id']}: source shortfall")
        if r['id'] in available and mode == 'full-review' and frames != r['frames']:
            errors.append(f"{r['id']}: presenter source must have exactly {r['frames']} frames")
        expected_scene_frames = scene_expected_frames.get(r['path'])
        if expected_scene_frames is not None and frames != expected_scene_frames:
            errors.append(f"{r['id']}: replacement whole scene must have exactly {expected_scene_frames} frames, got {frames}")
        r['sha_ok'] = h == r['sha256']
        r['probe'] = v

    result = {
        'record_type': 'ep009_r2_assembly_build', 'revision': 'r2', 'mode': mode,
        'status': 'blocked' if errors else 'ready_to_render_review_candidate',
        'owner_accepted': False, 'delivery_master': False,
        'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'base_sources': {'path': rel(A / '_tools/sources-r1.json'), 'sha256': sha(A / '_tools/sources-r1.json')},
        'shot_plan': {'path': rel(B / 'direction/SHOT-PLAN.json'), 'sha256': sha(B / 'direction/SHOT-PLAN.json')},
        'master': {'path': rel(MASTER), 'sha256': MASTER_SHA},
        'total_frames': 29607, 'picture_seconds': 29607 / FPS,
        'master_seconds': plan['master']['duration_seconds'],
        'audio_design': 'One continuous locked master, unity mono-to-stereo upmix; zero padding only to picture length. No source-clip audio, music, effects, or loudness normalization.',
        'timing_note': 'Locked plan ends at 29607, including seg075 at 186 frames. Generic round(end*24) would end at 29606; preserve the explicit plan and its 23 ms picture tail.',
        'presenter_replacements': {'expected': 15, 'available': available, 'pending': pending, 'flagged': flagged,
                                   'used': available if mode == 'full-review' else [],
                                   'retained_r1': [r['id'] for r in rows if r['lane'] == 'presenter'] if mode == 'graphics-only-draft' else []},
        'scene_replacements': scene_replacements,
        'changes': changed, 'sources': rows, 'errors': errors, 'warnings': warnings,
        'limitations': ['Technical assembly is not creative acceptance or lip-sync verification.',
                        'This experimental review candidate is not a finished Resolve delivery master.',
                        'Source packet counts are a precheck; verify_r2.py decodes every encoded output frame.'],
    }
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scene-source', type=Path, help='New shared 1757-frame scene MP4; never overwrite r1 source.')
    ap.add_argument('--opening-source', type=Path, help='Optional new complete seg004__seg006 plate; retain r1 source offsets.')
    ap.add_argument('--seg020-source', type=Path, help='Optional new complete seg020 plate; retain r1 duration.')
    ap.add_argument('--mode', choices=['full-review', 'graphics-only-draft'], default='full-review')
    ap.add_argument('--render', action='store_true', help='Explicitly encode; otherwise inspect only, with no writes.')
    args = ap.parse_args()
    data = prepare(args.mode, args.scene_source, args.opening_source, args.seg020_source)
    summary = {k: data[k] for k in ('status', 'mode', 'total_frames', 'scene_replacements', 'presenter_replacements', 'errors', 'warnings')}
    print(json.dumps(summary, indent=2), flush=True)
    if data['errors']:
        return 2
    if not args.render:
        return 0
    suffix = 'review-candidate' if args.mode == 'full-review' else 'graphics-only-draft'
    stem = f'ep009-full-r2-{suffix}'
    output, manifest = A / 'qa' / f'{stem}.mp4', A / f'BUILD-r2-{suffix}.json'
    graph_path, log = A / '_tools' / f'graph-r2-{suffix}.txt', A / '_tools' / f'encode-r2-{suffix}.log'
    for path in (output, manifest, graph_path, log):
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite retained artifact: {path}')
    graph, inputs = graph_for(data['sources'])
    cmd = ['ffmpeg', '-n', '-v', 'error', '-stats', '-filter_complex_threads', '2', *inputs,
           '-/filter_complex', str(graph_path), '-map', '[vout]', '-map', '[aout]',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', '-threads', '2',
           '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(output)]
    data.update(status='rendering_review_candidate', output=rel(output), graph=rel(graph_path),
                command=cmd, encode_log=rel(log),
                ffmpeg_version=subprocess.check_output(['ffmpeg', '-version'], text=True).splitlines()[0])
    with graph_path.open('x') as f:
        f.write(graph)
    write_new(manifest, data)
    with log.open('x') as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    data['encode_exit_code'] = result.returncode
    data['status'] = 'encoded_unverified_review_candidate' if result.returncode == 0 else 'encode_failed_partial_artifact_retained'
    if result.returncode == 0:
        data['output_sha256'] = sha(output)
    manifest.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'status': data['status'], 'manifest': str(manifest), 'output': str(output)}))
    return result.returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2)
