"""Offline, descriptive performance comparison. No provider calls or automatic approval.

Use the existing syncenv Python (cv2, mediapipe, numpy). Source/candidate are read-only.
All native frames are measured. Comparisons pair nearest presentation timestamps on
the source clock; they never stretch, align, interpolate, or modify either movie.
"""
import argparse
import csv
import datetime
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import cv2
import mediapipe as mp
import numpy as np


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def binding(path):
    return {'path': str(Path(path).resolve()), 'sha256': sha(path)}


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def number(value):
    return float(value) if value is not None and np.isfinite(value) else None


def probe(path):
    args = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate,avg_frame_rate,start_time,duration,nb_frames:format=duration:frame=best_effort_timestamp_time,pkt_duration_time,duration_time',
            '-show_frames', '-of', 'json', str(path)]
    raw = json.loads(subprocess.check_output(args))
    stream = raw['streams'][0]
    pts = np.array([float(f['best_effort_timestamp_time']) for f in raw['frames']])
    if len(pts) < 2 or np.any(np.diff(pts) <= 0):
        raise ValueError('Need strictly increasing decoded video PTS: ' + str(path))
    delta = np.diff(pts)
    last = raw['frames'][-1]
    tail = float(last.get('duration_time', last.get('pkt_duration_time', np.median(delta))))
    if tail <= 0:
        tail = float(np.median(delta))
    return {'stream': stream, 'format_duration_s': float(raw['format']['duration']),
            'decoded_frames': len(pts), 'first_pts_s': float(pts[0]),
            'decoded_picture_span_s': float(pts[-1] - pts[0] + tail),
            'median_frame_step_s': float(np.median(delta)),
            'min_frame_step_s': float(delta.min()), 'max_frame_step_s': float(delta.max()),
            'pts_relative_s': (pts - pts[0]).tolist()}


def pair_timestamps(source_pts, candidate_pts, candidate_span):
    """Nearest actual native frame, earlier one on a tie; -1 outside coverage."""
    pairs = []
    for t in source_pts:
        if t < 0 or t >= candidate_span - 1e-9:
            pairs.append(-1)
            continue
        right = int(np.searchsorted(candidate_pts, t))
        options = [i for i in (right - 1, right) if 0 <= i < len(candidate_pts)]
        pairs.append(min(options, key=lambda i: (abs(candidate_pts[i] - t), i)))
    return np.array(pairs, dtype=int)


def landmarks(result, attribute, count, visibility=False):
    obj = getattr(result, attribute)
    out = np.full((count, 3 if visibility else 2), np.nan, np.float32)
    if obj:
        for i, point in enumerate(obj.landmark[:count]):
            out[i] = [point.x, point.y, point.visibility] if visibility else [point.x, point.y]
    return out


def head_angles(face, width, height):
    # Approximate uncalibrated PnP orientation; useful only as a relative proxy.
    ids = [1, 152, 33, 263, 61, 291]
    if not np.isfinite(face[ids]).all():
        return np.full(3, np.nan)
    object_points = np.array([[0, 0, 0], [0, -330, -65], [-225, 170, -135],
                              [225, 170, -135], [-150, -150, -125], [150, -150, -125]], dtype=float)
    pixels = face[ids].astype(float) * [width, height]
    camera = np.array([[width, 0, width / 2], [0, width, height / 2], [0, 0, 1]], dtype=float)
    ok, rotation, _ = cv2.solvePnP(object_points, pixels, camera, np.zeros((4, 1)), flags=cv2.SOLVEPNP_ITERATIVE)
    if not ok:
        return np.full(3, np.nan)
    matrix, _ = cv2.Rodrigues(rotation)
    return np.array(cv2.RQDecomp3x3(matrix)[0])


