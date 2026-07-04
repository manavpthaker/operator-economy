"""
Arrange the music bed against the episode structure (v2, 2026-07-03).

Punctuation grammar — Search Engine beats + ColdFusion ambience — not
wallpaper. config/blueprint.json `music.map` assigns each section a mode:

  beat      — the actual track: dust intro, the DROP landing as the
              first quote card releases, body grooves, natural outro
  ambience  — the SAME track low-passed into a warm blur (-7dB): the
              harmonic glue under evidence-dense sections, so the
              episode keeps breathing without the beat competing

Consecutive same-mode sections merge into one span; spans crossfade
(1.5s) so the music reads as one piece breathing, not tracks trading.
Since ambience is derived from the beat track, key and texture always
cohere.

Voice-agnostic and idempotent: re-run after any VO regeneration
(timings come from vo/timeline.json + storyboard.json).

Usage:
    python scripts/originate/arrange_bed.py originate/<slug>/script.json
        [--track ...] [--drop 10.0] [--no-arrange]

Writes: remotion/public/music/bed.mp3
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

TREAT_CHAIN = (
    "acompressor=threshold=-28dB:ratio=4:attack=40:release=800:makeup=6,"
    "anequalizer=c0 f=2800 w=2600 g=-5 t=1|c1 f=2800 w=2600 g=-5 t=1,"
    "lowpass=f=7500,"
    "loudnorm=I=-16:TP=-2:LRA=5"
)

XFADE_SPAN = 1.5   # between beat/ambience spans
XFADE_LOOP = 1.0   # inside loops


def run(cmd: list[str]):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[-1200:], file=sys.stderr)
        sys.exit(1)


def duration_of(path: Path) -> float:
    p = subprocess.run(["ffprobe", "-hide_banner", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(p.stdout.strip())


def main():
    ap = argparse.ArgumentParser(description="Arrange the music bed (punctuation grammar)")
    ap.add_argument("script")
    ap.add_argument("--track", default=None)
    ap.add_argument("--drop", type=float, default=None)
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    ap.add_argument("--no-arrange", action="store_true", help="Treat + install only")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    m_cfg = config.get("music", {})
    track = Path(args.track or (ROOT / m_cfg.get("track", "")))
    if not track.is_absolute():
        track = ROOT / track
    if not track.exists():
        print(f"Error: track not found: {track}", file=sys.stderr)
        sys.exit(1)
    drop = args.drop if args.drop is not None else m_cfg.get("drop_time_s", 10.0)
    body = m_cfg.get("body", [40.0, 136.0])
    mode_map: dict = m_cfg.get("map", {})
    amb_cfg = m_cfg.get("ambience", {})
    amb_lp = amb_cfg.get("lowpass_hz", 700)
    amb_gain = amb_cfg.get("gain_db", -7)
    amb_win = amb_cfg.get("source_window_s", 30)

    base = Path(args.script).parent
    out = ROOT / "remotion" / "public" / "music" / "bed.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        flat = tdp / "flat.mp3"
        print(f"Treating {track.name} (flatten + carve + normalize)…")
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(track),
             "-af", TREAT_CHAIN, "-ar", "44100", "-b:a", "192k", str(flat)])
        track_len = duration_of(flat)

        if args.no_arrange or not mode_map:
            flat.replace(out)
            print(f"✓ Treated bed (unarranged, loops) → {out}")
            return

        timeline = json.loads((base / "vo" / "timeline.json").read_text())
        storyboard = json.loads((base / "storyboard.json").read_text())
        total = float(timeline["total_seconds"]) + 2.0  # +2s so SoundBed's loop never wraps

        first_quote = next((s for s in storyboard["screens"] if s["layout"] == "quote"), None)
        anchor = (first_quote["end"] + 0.15) if first_quote else 12.0

        # Merge consecutive sections of the same mode into spans.
        spans: list[dict] = []
        for sec in timeline["sections"]:
            mode = mode_map.get(sec["section"], "ambience")
            end = sec["start"] + sec["duration"]
            if spans and spans[-1]["mode"] == mode:
                spans[-1]["end"] = end
                spans[-1]["sections"].append(sec["section"])
            else:
                spans.append({"mode": mode, "start": sec["start"], "end": end,
                              "sections": [sec["section"]]})
        spans[-1]["end"] = total  # last span carries through the outro card

        segs: list[tuple[Path, float]] = []

        def cut(name: str, start: float, end: float, af: str = "anull") -> Path:
            f = tdp / f"{name}.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(flat),
                 "-af", af, str(f)])
            return f

        def looped(name: str, src: Path, need: float) -> Path:
            f = tdp / f"{name}.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-stream_loop", "20", "-i", str(src), "-t", f"{need:.3f}", str(f)])
            return f

        amb_src = cut("amb_src", body[0], body[0] + amb_win,
                      f"lowpass=f={amb_lp},volume={amb_gain}dB")

        n_beat_spans = 0
        for i, span in enumerate(spans):
            need = span["end"] - span["start"] + XFADE_SPAN
            name = f"s{i}-{span['mode']}"
            if span["mode"] == "ambience":
                segs.append((looped(name, amb_src, need), need))
                continue
            n_beat_spans += 1
            is_first = i == 0
            is_last = i == len(spans) - 1
            if is_first and span["start"] <= anchor <= span["end"]:
                # Dust under the hook, track intro run-up, DROP at anchor.
                pre_gap = anchor - drop - span["start"]
                if pre_gap > 0.5:
                    dust_src = cut("dust_src", 0.0, min(7.5, drop - 1.0),
                                   "lowpass=f=1000,volume=-5dB")
                    segs.append((looped("dust", dust_src, pre_gap + XFADE_LOOP),
                                 pre_gap + XFADE_LOOP))
                    main_start = 0.0
                else:
                    main_start = drop - anchor + span["start"]
                main_need = span["end"] - anchor + drop - main_start + XFADE_SPAN
                segs.append((cut(f"{name}-main", main_start,
                                 min(main_start + main_need, track_len)),
                             min(main_need, track_len - main_start)))
            elif is_last:
                # Close on the track's own tail so the episode ends on
                # the natural fade.
                start = max(track_len - need, 0.0)
                segs.append((cut(f"{name}-tail", start, track_len), track_len - start))
            else:
                # Mid-episode beat span: full-energy body material.
                if need <= (body[1] - body[0]):
                    segs.append((cut(name, body[0], body[0] + need), need))
                else:
                    body_src = cut(f"{name}-src", body[0], body[1])
                    segs.append((looped(name, body_src, need), need))

        # Chain with crossfades.
        inputs: list[str] = []
        for f, _ in segs:
            inputs += ["-i", str(f)]
        fc, prev = "", "0:a"
        for i in range(1, len(segs)):
            label = f"x{i}"
            fc += f"[{prev}][{i}:a]acrossfade=d={XFADE_SPAN}:c1=tri:c2=tri[{label}];"
            prev = label
        fc = fc.rstrip(";")
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
             "-filter_complex", fc, "-map", f"[{prev}]",
             "-ar", "44100", "-b:a", "192k", str(out)])

    final = duration_of(out)
    print(f"✓ Arranged bed (punctuation grammar) → {out}")
    print(f"  {final:.1f}s vs content {total - 2:.1f}s · drop @ {anchor:.1f}s")
    for s in spans:
        print(f"    {s['mode']:8s} {s['start']:6.1f}–{s['end']:6.1f}s  ({', '.join(s['sections'])})")


if __name__ == "__main__":
    main()
