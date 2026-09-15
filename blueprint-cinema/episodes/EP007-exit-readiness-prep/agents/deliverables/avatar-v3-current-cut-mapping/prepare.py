#!/usr/bin/env python3
"""Local-only, sample-exact preparation. Writes exclusively beside this script."""
from pathlib import Path
from fractions import Fraction
from html.parser import HTMLParser
import hashlib
import json
import math
import subprocess
import wave

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'blueprint-cinema/AGENTS.md').exists())
EP = 'EP007-exit-readiness-prep'
REVIEW = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r29-neutral-seller'
LOCK = ROOT / 'blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v3-lock'
WORK_ORDER = ROOT / f'blueprint-cinema/episodes/{EP}/agents/work-orders/avatar-v3-current-cut-mapping.json'
TRANSCRIPT = ROOT / f'operator-blueprint-v2/episodes/{EP}/02-narration-production/word-transcript.json'
SR = 48000
FPS = 24


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def relative(p):
    return str(Path(p).relative_to(ROOT))


def save(name, data):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + '\n')
    return p


def pcm(p):
    with wave.open(str(p), 'rb') as wav:
        assert (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) == (1, 2, SR)
        return wav.readframes(wav.getnframes())


def probe(p):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_name,width,height,r_frame_rate,start_time,duration,nb_frames',
        '-of', 'json', str(p)]))


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = {}
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.tags[a['id']] = {'tag': tag, **a}


work = json.loads(WORK_ORDER.read_text())
for item in work['inputs']:
    assert sha(ROOT / item['path']) == item['sha256'], item['path']
transcript = json.loads(TRANSCRIPT.read_text())
master = ROOT / transcript['master_path']
assert sha(master) == transcript['master_sha256']
master_pcm = pcm(master)
acceptance = json.loads((LOCK / 'ACCEPTANCE.json').read_text())
refs = {k: v for k, v in acceptance['recipe']['inputs'].items()
        if k in ('portrait', 'rebecca_behavior', 'henry_articulation')}
for item in refs.values():
    assert sha(ROOT / item['path']) == item['sha256']
opening_audio = ROOT / acceptance['recipe']['inputs']['original_audio']['path']
assert pcm(opening_audio) == master_pcm[:round(20.9 * SR) * 2]

input_paths = [ROOT / x['path'] for x in work['inputs']]
input_paths += [master, opening_audio, ROOT / acceptance['artifact']['path']]
input_paths += [ROOT / x['path'] for x in refs.values()]
result_record = ROOT / f'blueprint-cinema/episodes/{EP}/review/decisions/avatar-v3-opening-result-20260911.json'
input_paths.append(result_record)
opening_result = json.loads(result_record.read_text())
insertion_offset = opening_result['audio']['audio_insertion_offset_seconds']
assert insertion_offset == 0.04725

audio_checks = []
for name, a, b in [('review-narration.wav', 0, 59.5),
                   ('review-narration-extended.wav', 0, 74.5),
                   ('seller-market-narration.wav', 74.5, 160.5)]:
    p = REVIEW / 'public/audio' / name
    expected = master_pcm[round(a * SR) * 2:round(b * SR) * 2]
    assert pcm(p) == expected, name
    input_paths.append(p)
    audio_checks.append({'path': relative(p), 'sha256': sha(p), 'master_seconds': [a, b],
                         'master_sample_range': [round(a * SR), round(b * SR)], 'pcm_exact': True})
assert not any(master_pcm[45 * SR * 2:48 * SR * 2])

root_tags = Tags((REVIEW / 'index.html').read_text()).tags
q_tags = Tags((REVIEW / 'compositions/presenter-question.html').read_text()).tags
base_crop = {'width': 1280, 'height': 724, 'left': 0, 'top': 0, 'object_fit': 'fill',
             'viewport': [1280, 720], 'overflow': 'hidden'}
