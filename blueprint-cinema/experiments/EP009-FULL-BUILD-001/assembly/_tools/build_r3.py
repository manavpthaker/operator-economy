#!/usr/bin/env python3
"""Separate EP009 r3 review revision. No canonical master, plan or r2 media writes.

prepare --pickup-audio WAV --pickup-words JSON --pickup-review JSON
render --scope brand|hospitality|full [--film-selects JSON] [--name NEW-STEM]

Pickup words are {words:[{token,start,end}]} relative to the selected WAV.
Full rendering requires an explicit film-selection manifest:
{status:"selected_for_review", required_ids:["workflow"], selections:[
 {id:"workflow", original_frames:[start,end],
  source:{path:"repo/relative.mp4",sha256:"..."}, source_start_frame:0}]}
Selections replace picture only at original timeline coordinates, at original speed.
"""
import argparse
import copy
import datetime
import hashlib
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.dont_write_bytecode = True
A = Path(__file__).resolve().parents[1]
B = A.parent
R = next(p for p in B.parents if (p / '.agents').is_dir())
D = A / 'r3'
FPS, SR, SPF = 24, 48000, 2000
CUT = (1438, 1516)
REPLACE = (15998, 16547)
MASTER = R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
MASTER_SHA = 'e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944'
WT = MASTER.parents[1] / 'word-transcript.json'
BASE = A / 'BUILD-r2-graphics-only-draft.json'
TEXT = B / 'narration-revisions/r3-hospitality/paragraph.txt'
LOOK = B / 'presenter-regen/look/L3-chambray.png'
REVISION = D / 'REVISION.json'


def read(p):
    return json.loads(Path(p).read_text())


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(R))


def bound(p):
    return {'path': rel(p), 'sha256': sha(p)}


def verify_bound(b):
    p = (R / b['path']).resolve()
    p.relative_to(R)
    if sha(p) != b['sha256']:
        raise ValueError(f'Changed bound input: {p}')
    return p


def write(p, obj):
    with Path(p).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


def probe(p):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames',
        '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_read_frames,sample_rate,channels:format=duration',
        '-of', 'json', str(p)]))


def mono_params(p):
    with wave.open(str(p), 'rb') as f:
        if (f.getnchannels(), f.getsampwidth(), f.getframerate(), f.getcomptype()) != (1, 2, SR, 'NONE'):
            raise ValueError(f'Expected mono 48 kHz PCM16 WAV: {p}')
        return f.getnframes()


def digest_samples(p, start, end):
    h = hashlib.sha256()
    with wave.open(str(p), 'rb') as f:
        f.setpos(start)
        left = end - start
        while left:
            raw = f.readframes(min(left, SR * 5))
            if not raw:
                raise ValueError('Source audio shortfall')
            h.update(raw)
            left -= len(raw) // 2
    return h.hexdigest()


def mapping(f, n):
    if CUT[0] < f < CUT[1] or REPLACE[0] < f < REPLACE[1]:
        raise ValueError(f'No unchanged-source mapping inside an edited interval: {f}')
    if f <= CUT[0]:
        return f
    if f <= REPLACE[0]:
        return f - 78
    return f - 78 + n - 549


def mapped_time(t, n):
    return mapping(t * FPS, n) / FPS


def normalized(t):
    return re.sub(r'[^a-z0-9\']', '', t.lower().replace('’', "'"))


def review_label():
    """Technical video annotation; source photograph remains an untouched input."""
    path, record = D / 'presenter-pending-label.png', D / 'presenter-pending-label.json'
    if path.exists() or record.exists():
        verify_bound(read(record)['image'])
        return path
    from PIL import Image, ImageDraw, ImageFont
    font_path = Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    font = ImageFont.truetype(str(font_path), 22)
    image = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    label = 'corrected narration · presenter pending'
    box = draw.textbbox((32, 660), label, font=font)
    draw.rectangle((box[0]-9, box[1]-9, box[2]+9, box[3]+9), fill=(0, 0, 0, 184))
    draw.text((32, 660), label, font=font, fill='white')
    with path.open('xb') as f:
        image.save(f, format='PNG')
    write(record, {'image': bound(path), 'label': label, 'font': bound(font_path) if font_path.is_relative_to(R) else str(font_path),
                   'purpose': 'Transparent technical review annotation, not an edit to the locked L3 image.'})
    return path


