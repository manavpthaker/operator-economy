#!/usr/bin/env python3
"""Place each Short's movement boundaries on measured word boundaries in the accepted audio.

PICTURE-GRAMMAR-V1.md assigns paragraphs to the three movements and carries estimated
windows at 2.54 words a second. It also says those estimates are placeholders and that
boundaries must land on measured word boundaries, never on a proportioned guess. This
replaces them, now that the narration is owner accepted.

Method, and its honest precision: the locked paragraphs are anchored into the accepted
audio's word-level ASR timings by exact phrase match on the paragraph's closing and
opening words, never by proportion. Each cut is then placed inside the measured silence
between the last word of one movement and the first word of the next. Whisper word times
are approximate at the tens-of-milliseconds level, which is immaterial at a sentence
boundary with real silence either side, and the measured gap is reported for every cut so
the margin is visible. This is not WhisperX forced alignment; where a gap is tight it says
so rather than implying a precision it does not have.

Usage: beat_timing.py [--write]
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = next(p for p in (BASE, *BASE.parents) if p.name == "operator-economy")
W = BASE / "narration-v4"
GRAMMAR = BASE / "PICTURE-GRAMMAR-V1.md"

# Paragraph index per movement, exactly as PICTURE-GRAMMAR-V1.md assigns them.
PLAN = {
    "01": {"slug": "01-book-your-own-room", "presenter_open": [0, 1], "screens": [2, 3], "presenter_close": [4, 5]},
    "02": {"slug": "02-sounds-like-marketing", "presenter_open": [0], "screens": [1, 2], "presenter_close": [3]},
    "03": {"slug": "03-the-guest-book", "presenter_open": [0], "screens": [1, 2, 3], "presenter_close": [4]},
    "04": {"slug": "04-four-numbers", "presenter_open": [0], "screens": [1, 2, 3], "presenter_close": [4, 5]},
}
END_BRIDGE_SECONDS = 2.0


import importlib.util as _ilu
_cn = _ilu.spec_from_file_location("oe_capture", BASE / "capture_narration.py")
cn = _ilu.module_from_spec(_cn)
_cn.loader.exec_module(cn)


def toks(s: str) -> list[str]:
    """The same number-aware normalizer the exact-copy gate uses, stringified.

    The script says "twenty" and the transcriber writes "20"; matching on surface
    strings fails there, which is exactly how the first run of this tool failed to
    anchor Short 02.
    """
    return [str(x) for x in cn.norm(s)]


def paragraphs(short_id: str) -> list[str]:
    md = GRAMMAR.read_text()
    spoken = json.loads((BASE / "SPOKEN-TEXT-V1.json").read_text())["scripts"]
    text = next(s["spoken_text"] for s in spoken if s["id"] == short_id)
    # The locked scripts' own paragraph breaks live in STANDALONE-SCRIPTS-V1.md.
    src = (BASE / "STANDALONE-SCRIPTS-V1.md").read_text()
    for m in re.finditer(r"^## (\d)\. (.+?)$(.*?)(?=^Standalone payoff)", src, re.M | re.S):
        if m.group(1) != str(int(short_id)):
            continue
        out, cur = [], []
        for line in m.group(3).splitlines():
            if line.startswith("> ") and line[2:].strip():
                cur.append(line[2:].strip())
            elif cur:
                out.append(" ".join(cur))
                cur = []
        if cur:
            out.append(" ".join(cur))
        # the spoken layer renders one written form; apply it so tokens match the audio
        return [p.replace("Booking.com's", "Booking dot com's") for p in out]
    raise SystemExit(f"no paragraphs for {short_id}")


def words(short_id: str) -> list[dict]:
    d = W / PLAN[short_id]["slug"]
    cands = sorted(d.glob("final-asr-*/transcript.json")) + sorted(d.glob("final-asr-*/*/transcript.json"))
    if not cands:
        raise SystemExit(f"no accepted-audio transcript for {short_id}")
    # prefer the model whose read was accepted for this short
    for q in cands:
        model = q.parent.name.replace("final-asr-", "")
        rec = d / f"FINAL-ASR.{model}.json"
        if rec.exists() and json.loads(rec.read_text()).get("accepted"):
            return json.loads(q.read_text()), model
    return json.loads(cands[0].read_text()), cands[0].parent.name.replace("final-asr-", "")


def flat(ws: list[dict]) -> tuple[list[str], list[int]]:
    """Flatten ASR words to normalized tokens, keeping a token -> word index map."""
    fl, owner = [], []
    for i, w in enumerate(ws):
        for tk in toks(w["text"]):
            fl.append(tk)
            owner.append(i)
    return fl, owner


def find(ws: list[dict], phrase: list[str], from_token: int = 0):
    """First (word_index, token_index) where an exact normalized phrase begins."""
    fl, owner = flat(ws)
    n = len(phrase)
    for i in range(from_token, len(fl) - n + 1):
        if fl[i:i + n] == phrase:
            return owner[i], i
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    report = {}
    for sid, plan in PLAN.items():
        ps = paragraphs(sid)
        ws, model = words(sid)
        moves, cursor, rows = ["presenter_open", "screens", "presenter_close"], 0, []
        for mv in moves:
            idx = plan[mv]
            head = toks(ps[idx[0]])[:4]
            tail = toks(ps[idx[-1]])[-4:]
            h = find(ws, head, cursor)
            if h is None:
                raise SystemExit(f"{sid}: could not anchor the opening of {mv}: {head}")
            tl = find(ws, tail, h[1])
            if tl is None:
                raise SystemExit(f"{sid}: could not anchor the close of {mv}: {tail}")
            fi = h[0]
            lj = flat(ws)[1][tl[1] + len(tail) - 1]
            rows.append({"movement": mv, "paragraphs": idx,
                         "first_word": ws[fi]["text"], "first_word_start_s": ws[fi]["start"],
                         "last_word": ws[lj]["text"], "last_word_end_s": ws[lj]["end"],
                         "spoken_seconds": round(ws[lj]["end"] - ws[fi]["start"], 3)})
            cursor = tl[1] + len(tail)
        cuts = []
        FPS = 24
        for i in range(len(rows) - 1):
            end_prev = rows[i]["last_word_end_s"]
            start_next = rows[i + 1]["first_word_start_s"]
            gap = round(start_next - end_prev, 3)
            # Cut on the incoming word's onset, snapped back to a frame boundary, rather
            # than at the midpoint of the gap. The outgoing movement then keeps its word
            # complete and the incoming movement starts exactly as the new sentence does.
            # Midpoints looked reasonable in the abstract and are far too tight in practice:
            # six of these eight gaps are under 0.30 s and four are under 0.12 s.
            frame = int(start_next * FPS)
            cut = round(frame / FPS, 6)
            cuts.append({"between": f"{rows[i]['movement']} -> {rows[i+1]['movement']}",
                         "prev_word_end_s": end_prev, "next_word_start_s": start_next,
                         "measured_gap_s": gap,
                         "cut_at_s": cut, "cut_at_frame_24fps": frame,
                         "outgoing_keeps_word_by_s": round(cut - end_prev, 3),
                         "midpoint_alternative_s": round(end_prev + gap / 2, 3) if gap > 0 else end_prev,
                         "margin": ("comfortable" if gap >= 0.30 else
                                    "tight" if gap >= 0.12 else "very tight, inspect by ear")})
        last_end = rows[-1]["last_word_end_s"]
        audio = json.loads((W / "NARRATION-FINAL.json").read_text())
        dur = next(s["seconds"] for s in audio["shorts"] if s["short"] == sid)
        report[sid] = {
            "slug": plan["slug"], "asr_model": model,
            "accepted_audio_seconds": dur,
            "movements": rows, "cuts": cuts,
            "post_word_hold_s": round(dur - last_end, 3),
            "end_bridge_seconds": END_BRIDGE_SECONDS,
            "total_picture_seconds": round(dur + END_BRIDGE_SECONDS, 3),
            "presenter_share_of_speech": round(
                (rows[0]["spoken_seconds"] + rows[2]["spoken_seconds"])
                / sum(r["spoken_seconds"] for r in rows), 3),
        }
    out = {"schema": "oe-beat-timing-v1", "at_utc": "2026-10-08T00:00:00Z",
           "episode": "EP009", "episode_slug": "direct-booking-practice",
           "basis": "owner-accepted Original C narration, event ep009-shorts-narration-owner-accepted-v1",
           "method": ("Paragraphs anchored into the accepted audio's word timings by exact phrase match on "
                      "closing and opening words, never by proportion. Each cut is placed on the incoming "
                      "word's onset, snapped back to a 24 fps frame boundary, so the outgoing movement keeps "
                      "its last word complete. The measured gap is reported for every cut so the margin is "
                      "visible. Whisper word times are approximate at the tens-of-milliseconds level; this is "
                      "not WhisperX forced alignment and does not claim that precision."),
           "finding": ("The narration was generated as one continuous read per Short, so there is no "
                       "engineered silence at the movement boundaries. Six of the eight gaps are under 0.30 s "
                       "and four are under 0.12 s, against the 0.35 to 0.55 s protected hold in EP007's "
                       "accepted Short 01. Onset-aligned frame-snapped cuts are what make these usable "
                       "without new audio; a midpoint cut would clip the outgoing word's release."),
           "supersedes": "the estimated windows in PICTURE-GRAMMAR-V1.md",
           "shorts": report}
    if a.write:
        p = BASE / "BEAT-TIMING-V1.json"
        if p.exists():
            raise SystemExit("BEAT-TIMING-V1.json already exists")
        p.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
