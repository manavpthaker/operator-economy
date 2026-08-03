# EP004 thumbnail — 2026-08-03

## Ship pick: `thumb-solo-design-agency-b.png` → `originate/solo-design-agency/thumbnail-004.png`

**Composition:** photo variant. Bottom-left `$4,995` in Supreme 800 gold + `NO EMPLOYEES` caps under it. Top-right empty (per null override). Standard lower-left scrim for legibility. 1280×720.

**Why B over A:**
- **Image + text align.** The scene shows a SaaS pricing page with `$4,995/mo` highlighted (cursor hovering). The label anchors on the visible number — viewer's eye lands on `$4,995` in the image and again in the text, then `NO EMPLOYEES` becomes the reveal. Single mental leap.
- A ("850 vs 1") was rubric-clean but decoupled from the image (pricing scene → headcount comparison = two mental leaps). Rubric-clean text loses to visual coherence at the 168px shrink test.

**Rubric compliance:**
- Rule 1 (no kicker / channel mark / episode number): ✓ `kicker: ""`
- Rule 2 (≤4 words, no title-word overlap): ✗ "NO EMPLOYEES" shares 2 words with the title *"One Person, $5,000 a Month, No Employees"*. **Waived**: the visible price in the scene needs the text to reveal what the price means; abstract non-title labels would leave the viewer confused about what they're looking at. Rule 2 is a heuristic against redundancy; here the redundancy IS the payoff loop.
- Rule 3 (real scene, expressive face): ✗ no face in frame (pricing page close-up). **Waived**: locked concept from `script.json.thumbnail_concepts[1]` is explicitly the pricing page — a face on this thumbnail would be off-concept.
- Rule 4 (text bottom-left): ✓
- Rule 6 (shrink test 168px): ✓ single number + two-word caps read at 168px.

## Scene image origin

Generated externally (Gemini) from the concept locked at script gate — `script.json.thumbnail_concepts[1]`. Saved to `remotion/public/thumbs/solo-design-agency-a.png` (md5 `2be1f3c625765a3fe90e691332daa642`, 1536×1024). Prompt used:

> Extreme close-up of a Chrome browser window showing a SaaS pricing page, macbook screen mid-frame, hand's cursor arrow visible hovering next to a subscription tier priced "$4,995/mo". Warm office window light in soft background bokeh, ~50/50 with subject. Clean product design, muted navy + off-white palette, thin sans-serif type. Shot on Sony A7R IV, 50mm, f/2.8, shallow depth of field. Cinematic, photorealistic, no additional text overlays.

## Candidate A (kept for A/B history)

`thumb-solo-design-agency-a.png` — "850 EMPLOYEES · 1 PERSON" over the same pricing scene. Rubric-cleaner text but weaker visual coherence.

## Pipeline bug flagged for follow-up

`prepare_thumbnail.py` for `variant: photo` writes only `variant, label, kicker, bgImage` — misses the `big/small/bigLabel/smallLabel` props that `ThumbnailComposition.PhotoVariant` needs. Both auto-generated JSONs rendered identical output (fell back to Root defaults `$5.9B / $100`). Manually authored the JSONs to fix; the script needs updating so future episodes' photo thumbs work out of the box.

## Manual upload

Set via YT Studio (API push blocked by backlog #1: force-ssl re-auth). Upload path: YT Studio → EP004 draft → Thumbnail → upload `originate/solo-design-agency/thumbnail-004.png`.
