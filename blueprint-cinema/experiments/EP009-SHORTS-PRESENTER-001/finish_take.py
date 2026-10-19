#!/usr/bin/env python3
"""Bring one finished Seedance presenter take through react-1 and verification.

usage: finish_take.py <take-id> <seedance result url>

Per take:
 1. Download the native take, hash and probe it, full-decode it, write a contact sheet.
 2. fal-ai/sync-lipsync/react-1 (lips, neutral, 0.5, cut_off) with the same unpadded span
    slice that drove the generation, through the oe-cinema gate so intent is recorded first.
 3. Verify the repaired clip's duration against the span the Short needs. cut_off trims to the
    audio, so a correct result needs no downstream trimming.

One submission per stage, no retries. Records land in takes/<take-id>/TAKE.json.
Lip sync is not asserted here: it is settled by owner viewing, as EP007 settled it.
"""
import hashlib, json, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CDN = "https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/%s.mp3"

take_id, url = sys.argv[1], sys.argv[2]
intent = json.load(open(HERE / "BATCH-INTENT-V1.json"))
req = next(r for r in intent["requests"] if r["id"] == take_id)
plan = {t["id"]: t for t in json.load(open(HERE / "REMAINING-TAKES.json"))["takes"]}[take_id]
audio_media_id = next(m["value"] for m in req["params"]["medias"] if m["role"] == "audio_references")
audio_url = CDN % audio_media_id

d = HERE / "takes" / take_id
rec_path = d / "TAKE.json"
rec = json.load(open(rec_path)) if rec_path.exists() else {
    "take": take_id, "short": plan["short"], "span": plan["span"],
    "master_from_s": plan["from_s"], "master_to_s": plan["to_s"],
    "span_seconds": plan["speech_s"], "seedance_job_id": req["job_id"]}

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate,nb_frames:format=duration",
        "-of", "json", str(p)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def decode_ok(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "null", "-"],
                       capture_output=True, text=True)
    return r.returncode == 0 and not r.stderr.strip()

def sheet(src, dst, tile="6x2"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf",
                    f"fps=1,scale=360:-2,tile={tile}", "-frames:v", "1", str(dst)], check=True)

def save():
    json.dump(rec, open(rec_path, "w"), indent=1)

native = d / "take.mp4"
if "native" not in rec:
    native.write_bytes(urllib.request.urlopen(url).read())
    sheet(native, d / "take-sheet.jpg")
    rec["native"] = {"url": url, "path": str(native.relative_to(REPO)), "sha256": sha(native),
                     "probe": probe(native), "full_decode_ok": decode_ok(native)}
    save()
    print(f"{take_id}: native {rec['native']['probe']['format']['duration']}s")

out = HERE / "generated" / f"{take_id}-react1.mp4"
if rec.get("react1", {}).get("status") != "done":
    args = {"video_url": url, "audio_url": audio_url, "model_mode": "lips",
            "emotion": "neutral", "lipsync_mode": "cut_off", "temperature": 0.5}
    est = round(plan["speech_s"] / 60 * 10 + 0.25, 2)
    r = subprocess.run([str(REPO / "blueprint-cinema/bin/oe-cinema"), "generate", str(HERE),
        "--provider", "fal", "--model", "fal-ai/sync-lipsync/react-1", "--lane", "presenter",
        "--item", f"{take_id}-react1", "--out", str(HERE / "generated"),
        "--reason", f"EP009 Shorts presenter {take_id}: react-1 repair on the accepted route, "
                    f"cut_off against the same {plan['speech_s']}s span slice that drove the generation",
        "--est-usd", str(est), "--args", json.dumps(args)], capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        rec["react1"] = {"status": "failed", "stdout": r.stdout[-2000:], "stderr": r.stderr[-2000:]}
        save(); sys.exit(f"{take_id}: react-1 failed; this take holds")
    p = probe(out)
    # pick the VIDEO stream by codec_type: react-1 returns audio first, and
    # streams[0]["nb_frames"] there is an AAC frame count, not a picture count.
    v = next(st for st in p["streams"] if st["codec_type"] == "video")
    frames = int(v["nb_frames"])
    dur = float(p["format"]["duration"])
    rec["react1"] = {"status": "done", "item": f"{take_id}-react1", "est_usd": est,
        "audio_url": audio_url, "path": str(out.relative_to(REPO)), "sha256": sha(out),
        "probe": p, "full_decode_ok": decode_ok(out), "frames": frames,
        "fps": v["r_frame_rate"], "pixels": f'{v["width"]}x{v["height"]}', "duration_s": dur,
        "span_seconds": plan["speech_s"],
        "trimmed_to_audio": abs(dur - plan["speech_s"]) < 0.05,
        "note": "cut_off should return the span length exactly. A mismatch is reported, not trimmed away."}
    sheet(out, d / "react1-sheet.jpg")
    save()
    print(f"{take_id}: react1 {dur}s / {frames}f, span {plan['speech_s']}s, "
          f"trimmed_to_audio={rec['react1']['trimmed_to_audio']}")
