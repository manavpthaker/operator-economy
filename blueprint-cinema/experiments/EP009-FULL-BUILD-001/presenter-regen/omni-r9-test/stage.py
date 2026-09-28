#!/usr/bin/env python3
"""C3 route segment test: conform OmniHuman output, sync with react-1 face mode, join.

  stage.py prep <seg>                      conform the OmniHuman take to 1920x1080/24 at the slice's
                                            frame count; for seg071 also split at the pause frame
  stage.py sync <seg> <part> <video url>   react-1 face 0.5 on one uploaded part (part: all, a, b)
  stage.py final <seg>                     join the synced parts, conform, verify, write RESULT.json
"""
import hashlib, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
REPO = EP.parents[2]
GEN = EP / "presenter/generated"
test = json.load(open(HERE / "TEST.json"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def frames(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True).stdout
    return int(out.strip())


def enc(src, dst, n, vf):
    # Frame-rate change drops/duplicates frames at constant duration; speed is untouched.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", "-vf", f"{vf},tpad=stop_mode=clone:stop=48",
                    "-frames:v", str(n), "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "14",
                    "-preset", "slow", "-movflags", "+faststart", str(dst)], check=True)


cmd, seg = sys.argv[1], sys.argv[2]
S = test["segments"][seg]
d = HERE / seg
if cmd == "prep":
    src = GEN / f"r9t-{seg}-omni.mp4"
    conf = d / "omni-conform.mp4"
    enc(src, conf, S["frames"], "crop=1920:1080:(iw-1920)/2:(ih-1080)/2,fps=24")
    parts = {"all": conf}
    if "react_split" in S:
        k = S["react_split"]["at_frame"]
        enc(conf, d / "omni-a.mp4", k, "null")
        enc(conf, d / "omni-b.mp4", S["frames"] - k, f"trim=start_frame={k},setpts=PTS-STARTPTS")
        parts = {"a": d / "omni-a.mp4", "b": d / "omni-b.mp4"}
    for p, f in parts.items():
        print(p, f.relative_to(REPO), frames(f), sha(f))
elif cmd == "sync":
    part, url = sys.argv[3], sys.argv[4]
    audio = S["audio_url"] if part == "all" else S["react_split"][f"{part}_audio"]
    args = {"video_url": url, "audio_url": audio, "model_mode": "face", "emotion": "neutral", "lipsync_mode": "cut_off", "temperature": 0.5}
    r = subprocess.run([str(REPO / "blueprint-cinema/bin/oe-cinema"), "generate", str(EP), "--provider", "fal", "--model", "fal-ai/sync-lipsync/react-1",
                        "--lane", "presenter", "--item", f"r9t-{seg}-{part}-react1face", "--reason", "C3 route segment test: react-1 face 0.5",
                        "--est-usd", "2.5", "--args", json.dumps(args)], capture_output=True, text=True)
    print(r.stdout[-600:], r.stderr[-600:])
elif cmd == "final":
    parts = ["all"] if "react_split" not in S else ["a", "b"]
    synced = [GEN / f"r9t-{seg}-{p}-react1face.mp4" for p in parts]
    lst = d / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in synced))
    joined = d / "joined.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-an", "-c:v", "libx264", "-crf", "12", str(joined)], check=True)
    final = d / "final.mp4"
    enc(joined, final, S["frames"], "scale=1920:1080,fps=24")
    ok = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"], capture_output=True, text=True)
    res = {"segment": seg, "parts": [{"path": str(p.relative_to(REPO)), "sha256": sha(p), "frames": frames(p)} for p in synced],
           "final": {"path": str(final.relative_to(REPO)), "sha256": sha(final), "frames": frames(final), "slice_frames": S["frames"],
                     "full_decode_ok": ok.returncode == 0 and not ok.stderr.strip()}}
    json.dump(res, open(d / "RESULT.json", "w"), indent=1)
    print(json.dumps(res["final"]))