def cues(obj, n, pickup_words):
    out = copy.deepcopy(obj)
    # Old waveform measurements are retained in source_cues. They cannot be
    # presented as measurements of an audio boundary changed by this revision.
    for key in ('cut_window_rms_dbfs', 'measured_silent_run', 'cut_method'):
        out.pop(key, None)
    for k, v in list(out.items()):
        if k in ('word_start', 'previous_word_end', 'last_word_end', 'next_word_start') and isinstance(v, (int, float)):
            if REPLACE[0] / FPS < v < REPLACE[1] / FPS:
                if k == 'next_word_start':
                    out[k] = pickup_words[0]['start']
                    out['next_word_id'] = pickup_words[0]['w_id']
                elif k == 'previous_word_end':
                    out[k] = pickup_words[-1]['end']
                    out['previous_word_id'] = pickup_words[-1]['w_id']
                else:
                    raise ValueError('Unexpected old biography word reference outside seg044')
                out['adjacent_pickup_timing_is_approximate'] = True
            else:
                out[k] = mapped_time(v, n)
        elif k == 'cut_frame' and isinstance(v, int):
            out[k] = mapping(v, n)
    return out


def prepare(audio, words_file, review_file):
    if REVISION.exists():
        raise FileExistsError('r3 already prepared; preserve it and use a new revision for changes')
    if sha(MASTER) != MASTER_SHA:
        raise ValueError('Original master hash changed')
    base, oldwt, pickupwt, pickup_review = read(BASE), read(WT), read(words_file), read(review_file)
    if (pickup_review.get('local_asr_exact_43_words') is not True or pickup_review.get('ends_in_silence') is not True
            or pickup_review.get('retimed') is not False or verify_bound(pickup_review['selected_audio']) != audio
            or verify_bound(pickupwt['audio']) != audio):
        raise ValueError('Pickup has missing, stale or incomplete word/completion evidence')
    source_words = pickupwt['words']
    expected = TEXT.read_text().split()
    if len(expected) != 43 or [normalized(w['token']) for w in source_words] != [normalized(w) for w in expected]:
        raise ValueError('Pickup words must exactly match the authorized 43-word paragraph')
    count, original_count = mono_params(audio), mono_params(MASTER)
    n = math.ceil(count / SPF)
    if n >= 549 or n < 1:
        raise ValueError('Expected a natural shorter paragraph; do not stretch to the old duration')
    previous = -1.0
    for w in source_words:
        if not (0 <= w['start'] <= w['end'] <= count / SR + .001) or w['start'] < previous:
            raise ValueError('Pickup transcript is out of range or order')
        previous = w['start']
    with wave.open(str(MASTER), 'rb') as f:
        f.setpos(CUT[0] * SPF)
        if any(f.readframes((CUT[1] - CUT[0]) * SPF)):
            raise ValueError('Brand excision contains nonzero source samples')
    D.mkdir(exist_ok=True)
    for name in ('narration-master-r3.wav', 'TIMEMAP.json', 'word-transcript-r3.json', 'SOURCES.json'):
        if (D / name).exists():
            raise FileExistsError(f'Preserve existing partial preparation: {D / name}')
    master_out = D / 'narration-master-r3.wav'
    sections, position = [], 0
    with master_out.open('xb') as out_file, wave.open(out_file, 'wb') as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(SR)
        for p, lo, hi, kind in (
            (MASTER, 0, CUT[0] * SPF, 'unchanged_original'),
            (MASTER, CUT[1] * SPF, REPLACE[0] * SPF, 'unchanged_original'),
            (audio, 0, count, 'corrected_pickup'),
            (None, 0, n * SPF - count, 'zero_pad_pickup_to_frame'),
            (MASTER, REPLACE[1] * SPF, original_count, 'unchanged_original')):
            h = hashlib.sha256(); start = position
            if p is None:
                raw = b'\0' * (hi - lo) * 2
                out.writeframesraw(raw); h.update(raw); position += hi - lo
            else:
                with wave.open(str(p), 'rb') as src:
                    src.setpos(lo); left = hi - lo
                    while left:
                        raw = src.readframes(min(left, SR * 5))
                        if not raw:
                            raise ValueError('Input shortfall during lossless master assembly')
                        out.writeframesraw(raw); h.update(raw)
                        amount = len(raw) // 2; position += amount; left -= amount
            sections.append({'kind': kind, 'source': bound(p) if p else None,
                             'source_samples': [lo, hi], 'output_samples': [start, position],
                             'pcm_sha256': h.hexdigest()})
    if mono_params(master_out) != position:
        raise ValueError('Derived master sample count differs')
    for s in sections:
        if digest_samples(master_out, *s['output_samples']) != s['pcm_sha256']:
            raise ValueError('Derived master changed samples while copying')
    pickup_start = mapping(REPLACE[0], n)
    newwords, replaced = [], []
    for w in oldwt['words']:
        overlap = w['start'] < REPLACE[1] / FPS and w['end'] > REPLACE[0] / FPS
        if overlap:
            if w['start'] < REPLACE[0] / FPS or w['end'] > REPLACE[1] / FPS:
                raise ValueError('An original word straddles the replacement boundary')
            replaced.append(w)
            continue
        newwords.append({**w, 'source_start': w['start'], 'source_end': w['end'],
                         'start': mapped_time(w['start'], n), 'end': mapped_time(w['end'], n),
                         'timing_source': 'retained_original_forced_alignment'})
    pickup_words = []
    for i, w in enumerate(source_words):
        pickup_words.append({**w, 'w_id': f'R3P08W{i:04d}', 'pickup_relative_start': w['start'],
                             'pickup_relative_end': w['end'], 'start': pickup_start / FPS + w['start'],
                             'end': pickup_start / FPS + w['end'], 'timing_source': 'corrected_pickup_alignment'})
    newwords += pickup_words
    newwords.sort(key=lambda w: (w['start'], w['end']))
    transcript = {'schema': 'oe-word-transcript-revision-v1', 'status': 'review_revision',
                  'owner_accepted': False, 'episode': 'EP009', 'parent': bound(WT),
                  'master': bound(master_out), 'master_duration_seconds': position / SR,
                  'aligned_word_count': len(newwords), 'removed_word_count': len(replaced),
                  'added_word_count': len(pickup_words), 'removed_words': replaced,
                  'pickup_transcript': bound(words_file), 'pickup_alignment_metadata': {k: v for k, v in pickupwt.items() if k != 'words'},
                  'words': newwords,
                  'limits': 'Original word IDs/tokens/timing are preserved outside the edits, with explicit time shifts. New pickup IDs do not reuse obsolete biography word IDs. This is not the canonical transcript.'}
    rows, plan = [], read(B / 'direction/SHOT-PLAN.json')
    if len(base['sources']) != 75:
        raise ValueError('Expected all 75 retained source rows')
    for original, segment in zip(base['sources'], plan['segments']):
        if original['id'] != segment['id'] or original['out'] != segment['frames']:
            raise ValueError('Source rows differ from original shot plan')
        old_in, old_out = original['out']
        new_in, new_out = mapping(old_in, n), mapping(old_out, n)
        spans = []
        if original['id'] == 'seg044':
            spans.append({'kind': 'still', 'source': bound(LOOK), 'source_start_frame': 0,
                          'original_frames': [old_in, old_out], 'output_frames': [new_in, new_out],
                          'frames': n, 'label': 'corrected narration · presenter pending'})
            output_cues = {'first_word': pickup_words[0], 'last_word': pickup_words[-1],
                           'picture': 'Locked L3 still with explicit review label; original speaking P08 is excluded.'}
        else:
            for lo, hi in ((old_in, min(old_out, CUT[0])), (max(old_in, CUT[1]), old_out)) if original['id'] == 'seg010' else ((old_in, old_out),):
                if hi <= lo:
                    continue
                spans.append({'kind': 'video', 'source': {'path': original['path'], 'sha256': original['sha256']},
                              'source_start_frame': original['src_start'] + lo - old_in,
                              'original_frames': [lo, hi], 'output_frames': [mapping(lo, n), mapping(hi, n)], 'frames': hi - lo})
            output_cues = {'in_cue': cues(segment.get('in_cue', {}), n, pickup_words), 'out_cue': cues(segment.get('out_cue', {}), n, pickup_words)}
        rows.append({'id': original['id'], 'scene': original['scene'], 'lane': original['lane'],
                     'original': original, 'original_frames': original['out'], 'output_frames': [new_in, new_out],
                     'frames': new_out - new_in, 'output_seconds': [new_in / FPS, new_out / FPS],
                     'source_cues': {'in_cue': segment.get('in_cue'), 'out_cue': segment.get('out_cue')},
                     'output_cues': output_cues, 'spans': spans})
    total_frames = 29607 - 78 - 549 + n
    if rows[0]['output_frames'][0] or rows[-1]['output_frames'][1] != total_frames or any(a['output_frames'][1] != b['output_frames'][0] for a, b in zip(rows, rows[1:])):
        raise ValueError('Mapped 75-row timeline has a gap or overlap')
    if any(sum(s['frames'] for s in row['spans']) != row['frames'] for row in rows):
        raise ValueError('Picture source span length differs from mapped row length')
    timemap = {'record_type': 'ep009_r3_time_map', 'fps': FPS, 'sample_rate': SR, 'samples_per_frame': SPF,
               'brand_excision': {'original_frames': list(CUT), 'original_samples': [x * SPF for x in CUT], 'removed_frames': 78, 'all_samples_exact_zero': True},
               'paragraph_replacement': {'segment': 'seg044', 'original_frames': list(REPLACE),
                    'original_samples': [x * SPF for x in REPLACE], 'output_frames': [pickup_start, pickup_start + n],
                    'pickup_samples': count, 'pickup_frame_padding_samples': n * SPF - count, 'new_frames': n,
                    'old_word_count': len(replaced), 'new_word_count': len(pickup_words)},
               'audio_sections': sections, 'total_frames': total_frames, 'picture_seconds': total_frames / FPS,
               'master_samples': position, 'master_seconds': position / SR,
               'final_picture_tail_samples': total_frames * SPF - position,
               'all_segment_cues': [{k: row[k] for k in ('id', 'original_frames', 'output_frames', 'output_seconds', 'source_cues', 'output_cues')} for row in rows]}
    write(D / 'TIMEMAP.json', timemap)
    write(D / 'word-transcript-r3.json', transcript)
    write(D / 'SOURCES.json', rows)
    revision = {'record_type': 'ep009_r3_prepared_revision', 'status': 'prepared_review_only',
                'owner_accepted': False, 'delivery_master': False, 'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'base_assembly_manifest': bound(BASE), 'original_master': bound(MASTER), 'original_shot_plan': bound(B / 'direction/SHOT-PLAN.json'),
                'pickup': bound(audio), 'pickup_words': bound(words_file), 'pickup_review': bound(review_file),
                'paragraph_text': bound(TEXT), 'look_still': bound(LOOK), 'master': bound(master_out),
                'timemap': bound(D / 'TIMEMAP.json'), 'transcript': bound(D / 'word-transcript-r3.json'), 'sources': bound(D / 'SOURCES.json'),
                'total_frames': total_frames, 'pickup_frames': n,
                'audio_design': 'Lossless PCM concatenation: original slices unchanged; complete selected pickup unchanged; less than one frame of zero padding after pickup. No source-video audio, speed change, loudness processing or added fades.',
                'limitations': ['All presenter replacements remain pending. Corrected P08 uses a visibly labeled still, never old speaking footage against new words.', 'Full render additionally requires bound new film selections.', 'No final editorial, lip-sync, Resolve, owner or publication acceptance.']}
    write(REVISION, revision)
    print(json.dumps({'revision': str(REVISION), 'total_frames': total_frames, 'pickup_frames': n, 'old_words': len(replaced), 'new_words': len(pickup_words)}, indent=2))


