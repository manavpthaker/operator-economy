#!/usr/bin/env python3
"""Build the EP007 R79 uninterrupted owner-review conform.

This is an exact assembly of already locked picture sources. It deliberately
does not create new creative transitions, retime scenes, or reuse per-scene
encoded audio. The output remains a review conform pending whole-episode owner
acceptance and canonical Resolve finishing.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve()
OUT_DIR = SCRIPT.parent.parent
QA_DIR = OUT_DIR / "qa"
LOG_DIR = OUT_DIR / "_tools" / "logs"


def repo_root() -> Path:
    for parent in SCRIPT.parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Repository root not found")


ROOT = repo_root()
BASE_MAP = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R77-FULL-ASSEMBLY-MAP/ASSEMBLY-MAP.json"
PREFIX = ROOT / "blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r58-full-episode-through-s13/qa/full.mp4"
MASTER_AUDIO = ROOT / "operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav"
S15 = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R78-TOOL-INSERT-MOBILE-BUILD/projects/s15-mobile/qa/s15-mobile-review.mp4"
S16 = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R78-TOOL-INSERT-MOBILE-BUILD/projects/s16-mobile-r7/qa/s16-mobile-r7-review.mp4"
S17_CONTEXT = ROOT / "blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r76-s17-context/qa/context.mp4"

EXPECTED_OVERRIDES = {
    "S15": "b676995321b8f5e134b17e27f78b406ad94140b1a9dde8eb3b5ee0555bef6710",
    "S16": "eb8767961ba4ddeebc2b502c5672019d81ec970e96b3141318b340ee9e6223ba",
    "S17": "a10d322cc96198642be1b74edc3f3207b10c5f439fe10124f8cd5aa0d65bc7df",
}

EXPECTED_FRAMES = 27_241
EXPECTED_AUDIO_SAMPLES = 54_482_000
FPS = 24
WIDTH = 1280
HEIGHT = 720


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_logged(command: list[str], log_name: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / log_name
    with log_path.open("w", encoding="utf-8") as log:
        log.write("COMMAND\n")
        log.write(json.dumps(command, ensure_ascii=False) + "\n\nOUTPUT\n")
        log.flush()
        result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}); see {rel(log_path)}")


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def frame_count(media_probe: dict) -> int:
    stream = next(item for item in media_probe["streams"] if item["codec_type"] == "video")
    return int(stream["nb_frames"])


def build_segment_map() -> dict:
    source_map = json.loads(BASE_MAP.read_text(encoding="utf-8"))
    updated = copy.deepcopy(source_map)
    updated["record_type"] = "owner_locked_full_review_conform_map"
    updated["created_at_utc"] = datetime.now(timezone.utc).isoformat()
    updated["status"] = "R79 owner-review conform map; all scene sources owner locked; whole-episode acceptance, Resolve finishing, release and publication pending"
    updated["supersedes_map"] = rel(BASE_MAP)
    updated["assembly_decision_event_id"] = "r79-whole-episode-conform-plan-v2"
    updated["audio_plan"] = {
        "prefix_source": rel(PREFIX),
        "prefix_decoded_samples_half_open": [0, 26_752_000],
        "master_source": rel(MASTER_AUDIO),
        "master_samples_half_open": [26_892_000, 54_620_519],
        "final_zero_pad_samples": 1_481,
        "output_samples": EXPECTED_AUDIO_SAMPLES,
        "sample_rate": 48_000,
        "channels": 2,
        "purpose": "Preserve the R58 presenter-level fixes and accepted S12 timing, then continue with the locked narration master through exact EOF.",
    }

    rebuilt: list[dict] = []
    for original in updated["segments"]:
        scene = original["scene"]
        if scene == "S15":
            item = copy.deepcopy(original)
            item.update(
                {
                    "source": rel(S15),
                    "sha256": EXPECTED_OVERRIDES["S15"],
                    "source_frames_half_open": [0, 1368],
                    "source_total_frames": 1368,
                    "status": "owner accepted R78 actual-tool mobile framing",
                    "acceptance_evidence": "r78-owner-s15-s16-mobile-lock-v1",
                }
            )
            rebuilt.append(item)
            continue
        if scene == "S16":
            item = copy.deepcopy(original)
            item.update(
                {
                    "source": rel(S16),
                    "sha256": EXPECTED_OVERRIDES["S16"],
                    "source_frames_half_open": [0, 1293],
                    "source_total_frames": 1293,
                    "status": "owner accepted R78 actual-tool mobile framing",
                    "acceptance_evidence": "r78-owner-s15-s16-mobile-lock-v1",
                }
            )
            rebuilt.append(item)
            continue
        if scene == "S17-P1":
            item = copy.deepcopy(original)
            item.update(
                {
                    "scene": "S17",
                    "source": rel(S17_CONTEXT),
                    "sha256": EXPECTED_OVERRIDES["S17"],
                    "source_frames_half_open": [192, 1803],
                    "source_total_frames": 1803,
                    "frame_count": 1611,
                    "master_frames_half_open": [17877, 19488],
                    "master_seconds_half_open": [744.875, 812.0],
                    "output_frames_half_open": [17807, 19418],
                    "output_seconds_half_open": [17807 / 24, 19418 / 24],
                    "status": "owner accepted R62 P1/P2 plus R76 presenter C, carried by exact reviewed R76 context",
                    "acceptance_evidence": "r62-owner-s17-lock-v1 + r76-owner-s17-c-lock-v1",
                    "audio_plan": "continuous R79 audio master; ignore context AAC",
                    "dimensions": [1280, 720],
                }
            )
            rebuilt.append(item)
            continue
        if scene in {"S17-C", "S17-P2"}:
            continue
        rebuilt.append(copy.deepcopy(original))

    updated["segments"] = rebuilt
    updated["expected_output"] = {
        "frames": EXPECTED_FRAMES,
        "fps": FPS,
        "duration_seconds": EXPECTED_FRAMES / FPS,
        "timecode_24fps": "00:18:55:01",
        "dimensions": [WIDTH, HEIGHT],
    }
    updated["scope_limits"] = [
        "R79 is the uninterrupted owner-review conform and a conform-reference candidate.",
        "Technical verification cannot establish audience comprehension or whole-episode owner acceptance.",
        "DaVinci Resolve is not currently installed or represented by a project/interchange package in this workspace, so R79 is not claimed as the canonical Resolve finishing master.",
        "No release, publication, upload, commit or push is performed by this build.",
    ]
    return updated


def validate_sources(segment_map: dict) -> list[dict]:
    checks: list[dict] = []
    expected_output_start = 0
    for segment in segment_map["segments"]:
        path = ROOT / segment["source"]
        if not path.is_file():
            raise FileNotFoundError(path)
        actual_hash = sha256(path)
        if actual_hash != segment["sha256"]:
            raise RuntimeError(f"Hash mismatch for {segment['scene']}: {actual_hash}")
        media_probe = probe(path)
        video = next(item for item in media_probe["streams"] if item["codec_type"] == "video")
        actual_frames = int(video["nb_frames"])
        start, end = segment["source_frames_half_open"]
        if end > actual_frames or end - start != int(segment["frame_count"]):
            raise RuntimeError(f"Invalid source range for {segment['scene']}")
        if [int(video["width"]), int(video["height"])] != [WIDTH, HEIGHT]:
            raise RuntimeError(f"Unexpected dimensions for {segment['scene']}: {video['width']}x{video['height']}")
        if video["r_frame_rate"] != "24/1":
            raise RuntimeError(f"Unexpected frame rate for {segment['scene']}: {video['r_frame_rate']}")
        output_start, output_end = segment["output_frames_half_open"]
        if output_start != expected_output_start or output_end - output_start != int(segment["frame_count"]):
            raise RuntimeError(f"Non-contiguous output range for {segment['scene']}")
        expected_output_start = output_end
        checks.append(
            {
                "scene": segment["scene"],
                "source": segment["source"],
                "expected_sha256": segment["sha256"],
                "actual_sha256": actual_hash,
                "source_frames": actual_frames,
                "selected_frames_half_open": [start, end],
                "output_frames_half_open": [output_start, output_end],
                "pass": True,
            }
        )
    if expected_output_start != EXPECTED_FRAMES:
        raise RuntimeError(f"Expected {EXPECTED_FRAMES} output frames; mapped {expected_output_start}")
    return checks


def build_audio(ffmpeg: str, force: bool) -> Path:
    output = QA_DIR / "ep007-r79-audio-pcm.wav"
    if output.exists() and not force:
        return output
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-v",
        "error",
        "-xerror",
        "-err_detect",
        "explode",
        "-i",
        str(PREFIX),
        "-i",
        str(MASTER_AUDIO),
        "-filter_complex",
        (
            "[0:a:0]atrim=start_sample=0:end_sample=26752000,asetpts=N/SR/TB,"
            "aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo[prefix];"
            "[1:a:0]atrim=start_sample=26892000:end_sample=54620519,asetpts=N/SR/TB,"
            "pan=stereo|c0=c0|c1=c0,"
            "aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo[tail];"
            "aevalsrc=0|0:s=48000,atrim=start_sample=0:end_sample=1481,asetpts=N/SR/TB[silence];"
            "[prefix][tail][silence]concat=n=3:v=0:a=1[outa]"
        ),
        "-map",
        "[outa]",
        "-c:a",
        "pcm_s16le",
        str(output),
    ]
    run_logged(command, "build-audio.log")
    audio_probe = probe(output)
    stream = next(item for item in audio_probe["streams"] if item["codec_type"] == "audio")
    if int(stream["duration_ts"]) != EXPECTED_AUDIO_SAMPLES:
        raise RuntimeError(f"Audio sample count mismatch: {stream['duration_ts']}")
    return output


def build_video(ffmpeg: str, segment_map: dict, audio: Path, force: bool) -> Path:
    output = QA_DIR / "ep007-r79-full-review.mp4"
    if output.exists() and not force:
        return output
    command: list[str] = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-v",
        "error",
        "-xerror",
        "-err_detect",
        "explode",
        "-filter_complex_threads",
        "1",
    ]
    for segment in segment_map["segments"]:
        command.extend(["-i", str(ROOT / segment["source"])])
    audio_index = len(segment_map["segments"])
    command.extend(["-i", str(audio)])

    filters: list[str] = []
    labels: list[str] = []
    for index, segment in enumerate(segment_map["segments"]):
        start, end = segment["source_frames_half_open"]
        label = f"v{index}"
        filters.append(
            f"[{index}:v:0]trim=start_frame={start}:end_frame={end},"
            f"setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
        )
        labels.append(f"[{label}]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[outv]")
    filters.append(f"[{audio_index}:a:0]apad=pad_len=4096[aout]")
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-map",
            "[aout]",
            "-frames:v",
            str(EXPECTED_FRAMES),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "16",
            "-profile:v",
            "high",
            "-level:v",
            "4.0",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            "-fps_mode",
            "cfr",
            "-g",
            "48",
            "-keyint_min",
            "48",
            "-sc_threshold",
            "0",
            "-video_track_timescale",
            "12288",
            "-color_range",
            "tv",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            "-colorspace",
            "bt709",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-shortest",
            "-map_metadata",
            "-1",
            "-metadata",
            "title=EP007 R79 whole-episode owner-review conform",
            "-metadata",
            "comment=Review candidate only; not whole-episode locked or released",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    run_logged(command, "build-video.log")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Rebuild existing generated media")
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe are required")

    QA_DIR.mkdir(parents=True, exist_ok=True)
    segment_map = build_segment_map()
    source_checks = validate_sources(segment_map)
    write_json(OUT_DIR / "SEGMENTS.json", segment_map)
    write_json(OUT_DIR / "SOURCE-CHECK.json", {"status": "pass", "checks": source_checks})

    audio = build_audio(ffmpeg, args.force)
    video = build_video(ffmpeg, segment_map, audio, args.force)

    build_record = {
        "record_type": "ep007_r79_review_conform_build",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "built_pending_verification_and_owner_review",
        "decision_event_id": "r79-whole-episode-conform-plan-v2",
        "segments": rel(OUT_DIR / "SEGMENTS.json"),
        "audio": {
            "path": rel(audio),
            "sha256": sha256(audio),
            "samples": EXPECTED_AUDIO_SAMPLES,
            "sample_rate": 48_000,
            "channels": 2,
        },
        "review_video": {
            "path": rel(video),
            "sha256": sha256(video),
            "expected_frames": EXPECTED_FRAMES,
            "fps": FPS,
            "dimensions": [WIDTH, HEIGHT],
        },
        "tool_versions": {
            "ffmpeg": subprocess.run([ffmpeg, "-version"], text=True, capture_output=True, check=True).stdout.splitlines()[0],
            "ffprobe": subprocess.run([ffprobe, "-version"], text=True, capture_output=True, check=True).stdout.splitlines()[0],
        },
        "scope_limits": segment_map["scope_limits"],
    }
    write_json(OUT_DIR / "BUILD.json", build_record)
    print(json.dumps(build_record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
