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
8. **3840×2160 master, 16:9** (see A7 — this supersedes the old "1280×720 exactly"), high-res source imagery, no hard border frames, no emojis.

## Process rules

- **Thumbnail concept locks at script gate** (before production, MrBeast rule): the episode is written to pay off the thumbnail+title pair, not the reverse. The concept line lives in script.json (`thumbnail_concepts`).
- Thumbnail, title, and intro hook each carry DIFFERENT information: thumbnail = the visual scene + viewer's number; title = the claim; intro = the evidence. No repetition across the three.
- Two candidates per episode minimum; compare side-by-side against competitor thumbnails for the same search terms.
- Day-7 CTR check by traffic source; Test & Compare A/B when the channel unlocks it. Quarterly stale-thumbnail revisit on the back catalog.

## Symbols (allowed, sparingly)

Arrows/circles to direct the eye at ONE thing; red X / green ✓ only for genuine before/after episodes. Punctuation as emotion is fine. No emojis ever.

## Amendments (2026-08-10) — these override the rules above where they conflict

Synthesised from two external data-video thumbnail rubrics evaluated 2026-08-10. Kept only what
both agreed on, or what one argued convincingly for this register. A third rubric built on a
"Triple Threat" of glowing brains, AI humanoid silhouettes, and futuristic corporate buildings was
rejected outright: that is the stock-AI imagery the other two score as a zero, and it violates the
hype ban in `brand/brand.md`.

**A1. One hero number. Not two.** *(new, and the most important)*

Every OE thumbnail to date puts two figures on the canvas and asks for a comparison: `$5.9B vs
$2K`, `$11B vs $500`, `850 vs 1`. A comparison costs time nobody spends at feed size. One figure
should own roughly 35 to 50% of the frame; a second number halves the impact of the first. Use the
`hero` variant in `ThumbnailComposition.tsx`. The `split`, `versus`, and `numbers` variants all
violate this by construction and should be treated as legacy.

**A2. The text interprets the number, it does not label it.** *(new)*

`73%` is weak; `COSTS FELL 73%` is strong. `$500` is weak; `$500 EVERY MONTH` is strong. OE's
existing labels are pure naming: `ACCENTURE`, `YOU`, `A MONTH`, `ELEVENLABS`. A bare label makes
the viewer supply the meaning. Interpretation hands it to them. Keep to two or three words so it
sets on one line; a wrapped label reads as two ideas.

**A3. Faces are optional here, and usually wrong.** *(supersedes rule 3)*

Rule 3 mandated real scenes with expressive faces. That is general-audience advice imported from a
creator checklist, and it fights the register the whole brand runs on. For analytical business
video, an expressive face reads as hype and costs credibility on an episode that hedges its weak
sources aloud. Use a human element when it genuinely interprets the number. Do not add one for
attention. This also removes the scene-sourcing dependency that has left every episode either
hand-made or falling back to a title card.

**A4. Title and thumbnail split the work.** *(sharpens rule under Process)*

Title carries the subject and mechanism; thumbnail carries the consequence, contrast, or evidence.
If the thumbnail restates a number already in the title, it has spent the frame on nothing. EP003's
first draft failed exactly here: title "The 5 Billion Dollar Business That Sounds Boring", thumbnail
`$5B` and `Dull`.

**A5. Variants test different hypotheses.** *(replaces "two candidates minimum")*

Three variants, each changing one major variable: (A) hero metric, (B) before/after transformation,
(C) decision or tension. Three near-identical files teach nothing.

**A6. One shrink-test number.** *(resolves rule 6)*

The sources give four different sizes (168x94, 160x90, 10% zoom, 5%). Standardise on **120px wide**,
which is what `check_thumbnail.py` measures, so the doc and the checker agree.

**One correction to our own numbers.** Both sources warn against a universal CTR pass/fail target
and recommend comparing against similar videos and traffic sources on the same channel. The "4% is
healthy" figure repeated across our docs comes from `growth-strategy.md`, not from any external
benchmark. EP003's 0.0% on 142 impressions is bad on any reading, but 4% should be treated as an
internal reference point rather than a threshold.

## Amendment A7 (2026-08-11) — the spec, verified at source

The previous "unverified, do not enforce yet" note is resolved. Read from YouTube's Help Center,
[Add custom thumbnails on YouTube](https://support.google.com/youtube/answer/72431), on 2026-08-11.
Quoted, because this doc has twice recorded a spec that turned out to be someone's blog post:

> "Have a resolution of 3840 x 2160 pixels (with minimum width of 640 pixels). Be uploaded in image
> formats such as JPG, GIF, or PNG. Remain under MB limits. Limits depend on the device you're using
> to upload your thumbnail: Mobile: 2 MB for video thumbnails or 10 MB for podcasts. Desktop: 50MB
> for both video thumbnails and podcast thumbnails. Try to use a 16:9 aspect ratio... For Shorts or
> Shorts ads, upload a thumbnail with an aspect ratio of 9:16 (2160 x 3840 pixels resolution)."

So: **master at 3840×2160**, 16:9, JPG or PNG, under 50MB uploading from desktop. The three external
rubrics that claimed this were right, and rule 8's `1280×720 exactly` was a decade-old community
convention we had been treating as a platform requirement.

**Our floor stays 1280×720 anyway, for a different and now-sourced reason.** YouTube's stated
minimum is 640px wide, but
[A/B test titles & thumbnails](https://support.google.com/youtube/answer/16391400) states: "If the
resolution of any thumbnail is lower than 720p (1280 x 720), all experiment thumbnails will be
downscaled to 480p (854 x 480)." A sub-720p file silently degrades every variant in a test, so 1280
is a hard floor and 3840 is the target. `check_thumbnail.py` enforces the floor and warns below the
target.

**A/B testing mechanics, also verified** — these change how the test in the Process rules should be
run, so they are recorded rather than left to memory:

- Up to **3 variants**; title-only, thumbnail-only, or title+thumbnail.
- **The winner is the variant with the highest watch time, not the highest CTR.** This is decisive
  for us: it means the test rewards packaging that attracts the right viewer, and a thumbnail that
  wins clicks while losing retention loses the test. It is the same standard the register is already
  built for.
- No clear winner → **the first variant uploaded is kept**. Order the upload deliberately.
- A control group is held out and excluded from the calculation. Tests take days to two weeks.
- Desktop Studio only, needs advanced features. **Shorts cannot be A/B tested.**
- "Testing titles and thumbnails that are too similar to each other can cause tests to run for
  longer" — which is A5's point (three variants must test different hypotheses), now with a
  mechanical reason attached.

**Still unverified, still not enforced.** The niche CTR bands quoted in craft research (gaming 8.5%,
education 4.5%, finance 4–9%) come from vendor benchmark studies, not from YouTube. The only
platform-official figure is that half of all channels sit between **2% and 10%** impressions CTR.
Browse and Suggested run materially lower than Search on the same video, so an explainer channel
sitting at 3–4% on browse is not obviously broken. Treat all of these as reference points, never as
gates.

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
