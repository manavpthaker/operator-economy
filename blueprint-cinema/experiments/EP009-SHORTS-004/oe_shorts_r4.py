#!/usr/bin/env python3
"""Shared build helpers for EP009 SHORTS-004 (standalone-payoff revision).

Locked-source only. No provider calls, no generation, no retime. Every audio
slice is taken from the r3 narration master by exact sample boundary
(2000 samples per 24fps frame); every picture slice is taken from an existing
accepted look-transfer native by exact frame boundary.
"""
from __future__ import annotations

import array
import hashlib
import json
import math
import subprocess
from pathlib import Path

FPS = 24
SAMPLE_RATE = 48000
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS  # 2000

REPO = Path(__file__).resolve().parents[3]
FULL = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001"
MASTER_WAV = FULL / "assembly/r3/narration-master-r3.wav"
WORDS_JSON = FULL / "assembly/r3/word-transcript-r3.json"
CARRIER = FULL / "assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4"
LOCK_JSON = FULL / "assembly/r8-tool-clarity/FINAL-EPISODE-LOCK-r8.json"
NATIVES = FULL / "presenter-look-transfer/room-r1"
FONTS = REPO / "design-system/boundary-ledger/fonts"
GSAP = REPO / ".agents/skills/talking-head-recut/assets/vendor/gsap.min.js"

# Locked fingerprints. The build refuses to run against anything else.
LOCKED = {
    MASTER_WAV: "0f0d5d326262813cb5ff5392fb263f15f6a8e871ad22e54c1274ff974037ca85",
    WORDS_JSON: "0b5175dea2cbb1ac7682cd69b9ab032bc8c544131aae82575140e90ae0d76709",
    CARRIER: "cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e",
    LOCK_JSON: "b9d107718c0d760e388c1a5167bcaf7e06ebfb29504ed469fac385aa2aa54cd2",
}

HYPERFRAMES_PIN = "hyperframes@0.8.53"


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assert_locked() -> None:
    for path, digest in LOCKED.items():
        actual = sha(path)
        if actual != digest:
            raise SystemExit(f"Locked source changed: {path} ({actual})")


def run(args) -> None:
    subprocess.run([str(a) for a in args], check=True)


def words() -> list[dict]:
    return json.loads(WORDS_JSON.read_text())["words"]


def word_index() -> dict[str, dict]:
    return {w["w_id"]: w for w in words()}


# --------------------------------------------------------------------------
# audio
# --------------------------------------------------------------------------
def cut_voice(segments: list[tuple[int, int]], out: Path, *, stereo: bool = False) -> None:
    """Concatenate exact master frame ranges at unity into a PCM file."""
    graph = ";".join(
        f"[0:a]atrim=start_sample={a * SAMPLES_PER_FRAME}:end_sample={b * SAMPLES_PER_FRAME},"
        f"asetpts=PTS-STARTPTS[s{i}]"
        for i, (a, b) in enumerate(segments)
    )
    graph += ";" + "".join(f"[s{i}]" for i in range(len(segments)))
    graph += f"concat=n={len(segments)}:v=0:a=1"
    if stereo:
        graph += ",pan=stereo|c0=c0|c1=c0"
    graph += "[out]"
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", MASTER_WAV,
         "-filter_complex", graph, "-map", "[out]", "-c:a", "pcm_s24le", out])


def presenter_clip(native: Path, out: Path, in_frame: int, out_frame: int, vf: str) -> str:
    """Render one presenter picture slice. Exact native frames, no retime."""
    chain = (f"trim=start_frame={in_frame}:end_frame={out_frame},setpts=N/({FPS}*TB),{vf}")
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-threads", "1", "-i", native,
         "-vf", chain, "-an", "-c:v", "libx264", "-crf", "17", "-preset", "fast",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", out])
    return chain


