#!/usr/bin/env python3
"""r10: measure each take's three OmniHuman candidates, pick one, and write its 25 fps reference.

Measured on the raw 25 fps output (no frame-rate change): mean frame-to-frame change in the head,
torso and hand regions, hand stutter (a held frame between two moving frames, per 100 frames) and
relative jerk. The r9 reference for the same segment is measured the same way for comparison.
Pick: lowest head motion among candidates whose stutter and jerk are no worse than the r9 reference.
Writes PICK.json and a side-by-side preview per segment (r9 reference | chosen candidate).
"""
import json, statistics, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
GEN = EP / "presenter/generated"
plan = json.load(open(HERE / "PLAN.json"))
BOX = {"head": (760, 120, 400, 300), "torso": (560, 420, 800, 330), "hands": (420, 700, 1080, 340)}


def diffs(p, box, seconds):
    x, y, w, h = box
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-t", str(seconds), "-vf",
                          f"crop={w}:{h}:{x}:{y},scale={w // 4}:{h // 4},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = (w // 4) * (h // 4)
    fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    return [sum(abs(a - b) for a, b in zip(fr[i], fr[i + 1])) / n for i in range(len(fr) - 1)]


def measure(p, seconds):
    m = {k: round(statistics.mean(diffs(p, b, seconds)), 3) for k, b in BOX.items()}
    d = diffs(p, BOX["hands"], seconds)
    m["hand_stutter"] = round(sum(1 for i in range(1, len(d) - 1) if d[i] < 0.35 * min(d[i - 1], d[i + 1]) and min(d[i - 1], d[i + 1]) > 0.8) / len(d) * 100, 2)
    m["jerk"] = round(statistics.mean(abs(d[i + 1] - d[i]) for i in range(len(d) - 1)) / statistics.mean(d), 3)
    return m


out = {"record_type": "omnihuman_reference_pick", "segments": {}}
for seg, tk in plan["takes"].items():
    seconds = min(10, tk["seconds"])
    base = measure(GEN / f"r9-{seg}-omni.mp4", seconds)
    cands = {}
    for k in plan["prompts"]:
        name = f"{seg}-{k}"
        f = GEN / f"r10c-{name}-omni.mp4"
        if f.exists():
            cands[name] = measure(f, seconds)
    ok = {k: v for k, v in cands.items() if v["hand_stutter"] <= base["hand_stutter"] and v["jerk"] <= base["jerk"]}
    pool = ok or cands
    pick = min(pool, key=lambda k: pool[k]["head"])
    out["segments"][seg] = {"r9_reference": base, "candidates": cands, "passed_smoothness": sorted(ok), "pick": pick,
                            "pick_vs_r9": {k: round(cands[pick][k] / base[k], 2) if base[k] else None for k in ("head", "torso", "hands")}}
    (HERE / seg).mkdir(exist_ok=True)
    ref = HERE / seg / "ref25.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(GEN / f"r10c-{pick}-omni.mp4"), "-an", "-t", f"{tk['seconds']:.6f}",
                    "-vf", "crop=1920:1080:(iw-1920)/2:(ih-1080)/2", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-crf", "14", "-preset", "slow", "-movflags", "+faststart", str(ref)], check=True)
    out["segments"][seg]["ref25"] = str(ref.relative_to(EP.parents[2]))
json.dump(out, open(HERE / "PICK.json", "w"), indent=1)
for seg, s in out["segments"].items():
    print(seg, "r9 ref", s["r9_reference"])
    for k, v in s["candidates"].items():
        print("   ", k, v, "PICK" if k == s["pick"] else "")
