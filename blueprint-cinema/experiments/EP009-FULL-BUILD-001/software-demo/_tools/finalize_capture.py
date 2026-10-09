#!/usr/bin/env python3
"""Finalize the real S13 screen capture without rendering r6.

This helper performs only local media preparation.  It requires a reviewed
provenance record, selects exactly 706 existing raw screen frames, and writes
the two source reviews plus the selection/direction records consumed by
``build_r6.py``.  It never calls a provider, starts a browser, changes Node-RED,
or renders the full episode.

The S13 insert stays deliberately split:

* F03 existing illustrative establish: output [16704,16752), source [96,144)
* actual screen capture:                output [16752,17458), source [0,706)

The separate F03 entry is important: generated inn footage establishes the
task but is never presented as evidence that the workflow ran.

Expected provenance JSON (use --print-provenance-template for a fill-in form):

  record_type: ep009_software_demo_capture_provenance
  status: reviewed_for_capture_conform
  capture_id: same as --capture-id
  real_software_capture: true
  tools: {automation: Node-RED, model_provider: OpenAI}
  fixture: fixed fictional Maya Chen / Alder House Inn fixture
  no_send: true; email_sending_available: false
  human_review: all listed workflow and legibility booleans true
  f03_establish_review: human reviewer/method/limits plus three booleans true
  workflow.editorial_ellipsis: declared boolean, with a reason if true
  evidence: nonempty array of existing {path, sha256} records

All paths must remain inside this checkout and raw screen capture must live in
the isolated software-demo lane.  Existing outputs are never overwritten.
"""

import argparse
import copy
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

S = Path(__file__).resolve().parents[1]
B = S.parent
A = B / 'assembly'
sys.path[:0] = [str(B / 'presenter-look-transfer' / '_tools'), str(A / '_tools')]

import build_r6 as r6
from build_review import video_hashes

FPS = 24
SCREEN_FRAMES = 706
F03_FRAMES = 48
F03_SOURCE_START = 96
F03_SOURCE_END = F03_SOURCE_START + F03_FRAMES
F03_OUTPUT = [16704, 16752]
SCREEN_OUTPUT = [16752, 17458]
F03 = B / 'film' / 'F03' / 'final' / 'seg003.mp4'
F03_SHA = '26a4194672f3b3544b7d0d4057a9265ed83da7f2edd267fd61c44bc94a11eb85'
F03_EDIT = B / 'film' / 'F03' / 'EDIT-R1-seg003.json'
F03_EDIT_SHA = 'f5305948a7447984c0738764209fa403ed91af01319f745dcd7252fdd74d5d70'
DECISION = S / 'DECISION-EVENT-r1.json'

FIXTURE = {
    'id': 'alder-maya-20260918',
    'fictional': True,
    'guest': 'Maya Chen',
    'property': 'Alder House Inn',
    'checkout': '2026-09-18T10:00:00-04:00',
    'timezone': 'America/New_York',
    'communication_preference': 'One-off thank-you only. No future promotions.',
    'one_off_thank_you': True,
    'seasonal_campaign_eligible': False,
}


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def sequence_sha256(hashes):
    return hashlib.sha256(('\n'.join(hashes) + '\n').encode()).hexdigest()


def repo_file(path, label, within=None):
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f'{label} is not a file: {path}')
    try:
        path.relative_to(r6.R)
    except ValueError as exc:
        raise ValueError(f'{label} must be inside this checkout: {path}') from exc
    if within is not None:
        try:
            path.relative_to(within)
        except ValueError as exc:
            raise ValueError(f'{label} must be inside {within}: {path}') from exc
    return path


def bound(path):
    return r6.bound(path)


def verify_known_inputs():
    f03 = r6.verify_bound({'path': r6.rel(F03), 'sha256': F03_SHA})
    edit = r6.verify_bound({'path': r6.rel(F03_EDIT), 'sha256': F03_EDIT_SHA})
    decision = repo_file(DECISION, 'decision event', S)
    edit_data = read_json(edit)
    if (edit_data.get('path'), edit_data.get('sha256'), edit_data.get('frames')) != (r6.rel(f03), F03_SHA, 152):
        raise ValueError('F03 current edit record no longer binds the expected 152-frame source')
    return f03, edit, decision


