"""
Originate Step 4: Merge script + VO timing + assets + brand into
render data for the Remotion Blueprint composition (16:9 long-form).

Beat→time mapping: each section's beats are assigned time ranges by
matching beat vo_text word counts against the section's word timeline
(same word shape as the shorts pipeline).

Usage:
    python scripts/originate/prepare_longform.py originate/<slug>/script.json

Output:
    originate/<slug>/render_data/blueprint.json
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def load_json(path):
    with open(path) as f:
        return json.load(f)


def group_words(words: list[dict], per_group: int, highlights: set[str]) -> list[dict]:
    """Group words into caption groups (same shape the shorts renderer uses)."""
    groups = []
    for i in range(0, len(words), per_group):
        chunk = words[i:i + per_group]
        groups.append({
            "text": " ".join(w["word"] for w in chunk),
            "words": [{
                "word": w["word"],
                "start": w["start"],
                "end": w["end"],
                "highlight": w["word"].strip(".,!?").lower() in highlights,
            } for w in chunk],
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
        })
    # NOTE: groups deliberately keep their natural word-range windows.
    # Bridging inter-group gaps is the renderer's job (Captions.tsx holds a
    # group up to HOLD_MAX_S past its end, then fades). Data-level tiling
    # (tried 2026-07-03) made captions linger through every VO pause —
    # the renderer's capped hold is the correct layer for this.
    return groups


def main():
    parser = argparse.ArgumentParser(description="Prepare long-form render data")
    parser.add_argument("script", help="Path to script.json")
    parser.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = parser.parse_args()

    script_path = Path(args.script)
    base = script_path.parent
    script = load_json(script_path)
    config = load_json(args.config)
    brand = load_json(ROOT / "config" / "brand.json")
    words = load_json(base / "vo" / "words.json")
    timeline = load_json(base / "vo" / "timeline.json")
    assets = load_json(base / "assets.json")

    r_cfg = config["render"]
    fps = r_cfg["fps"]

    # Highlight vocabulary from all beats
    highlights = set()
    for s in script["sections"]:
        for b in s.get("beats", []):
            for h in b.get("highlight_words", []):
                for token in h.lower().split():
                    highlights.add(token.strip(".,!?"))

    # Map beats to time ranges by walking each section's words
    asset_index = {(s["id"], a["beat"]): a["spec"]
                   for s in assets["sections"] for a in s["assets"]}
    sections_out = []
    for s in script["sections"]:
        sec_words = [w for w in words if w["section"] == s["id"]]
        sec_meta = next((t for t in timeline["sections"] if t["section"] == s["id"]), None)
        if not sec_words or not sec_meta:
            continue
        total_beat_words = sum(len(b["vo_text"].split()) for b in s["beats"]) or 1
        beats_out, cursor = [], 0
        for b in s["beats"]:
            n = round(len(b["vo_text"].split()) / total_beat_words * len(sec_words))
            n = max(1, n)
            chunk = sec_words[cursor:cursor + n] or sec_words[-1:]
            cursor += n
            beats_out.append({
                "beat": b["beat"],
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"],
                "asset": asset_index.get((s["id"], b["beat"]),
                                         {"type": "slide", "title": "", "bullets": []}),
            })
        # TILE beats: each asset holds until the next beat starts; first beat
        # starts at section start, last holds to section end. Word-range
        # windows leave gaps (inter-sentence pauses) that render as blank
        # background (validated on pilot render, 2026-07-03).
        for bo, nxt in zip(beats_out, beats_out[1:]):
            bo["end"] = nxt["start"]
        if beats_out:
            beats_out[0]["start"] = sec_meta["start"]
            beats_out[-1]["end"] = sec_meta["start"] + sec_meta["duration"]
        sections_out.append({
            "id": s["id"],
            "start": sec_meta["start"],
            "duration": sec_meta["duration"],
            "audio": f"vo/{sec_meta['audio']}",
            "beats": beats_out,
        })

    # If storyboard.py has run, tuck the screens[] plan into render_data
    # so BlueprintComposition can prefer it over the run-grouping shim.
    # We reconcile each screen's beat numbers against the asset_index so
    # each reveal carries the plan_assets-authoritative title and body
    # (not the placeholder titles storyboard.py derived from asset_hint).
    storyboard_path = base / "storyboard.json"
    screens_out: list[dict] | None = None
    if storyboard_path.exists():
        storyboard = load_json(storyboard_path)
        # Index beat time-range lookups by (section, beat) → (start, end).
        beat_time = {
            (s["id"], b["beat"]): (b["start"], b["end"])
            for s in sections_out for b in s["beats"]
        }
        screens_out = []
        for screen in storyboard.get("screens", []):
            sid = screen["section"]
            reveals_out = []
            for r in screen.get("reveals", []):
                asset = asset_index.get((sid, r["beat"]), {})
                rng = beat_time.get((sid, r["beat"]))
                # Prefer explicit reveal timings/titles from the
                # storyboard (Manav's hand-tune) over the section-level
                # word-count fallback. This lets a hand-tuned quote card
                # OVERRIDE the underlying beat's plan_assets title.
                sb_title = r.get("title")
                sb_body = r.get("body")
                sb_at = r.get("at")
                sb_end = r.get("end")
                reveals_out.append({
                    "beat": r["beat"],
                    "at": sb_at if sb_at is not None else (rng[0] if rng else None),
                    "end": sb_end if sb_end is not None else (rng[1] if rng else None),
                    "title": sb_title or asset.get("title") or "",
                    "body": sb_body or (" · ".join(asset["bullets"]) if asset.get("bullets") else ""),
                    "asset": asset,
                    "tags": r.get("tags", []),
                    "word_anchor": r.get("word_anchor"),
                })
            screens_out.append({
                "id": screen["id"],
                "section": sid,
                "layout": screen["layout"],
                "heading": screen.get("heading"),
                "start": screen["start"],
                "end": screen["end"],
                "reveals": reveals_out,
                "figure": screen.get("figure"),
                "source": screen.get("source"),
                # SFX + music cues authored by the storyboard.
                "sfx": screen.get("sfx", []),
                "music": screen.get("music", {"intensity": "calm", "duck_db": -16}),
                # Hand-tuned custom props (quote text, ladder steps,
                # offer card fields, etc.). Composition prefers these
                # over derived fields when both are present.
                "custom": screen.get("custom"),
                # The audio path per section, so the composition can
                # sequence Audio without walking `sections`.
                "audio": next((s["audio"] for s in sections_out if s["id"] == sid), None),
            })

    total = timeline["total_seconds"]
    render_data = {
        "slug": script["slug"],
        "title": script["working_title"],
        "duration_seconds": total,
        "fps": fps,
        "total_frames": int(total * fps) + 1,
        "resolution": r_cfg["resolution"],
        "sections": sections_out,
        "captions": {
            "groups": group_words(words, r_cfg["words_per_group"], highlights),
            "style": r_cfg["caption_style"],
            "words_per_group": r_cfg["words_per_group"],
        },
        "brand": brand,
    }
    if screens_out is not None:
        render_data["screens"] = screens_out

    out_dir = base / "render_data"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "blueprint.json"
    with open(out, "w") as f:
        json.dump(render_data, f, indent=2)
    print(f"✓ Render data → {out} ({total:.0f}s, {len(sections_out)} sections)")


if __name__ == "__main__":
    main()
