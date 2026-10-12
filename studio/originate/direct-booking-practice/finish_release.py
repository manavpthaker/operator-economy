"""Stage EP009 (public No. 002) for launch.py. Run on the Mac, from studio/.

    python originate/direct-booking-practice/finish_release.py          # check only
    python originate/direct-booking-practice/finish_release.py --write  # encode and stage

1. Episode: scales the accepted 720p master (launch/ep009-master-720p.mp4, already -14 LUFS)
   to 1920x1080 for upload as ep009-final.mp4. Audio is copied, not re-encoded.
2. Shorts: takes the newest HyperFrames render of each Short, two-pass loudnorm to -14 LUFS /
   -1 dBTP, video stream copied, written to shorts/short-NN.mp4.
3. Verifies every output: resolution, frame count, integrated loudness.

Owner ruling 2026-10-12 (via this session): path 1 of PARKED-2026-10-09.md, upscale the 720p
master. No new detail; YouTube gives a 1080p upload a better bitrate ladder than 720p.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

EP = Path(__file__).resolve().parent
MASTER_720 = EP / "launch" / "ep009-master-720p.mp4"
EPISODE_OUT = EP / "ep009-final.mp4"
SHORTS_SRC = EP / "shorts-hyperframes"
SHORTS_OUT = EP / "shorts"
EPISODE_FRAMES = 29323
# Accepted frame counts from PARKED-2026-10-09.md; Short 01 is 1088 per commit 58286688.
SHORT_FRAMES = {1061, 1092, 1195, 1088}
TARGET_LUFS, TOLERANCE = -14.0, 0.5


def run(cmd: list[str]) -> str:
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"failed: {' '.join(cmd)}\n{out.stderr[-2000:]}")
    return out.stdout + out.stderr


def probe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
               "-show_entries", "stream=width,height,nb_read_packets,r_frame_rate",
               "-of", "json", str(path)])
    s = json.loads(out)["streams"][0]
    return {"w": s["width"], "h": s["height"], "frames": int(s["nb_read_packets"]),
            "fps": s["r_frame_rate"]}


def loudness(path: Path) -> dict:
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
               f"loudnorm=I={TARGET_LUFS}:TP=-1:LRA=11:print_format=json", "-f", "null", "-"])
    return json.loads(out[out.rindex("{"):out.rindex("}") + 1])


def newest_render(n: str) -> Path:
    dirs = sorted(SHORTS_SRC.glob(f"{n}-*"))
    if len(dirs) != 1:
        sys.exit(f"expected one shorts-hyperframes/{n}-* folder, found {dirs}")
    renders = sorted(dirs[0].glob("renders/*.mp4"), key=lambda p: p.stat().st_mtime)
    if not renders:
        sys.exit(f"no render in {dirs[0]}/renders/. Render it: cd {dirs[0]} && npm run render")
    return renders[-1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="encode and stage (default: check only)")
    args = ap.parse_args()
    problems: list[str] = []

    print("Episode")
    if not MASTER_720.exists():
        sys.exit(f"missing {MASTER_720}. Regenerate the -14 LUFS master first.")
    m = probe(MASTER_720)
    print(f"  source {MASTER_720.name}: {m['w']}x{m['h']} {m['frames']} frames {m['fps']}")
    if m["frames"] != EPISODE_FRAMES:
        problems.append(f"master has {m['frames']} frames, accepted r11 cut has {EPISODE_FRAMES}")
    if args.write and not EPISODE_OUT.exists():
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(MASTER_720),
             "-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
             "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-c:a", "copy", str(EPISODE_OUT)])
    if EPISODE_OUT.exists():
        e = probe(EPISODE_OUT)
        lu = float(loudness(EPISODE_OUT)["input_i"])
        print(f"  upload {EPISODE_OUT.name}: {e['w']}x{e['h']} {e['frames']} frames, {lu:.1f} LUFS")
        if (e["w"], e["h"]) != (1920, 1080) or e["frames"] != m["frames"]:
            problems.append("episode upload does not match the master's frames at 1920x1080")
        if abs(lu - TARGET_LUFS) > TOLERANCE:
            problems.append(f"episode at {lu:.1f} LUFS, target {TARGET_LUFS}")

    print("Shorts")
    SHORTS_OUT.mkdir(exist_ok=True)
    seen = set()
    for n in ("01", "02", "03", "04"):
        src = newest_render(n)
        s = probe(src)
        print(f"  {n} source {src.relative_to(EP)}: {s['w']}x{s['h']} {s['frames']} frames")
        if s["frames"] not in SHORT_FRAMES:
            problems.append(f"Short {n}: {s['frames']} frames is not an accepted length {SHORT_FRAMES}")
        seen.add(s["frames"])
        dst = SHORTS_OUT / f"short-{n}.mp4"
        if args.write and not dst.exists():
            first = loudness(src)
            af = (f"loudnorm=I={TARGET_LUFS}:TP=-1:LRA=11:measured_I={first['input_i']}:"
                  f"measured_TP={first['input_tp']}:measured_LRA={first['input_lra']}:"
                  f"measured_thresh={first['input_thresh']}:offset={first['target_offset']}:"
                  "linear=true")
            run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-c:v", "copy", "-af", af,
                 "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                 str(dst)])
        if dst.exists():
            d = probe(dst)
            lu = float(loudness(dst)["input_i"])
            print(f"     -> {dst.name}: {d['frames']} frames, {lu:.1f} LUFS")
            if d["frames"] != s["frames"]:
                problems.append(f"Short {n}: staged copy lost frames")
            if abs(lu - TARGET_LUFS) > TOLERANCE:
                problems.append(f"Short {n} at {lu:.1f} LUFS, target {TARGET_LUFS}")
    if seen != SHORT_FRAMES:
        problems.append(f"Short frame counts {sorted(seen)} differ from accepted {sorted(SHORT_FRAMES)}")

    if problems:
        print("\nHOLD:\n  " + "\n  ".join(problems))
        sys.exit(1)
    print("\nOK" + ("" if args.write else ". Check only; re-run with --write to encode."))


if __name__ == "__main__":
    main()
