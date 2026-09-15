"""Independent R15 input QA. Reads sources; writes diagnostics only in this packet."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path
import numpy as np

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[5]
ORDER = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/ep007-r15-pickup-qa-20260909.json"
PROJECT = ROOT / "blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r15-post-title"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))

def read_pcm(path, start=0, count=None):
    with wave.open(str(path), "rb") as w:
        assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, 48000)
        w.setpos(start)
        return w.readframes(w.getnframes() - start if count is None else count)

order = json.loads(ORDER.read_text())
for item in order["inputs"]:
    assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
master = ROOT / order["inputs"][0]["path"]
manifest_path = PROJECT / "provider/INPUTS.json"
manifest = json.loads(manifest_path.read_text())
report = {"pins_match": True, "manifest_sha256": sha(manifest_path), "pickups": [], "limits": "Threshold-based boundary checks and PCM identity; not listening or phoneme accuracy."}
expected = {"a": (2856000, 3164000, 154, 0, 154), "b": (3164000, 3576000, 206, 83, 289)}
joined = bytearray()
for item in manifest["inputs"]:
    start, end, frames, pic_start, pic_end = expected[item["id"]]
    assert item["source_samples"] == [start, end]
    assert item["source_frames"] == [pic_start, pic_end]
    audio = PROJECT / item["audio_path"]
    video = PROJECT / item["video_path"]
    assert sha(audio) == item["audio_sha256"]
    assert sha(video) == item["video_sha256"]
    raw = read_pcm(audio)
    assert raw == read_pcm(master, start, end - start)
    assert len(raw) == 2 * (end - start)
    joined.extend(raw)
    vp = probe(video)
    vs = next(x for x in vp["streams"] if x["codec_type"] == "video")
    assert vs["r_frame_rate"] == "24/1"
    assert int(vs["nb_frames"]) == frames
    assert abs(float(vs["duration"]) - frames / 24) < 0.00001
    decode = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(video), "-f", "null", "-"], capture_output=True, text=True)
    assert decode.returncode == 0, decode.stderr
    report["pickups"].append({"id": item["id"], "audio_sha256": sha(audio), "video_sha256": sha(video), "source_samples": [start, end], "pcm_identical": True, "samples": end - start, "duration": (end - start) / 48000, "frames": frames, "source_frames": [pic_start, pic_end], "probe": vp, "decode_returncode": decode.returncode})
assert joined == read_pcm(master, 2856000, 720000)
report["concatenated_pcm_identical"] = True
report["boundary_windows"] = []
for t in [59.5, 65 + 11 / 12, 74.5]:
    raw = read_pcm(master, round((t - 0.02) * 48000), 1920)
    x = np.frombuffer(raw, dtype="<i2").astype(float) / 32768
    report["boundary_windows"].append({"center_seconds": t, "window_seconds": 0.04, "rms": float(np.sqrt(np.mean(x*x))), "peak": float(np.max(np.abs(x)))})
scan = subprocess.run(["ffmpeg", "-hide_banner", "-ss", "59", "-t", "16.5", "-i", str(master), "-af", "silencedetect=noise=-40dB:d=0.06", "-f", "null", "-"], capture_output=True, text=True)
assert scan.returncode == 0
report["silence_scan_offset_seconds"] = 59
report["silence_scan"] = [line for line in scan.stderr.splitlines() if "silence_" in line]
(PACKET / "input-measurements.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"pins": "pass", "pcm": "exact for both and concatenated", "picture_frames": [154,206], "boundary_windows": report["boundary_windows"]}, indent=2))
