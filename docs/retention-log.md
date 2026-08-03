# Retention Log

Per-episode audience-retention findings → structural rules for the next script. Sample sizes noted; day-one curves are warm-audience-skewed. Re-pull at day 7.

## EP001 — day one (July 6, 2026 · n≈25 processed views, ~70 lifetime)

Topline: 1:57 avg view (20.8%) · LinkedIn-referred viewers avg 3:07+ · 4 likes / 4 comments / 6 shares / +1 sub.

Curve:
- **0:00→0:30: 80%→36%.** The branded open (welcome + series line + title card + 6s break) precedes the $5.9B payoff at 0:26. Cold viewers left during the ceremony.
- **2:00→5:00: 28% plateau, spike to 40% at ~2:50** (the $40K fact-check — scrub-to + rewatch behavior). Evidence body retains.
- **6:00: 20%→12%** mid-playbook. List fatigue at the attention floor. 12% flat to the end (finishers).

## EP002 — day-18 read, CLOSED as unreadable (voice-agent-agency, pub 2026-07-13)

Pulled Fri 2026-07-31 (day 18). **There is no retention curve, because there are no views.**

- Impressions **288** · CTR **0.7%** · Views **3** · unique viewers **3**.
- Impressions flatlined at ~day 8 and have not moved since.
- Its four shorts did fine by channel standards: **150 / 90 / 82 / 81 views** (403 combined).

**403 short views produced 3 episode views.** The routing is the failure, and the cause is
concrete: every EP002 short's pinned comment reads *"…is in the full episode — link in bio."*
Verified live on the 150-view short — pinned as `@operatoreconomy`, correct register, **zero
clickable URL**. The episode link exists only as a description chip, which on the Shorts player
is effectively invisible. The highest-traffic surface the channel has was pointed at a dead end
for the whole of EP002's window.

EP003's pinned comments carry real URLs (episode + blueprint), so the defect is already fixed
forward. It was never retro-fixed on EP002's shorts, which are still the channel's best-trafficked
assets. **Backfill those four pinned comments** — it is the cheapest reach the channel owns.

## EP003 — day-4 read, no curve available (boring-automation-agency, pub 2026-07-27)

Pulled Fri 2026-07-31 (day 4).

- Impressions **160** (142 in the 4-day funnel window, 41.5% of them YouTube-recommended) ·
  CTR **0.0%** · **Views from impressions: 0** · total views **1** (traffic source 100% "direct or unknown").
- AVD 0:37 on n=1. Watch time 0.0 hrs. No curve; n=1 is not a sample.

**YouTube served this episode 142 times and it earned zero clicks.** That is a packaging failure,
not a retention failure — and it is the first time the channel has had enough impressions to say so.
Prime suspect is the thumbnail. EP001 shipped "Consulting just collapsed." and EP002 shipped
"NOBODY PICKED UP" — three or four huge words, readable at 120px. EP003 shipped the raw title-card
frame: a full sentence in body-copy type ("The tool the operator runs on is itself a billion dollar
business."), unreadable at feed size. The publishing checklist's "Thumbnail = title-card frame" step
was never ticked for EP003, and the design-system rule that produced it now needs a caveat: the
title card is the *source*, not the deliverable.

Note also a render defect: all four EP003 shorts carry `THE OPERATOR ECONOMY · № 001` in the
title card. Wrong episode number on every short this week.

## Rules adopted for EP004+ (enforce at script/publish gate)

5. **Retention is not the bottleneck; the click is.** Do not spend another change-set on script
   structure until an episode clears ~2% CTR. Rules 1–3 stay in force but are unfalsified — they
   have never been tested on a cold audience, because no cold audience has arrived.
6. **Thumbnail gate at publish.** Three to five words, ≥90pt, readable at 120px, contrast-checked
   against the dark ground. The title-card frame is the starting point, not the export. No episode
   goes public without this checked by eye at feed size.

   **Root cause found 2026-07-31, and it wasn't a design failure.** The thumbnail was a manual
   ritual with no pipeline step and no gate. EP001 shipped a photo scene (`ep001-people.png`) and
   is still the channel's best video. EP002 got a hand-written rework with two candidates and a
   note (0.7% CTR). **EP003 got nothing at all** — no `thumbnail.json`, no scene image, no note —
   so the render fell back to the title-card frame and nothing in the pipeline noticed. The
   Remotion `Thumbnail` composition already existed, already had a photo variant, and its own
   docstring already named the problem ("designed for the 320px tile, where the title-card frame
   dies"). Nothing was generating its input.
   Fixed by `scripts/originate/prepare_thumbnail.py`, wired into `originate.py render`: it emits
   two rubric-checked candidates, refuses to invent an episode number on the thumbnail (rule 1),
   flags text options that duplicate title words (rule 2), and **exits 2 when no scene image
   exists** rather than letting the absence pass silently.
7. **Every pinned comment carries a live URL.** No "link in bio," no description chips. Episode URL
   + blueprint URL, both clickable, on every short. Backfill retroactively when a short passes 100 views.
8. **Day-7 read stands (Rule 4), with a floor:** if views < 25, log "no curve, n too small" and read
   the reach funnel (impressions → CTR → views) instead. Do not manufacture retention findings from
   single-digit samples.

1. **Payoff before ceremony.** The hook number lands ≤0:15. Series line, title card, and the musical break come AFTER the first slam — the break is the exhale, not the wait. (Bridge placement moves accordingly in layout config.)
2. **Playbook compression.** ≤60s on the steps; the video gives the shape, the blueprint PDF gives the detail. Strengthens the download CTA at the same time.
3. **Evidence structure unchanged** — plateau + fact-check spike says it works. Fact-check moments are confirmed shorts material.
4. **Day-7 re-read** per episode: retention curve (API: audienceWatchRatio × elapsedVideoTimeRatio), CTR by traffic source (Studio), before any further structural changes. One change-set per episode; don't over-rotate on n=25.
