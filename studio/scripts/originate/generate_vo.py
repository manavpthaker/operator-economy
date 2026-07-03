"""
Originate Step 2: Generate voiceover audio with word-level timestamps.

Reads the approved script.json and produces one MP3 per section via the
ElevenLabs with-timestamps API, plus a words.json compatible with the
caption pipeline (same word/start/end shape as Whisper output).

Refuses to run if any [POV: ...] tokens remain in the script (Gate 1
was skipped).

Usage:
    python scripts/originate/generate_vo.py originate/<slug>/script.json

Output:
    originate/<slug>/vo/<section_id>.mp3
    originate/<slug>/vo/words.json     # [{section, word, start, end}] global timeline
    originate/<slug>/vo/timeline.json  # per-section start/duration
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

# Broadcast-crispness mastering (validated 2026-07-03 A/B): harmonic
# exciter restores highs, presence + air EQ, de-ess, -14 LUFS. Duration
# is unchanged, so word timestamps stay aligned. Raw file kept beside it.
MASTER_CHAIN = (
    "highpass=f=70,"
    "aexciter=level_in=1:level_out=1:amount=2.2:drive=6:blend=0:freq=6500:ceil=14000,"
    "anequalizer=c0 f=3800 w=1600 g=2.5 t=1|c0 f=11000 w=5000 g=3.5 t=1,"
    "deesser=i=0.3,"
    "loudnorm=I=-14:TP=-1.5:LRA=9"
)


def master(path: Path) -> None:
    raw = path.with_suffix(".raw.mp3")
    path.rename(raw)
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(raw), "-af", MASTER_CHAIN,
                    "-ar", "44100", "-b:a", "192k", str(path)], check=True)


def pad_tail(path: Path, pad_s: float) -> None:
    """Append `pad_s` of silence to the section — the breath between
    sections (added 2026-07-03: sections read back-to-back with no room
    to breathe). Runs AFTER mastering so loudnorm sees only speech.
    Padded duration must be reflected in the cached duration so the
    timeline offsets carry the breath downstream."""
    if pad_s <= 0:
        return
    tmp = path.with_suffix(".pad.mp3")
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(path), "-af", f"apad=pad_dur={pad_s}",
                    "-ar", "44100", "-b:a", "192k", str(tmp)], check=True)
    tmp.replace(path)

ROOT = Path(__file__).parent.parent.parent
API_BASE = "https://api.elevenlabs.io/v1"


def section_text(section: dict) -> str:
    return " ".join(beat["vo_text"].strip() for beat in section.get("beats", []))


def chars_to_words(alignment: dict, offset: float) -> list[dict]:
    """Convert ElevenLabs character alignment to word-level timestamps."""
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    words, current, w_start = [], "", None
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if current:
                words.append({"word": current, "start": w_start + offset, "end": prev_end + offset})
                current, w_start = "", None
        else:
            if not current:
                w_start = s
            current += ch
            prev_end = e
    if current:
        words.append({"word": current, "start": w_start + offset, "end": prev_end + offset})
    return words


def main():
    parser = argparse.ArgumentParser(description="Generate section voiceovers via ElevenLabs")
    parser.add_argument("script", help="Path to approved script.json")
    parser.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    with open(args.config) as f:
        vo_cfg = json.load(f)["voiceover"]
    if vo_cfg["voice_id"] == "SET_ME":
        print("Error: set voiceover.voice_id in config/blueprint.json", file=sys.stderr)
        sys.exit(1)

    script_path = Path(args.script)
    with open(script_path) as f:
        script = json.load(f)

    raw = json.dumps(script)
    if "[POV:" in raw:
        print("Error: script still contains [POV: ...] tokens — Gate 1 not complete.", file=sys.stderr)
        sys.exit(1)

    vo_dir = script_path.parent / "vo"
    vo_dir.mkdir(exist_ok=True)

    all_words, timeline, offset = [], [], 0.0
    for section in script["sections"]:
        text = section_text(section)
        if not text:
            continue
        # Resumable: reuse cached section audio + alignment if present
        cache = vo_dir / f"words-{section['id']}.json"
        if cache.exists() and (vo_dir / f"{section['id']}.mp3").exists():
            cached = json.loads(cache.read_text())
            words = [dict(w, start=w["start"] + offset, end=w["end"] + offset,
                          section=section["id"]) for w in cached["words"]]
            all_words.extend(words)
            timeline.append({"section": section["id"], "start": offset,
                             "duration": cached["duration"],
                             "audio": f"{section['id']}.mp3"})
            offset += cached["duration"]
            print(f"  VO: {section['id']} (cached, {cached['duration']:.1f}s)")
            continue
        print(f"  VO: {section['id']} ({len(text)} chars)")
        payload = {
            "text": text,
            "model_id": vo_cfg["model_id"],
            "voice_settings": {
                "stability": vo_cfg["stability"],
                "similarity_boost": vo_cfg["similarity_boost"],
            },
            "output_format": vo_cfg.get("output_format", "mp3_44100_128"),
        }
        # Pronunciation dictionary (Airtable, n8n, SaaS…) — requires
        # eleven_v3; silently ignored on multilingual_v2.
        pdict = vo_cfg.get("pronunciation_dictionary")
        if pdict and pdict.get("id"):
            payload["pronunciation_dictionary_locators"] = [{
                "pronunciation_dictionary_id": pdict["id"],
                "version_id": pdict.get("version_id"),
            }]
        resp = requests.post(
            f"{API_BASE}/text-to-speech/{vo_cfg['voice_id']}/with-timestamps",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=300,
        )
        resp.raise_for_status()
        data = resp.json()

        audio_path = vo_dir / f"{section['id']}.mp3"
        audio_path.write_bytes(base64.b64decode(data["audio_base64"]))
        if vo_cfg.get("mastering", True):
            master(audio_path)

        words_local = chars_to_words(data["alignment"], 0.0)
        duration_local = data["alignment"]["character_end_times_seconds"][-1]
        # Breath between sections: pad the tail with silence and count it
        # in the section duration so every downstream offset carries it.
        pad_s = float(vo_cfg.get("section_pad_s", 0.0))
        if pad_s > 0:
            pad_tail(audio_path, pad_s)
            duration_local += pad_s
        cache.write_text(json.dumps({"duration": duration_local, "words": words_local}))

        words = [dict(w, start=w["start"] + offset, end=w["end"] + offset,
                      section=section["id"]) for w in words_local]
        all_words.extend(words)

        timeline.append({"section": section["id"], "start": offset, "duration": duration_local,
                         "audio": str(audio_path.name)})
        offset += duration_local

    with open(vo_dir / "words.json", "w") as f:
        json.dump(all_words, f, indent=2)
    with open(vo_dir / "timeline.json", "w") as f:
        json.dump({"total_seconds": offset, "sections": timeline}, f, indent=2)

    print(f"\n✓ {len(timeline)} sections, {offset:.1f}s total → {vo_dir}")


if __name__ == "__main__":
    main()
