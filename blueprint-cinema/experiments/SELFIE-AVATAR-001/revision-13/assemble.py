#!/usr/bin/env python3
"""Append a silent 144-frame closing plate; run only in the Higgsfield sandbox.

Usage: python assemble.py accepted-r11.mp4 closing.mp4 full.mp4 ASSEMBLY-QA.json
No encoding fallback: any failed preservation check exits nonzero with a report.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

ACCEPTED_SHA = "888a96f547cd15ef0690c876a5248b5f8ebeffd9ce0ac4bb784c476a11b0efba"
BODY_FRAMES, CLOSE_FRAMES, FPS = 1322, 144, 24


def run(args):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f"{args[0]} failed ({p.returncode}): "
                           + p.stderr.decode(errors="replace")[-5000:])
    return p.stdout


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-count_frames",
                           "-show_streams", "-show_format", "-of", "json", str(path)]))


def video_contract(info, frames):
    streams = [s for s in info["streams"] if s["codec_type"] == "video"]
    require(len(streams) == 1, "Expected exactly one video stream")
    v = streams[0]
    require((v["codec_name"], v["width"], v["height"], v["pix_fmt"])
            == ("h264", 720, 1280, "yuv420p"), "Video format mismatch")
    require(Fraction(v["r_frame_rate"]) == FPS, "Frame rate is not 24 fps")
    require(int(v["nb_read_frames"]) == frames, f"Expected {frames} decoded frames")
    require(abs(float(v["duration"]) - frames / FPS) < 0.001,
            "Video duration does not match exact frame count")
    return {key: v.get(key) for key in ("codec_name", "profile", "width", "height",
            "pix_fmt", "r_frame_rate", "avg_frame_rate", "time_base", "start_time",
            "duration", "nb_read_frames")}


def frame_records(path):
    raw = run(["ffmpeg", "-v", "error", "-xerror", "-err_detect", "explode",
               "-i", str(path), "-map", "0:v:0", "-an", "-fps_mode", "passthrough",
               "-pix_fmt", "yuv420p", "-f", "framemd5", "-"]).decode()
    lines = [line for line in raw.splitlines() if line and not line.startswith("#")]
    records = [[part.strip() for part in line.split(",")] for line in lines]
    require(all(len(r) == 6 for r in records), "Unexpected framemd5 record")
    # Retain presentation timestamps and pixel sizes alongside each decoded hash.
    return records


def frame_summary(records):
    pixel_records = "\n".join(f"{r[4]}:{r[5]}" for r in records).encode()
    return {"frames": len(records), "decoded_frame_sequence_sha256":
            hashlib.sha256(pixel_records).hexdigest()}


def audio_fingerprint(path):
    encoded = run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
                   "-c:a", "copy", "-f", "data", "-"])
    pcm = run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-map", "0:a:0",
               "-c:a", "pcm_s16le", "-f", "s16le", "-"])
    packet_info = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_packets", "-show_entries", "packet=pts,dts,duration,size",
        "-of", "json", str(path)]))["packets"]
    packet_json = json.dumps(packet_info, sort_keys=True, separators=(",", ":")).encode()
    return {"aac_packet_bytes_sha256": hashlib.sha256(encoded).hexdigest(),
            "aac_packet_bytes": len(encoded), "aac_packet_count": len(packet_info),
            "aac_packet_timing_sha256": hashlib.sha256(packet_json).hexdigest(),
            "decoded_pcm_s16le_sha256": hashlib.sha256(pcm).hexdigest(),
            "decoded_pcm_bytes": len(pcm)}


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    source, closing, output, report_path = map(lambda p: Path(p).resolve(), sys.argv[1:])
    report = {"status": "running", "at": datetime.now(timezone.utc).isoformat(),
              "method": "H264 packet-copy append, then separate original-AAC packet-copy mux",
              "closing_audio": "Intentionally silent; original audio ends before closing plate"}
    try:
        require(len({source, closing, output, report_path}) == 4, "Paths must be distinct")
        require(not output.exists(), "Refusing to overwrite an existing output")
        report["accepted_r11_sha256"] = sha(source)
        require(report["accepted_r11_sha256"] == ACCEPTED_SHA, "Accepted R11 SHA mismatch")
        report["closing_sha256"] = sha(closing)
        source_info, closing_info = probe(source), probe(closing)
        report["accepted_video"] = video_contract(source_info, BODY_FRAMES)
        report["closing_video"] = video_contract(closing_info, CLOSE_FRAMES)
        source_audio = [s for s in source_info["streams"] if s["codec_type"] == "audio"]
        require(len(source_audio) == 1 and source_audio[0]["codec_name"] == "aac",
                "Expected one original AAC audio stream")
        output.parent.mkdir(parents=True, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix="r13-append-", dir=output.parent))
        for input_path, name in ((source, "body.mp4"), (closing, "closing.mp4")):
            run(["ffmpeg", "-v", "error", "-xerror", "-i", str(input_path),
                 "-map", "0:v:0", "-an", "-c:v", "copy", "-video_track_timescale", "12288",
                 str(work / name)])
        manifest = work / "concat.txt"
        manifest.write_text("ffconcat version 1.0\nfile 'body.mp4'\nfile 'closing.mp4'\n")
        picture = work / "picture.mp4"
        run(["ffmpeg", "-v", "error", "-xerror", "-f", "concat", "-safe", "0",
             "-i", str(manifest), "-map", "0:v:0", "-an", "-c:v", "copy",
             "-video_track_timescale", "12288", str(picture)])
        # Never combine an encoding frame limit with copied audio. Do not use -shortest.
        run(["ffmpeg", "-v", "error", "-xerror", "-i", str(picture), "-i", str(source),
             "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-map_metadata", "-1",
             "-movflags", "+faststart", str(output)])
        run(["ffmpeg", "-v", "error", "-xerror", "-err_detect", "explode",
             "-i", str(output), "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"])
        report["strict_decode_passed"] = True
        final_info = probe(output)
        report["final_video"] = video_contract(final_info, BODY_FRAMES + CLOSE_FRAMES)
        report["final_format_duration_seconds"] = float(final_info["format"]["duration"])
        require(abs(report["final_format_duration_seconds"] - (BODY_FRAMES + CLOSE_FRAMES) / FPS) < 0.002,
                "Container duration mismatch")
        before, card, after = map(frame_records, (source, closing, output))
        require(len(before) == BODY_FRAMES and len(card) == CLOSE_FRAMES
                and len(after) == BODY_FRAMES + CLOSE_FRAMES, "Decoded frame count mismatch")
        require(before == after[:BODY_FRAMES],
                "Accepted picture pixels, frame sizes, or presentation timing changed")
        require([r[4:] for r in card] == [r[4:] for r in after[BODY_FRAMES:]],
                "Closing pixels or order changed during packet-copy append")
        require([int(r[2]) for r in after] == list(range(BODY_FRAMES + CLOSE_FRAMES)),
                "Video presentation timestamps are not continuous 24 fps")
        report["accepted_picture_prefix"] = frame_summary(before)
        report["closing_picture_tail"] = frame_summary(card)
        report["accepted_decoded_picture_and_timing_preserved"] = True
        report["closing_decoded_picture_preserved"] = True
        audio_before, audio_after = map(audio_fingerprint, (source, output))
        report["original_audio"] = audio_before
        report["final_audio"] = audio_after
        require(audio_before == audio_after,
                "Original AAC bytes, packet timing, or decoded PCM changed")
        report["original_audio_packets_and_pcm_preserved"] = True
        report.update(status="passed", output_sha256=sha(output), output_bytes=output.stat().st_size)
    except Exception as exc:
        report.update(status="failed", error=str(exc))
        raise
    finally:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, separators=(",", ":")))


if __name__ == "__main__":
    main()
