#!/usr/bin/env python3
"""Re-render EP009's 21 scene projects at 4K and verify each against the accepted cut.

Scenes were frozen at r3; r4 through r11 only replaced presenter segments. So the scene
content in the owner-accepted r11 cut is byte-identical to r3's, and re-rendering a scene
project reproduces the same picture at a higher device pixel ratio.

Each render is gated, not trusted: the 4K output is downscaled back to 720p and compared
against the exact file the accepted cut used. A project whose current source no longer
reproduces its accepted render fails here rather than silently entering the master.
"""
import json, subprocess, sys, pathlib, collections

E = pathlib.Path(__file__).resolve().parents[1]
OUT = E / "conform-1080p/scenes"
BUILD = E / "assembly/r3/ep009-full-r3-review-draft-BUILD.json"
GATE_MEAN, GATE_PCT = 6.0, 12.0   # antialiasing differs at higher DPR; content must not

rows = json.load(open(BUILD))["all_75_rows"]
scene_rows = [r for r in rows if "/scenes/" in (r.get("original", {}).get("path") or "")]
projects = collections.OrderedDict()
for r in scene_rows:
    p = r["original"]["path"]
    projects.setdefault(p.split("/scenes/")[1].split("/")[0], p)

def probe(p):
    o = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-count_frames",
        "-show_entries","stream=width,height,nb_read_frames,r_frame_rate","-of","json",str(p)],
        capture_output=True, text=True, check=True).stdout
    s = json.loads(o)["streams"][0]
    return int(s["width"]), int(s["height"]), int(s["nb_read_frames"]), s["r_frame_rate"]

def compare(a, b):
    """mean abs diff and percent of pixels differing, b downscaled to a's size"""
    import numpy as np
    from PIL import Image
    res = []
    for t in ("3", "25%", "60%"):
        fa, fb = "/tmp/_ga.png", "/tmp/_gb.png"
        for src, dst in ((a, fa), (b, fb)):
            subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",t if t.endswith("s") or t.isdigit() else "3",
                            "-i",str(src),"-frames:v","1",dst], check=True)
        ia = Image.open(fa).convert("RGB"); ib = Image.open(fb).convert("RGB").resize(ia.size, Image.LANCZOS)
        d = np.abs(np.asarray(ia).astype(int) - np.asarray(ib).astype(int))
        res.append((float(d.mean()), 100.0 * float((d.max(axis=2) > 24).mean())))
    return max(r[0] for r in res), max(r[1] for r in res)

report = {}
fails = []
for i, (proj, accepted_rel) in enumerate(projects.items(), 1):
    accepted = E.parents[2] / accepted_rel
    four_k = OUT / f"{proj}.4k.mp4"
    hd = OUT / f"{proj}.1080.mp4"
    print(f"[{i}/{len(projects)}] {proj}", flush=True)
    if not four_k.exists():
        r = subprocess.run(["npx","--yes","hyperframes@0.8.36","render", str(E/"scenes"/proj),
                            "--resolution","4k","--low-memory-mode","-o",str(four_k)],
                           capture_output=True, text=True)
        if r.returncode != 0 or not four_k.exists():
            fails.append((proj, "render failed", r.stderr[-400:])); print("   RENDER FAILED", flush=True); continue
    aw, ah, af, afr = probe(accepted)
    nw, nh, nf, nfr = probe(four_k)
    ok_frames = (af == nf and afr == nfr)
    mean, pct = compare(accepted, four_k)
    ok_px = (mean <= GATE_MEAN and pct <= GATE_PCT)
    report[proj] = {"accepted": accepted_rel, "accepted_probe": [aw,ah,af,afr], "rendered_probe": [nw,nh,nf,nfr],
                    "frames_match": ok_frames, "mean_abs_diff": round(mean,2), "pct_pixels_differing": round(pct,2),
                    "gate": "pass" if (ok_frames and ok_px) else "FAIL"}
    print(f"   {af}f vs {nf}f  frames_match={ok_frames}  mean={mean:.2f} pct={pct:.2f}  -> {report[proj]['gate']}", flush=True)
    if not (ok_frames and ok_px):
        fails.append((proj, "gate", report[proj])); continue
    if not hd.exists():
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-i",str(four_k),
                        "-vf","scale=1920:1080:flags=lanczos","-c:v","libx264","-preset","slow","-crf","14",
                        "-pix_fmt","yuv420p","-r","24","-an",str(hd)], check=True)

json.dump({"gate_thresholds": {"mean_abs_diff": GATE_MEAN, "pct_pixels_differing": GATE_PCT},
           "projects": report, "failures": [f[0] for f in fails]},
          open(E/"conform-1080p/SCENE-RENDER-REPORT.json","w"), indent=1)
print(f"\n{len(report)-len(fails)}/{len(projects)} passed the gate")
if fails:
    print("FAILURES:", [f[0] for f in fails]); sys.exit(1)