def require_string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be a nonempty string')
    return value.strip()


def require_true(mapping, key, label=None):
    if not isinstance(mapping, dict) or mapping.get(key) is not True:
        raise ValueError(f'{label or key} must be true')


def require_false(mapping, key, label=None):
    if not isinstance(mapping, dict) or mapping.get(key) is not False:
        raise ValueError(f'{label or key} must be false')


def assert_bound_evidence(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f'{label} must be a nonempty array of hash-bound evidence')
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not isinstance(item.get('sha256'), str):
            raise ValueError(f'{label} contains an unbound evidence item')
        r6.verify_bound(item)


def provenance_template(capture_id='<capture-id>'):
    return {
        'record_type': 'ep009_software_demo_capture_provenance',
        'status': 'reviewed_for_capture_conform',
        'capture_id': capture_id,
        'real_software_capture': True,
        'tools': {'automation': 'Node-RED', 'model_provider': 'OpenAI'},
        'fixture': copy.deepcopy(FIXTURE),
        'no_send': True,
        'email_sending_available': False,
        'workflow': {
            'run_id': '<persisted-real-test-run-id>',
            'raw_take_continuous': True,
            'editorial_ellipsis': {
                'declared': False,
                'reason': None,
                'note': 'Set declared true and describe any omitted real latency or non-contiguous operation.',
            },
        },
        'human_review': {
            'reviewer': '<human reviewer>',
            'method': '<reviewed raw take and conformed screen source at delivery scale>',
            'limits': '<bounded fictional test; no customer or send claim>',
            'legibility_checked': True,
            'workflow_sequence_checked': True,
            'date_to_queue_checked': True,
            'human_edit_checked': True,
            'one_off_approval_checked': True,
            'seasonal_exclusion_checked': True,
            'queued_draft_not_sent_checked': True,
        },
        'f03_establish_review': {
            'reviewer': '<human reviewer>',
            'method': '<reviewed F03 frames 96-143 at delivery scale>',
            'limits': 'Illustrative inn establish only; it is not evidence that software ran.',
            'source_window_checked': True,
            'illustrative_only_confirmed': True,
            'typing_task_focus_checked': True,
        },
        'evidence': [
            {
                'path': 'blueprint-cinema/experiments/EP009-FULL-BUILD-001/software-demo/capture/<capture-id>/SANITIZED-RUNTIME-EVIDENCE.json',
                'sha256': '<sha256>',
            }
        ],
    }


def validate_provenance(path, capture_id, raw_frames, source_start):
    path = repo_file(path, 'provenance', S)
    data = read_json(path)
    if data.get('record_type') != 'ep009_software_demo_capture_provenance':
        raise ValueError('Wrong provenance record type')
    if data.get('status') != 'reviewed_for_capture_conform':
        raise ValueError('Provenance must be reviewed_for_capture_conform')
    if data.get('capture_id') != capture_id:
        raise ValueError('Provenance capture_id must exactly match --capture-id')
    require_true(data, 'real_software_capture')
    tools = data.get('tools')
    if not isinstance(tools, dict) or tools.get('automation') != 'Node-RED' or tools.get('model_provider') != 'OpenAI':
        raise ValueError('Provenance must assert Node-RED automation and OpenAI model provider')
    if data.get('fixture') != FIXTURE:
        raise ValueError('Provenance must bind the exact fictional Maya Chen / Alder House fixture')
    require_true(data, 'no_send')
    require_false(data, 'email_sending_available')
    workflow = data.get('workflow')
    if not isinstance(workflow, dict):
        raise ValueError('Provenance workflow object is required')
    require_string(workflow.get('run_id'), 'workflow.run_id')
    require_true(workflow, 'raw_take_continuous')
    ellipsis = workflow.get('editorial_ellipsis')
    if not isinstance(ellipsis, dict) or not isinstance(ellipsis.get('declared'), bool):
        raise ValueError('workflow.editorial_ellipsis.declared must be a boolean')
    if ellipsis['declared']:
        require_string(ellipsis.get('reason'), 'workflow.editorial_ellipsis.reason')
    elif source_start != 0 or raw_frames != SCREEN_FRAMES:
        raise ValueError('A trimmed raw take requires a declared editorial ellipsis with its reason')
    human = data.get('human_review')
    if not isinstance(human, dict):
        raise ValueError('human_review object is required')
    for key in ('legibility_checked', 'workflow_sequence_checked', 'date_to_queue_checked', 'human_edit_checked',
                'one_off_approval_checked', 'seasonal_exclusion_checked', 'queued_draft_not_sent_checked'):
        require_true(human, key, 'human_review.' + key)
    require_string(human.get('reviewer'), 'human_review.reviewer')
    require_string(human.get('method'), 'human_review.method')
    require_string(human.get('limits'), 'human_review.limits')
    f03_review = data.get('f03_establish_review')
    if not isinstance(f03_review, dict):
        raise ValueError('f03_establish_review object is required')
    for key in ('source_window_checked', 'illustrative_only_confirmed', 'typing_task_focus_checked'):
        require_true(f03_review, key, 'f03_establish_review.' + key)
    require_string(f03_review.get('reviewer'), 'f03_establish_review.reviewer')
    require_string(f03_review.get('method'), 'f03_establish_review.method')
    require_string(f03_review.get('limits'), 'f03_establish_review.limits')
    assert_bound_evidence(data.get('evidence'), 'provenance.evidence')
    return path, data


