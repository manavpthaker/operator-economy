#!/usr/bin/env python3
"""Decide empirically which scene rows the accepted cut still shows.

EP009's picture went through r3 then r5, r6, r7, r8, r9, r10 and r11, each overlaying onto the
previous encode. The row tables record the r3 source for every segment and are not updated when a
later build paints something else on top, so they cannot tell you what is actually on screen.
Three separate assumptions drawn from them were wrong: that only presenters changed after r3, that
the software-demo inserts were the only later overlays, and that a row's lane tells you its content.

So this asks the picture instead. For each scene row, sample frames across its range in the
accepted master and compare them with the re-rendered scene at the matching source offset. Rows
that match are safe to sharpen. Rows that do not are whatever a later build put there, and the
conform must leave them alone.
"""
import json, subprocess, sys, pathlib
import numpy as np
from PIL import Image

E = pathlib.Path(__file__).resolve().parents[1]
REPO = E.parents[2]
ACCEPTED = REPO / "studio/originate/direct-booking-practice/launch/ep009-master-720p.mp4"
S = E / "conform-1080p/scenes"
FPS, MATCH = 24, 8.0          # the gate's own worst same-content reading was 1.64

rows = json.load(open(E / "assembly/r3/ep009-full-r3-review-draft-BUILD.json"))["all_75_rows"]
scene_rows = [r for r in rows if "/scenes/" in (r.get("original", {}).get("path") or "")]

def frame(src, t, size=None):
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{t:.5f}","-i",str(src),
                    "-frames:v","1","/tmp/_m.png"], check=True)
    im = Image.open("/tmp/_m.png").convert("RGB")
    return im.resize(size, Image.LANCZOS) if size else im

keep, drop = [], []
for r in scene_rows:
    o = r["original"]
    proj = o["path"].split("/scenes/")[1].split("/")[0]
    a, b = r["output_frames"]; n = b - a; st = o["src_start"]
    render = S / f"{proj}.1080.mp4"
    diffs = []
    for frac in (0.25, 0.5, 0.75):
        off = int(n * frac)
        ia = frame(ACCEPTED, (a + off) / FPS)
        ib = frame(render, (st + off) / FPS, ia.size)
        d = np.abs(np.asarray(ia).astype(int) - np.asarray(ib).astype(int))
        diffs.append(float(d.mean()))
    worst = max(diffs)
    rec = {"id": r["id"], "project": proj, "out": [a, b], "frames": n,
           "src_start": st, "worst_mean_diff": round(worst, 2),
           "samples": [round(x, 2) for x in diffs]}
    (keep if worst <= MATCH else drop).append(rec)
    print(f"  {r['id']:8s} {proj:20s} worst={worst:7.2f}  {'keep' if worst <= MATCH else 'DROP'}", flush=True)

json.dump({"threshold": MATCH, "kept": keep, "dropped": drop},
          open(E / "conform-1080p/ROW-MATCH.json", "w"), indent=1)
kf = sum(r["frames"] for r in keep); df = sum(r["frames"] for r in drop)
print(f"\nkeep {len(keep)} rows / {kf} frames ({kf/29323*100:.0f}% of the cut)")
print(f"drop {len(drop)} rows / {df} frames ({df/29323*100:.0f}%) — later builds painted over these")
for r in drop: print(f"   {r['id']} {r['out']} worst={r['worst_mean_diff']}")
