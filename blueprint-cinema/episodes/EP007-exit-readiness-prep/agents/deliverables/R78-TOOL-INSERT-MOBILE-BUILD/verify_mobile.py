#!/usr/bin/env python3
"""Technical verification for the isolated R78 mobile-framing review candidates."""
import array
import hashlib
import json
import math
import pathlib
import re
import subprocess
import wave

HERE = pathlib.Path(__file__).resolve().parent
SCENES = {
    "s15-mobile": {"frames": 1368, "audio_start": 2376000, "audio_window": 96000},
    "s16-mobile-r7": {"frames": 1293, "audio_start": 1200000, "audio_window": 96000},
}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(args):
    subprocess.run([str(item) for item in args], check=True)


def probe(path):
    raw = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "stream=codec_type,width,height,r_frame_rate,nb_frames,sample_rate",
            "-of", "json", str(path),
        ], text=True,
    )
    return json.loads(raw)["streams"]


def load_pcm(path):
    values = array.array("h")
    values.frombytes(path.read_bytes())
    return values


def correlation(reference, rendered, start, count):
    pairs = zip(reference[start:start + count], rendered[start:start + count])
    dot = ref_energy = render_energy = 0.0
    for left, right in pairs:
        dot += left * right
        ref_energy += left * left
        render_energy += right * right
    return dot / math.sqrt(ref_energy * render_energy), 20 * math.log10(math.sqrt(render_energy / ref_energy))


def blank_scan(video, qa):
    signalstats = qa / "signalstats.txt"
    run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"signalstats,metadata=print:file={signalstats}", "-an", "-f", "null", "-"])
    minima = [int(match.group(1)) for match in re.finditer(r"lavfi\.signalstats\.YMIN=(\d+)", signalstats.read_text())]
    return {"frames_analyzed": len(minima), "full_luma_blank_suspects": [index for index, value in enumerate(minima) if value >= 220]}


def check_report(path):
    content = path.read_text()
    if "{" in content:
        json_start = content.index("{")
        report = json.loads(content[json_start:])
        assert report["ok"] is True, report
        return {"ok": report["ok"], "error_count": sum(v.get("errorCount", 0) for v in report.values() if isinstance(v, dict))}
    assert "Check passed" in content, content
    return {"ok": True, "error_count": 0, "format": "human-readable HyperFrames strict report"}


def verify_scene(name, plan):
    project = HERE / "projects" / name
    qa = project / "qa"
    video = qa / f"{name}-review.mp4"
    assert video.is_file()
    streams = probe(video)
    visual = next(stream for stream in streams if stream["codec_type"] == "video")
    audio = next(stream for stream in streams if stream["codec_type"] == "audio")
    assert (int(visual["width"]), int(visual["height"]), visual["r_frame_rate"], int(visual["nb_frames"])) == (1280, 720, "24/1", plan["frames"])
    assert int(audio["sample_rate"]) == 48000
    run(["ffmpeg", "-v", "error", "-i", video, "-f", "null", "-"])
    decoded = qa / "rendered-audio.s16le"
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-map", "0:a:0", "-ac", "1", "-ar", "48000", "-f", "s16le", decoded])
    with wave.open(str(project / "public/audio/narration.wav"), "rb") as staged:
        assert (staged.getframerate(), staged.getnchannels(), staged.getsampwidth()) == (48000, 1, 2)
        reference = array.array("h")
        reference.frombytes(staged.readframes(staged.getnframes()))
    rendered = load_pcm(decoded)
    assert len(reference) >= plan["audio_start"] + plan["audio_window"]
    assert len(rendered) >= plan["audio_start"] + plan["audio_window"]
    zero_lag, level_delta = correlation(reference, rendered, plan["audio_start"], plan["audio_window"])
    assert zero_lag > 0.99, zero_lag
    blanks = blank_scan(video, qa)
    assert blanks["frames_analyzed"] == plan["frames"], blanks
    assert not blanks["full_luma_blank_suspects"], blanks
    (qa / "visual-uniformity.json").write_text(json.dumps(blanks, indent=2) + "\n")
    audio_report = {
        "reference_samples": len(reference),
        "rendered_samples": len(rendered),
        "sample_rate": 48000,
        "window_start_sample": plan["audio_start"],
        "window_samples": plan["audio_window"],
        "candidate_relative_lag_samples": 0,
        "candidate_relative_lag_frames": 0.0,
        "correlation_at_zero_lag": zero_lag,
        "level_delta_db": level_delta,
        "verdict": "pass",
        "note": "Rendered AAC decoded at the same timeline origin as the staged locked-master slice.",
    }
    (qa / "audio-alignment.json").write_text(json.dumps(audio_report, indent=2) + "\n")
    result = {
        "review_mp4": {"path": str(video.relative_to(HERE.parents[5])), "sha256": sha(video)},
        "strict_check": check_report(qa / "check.json"),
        "video": {"width": 1280, "height": 720, "fps": 24, "frames": plan["frames"]},
        "audio": audio_report,
        "blank_scan": blanks,
    }
    if name == "s16-mobile-r7":
        result["return_seam_repair"] = {
            "timeline_frames": [866, 875],
            "source": "accepted S16 P1 frame 866, held as a static source-derived overlay",
            "purpose": "Covers the browser video's return seam. The accepted source is visually static over these ten frames; no replacement action, text, or pointer is introduced.",
        }
    return result


if __name__ == "__main__":
    report = {"result": "pass", "scope": "Isolated R78 mobile-framing review candidates only.", "owner_review": "pending", "scenes": {}}
    for scene, plan in SCENES.items():
        report["scenes"][scene] = verify_scene(scene, plan)
    report["limitations"] = [
        "Technical verification does not accept the candidate, integrate it into the full episode, conform it, or release it.",
        "The illustration label remains; the recordings show no client case, business outcome, or resolved exception authority.",
    ]
    (HERE / "qa").mkdir(exist_ok=True)
    (HERE / "qa/VERIFICATION.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
