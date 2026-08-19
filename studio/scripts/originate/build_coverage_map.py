"""Build transcript-aligned visual coverage and a planned asset manifest.

This is the first visual pass: coverage and sourcing intent only. It does not
select media, design final frames, arrange music, or mark coverage approved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path


def tc(seconds: float) -> str:
    minutes = int(seconds // 60)
    return f"{minutes:02d}:{seconds - minutes * 60:04.1f}"


def segment(words: list[dict], min_s: float = 3.0, target_s: float = 6.5,
            max_s: float = 10.0) -> list[list[dict]]:
    chunks, current = [], []
    for word in words:
        if current and word["section"] != current[-1]["section"]:
            chunks.append(current)
            current = []
        prospective = word["end"] - current[0]["start"] if current else 0
        if current and prospective > max_s and (
                current[-1]["end"] - current[0]["start"] >= min_s):
            chunks.append(current)
            current = []
        current.append(word)
        duration = current[-1]["end"] - current[0]["start"]
        sentence_end = bool(re.search(r"[.!?][\"']?$", word["word"]))
        if duration >= max_s or (duration >= target_s and sentence_end):
            chunks.append(current)
            current = []
        elif duration >= min_s and sentence_end:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    # A section-ending fragment can be shorter than three seconds. Move the
    # preceding words across the boundary until both contiguous beats clear
    # the minimum; never merge across sections or create an overlong beat.
    for index in range(1, len(chunks)):
        cur, prev = chunks[index], chunks[index - 1]
        if cur[0]["section"] != prev[0]["section"]:
            continue
        while cur[-1]["end"] - cur[0]["start"] < min_s and len(prev) > 1:
            candidate = prev[-1:]
            shorter = prev[:-1]
            if shorter[-1]["end"] - shorter[0]["start"] < min_s:
                break
            if cur[-1]["end"] - candidate[0]["start"] > max_s:
                break
            prev[:] = shorter
            cur[:0] = candidate
    return chunks


def classify(text: str, section: str) -> dict:
    low = text.lower()
    rules = [
        (("this is the operator economy",), "orient", "brand_ident", "process",
         "OE logo ident, then the one-line channel promise types on in two restrained lines.",
         "original_motion"),
        (("more than 60 percent", "ninety million bookings", "cloudbeds"), "prove",
         "source_document", "proof", "Cloudbeds report page with the exact finding highlighted; source label remains visible.",
         "source_capture"),
        (("$300 million", "$2.5 billion", "mews announced"), "prove", "headline_document",
         "proof", "Mews funding announcement and valuation headline, with the relevant figures isolated.",
         "source_capture"),
        (("$180", "$135,000", "$94,500", "$140,000", "twenty-room"), "explain",
         "custom_chart", "proof", "Build the hotel economics one assumption at a time; distinguish reported inputs from the estimate.",
         "original_graphic"),
        (("cancelled", "cancellations", "twice the rate"), "contrast", "comparison_chart",
         "proof", "Direct-versus-OTA cancellation comparison with restrained motion and a visible source footnote.",
         "original_graphic"),
        (("booking or expedia", "booking next time", "ota", "platform"), "contrast",
         "platform_visual", "market_force", "Booking and Expedia branded surfaces pull the guest journey back toward the intermediary; use logos only where editorially necessary.",
         "licensed_or_capture"),
        (("google profile", "search result", "search for the hotel", "profile current"),
         "explain", "interface_capture", "process", "Phone-sized Google hotel result: current profile, photography, offers, reviews, and direct destination.",
         "original_capture"),
        (("website", "booking page", "booking engine", "book a room", "direct path"),
         "explain", "interface_capture", "process", "Mobile direct-booking walkthrough showing rate, trust, policy, availability, and checkout friction.",
         "original_capture"),
        (("mews", "cloudbeds", "siteminder", "little hotelier", "twilio", "resend", "n8n"),
         "explain", "stack_diagram", "process", "Outcome stack: each named tool enters only beside the job it performs, never as a logo wall.",
         "original_graphic"),
        (("audit", "before picture", "baseline", "scorecard", "report one main outcome"),
         "explain", "document_template", "process", "Blueprint audit or monthly scorecard fills in on screen: baseline, change made, outcome, exceptions.",
         "original_document"),
        (("group project",), "humanize", "visual_metaphor", "process",
         "Dry group-project metaphor: disconnected owners pass Google, website, desk, and follow-up cards around with no accountable owner.",
         "original_motion"),
        (("menu price", "add-ons"), "explain", "visual_metaphor", "proof",
         "Commission appears as a menu price; loyalty and visibility add-ons increase the check.",
         "original_motion"),
        (("shakier rsvp",), "humanize", "visual_metaphor", "proof",
         "Reservation card changes from confirmed to tentative while the higher acquisition cost remains.",
         "original_motion"),
        (("matchmaker", "second date"), "humanize", "visual_metaphor", "market_force",
         "Matchmaker analogy: the hotel pays for the same introduction again even though the first stay already happened.",
         "original_motion"),
        (("fresh coat of paint", "door that doesn't open"), "humanize", "visual_metaphor",
         "process", "Beautiful hotel homepage becomes a freshly painted door whose booking handle still will not turn.",
         "original_motion"),
        (("power tool", "contractor"), "explain", "visual_metaphor", "process",
         "Software as neatly arranged power tools; the operator is the person who knows what to build and checks the work.",
         "original_motion"),
        (("junk drawer", "monthly billing"), "humanize", "visual_metaphor", "process",
         "Disconnected app subscriptions accumulate in a junk drawer while recurring charges tick upward.",
         "original_motion"),
        (("newsletter wearing a name tag",), "humanize", "visual_metaphor", "process",
         "Generic automated email receives a fake handwritten name tag; contrast it with one relevant hospitality message.",
         "original_motion"),
        (("flat tire look busy",), "humanize", "visual_metaphor", "proof",
         "Dashboard gauges animate energetically while the direct-booking tire remains visibly flat.",
         "original_motion"),
        (("summer is not your case study",), "humanize", "visual_metaphor", "proof",
         "Seasonal occupancy rises with summer weather while the operator's claimed contribution stays unproven.",
         "original_motion"),
        (("coqui coqui", "more than fifty people"), "humanize", "hospitality_footage",
         "human_context", "Warm, design-led tropical resort operations: guest arrival, property detail, staff coordination, and lived hospitality.",
         "licensed_footage"),
        (("front desk", "innkeeper", "hotel served the guest", "thank-you", "review request"),
         "humanize", "hospitality_footage", "human_context", "Specific independent-hotel human action matching the line; no masks, corporate lobby, passport paperwork, or generic desk work.",
         "licensed_footage"),
        (("return visit", "come back", "repeat business", "next booking"), "resolve",
         "hospitality_footage", "outcome", "Recognizable returning guest welcomed directly by a small-property host; warm but not staged luxury advertising.",
         "licensed_footage"),
        (("permission", "consent", "sensitive", "decide when not to send"), "explain",
         "process_diagram", "process", "Human-review gate: consent, relevance, sensitive content, approve or do not send.",
         "original_graphic"),
        (("subscribe", "blueprint"), "orient", "cta_card", "outcome",
         "Branded but restrained blueprint and subscribe card tied to the viewer's next action.",
         "original_motion"),
    ]
    for needles, purpose, asset_type, role, shot, route in rules:
        if any(needle in low for needle in needles):
            return {"purpose": purpose, "asset_type": asset_type, "role": role,
                    "shot": shot, "source_route": route}
    defaults = {
        "hook": ("humanize", "hospitality_footage", "human_context",
                 "Innkeeper and guest in a specific independent-property moment; preserve space for the cold-open graphic.", "licensed_footage"),
        "thesis": ("explain", "process_diagram", "process",
                   "Guest journey flows from discovery to direct return; reveal only the mechanism named in the narration.", "original_graphic"),
        "evidence": ("prove", "evidence_card", "proof",
                     "Source-led evidence card or calculation that makes the spoken claim inspectable rather than decorative.", "source_capture"),
        "stack": ("explain", "process_diagram", "process",
                  "Show the job, handoff, and accountable human before introducing any tool.", "original_graphic"),
        "playbook": ("explain", "checklist_motion", "process",
                     "Blueprint checklist advances one operator action at a time with a concrete hotel artifact beside it.", "original_document"),
        "economics": ("prove", "custom_chart", "proof",
                      "Economics or attribution graphic that separates known inputs, estimates, labor, and measured outcomes.", "original_graphic"),
        "cta": ("resolve", "outcome_card", "outcome",
                "Return to the host and guest relationship, then resolve into the blueprint and subscribe action.", "original_motion"),
    }
    purpose, asset_type, role, shot, route = defaults[section]
    return {"purpose": purpose, "asset_type": asset_type, "role": role,
            "shot": shot, "source_route": route}


def queries(asset_type: str, role: str, description: str) -> list[str]:
    if asset_type == "hospitality_footage":
        if role == "outcome":
            return [
                "returning couple warmly welcomed by independent inn host daylight no masks",
                "boutique hotel owner greeting repeat guests rustic property natural interaction",
                "small hotel host handing key to familiar guest warm candid 16:9",
            ]
        return [
            "independent innkeeper helping guests boutique hotel natural daylight no masks",
            "small rustic hotel host guest interaction candid hospitality 16:9",
            "boutique bed and breakfast owner welcoming travelers no corporate lobby no desk work",
        ]
    if asset_type == "platform_visual":
        return ["capture current Booking.com hotel listing and checkout", "capture current Expedia hotel search comparison", "licensed OTA press imagery with canonical source"]
    if asset_type in {"source_document", "headline_document"}:
        return ["capture canonical source page and highlighted claim", "archive source PDF page with title and date", "create citation card from verified source metadata"]
    return [description]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    args = ap.parse_args()
    base = args.script.parent
    script = json.loads(args.script.read_text())
    words = json.loads((base / "vo" / "words.json").read_text())
    timeline = json.loads((base / "vo" / "timeline.json").read_text())
    state = json.loads((base / "production_state.json").read_text())
    old_footage_path = base / "footage_manifest.json"
    old_entries = json.loads(old_footage_path.read_text()).get("entries", []) if old_footage_path.exists() else []
    beats, assets, asset_by_key = [], [], {}
    for index, chunk in enumerate(segment(words), 1):
        start, end = chunk[0]["start"], chunk[-1]["end"]
        text = " ".join(word["word"] for word in chunk)
        section = chunk[0]["section"]
        spec = classify(text, section)
        visual_id = f"V{index:03d}"
        candidates = [entry["id"] for entry in old_entries
                      if entry.get("section") == section and entry.get("role") == spec["role"]]
        # Reuse the same planned source or designed element where its editorial
        # job is genuinely identical. Section-scoped defaults remain distinct.
        asset_key = (section, spec["asset_type"], spec["shot"])
        asset_id = asset_by_key.get(asset_key)
        if not asset_id:
            asset_id = f"A{len(assets) + 1:03d}"
            asset_by_key[asset_key] = asset_id
            assets.append({
                "id": asset_id, "coverage_ids": [], "section": section,
                "role": spec["role"], "asset_type": spec["asset_type"],
                "description": spec["shot"], "source_route": spec["source_route"],
                "query_variants": queries(spec["asset_type"], spec["role"], spec["shot"]),
                "legacy_candidate_refs": candidates, "status": "planned",
                "provider": None, "asset_id": None, "page_url": None,
                "creator": None, "license": None, "license_checked_at": None,
                "downloaded_at": None, "local_path": None, "sha256": None,
                "faces_review": "pending" if spec["asset_type"] == "hospitality_footage" else "not_applicable",
                "synthetic": spec["source_route"] == "original_motion",
                "source_in": None, "source_out": None, "crop": "16:9 cover",
                "focal_point": "center", "review_notes": None,
            })
        next(asset for asset in assets if asset["id"] == asset_id)["coverage_ids"].append(visual_id)
        beats.append({
            "id": visual_id, "start": round(start, 3), "end": round(end, 3),
            "duration": round(end - start, 3), "timecode": f"{tc(start)}–{tc(end)}",
            "section": section, "narration": text,
            "visual_purpose": spec["purpose"], "asset_type": spec["asset_type"],
            "story_role": spec["role"], "intended_shot": spec["shot"],
            "asset_ids": [asset_id], "preview_eligible": start < 30,
        })
    payload = {
        "schema_version": "oe-coverage-v1", "episode": script["slug"],
        "script_revision": script.get("revision"), "script_sha256": state["script_sha256"],
        "vo_total_seconds": timeline["total_seconds"], "status": "draft_review",
        "target_visual_duration_seconds": "3-10", "beat_count": len(beats),
        "beats": beats,
    }
    manifest = {
        "schema_version": "oe-asset-plan-v1", "episode": script["slug"],
        "script_sha256": state["script_sha256"], "coverage_status": "draft_review",
        "created_at": str(date.today()), "entry_count": len(assets), "entries": assets,
    }
    (base / "coverage_map.json").write_text(json.dumps(payload, indent=2) + "\n")
    (base / "asset_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = [f"# Visual Coverage Review — {script['working_title']}", "",
             f"> `{script.get('revision')}` · {timeline['total_seconds']:.1f}s VO · {len(beats)} visual beats · draft, not approved", ""]
    last_section = None
    for beat in beats:
        if beat["section"] != last_section:
            lines += [f"## {beat['section'].title()}", ""]
            last_section = beat["section"]
        lines += [f"### {beat['id']} · {beat['timecode']} · {beat['visual_purpose']} / {beat['asset_type']}", "",
                  f"> {beat['narration']}", "", beat["intended_shot"], "",
                  f"Asset: `{beat['asset_ids'][0]}` · role: `{beat['story_role']}`", ""]
    (base / "COVERAGE-REVIEW.md").write_text("\n".join(lines) + "\n")
    digest = hashlib.sha256((base / "coverage_map.json").read_bytes()).hexdigest()
    print(f"coverage: {len(beats)} beats over {timeline['total_seconds']:.1f}s")
    print(f"assets: {len(assets)} planned; coverage sha256 {digest}")


if __name__ == "__main__":
    main()
