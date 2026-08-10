# Back-catalog thumbnail test — EP001 to EP004

Opened 2026-08-10. **This is the only controlled experiment the channel can run.**

Four episodes already have impressions against fixed content. Swap the thumbnail, change nothing
else, and the CTR delta is attributable. A new episode confounds thumbnail with topic, title,
timing and length, so it teaches almost nothing at this sample size. This test isolates the one
variable the data says is binding.

## Why this is the priority

| Episode | Impressions | CTR | Views |
|---|---|---|---|
| EP002 | 288 | 0.7% | 3 |
| EP003 | 160 | **0.0%** | 1 |

Healthy is 4% or better. EP003 drew zero clicks from 142 recommended impressions **because it has
no thumbnail file at all** and YouTube fell back to the title-card frame.

## What the current four actually are

Audited 2026-08-10 against `thumbnail-rubric.md`. All four pass `check_thumbnail.py`; mechanical
soundness is not the problem here, composition is.

| Ep | What's on it | Rubric breaks | Read at 120px |
|---|---|---|---|
| 001 | Cream title card. "The $5.9 Billion Business You Can Start for $100" in serif display, plus a subtitle line and an `OPERATOR BLUEPRINT · № 001` kicker | 1, 2 (9 words + serif), 3, 5 (cream on cream), 6 | Nothing. It is a paragraph |
| 002 | Split field. Navy/gold `$11B ELEVENLABS` against cream/navy `$500 PER CLIENT / MO`. Strong bones | 1 (kicker **and** an `OE.` mark), 3, 4 (`OE.` sits in the duration-stamp corner) | The two numbers read. The labels do not |
| 003 | **Nothing. No file exists.** | all | n/a |
| 004 | Photo scene, laptop pricing page, warm bokeh. `$4,995` gold over `NO EMPLOYEES` white, bottom-left | 3 (no face; a screen is not a person) | Both lines read. Best of the four |

**EP004 is the template.** Real scene, text bottom-left, no branding, high contrast, ≤4 words. The
design was converging, and then EP005 regressed to floating text on a transparent ground because
it was generated outside the pipeline.

## The four replacement concepts

Rules held across all four: one photo scene, one text block bottom-left, ≤4 words, thick sans
(Supreme 800), gold or paper on a dark scrim, no kicker, no `OE.` mark, no episode number,
1280x720 opaque. Each states a number that does not explain itself.

### EP003 first — it has nothing, and it is the cheapest win

**"The 5 Billion Dollar Business That Sounds Boring"** (boring-automation-agency)

Scene: a small warehouse or back-office desk, late afternoon, one person's workspace with paper
invoices stacked beside a laptop. Warm, unglamorous, real.
Text: `$5.2B` over `STILL ON PAPER`.
Why: the episode's whole tension is that the money is in work nobody wants to look at. The scene
has to look boring while the number refuses to be. Currently there is no thumbnail at all, so any
compliant image is a strict improvement and the CTR read is clean from zero.

### EP002 — keep the bones, strip the branding

**"The Phone Call Businesses Never Answer"** (voice-agent-agency)

The split-field composition is the strongest idea in the set and should survive. What has to go is
the `OPERATOR BLUEPRINT · № 002` kicker and the `OE.` mark, which together burn the top-left and
bottom-right of a 1280x720 canvas on information the viewer already sees next to the title. The
`OE.` mark is also sitting exactly where YouTube stamps the duration.

Revision: same `$11B` / `$500` split, labels dropped to a single word each, both marks removed,
and the reclaimed space given to the numbers. Optional stronger variant: replace the left panel
with a real scene of a phone ringing on an empty reception desk, keeping `$500` as the only text.
That adds the human absence the episode is about and fixes rule 3.

### EP001 — replace the title card entirely

**"The $5.9 Billion Business You Can Start for $100"** (ai-implementation-consulting)

Nothing here is salvageable; it is a title card that duplicates the title word for word, which
rule 2 forbids outright.

Scene: a small business owner mid-conversation at their own counter, expressive, close crop, eyes
on the upper third.
Text: `$100` over `TO START`.
Why: the title already carries $5.9B, so the thumbnail must carry the other end. $100 against a
real person's face is the curiosity gap, and it is the first thumbnail in the set with a human in
it, which is the rubric's own priority-1 answer for attention.

### EP004 — light touch, it is already closest

**"The Design Agency You Can Run Alone"** (solo-design-agency)

Keep the composition. One fix: the laptop screenshot contains its own `$4,995/mo` and a partial
`$9,99...`, so three dollar figures compete and at 120px it reads as noise. Blur or crop the
screen so the overlaid `$4,995` is the only number, and darken the lower-left scrim for
separation.

Optional test variant: swap the laptop for a person at a desk to add a face, and run it against
the current one. This is the cleanest A/B in the set because everything else stays fixed.

## Running it

1. Generate each inside the pipeline, not externally. Save as
   `studio/remotion/public/thumbs/<slug>-a.png` so `prepare_thumbnail.py` finds it.
2. Run `check_thumbnail.py` on each. Do not upload a failing file.
3. Swap all four on the same day so they share a traffic window.
4. Record the pre-swap baseline first: impressions and CTR **by traffic source** per episode.
   Browse and Suggested are the numbers that matter; overall CTR blends in subscriber impressions
   and hides the problem.
5. Read at day 7 and day 14 into `docs/retention-log.md`.

**Expect a slow read.** At 160 to 288 impressions per episode, a swing from 0.7% to 4% is a handful
of clicks, well inside noise. Treat direction as signal and magnitude as unreliable until the
impression base grows. The one unambiguous read available is EP003, which cannot do worse than
zero.

**Do not swap titles at the same time.** One variable.
