"""
Arrange the music bed (v7, 2026-07-05) — plays MANAV'S SCORE.

The template was decoded from his EP001 GarageBand session (bar-by-bar
spectral classification of his instrumental export against his own
hand-cut kit, music-src/kit/*.flac). His grammar:

  intro chords (8 bars) under the series line
  rising loops through the hook + THE BRIDGE (music steps forward)
  full groove enters ~2 bars after the thesis starts
  long BREAKDOWN under the dense back half of the argument
  body loops under the evidence
  stripped BASSLINE under the evidence payoff (numbers land on bass)
  sting + roll pivot → INTRO-CHORDS REPRISE when the stack starts
  [extended past his test score, same grammar:]
  groove under the playbook · breakdown + bassline for honest math
  ender → finale cresting at the Blueprint → closing

Continuous music, no dead air; every span is whole bars of his loops;
spans that must END on an anchor get whole-bar front trims. SoundBed
still ducks under VO and silences quote cards on top of this.

Usage:
    python scripts/originate/arrange_bed.py originate/<slug>/script.json

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
KIT = ROOT / "music-src" / "kit"
BAR = 2.4145
DECLICK = 0.012

BARS = {  # whole-bar lengths of the kit (his cuts are grid-exact)
    "MP-loop-01": 8, "MP-loop-02": 8, "MP-loop-03": 12, "MP-loop-04": 16,
    "MP-loop-05": 16, "MP-loop-06": 8, "MP-loop-06-end": 7,
    "MP-bassline-01": 2, "MP-drum-roll-01": 1, "MP-drum-roll-02": 1,
    "MP-drum-roll-02-loop-end": 4, "MP-p2-loop-01": 8, "MP-p2-loop-02": 8,
    "MP-p2-loop-02-end": 5, "MP-p2-breakdown-01": 11, "MP-p2-drum-roll-01": 1,
    "MP-p3-final-loop-01": 8, "MP-p3-final-closing": 3, "MP-mini-loop-06": 8,
}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[-1000:], file=sys.stderr)
        sys.exit(1)


def duration_of(path: Path) -> float:
    p = subprocess.run(["ffprobe", "-hide_banner", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(p.stdout.strip())


def main():
    ap = argparse.ArgumentParser(description="Play Manav's score against the episode anchors")
    ap.add_argument("script")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    ap.add_argument("--stage", choices=["all", "cut", "mix"], default="all",
                    help="cut: emit segments + span concat only; mix: crossfade+encode from existing .bedwork")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    base = Path(args.script).parent
    out = ROOT / "remotion" / "public" / "music" / "bed.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)

    for n in BARS:
        if not (KIT / f"{n}.flac").exists():
            print(f"Error: kit missing {n}.flac", file=sys.stderr)
            sys.exit(1)

    timeline = json.loads((base / "vo" / "timeline.json").read_text())
    render_data = json.loads((base / "render_data" / "blueprint.json").read_text())
    bk = config.get("render", {}).get("bookends", {})
    offset = bk.get("brand_seconds", 0) + bk.get("title_seconds", 0) - bk.get("j_cut_seconds", 0)
    total = render_data["total_frames"] / render_data["fps"] + 1.0

    sec = {s["section"]: (offset + s["start"], offset + s["start"] + s["duration"])
           for s in timeline["sections"]}
    t_thesis = sec["thesis"][0]
    t_evid, t_evid_end = sec["evidence"]
    t_stack = sec["stack"][0]
    t_econ, t_econ_end = sec["economics"]
    t_cta = sec["cta"][0]

    def bars_at(t: float) -> int:
        return max(int(round(t / BAR)), 0)

    # ---- The score: (cycle, target_end_bar) — spans fill with whole
    # loops from the cycle; the last loop is front-trimmed in whole bars
    # to land the span exactly on the target bar.
    plan: list[tuple[list[str], int]] = [
        (["MP-loop-01"], 8),                                            # intro chords
        (["MP-loop-02", "MP-loop-05"], bars_at(t_thesis) + 2),          # rise thru hook+bridge
        (["MP-loop-04", "MP-loop-05"], bars_at(t_evid) - 20),           # full groove
        (["MP-p2-breakdown-01"], bars_at(t_evid)),                      # breakdown → evidence
        (["MP-loop-06", "MP-p2-loop-02", "MP-loop-06", "MP-loop-03"],
         bars_at(t_evid_end) - 10),                                     # evidence body
        (["MP-bassline-01"], bars_at(t_evid_end) - 4),                  # payoff on bass
        (["MP-p3-final-closing"], bars_at(t_evid_end) - 1),             # sting
        (["MP-drum-roll-02-loop-end"], bars_at(t_stack)),               # roll → pivot
        (["MP-loop-01"], bars_at(t_stack) + 16),                        # CHORDS REPRISE
        (["MP-loop-02"], bars_at(t_stack) + 24),                        # re-rise
        (["MP-p2-loop-01", "MP-p2-loop-02"], bars_at(t_econ)),          # playbook groove
        (["MP-p2-breakdown-01"], bars_at(t_econ) + 11),                 # honest-math breakdown
        (["MP-bassline-01"], bars_at(t_econ_end) - 5),                  # risk on bass
        (["MP-p2-loop-02-end"], bars_at(t_econ_end)),                   # ender
        (["MP-p3-final-loop-01"], bars_at(t_cta) + 8),                  # finale crests thru cta
        (["MP-p3-final-closing"], bars_at(t_cta) + 11),                 # closing
    ]

    tdp = ROOT / ".bedwork"
    if args.stage in ("all", "cut"):
        import shutil
        shutil.rmtree(tdp, ignore_errors=True)
    tdp.mkdir(exist_ok=True)
    if True:
        seg_files: list[str] = []
        cur = 0  # bar cursor

        def emit(loop: str, n_bars_needed: int, idx: int):
            """One loop instance trimmed to whole bars from the FRONT."""
            lb = BARS[loop]
            take = min(lb, n_bars_needed)
            trim = (lb - take) * BAR
            f = tdp / f"s{idx:03d}-{loop}.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-i", str(KIT / f"{loop}.flac"),
                 "-af", f"atrim=start={trim:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={DECLICK}",
                 "-ar", "44100", "-ac", "2", "-acodec", "pcm_s16le", str(f)])
            seg_files.append(str(f))
            return take

        idx = 0
        span_files: list[Path] = []  # one pre-concatenated file per plan span
        if args.stage == "mix":
            span_files = sorted(tdp.glob("span*.wav"))
            cur = 235  # bar count persisted implicitly; recompute below
            cur = int(round(sum(duration_of(f) for f in span_files) / BAR))
        else:
            for cycle, end_bar in plan:
                if end_bar <= cur:
                    continue
                seg_files.clear()
                ci = 0
                while cur < end_bar:
                    loop = cycle[ci % len(cycle)]
                    remaining = end_bar - cur
                    lb = BARS[loop]
                    if remaining < lb and len(cycle) > 1:
                        # find the cycle member that fits best whole
                        fit = min(cycle, key=lambda l: abs(BARS[l] - remaining))
                        loop = fit
                    cur += emit(loop, remaining, idx)
                    idx += 1
                    ci += 1
                # Same-family repeats butt-join via the concat demuxer (fast,
                # seamless — bar-exact cuts + declick fades already applied).
                sp = tdp / f"span{len(span_files):02d}.wav"
                lst = tdp / "seq.txt"
                lst.write_text("\n".join(f"file '{f}'" for f in seg_files))
                run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-f", "concat",
                     "-safe", "0", "-i", str(lst), "-c", "copy", str(sp)])
                span_files.append(sp)


        if args.stage == "cut":
            print(f"✓ cut stage done: {len(span_files)} spans, {cur} bars in {tdp}")
            return
        # Crossfade ONLY at span boundaries (~a dozen joins, not 40+).
        assembled = tdp / "assembled.wav"
        if len(span_files) == 1:
            span_files[0].replace(assembled)
        else:
            inputs2 = []
            for f in span_files:
                inputs2 += ["-i", str(f)]
            fc2, prev2 = "", "0:a"
            for i in range(1, len(span_files)):
                fc2 += f"[{prev2}][{i}:a]acrossfade=d=0.35:c1=tri:c2=tri[y{i}];"
                prev2 = f"y{i}"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs2,
                 "-filter_complex", fc2.rstrip(";"), "-map", f"[{prev2}]", str(assembled)])

        # Fast level match (loudnorm is too slow here): measured gain to −16.
        p = subprocess.run(["ffmpeg", "-i", str(assembled), "-af", "volumedetect",
                            "-f", "null", "-"], capture_output=True, text=True)
        mean = next((l.split()[-2] for l in p.stderr.splitlines() if "mean_volume" in l), "-16")
        gain = -16.0 - float(mean)
        pad = max(total - cur * BAR + 2.0, 0.0)
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(assembled),
             "-af", f"volume={gain:.1f}dB,apad=pad_dur={pad:.2f}",
             "-ar", "44100", "-b:a", "192k", str(out)])

    print(f"✓ Bed v7 (Manav's score) → {out}")
    print(f"  {cur} bars ({cur * BAR:.1f}s) + tail pad vs video {total - 1:.1f}s · "
          f"{idx} segments in {len(span_files)} spans")
    print(f"  groove @ thesis+2 bars · breakdown → evidence @ {t_evid:.0f}s · bass payoff · "
          f"chords reprise @ stack {t_stack:.0f}s · finale crests @ cta {t_cta:.0f}s")


if __name__ == "__main__":
    main()