def video_stream(path, label):
    info = r6.probe(path)
    try:
        stream = next(item for item in info['streams'] if item['codec_type'] == 'video')
    except StopIteration as exc:
        raise ValueError(f'{label} has no video stream') from exc
    try:
        frames = int(stream['nb_read_frames'])
    except (TypeError, ValueError, KeyError) as exc:
        raise ValueError(f'{label} lacks a readable decoded frame count') from exc
    if (stream.get('width'), stream.get('height'), stream.get('r_frame_rate')) != (1280, 720, '24/1'):
        raise ValueError(f'{label} must be 1280x720 at 24/1, got {stream.get("width")}x{stream.get("height")} at {stream.get("r_frame_rate")}')
    return info, stream, frames


def decoded_hashes(path):
    command = [
        'ffmpeg', '-nostdin', '-v', 'error', '-threads', '1', '-i', str(path),
        '-map', '0:v:0', '-an', '-vf', 'format=yuv420p', '-fps_mode', 'passthrough',
        '-f', 'framehash', '-hash', 'sha256', '-',
    ]
    text = subprocess.check_output(command, text=True)
    lines = [line for line in text.splitlines() if line and not line.startswith('#')]
    hashes = [line.rsplit(',', 1)[-1].strip() for line in lines]
    if any(not re.fullmatch('[0-9a-f]{64}', item) for item in hashes):
        raise ValueError(f'Unreadable decoded frame hashes: {path}')
    return hashes


def run(command):
    subprocess.run(command, check=True)


def normalize_screen(raw, source_start, output):
    source_end = source_start + SCREEN_FRAMES - 1
    select = f"select=between(n\\,{source_start}\\,{source_end}),setpts=N/(24*TB),setsar=1,format=yuv420p"
    command = [
        'ffmpeg', '-nostdin', '-n', '-v', 'error', '-stats', '-filter_complex_threads', '2',
        '-i', str(raw), '-map', '0:v:0', '-an', '-vf', select,
        '-frames:v', str(SCREEN_FRAMES), '-r', '24', '-fps_mode', 'passthrough',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '0', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', str(output),
    ]
    run(command)
    return command


def output_paths(capture_id):
    directory = S / 'capture' / capture_id
    return {
        'directory': directory,
        'screen': directory / 'screen-706.mp4',
        'conform': directory / 'SCREEN-CONFORM.json',
        'screen_review': directory / 'SCREEN-REVIEW.json',
        'f03_review': directory / 'F03-ESTABLISH-REVIEW.json',
        'direction': directory / 'SELECTED-PICTURE-DIRECTION.json',
        'selections': S / 'SELECTIONS.json',
    }


