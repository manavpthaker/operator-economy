#!/usr/bin/env python3
"""Root-run verification-only resume for the exact already-rendered R76 files.

Never renders or modifies MP4/WAV/source files. Preserves the initial assembler's
five near-uniform flags, then classifies only the inspected, hash-bound inherited
P2 crossfade. Any other near-uniform frame remains a failure.
"""
from pathlib import Path
import ast
import importlib.util
import json
import math

OWN = Path(__file__).resolve().parent
ASSEMBLER = OWN / 'assemble_review.py'
ASSEMBLER_SHA = '034221d56b581c1a0c9e30ae5ae237ac3559c45ca32f35c8beb0facb57f53ffc'
spec = importlib.util.spec_from_file_location('r76_assembly_helpers', ASSEMBLER)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
assert a.sha(ASSEMBLER) == ASSEMBLER_SHA
SCENE = a.H / 'qa/s17-c.mp4'
CONTEXT = a.C / 'qa/context.mp4'
SCENE_SHA = '3b9229f61825add2b5ddd30d015f495c0f3cd6ad6c2e5b92655a7cba0fb81431'
CONTEXT_SHA = 'a10d322cc96198642be1b74edc3f3207b10c5f439fe10124f8cd5aa0d65bc7df'
ALLOWED = list(range(1444, 1449))


def sd(row):
    mean = sum(row) / len(row)
    return math.sqrt(max(0, sum(x * x for x in row) / len(row) - mean * mean))


def gray(path, select=None):
    filters = ('select=' + select + ',setpts=N/24/TB,' if select else '')
    return a.run(['ffmpeg', '-v', 'error', '-xerror', '-err_detect', 'explode',
                  '-i', str(path), '-an', '-vf', filters + 'scale=64:36,format=gray',
                  '-f', 'rawvideo', '-'])


def inspect_context():
    info = a.require_video(CONTEXT, 1803, (1280, 720))
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    assert (int(audio['sample_rate']), audio['channels']) == (48000, 2)
    assert abs(float(a.video_stream(info)['duration']) - 75.125) < 1 / 24000
    raw = gray(CONTEXT)
    assert len(raw) == 1803 * 2304
    deviations = [sd(raw[n * 2304:(n + 1) * 2304]) for n in range(1803)]
    flagged = [n for n, value in enumerate(deviations) if value <= 3]
    assert flagged == ALLOWED, ('Unexpected near-uniform flags; no general exemption', flagged)
    reference = gray(a.P2, 'between(n\\,349\\,353)')
    assert len(reference) == 5 * 2304
    comparisons = []
    for index, frame in enumerate(ALLOWED):
        source = reference[index * 2304:(index + 1) * 2304]
        candidate = raw[frame * 2304:(frame + 1) * 2304]
        difference = sum(abs(x - y) for x, y in zip(source, candidate)) / 2304
        roi = b''.join(candidate[row * 64 + 25:row * 64 + 39] for row in range(13, 25))
        assert difference < .25, ('Inherited frame changed materially', frame, difference)
        assert sd(roi) > 3 and max(roi) - min(roi) >= 12, ('House region lacks inspected content', frame)
        comparisons.append({'source_frame': frame - 1095, 'context_frame': frame,
                            'source_sd': sd(source), 'context_sd': deviations[frame],
                            'source_context_mean_absolute_gray_difference': difference,
                            'house_roi_sd': sd(roi), 'house_roi_gray_range': max(roi) - min(roi)})
    return {'path': a.relative(CONTEXT), 'sha256': a.sha(CONTEXT),
            'frames': 1803, 'duration': 75.125, 'full_decode_pass': True,
            'near_uniform_frames': len(flagged), 'near_uniform_frame_indices': flagged,
            'minimum_frame_sd': min(deviations), 'unresolved_blank_frame_candidates': 0,
            'blank_scan': 'Every decoded frame at64x36 gray; SD<=3 flags retained. Only exact hash-bound inherited P2 frames349–353 classified after visual/source comparison.',
            'classified_false_positive': {
                'reason': 'Sparse house and label remain visible during an authored overlapping crossfade; full-canvas variance falls below the general heuristic.',
                'source_path': a.relative(a.P2), 'source_sha256': a.FIXED_PINS[a.P2],
                'source_frames': list(range(349, 354)), 'context_frames': flagged,
                'house_roi_at_64x36': {'x': [25, 39], 'y': [13, 25]},
                'frame_comparisons': comparisons},
            **a.compare_audio(CONTEXT, 0, 736.875, 75.125), 'probe': info}


