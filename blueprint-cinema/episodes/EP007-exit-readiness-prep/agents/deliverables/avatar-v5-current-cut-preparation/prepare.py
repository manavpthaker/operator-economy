#!/usr/bin/env python3
"""Prepare only this owned local V5 packet; no provider or runtime operations."""
from pathlib import Path
from html.parser import HTMLParser
import copy
import hashlib
import json
import re
import shutil
import wave

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'blueprint-cinema/AGENTS.md').exists())
EP = 'EP007-exit-readiness-prep'
WORK = ROOT / f'blueprint-cinema/episodes/{EP}/agents/work-orders/avatar-v5-current-cut-preparation.json'
PRIOR = OUT.parent / 'avatar-v3-current-cut-mapping'
LOCK = ROOT / 'blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v5-gestures'
R30 = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r30-avatar-v3-hook'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).relative_to(ROOT))
def save(name, obj):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + '\n')
    return p
def pcm(p):
    with wave.open(str(p), 'rb') as w:
        assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, 48000)
        return w.readframes(w.getnframes())

work = json.loads(WORK.read_text())
inputs = list(work['inputs'])
for x in inputs: assert sha(ROOT / x['path']) == x['sha256'], x['path']
v5 = json.loads((LOCK / 'ACCEPTANCE.json').read_text())
assert v5['status'] == 'owner_accepted_locked'
for x in [*v5['recipe']['inputs'].values(), v5['artifact'], v5['corresponding_restored_source'],
          v5['owner_feedback'], v5['recipe']['performance_baseline']]:
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
    inputs.append({'path': x['path'], 'sha256': x['sha256']})
prior = json.loads((PRIOR / 'mapping.json').read_text())
master = ROOT / prior['master']['path']
assert sha(master) == prior['master']['sha256']
inputs.append({'path': rel(master), 'sha256': sha(master)})
master_pcm = pcm(master)
transcript = json.loads((ROOT / next(x['path'] for x in work['inputs'] if x['path'].endswith('word-transcript.json'))).read_text())
params = json.loads((LOCK / 'SUBMISSION-INTENT.json').read_text())['params']
assert params['resolution'] == '1080p'
sync = json.loads((LOCK / 'SYNC-REQUEST.json').read_text())
assert sync['model'] == 'fal-ai/sync-lipsync/v3' and sync['input']['sync_mode'] == 'silence'
base = (LOCK / 'PROMPT.txt').read_text().strip().split('\n\n')

class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.tags = {}; self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.tags[a['id']] = a
root_tags = Tags((R30 / 'index.html').read_text()).tags
q_tags = Tags((R30 / 'compositions/presenter-question.html').read_text()).tags
for s in prior['moving_avatar_slots'][1:]:
    a = (q_tags if s['slot_id'] == 'question-speaking' else root_tags)[s['element_id']]
    start = 0 if s['slot_id'] == 'question-speaking' else s['review_seconds'][0]
    assert abs(float(a['data-start']) - start) < 1e-7
    assert abs(float(a['data-duration']) - (s['review_seconds'][1] - s['review_seconds'][0])) < 1e-7
    assert abs(float(a['data-media-start']) - s['old_source_seconds'][0]) < 1e-7
assert "67.58" in (R30 / 'index.html').read_text()
assert abs(float(q_tags['q-final-hold']['data-start']) - 289 / 24) < 1e-7
assert float(q_tags['q-final-hold']['data-duration']) == .75

