#!/usr/bin/env python3
"""Conform each OmniHuman reference to 1920x1080/24 at its slice length and measure its motion.

A reference that moves more than the owner-approved seg021 reference (head, torso or hands over
the ceiling by more than 5%) gets the gentler-scale line in its Seedance prompt. Writes REFS.json.
"""
import hashlib, json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
REPO = EP.parents[2]
plan = json.load(open(HERE / "PLAN.json"))
ceiling = plan["motion_ceiling"]
BOXES = {"torso": (560, 420, 800, 330), "hands": (420, 780, 1080, 260), "head": (760, 120, 400, 300)}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def motion(p, box, seconds):
    x, y, w, h = box
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-t", str(seconds), "-vf",
                          f"crop={w}:{h}:{x}:{y},scale={w // 4}:{h // 4},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = (w // 4) * (h // 4)
    fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    d = [sum(abs(a - b) for a, b in zip(fr[i], fr[i + 1])) / n for i in range(len(fr) - 1)]
    return round(sum(d) / len(d), 3)


refs = {}
for take, t in plan["takes"].items():
    src = EP / "presenter/generated" / f"r9-{take}-omni.mp4"
    if not src.exists():
        refs[take] = {"status": "missing"}
        continue
    n = t["master_frames"][1] - t["master_frames"][0]
    dst = HERE / take / "omni-ref.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", "-vf",
                    "crop=1920:1080:(iw-1920)/2:(ih-1080)/2,fps=24,tpad=stop_mode=clone:stop=48", "-frames:v", str(n),
                    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "slow",
                    "-movflags", "+faststart", str(dst)], check=True)
    m = {k: motion(dst, b, min(10, t["seconds"])) for k, b in BOXES.items()}
    over = {k: round(m[k] / ceiling[k], 2) for k in m if m[k] > ceiling[k] * 1.05}
    refs[take] = {"status": "ready", "path": str(dst.relative_to(REPO)), "sha256": sha(dst), "frames": n, "motion": m,
                  "over_ceiling": over, "gentle": bool(over)}
json.dump({"record_type": "omniref_r9_references", "ceiling": ceiling, "refs": refs}, open(HERE / "REFS.json", "w"), indent=1)
for k, v in refs.items():
    print(k, v.get("status"), v.get("motion"), "GENTLE" if v.get("gentle") else "")
