#!/usr/bin/env python3
"""Build EP009's 1080p delivery master from the owner-accepted r11 cut.

The accepted picture is r11. This does not rebuild it. It takes the accepted cut as the base,
upscales it to 1920x1080, and overlays the natively re-rendered scenes on top at exactly the
frame ranges the frozen r3 timeline gives them. Scenes were never revised after r3 (r4 through
r11 only replaced presenter segments), so a scene's frame range and sub-range are the same in
r11 as in r3.

The result: 83 percent of the picture is natively sharp, the remaining 17 percent (presenter and
film plates, which exist only at 720p) is upscaled, and the cut's timing is untouched because
nothing is re-timed, only painted over.
"""
import json, subprocess, sys, pathlib

E = pathlib.Path(__file__).resolve().parents[1]
REPO = E.parents[2]
S = E / "conform-1080p/scenes"
BASE = REPO / "studio/originate/direct-booking-practice/launch/ep009-master-720p.mp4"
OUT = REPO / "studio/originate/direct-booking-practice/launch/ep009-master-1080p.mp4"
FPS = 24

# Only the rows the accepted picture still shows. match_rows.py decides that by comparing the
# accepted master against each re-rendered scene, because the build tables record r3 sources and
# are not updated when a later build overlays something else. Four ranges are excluded that way.
match = json.load(open(E / "conform-1080p/ROW-MATCH.json"))
keep_ids = {r["id"] for r in match["kept"]}
rows = json.load(open(E / "assembly/r3/ep009-full-r3-review-draft-BUILD.json"))["all_75_rows"]
scene_rows = [r for r in rows
              if "/scenes/" in (r.get("original", {}).get("path") or "") and r["id"] in keep_ids]
print(f"overlaying {len(scene_rows)} verified rows; "
      f"{len(match['dropped'])} excluded as later-painted: "
      + ", ".join(d["id"] for d in match["dropped"]))

# one input per project, split as many ways as it has rows
projects = {}
for r in scene_rows:
    proj = r["original"]["path"].split("/scenes/")[1].split("/")[0]
    projects.setdefault(proj, []).append(r)

missing = [p for p in projects if not (S / f"{p}.1080.mp4").exists()]
if missing:
    sys.exit(f"missing 1080p renders for: {missing}")

inputs = ["-i", str(BASE)]
order = list(projects)
for p in order:
    inputs += ["-i", str(S / f"{p}.1080.mp4")]

# The accepted cut is 720p. Upscale it to the delivery frame FIRST: overlaying 1920x1080
# scenes onto a 1280x720 canvas places them at the origin and crops them, which is exactly
# what the verifier caught on the first attempt.
parts = ["[0:v]scale=1920:1080:flags=lanczos,setsar=1[base]"]
cur, n = "[base]", 0
for idx, proj in enumerate(order, start=1):
    rs = projects[proj]
    labels = [f"s{idx}_{j}" for j in range(len(rs))]
    parts.append(f"[{idx}:v]split={len(rs)}" + "".join(f"[{l}]" for l in labels))
    for r, lab in zip(rs, labels):
        o = r["original"]
        a, b = r["output_frames"]          # final position on the master timeline
        fr = b - a                          # final length
        st = o["src_start"]                 # offset into the scene render
        # r3 trimmed one segment's LENGTH (seg010, 90 frames down to 12) and shifted the
        # rest. original.out and original.frames are pre-trim; output_frames is final.
        if fr != r["frames"]:
            sys.exit(f"{r['id']}: output span {fr} != frames {r['frames']}")
        if st + fr > o["frames"] + st:
            sys.exit(f"{r['id']}: source range runs past the render")
        parts.append(
            f"[{lab}]trim=start_frame={st}:end_frame={st+fr},setpts=PTS-STARTPTS+{a}/({FPS}*TB)[p{n}]")
        parts.append(f"{cur}[p{n}]overlay=eof_action=pass:enable='between(n,{a},{b-1})'[v{n}]")
        cur = f"[v{n}]"; n += 1

graph = ";".join(parts)
(E / "conform-1080p/conform-graph.txt").write_text(graph)
print(f"{len(order)} scene inputs, {n} overlays, graph {len(graph)} chars")

cmd = ["ffmpeg", "-nostdin", "-v", "error", "-stats", "-y", *inputs,
       "-filter_complex", graph, "-map", cur, "-map", "0:a",
       "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-level", "4.1",
       "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "48",
       "-c:a", "copy", "-movflags", "+faststart", str(OUT)]
json.dump({"inputs": [str(x) for x in inputs], "overlays": n,
           "base": str(BASE.relative_to(REPO)), "out": str(OUT.relative_to(REPO))},
          open(E / "conform-1080p/CONFORM-CMD.json", "w"), indent=1)
print("encoding ...", flush=True)
r = subprocess.run(cmd)
sys.exit(r.returncode)