def apply_films(rows, manifest):
    obj = read(manifest)
    patches = obj.get('selections', [])
    required = obj.get('required_ids', [])
    ids = [p['id'] for p in patches]
    if obj.get('status') != 'selected_for_review' or not required or not patches or len(set(ids)) != len(ids) or not set(required).issubset(ids):
        raise ValueError('Full r3 requires every explicitly required film selection')
    ranges = sorted(tuple(p['original_frames']) for p in patches)
    if any(a[1] > b[0] for a, b in zip(ranges, ranges[1:])):
        raise ValueError('Film selections overlap')
    for p in patches:
        lo, hi = p['original_frames']
        if not (0 <= lo < hi <= 29607) or any(max(lo, a) < min(hi, z) for a, z in (CUT, REPLACE)):
            raise ValueError('Film replacement crosses a removed or rewritten interval')
        video = verify_bound(p['source'])
        stream = next(s for s in probe(video)['streams'] if s['codec_type'] == 'video')
        if (stream['width'], stream['height'], stream['r_frame_rate']) != (1280, 720, '24/1') or p['source_start_frame'] < 0 or p['source_start_frame'] + hi - lo > int(stream['nb_read_frames']):
            raise ValueError('Film selection must cover its exact source range at 1280x720/24fps')
        covered = 0
        for row in rows:
            result = []
            for s in row['spans']:
                a, z = s['original_frames']; x, y = max(a, lo), min(z, hi)
                if x >= y:
                    result.append(s); continue
                for c, d, replacement in ((a, x, False), (x, y, True), (y, z, False)):
                    if c == d:
                        continue
                    part = copy.deepcopy(s)
                    part.update(original_frames=[c, d], output_frames=[s['output_frames'][0] + c - a, s['output_frames'][0] + d - a], frames=d - c)
                    if replacement:
                        part.update(kind='video', source=p['source'], source_start_frame=p['source_start_frame'] + c - lo, film_selection_id=p['id'])
                        covered += d - c
                    else:
                        part['source_start_frame'] += c - a
                    result.append(part)
            row['spans'] = result
        if covered != hi - lo:
            raise ValueError('Film selection not completely mapped')
    return bound(manifest)