def require_fresh_outputs(paths):
    existing = [path for path in paths.values() if isinstance(path, Path) and path.exists()]
    if existing:
        raise FileExistsError('Refusing to overwrite existing capture artifacts: ' + ', '.join(str(path) for path in existing))


def screen_conform_record(raw, raw_probe, raw_stream, raw_hashes, source_start, screen, screen_hashes, command, provenance):
    selected = raw_hashes[source_start:source_start + SCREEN_FRAMES]
    return {
        'record_type': 'ep009_software_demo_screen_conform',
        'status': 'conformed_for_review',
        'at': utc_now(),
        'source': bound(raw),
        'source_probe': raw_probe,
        'source_video_stream': raw_stream,
        'source_total_frames': len(raw_hashes),
        'source_selected_frames': [source_start, source_start + SCREEN_FRAMES],
        'source_selected_decoded_frame_sequence_sha256': sequence_sha256(selected),
        'output': bound(screen),
        'output_frames': [0, SCREEN_FRAMES],
        'output_decoded_frame_sequence_sha256': screen_hashes['sequence_sha256'],
        'operations': {
            'frame_select_only': True,
            'interpolation': False,
            'respeed': False,
            'frame_duplication': False,
            'unselected_source_frames_discarded': True,
            'audio_discarded': True,
            'encoder': 'libx264 lossless CRF 0 after yuv420p normalization',
        },
        'command': command,
        'selected_source_pixels_match_output': screen_hashes['hashes'] == selected,
        'provenance': bound(provenance),
        'editorial_ellipsis': copy.deepcopy(read_json(provenance)['workflow']['editorial_ellipsis']),
        'limits': 'This proves exact decoded frame selection and conform. It does not prove client results, consent, sending, capacity, or legal compliance.',
    }


def f03_review_record(f03, edit, provenance):
    review = read_json(provenance)['f03_establish_review']
    return {
        'record_type': 'ep009_software_demo_f03_establish_review',
        'status': 'reviewed_for_insertion',
        'at': utc_now(),
        'source': bound(f03),
        'source_frames': [F03_SOURCE_START, F03_SOURCE_END],
        'errors': [],
        'reviewer': review['reviewer'],
        'method': review['method'],
        'limits': review['limits'],
        'evidence': {
            'source_edit': bound(edit),
            'source_video': bound(f03),
            'direction': bound(S / 'DIRECTION.md'),
            'capture_provenance': bound(provenance),
        },
        'illustrative_establish_only': True,
        'software_execution_evidence': False,
        'source_window_checked': True,
        'illustrative_only_confirmed': True,
        'typing_task_focus_checked': True,
        'selection': {
            'output_frames': F03_OUTPUT,
            'source_frames': [F03_SOURCE_START, F03_SOURCE_END],
            'purpose': 'Familiar inn/laptop context before the real fixture and workflow capture.',
        },
    }


def screen_review_record(screen, conform, provenance):
    source = read_json(provenance)
    review = source['human_review']
    return {
        'record_type': 'ep009_software_demo_screen_capture_review',
        'status': 'reviewed_for_insertion',
        'at': utc_now(),
        'source': bound(screen),
        'source_frames': [0, SCREEN_FRAMES],
        'errors': [],
        'reviewer': review['reviewer'],
        'method': review['method'],
        'limits': review['limits'],
        'evidence': {
            'capture_provenance': bound(provenance),
            'screen_conform': bound(conform),
            'raw_capture': bound(r6.verify_bound(read_json(conform)['source'])),
            'decision': bound(DECISION),
        },
        'real_software_capture': True,
        'legibility_checked': True,
        'workflow_sequence_checked': True,
        'date_to_queue_checked': True,
        'human_edit_checked': True,
        'one_off_approval_checked': True,
        'seasonal_exclusion_checked': True,
        'queued_draft_not_sent_checked': True,
        'fixture': copy.deepcopy(FIXTURE),
        'tools': {'automation': 'Node-RED', 'model_provider': 'OpenAI'},
        'no_send': True,
        'email_sending_available': False,
        'workflow_run_id': source['workflow']['run_id'],
        'editorial_ellipsis': copy.deepcopy(source['workflow']['editorial_ellipsis']),
        'selection': {
            'output_frames': SCREEN_OUTPUT,
            'source_frames': [0, SCREEN_FRAMES],
            'purpose': 'Actual fictional Node-RED/OpenAI test: draft, date-to-queue, human edit/approval, seasonal exclusion.',
        },
    }


