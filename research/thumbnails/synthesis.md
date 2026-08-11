# Thumbnail research synthesis (2026-08-11)

Two independent bodies of evidence landed the same day and they do not fully agree. Same drill as
`research/comp-synthesis.md`: convergence, conflict, what changes.

**Source A — craft report** (`../reports/thumbnail-craft-report-2026-08.md`). External research on
2026 specs, CTR strategy, and workflow for data/motion-graphics channels. Primary-sourced on
platform mechanics; explicit that most of its design guidance is "conventional wisdom and creator
anecdote, not controlled studies," and it flags its own unverifiable CTR-lift numbers.

**Source B — comp-set measurement** (`findings.md`). First-party: 221 videos, 8 comp channels,
banded within channel. Titles and performance only; the images are unread.

## Verified at source, so no longer anyone's opinion

I checked Source A's mechanical claims against YouTube's Help Center directly rather than taking a
third report's word for it — this doc has twice recorded a spec that turned out to be a blog post.
**Every mechanically-checkable claim in the craft report held up.** Verified 2026-08-11:

- **3840×2160 recommended, minimum width 640, JPG/GIF/PNG, 16:9. Mobile 2MB, desktop 50MB.** Shorts
  9:16 at 2160×3840. ([answer/72431](https://support.google.com/youtube/answer/72431))
- **A/B test winner is decided by highest watch time, not CTR.** Up to 3 variants; no clear winner
  keeps the first uploaded; control group held out; days to two weeks; desktop only; Shorts
  ineligible. ([answer/16391400](https://support.google.com/youtube/answer/16391400))
- **Sub-720p poisons a test:** "If the resolution of any thumbnail is lower than 720p (1280 x 720),
  all experiment thumbnails will be downscaled to 480p."

That accuracy record raises confidence in the report's unverified sections, but does not settle
them — the design claims are a different kind of claim, and the report says so itself.

Landed in `docs/thumbnail-rubric.md` amendment A7 and in `check_thumbnail.py`.

## Where A and B converge (treat as settled)

**1. Faces are not required for this register.** A says data channels don't need a shocked face and
names faceless explainer channels at scale; B's comp set is dominated by them. This independently
re-confirms our amendment A3, which had already overturned rule 3 on register grounds alone.

**2. Simplify ruthlessly; one focal element.** A's strongest primary voice (PolyMatter) teaches
"as simple as possible… as scalable as possible," names too-much-text and fear-of-empty-space as
top mistakes, and argues against literal charts. B doesn't contradict this and the 120px shrink
test already encodes it.

**3. Thumbnail must not restate the title.** Both. Already rule 2 and amendment A4.

**4. CTR is the wrong optimisation target.** A: YouTube penalises high-CTR/low-retention packaging,
and Test & Compare deliberately optimises watch time. B: nothing in the title-feature data rewards
click-bait construction. Both point at the same place, and the platform mechanic now proves it:
**a thumbnail that wins clicks and loses retention loses the A/B test.** The documentary register
is not a handicap under that rule — it is the thing being rewarded.

**5. Don't copy a competitor's formula.** PolyMatter explicitly tells students not to. B's Finding 2
gives the measured version: the surface features you'd copy don't discriminate anyway.

## Where they conflict, and what we assume

| Question | A (craft report) | B (measured) | Our assumption |
|---|---|---|---|
| Do design-form rules drive clicks? | Yes — text size, contrast, colour pairing, ≤3–4 words, 150–200px type | Surface title features show **+0pt to −8pt**, all inside noise (n=161) | **They are a floor, not a driver.** Form rules stop a thumbnail failing; they don't make it win. Keep them cheap and mechanical, stop weighting them as if they were the strategy |
| What actually moves performance? | Curiosity gap / stakes / one striking number | **Subject recognisability** — Crumbl 2.2M vs OpenAI 143K on identical grammar | B, with A's caveat. B's effect is far larger than anything A claims, but B cannot separate packaging from topic demand |
| Big numbers | "a striking number… signals magnitude and stakes" | Believable beats big: $20K/mo beat $340K/mo 4.9×; $3M/yr beat $5M/mo 18.8× | **B.** A treats magnitude as the variable; the data says credibility is. Convenient — it is the constraint the register already imposes |
| Arrows and circles | PolyMatter: they backfire, "by trying to stand out they actually blend in" | untested | **Lean A, but do not harden it.** Our rubric's Symbols section permits them sparingly. One expert's teaching is not a measurement, and swapping an unmeasured rule for another unmeasured rule is how we got here |
| Charts in thumbnails | Against literal charts; use a simplified iconic shape | untested | **A.** It is also the only guidance either source gives on the thing OE actually makes |

The honest read on the biggest conflict: **A is a much better source on platform mechanics; B is a
much better source on what wins.** A's design section is aggregated creator convention, which is
precisely the class of evidence that produced our current rubric and had to be amended six times.

## What changes

**Done in this pass:**

1. `thumbnail-rubric.md` A7 — the verified spec, the A/B mechanics, the sourced CTR bands replacing
   our internal "4% is healthy" figure. Rule 8's `1280×720 exactly` retired.
2. `check_thumbnail.py` — 3840 target with 1280 hard floor (sourced to the A/B downscale rule, not
   to a minimum YouTube doesn't impose), file-size ceilings, and a clean failure when ffmpeg is
   absent instead of a traceback.

**Still open, and deliberately not done:**

3. **The re-weighting.** B says the weights are close to inverted — `hero` holds 22 points for a
   property with no measured effect while specificity holds 10. A does not resolve this: it argues
   for a striking number on convention, B measures against it. The tie-breaker is the visual read of
   `contact-sheet.html`, which is still the missing half.
4. **The A/B test is now the real instrument.** Everything above is inference from other people's
   channels. Test & Compare measures ours, and it judges by watch time. The threshold from A is
   ~1,000 impressions per variant, so this needs the channel to grow first — but when it unlocks,
   variants should test *different hypotheses* (A5), because "too similar" is now a documented cause
   of an inconclusive result, not just an aesthetic complaint.

## What to distrust in both

- A's specific CTR-lift figures (+41%, +49%, "dark thumbnails +70%") have no named source; A flags
  them itself. The niche bands (gaming 8.5% / education 4.5% / finance 4–9%) are vendor studies. The
  only platform-official figure is **2–10% for half of all channels**.
- B cannot separate packaging from topic demand, and measures views rather than CTR.
- Neither has looked at a comp thumbnail image. That remains true until the contact sheet is read.