directions = {
 'v5-opportunity': {
    'performance': 'This short return turns the unfinished answer into a possible business opportunity. Keep it matter-of-fact, without a sales smile. Begin from the resting pose and allow compact conversational hand activity to support the whole thought, then settle as it finishes. A loose opening or small outward hand movement can make room for the idea if it fits his delivery; it is an option, not a required gesture. Do not mime hiding, point to imaginary people or hit every phrase with a beat. Preserve the entire last word "running" and the original ending quiet.',
    'viewer_job': 'Connect the witnessed pause to a business opportunity while retaining a direct, grounded presenter return.',
    'framing': [{'review_seconds': [962/24, 44.5], 'source_seconds': [8/24, 4.75], 'framing': 'wide with complete hands', 'reason': 'The brief single-thought return benefits from the accepted hand presence; no new crop cue is needed.'}]},
 'v5-post-title-continuous': {
    'performance': 'This is one continuous explanation across both post-title sentences. In the practical description of one person working with owners before a sale, let the hands participate with restrained, uneven conversational movement that follows the whole explanation. Do not count fingers for "one person," mime a licence or act out signing papers. Allow the existing pause after "anything" to breathe and the hands to settle naturally. As the viewing promise begins, hand activity may become a little more open toward the listener if the thought calls for it, then quieter while "the one number" lands. Do not raise one finger at "one number" or repeat the opportunity take\'s gesture sequence. Preserve clear connected articulation through "honestly charge for" and "the one number." Do not cut or zoom inside the source: all framing changes happen later in the edit while the same performance and source time continue.',
    'viewer_job': 'Move from the concrete practice to what the viewer will learn, then concentrate attention on the decisive number.',
    'framing': [
      {'review_seconds': [56.5, 1510/24], 'source_seconds': [0, 154/24], 'framing': 'wide with complete hands', 'reason': 'Establish the practical explanation in the accepted seated framing.'},
      {'review_seconds': [1510/24, 67.58], 'source_seconds': [154/24, 11.08], 'framing': 'medium', 'reason': 'The existing definition-to-promise cut shifts attention toward direct address.'},
      {'review_seconds': [67.58, 71.5], 'source_seconds': [11.08, 15], 'framing': 'close', 'reason': 'The existing cut immediately after and focuses the face before the one number; preserve source continuity.'}]},
 'v5-question': {
    'performance': 'Address the listener to frame the question the episode will answer. Hands can participate in the first explanation and the conditional clause with compact, irregular movement; avoid pointing to imaginary professionals around the room. Let the original pause after "answer" remain unhurried, with hands and face comfortably settling as appropriate. On the turn "then who is getting paid," leave the voice and face room to carry the question. A small change of hand orientation is permissible if natural, but do not prescribe an obligatory palm-up question gesture or repeat another take\'s choreography. No accusation, theatrical worry, dramatic lean-in or prolonged chin lift. Finish "closeable" completely, close the lips gently and return toward a credible quiet resting pose. Do not say "Nobody is" or anticipate the answer.',
    'viewer_job': 'Frame the unassigned paid work as a direct question, then preserve the unanswered pause before the next scene.',
    'framing': [
      {'review_seconds': [131, 3359/24], 'source_seconds': [0, 215/24], 'framing': 'wide with complete hands', 'reason': 'The opening and conditional explanation retain the accepted seated hand performance.'},
      {'review_seconds': [3359/24, 3451/24], 'source_seconds': [215/24, 289/24], 'framing': 'medium-close', 'reason': 'The existing cut before then concentrates attention on the question; hold the same crop through the final18-frame freeze.', 'picture_hold_last_18_frames': True}]},
}
articulation = base[2].split(' His upper body')[0].replace('He tells the opening story calmly', 'He speaks calmly')
hands = ('His upper body is comfortably settled and his arms are free to move. Both forearms and complete hands remain visible in the fixed wide source. '
         'Use the accepted V5 hand activity as a natural baseline, adapting gesture choice, size and timing to this passage, with varied movement and returns to rest. '
         'There is no required gesture count, hand side or repeated choreography across takes. Hands move over whole thoughts rather than tapping every stressed word. '
         'Keep gestures between tabletop and lower chest, inside the source frame. Elbows and wrists bend naturally; fingers remain loosely curved, distinct and consistent. '
         'Maintain credible contact when hands return to the table. No rapid waving, rhythmic pumping, finger counting, steepling or large symmetrical presentation poses. '
         'A brief spontaneous eye movement or look-away is permissible as in accepted V5, with a natural return near the lens. Do not schedule glances or copy either interview\'s sustained off-screen gaze. '
         'Preserve breathing, ordinary blinks, subtle asymmetry and comfortable stillness rather than freezing him.')