def make_direction(base, f03, screen, provenance):
    f03_source = bound(f03)
    screen_source = bound(screen)
    selected_inserts = [
        {
            'id': 's13-f03-establish',
            'output_frames': F03_OUTPUT,
            'source': f03_source,
            'source_start_frame': F03_SOURCE_START,
        },
        {
            'id': 's13-screen-workflow',
            'output_frames': SCREEN_OUTPUT,
            'source': screen_source,
            'source_start_frame': 0,
        },
    ]
    return {
        'record_type': 'ep009_s13_software_demo_selected_picture_direction',
        'status': 'selected_for_review',
        'at': utc_now(),
        'base_build': bound(r6.BASE),
        'base_verification': bound(r6.BASE_VERIFY),
        'timing_contract': bound(r6.CONTRACT),
        'master': base['master'],
        'allowed_output_frames': r6.SCOPE,
        'source_direction': bound(S / 'DIRECTION.md'),
        'decision_event': bound(DECISION),
        'selected_inserts': selected_inserts,
        'editorial_ellipsis': copy.deepcopy(read_json(provenance)['workflow']['editorial_ellipsis']),
        'continuity': {
            'fixture_id': FIXTURE['id'],
            'f03_is_illustrative_only': True,
            'screen_is_actual_test_capture': True,
            'no_send': True,
            'preserve_question_frames': [16609, 16704],
            'preserve_closing_judgment_frames': [17458, 17523],
        },
        'limits': 'Selected picture only. No narration, presentation, P00/P08, owner-acceptance, release, customer-proof, or capacity change is inferred.',
    }