def track(path, metadata, prefix):
    frames = metadata['decoded_frames']
    face = np.full((frames, 468, 2), np.nan, np.float32)
    pose = np.full((frames, 33, 3), np.nan, np.float32)
    left = np.full((frames, 21, 2), np.nan, np.float32)
    right = left.copy()
    angles = np.full((frames, 3), np.nan, np.float32)
    capture = cv2.VideoCapture(str(path))
    detector = mp.solutions.holistic.Holistic(static_image_mode=False, model_complexity=1,
        smooth_landmarks=False, enable_segmentation=False, refine_face_landmarks=False,
        min_detection_confidence=0.5, min_tracking_confidence=0.5)
    i = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if i >= frames:
                raise RuntimeError('OpenCV decode has more frames than ffprobe')
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            detected = detector.process(rgb)
            face[i] = landmarks(detected, 'face_landmarks', 468)
            pose[i] = landmarks(detected, 'pose_landmarks', 33, True)
            left[i] = landmarks(detected, 'left_hand_landmarks', 21)
            right[i] = landmarks(detected, 'right_hand_landmarks', 21)
            angles[i] = head_angles(face[i], frame.shape[1], frame.shape[0])
            i += 1
            if i % 120 == 0:
                print(f'{prefix}: measured {i}/{frames}', flush=True)
    finally:
        capture.release()
        detector.close()
    if i != frames:
        raise RuntimeError(f'{prefix}: decoded {i}, ffprobe reports {frames}; no assumed mapping')
    return {'face': face, 'pose': pose, 'left_hand': left, 'right_hand': right,
            'head_angles': angles, 'pts': np.array(metadata['pts_relative_s'])}


def features(traces, width, height):
    f, p = traces['face'].astype(float), traces['pose'].astype(float)
    # Pixel-isotropic coordinates / image width; avoid distorted aspect-ratio ratios.
    aspect = np.array([1, height / width])
    fi = f * aspect
    distance = lambda a, b: np.linalg.norm(fi[:, a] - fi[:, b], axis=1)
    eye = distance(33, 263)
    eye[eye < 1e-6] = np.nan
    shoulder = np.linalg.norm((p[:, 11, :2] - p[:, 12, :2]) * aspect, axis=1)
    shoulder[shoulder < 1e-6] = np.nan
    center = (p[:, 11, :2] + p[:, 12, :2]) / 2
    shoulder_visible = (p[:, 11, 2] >= .5) & (p[:, 12, 2] >= .5)
    shoulder[~shoulder_visible] = np.nan
    center[~shoulder_visible] = np.nan
    out = {'mouth_aperture': distance(13, 14) / eye,
           'mouth_width': distance(61, 291) / eye,
           'left_eye_aperture': distance(159, 145) / eye,
           'right_eye_aperture': distance(386, 374) / eye,
           'left_brow_height': (fi[:, 159, 1] - fi[:, 70, 1]) / eye,
           'right_brow_height': (fi[:, 386, 1] - fi[:, 300, 1]) / eye,
           'interocular_width_fraction': eye}
    for axis, label in enumerate(['x', 'y']):
        out['face_center_' + label] = (f[:, 33, axis] + f[:, 263, axis]) / 2
        out['nose_' + label] = f[:, 1, axis]
        out['shoulder_center_' + label] = center[:, axis]
    for axis, label in enumerate(['pitch', 'yaw', 'roll']):
        angles = traces['head_angles'][:, axis].astype(float).copy()
        valid_indices = np.flatnonzero(np.isfinite(angles))
        for group in np.split(valid_indices, np.where(np.diff(valid_indices) > 1)[0] + 1):
            if len(group):
                angles[group] = np.rad2deg(np.unwrap(np.deg2rad(angles[group])))
        out['head_' + label + '_deg'] = angles
    for name, idx in [('left_wrist', 15), ('right_wrist', 16), ('left_elbow', 13), ('right_elbow', 14)]:
        valid = p[:, idx, 2] >= 0.5
        for axis, label in enumerate(['x', 'y']):
            out[name + '_' + label] = np.where(valid, p[:, idx, axis], np.nan)
            out[name + '_body_relative_' + label] = np.where(valid, (p[:, idx, axis] - center[:, axis]) * aspect[axis] / shoulder, np.nan)
    return out


def summary(values):
    v = np.asarray(values)
    v = v[np.isfinite(v)]
    return {'count': len(v), 'median': number(np.median(v)) if len(v) else None,
            'p95': number(np.percentile(v, 95)) if len(v) else None,
            'max': number(v.max()) if len(v) else None}


def lag_comparison(source, candidate, max_lag, step):
    candidates = []
    for lag in range(-max_lag, max_lag + 1):
        a, b = (source[:-lag], candidate[lag:]) if lag > 0 else ((source[-lag:], candidate[:lag]) if lag < 0 else (source, candidate))
        keep = np.isfinite(a) & np.isfinite(b)
        if keep.sum() < max(12, int(round(1 / step))):
            continue
        a, b = a[keep], b[keep]
        if a.std() <= 1e-5 or b.std() <= 1e-5:
            continue
        candidates.append({'lag_source_frames': lag, 'lag_seconds': round(lag * step, 6),
                           'correlation': float(np.corrcoef(a, b)[0, 1]), 'paired_samples': len(a)})
    if not candidates:
        return {'status': 'insufficient_overlap_or_motion', 'best': None, 'zero_lag': None}
    best = max(candidates, key=lambda x: (x['correlation'], -abs(x['lag_source_frames'])))
    return {'status': 'descriptive_only', 'best': best,
            'zero_lag': next((x for x in candidates if x['lag_source_frames'] == 0), None),
            'all_lags': candidates}


