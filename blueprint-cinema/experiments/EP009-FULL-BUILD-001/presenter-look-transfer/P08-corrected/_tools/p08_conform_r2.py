#!/usr/bin/env python3
"""Exact P08 pause-comparison A + unchanged B; requires bound root selection."""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import wave
from pathlib import Path

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parents[1]
T = D.parent
A = T.parent / 'assembly'
F = D / 'final-r2'
PLAN = F / 'PLAN.json'
DECISION = F / 'SELECTION-DECISION.json'
sys.path[:0] = [str(T / '_tools'), str(A / '_tools')]
from build_r3 import bound, read, verify_bound, write, probe
from build_review import video_hashes
from verify_r3 import audio_check


def checked_plan():
    p = read(PLAN)
    if (p['frames'], p['master_frames'], p['master_samples']) != (343, [15920, 16263], [31840000, 32526000]):
        raise ValueError('Only the unchanged P08 slot is allowed')
    paths = {k: verify_bound(v) for k, v in p['bindings'].items()}
    if p['helper'] != bound(Path(__file__)):
        raise ValueError('Frozen helper changed')
    for b in p['prior_A_failed_evidence']:
        verify_bound(b)
    with wave.open(str(paths['master']), 'rb') as w:
        if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (48000, 1, 2):
            raise ValueError('Unexpected master format')
        w.setpos(31840000)
        raw = w.readframes(686000)
    if len(raw) != 1372000:
        raise ValueError('Master sample shortfall')
    for key, lo, hi in [('A_audio', 0, 346000), ('B_audio', 346000, 686000)]:
        with wave.open(str(paths[key]), 'rb') as w:
            if (w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()) != (48000, 1, 2, hi-lo):
                raise ValueError('Wrong local narration format or duration: ' + key)
            if w.readframes(hi-lo) != raw[lo*2:hi*2]:
                raise ValueError('Local narration differs from locked master: ' + key)
    if p['A']['source_frames'] != [0, 173] or p['B']['source_frames'] != [2, 172]:
        raise ValueError('Selected frame intervals changed')
    prior = read(paths['prior_conform'])
    bp = next(x for x in prior['pieces'] if x['part'] == 'P08r3b')
    if (p['B']['crop_rect'] != bp['crop_rect'] or p['bindings']['B_restored'] != bp['restored']
            or p['bindings']['B_nose'] != bp['crop_measurement'] or p['B']['source_frames'] != bp['source_frames']):
        raise ValueError('B differs from the previous exact conform')
    mapping = read(paths['A_frame_map'])
    expected = list(range(107)) + [106]*4 + list(range(107, 169))
    if (mapping['picture'] != p['bindings']['A_picture'] or mapping['output_to_source_frames'] != expected
            or mapping['decoded_frames_exactly_match_map'] is not True or mapping['frames'] != 173 or mapping['fps'] != 24):
        raise ValueError('Wrong pause candidate provenance')
    review = read(paths['A_independent_review'])
    if review['candidate'] != p['bindings']['A_picture'] or review['lexical_acoustic_audit'] != p['bindings']['lexical_audit']:
        raise ValueError('Independent comparison is stale')
    for key, n in [('A_picture', 173), ('B_restored', 175)]:
        v = next(x for x in probe(paths[key])['streams'] if x['codec_type'] == 'video')
        if (v['width'], v['height'], v['r_frame_rate'], int(v['nb_read_frames'])) != (1920, 1080, '24/1', n):
            raise ValueError('Unexpected selected picture format: ' + key)
    return p, paths, raw


def checked_decision(p, expected_sha):
    if not expected_sha:
        raise ValueError('Render needs the explicit root decision SHA256')
    decision = read(verify_bound({'path': str(DECISION), 'sha256': expected_sha}))
    if (decision.get('status') != 'selected_for_private_review' or decision.get('plan') != bound(PLAN)
            or decision.get('selected_A') != p['bindings']['A_picture']
            or decision.get('independent_sync_review') != p['bindings']['A_independent_review']
            or decision.get('owner_accepted') is not False or not decision.get('reason')):
        raise ValueError('Missing, stale, or wrong scoped root selection')
    return decision