def make_selection(base, f03, f03_hashes, screen, screen_hashes, f03_review, screen_review, conform, direction):
    f03_source = bound(f03)
    screen_source = bound(screen)
    f03_insert = {
        'id': 's13-f03-establish',
        'kind': 'existing_film',
        'output_frames': F03_OUTPUT,
        'source': f03_source,
        'source_start_frame': F03_SOURCE_START,
        'source_total_frames': 152,
        'decoded_frame_sequence_sha256': f03_hashes['sequence_sha256'],
        'review': bound(f03_review),
    }
    screen_insert = {
        'id': 's13-screen-workflow',
        'kind': 'real_software_capture',
        'output_frames': SCREEN_OUTPUT,
        'source': screen_source,
        'source_start_frame': 0,
        'source_total_frames': SCREEN_FRAMES,
        'decoded_frame_sequence_sha256': screen_hashes['sequence_sha256'],
        'review': bound(screen_review),
    }
    return {
        'record_type': 'ep009_software_demo_selections',
        'status': 'selected_for_review',
        'at': utc_now(),
        'base_build': bound(r6.BASE),
        'timing_contract': bound(r6.CONTRACT),
        'master': base['master'],
        'direction': bound(direction),
        'inserts': [f03_insert, screen_insert],
        'source_conform': bound(conform),
        'limits': 'Private r6 source selection only. The actual screen source is a fictional, no-send test and the F03 establish is illustrative.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--print-provenance-template', action='store_true', help='Print the required provenance shape and exit.')
    parser.add_argument('--capture-id', help='Simple immutable capture ID, e.g. maya-run-r1.')
    parser.add_argument('--raw', type=Path, help='Raw 1280x720 24fps screen capture inside software-demo/.')
    parser.add_argument('--provenance', type=Path, help='Reviewed, hash-bound capture-provenance JSON inside software-demo/.')
    parser.add_argument('--capture-start-frame', type=int, default=0, help='First raw decoded frame to retain; default: 0.')
    parser.add_argument('--dry-run', action='store_true', help='Validate inputs and print paths without writing media or JSON.')
    args = parser.parse_args()

    if args.print_provenance_template:
        print(json.dumps(provenance_template(args.capture_id or '<capture-id>'), indent=2))
        return 0
    if not args.capture_id or not re.fullmatch(r'[a-z][a-z0-9-]{2,63}', args.capture_id):
        parser.error('--capture-id must be 3-64 lowercase letters, digits, or hyphens and start with a letter')
    if args.raw is None or args.provenance is None:
        parser.error('--raw and --provenance are required unless --print-provenance-template is used')
    if args.capture_start_frame < 0:
        parser.error('--capture-start-frame must be zero or greater')

    raw = repo_file(args.raw, 'raw capture', S)
    f03, edit, _ = verify_known_inputs()
    base = r6.checked_base()
    raw_probe, raw_stream, raw_frames = video_stream(raw, 'raw capture')
    if args.capture_start_frame + SCREEN_FRAMES > raw_frames:
        raise ValueError(f'Raw capture has {raw_frames} decoded frames; need [{args.capture_start_frame},{args.capture_start_frame + SCREEN_FRAMES})')
    provenance, _ = validate_provenance(args.provenance, args.capture_id, raw_frames, args.capture_start_frame)
    paths = output_paths(args.capture_id)
    if args.dry_run:
        print(json.dumps({
            'status': 'inputs_validated_not_written',
            'raw': bound(raw),
            'raw_frames': raw_frames,
            'source_selected_frames': [args.capture_start_frame, args.capture_start_frame + SCREEN_FRAMES],
            'f03_source_frames': [F03_SOURCE_START, F03_SOURCE_END],
            'f03_output_frames': F03_OUTPUT,
            'screen_output_frames': SCREEN_OUTPUT,
            'outputs': {key: r6.rel(value) for key, value in paths.items() if key != 'directory'},
        }))
        return 0

    require_fresh_outputs(paths)
    paths['directory'].mkdir(parents=True, exist_ok=False)
    raw_hashes = decoded_hashes(raw)
    if len(raw_hashes) != raw_frames:
        raise ValueError('Raw decoded framehash count differs from ffprobe count')
    normalize_command = normalize_screen(raw, args.capture_start_frame, paths['screen'])
    _, _, screen_frames = video_stream(paths['screen'], 'normalized screen capture')
    if screen_frames != SCREEN_FRAMES:
        raise ValueError(f'Normalized screen output has {screen_frames} frames, expected {SCREEN_FRAMES}')
    screen_hashes = video_hashes(paths['screen'], SCREEN_FRAMES)
    selected_raw_hashes = raw_hashes[args.capture_start_frame:args.capture_start_frame + SCREEN_FRAMES]
    if screen_hashes['hashes'] != selected_raw_hashes:
        raise ValueError('Normalized screen pixels do not exactly match selected raw frames; no interpolation/respeed claim is permitted')
    f03_hashes = video_hashes(f03, 152)

    conform = screen_conform_record(raw, raw_probe, raw_stream, raw_hashes, args.capture_start_frame,
                                    paths['screen'], screen_hashes, normalize_command, provenance)
    write_new(paths['conform'], conform)
    f03_review = f03_review_record(f03, edit, provenance)
    write_new(paths['f03_review'], f03_review)
    screen_review = screen_review_record(paths['screen'], paths['conform'], provenance)
    write_new(paths['screen_review'], screen_review)
    direction = make_direction(base, f03, paths['screen'], provenance)
    write_new(paths['direction'], direction)
    selection = make_selection(base, f03, f03_hashes, paths['screen'], screen_hashes,
                               paths['f03_review'], paths['screen_review'], paths['conform'],
                               paths['direction'])
    write_new(paths['selections'], selection)

    print(json.dumps({
        'status': 'screen_source_and_r6_selection_prepared_not_rendered',
        'screen': bound(paths['screen']),
        'screen_frames': SCREEN_FRAMES,
        'f03_source_frames': [F03_SOURCE_START, F03_SOURCE_END],
        'f03_output_frames': F03_OUTPUT,
        'screen_output_frames': SCREEN_OUTPUT,
        'review': bound(paths['screen_review']),
        'f03_review': bound(paths['f03_review']),
        'direction': bound(paths['direction']),
        'selections': bound(paths['selections']),
        'r6_rendered': False,
    }))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        raise SystemExit(2)
