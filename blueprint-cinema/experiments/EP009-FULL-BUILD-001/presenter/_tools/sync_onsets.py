"""Which audio placement is each lip-synced file actually synced to?

For each take: narration speech onsets after pauses >= 0.25 s (from the take's
narration.wav). For every onset, the mouth-opening rise in restored.mp4 (first
frame after a closed stretch where the inner-lip gap rises above a threshold).
Report median (mouth_rise_frame - onset_frame) under placement A (narration at
restored sample L, as used in the build) and placement B (narration at 0).
Natural speech: the mouth starts opening 0-3 frames before the sound.
"""
import json, sys, subprocess, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import sync_audit as sa
P = "blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter"

def onsets(wav):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "48000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(float)
    hop = 480; e = np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0, len(a)-hop, hop)])
    thr = max(np.percentile(e, 20) * 3, np.max(e) * 0.06)
    loud = e > thr; out = []; quiet = 0
    for i, l in enumerate(loud):
        if not l: quiet += 1
        else:
            if quiet >= 25: out.append(i * hop / 48000.0)
            quiet = 0
    return out

def rises(m):
    m = sa.smooth(m, 3); closed = np.nanpercentile(m, 25); openv = np.nanpercentile(m, 70)
    thr = closed + 0.35 * (openv - closed); res = []
    for i in range(3, len(m)):
        if m[i] > thr and np.all(m[i-3:i] <= thr): res.append(i)
    return np.array(res)

for t in sys.argv[1:]:
    al = json.load(open(f"{P}/{t}/ALIGNMENT.json")); L = al["restored_audio_lag_samples"]
    ons = onsets(f"{P}/{t}/audio/narration.wav")
    r = rises(sa.mouth_series(f"{P}/{t}/restored.mp4"))
    res = {}
    for name, off in (("A_as_built", L / 48000.0), ("B_unshifted", 0.0)):
        d = []
        for o in ons:
            f = (o + off) * 24
            near = r[(r > f - 12) & (r < f + 12)]
            if len(near): d.append(float(near[np.argmin(np.abs(near - f))] - f))
        res[name] = (round(float(np.median(d)), 1) if d else None, len(d))
    print(f"{t}: L={L/2000:.1f}f onsets={len(ons)}  mouth-minus-sound median frames: as built {res['A_as_built']}  unshifted {res['B_unshifted']}", flush=True)