def selected_frames(path, indices):
    wanted = set(indices)
    capture = cv2.VideoCapture(str(path))
    found, i = {}, 0
    try:
        while wanted:
            ok, frame = capture.read()
            if not ok:
                break
            if i in wanted:
                found[i] = frame
                wanted.remove(i)
            i += 1
    finally:
        capture.release()
    if wanted:
        raise RuntimeError('Could not decode representative frame indices: ' + str(wanted))
    return found


def panel(image, label, width=480, height=270):
    canvas = np.zeros((height + 36, width, 3), np.uint8)
    scale = min(width / image.shape[1], height / image.shape[0])
    small = cv2.resize(image, (round(image.shape[1] * scale), round(image.shape[0] * scale)))
    x, y = (width - small.shape[1]) // 2, (height - small.shape[0]) // 2
    canvas[y:y + small.shape[0], x:x + small.shape[1]] = small
    cv2.putText(canvas, label, (8, height + 24), cv2.FONT_HERSHEY_SIMPLEX, .43, (240, 240, 240), 1, cv2.LINE_AA)
    return canvas


def self_test():
    for fps in (24, 25, 30):
        source, candidate = np.arange(288) / 24, np.arange(12 * fps) / fps
        pairs = pair_timestamps(source, candidate, 12)
        assert len(pairs) == 288 and (pairs >= 0).all()
        assert np.max(np.abs(candidate[pairs] - source)) <= .5 / fps + 1e-9
    assert pair_timestamps(np.array([0, 1, 2]), np.array([0, 1]), 2).tolist() == [0, 1, -1]
    rng = np.random.default_rng(42)
    source = rng.normal(size=288)
    delayed = np.r_[np.full(5, np.nan), source[:-5]]
    assert lag_comparison(source, delayed, 18, 1 / 24)['best']['lag_source_frames'] == 5
    assert lag_comparison(np.ones(50), np.ones(50), 5, 1 / 24)['best'] is None
    print('Self-tests passed: timestamp pairing at24/25/30fps; coverage; lag sign; static-signal refusal.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--source-sha256')
    parser.add_argument('--candidate-sha256')
    parser.add_argument('--contact-count', type=int, default=12)
    parser.add_argument('--lag-seconds', type=float, default=.75)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not all([args.source, args.candidate, args.out, args.source_sha256]):
        parser.error('--source, --candidate, --out and --source-sha256 are required')
    if not 2 <= args.contact_count <= 24 or not 0 <= args.lag_seconds <= 2:
        parser.error('contact-count must be2..24; lag-seconds0..2')
    source, candidate, out = args.source.resolve(), args.candidate.resolve(), args.out.resolve()
    sb, cb = binding(source), binding(candidate)
    if sb['sha256'] != args.source_sha256 or (args.candidate_sha256 and cb['sha256'] != args.candidate_sha256):
        raise RuntimeError('Input hash does not match the requested immutable source/candidate')
    if out.exists() and any(out.iterdir()):
        raise RuntimeError('Output directory is not empty; use a new QA revision')
    if source.is_relative_to(out) or candidate.is_relative_to(out):
        raise RuntimeError('Inputs must live outside the output directory')
    out.mkdir(parents=True, exist_ok=True)
    source_meta, candidate_meta = probe(source), probe(candidate)
    write_json(out / 'SOURCE-PROBE.json', source_meta)
    write_json(out / 'CANDIDATE-PROBE.json', candidate_meta)
    s = track(source, source_meta, 'source')
    c = {k: v.copy() for k, v in s.items()} if sb['sha256'] == cb['sha256'] else track(candidate, candidate_meta, 'candidate')
    np.savez_compressed(out / 'source-trajectories.npz', **s)
    np.savez_compressed(out / 'candidate-trajectories.npz', **c)
    pairs = pair_timestamps(s['pts'], c['pts'], candidate_meta['decoded_picture_span_s'])
    valid = pairs >= 0
    safe = np.maximum(pairs, 0)
    paired = {k: v[safe].astype(float) for k, v in c.items() if k != 'pts'}
    for v in paired.values():
        v[~valid] = np.nan
    sf = features(s, source_meta['stream']['width'], source_meta['stream']['height'])
    cf = features(paired, candidate_meta['stream']['width'], candidate_meta['stream']['height'])
    differences, temporal = {}, {}
    step = source_meta['median_frame_step_s']
    regular_source_clock = source_meta['max_frame_step_s'] - source_meta['min_frame_step_s'] < 1e-5
    for name in sf:
        delta = cf[name] - sf[name]
        if name.endswith('_deg'):
            delta = (delta + 180) % 360 - 180
        differences[name] = {'absolute_error': summary(np.abs(delta)),
                             'source_std': number(np.nanstd(sf[name])) if np.isfinite(sf[name]).any() else None,
                             'candidate_std': number(np.nanstd(cf[name])) if np.isfinite(cf[name]).any() else None}
        temporal[name] = lag_comparison(sf[name], cf[name], round(args.lag_seconds / step), step) if regular_source_clock else {'status': 'disabled_for_irregular_source_clock'}
    geometry = {}
    for name, ids in [('face', np.arange(468)), ('left_hand', np.arange(21)), ('right_hand', np.arange(21))]:
        distance = np.linalg.norm((paired[name][:, ids] - s[name][:, ids]) * [100, 100], axis=2)
        geometry[name + '_landmark_displacement_percent_of_axes'] = summary(distance)
        if name.endswith('hand'):
            sa, ca = s[name].astype(float), paired[name]
            sp = np.linalg.norm(sa[:, 9] - sa[:, 0], axis=1)
            cp = np.linalg.norm(ca[:, 9] - ca[:, 0], axis=1)
            sp[sp < 1e-6] = np.nan
            cp[cp < 1e-6] = np.nan
            a = (sa - sa[:, 0:1]) / sp[:, None, None]
            b = (ca - ca[:, 0:1]) / cp[:, None, None]
            geometry[name + '_wrist_relative_shape_error_palm_units'] = summary(np.linalg.norm(b - a, axis=2))
    coverage = {}
    for name in ['face', 'left_hand', 'right_hand']:
        coverage[name] = {'source_detected_frames': int(np.isfinite(s[name][:, 0, 0]).sum()),
                          'candidate_detected_native_frames': int(np.isfinite(c[name][:, 0, 0]).sum()),
                          'paired_detected_frames': int((np.isfinite(s[name][:, 0, 0]) & np.isfinite(paired[name][:, 0, 0])).sum())}
    frame_rows = []
    for i, j in enumerate(pairs):
        row = {'source_frame': i, 'source_time_s': float(s['pts'][i]), 'candidate_frame': int(j),
               'candidate_time_s': float(c['pts'][j]) if j >= 0 else None,
               'candidate_minus_source_sampling_ms': float((c['pts'][j] - s['pts'][i]) * 1000) if j >= 0 else None}
        for name in sf:
            row['source_' + name], row['candidate_' + name] = number(sf[name][i]), number(cf[name][i])
        frame_rows.append(row)
    with (out / 'PAIRED-TRAJECTORIES.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(frame_rows[0]))
        writer.writeheader()
        writer.writerows(frame_rows)
    write_json(out / 'FRAME-PAIRS.json', [{k: v for k, v in row.items() if k in ['source_frame', 'source_time_s', 'candidate_frame', 'candidate_time_s', 'candidate_minus_source_sampling_ms']} for row in frame_rows])
    uniform = np.linspace(0, len(pairs) - 1, args.contact_count).round().astype(int).tolist()
    # Add maximum observed face/wrist error frames as descriptive inspection targets.
    extras = []
    for names in [('face_center_x', 'face_center_y'), ('left_wrist_x', 'left_wrist_y'), ('right_wrist_x', 'right_wrist_y')]:
        error = sum((cf[n] - sf[n]) ** 2 for n in names)
        if np.isfinite(error).any():
            extras.append(int(np.nanargmax(error)))
    chosen = sorted(set(i for i in uniform + extras if pairs[i] >= 0))
    source_images = selected_frames(source, chosen)
    candidate_images = selected_frames(candidate, [int(pairs[i]) for i in chosen])
    visual_records = []
    visual_dir = out / 'paired-frames'
    visual_dir.mkdir()
    sheet_rows = []
    for i in chosen:
        j, a, b = int(pairs[i]), source_images[i], candidate_images[int(pairs[i])]
        resized = cv2.resize(b, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_AREA)
        difference = cv2.absdiff(a, resized)
        row = np.hstack([panel(a, f'SOURCE f{i}  t={s["pts"][i]:.4f}s'),
                         panel(b, f'CAND f{j}  t={c["pts"][j]:.4f}s'),
                         panel(difference, 'ABS PIXEL DIFF - look changes dominate')])
        filename = visual_dir / f'source-{i:04d}_candidate-{j:04d}.jpg'
        cv2.imwrite(str(filename), row, [cv2.IMWRITE_JPEG_QUALITY, 94])
        sheet_rows.append(row)
        visual_records.append({'source_frame': i, 'candidate_frame': j, 'image': binding(filename),
                               'selection_reason': 'uniform' if i in uniform else 'maximum_observed_landmark_difference'})
    for i in range(0, len(sheet_rows), 4):
        cv2.imwrite(str(out / f'contact-{i // 4 + 1:02d}.jpg'), np.vstack(sheet_rows[i:i + 4]), [cv2.IMWRITE_JPEG_QUALITY, 92])
    sampling = [abs(row['candidate_minus_source_sampling_ms']) for row in frame_rows if row['candidate_frame'] >= 0]
    report = {'schema': 'ep009.performance-comparison.v1', 'status': 'metrics_only_review_required',
        'owner_accepted': False, 'automatic_approval': False,
        'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source': sb, 'candidate': cb,
        'script': binding(Path(__file__)), 'runtime': {'python': sys.version, 'opencv': cv2.__version__, 'mediapipe': mp.__version__, 'numpy': np.__version__},
        'time_comparison': {'source_native_frames': len(s['pts']), 'candidate_native_frames': len(c['pts']),
            'source_nominal_fps': source_meta['stream']['r_frame_rate'], 'candidate_nominal_fps': candidate_meta['stream']['r_frame_rate'],
            'source_picture_duration_s': source_meta['decoded_picture_span_s'], 'candidate_picture_duration_s': candidate_meta['decoded_picture_span_s'],
            'duration_difference_s': candidate_meta['decoded_picture_span_s'] - source_meta['decoded_picture_span_s'],
            'first_pts_difference_s': candidate_meta['first_pts_s'] - source_meta['first_pts_s'],
            'unmatched_source_frames': np.flatnonzero(~valid).tolist(), 'nearest_frame_sampling_error_abs_ms': summary(sampling),
            'source_clock_regular': regular_source_clock, 'mapping': 'Actual source-frame times; candidate nearest PTS; both origins normalized to first presented frame. No time shift, stretch, or interpolation.'},
        'detection_coverage': coverage, 'feature_differences': differences, 'landmark_geometry': geometry,
        'temporal_lag_diagnostics': temporal, 'lag_sign': 'Positive means candidate movement occurs later: source(t) compared with candidate(t+lag). This diagnosis does not realign the comparison.',
        'representative_frames': visual_records,
        'data': {p.name: binding(p) for p in [out/'SOURCE-PROBE.json', out/'CANDIDATE-PROBE.json', out/'source-trajectories.npz', out/'candidate-trajectories.npz', out/'PAIRED-TRAJECTORIES.csv', out/'FRAME-PAIRS.json']},
        'limitations': ['Descriptive detector proxies only; no thresholds or automatic approval. Inspect actual paired frames and normal-speed video.',
            'Wardrobe, lighting, occlusion, camera geometry and generative artifacts can change detector estimates. Missing detection is not missing motion.',
            'Face/pose x/y use image-width/height fractions. Head orientation is uncalibrated PnP, not physical motion capture.',
            'Handedness is anatomical detector labeling, not screen-left/right. Occlusion or crossing may produce label errors.',
            'Raw pixel differences are dominated by intentional clothing/background edits and are not a quality or preservation score.',
            'Expression ratios, eyelids and mouth aperture do not certify identity, emotion, spoken phonemes or lip sync.',
            'Lag correlation can peak spuriously for periodic, low-amplitude or short gestures. All lags and zero-lag results are retained; no correction is applied.',
            'Different frame rates create nearest-frame sampling error, explicitly reported. Duration/fps differences are not silently conformed.',
            'The candidate audio is not inspected or adopted. Original episode narration remains authoritative.']}
    write_json(out / 'PERFORMANCE-COMPARISON.json', report)
    print(json.dumps({'status': report['status'], 'report': binding(out / 'PERFORMANCE-COMPARISON.json'), 'coverage': coverage, 'duration_difference_s': report['time_comparison']['duration_difference_s']}))


if __name__ == '__main__':
    main()
