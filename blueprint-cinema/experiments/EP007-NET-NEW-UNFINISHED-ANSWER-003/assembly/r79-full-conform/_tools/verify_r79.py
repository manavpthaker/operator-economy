#!/usr/bin/env python3
"""Verify the EP007 R79 whole-episode owner-review conform."""

from __future__ import annotations

import array
import hashlib
import json
import math
import re
import shutil
import subprocess
import wave
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve()
OUT_DIR = SCRIPT.parent.parent
QA_DIR = OUT_DIR / "qa"
VIDEO = QA_DIR / "ep007-r79-full-review.mp4"
AUDIO = QA_DIR / "ep007-r79-audio-pcm.wav"
EXPECTED_FRAMES = 27_241
EXPECTED_SAMPLES = 54_482_000


def repo_root() -> Path:
    for parent in SCRIPT.parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Repository root not found")


ROOT = repo_root()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def probe(path: Path) -> dict:
    result = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def decoded_audio_samples(path: Path) -> int:
    process = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", "2", "-ar", "48000", "-f", "s16le", "-"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    byte_count = 0
    for chunk in iter(lambda: process.stdout.read(1024 * 1024), b""):
        byte_count += len(chunk)
    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code:
        raise RuntimeError(stderr)
    if byte_count % 4:
        raise RuntimeError(f"Decoded stereo s16 byte count is not sample aligned: {byte_count}")
    return byte_count // 4


def decode_audio_8k_mono(path: Path) -> array.array:
    result = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-xerror",
            "-err_detect",
            "explode",
            "-i",
            str(path),
            "-map",
            "0:a:0",
            "-ac",
            "1",
            "-ar",
            "8000",
            "-f",
            "s16le",
            "-",
        ],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    decoded = array.array("h")
    decoded.frombytes(result.stdout)
    return decoded


def audio_reference_metrics(candidate_path: Path, reference_path: Path) -> dict:
    candidate = decode_audio_8k_mono(candidate_path)
    reference = decode_audio_8k_mono(reference_path)
    compared = min(len(candidate), len(reference), round(EXPECTED_SAMPLES * 8000 / 48000))
    if compared <= 0:
        raise RuntimeError("No decoded audio samples available for comparison")
    candidate = candidate[:compared]
    reference = reference[:compared]
    candidate_energy = sum(value * value for value in candidate)
    reference_energy = sum(value * value for value in reference)
    dot = sum(a * b for a, b in zip(candidate, reference))
    error_energy = sum((a - b) * (a - b) for a, b in zip(candidate, reference))
    correlation = dot / math.sqrt(candidate_energy * reference_energy)
    level_db = 10 * math.log10(candidate_energy / reference_energy)
    snr_db = 10 * math.log10(reference_energy / error_energy)
    return {
        "method": "Full-duration decoded mono 8 kHz signed-16-bit zero-offset comparison over the exact picture interval",
        "compared_samples": compared,
        "zero_lag_correlation": correlation,
        "level_db_vs_pcm_reference": level_db,
        "snr_db_vs_pcm_reference": snr_db,
        "candidate_rms": math.sqrt(candidate_energy / compared),
        "reference_rms": math.sqrt(reference_energy / compared),
    }


def pcm_tail_is_zero(path: Path, tail_samples: int) -> bool:
    with wave.open(str(path), "rb") as source:
        if source.getframerate() != 48_000 or source.getnchannels() != 2 or source.getsampwidth() != 2:
            return False
        if source.getnframes() != EXPECTED_SAMPLES:
            return False
        source.setpos(source.getnframes() - tail_samples)
        return source.readframes(tail_samples) == bytes(tail_samples * source.getnchannels() * source.getsampwidth())


def spatial_sd(frame: bytes) -> float:
    mean = sum(frame) / len(frame)
    return math.sqrt(max(0.0, sum(value * value for value in frame) / len(frame) - mean * mean))


