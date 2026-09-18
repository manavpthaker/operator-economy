"""Exact source slices for the bounded seg059 room repair. Storage only."""
import csv
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[1]
R = T.parents[3]
D = T / 'room-repair-seg059-r2'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def bound(path): return {'path': str(path.relative_to(R)), 'sha256': sha(path)}
def read(path): return json.loads(path.read_text())
def save(path, data):
    with path.open('x') as f: json.dump(data, f, indent=2); f.write('\n')
def run(args): return subprocess.check_output(args)
def pcm(path):
    return run(['ffmpeg', '-nostdin', '-v', 'error', '-threads', '1', '-i', str(path), '-map', '0:a:0', '-f', 'f32le', '-c:a', 'pcm_f32le', '-'])

def main():
    D.mkdir(exist_ok=False)
    m = module('review', T / '_tools/build_review.py')
    source = T / 'wardrobe-guarded-r2/seg059/native.mp4'
    assert sha(source) == 'ed8f11aba7404bd38a0f128d17d74890099f3a050fdc8c4031fef0a10b2d171f'
    before = m.video_hashes(source, 161)
    source_audio = pcm(source)
    assert len(source_audio) % 8 == 0
    source_samples = len(source_audio) // 8
    save(D / 'SOURCE-FRAME-HASHES.json', before)
    rows = []
    for sid, start, end, eligible, original in [
        ('seg059-close', 33, 161, 119, [33, 152]),
        ('seg059-wide', 0, 72, 33, [0, 33]),
    ]:
        count = end - start
        out = D / (sid + '-source.mov')
        expected_audio = source_audio[start * 2000 * 8:end * 2000 * 8]
        retained_samples = len(expected_audio) // 8
        assert retained_samples >= eligible * 2000
        padding = count * 2000 - retained_samples
        expected_audio += bytes(padding * 8)
        cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-threads', '1', '-i', str(source),
               '-filter_complex', f'[0:v]trim=start_frame={start}:end_frame={end},setpts=N/(24*TB)[v];[0:a]atrim=start_sample={start*2000}:end_sample={end*2000},asetpts=N/SR/TB,apad=whole_len={count*2000}[a]',
               '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '0', '-preset', 'medium', '-threads', '2',
               '-pix_fmt', 'yuv420p', '-r', '24', '-fps_mode', 'cfr', '-c:a', 'pcm_f32le', '-movflags', '+faststart', '-map_metadata', '-1', str(out)]
        run(cmd)
        frames = m.video_hashes(out, count)
        assert frames['hashes'] == before['hashes'][start:end]
        actual_audio = pcm(out)
        assert actual_audio == expected_audio
        hashes = D / (sid + '-FRAME-HASHES.json')
        save(hashes, frames)
        rows.append({'id': sid, 'segment': 'seg059', 'source': bound(source), 'source_frames': [start, end],
                     'input': bound(out), 'input_frames': count, 'input_duration_seconds': count / 24,
                     'select_local_frames': [0, eligible], 'original_segment_frames': original,
                     'output_frames': [23153 + original[0], 23153 + original[1]],
                     'master_audio_samples': [(23153 + original[0]) * 2000, (23153 + original[1]) * 2000],
                     'discarded_provider_input_frames': [eligible, count],
                     'disposable_tail_kind': 'existing returned terminal guard' if sid.endswith('close') else 'following source context, including source cut at local33',
                     'original_payload_exact_decoded_frames': True, 'frame_hashes': bound(hashes),
                     'source_audio_sample_count': source_samples, 'audio_samples': count * 2000,
                     'source_audio_samples_retained': retained_samples, 'audio_zero_padding_samples': padding,
                     'audio_f32le_stereo_sha256': hashlib.sha256(actual_audio).hexdigest(), 'audio_preservation': 'Exact decoded source samples; any zero padding is after the entire eligible interval. Conditioning audio only; episode master never replaced.',
                     'retime': False, 'resize': False, 'input_bytes': out.stat().st_size, 'encode_command': cmd})
        print(json.dumps({'id': sid, 'frames': count, 'sha256': sha(out), 'padding_samples': padding}), flush=True)
    plan = {'record_type': 'ep009_seg059_bounded_room_repair_sources', 'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status': 'verified_prepared_sources_only_no_generation', 'owner_accepted': False,
            'authority': 'Root instruction: prepare lossless wardrobe[33,161) selecting0..119 and if wide-prefix QA does not confirm, wardrobe[0,72) selecting0..33. Storage uploads only; parent owns paid production.',
            'helper': bound(Path(__file__)), 'source_audit': bound(T/'SOURCE-AUDIT.json'),
            'wardrobe_review': bound(T/'wardrobe-guarded-r2/seg059/qa/WARDROBE-REVIEW.json'),
            'failed_room_review': bound(T/'room-r1/seg059/qa-selected-r1/ROOM-REVIEW.json'),
            'wide_prefix_review': bound(T/'room-r1/seg059/qa-selected-r1/WIDE-PREFIX-REVIEW.json'),
            'source_download': bound(source.parent/'DOWNLOAD.json'),
            'master_audio': bound(T.parent/'assembly/r3/narration-master-r3.wav'),
            'source_frame_hashes': bound(D/'SOURCE-FRAME-HASHES.json'), 'slices': rows,
            'restrictions': ['No generated, reconstructed or retimed performance.', 'Only selected ranges may be conformed, preserving original cut33 and all152 frames.', 'Provider context and tail guards never enter final program.', 'Original failed room and all earlier artifacts remain unchanged.', 'The existing single-piece seg059 conform helper does not yet accept this two-piece repair; additive conform support required after new outputs are reviewed.']}
    save(D/'PLAN.json', plan)
    storage = module('storage', R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py')
    deliveries = []
    for row in rows:
        folder = D/row['id']; folder.mkdir()
        url = storage.upload(R/row['input']['path'], folder, 'video/quicktime')
        receipt = read(folder/'UPLOAD.json')
        assert receipt['status'] == 'verified' and receipt['sha256'] == row['input']['sha256']
        deliveries.append(dict(row, fal_url=url, upload_receipt=bound(folder/'UPLOAD.json')))
        print(json.dumps({'id': row['id'], 'storage_verified': True}), flush=True)
    save(D/'DELIVERY.json', {'record_type': 'ep009_seg059_room_repair_storage_delivery', 'plan': bound(D/'PLAN.json'), 'status': 'verified_storage_only', 'slices': deliveries})

if __name__ == '__main__': main()
