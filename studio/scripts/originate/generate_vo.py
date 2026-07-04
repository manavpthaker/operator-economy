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
import re
import subprocess
import sys
from pathlib import Path

import requests

# Mastering v2 (2026-07-03, "pharma ad" fix): the original chain
# (exciter 2.2 / presence +2.5 / air +3.5) over-articulated the voice —
# hyper-crisp diction read as ad-narrator. Softened to roughly half
# enhancement: warm, present, human. Duration unchanged → timestamps
# stay aligned. Raw file kept beside the master.
MASTER_CHAIN = (
    "highpass=f=70,"
    "aexciter=level_in=1:level_out=1:amount=1.1:drive=4:blend=0:freq=6500:ceil=13000,"
    "anequalizer=c0 f=3800 w=1600 g=1.2 t=1|c0 f=11000 w=5000 g=1.8 t=1,"
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


def room_tone(path: Path) -> None:
    """Mix faint brown-noise room tone (-~55dB, band-limited) under the
    whole section INCLUDING the tail pad — a real mic never records
    digital zero, and the ear knows (2026-07-03 'real person' pass).
    Runs after pad_tail so the breath between sections has air in it."""
    tmp = path.with_suffix(".room.mp3")
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(path), "-filter_complex",
                    "anoisesrc=colour=brown:amplitude=0.0016:duration=3600[nz];"
                    "[nz]highpass=f=80,lowpass=f=4000[room];"
                    "[0:a][room]amix=inputs=2:duration=first:normalize=0[out]",
                    "-map", "[out]", "-ar", "44100", "-b:a", "192k", str(tmp)],
                   check=True)
    tmp.replace(path)


# ---------------------------------------------------------------------
# Performance pass (2026-07-03): written English read aloud sounds READ.
# This pass rewrites each section's vo_text into performed think-aloud
# speech — the register locked on the loose-E demo (Louis CK/Gillis
# principle: written to sound unwritten). The performed text is what
# gets spoken AND captioned (minus tags); script.json stays canonical
# for claims. Cached per section for review at the pre-publish gate.
# ---------------------------------------------------------------------

PERFORM_SYSTEM = """You transform a YouTube narration section from written prose into PERFORMED think-aloud speech for ElevenLabs v3. The speaker is a wry mid-40s New York insider explaining how the game works to a friend — practiced material delivered like it's off the top of his head.

HARD RULES (violating any = failure):
- Preserve every claim, number, name, source mention, and the ORDER of ideas exactly. No new facts, no dropped facts, no changed figures.
- Never place a tag or ellipsis inside a number, or between a number and its source/qualifier ("reported", "estimate").
- NO EM DASHES anywhere in the output. Where prose wants "—", use a new sentence, an ellipsis, or a paragraph break instead.
- Output plain text only — the performed section, nothing else.

TECHNIQUES (use per the density instruction):
- Mid-thought pivots and restatements: "They know it. They just... nobody knows how."
- Rhetorical questions doing the emphasis: "That gap? Between knowing and doing?"
- Discourse markers: "Okay, so." "And look —" "right?" "Here's the thing."
- Fragments for lists: "The intake. The follow-ups. The reporting."
- Paragraph breaks (blank line) between thoughts — these become real stops.
- Breath tags at thought boundaries: [exhales] [inhales] [short pause] — standalone, never mid-clause.
- Ellipses where a person hunts for the next word.

DENSITY:
- seasoned (hook, thesis, cta): full treatment — tags at the open, paragraph breathing throughout, one deliberate restatement.
- light (evidence, stack, playbook, economics): tighter — paragraph breaks and an occasional "right?" / pivot; at most ONE breath tag per ~40s of material; numbers and sources flow clean and uninterrupted.

LENGTH BUDGET (hard):
- hook: output word count within +10% of the source — the hook is a ≤15s cold open and COMPRESSION IS THE CRAFT. Air comes from one or two short pauses, never from added words.
- all other sections: within +25% of the source word count.

Throwaway the setups, land the payoffs: the sentence BEFORE a key line can be casual/quick; the key line itself gets space around it."""

SEASONED = {"hook", "thesis", "cta"}