def low_variance_frames(path: Path) -> tuple[list[int], float, dict[int, bytes]]:
    frame_size = 64 * 36
    process = subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-xerror",
            "-err_detect",
            "explode",
            "-i",
            str(path),
            "-an",
            "-vf",
            "scale=64:36,format=gray",
            "-f",
            "rawvideo",
            "-",
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    flagged: list[int] = []
    flagged_gray: dict[int, bytes] = {}
    minimum = float("inf")
    frame_index = 0
    while True:
        frame = process.stdout.read(frame_size)
        if not frame:
            break
        while len(frame) < frame_size:
            remainder = process.stdout.read(frame_size - len(frame))
            if not remainder:
                raise RuntimeError(f"Truncated gray frame {frame_index}")
            frame += remainder
        deviation = spatial_sd(frame)
        minimum = min(minimum, deviation)
        if deviation <= 3:
            flagged.append(frame_index)
            flagged_gray[frame_index] = frame
        frame_index += 1
    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code:
        raise RuntimeError(stderr)
    if frame_index != EXPECTED_FRAMES:
        raise RuntimeError(f"Gray scan decoded {frame_index} frames; expected {EXPECTED_FRAMES}")
    return flagged, minimum, flagged_gray


def contiguous_ranges(frames: list[int]) -> list[list[int]]:
    if not frames:
        return []
    ranges: list[list[int]] = []
    start = previous = frames[0]
    for frame in frames[1:]:
        if frame != previous + 1:
            ranges.append([start, previous + 1])
            start = frame
        previous = frame
    ranges.append([start, previous + 1])
    return ranges


def representative_frames(ranges: list[list[int]]) -> list[int]:
    representatives: list[int] = []
    for start, end in ranges:
        for frame in (start, (start + end - 1) // 2, end - 1):
            if frame not in representatives:
                representatives.append(frame)
    return representatives


def source_match_low_variance_frames(
    segments: list[dict], flagged: list[int], output_gray: dict[int, bytes]
) -> tuple[bool, list[dict]]:
    frame_size = 64 * 36
    comparisons: list[dict] = []
    for segment in segments:
        output_start, output_end = [int(value) for value in segment["output_frames_half_open"]]
        affected = [frame for frame in flagged if output_start <= frame < output_end]
        if not affected:
            continue
        source_start, source_end = [int(value) for value in segment["source_frames_half_open"]]
        source = ROOT / segment["source"]
        result = subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-xerror",
                "-err_detect",
                "explode",
                "-i",
                str(source),
                "-an",
                "-vf",
                f"trim=start_frame={source_start}:end_frame={source_end},setpts=PTS-STARTPTS,scale=64:36,format=gray",
                "-f",
                "rawvideo",
                "-",
            ],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        expected_bytes = (source_end - source_start) * frame_size
        if result.returncode or len(result.stdout) != expected_bytes:
            raise RuntimeError(
                f"Could not decode source comparison for {segment['scene']}: "
                f"{len(result.stdout)} bytes, expected {expected_bytes}; "
                + result.stderr.decode("utf-8", errors="replace")[-1000:]
            )
        for output_frame in affected:
            local_frame = output_frame - output_start
            source_frame = source_start + local_frame
            reference = result.stdout[local_frame * frame_size : (local_frame + 1) * frame_size]
            candidate = output_gray[output_frame]
            mean_absolute_difference = sum(abs(a - b) for a, b in zip(candidate, reference)) / frame_size
            source_deviation = spatial_sd(reference)
            inherited = source_deviation <= 4.0 and mean_absolute_difference <= 2.0
            comparisons.append(
                {
                    "output_frame": output_frame,
                    "scene": segment["scene"],
                    "source_frame": source_frame,
                    "source_spatial_sd": source_deviation,
                    "output_spatial_sd": spatial_sd(candidate),
                    "mean_absolute_gray_difference": mean_absolute_difference,
                    "source_matched_inherited": inherited,
                }
            )
    compared = {item["output_frame"] for item in comparisons}
    return compared == set(flagged) and all(item["source_matched_inherited"] for item in comparisons), comparisons