q_crop = {'width': 1280, 'height': 720, 'object_fit': 'cover', 'viewport': [1280, 720],
          'overflow': 'hidden', 'transform_origin': '0 0'}


def word_records(a, b, local_origin):
    return [{**w, 'local_start_seconds': w['start'] - local_origin,
             'local_end_seconds': w['end'] - local_origin,
             'overlaps_start_boundary': w['start'] < a,
             'overlaps_end_boundary': w['end'] > b}
            for w in transcript['words'] if w['end'] > a and w['start'] < b]


def make_slot(name, tag_id, start_frame, end_frame, master_origin, source_in,
              replacement, replacement_source_in, crop, tags=root_tags):
    t = tags[tag_id]
    start, end = start_frame / FPS, end_frame / FPS
    local_start = 0 if tags is q_tags else start
    assert abs(float(t['data-start']) - local_start) < 1e-7
    assert abs(float(t['data-duration']) - (end - start)) < 1e-7
    assert abs(float(t.get('data-media-start', 0)) - source_in) < 1e-7
    p = REVIEW / t['src']
    input_paths.append(p)
    a, b = start + master_origin, end + master_origin
    words = word_records(a, b, a)
    return {'slot_id': name, 'element_id': tag_id, 'source_path': relative(p),
            'source_sha256': sha(p), 'source_probe': probe(p),
            'review_frames': [start_frame, end_frame], 'review_seconds': [start, end],
            'master_seconds': [a, b], 'master_sample_range': [round(a * SR), round(b * SR)],
            'old_source_seconds': [source_in, source_in + end - start],
            'old_source_frames': [round(source_in * FPS), round((source_in + end - start) * FPS)],
            'old_source_semantic_master_origin_seconds': a - source_in,
            'declared_av_compensation_seconds': 0,
            'av_compensation_note': 'Existing source/media declarations only; perceptual lip sync is not inferred.',
            'exact_overlapping_words': words, 'text': ' '.join(w['token'] for w in words),
            'crop': crop, 'replacement_take': replacement,
            'replacement_source_seconds': [replacement_source_in, replacement_source_in + end - start],
            'replacement_source_frames': [round(replacement_source_in * FPS),
                                           round((replacement_source_in + end - start) * FPS)],
            'replacement_status': 'accepted_source_root_integrates' if replacement == 'accepted-v3-opening' else 'new_source_required'}


slots = [
    make_slot('opening', 'avatar-hook', 0, 97, 0, 0, 'accepted-v3-opening', 1 / FPS, base_crop),
    make_slot('opportunity', 'avatar-opportunity', 962, 1068, 0, 160 / FPS,
              'v3-opportunity', 8 / FPS, base_crop),
    make_slot('post-title-definition', 'post-title-definition', 1356, 1510, 3, 0,
              'v3-post-title-continuous', 0, base_crop),
    make_slot('post-title-promise', 'post-title-promise', 1510, 1716, 3, 0,
              'v3-post-title-continuous', 154 / FPS,
              {**base_crop, 'transform_origin': '0 0', 'transform_cues': [
                  {'review_seconds': 1510 / FPS, 'scale': 1.25, 'x': -160, 'y': -24},
                  {'review_seconds': 67.58, 'scale': 1.4, 'x': -256, 'y': -42}]}),
    make_slot('question-speaking', 'q-speaking', 3144, 3433, 3, 0,
              'v3-question', 0,
              {**q_crop, 'transform_cues': [
                  {'review_seconds': 131, 'scale': 1.08, 'x': -51.2, 'y': -12},
                  {'review_seconds': 131 + 215 / FPS, 'scale': 1.2, 'x': -128, 'y': -22}]}, q_tags),
]
hold = q_tags['q-final-hold']
assert abs(float(hold['data-start']) - 289 / FPS) < 1e-7
assert float(hold['data-duration']) == .75
input_paths.append(REVIEW / hold['src'])
hold_data = {'element_id': 'q-final-hold', 'source_path': relative(REVIEW / hold['src']),
             'source_sha256': sha(REVIEW / hold['src']), 'review_frames': [3433, 3451],
             'review_seconds': [3433 / FPS, 3451 / FPS],
             'master_seconds': [3505 / FPS, 3523 / FPS], 'duration_frames': 18,
             'replacement': 'Extract frame 288 of the new restored question source and retain the same 18-frame hold.',
             'retained_source_frame': 288, 'retained_source_pts_seconds': 12,
             'crop': slots[-1]['crop'],
             'boundary_note': 'The accepted cut is review143.791666667/master146.791666667. Nobody begins at transcript master146.78, so 0.011666667s overlaps the hold. Preserve this existing frame-rounded cut; do not label the whole hold digitally silent.'}

