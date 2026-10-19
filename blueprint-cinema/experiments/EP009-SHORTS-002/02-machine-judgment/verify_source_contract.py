#!/usr/bin/env python3
import hashlib, json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
FPS = 24
edl = json.loads((HERE / "data/edl.json").read_text())
caps = json.loads((HERE / "data/captions.json").read_text())
transcript_path = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r3/word-transcript-r3.json"
transcript = json.loads(transcript_path.read_text())
words = transcript["words"]
by_id = {w["w_id"]: (i, w) for i, w in enumerate(words)}
checks = []

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def record(name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": detail})

carrier = (HERE / edl["carrier"]["path"]).resolve()
carrier_sha = sha(carrier)
record("locked carrier sha256", carrier_sha == edl["carrier"]["sha256"], carrier_sha)
transcript_sha = sha(transcript_path)
record("locked transcript sha256", transcript_sha == "0b5175dea2cbb1ac7682cd69b9ab032bc8c544131aae82575140e90ae0d76709", transcript_sha)

segments = edl["audio_segments"]
cursor = 0
for seg in segments:
    count_t = seg["timeline_out_frame_exclusive"] - seg["timeline_in_frame"]
    count_s = seg["source_out_frame_exclusive"] - seg["source_in_frame"]
    record(f"{seg['id']} frame length", count_t == count_s, {"timeline": count_t, "source": count_s})
    record(f"{seg['id']} timeline continuity", seg["timeline_in_frame"] == cursor, {"expected": cursor, "actual": seg["timeline_in_frame"]})
    cursor = seg["timeline_out_frame_exclusive"]
    i0, w0 = by_id[seg["word_in"]]; i1, w1 = by_id[seg["word_out"]]
    joined = " ".join(w["token"] for w in words[i0:i1+1])
    record(f"{seg['id']} exact locked words", joined == seg["text"], joined)
    record(f"{seg['id']} words inside source window", w0["start"] >= seg["source_in_frame"] / FPS - 1e-6 and w1["end"] <= seg["source_out_frame_exclusive"] / FPS + 1e-6, {"window":[seg["source_in_frame"]/FPS,seg["source_out_frame_exclusive"]/FPS],"words":[w0["start"],w1["end"]]})

silent = edl["silent_segments"][0]
record("CTA follows narration", silent["timeline_in_frame"] == cursor, {"narration_out": cursor, "cta_in": silent["timeline_in_frame"]})
record("timeline ends at declared frame", silent["timeline_out_frame_exclusive"] == edl["timeline_duration_frames"], silent["timeline_out_frame_exclusive"])
record("CTA is three seconds", silent["duration_frames"] == 72, silent["duration_frames"])

for cap in caps["captions"]:
    i0, w0 = by_id[cap["word_in"]]; i1, w1 = by_id[cap["word_out"]]
    joined = " ".join(w["token"] for w in words[i0:i1+1])
    record(f"{cap['id']} exact locked words", joined == cap["text"], joined)
    owner = next(s for s in segments if i0 >= by_id[s["word_in"]][0] and i1 <= by_id[s["word_out"]][0])
    expected_start = owner["timeline_in_frame"] / FPS + w0["start"] - owner["source_in_frame"] / FPS
    expected_duration = w1["end"] - w0["start"]
    record(f"{cap['id']} timed from word alignment", abs(cap["start"] - expected_start) <= 0.045 and abs(cap["duration"] - expected_duration) <= 0.045, {"declared":[cap["start"],cap["duration"]],"aligned":[expected_start,expected_duration]})

html = (HERE / "index.html").read_text()
for seg, audio_id in zip(segments, ["audio-hook","audio-software","audio-drafting","audio-scheduling","audio-human"]):
    m = re.search(rf'<audio id="{audio_id}"[^>]+>', html)
    attrs = m.group(0) if m else ""
    expected = {
        "data-start": seg["timeline_in_frame"] / FPS,
        "data-duration": (seg["timeline_out_frame_exclusive"] - seg["timeline_in_frame"]) / FPS,
        "data-media-start": seg["source_in_frame"] / FPS,
    }
    parsed = {k: float(re.search(rf'{k}="([^"]+)"', attrs).group(1)) for k in expected} if attrs else {}
    record(f"{audio_id} bound to EDL", bool(attrs) and all(abs(parsed[k]-v) < 1e-9 for k,v in expected.items()), {"declared": parsed, "expected": expected})

probe = json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height,r_frame_rate:format=duration","-of","json",str(carrier)]))
record("carrier geometry and fps", any(s.get("codec_type") == "video" and s.get("width") == 1280 and s.get("height") == 720 and s.get("r_frame_rate") == "24/1" for s in probe["streams"]), probe)

result = {
    "schema": "ep009-short02-source-contract-verification-v1",
    "ok": all(c["ok"] for c in checks),
    "checks_passed": sum(c["ok"] for c in checks),
    "checks_total": len(checks),
    "carrier": str(carrier),
    "transcript": str(transcript_path),
    "timeline_duration_frames": edl["timeline_duration_frames"],
    "timeline_duration_seconds": edl["timeline_duration_seconds"],
    "checks": checks,
}
out = HERE / "review/source-contract-verification.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"ok": result["ok"], "checks_passed": result["checks_passed"], "checks_total": result["checks_total"], "output": str(out)}, indent=2))
raise SystemExit(0 if result["ok"] else 1)