def loudness_metrics(path: Path) -> dict:
    result = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-map",
            "0:a:0",
            "-af",
            "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
            "-f",
            "null",
            "-",
        ]
    )
    matches = re.findall(r"\{\s*\"input_i\".*?\}", result.stderr, flags=re.DOTALL)
    if result.returncode or not matches:
        raise RuntimeError("Loudness analysis failed: " + result.stderr[-1000:])
    payload = json.loads(matches[-1])
    return {
        "integrated_lufs": float(payload["input_i"]),
        "true_peak_dbtp": float(payload["input_tp"]),
        "loudness_range_lu": float(payload["input_lra"]),
        "threshold_lufs": float(payload["input_thresh"]),
        "method": "FFmpeg loudnorm analysis pass only; no normalization applied to the artifact",
    }


def make_sheet(video: Path, frames: list[int], output: Path, columns: int, rows: int) -> None:
    expression = "+".join(f"eq(n\\,{frame})" for frame in frames)
    command = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(video),
        "-vf",
        f"select='{expression}',scale=320:180:flags=lanczos,tile={columns}x{rows}:padding=4:margin=4:color=0x173530",
        "-frames:v",
        "1",
        str(output),
    ]
    result = run(command)
    if result.returncode:
        raise RuntimeError(result.stderr)