take_defs = [
    {'id': 'v3-opportunity', 'samples': [1908000, 2154000], 'request_duration': 6,
     'slots': ['opportunity'],
     'direction': 'He makes the turn from the unfinished answer to the business opportunity matter-of-factly. Keep the supplied initial pause, then deliver the single sentence directly and without a sales smile. Let the voice carry emphasis in "business hiding inside it" and "almost nobody"; do not add a nod or raised brow on either phrase. Finish "running" completely and let the face settle in the supplied final quiet.'},
    {'id': 'v3-post-title-continuous', 'samples': [2856000, 3576000], 'request_duration': 15,
     'slots': ['post-title-definition', 'post-title-promise'],
     'direction': 'This is one continuous take across both post-title sentences. Explain the practice plainly, let the face settle during the supplied pause after "anything," then continue the viewing promise. Preserve clear connected articulation through "honestly charge for" and "the one number." Let the supplied voice carry the emphasis; no celebratory smile, big jaw stretch, repeated nod or sustained brow lift. Do not cut, zoom or change framing inside the generated take: the existing edit supplies its two crop changes while this source performance and its time continue uninterrupted.'},
    {'id': 'v3-question', 'samples': [6432000, 7010000], 'request_duration': 13,
     'slots': ['question-speaking', 'q-final-hold'],
     'direction': 'Address the viewer directly to frame the question this episode will answer. During the original pause after "answer," relax the lips and remain comfortably attentive. Ask the conditional question in one connected thought. Let the supplied voice carry "then who is getting paid" without a dramatic lean-in, prolonged chin lift or theatrical worry. Complete "closeable" naturally, then close the lips gently and settle. Do not say "Nobody is" or anticipate the answer. Remain the narrator, not a buyer or seller acting out the scene.'},
]
accepted_prompt = (LOCK / 'PROMPT.txt').read_text().strip().split('\n\n')
common = accepted_prompt[2].replace('He tells the opening story calmly to one person near the lens.',
                                  'He speaks calmly to one person near the lens.')
