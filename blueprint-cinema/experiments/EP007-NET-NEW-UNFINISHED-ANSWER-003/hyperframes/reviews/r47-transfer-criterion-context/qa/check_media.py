#!/usr/bin/env python3
"""Check the finished R47 context assembly; requires ffmpeg, ffprobe and numpy.

This detects encoding/placement errors, not performance or lip-sync quality.
Missing presenter files are an error, never replaced with placeholder media.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FPS = 24
RATE = 48000
LEAD_FRAMES = 2212
TAIL_FRAMES = 269
FRAMES = LEAD_FRAMES + TAIL_FRAMES
LEAD_SAMPLES = LEAD_FRAMES * RATE // FPS
TAIL_SAMPLES = TAIL_FRAMES * RATE // FPS
ACCEPTED_SHA = "02204facdb76020d07261eeabed035b8e9171f44f00dc40f571e22badc9c2a42"


def run(*args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def probe(path):
    return json.loads(run("ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(path)))


def samples(path):
    info = json.loads(run("ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels", "-of", "json", str(path)))
    channels = info["streams"][0]["channels"]
    if channels not in (1, 2):
        raise ValueError(f"Unsupported comparison channel layout: {channels} channels in {path}")
    # Default ffmpeg stereo-to-mono conversion sums with sqrt(1/2) weights.
    # That artificially raises a dual-mono reference by sqrt(2) against a mono WAV.
    channel_filter = ["-af", "pan=mono|c0=0.5*c0+0.5*c1"] if channels == 2 else []
    return np.frombuffer(run("ffmpeg", "-v", "error", "-i", str(path), "-vn", *channel_filter, "-ac", "1", "-ar", str(RATE), "-f", "f32le", "pipe:1"), dtype="<f4")


def gray_frames(path):
    raw = run("ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf", "scale=160:90", "-pix_fmt", "gray", "-f", "rawvideo", "pipe:1")
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, 90, 160)


def one_frame(path, number):
    raw = run("ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf", f"select=eq(n\\,{number}),scale=160:90", "-frames:v", "1", "-pix_fmt", "gray", "-f", "rawvideo", "pipe:1")
    return np.frombuffer(raw, dtype=np.uint8).reshape(90, 160)


def corr(a, b):
    n = min(len(a), len(b))
    if n < 2 or np.std(a[:n]) == 0 or np.std(b[:n]) == 0:
        return None
    return float(np.corrcoef(a[:n], b[:n])[0, 1])


def placement_windows(actual, reference, base, starts):
    """Measure placement independently in separated one-second speech windows.

    Search ±50 ms so an out-of-tolerance edit is detected rather than clamped to
    the allowed ±1 ms. The caller separately applies the 48-sample threshold.
    """
    rows = []
    radius = RATE // 20
    for seconds in starts:
        i = round(seconds * RATE)
        target = reference[i:i + RATE].astype(float)
        window = actual[base + i - radius:base + i + RATE + radius].astype(float)
        nfft = 1 << (len(window) + len(target) - 2).bit_length()
        convolution = np.fft.irfft(np.fft.rfft(window, nfft) * np.fft.rfft(target[::-1], nfft), nfft)
        valid = convolution[len(target) - 1:len(window)]
        lag = int(np.argmax(valid)) - radius
        matched = actual[base + i + lag:base + i + lag + RATE].astype(float)
        gain = float(np.dot(matched, target) / np.dot(target, target))
        rows.append({"reference_seconds": seconds, "lag_samples": lag, "lag_ms": lag / RATE * 1000,
                     "aligned_correlation": corr(matched, target), "gain": gain,
                     "gain_db": float(20 * np.log10(gain)),
                     "gain_normalized_rmse": float(np.sqrt(np.mean((matched - gain * target) ** 2)))})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("render", nargs="?", type=Path, default=ROOT / "qa/r47-transfer-criterion-context.mp4")
    parser.add_argument("--report", type=Path, default=ROOT / "qa/MEDIA-CHECK.json")
    args = parser.parse_args()
    accepted = ROOT / "public/media/accepted-context.mp4"
    picture = ROOT / "public/media/transfer-criterion.mp4"
    audio = ROOT / "public/audio/transfer-criterion.wav"
    required = [accepted, picture, audio, args.render]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        parser.error("Required real media missing: " + ", ".join(missing))

    src_sha = hashlib.sha256(accepted.read_bytes()).hexdigest()
    metadata = probe(args.render)
    picture_metadata = probe(picture)
    stream = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    tail_stream = next(s for s in picture_metadata["streams"] if s["codec_type"] == "video")
    frames = gray_frames(args.render)
    blank = np.flatnonzero(frames.std(axis=(1, 2)) < 1.0).tolist()
    lead_audio = samples(accepted)
    tail_audio = samples(audio)
    expected = np.concatenate([lead_audio[:LEAD_SAMPLES], tail_audio[:TAIL_SAMPLES]])
    actual = samples(args.render)
    n = min(len(actual), len(expected))
    global_corr = corr(actual[:n], expected[:n])
    lo, hi = LEAD_SAMPLES - RATE, LEAD_SAMPLES + RATE
    join_corr = corr(actual[lo:hi], expected[lo:hi])
    lead_windows = placement_windows(actual, lead_audio, 0, [5, 30, 80, 90])
    tail_windows = placement_windows(actual, tail_audio, LEAD_SAMPLES, [0.25, 2, 5, 8.5])
    tail_lags = [w["lag_samples"] for w in tail_windows]
    tail_lag = int(np.median(tail_lags))
    # Keep the ideal zero-lag result above, then compare to the measured placement.
    # This accommodates bounded mixer quantization; it never retimes output media.
    placed_reference = np.zeros(LEAD_SAMPLES + TAIL_SAMPLES, dtype=np.float32)
    placed_reference[:LEAD_SAMPLES] = lead_audio[:LEAD_SAMPLES]
    tail_start = LEAD_SAMPLES + tail_lag
    tail_end = min(len(placed_reference), tail_start + len(tail_audio))
    placed_reference[tail_start:tail_end] += tail_audio[:tail_end - tail_start]
    placed_corr = corr(actual, placed_reference)
    placed_join_corr = corr(actual[lo:hi], placed_reference[lo:hi])
    boundary_mae = {
        "before": float(np.abs(frames[LEAD_FRAMES - 1].astype(float) - one_frame(accepted, LEAD_FRAMES - 1)).mean()) if len(frames) >= LEAD_FRAMES else None,
        "after": float(np.abs(frames[LEAD_FRAMES].astype(float) - one_frame(picture, 0)).mean()) if len(frames) > LEAD_FRAMES else None,
    }
    stream_rate = stream["avg_frame_rate"].split("/")
    measured_fps = int(stream_rate[0]) / int(stream_rate[1])
    checks = {
        "accepted_source_sha256_matches": src_sha == ACCEPTED_SHA,
        "frame_count_matches": len(frames) == FRAMES,
        "picture_dimensions_match": (stream["width"], stream["height"]) == (1280, 720),
        "fps_matches": abs(measured_fps - FPS) < 1e-9,
        "presentation_duration_matches": abs(float(stream["duration"]) - FRAMES / FPS) <= 1 / FPS,
        "new_presenter_has_269_frames": int(tail_stream.get("nb_read_frames", -1)) == TAIL_FRAMES,
        "no_uniform_blank_frames": not blank,
        "reference_prefix_has_required_samples": len(lead_audio) >= LEAD_SAMPLES,
        "reference_tail_has_exact_samples": len(tail_audio) == TAIL_SAMPLES,
        "audio_decode_length_within_codec_padding": abs(len(actual) - (LEAD_SAMPLES + TAIL_SAMPLES)) <= 2048,
        "accepted_audio_has_no_measured_offset": all(w["lag_samples"] == 0 for w in lead_windows),
        "tail_audio_placement_within_one_millisecond": all(abs(lag) <= 48 for lag in tail_lags),
        "tail_audio_placement_consistent": max(tail_lags) - min(tail_lags) <= 1,
        "audio_matches_within_placement_tolerance": placed_corr is not None and placed_corr >= 0.99,
        "join_audio_matches_within_placement_tolerance": placed_join_corr is not None and placed_join_corr >= 0.98,
        "join_picture_matches_sources": all(v is not None and v < 5 for v in boundary_mae.values()),
    }
    report = {
        "result": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "expected_frames": FRAMES,
        "decoded_frames": len(frames),
        "uniform_blank_frame_indices": blank,
        "expected_duration_seconds": FRAMES / FPS,
        "video_stream_duration_seconds": float(stream["duration"]),
        "join_seconds": LEAD_FRAMES / FPS,
        "audio_samples": len(actual),
        "reference_samples": len(expected),
        "zero_lag_audio_correlation": global_corr,
        "join_audio_correlation": join_corr,
        "audio_comparison_channel_basis": "Mono unchanged; stereo arithmetic mean (L+R)/2, avoiding default equal-power downmix gain.",
        "tail_audio_placement_samples": tail_lag,
        "tail_audio_placement_tolerance_samples": 48,
        "placement_compensated_audio_correlation": placed_corr,
        "placement_compensated_join_audio_correlation": placed_join_corr,
        "join_frame_mean_absolute_difference_gray_160x90": boundary_mae,
        "accepted_source_sha256": src_sha,
        "render_sha256": hashlib.sha256(args.render.read_bytes()).hexdigest(),
        "limits": "Uniform-frame detection is an encoding heuristic. These checks do not establish lip sync, natural performance, audience comprehension, creative acceptance, or publication readiness. AAC raw decoding may expose padding beyond presentation duration.",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    diagnostic = {
        "original_failed_report": "qa/MEDIA-CHECK-ZERO-LAG.json",
        "finding": "The initial reference mixed default stereo downmix with unchanged mono audio. The new tail also starts 16 samples later than its exact fractional-second cue; all measured prefix windows remain at zero lag.",
        "channel_basis": "Arithmetic mean of stereo channels; mono WAV unchanged. The initial default ffmpeg -ac 1 basis made stereo roughly sqrt(2) louder than mono during comparison, not in the actual channels.",
        "placement_cause": "The measured 16-sample delay is consistent with rounding 92166.666667 milliseconds to 92167 milliseconds in the mixer. This is an inference from exact timing, not a claim of a source-code trace.",
        "prefix_windows": lead_windows,
        "presenter_windows": tail_windows,
        "allowed_placement_error_samples": 48,
        "allowed_placement_error_ms": 1,
        "measured_tail_delay_samples": tail_lag,
        "global_correlation_after_channel_correction_and_measured_placement": placed_corr,
        "join_correlation_after_channel_correction_and_measured_placement": placed_join_corr,
        "global_rmse_after_channel_correction_and_measured_placement": float(np.sqrt(np.mean((actual[:len(placed_reference)] - placed_reference) ** 2))),
        "media_changed": False,
        "limits": "Source-placement and channel-level checks do not prove perceived lip sync or natural performance. Initial failed report is preserved; output audio and video were not changed to satisfy this check.",
    }
    (ROOT / "qa/AUDIO-ALIGNMENT-CHECK.json").write_text(json.dumps(diagnostic, indent=2) + "\n")
    (ROOT / "qa/PROBE.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