take_records = []
for old in prior['prepared_takes']:
    tid = old['take_id'].replace('v3-', 'v5-')
    src = ROOT / old['audio_path']
    assert sha(src) == old['audio_sha256']
    a, b = old['master_sample_range_half_open']
    assert pcm(src) == master_pcm[a*2:b*2]
    words = [w for w in transcript['words'] if w['end'] > a/48000 and w['start'] < b/48000]
    assert ' '.join(w['token'] for w in words) == old['original_words']
    assert all(w['start'] >= a/48000 and w['end'] <= b/48000 for w in words)
    inputs.append({'path': rel(src), 'sha256': sha(src)})
    dst = OUT / 'audio' / f'{tid}.wav'
    dst.parent.mkdir(exist_ok=True); shutil.copyfile(src, dst)
    assert sha(dst) == old['audio_sha256']
    duration = old['audio_duration_seconds']; requested = old['request_duration_seconds']
    first = base[0].replace('21-second', f'{requested}-second')
    last = (f'The audio is {duration:.9f} seconds including its unchanged original pauses and end quiet. '
        'Lip and jaw movement follow this audio, not either muted video\'s speech timing. '
        f'Preserve the original cadence, complete the final word naturally, then close the lips gently, return the hands to rest and settle through {requested} seconds. '
        'Do not slow or stretch the words to fill the video duration. No extra words, silent syllables or pursed-lip hold. '
        'The camera, background and light remain still. Preserve the IMAGE\'s wider framing for the entire take: no automatic crop toward the face and no hands cut off. '
        'Real-time motion, one shot, no captions, titles, logos, cutaways, zoom, music or additional people.')
    prompt = '\n\n'.join([first, base[1], articulation, hands, directions[tid]['performance'],
        f'Speak only the supplied AUDIO reference, preserving its exact voice, words, rhythm and pauses from the beginning: "{old["original_words"]}"', last]) + '\n'
    pp = OUT / 'prompts' / f'{tid}.txt'; pp.parent.mkdir(exist_ok=True); pp.write_text(prompt)
    record = copy.deepcopy(old)
    record.update({'take_id': tid, 'baseline': 'owner-accepted V5', 'audio_path': rel(dst), 'audio_sha256': sha(dst),
        'prompt_path': rel(pp), 'prompt_sha256': sha(pp), 'source_audio_reused_from': rel(src),
        'generation_resolution': '1080p', 'source_framing': 'fixed wide seated study with both complete hands visible',
        'contextual_direction': directions[tid], 'future_waveform_or_perceptual_offset_seconds': None})
    plan_params = {k: v for k, v in params.items() if k not in ('prompt', 'medias', 'duration')}
    plan_params['duration'] = requested
    reference_inputs = []
    for name, role, job in [('framing', 'image', 'V5 identity, wide seated framing, hands, wardrobe, study and lighting'),
                             ('rebecca_behavior', 'video', 'Relaxed settling, ordinary blinks, subtle asymmetric head adjustments'),
                             ('henry_articulation', 'video', 'Clear connected articulation and concise emphasis that settles')]:
        reference_inputs.append({'role': role, 'function': job, **v5['recipe']['inputs'][name]})
    reference_inputs.append({'role': 'audio', 'function': 'Exact new words, voice, cadence and pauses', 'path': rel(dst), 'sha256': sha(dst)})
    req = {'status': 'local_preparation_only', 'execution_permitted': False,
        'provider_route': 'Existing Higgsfield Seedance 2.5 connection',
        'parameters_from_accepted_v5_except_duration': plan_params,
        'reference_inputs_in_order': reference_inputs, 'prompt_path': rel(pp), 'prompt_sha256': sha(pp),
        'source_generation_framing': 'Fixed wide; no generated camera move or crop.',
        'restoration_plan': {'model': sync['model'], 'sync_mode': sync['input']['sync_mode'],
            'audio_path': rel(dst), 'audio_sha256': sha(dst), 'original_audio_only': True,
            'native_video': 'Fresh matching V5 take only; no footage against unrelated words.',
            'output_alignment': 'Measure each restored output waveform insertion separately; do not inherit a V3/V5 offset. Waveform placement is not a measured perceptual lip-sync result.'},
        'audio_encoding_note': 'Retain this exact WAV. If an upload route requires MP3, create a true MP3 derivative with matching extension/MIME; no derivative encoding or upload occurred in this packet.',
        'proposed_editorial_framing': directions[tid]['framing'],
        'crop_geometry': None, 'crop_geometry_owner': 'Root chooses from actual generated frames and checks face/hand continuity.',
        'new_spend_or_upload_authority': False, 'price_or_credit_quote': None,
        'provider_duration_support_preflight': 'Root-owned; not queried here.', 'submission_performed': False}
    rp = save(f'requests/{tid}.json', req); record['request_path'] = rel(rp)
    take_records.append(record)