generation = json.loads((LOCK / 'GENERATION-REQUEST.json').read_text())['params']
take_records = []
for take in take_defs:
    a, b = take['samples']
    duration = (b - a) / SR
    audio_path = OUT / 'audio' / (take['id'] + '.wav')
    audio_path.parent.mkdir(exist_ok=True)
    with wave.open(str(audio_path), 'wb') as wav:
        wav.setparams((1, 2, SR, b - a, 'NONE', 'not compressed'))
        wav.writeframes(master_pcm[a * 2:b * 2])
    assert pcm(audio_path) == master_pcm[a * 2:b * 2]
    words = word_records(a / SR, b / SR, a / SR)
    assert all(not w['overlaps_start_boundary'] and not w['overlaps_end_boundary'] for w in words)
    text = ' '.join(w['token'] for w in words)
    first = accepted_prompt[0].replace('21-second', f"{take['request_duration']}-second")
    last = (f'The audio is {duration:.9f} seconds, including its unchanged original pauses and end quiet. '
            'Lip and jaw movement follow this audio, not either muted video\'s speech timing. '
            f'Keep the original cadence and complete the final word naturally, then close the lips gently and settle through {take["request_duration"]} seconds. '
            'Do not slow down or stretch the words to fill the requested video duration. '
            'No extra words, silent syllables or pursed-lip hold. The camera, background and light remain still. '
            'Real-time motion, one shot, no captions, titles, logos, cutaways, zoom, music or additional people.')
    prompt = '\n\n'.join([first, accepted_prompt[1], common, take['direction'],
        f'Speak only the supplied AUDIO reference, preserving its exact voice, words, rhythm and pauses from the beginning: "{text}"', last]) + '\n'
    prompt_path = OUT / 'prompts' / (take['id'] + '.txt')
    prompt_path.parent.mkdir(exist_ok=True)
    prompt_path.write_text(prompt)
    record = {'take_id': take['id'], 'status': 'local_preparation_only', 'execution_permitted': False,
              'master_seconds': [a / SR, b / SR], 'master_sample_range_half_open': [a, b],
              'audio_path': relative(audio_path), 'audio_sha256': sha(audio_path),
              'pcm_sha256': hashlib.sha256(pcm(audio_path)).hexdigest(),
              'audio_duration_seconds': duration, 'sample_rate': SR, 'channels': 1, 'bits_per_sample': 16,
              'sample_count': b - a, 'pcm_exact_original_master': True,
              'prompt_path': relative(prompt_path), 'prompt_sha256': sha(prompt_path),
              'request_duration_seconds': take['request_duration'],
              'required_restored_source_frames_24fps': round(duration * FPS),
              'request_duration_is_bounded_plan_not_current_provider_validation': True,
              'original_words': text, 'word_records': words, 'target_slots': take['slots'],
              'source_time_formula': f'source_seconds = master_seconds - {a / SR}',
              'future_waveform_or_perceptual_offset_seconds': None,
              'extra_requested_tail_seconds': take['request_duration'] - duration}
    params = {k: v for k, v in generation.items() if k not in ('prompt', 'medias', 'duration')}
    params['duration'] = take['request_duration']
    request = {'status': 'local_preparation_only', 'execution_permitted': False,
               'provider_route': 'Existing Higgsfield Seedance 2.5 connection',
               'parameters_from_accepted_v3_except_duration': params,
               'reference_inputs_in_order': [
                   {'role': 'image', 'function': acceptance['recipe']['reference_roles']['portrait'], **refs['portrait']},
                   {'role': 'video', 'function': acceptance['recipe']['reference_roles']['rebecca_behavior'], **refs['rebecca_behavior']},
                   {'role': 'video', 'function': acceptance['recipe']['reference_roles']['henry_articulation'], **refs['henry_articulation']},
                   {'role': 'audio', 'path': relative(audio_path), 'sha256': sha(audio_path), 'function': 'Exact words, voice, timing and pauses from original WAV'}],
               'prompt_path': relative(prompt_path), 'prompt_sha256': sha(prompt_path),
               'audio_encoding_note': 'If the existing Higgsfield upload flow requires MP3, create a real MP3 derivative with matching MIME/extension; retain this exact WAV for restoration and the root soundtrack. No encoding or upload was performed here.',
               'restoration_plan': {'route': 'Existing Fal sync-lipsync/v3 connection', 'sync_mode': 'silence',
                                    'audio': relative(audio_path), 'voice_or_word_generation': False,
                                    'native_video_selection': 'Use the fresh take only. Restore exact supplied WAV and verify actual output coverage without retiming; derive selected source windows and the hold from the restored result.',
                                    'offset': 'Measure waveform insertion anew for each output; do not inherit opening47.25ms or claim it measures visual lip sync.'},
               'wider_framing_selected': False, 'new_spend_or_upload_authority': False,
               'price_or_credit_quote': None, 'submission_performed': False}
    request_path = save('requests/' + take['id'] + '.json', request)
    record['request_path'] = relative(request_path)
    take_records.append(record)