def main():
    for path, expected in a.FIXED_PINS.items():
        assert a.sha(path) == expected, str(path)
    assert a.sha(SCENE) == SCENE_SHA and a.sha(CONTEXT) == CONTEXT_SHA
    alignment = json.loads(a.ALIGNMENT.read_text())
    alignment_sha = a.sha(a.ALIGNMENT)
    restored_sha = a.sha(a.RESTORED)
    assert alignment['selected_source_in_frame'] == 8
    if 'source_sha256' in alignment:
        assert alignment['source_sha256'] == restored_sha
    if 'original_audio_sha256' in alignment:
        assert alignment['original_audio_sha256'] == a.FIXED_PINS[a.REFERENCE]
    hqa, cqa = a.H / 'qa', a.C / 'qa'
    generated = [hqa / 'VERIFICATION.json', cqa / 'VERIFICATION.json', a.C / 'index.html',
                 hqa / 'encoded-contact.png', hqa / 'seam-contact.png',
                 hqa / 'encoded-0.png', hqa / 'encoded-96.png', hqa / 'encoded-191.png']
    assert not [str(p) for p in generated if p.exists()], 'Refuse to overwrite review artifacts'
    scene_pcm = a.read_master_pcm(37176000, 384000)
    context_pcm = a.read_master_pcm(35370000, 3606000)
    pcm = {'provider_reference': a.verify_pcm(a.REFERENCE, scene_pcm),
           'scene': a.verify_pcm(hqa / 's17-c-source.wav', scene_pcm),
           'context': a.verify_pcm(cqa / 'context-source.wav', context_pcm)}
    scene_report = a.inspect(SCENE, 774.5, 192)
    context_report = inspect_context()
    presenter_audio = a.compare_audio(CONTEXT, 37.625, 774.5, 8.0)
    sheets = [a.contact(CONTEXT, [0, 191, 192, 804, 901, 902, 903, 904,
                                  951, 999, 1047, 1093, 1094, 1095, 1096, 1802],
                        hqa / 'encoded-contact.png', 2),
              a.contact(CONTEXT, [902, 903, 904, 1094, 1095, 1096],
                        hqa / 'seam-contact.png', 3)]
    for n in [0, 96, 191]:
        target = hqa / f'encoded-{n}.png'
        a.run(['ffmpeg', '-n', '-v', 'error', '-i', str(SCENE), '-vf',
               f'select=eq(n\\,{n})', '-frames:v', '1', '-update', '1', str(target)])
        sheets.append({'path': a.relative(target), 'sha256': a.sha(target),
                       'source_path': a.relative(SCENE), 'frames': [n], 'native_resolution': [1280, 720]})
    # Reuse exactly the reviewed, immutable assembler's self-contained player.
    tree = ast.parse(ASSEMBLER.read_text())
    player_nodes = [node.value for node in ast.walk(tree) if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'player' for t in node.targets)]
    assert len(player_nodes) == 1
    a.fresh_write(a.C / 'index.html', ast.literal_eval(player_nodes[0]))
    evidence = OWN / 'inherited-transition-evidence.json'
    report = {
        'status': 'technical_pass_owner_review_pending',
        'source_pcm_bit_exact': True, 'source_prefix_pcm_bit_exact': True,
        'preserved_source_samples': 384000, 'context_source_samples': 3606000,
        'appended_zero_samples': 0, 'padding_seconds': 0,
        'strict_check': None, 'strict_check_note': 'FFmpeg review assembly; no new HyperFrames source.',
        'runtime': 'ffmpeg verification-only resume', 'source_sha256': restored_sha,
        'selected_source_in_frame': 8, 'selected_source_out_frame_exclusive': 200,
        'alignment': {'path': a.relative(a.ALIGNMENT), 'sha256': alignment_sha,
                      'source_hash_explicit_in_alignment': 'source_sha256' in alignment},
        'fixed_inputs': [{'path': a.relative(p), 'sha256': digest} for p, digest in a.FIXED_PINS.items()],
        'source_pcm': pcm, 'scene': scene_report, 'context': context_report,
        'context_presenter_audio': presenter_audio,
        'seams': {'s17_start_frame': 192, 'presenter_start_frame': 903,
                  'presenter_end_frame_exclusive': 1095, 'review_initial_time_seconds': 33.5},
        'contact_sheets_and_native_stills': sheets,
        'review_player': {'path': a.relative(a.C / 'index.html'), 'sha256': a.sha(a.C / 'index.html')},
        'assembler': {'path': a.relative(ASSEMBLER), 'sha256': ASSEMBLER_SHA},
        'verifier': {'path': a.relative(Path(__file__).resolve()), 'sha256': a.sha(Path(__file__).resolve())},
        'inherited_transition_evidence': {'path': a.relative(evidence), 'sha256': a.sha(evidence)},
        'initial_scan_finding_preserved': 'Five near-uniform flags are retained and narrowly classified as inherited sparse-graphic false positives; no frames or media changed.',
        'commands': a.COMMANDS,
        'limits': ['No owner acceptance, canonical conform or release.',
                   'Audio metrics do not establish perceptual lip sync or performance quality.',
                   'Source PCM is exact; encoded AAC is lossy.',
                   'Five documented near-uniform inherited frames remain counted; no blanket blank-scan exception.',
                   'No MP4, WAV or accepted source was rewritten by this verification-only resume.']}
    assert a.sha(SCENE) == SCENE_SHA and a.sha(CONTEXT) == CONTEXT_SHA
    assert a.sha(a.ALIGNMENT) == alignment_sha and a.sha(a.RESTORED) == restored_sha
    for path, expected in a.FIXED_PINS.items():
        assert a.sha(path) == expected, str(path)
    a.save(hqa / 'VERIFICATION.json', report)
    a.save(cqa / 'VERIFICATION.json', report)
    print(json.dumps({'status': report['status'], 'scene_frames': 192,
                      'context_frames': 1803, 'inherited_false_positive_flags': ALLOWED,
                      'scene_sha256': SCENE_SHA, 'context_sha256': CONTEXT_SHA,
                      'review_player': a.relative(a.C / 'index.html')}, indent=2))


if __name__ == '__main__':
    main()
