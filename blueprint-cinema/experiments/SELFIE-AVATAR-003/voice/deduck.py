"""Duck audible inhales in the master voice take.

The locked take (voice-w4g.original-c.wav) has breaths in several of its
pauses. The one at 39.40 lands immediately before the cut to avatar-insight at
39.82, which is why it reads as odd rather than as natural breathing.

This does NOT re-time anything. It only lowers the gain inside spans that sit
entirely within a pause, so every word timing, the shot plan, the lip-syncs and
the captions stay valid.

Two guards decide what is safe to touch, because ASR word boundaries are
approximate and a word onset can sit inside what the timings call a "gap":

  * peak must be below SPEECH_CEIL — anything louder is voice, not a breath
  * the span must be clear of the neighbouring words by CLEAR seconds

Spans that fail either test are left alone and reported. Breaths are attenuated
to just above the pause's own noise floor rather than to silence: a digital
hole in room tone is more noticeable than the breath was.

  python3 voice/deduck.py [--apply]
"""
import argparse
import json
import math
import struct
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
SRC = EXP / "media/voice/voice-w4g.original-c.wav"
DST = EXP / "media/voice/voice-w4g.original-c.debreathed.wav"
TIMINGS = HERE / "asr-final/FINAL-WORD-TIMINGS.json"

WIN = 0.020          # analysis window
MIN_LEN = 0.10       # shorter than this is a tick, not a breath
LIFT = 6.0           # dB above the pause floor to count as something
SPEECH_CEIL = -24.0  # dB; louder than this is voice
CLEAR = 0.10         # s of clearance required from neighbouring words
HEADROOM = 3.0       # dB above the pause floor to leave after ducking
FADE = 0.015         # s raised-cosine fade at each edge


def load(path):
    w = wave.open(str(path))
    n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    raw = w.readframes(n)
    w.close()
    if sw != 2:
        sys.exit(f"{path}: expected 16-bit, got {sw * 8}-bit")
    samples = list(struct.unpack(f"<{len(raw) // 2}h", raw))
    return samples, sr, ch


def dbfs(samples, sr, a, b):
    seg = samples[int(a * sr):int(b * sr)]
    if not seg:
        return -120.0
    r = math.sqrt(sum(x * x for x in seg) / len(seg))
    return 20 * math.log10(r / 32768.0) if r > 0 else -120.0


def find(samples, sr, words):
    gaps = [(a["e"] + 0.04, b["s"] - 0.04, a["t"], b["t"])
            for a, b in zip(words, words[1:]) if b["s"] - a["e"] > 0.30]
    found = []
    for s, e, wa, wb in gaps:
        times = [s + i * WIN for i in range(int((e - s) / WIN))]
        if len(times) < 4:
            continue
        levels = [dbfs(samples, sr, t, t + WIN) for t in times]
        floor = sorted(levels)[len(levels) // 4]
        run, runs = None, []
        for t, l in zip(times, levels):
            if l > floor + LIFT:
                run = (t, t + WIN, l) if run is None else (run[0], t + WIN, max(run[2], l))
            elif run:
                runs.append(run)
                run = None
        if run:
            runs.append(run)
        for a, b, peak in runs:
            if b - a >= MIN_LEN:
                found.append({"start": a, "end": b, "peak": peak, "floor": floor,
                              "after": wa, "before": wb})
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the file (default is a dry run)")
    args = ap.parse_args()

    samples, sr, ch = load(SRC)
    if ch != 1:
        sys.exit(f"{SRC}: expected mono, got {ch} channels")
    words = json.loads(TIMINGS.read_text())["words"]

    keep, skip = [], []
    for c in find(samples, sr, words):
        prev = max((w["e"] for w in words if w["e"] <= c["start"]), default=-99.0)
        nxt = min((w["s"] for w in words if w["s"] >= c["end"]), default=99.0)
        if c["peak"] > SPEECH_CEIL:
            skip.append((c, f"peak {c['peak']:.1f} dB is speech level"))
        elif c["start"] - prev < CLEAR:
            skip.append((c, f"only {c['start'] - prev:.2f}s after {c['after']!r}"))
        elif nxt - c["end"] < CLEAR:
            skip.append((c, f"only {nxt - c['end']:.2f}s before {c['before']!r}"))
        else:
            keep.append(c)

    print(f"ducking {len(keep)}, leaving {len(skip)}\n")
    for c in keep:
        gain_db = min(0.0, (c["floor"] + HEADROOM) - c["peak"])
        print(f"  {c['start']:6.2f}-{c['end']:<6.2f}  peak {c['peak']:6.1f} -> "
              f"{c['peak'] + gain_db:6.1f} dB  ({gain_db:+.1f})   …{c['after']!r} | {c['before']!r}…")
    for c, why in skip:
        print(f"  skip {c['start']:6.2f}-{c['end']:<6.2f}  {why}")

    if not args.apply:
        print("\ndry run — pass --apply to write")
        return

    out = list(samples)
    for c in keep:
        gain = 10 ** (min(0.0, (c["floor"] + HEADROOM) - c["peak"]) / 20)
        i0, i1 = int(c["start"] * sr), int(c["end"] * sr)
        f = max(1, int(FADE * sr))
        for i in range(i0, min(i1, len(out))):
            if i - i0 < f:
                t = (i - i0) / f
            elif i1 - i < f:
                t = (i1 - i) / f
            else:
                t = 1.0
            ramp = (1 - math.cos(math.pi * t)) / 2          # raised cosine
            g = 1.0 + (gain - 1.0) * ramp
            out[i] = int(max(-32768, min(32767, out[i] * g)))

    w = wave.open(str(DST), "wb")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(struct.pack(f"<{len(out)}h", *out))
    w.close()
    print(f"\nwrote {DST}")


if __name__ == "__main__":
    main()