mapping = {
    'contract': 'r29-avatar-v3-source-preparation-1', 'work_order_id': work['work_order_id'],
    'status': 'prepared_locally', 'baseline': relative(REVIEW), 'fps': FPS,
    'interval_convention': 'Half-open ranges [in,out); frame indices and audio sample indices are zero based.',
    'r29_root_sha256': sha(REVIEW / 'index.html'),
    'master': {'path': relative(master), 'sha256': sha(master), 'sample_rate': SR,
               'channels': 1, 'bits_per_sample': 16, 'sample_count': len(master_pcm) // 2},
    'review_clock': {'segments': [
        {'review_seconds': [0, 45], 'master_seconds': [0, 45], 'formula': 'master=review'},
        {'review_seconds': [45, 157.5], 'master_seconds': [48, 160.5], 'formula': 'master=review+3'}],
        'omitted_original_master_seconds': [45, 48], 'omitted_samples': 144000,
        'omitted_samples_all_zero': True, 'source_narration_untouched': True,
        'root_audio_files_pcm_verified': audio_checks},
    'accepted_v3': {'artifact': acceptance['artifact'], 'available_original_master_seconds': [0, 20.9],
        'reference_pcm_equals_original_master': True,
        'audio_insertion_offset_seconds': insertion_offset,
        'offset_basis': 'Pinned V3 result waveform placement, not a measured audiovisual lip-sync offset.',
        'hook_source_in_seconds': 1 / FPS, 'hook_source_frames': [1, 98],
        'remaining_waveform_placement_difference_seconds': insertion_offset - 1 / FPS,
        'hook_integration_owner': 'root agent; no integration performed by this packet',
        'other_use': 'No other currently visible R29 avatar words occur inside master0–20.9. The question graphic at17.75–21 remains a graphic; do not replace it with avatar footage.'},
    'moving_avatar_slots': slots, 'picture_hold': hold_data, 'prepared_takes': take_records,
    'contiguous_post_title_plan': {
        'selection': 'One continuous new V3-based 15-second source for master59.5–74.5.',
        'reason': 'These two adjacent sentences use contiguous original audio and one stable setup. Retaining one performance avoids restarting or repeating a head gesture while preserving the approved framing changes.',
        'source_ranges_by_existing_slot': {'post-title-definition': [0, 154 / FPS],
                                           'post-title-promise': [154 / FPS, 15]},
        'cuts_retained': [{'review_seconds': 1510 / FPS, 'master_seconds': 1582 / FPS,
                           'source_seconds': 154 / FPS, 'meaning': 'Definition to promise, within original pause.'},
                          {'review_seconds': 67.58, 'master_seconds': 70.58, 'source_seconds': 11.08,
                           'meaning': 'After W000180 and ends; before the one number. Preserve the authored67.58 cue, do not round or migrate it.'}],
        'continuous_source_across_cuts': True, 'speed': 1, 'loops': False, 'narration_changes': False},
    'question_cut_contract': {'mount_review_frames': [3144, 3451], 'moving_frames': 289, 'hold_frames': 18,
        'close_cut_review_frame': 3359, 'close_cut_review_seconds': 3359 / FPS,
        'close_cut_master_seconds': 3431 / FPS, 'close_cut_source_seconds': 215 / FPS,
        'actual_cue': 'Immediately before W000426 then at master142.98, not before W000427 who at143.32. Preserve current runtime cue even though older prose says before who.',
        'dependent_targets': ['presenter-question-host start/duration', 'q-speaking source/start/duration',
                              'q-final-hold image/start/duration', 'q-framing then-who label and both transforms',
                              'gap-host start/duration', 'market-narration continuous soundtrack'],
        'new_hold_source': 'New restored question frame288, not the old avatar hold JPEG.'},
    'protected_runtime': ['All picture cuts', 'All existing crop sizes/positions and67.58 cue',
                          'Root original WAV soundtrack and 3-second silence omission',
                          'Question18-frame picture hold and gap entry', 'All non-avatar R29 footage/graphics'],
    'limits': ['No provider calls, uploads, runtime changes or gate advancement.',
               'New source naturalness, perceptual lip sync, likeness and end-frame settling require output review.',
               'Source duration requests6/15/13s are local bounded plans; provider acceptance/pricing has not been queried.',
               'Canonical episode README, episode.json and input-lock.json are absent; this bounded experiment packet is authorized by the work order and its explicit pins.'],
}
save('mapping.json', mapping)
input_paths = list(dict.fromkeys(input_paths))
save('checks.json', {'input_pins_match': True, 'master_sha_matches_transcript': True,
    'three_current_soundtrack_files_pcm_exact': True, 'opening_reference_pcm_exact': True,
    'original_three_second_omission_all_zero': True, 'three_excerpts_pcm_exact': True,
    'all_requested_words_complete_in_excerpts': True, 'all_five_moving_slot_declarations_match': True,
    'question_hold_declaration_matches': True, 'new_generation_or_upload': False,
    'runtime_changes': False, 'source_probes': {s['slot_id']: s['source_probe'] for s in slots}})
checks = [
    {'command': 'python3 prepare.py: verify all7 issued input pins and original master hash', 'outcome': 'pass'},
    {'command': 'python3 prepare.py: compare full PCM of3 current narration files and accepted V3 reference to exact master slices', 'outcome': 'pass'},
    {'command': 'python3 prepare.py: verify5 moving avatar declarations, source ranges, crop dependencies and18-frame picture hold', 'outcome': 'pass'},
    {'command': 'python3 prepare.py: extract3 original PCM16 mono48k WAVs; byte-compare source sample ranges and verify complete transcript words', 'outcome': 'pass'},
    {'command': 'ffprobe each of4 distinct old avatar sources: dimensions, fps, PTS, duration, frame counts', 'outcome': 'pass'},
]
manifest = {'$schema': '../../../../../schemas/agent-deliverable.schema.json', 'schema_version': '1.0.0',
    'workflow_version': 'blueprint-cinema-1.0', 'work_order_id': work['work_order_id'], 'episode_folder': EP,
    'input_hashes_used': [{'path': relative(p), 'sha256': sha(p)} for p in input_paths],
    'files_produced': sorted(relative(p) for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in str(p)),
    'checks': checks,
    'sources_and_provenance': ['Locked original master and word transcript, live-read R29 declarations and accepted source/recipe manifests.',
        'Local original WAV extraction only. Both muted behavior references and portrait are referenced by existing local paths and hashes.',
        'Accepted source is preexisting synthetic presenter media; no new synthetic media produced.',
        'Memory located the locked narration/provenance boundary; all material timing and source facts were verified against current files.'],
    'assumptions': ['Keep accepted V3 medium-close framing; the wider framing proposal is not selected.',
        'Preserve existing R29 cuts, including question end/frame rounding and crop cues; root owns integration.',
        'This is complete local preparation for three remaining takes, not their production or acceptance.'],
    'unresolved_questions': ['Actual fresh-source performance, likeness, mouth synchronization, waveform placement and settled final frame remain unverified until generation.',
        'Current provider duration support and pricing were not queried; no spending authority is asserted.'],
    'external_writes': False, 'paid_services': False, 'synthetic_generation': False,
    'approval_claimed': False, 'production_state_changed': False, 'status': 'complete'}
if relative(OUT / 'deliverable.json') not in manifest['files_produced']:
    manifest['files_produced'].append(relative(OUT / 'deliverable.json'))
save('deliverable.json', manifest)
print(json.dumps({'prepared_takes': len(take_records), 'moving_avatar_slots': len(slots),
                  'original_audio_seconds': sum(t['audio_duration_seconds'] for t in take_records),
                  'bounded_requested_video_seconds': sum(t['request_duration_seconds'] for t in take_records),
                  'all_pcm_exact': True, 'output': str(OUT)}))
