#!/usr/bin/env python3
"""Verify the 1080p conform against the owner-accepted 720p cut.

The conform paints re-rendered scenes onto the accepted picture. If any scene landed at the wrong
frame or took the wrong source range, the picture at that timestamp is simply a different shot,
which shows up as a large difference. So: sample across the whole timeline, downscale the conform
back to 720p, and compare frame for frame against the accepted master.

Scene timestamps should differ a little (higher-DPR antialiasing). Presenter and film timestamps
should differ almost not at all, since both sides are the same 720p pixels. Anything large is a
misalignment, not a rendering difference.
"""
import json, subprocess, sys, pathlib
import numpy as np
from PIL import Image

E = pathlib.Path(__file__).resolve().parents[1]
REPO = E.parents[2]
A = REPO / "studio/originate/direct-booking-practice/launch/ep009-master-720p.mp4"
B = REPO / "studio/originate/direct-booking-practice/launch/ep009-master-1080p.mp4"
FPS, BIG = 24, 18.0

rows = json.load(open(E / "assembly/r3/ep009-full-r3-review-draft-BUILD.json"))["all_75_rows"]
spans = []
for r in rows:
    a, b = r["output_frames"]
    kind = ("scene" if "/scenes/" in (r.get("original", {}).get("path") or "")
            else "presenter" if "/presenter/" in (r.get("original", {}).get("path") or "")
            else "film/other")
    spans.append((a, b, kind, r["id"]))

def frame(src, t, size=None):
    out = "/tmp/_v.png"
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{t:.4f}","-i",str(src),
                    "-frames:v","1",out], check=True)
    im = Image.open(out).convert("RGB")
    return im.resize(size, Image.LANCZOS) if size else im

probe = lambda p: json.loads(subprocess.run(
    ["ffprobe","-v","error","-select_streams","v:0","-count_frames","-show_entries",
     "stream=width,height,nb_read_frames,r_frame_rate","-show_entries","format=duration",
     "-of","json",str(p)], capture_output=True, text=True, check=True).stdout)

pa, pb = probe(A), probe(B)
sa, sb = pa["streams"][0], pb["streams"][0]
print(f"accepted : {sa['width']}x{sa['height']} {sa['nb_read_frames']}f @{sa['r_frame_rate']}")
print(f"conform  : {sb['width']}x{sb['height']} {sb['nb_read_frames']}f @{sb['r_frame_rate']}")
ok_frames = sa["nb_read_frames"] == sb["nb_read_frames"]
print(f"frame counts match: {ok_frames}\n")

bad, results = [], []
for a, b, kind, sid in spans:
    if b - a < 8: continue
    t = (a + (b - a) * 0.5) / FPS                 # mid-segment, away from cut boundaries
    ia = frame(A, t)
    ib = frame(B, t, ia.size)
    d = np.abs(np.asarray(ia).astype(int) - np.asarray(ib).astype(int))
    mean = float(d.mean())
    results.append((sid, kind, mean))
    if mean > BIG: bad.append((sid, kind, mean))

by = {}
for sid, kind, m in results: by.setdefault(kind, []).append(m)
for kind, ms in by.items():
    print(f"  {kind:12s} n={len(ms):3d}  mean {np.mean(ms):6.2f}  max {max(ms):6.2f}")
print(f"\nsegments over the {BIG} misalignment threshold: {len(bad)}")
for sid, kind, m in bad: print(f"  {sid} ({kind}) {m:.2f}")

json.dump({"accepted": str(A.relative_to(REPO)), "conform": str(B.relative_to(REPO)),
           "frame_counts_match": ok_frames, "threshold": BIG,
           "by_kind": {k: {"n": len(v), "mean": round(float(np.mean(v)),2), "max": round(max(v),2)} for k,v in by.items()},
           "over_threshold": [{"id": s, "kind": k, "mean": round(m,2)} for s,k,m in bad]},
          open(E/"conform-1080p/CONFORM-VERIFICATION.json","w"), indent=1)
sys.exit(1 if (bad or not ok_frames) else 0)
