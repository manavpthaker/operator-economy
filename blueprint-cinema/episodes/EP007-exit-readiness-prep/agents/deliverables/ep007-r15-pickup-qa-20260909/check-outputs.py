"""Read-only independent output QA; invoke with output A and B paths."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[5]
PROJECT = ROOT / "blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r15-post-title"
ORDER = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/ep007-r15-pickup-qa-20260909.json"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def pcm(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1"])
    return np.frombuffer(raw, dtype="<f4").astype(float)

assert len(sys.argv) in (2, 3), "Supply output A, optionally followed by B."
order = json.loads(ORDER.read_text())
for item in order["inputs"]:
    assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
manifest = json.loads((PROJECT / "provider/INPUTS.json").read_text())
notified_hashes = {"a": "6e7bba71467acf91ecc0541d85c53ba41d86c977fcfe25b25606c8dc9afdfc90", "b": "41a1a6a9fa66c60d41f77eb5d13ec4edbfed3931c24983b1823836cd72cbd823"}
report = {"pins_match": True, "outputs": [], "limits": "Audio preservation, decode and timing only. No claim of phoneme-level mouth fidelity or performance approval."}
for path_arg, item in zip(sys.argv[1:], manifest["inputs"]):
    output = Path(path_arg).resolve()
    assert sha(output) == notified_hashes[item["id"]], "Generated output differs from orchestrator-notified hash"
    reference = PROJECT / item["audio_path"]
    assert sha(reference) == item["audio_sha256"]
    x, y = pcm(reference), pcm(output)
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(output)]))
    vs = next(s for s in probe["streams"] if s["codec_type"] == "video")
    decode = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(output), "-f", "null", "-"], capture_output=True, text=True)
    windows = []
    duration = len(x) / 16000
    for st in np.arange(0.3, duration - 0.75, 1.2):
        en = min(st + 1.2, duration - 0.2)
        start, end, pad = round(st * 16000), round(en * 16000), 2400
        a = x[start:end]
        a = a - a.mean()
        if np.sqrt(np.mean(a*a)) < 0.006:
            continue
        low = max(0, start - pad)
        high = min(len(y), end + pad)
        region = y[low:high]
        n = len(a)
        if len(region) < n:
            windows.append({"reference_seconds": [float(st),float(en)], "error": "output too short"})
            continue
        score = np.correlate(region, a, mode="valid")
        sums = np.concatenate(([0], np.cumsum(region)))
        squares = np.concatenate(([0], np.cumsum(region**2)))
        centered_energy = squares[n:] - squares[:-n] - (sums[n:] - sums[:-n])**2/n
        score /= np.sqrt(np.maximum(centered_energy, 1e-15) * np.dot(a,a))
        best = int(np.argmax(score))
        zero = start - low
        windows.append({"reference_seconds": [float(st),float(en)], "best_lag_samples_16000hz": best + low - start, "best_lag_seconds": (best + low - start)/16000, "best_correlation": float(score[best]), "zero_lag_correlation": float(score[zero]) if zero < len(score) else None})
    n = min(len(x),len(y))
    full_corr = float(np.corrcoef(x[:n],y[:n])[0,1])
    derivative = PROJECT / f"public/media/post-title-{item['id']}.mp4"
    dp = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(derivative)]))
    assert len(dp["streams"]) == 1 and dp["streams"][0]["codec_type"] == "video"
    def video_hash(path):
        return subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-f", "hash", "-hash", "sha256", "-"], text=True).strip()
    track_hash = video_hash(output)
    assert track_hash == video_hash(derivative)
    report["outputs"].append({"id": item["id"], "path": str(output.relative_to(ROOT)), "sha256": sha(output), "probe": probe, "expected_frames": item["frames"], "expected_seconds": item["duration"], "available_video_seconds": float(vs["duration"]), "full_requested_picture_range_available": float(vs["duration"]) + 0.00001 >= item["duration"], "reference_samples_16000hz": len(x), "output_samples_16000hz": len(y), "whole_zero_lag_correlation_over_common_samples": full_corr, "audio_windows": windows, "decode_returncode": decode.returncode, "decode_stderr": decode.stderr, "silent_derivative": {"path": str(derivative.relative_to(ROOT)), "sha256": sha(derivative), "probe": dp, "video_packet_hash_identical": True, "video_packet_hash": track_hash}})
(PACKET / ("output-measurements.json" if len(sys.argv) == 3 else "output-a-measurements.json")).write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps([{k: o[k] for k in ["id", "sha256", "available_video_seconds", "full_requested_picture_range_available", "decode_returncode", "whole_zero_lag_correlation_over_common_samples", "audio_windows"]} for o in report["outputs"]], indent=2))
