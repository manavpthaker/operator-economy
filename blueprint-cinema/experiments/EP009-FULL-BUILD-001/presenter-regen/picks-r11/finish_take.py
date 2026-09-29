#!/usr/bin/env python3
"""Take one finished Seedance kit take through review prep, react-1 and the browser-safe conform.

usage: finish_take.py <take> <seedance result url> [sync video url]

The optional sync video url is a trimmed copy of the native take for react-1, which refuses video over 15 s.

1. Download the native take, hash and probe it, full-decode it, write a 1 fps contact sheet.
2. fal-ai/sync-lipsync/react-1 (lips, neutral, 0.5, cut_off) through oe-cinema generate.
3. Conform: H.264 High, yuv420p, 24 fps, audio stripped, not retimed or recropped.
Records land in <take>/TAKE.json. One submission, no retries.
"""
import hashlib, json, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
REPO = EP.parents[2]
take, url = sys.argv[1], sys.argv[2]
sync_url = sys.argv[3] if len(sys.argv) > 3 else url
T = {t["take"]: t for t in json.load(open(HERE / "TAKES.json"))["takes"]}[take]
up = json.load(open(HERE / "HIGGSFIELD-AUDIO-UPLOADS.json"))[take]
job = json.load(open(HERE / "SEEDANCE-JOBS.json"))[take]
d = HERE / take
rec_path = d / "TAKE.json"
rec = json.load(open(rec_path)) if rec_path.exists() else {"take": take, "segment": T["segment"], "seedance_job_id": job["job_id"]}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames:format=duration",
                          "-of", "json", str(p)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def decode_ok(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "null", "-"], capture_output=True, text=True)
    return r.returncode == 0 and not r.stderr.strip()


def save():
    json.dump(rec, open(rec_path, "w"), indent=1)


native = d / "native.mp4"
if "native" not in rec:
    native.write_bytes(urllib.request.urlopen(url).read())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", native, "-vf", "fps=1,scale=480:-2,tile=6x3", "-frames:v", "1", d / "native-sheet.jpg"], check=True)
    rec["native"] = {"url": url, "path": str(native.relative_to(REPO)), "sha256": sha(native), "probe": probe(native), "full_decode_ok": decode_ok(native)}
    save()

item = f"r11-{take}-react1"
synced = EP / "presenter/generated" / f"{item}.mp4"
if rec.get("react1", {}).get("status") != "done":
    args = {"video_url": sync_url, "audio_url": up["url"], "model_mode": "lips", "emotion": "neutral", "lipsync_mode": "cut_off", "temperature": 0.5}
    est = round(T["seconds"] / 60 * 10 + 0.25, 2)
    r = subprocess.run([str(REPO / "blueprint-cinema/bin/oe-cinema"), "generate", str(EP), "--provider", "fal", "--model", "fal-ai/sync-lipsync/react-1",
                        "--lane", "presenter", "--item", item, "--reason", f"r11 owner-picked regeneration of {take}: react-1 lips/neutral/0.5",
                        "--est-usd", str(est), "--args", json.dumps(args)], capture_output=True, text=True)
    if r.returncode != 0 or not synced.exists():
        rec["react1"] = {"status": "failed", "stdout": r.stdout[-2000:], "stderr": r.stderr[-2000:]}
        save(); sys.exit(f"{take}: react-1 failed; lane holds for this take")
    rec["react1"] = {"status": "done", "item": item, "sync_video_url": sync_url, "est_usd": est, "path": str(synced.relative_to(REPO)), "sha256": sha(synced), "probe": probe(synced)}
    save()

final = d / "final.mp4"
if "final" not in rec:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", synced, "-an", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "24",
                    "-crf", "14", "-preset", "slow", "-movflags", "+faststart", final], check=True)
    p = probe(final)
    frames = int(p["streams"][0]["nb_frames"])
    want = T["master_frames"][1] - T["master_frames"][0]
    rec["final"] = {"path": str(final.relative_to(REPO)), "sha256": sha(final), "probe": p, "full_decode_ok": decode_ok(final),
                    "frames": frames, "slice_frames": want, "frames_match": frames == want}
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", final, "-vf", "fps=1,scale=480:-2,tile=6x3", "-frames:v", "1", d / "final-sheet.jpg"], check=True)
    save()
print(take, "final frames", rec["final"]["frames"], "of", rec["final"]["slice_frames"], "decode", rec["final"]["full_decode_ok"])