def main() -> int:
    if not VIDEO.is_file() or not AUDIO.is_file():
        raise FileNotFoundError("Run build_r79.py first")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe are required")

    segments = json.loads((OUT_DIR / "SEGMENTS.json").read_text(encoding="utf-8"))["segments"]
    media_probe = probe(VIDEO)
    audio_probe = probe(AUDIO)
    video_stream = next(item for item in media_probe["streams"] if item["codec_type"] == "video")
    encoded_audio_stream = next(item for item in media_probe["streams"] if item["codec_type"] == "audio")
    pcm_stream = next(item for item in audio_probe["streams"] if item["codec_type"] == "audio")

    checks = {
        "video_frame_count": int(video_stream["nb_frames"]) == EXPECTED_FRAMES,
        "video_rate": video_stream["r_frame_rate"] == "24/1",
        "video_dimensions": [int(video_stream["width"]), int(video_stream["height"])] == [1280, 720],
        "video_pixel_format": video_stream.get("pix_fmt") == "yuv420p",
        "video_color_range": video_stream.get("color_range") == "tv",
        "video_color_primaries": video_stream.get("color_primaries") == "bt709",
        "video_color_transfer": video_stream.get("color_transfer") == "bt709",
        "video_color_space": video_stream.get("color_space") == "bt709",
        "audio_rate": int(encoded_audio_stream["sample_rate"]) == 48_000,
        "audio_channels": int(encoded_audio_stream["channels"]) == 2,
        "pcm_sample_count": int(pcm_stream["duration_ts"]) == EXPECTED_SAMPLES,
        "pcm_exact_zero_tail_1481_samples": pcm_tail_is_zero(AUDIO, 1481),
    }

    decode = run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-xerror",
            "-err_detect",
            "explode",
            "-i",
            str(VIDEO),
            "-map",
            "0:v:0",
            "-map",
            "0:a:0",
            "-f",
            "null",
            "-",
        ]
    )
    checks["complete_decode"] = decode.returncode == 0

    decoded_samples = decoded_audio_samples(VIDEO)
    checks["encoded_audio_decodes_through_picture_end"] = decoded_samples >= EXPECTED_SAMPLES

    audio_comparison = audio_reference_metrics(VIDEO, AUDIO)
    checks["audio_reference_comparison_pass"] = (
        audio_comparison["zero_lag_correlation"] > 0.999
        and abs(audio_comparison["level_db_vs_pcm_reference"]) < 0.1
        and audio_comparison["snr_db_vs_pcm_reference"] > 35
    )

    near_uniform, minimum_frame_sd, near_uniform_gray = low_variance_frames(VIDEO)
    low_variance_source_match, low_variance_comparisons = source_match_low_variance_frames(
        segments, near_uniform, near_uniform_gray
    )
    checks["low_variance_frames_are_source_matched_inherited_picture"] = low_variance_source_match
    loudness = loudness_metrics(VIDEO)
    checks["loudness_and_true_peak_measured"] = all(math.isfinite(value) for key, value in loudness.items() if key != "method")

    midpoints = [(int(item["output_frames_half_open"][0]) + int(item["output_frames_half_open"][1]) - 1) // 2 for item in segments]
    boundaries: list[int] = []
    for item in segments[1:]:
        boundary = int(item["output_frames_half_open"][0])
        boundaries.extend([boundary - 1, boundary])
    make_sheet(VIDEO, midpoints, QA_DIR / "contact-sheet.jpg", 4, 4)
    make_sheet(VIDEO, boundaries, QA_DIR / "boundary-sheet.jpg", 5, 6)
    low_variance_ranges = contiguous_ranges(near_uniform)
    low_variance_representatives = representative_frames(low_variance_ranges)
    make_sheet(
        VIDEO,
        low_variance_representatives,
        QA_DIR / "documented-low-variance-sheet.jpg",
        4,
        math.ceil(len(low_variance_representatives) / 4),
    )

    output_hash = sha256(VIDEO)
    verification = {
        "record_type": "ep007_r79_review_conform_verification",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if all(checks.values()) else "fail",
        "decision_event_id": "r79-whole-episode-conform-plan-v2",
        "artifact": {
            "path": rel(VIDEO),
            "sha256": output_hash,
            "size_bytes": VIDEO.stat().st_size,
            "duration_seconds": EXPECTED_FRAMES / 24,
            "frames": int(video_stream["nb_frames"]),
            "fps": video_stream["r_frame_rate"],
            "dimensions": [int(video_stream["width"]), int(video_stream["height"])],
        },
        "pcm_reference": {
            "path": rel(AUDIO),
            "sha256": sha256(AUDIO),
            "samples": int(pcm_stream["duration_ts"]),
            "sample_rate": int(pcm_stream["sample_rate"]),
            "channels": int(pcm_stream["channels"]),
        },
        "encoded_audio_decoded_samples": decoded_samples,
        "loudness": loudness,
        "low_variance_scan": {
            "method": "Every decoded frame scaled to 64x36 gray; spatial standard deviation <= 3 is flagged",
            "actual_frames": near_uniform,
            "actual_half_open_ranges": low_variance_ranges,
            "minimum_frame_sd": minimum_frame_sd,
            "classification": "Every flagged output frame must match its exact pinned source frame after the expected CRF-16 conform transcode.",
            "source_match_thresholds": {
                "source_spatial_sd_max": 4.0,
                "mean_absolute_gray_difference_max": 2.0
            },
            "source_comparisons": low_variance_comparisons,
        },
        "audio_reference_comparison": audio_comparison,
        "checks": checks,
        "visual_review_artifacts": [
            rel(QA_DIR / "contact-sheet.jpg"),
            rel(QA_DIR / "boundary-sheet.jpg"),
            rel(QA_DIR / "documented-low-variance-sheet.jpg"),
        ],
        "limitations": [
            "Automated verification and contact sheets do not replace uninterrupted human audiovisual review.",
            "The R58 prefix retains its recorded inherited R39 and R47 review-status exceptions; R79 does not invent new scene-level verdicts for those sources.",
            "This file is a conform-reference and owner-review candidate, not a canonical Resolve finishing master, whole-episode lock, release or publication approval.",
        ],
    }
    write_json(OUT_DIR / "VERIFICATION.json", verification)
    print(json.dumps(verification, indent=2))
    return 0 if verification["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