def render(scope, film_selects, name):
    revision = read(REVISION)
    for key in ('master', 'timemap', 'transcript', 'sources', 'pickup', 'pickup_words', 'pickup_review', 'original_master', 'original_shot_plan', 'base_assembly_manifest', 'look_still'):
        verify_bound(revision[key])
    lock_path = B / 'direction/r3-owner-revisions/OWNER-LOCK.json'
    owner_lock = None
    if lock_path.exists():
        lock = read(lock_path)
        if lock.get('status') != 'locked_by_owner':
            raise ValueError('Unexpected scoped owner-lock state')
        for key in ('source', 'brand_preview', 'hospitality_preview', 'selected_paragraph_audio', 'selected_script', 'time_map', 'master_carrier'):
            verify_bound(lock[key])
        if lock['master_carrier'] != revision['master'] or lock['time_map'] != revision['timemap']:
            raise ValueError('Revision differs from the owner-locked carrier or timing map')
        owner_lock = bound(lock_path)
    rows = read(verify_bound(revision['sources']))
    film_binding = apply_films(rows, film_selects) if film_selects else None
    if scope == 'full' and film_binding is None:
        raise ValueError('Full r3 render held until new film selections are supplied')
    pickup = next(r for r in rows if r['id'] == 'seg044')
    start, end = {'full': (0, revision['total_frames']), 'brand': (1306, 1602),
                  'hospitality': (pickup['output_frames'][0] - 120, pickup['output_frames'][1] + 120)}[scope]
    spans = []
    for row in rows:
        for s in row['spans']:
            a, z = s['output_frames']; x, y = max(a, start), min(z, end)
            if x < y:
                piece = copy.deepcopy(s)
                piece.update(source_start_frame=s['source_start_frame'] + x - a,
                             output_frames=[x - start, y - start], frames=y - x, segment_id=row['id'])
                spans.append(piece)
    if sum(s['frames'] for s in spans) != end - start:
        raise ValueError('Review span gap or overlap')
    # Keep adjacent selections from one source in one decoder branch. A lone
    # frame between concat branches otherwise has zero inferred branch duration.
    # This matters for the one retained sting frame after the brand excision.
    groups = []
    for s in spans:
        source_range = [s['source_start_frame'], s['source_start_frame'] + s['frames']]
        if (groups and groups[-1]['source'] == s['source'] and groups[-1]['kind'] == s['kind']
                and source_range[0] >= groups[-1]['ranges'][-1][1]):
            groups[-1]['ranges'].append(source_range)
            groups[-1]['frames'] += s['frames']
        else:
            groups.append({'source': s['source'], 'kind': s['kind'], 'ranges': [source_range], 'frames': s['frames']})
    if any(g['frames'] < 2 for g in groups):
        raise ValueError('An isolated one-frame concat branch needs an explicit source-selection treatment')
    sources, kinds = {}, {}
    for s in groups:
        path = verify_bound(s['source'])
        sources[str(path)] = s['source']; kinds[str(path)] = s['kind']
    paths = list(sources)
    graph, inputs, counts = [], [], {}
    for i, p in enumerate(paths):
        uses = sum(s['source']['path'] == rel(p) for s in groups)
        if kinds[p] == 'still':
            inputs += ['-loop', '1', '-framerate', '24', '-i', p]
        else:
            inputs += ['-threads', '1', '-i', p]
        if uses > 1:
            graph.append(f'[{i}:v]split={uses}' + ''.join(f'[src{i}_{j}]' for j in range(uses)))
    label_path = review_label() if any(s['kind'] == 'still' for s in groups) else None
    label_index = len(paths)
    if label_path:
        inputs += ['-loop', '1', '-framerate', '24', '-i', str(label_path)]
    for j, s in enumerate(groups):
        i = paths.index(str(R / s['source']['path'])); k = counts.get(i, 0); counts[i] = k + 1
        multiple = sum(t['source']['path'] == s['source']['path'] for t in groups) > 1
        source = f'[src{i}_{k}]' if multiple else f'[{i}:v]'
        a, z = s['ranges'][0][0], s['ranges'][-1][1]
        if z - a == s['frames']:
            selection = f'trim=start_frame={a}:end_frame={z}'
        else:
            selection = "select='" + '+'.join(f'between(n,{x},{y-1})' for x, y in s['ranges']) + "'"
            # The source remains finite, but stop decoding after the last range.
            selection = f'trim=end_frame={z},' + selection
        sizing = 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720' if s['kind'] == 'still' else 'scale=1280:720'
        filters = f'{selection},setpts=N/(24*TB),{sizing},setsar=1,format=yuv420p'
        if s['kind'] == 'still':
            graph.append(source + filters + f'[still{j}]')
            graph.append(f'[still{j}][{label_index}:v]overlay=shortest=1:eof_action=repeat[v{j}]')
        else:
            graph.append(source + filters + f'[v{j}]')
    graph.append(''.join(f'[v{j}]' for j in range(len(groups))) + f'concat=n={len(groups)}:v=1:a=0,fps=24[vout]')
    inputs += ['-threads', '1', '-i', str(verify_bound(revision['master']))]
    audio_index = len(paths) + (1 if label_path else 0)
    graph.append(f'[{audio_index}:a]atrim=start_sample={start * SPF}:end_sample={end * SPF},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0,apad=whole_len={(end-start)*SPF},atrim=end_sample={(end-start)*SPF}[aout]')
    stem = name or f'ep009-r3-{scope}-review'
    if not re.fullmatch(r'[A-Za-z0-9_-]+', stem):
        raise ValueError('Use a simple new output stem')
    qa = A / 'qa/r3'; qa.mkdir(exist_ok=True)
    output, manifest, graphpath, log = qa / (stem + '.mp4'), D / (stem + '-BUILD.json'), D / (stem + '-graph.txt'), D / (stem + '-encode.log')
    for p in (output, manifest, graphpath, log):
        if p.exists():
            raise FileExistsError(f'Preserve existing artifact: {p}')
    with graphpath.open('x') as f:
        f.write(';\n'.join(graph) + '\n')
    cmd = ['ffmpeg', '-n', '-v', 'error', '-stats', '-filter_complex_threads', '2', *inputs,
           '-/filter_complex', str(graphpath), '-map', '[vout]', '-map', '[aout]', '-c:v', 'libx264',
           '-preset', 'medium', '-crf', '16', '-threads', '2', '-pix_fmt', 'yuv420p', '-r', '24',
           '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(output)]
    info = {'record_type': 'ep009_r3_review_build', 'status': 'rendering', 'scope': scope,
            'owner_accepted': False, 'delivery_master': False, 'revision': bound(REVISION),
            'master': revision['master'], 'owner_scoped_lock': owner_lock, 'film_selections': film_binding, 'output_master_frames': [start, end],
            'total_frames': end - start, 'source_spans': spans, 'render_groups': groups, 'all_75_rows': rows,
            'sources': list(sources.values()), 'review_label': bound(label_path) if label_path else None, 'output': rel(output), 'command': cmd,
            'graph': bound(graphpath), 'encode_log': rel(log), 'limitations': revision['limitations']}
    write(manifest, info)
    with log.open('x') as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    info['status'] = 'encoded_unverified_review_only' if result.returncode == 0 else 'failed_partial_preserved'
    info['encode_exit_code'] = result.returncode
    if result.returncode == 0:
        info['output_sha256'] = sha(output)
    manifest.write_text(json.dumps(info, indent=2) + '\n')
    if result.returncode == 0:
        page_command = [sys.executable, str(A / '_tools/review_r3.py')]
        if scope == 'full':
            page_command += ['--build', str(manifest)]
        subprocess.run(page_command, check=True)
    print(json.dumps({'status': info['status'], 'manifest': str(manifest), 'output': str(output)}, indent=2))
    return result.returncode


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('--pickup-audio', required=True, type=Path)
    prep.add_argument('--pickup-words', required=True, type=Path)
    prep.add_argument('--pickup-review', required=True, type=Path)
    build = sub.add_parser('render')
    build.add_argument('--scope', required=True, choices=['brand', 'hospitality', 'full'])
    build.add_argument('--film-selects', type=Path)
    build.add_argument('--name')
    a = p.parse_args()
    if a.command == 'prepare':
        prepare(a.pickup_audio.resolve(), a.pickup_words.resolve(), a.pickup_review.resolve())
        return 0
    return render(a.scope, a.film_selects, a.name)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        raise SystemExit(2)
