"""
Master VO through a bright+weighty broadcast-voice ffmpeg chain. No
external API, no monthly fee, no watermark. Uses the padded, room-toned
clean master written by generate_vo.py (falling back to .raw.mp3 only
for legacy batches) and writes
.broadcast.mp3. --commit promotes to primary .mp3.

The BROADCAST chain: hi-pass, cut the boxy 300-400 Hz mud, small bass
body shelf for weight, presence lift at 4.5 kHz for consonants, air
lift at 10-13 kHz for openness, light de-ess, gentle compressor for
evenness, two-pass loudnorm to -14 LUFS. This is the HowMoneyWorks /
Bloomberg documentary voice profile — bright with weight, not warm
and dull.

Usage:
    python scripts/originate/master_vo_local.py originate/<slug>/vo/
    python scripts/originate/master_vo_local.py originate/<slug>/vo/ --sections hook
    python scripts/originate/master_vo_local.py originate/<slug>/vo/ --commit
    python scripts/originate/master_vo_local.py originate/<slug>/vo/ --chain clean
"""

import argparse
import subprocess
import sys
from pathlib import Path


# Bright+weighty broadcast voice — this is the default. Each EQ move
# is deliberate; do not add "warm" back or the whole point is lost.
BROADCAST_CHAIN = (
    # Broadcast VO chain, revised per engineer read (2026-08-02):
    #   - "voice body range heavy" → cut at 200 Hz instead of boost
    #   - "high-pass 70-85 Hz" → lower corners (was 115/90 → 80/70)
    #   - "presence 2.5-4 kHz +0.5 to +1.5" → moved from 4500 → 3200, gain +2 → +1.2
    #   - "cap at -1.5 to -2.0 dBTP" → limiter to -2 dBTP for video re-encode headroom
    #   - "already controlled, don't compress more" → no additional dynamics
    # Plosive control (from prior iteration): two-stage highpass + surgical
    # notch at 85 Hz. Softened because engineer noted overall low end was
    # already thick — trimming pop energy no longer needs to work around
    # a compensating body boost.
    "highpass=f=80,"                                                       # engineer: 70-85 Hz range
    "highpass=f=70,"                                                       # second pass — combined ~24 dB/oct steepness in plosive band
    "equalizer=f=85:t=q:w=1.1:g=-3.0,"                                    # surgical plosive notch
    "equalizer=f=200:t=q:w=1.2:g=-1.5,"                                   # engineer: gentle 160-250 Hz cut ("chesty/thick")
    "equalizer=f=350:t=q:w=1.4:g=-1.0,"                                   # residual mud cut (softer — 200 already cuts)
    "equalizer=f=3200:t=q:w=1.2:g=1.2,"                                   # engineer: 2.5-4 kHz presence lift
    "equalizer=f=10500:t=q:w=1.4:g=1.0,"                                  # openness (softened from +1.5)
    "equalizer=f=13500:t=q:w=1.8:g=1.5,"                                  # air (softened from +1.8)
    "deesser=i=0.28,"                                                      # engineer: light, only catch sharp S
    "alimiter=level_in=1:level_out=1:limit=0.794:attack=5:release=50,"    # -2 dBTP ceiling (was -1)
    "loudnorm=I=-14:TP=-2:LRA=11"                                         # broadcast target; master_final locks final mix
)

# Clean chain kept for parity with generate_vo.py's default (highpass +
# deesser + loudnorm only). Use when the ElevenLabs raw is already
# broadcast-ready and any EQ would harm it.
CLEAN_CHAIN = (
    "highpass=f=85,"
    "deesser=i=0.35,"
    "loudnorm=I=-14:TP=-1.5:LRA=9"
)

CHAINS = {"broadcast": BROADCAST_CHAIN, "clean": CLEAN_CHAIN}
SUFFIX = {"broadcast": ".broadcast.mp3", "clean": ".clean.mp3"}


def process(raw: Path, chain: str) -> Path:
    section = raw.name.removesuffix(".raw.mp3")
    out = raw.parent / f"{section}{SUFFIX[chain]}"
    if out.exists():
        print(f"  {section}: cached ({out.name})")
        return out
    # generate_vo.py's .raw.mp3 is captured by its first mastering pass before
    # section_pad_s and room tone are added. Mastering that file used to remove
    # every approved breath between sections while timeline.json retained the
    # padding, creating cumulative caption/visual drift. The clean primary is
    # the correct first-run source; after a promotion, .legacy.mp3 preserves it
    # for deterministic remastering.
    legacy = raw.parent / f"{section}.legacy.mp3"
    primary = raw.parent / f"{section}.mp3"
    source = legacy if legacy.exists() else primary if primary.exists() else raw
    print(f"→ {section}: {chain} chain from {source.name}...")
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
         "-i", str(source), "-af", CHAINS[chain],
         "-ar", "44100", "-b:a", "192k", str(out)],
        check=True,
    )
    print(f"  ✓ {section} → {out.name}")
    return out


def commit(vo_dir: Path, chain: str) -> int:
    """Promote every .<chain>.mp3 to primary .mp3. Backs up existing
    primaries to .legacy.mp3 ONCE (won't overwrite an existing legacy)."""
    suffix = SUFFIX[chain]
    promoted = 0
    for src in sorted(vo_dir.glob(f"*{suffix}")):
        section = src.name.removesuffix(suffix)
        primary = vo_dir / f"{section}.mp3"
        legacy = vo_dir / f"{section}.legacy.mp3"
        if primary.exists() and not legacy.exists():
            primary.rename(legacy)
        src.replace(primary)
        print(f"  ✓ {section}: promoted (legacy kept at {legacy.name})")
        promoted += 1
    return promoted


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("vo_dir", type=Path, help="originate/<slug>/vo/")
    ap.add_argument("--sections", nargs="+",
                    help="section ids to process (default: all *.raw.mp3)")
    ap.add_argument("--chain", choices=CHAINS.keys(), default="broadcast",
                    help="which mastering chain (default: broadcast)")
    ap.add_argument("--commit", action="store_true",
                    help="promote .broadcast.mp3 (or .clean.mp3) → primary .mp3")
    args = ap.parse_args()

    if not args.vo_dir.is_dir():
        sys.exit(f"Not a directory: {args.vo_dir}")

    if args.sections:
        raws = [args.vo_dir / f"{s}.raw.mp3" for s in args.sections]
        missing = [r for r in raws if not r.exists()]
        if missing:
            sys.exit(f"Missing raw files: {[str(m) for m in missing]}")
    else:
        raws = sorted(args.vo_dir.glob("*.raw.mp3"))
        if not raws:
            sys.exit(f"No *.raw.mp3 files in {args.vo_dir}")

    print(f"Mastering {len(raws)} section(s) via '{args.chain}' chain")
    for raw in raws:
        process(raw, args.chain)

    if args.commit:
        print("\nCommitting to primary...")
        n = commit(args.vo_dir, args.chain)
        print(f"Promoted {n} section(s). Legacy masters kept as *.legacy.mp3.")
    else:
        print("\nA/B ready. Compare:")
        print(f"  existing:   {args.vo_dir}/<section>.mp3")
        print(f"  {args.chain}:  {args.vo_dir}/<section>{SUFFIX[args.chain]}")
        print("Promote with:  --commit")


if __name__ == "__main__":
    main()
