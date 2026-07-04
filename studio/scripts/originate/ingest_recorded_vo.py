"""
Ingest RECORDED voiceover (2026-07-04): Manav reads the performed script;
this replaces ElevenLabs synthesis with the real thing. The training
session for the PVC doubles as the pilot's actual VO.

Takes one audio file per section in originate/<slug>/recorded/
(hook.wav, thesis.wav, … — wav/m4a/mp3 all fine) and produces the exact
vo/ cache shape generate_vo.py writes, so EVERYTHING downstream is
untouched: run generate_vo afterwards (it assembles words.json +
timeline.json from the caches without touching ElevenLabs), then
hand_tune → pace → prepare → arrange → render.

Per section:
  1. Master (same softened chain as synthetic VO) + tail pad + room tone
  2. Word timestamps via OpenAI Whisper API (word granularity)
  3. Caption display restored from the performed script (Whisper strips
     punctuation/casing; we align its words to performed-<id>.txt tokens
     so captions read "Okay, so." not "okay so")

Needs OPENAI_API_KEY (same key viddy's transcribe step uses).

Usage:
    python scripts/originate/ingest_recorded_vo.py originate/<slug>/script.json
        [--recorded-dir originate/<slug>/recorded]
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_vo import MASTER_CHAIN, pad_tail, room_tone  # noqa: E402

ROOT = Path(__file__).parent.parent.parent
AUDIO_EXTS = (".wav", ".m4a", ".mp3", ".aiff", ".flac")


def find_recording(rec_dir: Path, section_id: str) -> Path | None:
    for ext in AUDIO_EXTS:
        p = rec_dir / f"{section_id}{ext}"
        if p.exists():
            return p
    return None


def whisper_words(audio_path: Path) -> list[dict]:
    from openai import OpenAI
    client = OpenAI()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav16 = Path(tf.name)
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(audio_path), "-ar", "16000", "-ac", "1",
                    "-acodec", "pcm_s16le", str(wav16)], check=True)
    try:
        with open(wav16, "rb") as f:
            resp = client.audio.transcriptions.create(
                model="whisper-1", file=f, response_format="verbose_json",
                timestamp_granularities=["word"], language="en")
    finally:
        wav16.unlink(missing_ok=True)
    return [{"word": w.word.strip(), "start": w.start, "end": w.end}
            for w in (resp.words or [])]


def _norm(w: str) -> str:
    return re.sub(r"[^\w']", "", w).lower()


def restore_display(words: list[dict], performed_text: str) -> list[dict]:
    """Align Whisper's stripped words to the performed script's tokens so
    captions keep punctuation and casing. Unmatched words (ad-libs,
    retake residue) keep Whisper's form."""
    script_tokens = [t for t in performed_text.split()
                     if not (t.startswith("[") or t.endswith("]"))]
    a = [_norm(w["word"]) for w in words]
    b = [_norm(t) for t in script_tokens]
    out = [dict(w) for w in words]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            out[block.a + k]["word"] = script_tokens[block.b + k]
    return out


def main():
    ap = argparse.ArgumentParser(description="Ingest recorded VO sections")
    ap.add_argument("script")
    ap.add_argument("--recorded-dir", default=None)
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = ap.parse_args()

    script_path = Path(args.script)
    base = script_path.parent
    script = json.loads(script_path.read_text())
    config = json.loads(Path(args.config).read_text())
    vo_cfg = config["voiceover"]
    rec_dir = Path(args.recorded_dir) if args.recorded_dir else base / "recorded"
    if not rec_dir.exists():
        print(f"Error: {rec_dir} not found. Drop one file per section there "
              f"(hook.wav, thesis.wav, …).", file=sys.stderr)
        sys.exit(1)

    vo_dir = base / "vo"
    vo_dir.mkdir(exist_ok=True)

    missing = []
    for section in script["sections"]:
        sid = section["id"]
        rec = find_recording(rec_dir, sid)
        if not rec:
            missing.append(sid)
            continue
        print(f"  {sid}: {rec.name}")
        out_mp3 = vo_dir / f"{sid}.mp3"
        # Master with the same chain as synthetic VO (keeps episode tone
        # uniform if a section ever mixes sources), then pad + room tone.
        subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                        "-i", str(rec), "-af", MASTER_CHAIN,
                        "-ar", "44100", "-b:a", "192k", str(out_mp3)], check=True)
        pad_s = float(vo_cfg.get("section_pad_s", 0.0))
        if pad_s > 0:
            pad_tail(out_mp3, pad_s)
        if vo_cfg.get("room_tone", True):
            room_tone(out_mp3)

        words = whisper_words(out_mp3)
        performed = vo_dir / f"performed-{sid}.txt"
        if performed.exists():
            words = restore_display(words, performed.read_text())

        # Duration = actual mastered+padded file (authoritative).
        p = subprocess.run(["ffprobe", "-hide_banner", "-show_entries",
                            "format=duration", "-of", "csv=p=0", str(out_mp3)],
                           capture_output=True, text=True)
        duration = float(p.stdout.strip())
        (vo_dir / f"words-{sid}.json").write_text(
            json.dumps({"duration": duration, "words": words}))
        print(f"    {len(words)} words · {duration:.1f}s")

    if missing:
        print(f"\n⚠ no recording found for: {', '.join(missing)} — "
              f"those sections keep their existing (synthetic) caches.")

    print("\nNow assemble + continue the normal chain:")
    print("  python scripts/originate/generate_vo.py <script>   (assembles from caches)")
    print("  python originate/<slug>/hand_tune_storyboard.py")
    print("  pace_storyboard → prepare_longform → arrange_bed → render")


if __name__ == "__main__":
    main()