later_slots = copy.deepcopy(prior['moving_avatar_slots'][1:])
for slot in later_slots:
    slot['replacement_take'] = slot['replacement_take'].replace('v3-', 'v5-')
    slot['baseline_crop_geometry'] = slot.pop('crop')
    slot['replacement_crop_geometry'] = None
    slot['replacement_crop_status'] = 'Framing progression proposed; root chooses exact geometry from actual frames.'
    slot['current_source_path'] = slot['source_path'].replace('/r29-neutral-seller/', '/r30-avatar-v3-hook/')
    assert sha(ROOT / slot['current_source_path']) == slot['source_sha256']
    inputs.append({'path': slot['current_source_path'], 'sha256': slot['source_sha256']})
mapping = {'contract': 'current-cut-avatar-v5-preparation-1', 'status': 'local_preparation_complete',
    'work_order_id': work['work_order_id'], 'baseline_acceptance': v5,
    'timing_provenance': {'path': rel(PRIOR / 'mapping.json'), 'sha256': sha(PRIOR / 'mapping.json')},
    'current_review': rel(R30), 'fps': 24, 'interval_convention': prior['interval_convention'],
    'master': prior['master'], 'review_clock': prior['review_clock'],
    'opening': {'owner': 'Root integration', 'replacement': 'Accepted V5 corresponding restored source',
        'master_available_seconds': [0, 20.9], 'current_slot_review_seconds': [0, 97/24],
        'chosen_v5_inpoint_seconds': None, 'note': 'Root measures V5 placement and selects its opening source. V3 inpoint/offset is not transferred.'},
    'later_avatar_slots': later_slots, 'picture_hold': prior['picture_hold'],
    'question_cut_contract': prior['question_cut_contract'], 'prepared_takes': take_records,
    'generation_source_contract': {'resolution': '1080p', 'aspect_ratio': '16:9', 'fixed_camera': True,
        'wide_complete_hands': True, 'contextual_gestures': True, 'fixed_gesture_count': False,
        'scheduled_glances': False, 'brief_natural_lookaway_permitted': True},
    'crop_plan_status': 'Proposed framing progression only; exact pixels chosen by root from actual output.',
    'preserved_cues': {'post_title_entry_review': 56.5, 'post_title_medium_review': 1510/24,
        'post_title_close_review': 67.58, 'question_entry_review': 131,
        'question_medium_close_review': 3359/24, 'question_hold_start_review': 3433/24,
        'question_exit_review': 3451/24},
    'continuous_post_title': 'One15-second source, source0–6.416667 definition then6.416667–15 promise; advance continuously through both crop cuts.',
    'crop_review_criteria': ['Select face position and headroom from actual source rather than transplanting old tight-avatar transforms.',
        'Keep complete moving hands in each wide interval. Closer crops should not create distracting severed fingers at frame edges.',
        'Preserve continuous gesture state and source time across crop cues; do not retime or insert a cut to hide an inconvenient gesture.',
        'If a gesture intersects a fixed cut awkwardly, report and review it; do not silently move the cue.',
        'Retain the question last selected frame288 for the18-frame hold in its medium-close crop; inspect face and hand settling.'],
    'limits': ['No provider calls, uploads, runtime edits or canonical-state changes.',
        'V5 acceptance supersedes the older V3 tight-framing baseline. New stochastic takes need their own review.',
        'The question hold and close-cue details remain as recorded in the prior packet; no timing polish is proposed.']}
save('mapping.json', mapping)
checks = {'all_11_work_order_input_hashes_match': True, 'v5_acceptance_and_recipe_input_hashes_match': True,
    'original_master_hash_match': True, 'three_wavs_byte_identical_to_prior': True,
    'three_wavs_pcm_exact_original_master': True, 'three_word_quotes_match_locked_transcript': True,
    'later_r30_intervals_source_ranges_and_question_hold_match_prior': True,
    'all_three_request_plans_1080p': True, 'source_generation_fixed_wide': True,
    'post_title_crop_cues_retained': True, 'question_crop_cue_retained': True,
    'repeated_choreography_or_scheduled_glance_required': False,
    'provider_operations_or_runtime_edits': False}
