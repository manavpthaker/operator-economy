# The Thumbnail Rubric

**Every episode thumbnail passes this before the API push.** Condensed July 6, 2026 from the r/YouTubeThumbnailHub checklist (the community-maintained CTR guide) + OE adaptations. Companion to `docs/post-rubric.md`; referenced from `publishing-flow.md` Phase 1.

## Theory before design (80/20)

People click videos they want to watch, not pretty images. Before opening the composition, answer in one line each: what grabs **attention** (priority 1), what speaks to the viewer's **interest** (priority 2), what creates the **curiosity gap** (priority 3). For OE the standing answer: attention = an expressive human face in a real small business; interest = "someone like me, doing this"; curiosity = the specific dollar figure that doesn't explain itself.

**The OE thumbnail concept: the install moment.** Each episode's thumbnail shows THAT week's business being delivered to a real customer — barbershop, restaurant, clinic, whatever the episode covers. The viewer's stand-in is the hero; the corporate giant stays inside the video as evidence. This varies naturally week to week (different business, different scene), which sidesteps the "identical PowerPoint template" trap while the warm-photo + gold-number style stays recognizable.

## Hard rules (break only with a written reason)

1. **≤3 elements.** Scene-with-faces (1) + one text block (2). That's it. No kicker, no OE mark, no episode number — the channel name renders next to the title anyway; branding on the thumbnail is wasted curiosity space.
2. **≤4 words**, LARGE, thick/bold **sans** (Supreme 800 — the brand sans; serif display fails the thin-stroke test at 168px-wide tiles). Gold or paper on the dark scrim. Never duplicate the title's words.
3. **Faces**: real scenes with expressive faces (generic/AI people — Manav stays off camera; the channel is nameless, not humanless). Emotion must be *earned by the scene*, eyes near the upper-third line, close crop.
4. **No man's land**: nothing important in the lower-right (duration stamp) or hugging the right edge. Text block anchors bottom-LEFT.
5. **Contrast**: scrim/darken behind text, subject visually separated from background (depth of field or masking), bright-warm subject on dark ground — pops against YouTube's white UI.
6. **Shrink test is the ship gate**: judge at 320px AND 168px. If the text or the emotion doesn't read, revise. Second opinion blink-test when possible: "what do you think this video is about?"
7. **Good clickbait only**: the scene must literally happen in the episode's playbook. Mismatched expectations = abandonment = suppressed recommendations.
8. **1280×720 exactly**, high-res source imagery, no hard border frames, no emojis.

## Process rules

- **Thumbnail concept locks at script gate** (before production, MrBeast rule): the episode is written to pay off the thumbnail+title pair, not the reverse. The concept line lives in script.json (`thumbnail_concepts`).
- Thumbnail, title, and intro hook each carry DIFFERENT information: thumbnail = the visual scene + viewer's number; title = the claim; intro = the evidence. No repetition across the three.
- Two candidates per episode minimum; compare side-by-side against competitor thumbnails for the same search terms.
- Day-7 CTR check by traffic source; Test & Compare A/B when the channel unlocks it. Quarterly stale-thumbnail revisit on the back catalog.

## Symbols (allowed, sparingly)

Arrows/circles to direct the eye at ONE thing; red X / green ✓ only for genuine before/after episodes. Punctuation as emotion is fine. No emojis ever.

## Enforcement (added 2026-08-10)

Everything above is design guidance and was, until now, self-certified. That failed. EP005 shipped
with a note asserting "Rule 6 ✓ reads at browse-strip size" on a file that was 2272x1198 (not
16:9), 94% fully transparent, and whose secondary text resolved to roughly 2px of cap height at
browse width. A note cannot be the gate for a rule that a machine can measure.

Two checks now run, and they cover different things:

| Check | Enforces | Run by |
|---|---|---|
| `prepare_thumbnail.py` | the **words**: rule 2 (≤4 words, no title overlap), rule 1 (no kicker/mark/number), and that a scene image exists at all | `originate.py render` |
| `check_thumbnail.py` | the **pixels**: no alpha channel, 16:9 within 1%, ≥1280x720, and that content survives the shrink to 120px on both a white and a black ground | manual today; wire into `launch.py --go` |

```bash
.venv/bin/python studio/scripts/originate/check_thumbnail.py <image.png>
# exit 0 = pass, 1 = at least one FAIL
```

**The alpha check is not pedantry.** YouTube flattens uploads to JPEG, so a transparent PNG does
not ship the design you reviewed; transparent regions composite to black. EP005's thumbnail has no
background in the file at all.

**What is deliberately not checked.** Faces, composition, the curiosity gap, and whether the scene
actually happens in the episode. Those need eyes, and the mechanical layer is a floor rather than a
ceiling: EP001's thumbnail is a 9-word serif title card carrying a kicker and an episode number,
violating rules 1, 2, 3, 5, and 6, and it passes every mechanical check cleanly. Passing the script
means the file is not broken. It does not mean the thumbnail is good.

**Waivers.** Rules 3 and 4 were both waived on EP005 in a note, silently, which is how a
figure-only composition with no ground reached upload. A waiver is a real decision and belongs in
the episode's `thumbnail-note.md` with a reason, and it should be read at Gate 3 rather than
discovered afterward. Two waivers on one thumbnail is a signal the concept is fighting the format.

**Generate inside the pipeline.** EP005's note records that the image was "generated externally."
Every mechanical defect above entered at exactly that step, and the same pattern produced the
launch-ledger defects when the episode was uploaded outside `launch.py`. Externally-produced
artifacts skip every guard that exists.
