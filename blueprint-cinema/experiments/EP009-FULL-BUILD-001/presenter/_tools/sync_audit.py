"""Measure lip-sync offset per presenter clip: mouth opening vs audio loudness.

For each clip, per frame: inner-lip gap (face landmarks 13/14) normalised by face
height, and audio RMS at 24 fps. Both are smoothed and differenced into "opening
velocity" and "loudness rise" signals, then cross-correlated over lags of
+-20 frames in overlapping 3 s windows. A positive lag means the picture is
LATE (mouth moves after the sound); negative means the picture LEADS.

Usage: sync_audit.py <clip.mp4> [<clip.mp4> ...] --json out.json
"""
import json, subprocess, sys, pathlib
import numpy as np, cv2
import mediapipe as mp

FPS = 24
MAXLAG = 20
WIN, HOP = 72, 24


def mouth_series(path):
    fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=False)
    cap = cv2.VideoCapture(path)
    out = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        r = fm.process(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
        if r.multi_face_landmarks:
            p = r.multi_face_landmarks[0].landmark
            face_h = abs(p[152].y - p[10].y) or 1e-6
            out.append(abs(p[14].y - p[13].y) / face_h)
        else:
            out.append(np.nan)
    cap.release()
    return np.array(out)


def audio_series(path, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float64)
    spf = 2000
    frames = min(n, len(a) // spf)
    rms = np.array([np.sqrt(np.mean(a[k * spf:(k + 1) * spf] ** 2)) for k in range(frames)])
    return np.log1p(rms)


def smooth(x, k=3):
    x = np.where(np.isnan(x), np.nanmean(x), x)
    return np.convolve(x, np.ones(k) / k, mode="same")


def best_lag(v, a):
    best, bc = 0, -2
    for lag in range(-MAXLAG, MAXLAG + 1):
        if lag >= 0:
            vv, aa = v[lag:], a[:len(a) - lag]
        else:
            vv, aa = v[:lag], a[-lag:]
        m = min(len(vv), len(aa))
        if m < 24:
            continue
        vv, aa = vv[:m], aa[:m]
        if vv.std() < 1e-9 or aa.std() < 1e-9:
            continue
        c = float(np.corrcoef(vv, aa)[0, 1])
        if c > bc:
            bc, best = c, lag
    return best, bc


def audit(path):
    m = mouth_series(path)
    a = audio_series(path, len(m))
    n = min(len(m), len(a))
    m, a = smooth(m[:n]), smooth(a[:n])
    v = np.diff(m, prepend=m[0])
    da = np.diff(a, prepend=a[0])
    whole = best_lag(m, a)
    h = n // 2
    first = best_lag(m[:h], a[:h]) if h >= 48 else (None, None)
    second = best_lag(m[h:], a[h:]) if n - h >= 48 else (None, None)
    windows = []
    for s in range(0, max(1, n - WIN + 1), HOP):
        lag, c = best_lag(v[s:s + WIN], da[s:s + WIN])
        windows.append({"start_s": round(s / FPS, 2), "lag_frames": lag, "corr": round(c, 3)})
    good = [w["lag_frames"] for w in windows if w["corr"] >= 0.35]
    return {"clip": path, "frames": int(n), 
            "whole_level_lag_frames": whole[0], "whole_level_corr": round(whole[1], 3),
            "first_half_lag_frames": first[0], "second_half_lag_frames": second[0],
            "window_median_lag_frames": (int(np.median(good)) if good else None),
            "window_lag_spread_frames": (int(np.max(good) - np.min(good)) if len(good) > 1 else None),
            "confident_windows": len(good), "windows": windows}


if __name__ == "__main__":
    args = sys.argv[1:]
    out = None
    if "--json" in args:
        out = args[args.index("--json") + 1]
        args = args[:args.index("--json")]
    res = []
    for p in args:
        r = audit(p)
        res.append(r)
        print(f"{p}: level lag {r['whole_level_lag_frames']:+d}f (c {r['whole_level_corr']}), "
              f"halves {r['first_half_lag_frames']}/{r['second_half_lag_frames']}", flush=True)
    if out:
        pathlib.Path(out).write_text(json.dumps(res, indent=1))