save('checks.json', checks)
unique_inputs = {x['path']: x for x in inputs}
manifest = {'$schema': '../../../../../schemas/agent-deliverable.schema.json', 'schema_version': '1.0.0',
    'workflow_version': 'blueprint-cinema-1.0', 'work_order_id': work['work_order_id'], 'episode_folder': EP,
    'input_hashes_used': list(unique_inputs.values()),
    'files_produced': sorted(rel(p) for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in str(p)),
    'checks': [
        {'command': 'python3 prepare.py: verify11 issued pins and all V5 acceptance recipe/media hashes', 'outcome': 'pass'},
        {'command': 'python3 prepare.py: compare3 reused WAVs to prior hashes and exact original master PCM; verify complete transcript words', 'outcome': 'pass'},
        {'command': 'python3 prepare.py: verify later R30 intervals, current source hashes, crop cue and question hold against prior timing packet', 'outcome': 'pass'},
        {'command': 'python3 prepare.py: preserve V5 recipe1080p and both behavioral roles in3 local requests; no provider operations', 'outcome': 'pass'}],
    'sources_and_provenance': ['Current owner-accepted V5 artifact, baseline, framing image, two muted behavior references and successful request/restoration records, all hash verified.',
        'Three prior exact WAVs copied without re-encoding and independently byte-compared with original master PCM.',
        'R30 later picture intervals verified against prior source/master/review mapping; prior packet left unchanged.',
        'Wide reference image inspected locally; no new image/video or audio generated.'],
    'assumptions': ['Root integrates the accepted opening and performs provider preflight.',
        'Existing scene boundaries and crop cue times remain; root chooses new crop geometry from actual output.',
        'Later passages use new matching audio-driven V5 takes, never unrelated opening footage.'],
    'unresolved_questions': ['Actual generated gesture/face/hand performance and perceptual lip sync require output review.',
        'Exact crop geometry and each restored output waveform insertion offset are intentionally not chosen before output exists.'],
    'external_writes': False, 'paid_services': False, 'synthetic_generation': False,
    'approval_claimed': False, 'production_state_changed': False, 'status': 'complete'}
if rel(OUT / 'deliverable.json') not in manifest['files_produced']: manifest['files_produced'].append(rel(OUT / 'deliverable.json'))
save('deliverable.json', manifest)

# Validate every keyword used by the strict standard manifest schema without adding a dependency.
schema = json.loads((ROOT / 'blueprint-cinema/schemas/agent-deliverable.schema.json').read_text())
def validate(v, s):
    if '$ref' in s: return validate(v, schema['$defs'][s['$ref'].rsplit('/', 1)[1]])
    if 'const' in s: assert v == s['const']
    if 'enum' in s: assert v in s['enum']
    t = s.get('type')
    if t == 'object':
        assert isinstance(v, dict) and set(s.get('required', [])) <= set(v)
        if s.get('additionalProperties') is False: assert set(v) <= set(s.get('properties', {}))
        for k, x in v.items(): validate(x, s.get('properties', {}).get(k, {}))
    if t == 'array':
        assert isinstance(v, list) and len(v) >= s.get('minItems', 0)
        if s.get('uniqueItems'): assert len(v) == len({json.dumps(x, sort_keys=True) for x in v})
        for x in v: validate(x, s.get('items', {}))
    if t == 'string':
        assert isinstance(v, str) and len(v) >= s.get('minLength', 0)
        if 'pattern' in s: assert re.search(s['pattern'], v)
validate(manifest, schema)
assert all((ROOT / x).is_file() and (ROOT / x).is_relative_to(OUT) for x in manifest['files_produced'])
manifest['checks'].append({'command': 'Python stdlib validate all standard manifest schema keywords and output existence/owned paths', 'outcome': 'pass'})
save('deliverable.json', manifest)
print(json.dumps({'takes': len(take_records), 'audio_pcm_exact': True, 'resolution': '1080p',
    'planned_video_seconds': sum(t['request_duration_seconds'] for t in take_records),
    'manifest_constraints': 'pass', 'output': str(OUT)}))
