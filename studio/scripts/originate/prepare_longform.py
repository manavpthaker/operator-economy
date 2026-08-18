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
import shutil
from pathlib import Path

try:
    from footage_manifest import (resolve_entry, resolve_local_path,
                                  validate_manifest)
except ImportError:
    from .footage_manifest import (resolve_entry, resolve_local_path,
                                   validate_manifest)

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
    storyboard_path = base / "storyboard.json"
    use_storyboard = storyboard_path.exists()
    footage_path = base / "footage_manifest.json"
    footage = load_json(footage_path) if footage_path.exists() else None
    if footage is not None:
        footage_errors = validate_manifest(footage, base, require_files=True)
        if footage_errors:
            raise SystemExit("FOOTAGE GATE: BLOCKED\n" +
                             "\n".join(f"- {error}" for error in footage_errors))

    public_footage = ROOT / "remotion" / "public" / "footage" / script["slug"]
    staged_footage: dict[str, dict] = {}

    def render_asset(section_id: str, beat: int, asset: dict,
                     screen_id: str | None = None, force_broll: bool = False) -> dict:
        """Resolve an approved manifest entry and stage it for Remotion."""
        if asset.get("type") != "broll" and not force_broll:
            return asset
        asset = {**asset, "type": "broll"}
        if footage is None:
            raise SystemExit(
                f"FOOTAGE GATE: BLOCKED\n- {section_id} beat {beat} requests b-roll "
                f"but {footage_path.name} does not exist\n"
                f"  run: python scripts/originate/footage_manifest.py init {script_path}")
        entry = resolve_entry(footage, section_id, beat, asset, screen_id)
        if entry is None:
            raise SystemExit(
                f"FOOTAGE GATE: BLOCKED\n- {section_id} beat {beat} has no matching "
                "footage manifest entry")
        source = resolve_local_path(entry, base)
        assert source is not None  # validate_manifest proved it exists
        public_footage.mkdir(parents=True, exist_ok=True)
        staged = public_footage / f"{entry['id']}{source.suffix.lower()}"
        shutil.copy2(source, staged)
        resolved = {
            **asset,
            "manifest_id": entry["id"],
            "footage_role": entry["role"],
            "source_video": f"footage/{script['slug']}/{staged.name}",
            "source_in": float(entry.get("source_in", 0)),
            "source_out": entry.get("source_out"),
            "crop": entry.get("crop", "cover"),
            "focal_position": entry.get("focal_point", "center"),
            "caption": entry.get("caption") or asset.get("caption"),
            "preview_eligible": bool(entry.get("preview_eligible")),
        }
        staged_footage[entry["id"]] = {**entry, "asset": resolved}
        return resolved

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
                # `screens[]` is the preferred renderer. Do not require or
                # stage a legacy beat asset that the final storyboard removed.
                "asset": (asset_index.get((s["id"], b["beat"]),
                                          {"type": "slide", "title": "", "bullets": []})
                          if use_storyboard else render_asset(
                              s["id"], b["beat"],
                              asset_index.get((s["id"], b["beat"]),
                                              {"type": "slide", "title": "", "bullets": []}))),
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
    screens_out: list[dict] | None = None
    if storyboard_path.exists():
        storyboard = load_json(storyboard_path)
        # Index beat time-range lookups by (section, beat) → (start, end).
        beat_time = {
            (s["id"], b["beat"]): (b["start"], b["end"])
            for s in sections_out for b in s["beats"]
        }
        screens_out = []
        # Sheet-line ordinals run PER SECTION ACROSS screens (fix
        # 2026-07-03: every sheet screen restarted at "01", so the
        # section's list never appeared to advance). The renderer shows
        # reveal.ordinal instead of its local index.
        sheet_ordinal: dict[str, int] = {}
        for screen in storyboard.get("screens", []):
            sid = screen["section"]
            reveals_out = []
            for r in screen.get("reveals", []):
                ordinal = None
                if screen["layout"] == "sheet":
                    sheet_ordinal[sid] = sheet_ordinal.get(sid, 0) + 1
                    ordinal = sheet_ordinal[sid]
                planned_asset = asset_index.get((sid, r["beat"]), {})
                # The final storyboard owns layout. A stale plan_assets b-roll
                # hint must not resurrect footage after a screen was hand-tuned
                # into an artifact/chart/etc.
                asset = (render_asset(
                    sid, r["beat"], planned_asset,
                    screen_id=screen["id"], force_broll=True)
                    if screen["layout"] == "broll" else planned_asset)
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
                    "ordinal": ordinal,
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
                "preview_role": screen.get("preview_role") or screen.get("footage_role"),
                "narrative_state": screen.get("narrative_state"),
                "score_state": screen.get("score_state"),
                "footage_role": screen.get("footage_role"),
                "camera": screen.get("camera"),
                "preview_eligible": bool(screen.get("preview_eligible")),
                "visual_intent": screen.get("visual_intent"),
                "search_query": screen.get("search_query"),
                "query_variants": screen.get("query_variants", []),
                "visual_exclusions": screen.get("visual_exclusions", []),
                "heading": screen.get("heading"),
                "start": screen["start"],
                "end": screen["end"],
                "reveals": reveals_out,
                "figure": screen.get("figure"),
                "source": screen.get("source"),
                # Pacing pass (pace_storyboard.py): timed visual events
                # the renderer performs inside the screen — fragment
                # staging, item staging, highlight pulses, focus cycles.
                "events": screen.get("events", []),
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


    # Rev D preview-proof gate. A manifest opts the episode into the footage
    # contract; both storyboard and legacy beat render paths are supported.
    if footage and footage.get("enforce_preview_gate", True):
        if screens_out is not None:
            opening_ids = {
                r["asset"].get("manifest_id")
                for screen in screens_out if screen.get("start", 999) < 30
                for r in screen.get("reveals", [])
                if r.get("asset", {}).get("type") == "broll"
            }
        else:
            opening_ids = {
                b["asset"].get("manifest_id")
                for section in sections_out
                for b in section.get("beats", []) if b.get("start", 999) < 30
                if b.get("asset", {}).get("type") == "broll"
            }
        opening_roles = {
            staged_footage[mid]["role"] for mid in opening_ids
            if mid in staged_footage and staged_footage[mid].get("preview_eligible")
        }
        if screens_out is not None:
            for screen in screens_out:
                if screen.get("start", 999) >= 30:
                    continue
                if screen.get("preview_role") in {"market_force", "proof", "process", "outcome"}:
                    opening_roles.add(screen["preview_role"])
                elif screen.get("layout") in {"chart", "proof_card", "artifact", "source_card"}:
                    opening_roles.add("proof")
                elif screen.get("layout") in {"screen_rec", "schematic"}:
                    opening_roles.add("process")
        missing_groups = []
        if "human_context" not in opening_roles:
            missing_groups.append("human_context")
        if not opening_roles.intersection({"market_force", "proof"}):
            missing_groups.append("market_force|proof")
        if not opening_roles.intersection({"process", "outcome"}):
            missing_groups.append("process|outcome")
        if missing_groups:
            raise SystemExit(
                "FOOTAGE PREVIEW GATE: BLOCKED\n"
                f"- first 30 seconds lacks preview-eligible: {', '.join(missing_groups)}\n"
                f"- observed roles: {', '.join(sorted(opening_roles)) or 'none'}")

    total = timeline["total_seconds"]

    # Bookends (2026-07-03): brand sting + title/thesis before the hook,
    # URL/CTA card after the CTA section. The composition offsets all
    # content by the intro; total_frames covers intro + episode + outro.
    bk_cfg = r_cfg.get("bookends", {})
    channel = config.get("channel", {})
    bookends = {
        "brand_seconds": bk_cfg.get("brand_seconds", 1.8),
        "title_seconds": bk_cfg.get("title_seconds", 3.2),
        "brand_at_seconds": bk_cfg.get("brand_at_seconds", 0.0),
        "overlay_on_content": bk_cfg.get("overlay_on_content", False),
        "sting_audio": bk_cfg.get("sting_audio"),
        "outro_seconds": bk_cfg.get("outro_seconds", 6.0),
        # J/L-cuts (2026-07-03): VO runs under the title card and under
        # the outro card, so the bookends feel like edits, not slides.
        "j_cut_seconds": bk_cfg.get("j_cut_seconds", bk_cfg.get("title_seconds", 3.2)),
        "l_cut_seconds": bk_cfg.get("l_cut_seconds", 2.5),
        "title": script.get("working_title", ""),
        "thesis": script.get("topic", ""),
        "episode_no": next(
            (e.get("number") for e in
             load_json(ROOT.parent / "site" / "data" / "episodes.json").get("episodes", [])
             if e.get("slug") == script["slug"]),
            None),  # filled from site/data/episodes.json
        "brand": {
            "name": channel.get("name", "The Operator Economy"),
            "tagline": channel.get("tagline", "Build. Own. Operate."),
            "domain": channel.get("domain", "theoperatoreconomy.com"),
        },
        "ctas": bk_cfg.get("outro_ctas", []),
    }

    # Cold open (2026-08-12). The brand sting opens on the episode's OWN
    # thumbnail ground and dissolves it into the navy over its existing 1.8
    # seconds — no extra time before the hook, which is the constraint the
    # sting was built around in the first place.
    #
    # Why this is here and not left to the editor: rendering four frames of a
    # finished episode beside its thumbnail showed the two surfaces share
    # nothing. Photograph against vector, Supreme 800 at 196px against Boska
    # serif at ~48px, dense-to-the-edges against 70-85% empty, hands in frame
    # against no human anywhere. Somebody clicks a tactile overhead photograph
    # and lands on a silent navy slide, which is the packaging equivalent of an
    # ad that does not match its landing page.
    #
    # The file has to be the SAME one the thumbnail composites over, not a
    # lookalike, so it is read from the thumbnail props rather than guessed.
    # An episode can carry several thumbnail props — one per archetype tested,
    # plus whichever one was actually chosen. The chosen one is marked
    # `"_chosen": true` and wins, because otherwise this silently opens the
    # video on a REJECTED candidate: EP001's thumbnail is a tower in a palm and
    # this list would have opened it on a hotel-desk flat-lay. That is not a
    # lookalike, which J1 already forbids — it is a different subject, and worse
    # than having no cold open at all.
    # A storyboard older than the script is a correctness bug, not a warning.
    # EP006 rendered 12 minutes of video carrying "The old idea was a better
    # booking" on screen — wording removed from the script hours earlier — because
    # storyboard.py runs in `continue` and nothing re-runs it in `render`. Silent
    # staleness is worse than a stop.
    sb_p = base / "storyboard.json"
    if sb_p.exists() and sb_p.stat().st_mtime < script_path.stat().st_mtime:
        raise SystemExit(
            f"storyboard.json is older than script.json — the render would put "
            f"retired wording on screen.\n"
            f"  re-run:  storyboard.py {script_path}\n"
            f"  then:    pace_storyboard.py {script_path}")

    rd = base / "render_data"
    chosen = [f for f in sorted(rd.glob("thumb-*.json"))
              if load_json(f).get("_chosen") is True]
    order = chosen + [rd / c for c in
                      ("thumb-flatlay.json", "thumbnail-flatlay.json", "thumbnail-a8.json")]
    for tp in order:
        if not tp.exists():
            continue
        bg = load_json(tp).get("bgImage")
        if bg and (ROOT / "remotion" / "public" / bg).exists():
            bookends["cold_open_image"] = bg
            if tp in chosen:
                print(f"  cold open ← {tp.name} (chosen thumbnail)")
            else:
                print(f"  note: no thumbnail marked _chosen; falling back to "
                      f"{tp.name}. The video will open on a candidate that may "
                      f"not be the one shipped.")
            break
    else:
        print("  note: no thumbnail ground found; brand sting opens on navy. "
              "Run generate_scene.py to give this episode a cold open.")
    # Rev D overlays identity on story motion after the cold open has begun.
    # Legacy episodes still prepend their bookends.
    intro_s = (0.0 if bookends["overlay_on_content"] else
               bookends["brand_seconds"] + bookends["title_seconds"])
    overlap_s = bookends["j_cut_seconds"] + bookends["l_cut_seconds"]

    render_data = {
        "slug": script["slug"],
        "title": script["working_title"],
        "duration_seconds": total,
        "fps": fps,
        "total_frames": int((intro_s + total + bookends["outro_seconds"] - overlap_s) * fps) + 1,
        "bookends": bookends,
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

    # Sync VO into remotion/public — Remotion's staticFile() reads from
    # public/, and a stale manual copy there caused a full-episode
    # audio/caption desync (2026-07-03: old NY-A1 audio rendered under
    # LW3 captions). prepare_longform now owns the copy so it can never
    # go stale: whatever timeline.json points at is what renders.
    pub_vo = ROOT / "remotion" / "public" / "vo"
    pub_vo.mkdir(parents=True, exist_ok=True)
    for stale in pub_vo.glob("*.mp3"):
        stale.unlink()
    for t in timeline["sections"]:
        shutil.copy2(base / "vo" / t["audio"], pub_vo / t["audio"])
    print(f"✓ Synced {len(timeline['sections'])} VO files → remotion/public/vo/")


if __name__ == "__main__":
    main()
