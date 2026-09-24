"""Record the checked local R47 candidate; never accepts its creative output."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent.parent
ROOT = EXP.parents[2]
TAKE = EXP / 'hyperframes/reviews/r47-transfer-criterion'
CONTEXT = EXP / 'hyperframes/reviews/r47-transfer-criterion-context'
NOW = datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def binding(path, locator=None):
    result = {'path': str(path.relative_to(ROOT)), 'sha256': sha(path)}
    if locator:
        result['locator'] = locator
    return result

qa = read(CONTEXT / 'qa/MEDIA-CHECK.json')
assert qa['result'] == 'pass', 'Complete and inspect media QA before recording a pass.'
for folder in [TAKE, CONTEXT]:
    pins = read(folder / 'RUNTIME-PINS.json')
    for name, digest in pins['files'].items():
        assert sha(folder / name) == digest, name

limitations = [
    'Waveform alignment and encoded media checks do not establish perceptual lip sync or natural performance.',
    'Root and independent visual review covered contact sheets and selected actual frames. Live playback was exercised with sound enabled; this is not a certified perceptual lip-sync verdict.',
    'Owner approved the generation plan; the returned R47 performance and this context assembly await owner review.',
    'The relationships, concentration and records examples are not included. No canonical episode or publication gate advances.'
]
short = TAKE / 'qa/r47-transfer-criterion.mp4'
context = CONTEXT / 'qa/r47-transfer-criterion-context.mp4'
shared = {
    'recorded_at_utc': NOW,
    'status': 'technically_checked_owner_review_pending',
    'hyperframes_version': '0.8.36',
    'owner_output_accepted': False,
    'canonical_gate_advanced': False,
    'limitations': limitations,
    'visual_observations': [
        'V5 wide seated study identity; both complete hands remain within frame.',
        'One restrained explanatory hand sweep returns to rest; no count gesture or compulsory look-away.',
        'Encoded boundary frames show the accepted machine followed immediately by the presenter; final frame remains covered.'
    ]
}
write(TAKE / 'VERIFICATION.json', {
    **shared, 'runtime_fingerprint_sha256': read(TAKE / 'RUNTIME-PINS.json')['fingerprint_sha256'],
    'render': binding(short), 'duration_seconds': 269 / 24, 'frames': 269,
    'picture_conform': read(TAKE / 'PICTURE-CONFORM.json'),
    'audio_alignment': read(TAKE / 'provider/ALIGNMENT.json'),
    'original_audio': binding(TAKE / 'public/audio/narration.wav'),
    'structure_check': binding(TAKE / 'qa/CHECK.json'),
    'cost_reconciliation': binding(TAKE / 'provider/COST-RECONCILIATION.json')
})
write(CONTEXT / 'VERIFICATION.json', {
    **shared, 'runtime_fingerprint_sha256': read(CONTEXT / 'RUNTIME-PINS.json')['fingerprint_sha256'],
    'render': binding(context), 'duration_seconds': 2481 / 24, 'frames': 2481,
    'accepted_context': binding(CONTEXT / 'public/media/accepted-context.mp4'),
    'presenter_entry_seconds': 2212 / 24,
    'structure_check': binding(CONTEXT / 'qa/CHECK.json'),
    'media_check': binding(CONTEXT / 'qa/MEDIA-CHECK.json'),
    'media_check_result': qa,
    'live_preview': {'url': 'http://100.101.49.30:3062/', 'http_status': 200,
                     'observed': 'Played from around1:27 through presenter ending; final wide shot visible. Paused back at1:27 with sound enabled for owner review.'}
})
event = {
    'event_id': 'r47-transfer-criterion-render-verified-v1',
    'decision_id': 's08-transfer-criterion-presenter', 'event_type': 'verification',
    'tags': ['presenter-return', 'v5-baseline', 'visible-hands', 'cut-timing', 'original-audio'],
    'data': {
        'decision_event_id': 'r47-transfer-criterion-presenter-v1',
        'method': 'Provider receipt and source hash readback; early/middle/late audio alignment; HyperFrames strict checks; full encoded picture decode and measured audio comparison; selected-frame and live preview inspection.',
        'result': 'pass', 'scope': 'R47 exact two-sentence take and appended R46 context as a technically checked review candidate.',
        'limitations': ' '.join(limitations),
        'artifact_hashes': [binding(short), binding(context)],
        'observed_performance': shared['visual_observations']
    },
    'evidence': [binding(TAKE / 'VERIFICATION.json', 'Take source, alignment and performance scope'),
                 binding(CONTEXT / 'VERIFICATION.json', 'Encoded context and live preview checks'),
                 binding(TAKE / 'provider/COST-RECONCILIATION.json', 'One generation and one restoration; no retries'),
                 binding(HERE / 'skill-after-generated-take/precedent-index.md', 'Frozen conditional precedent and review limits')]
}
write(HERE / 'RENDER-VERIFICATION-EVENT.json', event)

p = EXP / 'PRODUCTION-CHECKPOINT.json'
state = read(p)
state['recorded_at_utc'] = NOW
state['active_work'] = 'R47 original-audio V5 presenter take and joined context rendered and technically checked; owner performance review pending.'
if state['context_review']['path'].endswith('r46-revenue-machine-context'):
    state['accepted_context_review'] = state['context_review']
state['context_review'] = {
    'path': str(CONTEXT.relative_to(EXP)), 'url': 'http://100.101.49.30:3062/',
    'duration_seconds': 2481 / 24, 'authored_tail_entry_seconds': 2212 / 24,
    'status': 'rendered_owner_review_pending',
    'runtime_fingerprint_sha256': read(CONTEXT / 'RUNTIME-PINS.json')['fingerprint_sha256'],
    'verification': str((CONTEXT / 'VERIFICATION.json').relative_to(EXP)),
    'video': str(context.relative_to(EXP)), 'encoded_sha256': sha(context)
}
state['next_scene'].update({
    'status': 'rendered_owner_review_pending',
    'short_review': str(TAKE.relative_to(EXP)),
    'context_review': str(CONTEXT.relative_to(EXP)),
    'verification': str((TAKE / 'VERIFICATION.json').relative_to(EXP)),
    'cost_reconciliation': str((TAKE / 'provider/COST-RECONCILIATION.json').relative_to(EXP)),
    'automatic_retries': 0, 'owner_output_accepted': False
})
state['next_script_section'] = {
    'starts_at_master_seconds': 301.5,
    'first_line': 'Sometimes it is the relationships.',
    'direction': 'Develop the customer relationship example first, then concentration and records; preserve uncertainty over customer retention.',
    'status': 'not_built'
}
state['automation_status']['this_experiment'] = 'R46 accepted and pinned. R47 one V5 generation and one original-audio restoration completed, rendered in context and technically checked; owner output review pending.'
state['automation_status']['next_steps'][0] = 'Review R47 in context, then develop the relationships example. Preserve the earlier question-avatar hand-movement rebuild trigger.'
state['new_paid_work'] = True
state['canonical_gate_advanced'] = False
state['decision_system_updated_at_utc'] = NOW
write(p, state)
print(json.dumps({'event': str(HERE / 'RENDER-VERIFICATION-EVENT.json'), 'context_sha256': sha(context), 'short_sha256': sha(short)}, indent=2))