def carrier_clip(out: Path, in_frame: int, frames: int, vf: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-threads", "1",
         "-ss", f"{in_frame / FPS:.9f}", "-i", CARRIER, "-t", f"{frames / FPS:.9f}",
         "-vf", vf, "-an", "-c:v", "libx264", "-crf", "17", "-preset", "fast",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", out])


# --------------------------------------------------------------------------
# captions
# --------------------------------------------------------------------------
def caption_groups(wi: dict, spans: list[tuple[str, str]], shift_for,
                   clamp: float, *, lead: float = 0.03, tail: float = 0.10) -> list[dict]:
    """Build burned-in phrase groups from locked word timings.

    ``shift_for(w_id)`` returns the timeline offset (seconds) to subtract-adjust
    a master word time into short time. Groups never overlap: each group ends
    at the later of its own tail or just before the next group starts.
    """
    out = []
    for first, last in spans:
        n0 = int(first[1:])
        n1 = int(last[1:])
        ws = [wi[f"W{n:06d}"] for n in range(n0, n1 + 1)]
        shift = shift_for(first)
        start = max(0.0, ws[0]["start"] + shift - lead)
        end = min(clamp, ws[-1]["end"] + shift + tail)
        out.append({
            "start": round(start, 6),
            "end": round(end, 6),
            "text": " ".join(w["token"] for w in ws),
            "words": [w["w_id"] for w in ws],
        })
    for i in range(len(out) - 1):
        out[i]["end"] = round(min(out[i]["end"], out[i + 1]["start"] - 0.001), 6)
    return out


def _stamp(seconds: float, comma: bool) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    sep = "," if comma else "."
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def write_srt(cues: list[dict], path: Path) -> None:
    blocks = []
    for i, c in enumerate(cues, 1):
        blocks.append(
            f"{i}\n{_stamp(c['start'], True)} --> {_stamp(c['end'], True)}\n{c['text']}\n"
        )
    path.write_text("\n".join(blocks))


def write_vtt(cues: list[dict], path: Path) -> None:
    lines = ["WEBVTT", ""]
    for i, c in enumerate(cues, 1):
        lines.append(str(i))
        lines.append(f"{_stamp(c['start'], False)} --> {_stamp(c['end'], False)}")
        lines.append(c["text"])
        lines.append("")
    path.write_text("\n".join(lines))


# --------------------------------------------------------------------------
# project scaffolding
# --------------------------------------------------------------------------
def scaffold(project: Path, name: str, font_names: list[str]) -> None:
    assets = project / "assets"
    (assets / "fonts").mkdir(parents=True, exist_ok=True)
    (assets / "vendor").mkdir(parents=True, exist_ok=True)
    for font in font_names:
        (assets / "fonts" / font).write_bytes((FONTS / font).read_bytes())
    (assets / "vendor" / "gsap.min.js").write_bytes(GSAP.read_bytes())
    (project / "package.json").write_text(json.dumps({
        "name": name, "private": True, "type": "module",
        "scripts": {"check": f"npx --yes {HYPERFRAMES_PIN} check",
                    "render": f"npx --yes {HYPERFRAMES_PIN} render"},
    }, indent=2) + "\n")
    (project / "hyperframes.json").write_text(json.dumps({
        "paths": {"assets": "assets"}, "authoringSkill": "general-video",
    }, indent=2) + "\n")


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


# --------------------------------------------------------------------------
# verification helpers
# --------------------------------------------------------------------------
def master_samples(a_frame: int, b_frame: int) -> array.array:
    """Read the locked master as int16 samples over a frame range."""
    out = subprocess.check_output([
        "ffmpeg", "-nostdin", "-v", "error", "-i", str(MASTER_WAV),
        "-af", f"atrim=start_sample={a_frame * SAMPLES_PER_FRAME}:"
               f"end_sample={b_frame * SAMPLES_PER_FRAME}",
        "-f", "s16le", "-acodec", "pcm_s16le", "-ar", str(SAMPLE_RATE), "-ac", "1", "-",
    ])
    arr = array.array("h")
    arr.frombytes(out)
    return arr


def rendered_samples(path: Path, a_frame: int, b_frame: int) -> array.array:
    out = subprocess.check_output([
        "ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
        "-af", f"atrim=start_sample={a_frame * SAMPLES_PER_FRAME}:"
               f"end_sample={b_frame * SAMPLES_PER_FRAME}",
        "-f", "s16le", "-acodec", "pcm_s16le", "-ar", str(SAMPLE_RATE), "-ac", "1", "-",
    ])
    arr = array.array("h")
    arr.frombytes(out)
    return arr


def correlation(a: array.array, b: array.array, step: int = 7) -> float:
    """Normalised zero-lag cross-correlation on a decimated pair."""
    n = min(len(a), len(b))
    xs = a[:n:step]
    ys = b[:n:step]
    sxy = sxx = syy = 0.0
    for x, y in zip(xs, ys):
        sxy += x * y
        sxx += x * x
        syy += y * y
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def sub_composition(project: Path, ident: str, css: str, body: str,
                    duration: float, anim: str = "") -> None:
    """Write a mountable sub-composition. The root composition is built only
    from sub-compositions, so any nested structure lives in one of these."""
    out = project / "compositions"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ident}.html").write_text(
        "<html><body><template><style>" + css
        + f"#{ident}{{position:absolute;inset:0;width:1080px;height:1920px}}</style>"
        + f'<div id="{ident}" data-composition-id="{ident}" data-start="0" '
        + f'data-duration="{duration:.9f}" data-width="1080" data-height="1920">{body}</div>'
        + "<script>const tl=gsap.timeline({paused:true});" + anim
        + "window.__timelines=window.__timelines||{};"
        + f"window.__timelines.{ident}=tl;</script></template></body></html>"
    )


def mount(ident: str, start: float, duration: float, track: int) -> str:
    return (f'<div id="{ident}-host" class="clip" data-composition-id="{ident}" '
            f'data-composition-src="compositions/{ident}.html" '
            f'data-start="{start:.9f}" data-duration="{duration:.9f}" '
            f'data-track-index="{track}"></div>')
