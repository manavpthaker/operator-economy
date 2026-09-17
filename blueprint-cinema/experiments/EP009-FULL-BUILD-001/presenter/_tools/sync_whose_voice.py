"""Does the lip-synced mouth follow the narration, or the generator's own voice?

restored.mp4 keeps native-trim.mp4's frame timing. Correlate the restored mouth
opening against (a) restored.mp4's audio (the narration Fal was asked to sync to)
and (b) native-trim.mp4's audio (the video generator's own voice), best of +-4
frames each. If (b) wins clearly, the lip sync did not re-time the mouth.
"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import sync_audit as sa

def corr_near(m, a, k=4):
    best = -2
    for lag in range(-k, k + 1):
        vv, aa = (m[lag:], a[:len(a) - lag]) if lag >= 0 else (m[:lag], a[-lag:])
        n = min(len(vv), len(aa)); vv, aa = vv[:n], aa[:n]
        if n > 24 and vv.std() > 1e-9 and aa.std() > 1e-9:
            best = max(best, float(np.corrcoef(vv, aa)[0, 1]))
    return best

for take_dir, restored, native in [a.split(',') for a in sys.argv[1:]]:
    m = sa.mouth_series(restored)
    n = len(m)
    narr = sa.audio_series(restored, n); own = sa.audio_series(native, n)
    k = min(n, len(narr), len(own))
    mm = sa.smooth(m[:k])
    cn, co = corr_near(mm, sa.smooth(narr[:k])), corr_near(mm, sa.smooth(own[:k]))
    nm = sa.smooth(sa.mouth_series(native)[:k])
    base = corr_near(nm, sa.smooth(own[:k]))
    print(f"{take_dir}: restored mouth vs NARRATION {cn:.3f} | vs GENERATOR VOICE {co:.3f} | (native mouth vs own voice {base:.3f})", flush=True)
