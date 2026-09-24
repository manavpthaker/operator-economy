"""Score presenter natives against the locked narration: word lag and held-pose runs.

Usage: python3 compare.py narration.wav A=native_a.mp4 B=native_b.mp4 ...
Writes COMPARISON.json next to this script.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

MODEL = Path.home() / "whisper-models" / "ggml-small.en.bin"
HERE = Path(__file__).parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(media: Path) -> list[tuple[str, float]]:
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(media), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
        subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(wav), "-oj", "-of", str(Path(tmp) / "t"), "-ml", "1", "-np"],
                       check=True, capture_output=True)
        data = json.loads((Path(tmp) / "t.json").read_text())["transcription"]
    out = []
    for seg in data:
        token = "".join(ch for ch in seg["text"].lower() if ch.isalnum())
        if token:
            out.append((token, seg["offsets"]["from"] / 1000))
    return out


def lag(narration: list, native: list) -> dict:
    matcher = difflib.SequenceMatcher(a=[w for w, _ in narration], b=[w for w, _ in native], autojunk=False)
    pairs = []
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            word, t_n = narration[block.a + k]
            pairs.append({"word": word, "narration_s": t_n, "native_s": native[block.b + k][1],
                          "lag_s": round(native[block.b + k][1] - t_n, 2)})
    lags = [abs(p["lag_s"]) for p in pairs]
    return {
        "matched_words": len(pairs),
        "narration_words": len(narration),
        "native_transcript": " ".join(w for w, _ in native),
        "mean_abs_lag_s": round(sum(lags) / len(lags), 3) if lags else None,
        "max_abs_lag_s": round(max(lags), 2) if lags else None,
        "pairs": pairs,
    }


def held_runs(media: Path, speech_end_s: float) -> list[dict]:
    """Runs of >= 5 near-duplicate frames (about 208 ms at 24 fps) while speech is still going.

    0.1 mean grey-level change sits well under the ~0.2 compression noise floor of a
    live seated take, so only genuinely frozen pictures count.
    """
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(media), "-vf", "scale=192:108,format=gray", "-f", "rawvideo", "-"],
                         check=True, capture_output=True).stdout
    size = 192 * 108
    fps = 24.0
    frames = [raw[i:i + size] for i in range(0, len(raw) - size + 1, size)]
    runs, start = [], None
    for i in range(1, len(frames) + 1):
        still = i < len(frames) and sum(abs(a - b) for a, b in zip(frames[i], frames[i - 1])) / size < 0.1
        if still and start is None:
            start = i - 1
        if not still and start is not None:
            if i - start >= 5 and start / fps < speech_end_s:
                runs.append({"start_s": round(start / fps, 2), "frames": i - start})
            start = None
    return runs


def main() -> None:
    narration_path = Path(sys.argv[1])
    narration = words(narration_path)
    speech_end = narration[-1][1] + 0.5
    result = {"narration": {"path": str(narration_path), "sha256": sha(narration_path), "words": len(narration)}, "arms": {}}
    for spec in sys.argv[2:]:
        label, path = spec.split("=", 1)
        media = Path(path)
        result["arms"][label] = {"path": str(media), "sha256": sha(media), **lag(narration, words(media)),
                                 "held_pose_runs_during_speech": held_runs(media, speech_end)}
    (HERE / "COMPARISON.json").write_text(json.dumps(result, indent=2) + "\n")
    for label, arm in result["arms"].items():
        print(f"{label}: matched {arm['matched_words']}/{arm['narration_words']}, mean |lag| {arm['mean_abs_lag_s']}s, "
              f"max {arm['max_abs_lag_s']}s, held runs {arm['held_pose_runs_during_speech']}")
        print(f"   heard: {arm['native_transcript']}")


if __name__ == "__main__":
    main()