def perform_section(section: dict, vo_dir: Path, config: dict, text: str) -> str:
    cache = vo_dir / f"performed-{section['id']}.txt"
    if cache.exists():
        return cache.read_text()
    try:
        import anthropic
    except ImportError:
        print("  (anthropic SDK missing — skipping performance pass)", file=sys.stderr)
        return text
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("  (ANTHROPIC_API_KEY not set — skipping performance pass)", file=sys.stderr)
        return text
    density = "seasoned" if section["id"] in SEASONED else "light"
    # Voice-print: observed speech patterns from Manav's real recording
    # sessions (config/speech-profile.md). When present it overrides the
    # generic register — the goal is HIS cadence, not a house style.
    system = PERFORM_SYSTEM
    profile = ROOT / "config" / "speech-profile.md"
    if profile.exists():
        system += ("\n\nVOICE-PRINT (observed patterns from the narrator's real "
                   "recordings — these override the generic techniques above; "
                   "match THIS person):\n\n" + profile.read_text())
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=config.get("models", {}).get("script", "claude-sonnet-4-20250514"),
        max_tokens=3000,
        system=system,
        messages=[{"role": "user", "content":
                   f"Section: {section['id']} · Density: {density}\n\n{text}"}],
    )
    performed = next(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    cache.write_text(performed)
    print(f"  performed: {section['id']} ({density}, {len(text)}→{len(performed)} chars)")
    return performed


def strip_tag_words(words: list[dict]) -> list[dict]:
    """Remove audio-tag tokens ([exhales], [short pause], …) from the
    word list so they never reach captions. Tags may span tokens
    ('[short' + 'pause]')."""
    out, in_tag = [], False
    for w in words:
        tok = w["word"].strip()
        if not in_tag and tok.startswith("["):
            if not tok.endswith("]"):
                in_tag = True
            continue
        if in_tag:
            if tok.endswith("]"):
                in_tag = False
            continue
        out.append(w)
    return out

ROOT = Path(__file__).parent.parent.parent
API_BASE = "https://api.elevenlabs.io/v1"


def section_text(section: dict) -> str:
    return " ".join(beat["vo_text"].strip() for beat in section.get("beats", []))


# ---------------------------------------------------------------------
# Speech aliases (2026-07-03): eleven_v3 silently ignores pronunciation
# dictionary locators (verified on the pilot — Airtable/n8n unchanged
# with the dictionary attached). The model-independent fix: SPEAK a
# phonetic spelling, then restore the display word in the alignment so
# captions still show "n8n", not "en eight en".
# ---------------------------------------------------------------------

def apply_speech_aliases(text: str, aliases: dict) -> str:
    for display, spoken in aliases.items():
        text = re.sub(rf"(?<!\w){re.escape(display)}(?!\w)", spoken, text)
    return text


def restore_alias_words(words: list[dict], aliases: dict) -> list[dict]:
    """Collapse spoken-alias token runs back to the display word, keeping
    the first token's start, the last token's end, and any punctuation
    that clung to the run's edges."""
    def norm(w: str) -> str:
        return re.sub(r"[^\w']", "", w).lower()

    seqs = [( [norm(t) for t in spoken.split()], display)
            for display, spoken in aliases.items()]
    out, i = [], 0
    while i < len(words):
        hit = None
        for toks, display in seqs:
            n = len(toks)
            if i + n <= len(words) and [norm(w["word"]) for w in words[i:i + n]] == toks:
                hit = (n, display)
                break
        if hit:
            n, display = hit
            lead = re.match(r"^[^\w']*", words[i]["word"]).group(0)
            trail = re.search(r"[^\w']*$", words[i + n - 1]["word"]).group(0)
            out.append({"word": lead + display + trail,
                        "start": words[i]["start"], "end": words[i + n - 1]["end"]})
            i += n
        else:
            out.append(words[i])
            i += 1
    return out


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
        # Performance pass: prose → performed think-aloud (cached for
        # gate review at vo/performed-<id>.txt).
        if vo_cfg.get("performance", {}).get("enabled", False):
            with open(args.config) as _f:
                full_config = json.load(_f)
            text = perform_section(section, vo_dir, full_config, text)
        aliases = {k: v for k, v in (vo_cfg.get("speech_aliases") or {}).items()
                   if not k.startswith("_")}
        spoken_text = apply_speech_aliases(text, aliases) if aliases else text
        # Audio tags ([exhales], [short pause], …) are an eleven_v3
        # feature — every other model reads them as literal text. On
        # non-v3 models strip them; paragraph breaks + ellipses carry
        # the pacing instead.
        if vo_cfg["model_id"] != "eleven_v3":
            spoken_text = re.sub(r"\[[^\]\n]{1,40}\]", "", spoken_text)
            spoken_text = re.sub(r"[ \t]{2,}", " ", spoken_text)
            spoken_text = re.sub(r"\n{3,}", "\n\n", spoken_text).strip()
        voice_settings = {
            "stability": vo_cfg["stability"],
            "similarity_boost": vo_cfg["similarity_boost"],
        }
        if vo_cfg.get("style") is not None:
            voice_settings["style"] = vo_cfg["style"]
        payload = {
            "text": spoken_text,
            "model_id": vo_cfg["model_id"],
            "voice_settings": voice_settings,
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
        if aliases:
            words_local = restore_alias_words(words_local, aliases)
        words_local = strip_tag_words(words_local)
        duration_local = data["alignment"]["character_end_times_seconds"][-1]
        # Breath between sections: pad the tail with silence and count it
        # in the section duration so every downstream offset carries it.
        pad_s = float(vo_cfg.get("section_pad_s", 0.0))
        if pad_s > 0:
            pad_tail(audio_path, pad_s)
            duration_local += pad_s
        # Room tone under everything, pad included (never digital zero).
        if vo_cfg.get("room_tone", True):
            room_tone(audio_path)
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
