"""
Arrange the music bed against the episode structure (v5, 2026-07-04).

Manav's arc — instrumental opens, ONE drop, and the beat never stops:

  chords      — soft instrumental from FRAME 0 (sting, title, intro line)
  crescendo 1 — rises INTO "It's called implementation." (first quote);
                the quote itself is the SoundBed silence
  THE DROP    — beat enters on the quote's release and RUNS
  variation   — beat section B at the n8n sim screen ("something new is
                on screen")
  crescendo 2 — through the "one person" build, cresting at the
                "charging billions" quote; evidence ties back down
  settled beat— long body region loops (2.5s seams — choppiness fix),
                SoundBed intensity does the dynamics
  build → cta — crescendo crests at "The Blueprint", finale + fade

All joins ≥2s musical crossfades except the drop itself (0.3s).
Anchors come from storyboard.json, so this re-fits after any VO regen.

Usage:
    python scripts/originate/arrange_bed.py originate/<slug>/script.json [--no-arrange]

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

FLAT_CHAIN = (
    "acompressor=threshold=-28dB:ratio=4:attack=40:release=800:makeup=6,"
    "anequalizer=c0 f=2800 w=2600 g=-5 t=1|c1 f=2800 w=2600 g=-5 t=1,"
    "lowpass=f=7500,"
    "loudnorm=I=-16:TP=-2:LRA=5"
)
DYN_CHAIN = (
    "anequalizer=c0 f=2800 w=2600 g=-4 t=1|c1 f=2800 w=2600 g=-4 t=1,"
    "lowpass=f=8000,"
    "loudnorm=I=-16:TP=-2:LRA=9"
)

XFADE = 2.2      # musical joins — the choppiness fix
XFADE_DROP = 0.3 # the one hard arrival


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
    ap = argparse.ArgumentParser(description="Arrange the music bed (v5: one drop, beat never stops)")
    ap.add_argument("script")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    ap.add_argument("--no-arrange", action="store_true")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    m = config.get("music", {})
    track = ROOT / m.get("track", "")
    if not track.exists():
        print(f"Error: track not found: {track}", file=sys.stderr)
        sys.exit(1)

    base = Path(args.script).parent
    out = ROOT / "remotion" / "public" / "music" / "bed.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)

    chords = m.get("chords", [0.0, 20.0])
    build = m.get("build", [258.0, 276.0])
    beat_a = m.get("beat_a", [22.0, 80.0])
    beat_b = m.get("beat_b", [120.0, 156.0])
    body_loop = m.get("body_loop", [48.0, 140.0])
    finale = m.get("finale")
    build_into = m.get("build_into", "cta")
    build_len = build[1] - build[0]

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def cut(name: str, start: float, end: float, chain: str, extra: str = "") -> Path:
            f = tdp / f"{name}.wav"
            af = chain + ("," + extra if extra else "")
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(track),
                 "-af", af, "-ar", "44100", str(f)])
            return f

        def looped(name: str, src: Path, need: float) -> Path:
            f = tdp / f"{name}.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-stream_loop", "30", "-i", str(src), "-t", f"{need:.3f}", str(f)])
            return f

        if args.no_arrange:
            flat = tdp / "flat.mp3"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(track),
                 "-af", FLAT_CHAIN, "-ar", "44100", "-b:a", "192k", str(flat)])
            flat.replace(out)
            print(f"✓ Treated bed (unarranged, loops) → {out}")
            return

        timeline = json.loads((base / "vo" / "timeline.json").read_text())
        storyboard = json.loads((base / "storyboard.json").read_text())
        render_data = json.loads((base / "render_data" / "blueprint.json").read_text())

        bk = config.get("render", {}).get("bookends", {})
        offset = bk.get("brand_seconds", 0) + bk.get("title_seconds", 0) - bk.get("j_cut_seconds", 0)
        total = render_data["total_frames"] / render_data["fps"] + 1.0

        screens = storyboard["screens"]
        quotes = [s for s in screens if s["layout"] == "quote"]
        q1 = quotes[0] if quotes else None                       # "It's called implementation."
        thesis_quotes = [s for s in quotes if s["section"] == "thesis"]
        q_bill = thesis_quotes[-1] if thesis_quotes else None    # "charging billions"
        sim1 = next((s for s in screens
                     if (s.get("custom") or {}).get("sim", {}).get("kind") == "workflow"), None)

        q1_start = offset + (q1["start"] if q1 else 55.0)
        q1_end = offset + (q1["end"] if q1 else 58.0)
        sim_start = offset + (sim1["start"] if sim1 else q1_end + 25.0)
        bill_start = offset + (q_bill["start"] if q_bill else sim_start + 40.0)

        cta = next((s for s in timeline["sections"] if s["section"] == build_into), None)
        target = offset + (cta["start"] if cta else total - 16.0)
        body_start = bill_start  # crescendo 2 crests here; body runs on under evidence
        build3_start = max(target - build_len, body_start + 20.0)

        segs: list[tuple[Path, float, str]] = []  # (file, dur, joinmode)

        # 1) chords → crescendo1 crest at q1_start.
        c1_start = max(q1_start - build_len, 0.0)
        chords_src = cut("chords_src", chords[0], chords[1], DYN_CHAIN, "volume=-2dB")
        segs.append((looped("chords", chords_src, c1_start + XFADE), c1_start + XFADE, "x"))
        segs.append((cut("cresc1", build[0], build[1], DYN_CHAIN), build_len, "x"))
        # bed content under the quote itself is ducked to silence by
        # SoundBed — the drop arrives at q1_end.
        gap1 = q1_end - q1_start
        segs.append((cut("underq1", chords[0], chords[0] + gap1 + XFADE_DROP, FLAT_CHAIN,
                         "volume=-8dB"), gap1 + XFADE_DROP, "x"))

        # 2) THE DROP — beat A runs q1_end → sim screen.
        need_a = sim_start - q1_end + XFADE
        srcA = cut("beatA_src", beat_a[0], beat_a[1], DYN_CHAIN)
        segs.append((looped("beatA", srcA, need_a) if need_a > (beat_a[1] - beat_a[0]) else
                     cut("beatA", beat_a[0], beat_a[0] + need_a, DYN_CHAIN), need_a, "drop"))

        # 3) variation at the n8n screen → crescendo2 into "billions".
        c2_start = max(bill_start - build_len, sim_start + 6.0)
        need_b = c2_start - sim_start + XFADE
        srcB = cut("beatB_src", beat_b[0], beat_b[1], DYN_CHAIN)
        segs.append((looped("beatB", srcB, need_b) if need_b > (beat_b[1] - beat_b[0]) else
                     cut("beatB", beat_b[0], beat_b[0] + need_b, DYN_CHAIN), need_b, "x"))
        segs.append((cut("cresc2", build[0], build[1], DYN_CHAIN), build_len, "x"))

        # 4) settled beat through the body (long region, few seams).
        need_body = build3_start - bill_start + XFADE
        body_src = cut("body_src", body_loop[0], body_loop[1], FLAT_CHAIN)
        segs.append((looped("body", body_src, need_body), need_body, "x"))

        # 5) build → finale (tail keeps its natural fade).
        segs.append((cut("build3", build[0], build[1], DYN_CHAIN), build_len, "x"))
        if finale:
            fin_need = total - target
            fin_len = finale[1] - finale[0]
            f_start = finale[0] + max(fin_len - fin_need, 0.0)
            segs.append((cut("finale", f_start, finale[1], DYN_CHAIN), finale[1] - f_start, "x"))

        inputs = []
        for f, _, _ in segs:
            inputs += ["-i", str(f)]
        fc, prev = "", "0:a"
        for i in range(1, len(segs)):
            d = XFADE_DROP if segs[i][2] == "drop" else XFADE
            fc += f"[{prev}][{i}:a]acrossfade=d={d}:c1=tri:c2=tri[x{i}];"
            prev = f"x{i}"
        mixed = tdp / "mixed.mp3"
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
             "-filter_complex", fc.rstrip(";"), "-map", f"[{prev}]",
             "-ar", "44100", "-b:a", "192k", str(mixed)])
        cur = duration_of(mixed)
        pad = max(total - cur + 2.0, 0.0)
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(mixed),
             "-af", f"apad=pad_dur={pad:.2f}", "-ar", "44100", "-b:a", "192k", str(out)])

    final = duration_of(out)
    print(f"✓ Arranged bed v5 → {out}  ({final:.1f}s vs video {total - 1:.1f}s)")
    print(f"  chords → cresc1 crests @ {q1_start:.1f} ('implementation') · DROP @ {q1_end:.1f} · "
          f"variation @ {sim_start:.1f} (n8n sim) · cresc2 crests @ {bill_start:.1f} ('billions') · "
          f"settled beat → build3 @ {build3_start:.1f} · crest @ {target:.1f} ('{build_into}') · finale")


if __name__ == "__main__":
    main()