def render(p, paths, raw, decision):
    names = ['seg044.mp4', 'narration-exact-master.wav', 'CONFORM-INTENT.json', 'CONFORM.json',
             'SOURCE-FRAME-MAP.json', 'FRAME-HASHES.json', 'VERIFY.json', 'SELECT.json']
    if any((F/n).exists() for n in names):
        raise FileExistsError('Preserve every existing final-r2 artifact; use a new version after any partial failure')
    cw, ch, x, y = p['B']['crop_rect']
    graph = ('[0:v]trim=start_frame=0:end_frame=173,setpts=N/(24*TB),scale=1280:720:flags=lanczos,setsar=1,format=yuv420p[v0];'
             f'[1:v]trim=start_frame=2:end_frame=172,setpts=N/(24*TB),crop={cw}:{ch}:{x}:{y},scale=1280:720:flags=lanczos,setsar=1,format=yuv420p[v1];'
             '[v0][v1]concat=n=2:v=1:a=0,setpts=N/(24*TB)[vo];'
             '[2:a]atrim=start_sample=31840000:end_sample=32526000,asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[ao]')
    output = F/'seg044.mp4'
    cmd = ['ffmpeg', '-nostdin', '-n', '-v', 'error', '-filter_complex_threads', '2',
           '-threads', '1', '-i', str(paths['A_picture']), '-threads', '1', '-i', str(paths['B_restored']),
           '-i', str(paths['master']), '-filter_complex', graph, '-map', '[vo]', '-map', '[ao]',
           '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-threads', '2', '-pix_fmt', 'yuv420p', '-r', '24',
           '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(output)]
    write(F/'CONFORM-INTENT.json', {'status': 'rendering_root_selected_private_review_candidate',
          'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'plan': bound(PLAN),
          'root_selection': bound(DECISION), 'helper': bound(Path(__file__)), 'command': cmd, 'owner_accepted': False})
    subprocess.run(cmd, check=True)
    narration = F/'narration-exact-master.wav'
    with wave.open(str(narration), 'wb') as w:
        w.setparams((1, 2, 48000, 0, 'NONE', 'not compressed')); w.writeframes(raw)
    amap = read(paths['A_frame_map'])['output_to_source_frames']
    fm = {'frames': 343, 'fps': 24, 'master_frames': p['master_frames'], 'plan': bound(PLAN),
          'A_source_map': p['bindings']['A_frame_map'], 'entries': [
              {'output_frame': i, 'piece': 'P08r3a', 'selected_source_frame': i, 'pre_pause_v2_source_frame': s}
              for i, s in enumerate(amap)] + [
              {'output_frame': 173+i, 'piece': 'P08r3b', 'selected_source_frame': 2+i} for i in range(170)],
          'source_bindings': {'P08r3a': p['bindings']['A_picture'], 'P08r3b': p['bindings']['B_restored']},
          'A_four_extra_hold_frames_disclosed': True, 'B_timing_and_crop_unchanged': True}
    write(F/'SOURCE-FRAME-MAP.json', fm)
    hashes = video_hashes(output, 343)
    write(F/'FRAME-HASHES.json', {**hashes, 'output': bound(output)})
    conform = {'record_type': 'corrected_P08_root_selected_pause_A_plus_unchanged_B',
        'status': 'rendered_private_review_candidate', 'plan': bound(PLAN), 'root_selection': bound(DECISION),
        'helper': bound(Path(__file__)), 'output': bound(output), 'master': p['bindings']['master'],
        'output_frames': p['master_frames'], 'frames': 343, 'master_sample_range': p['master_samples'],
        'master_pcm_sha256': hashlib.sha256(raw).hexdigest(), 'exact_narration': bound(narration),
        'source_frame_map': bound(F/'SOURCE-FRAME-MAP.json'), 'replacement_frame_sequence_sha256': hashes['sequence_sha256'],
        'frame_hashes': bound(F/'FRAME-HASHES.json'), 'pieces': [
            {'part': 'P08r3a', 'local_frames': [0,173], 'source_frames': [0,173], 'crop_size': 'W',
             'source': p['bindings']['A_picture'], 'picture_edit': p['bindings']['A_pause_plan'],
             'source_frame_map': p['bindings']['A_frame_map'], 'independent_review': p['bindings']['A_independent_review']},
            {'part': 'P08r3b', 'local_frames': [173,343], 'source_frames': [2,172], 'crop_size': 'M',
             'crop_rect': p['B']['crop_rect'], 'source': p['bindings']['B_restored'], 'crop_measurement': p['bindings']['B_nose'],
             'alignment': p['bindings']['B_alignment'], 'sync_diagnostics': p['bindings']['B_gate']}],
        'prior_failed_A_diagnostics_preserved': p['prior_A_failed_evidence'],
        'review_limits': p['review_limits'], 'owner_accepted': False, 'lip_sync_approved': False,
        'existing14performances_modified': False, 'diagnostic_guide_in_final': False, 'command': cmd}
    write(F/'CONFORM.json', conform)
    info = probe(output)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    errors = []
    if (v['width'], v['height'], v['r_frame_rate'], int(v['nb_read_frames'])) != (1280,720,'24/1',343):
        errors.append('video_format_or_frame_count')
    if (a['sample_rate'], a['channels']) != ('48000',2): errors.append('audio_format')
    if abs(float(info['format']['duration'])-343/24) > .002: errors.append('container_duration')
    audio = audio_check(output, paths['master'], p['master_frames'])
    if audio['compared_samples'] != 686000 or any(audio['decode_exit_codes']): errors.append('audio_length_or_decode')
    if audio['min_voiced_window_corr'] < .999 or audio['max_abs_voiced_window_rms_db'] > .1: errors.append('audio_identity_or_level')
    if not 0 <= audio['aac_padding_samples'] <= 1024: errors.append('excess_AAC_padding')
    verification = {'record_type': 'corrected_P08_final_r2_mechanical_verification',
        'status': 'mechanical_pass_private_review_only' if not errors else 'failed', 'errors': errors,
        'output': bound(output), 'conform': bound(F/'CONFORM.json'), 'frames': 343, 'master_sample_range': p['master_samples'],
        'master_pcm_sha256': conform['master_pcm_sha256'], 'program_samples': 686000, 'probe': info, 'audio': audio,
        'replacement_frame_sequence_sha256': hashes['sequence_sha256'], 'owner_accepted': False,
        'lip_sync_approved': False, 'review_limits': p['review_limits']}
    write(F/'VERIFY.json', verification)
    if errors: raise ValueError('Mechanical verification failed: '+str(errors))
    write(F/'SELECT.json', {'record_type': 'corrected_P08_scoped_private_review_candidate',
        'status': 'root_selected_private_review_candidate_sync_limits_retained', 'segment_id': 'seg044',
        **bound(output), 'source_start_frame': 0, 'output_frames': p['master_frames'], 'frames': 343,
        'master': p['bindings']['master'], 'exact_narration': bound(narration), 'plan': bound(PLAN),
        'root_selection': bound(DECISION), 'verification': bound(F/'VERIFY.json'), 'conform': bound(F/'CONFORM.json'),
        'technical_complete': True, 'owner_accepted': False, 'lip_sync_approved': False,
        'parts_used': ['P08r3a','P08r3b'], 'review_limits': p['review_limits'], 'release_approved': False})
    print(json.dumps({'status': verification['status'], 'output': bound(output), 'verification': bound(F/'VERIFY.json')}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check','render'])
    parser.add_argument('--decision-sha256')
    args = parser.parse_args()
    p, paths, raw = checked_plan()
    if args.action == 'check':
        print(json.dumps({'status': 'prepared_inputs_verified', 'frames': 343, 'master_samples': 686000,
                          'decision_exists': DECISION.exists(), 'plan': bound(PLAN), 'owner_accepted': False}, indent=2))
        return
    decision = checked_decision(p, args.decision_sha256)
    render(p, paths, raw, decision)


if __name__ == '__main__':
    main()
