# EP009 full cut review, reviewer A (S00 to S10, master 0.000 to 589.875)

Artifact: `assembly/qa/ep009-full.mp4`, sha256 `7409e5c25c5fa42666fc5ae8eeaeb7d6ea6a1c1ba251677251d7ed506c9b2f9a` (hash re-checked).
Machine-readable findings: `review/FINDINGS-A.json`. Evidence frames: `review/frames-A/`.
Status: agent reviewer recommendation. Not owner acceptance, no gate passed.

## Method

- Extracted the range at 4 fps (640x360) and built contact sheets per scene at 1, 2 and 4 fps, read against `word-transcript.json` words in each window.
- Full-size stills at every major state change (31 kept in `frames-A/`).
- Four-frame strips (two out, two in) at every one of the 40 segment boundaries from seg002 to seg040 (`frames-A/seams-*.png`).
- Presenter: assembly sync strips for P01, P03, P05 at 12 fps around the first word; 1 fps sheets for all of P01 to P07.
- Compared with EP007 accepted frames: `r58-full-episode-through-s13/qa/full.mp4` (1 frame per 8 s) and `r60-s15-context`.
- Standard: oe-video-direction SKILL, decision-method, precedent-index, presenter-references, every EP007 owner revise/reject/reopen, the EP009 direction plan and shot plan, the claims map.

## Could not judge

No audio playback and no normal-speed viewing. Unjudged: lip sync and voice match on every presenter take (only first-word strips), whether gestures land on their words, cut feel and reading time at speed, film motion quality and any reversal or morph artifacts between sampled frames (none of the S00, S03 film takes is reversed; F08 is outside my range), and loudness. The EP007 comparison is by eye on stills.

## Summary

29 findings: 3 blocking, 17 should-fix, 9 notes. The recurring gap against accepted EP007 work is text load: the evidence cards and the S09 and S10 models read as report pages, where EP007 accepted frames carry a heading, one drawing and a few short labels. Three truth problems: S06's range band implies only some bookings carry commission, S09 headlines exact filed figures the narration rounds, and S10 accumulates about 35 labels, dropping the direct-cost caveat while its result persists.

Would send to the owner as-is: S01, S02, S04, S08.

---

## S00 Cold open (0.000 to 59.458)

Works: the film establishes the inn, the two people and the counter cleanly, with no readable text or logos; F04's recognition smile lands the "knows by name" beat; the drawn reservation record and relay string are honest and legible; the second tag arrives on "same" at the same size as the first; the dashed "a service" inside the second tag makes "hiding inside" spatial. The inn has twenty windows, matching the rooms.

- **A-01 should-fix** seg001/seg002, 5.625. `frames-A/s00-0005.55-f01-end.png`, `s00-0005.70-f02-start.png`. Jump cut in nearly the same setup: the guest vanishes from counter to doorway while her key hand holds the same pose. Fix: scale all of seg002 to about 120 percent centred on her; seg001 stays wide.
- **A-02 should-fix** seg002/seg003, 10.500. `frames-A/s00-0010.45-f02-end.png`, `s00-0010.55-f03-start.png`. Second same-setup jump within five seconds (looking out of the window, then instantly facing front with her hand on the bell). Fix: with A-01, seg003 returns to wide so the size change motivates the cut; otherwise scale seg003 to about 115 percent.
- **A-03 note** seg003. The stop on "isn't his" is never performed (F03 accepted_partial); seg004 carries it. Keep.
- **A-04 should-fix** seg005, 23.2 to 26.0. `frames-A/s00-0024.80-relay-line.png`. The relay line is a short floating dash attached to neither building nor the relay field, so "the relay stops working" is not observable. Fix: start the line at the inn door, carry the relay field on its head, stop it just past "checkout" with the field resting at the stop.
- **A-05 note** seg005, 28.1 to 32.0. `frames-A/s00-0030.50-year-later.png`. The lit window cannot be seen at 720p, and the returning guest stands under the site instead of travelling the route. Fix: move the figure along the arc on "same" 28.12; fill the window with solid pencil tone on 29.44.
- **A-06 should-fix** seg008, 40.083 to 50.292. `frames-A/s00-0049.00-service-slip.png`. Scaled-up tags and site turn into heavy marker strokes unlike the thin pencil world; 3.6 s with no change. Fix: non-scaling strokes at world-kit weight, or about 70 percent scale centred. Cues unchanged.
- **A-07 should-fix** seg009 P01, 50.292 to 50.900. `frames-A/p01-sync-strip.png`. The mouth shapes speech and the hand gestures through 0.6 s of silence before "I"; with the 0.528 s Fal placement, picture may lead audio for the whole take. Fix: normal-speed check first; if leading, delay picture by the measured offset (earlier source frames or a held first closed-mouth frame), master audio untouched.

## S01 Sting (59.458 to 63.208)

Works: the accepted EP007 sting, silent room kept. No findings.

## S02 Brand and promise (63.208 to 87.833)

Works: BUILD, OWN, OPERATE on their words (about 67.0 to 68.2); title card on "Today" at 71.0 matches EP007; P02 hands frame a small space around "four numbers" and lower on "honestly pay", with no prop and eyes near lens. The seams at 73.542 and 87.833 are clean. No findings.

## S03 Context runway (87.833 to 188.667)

Works: F05 is the same kind of guest, and the phone back hides the screen; seg015's two flows (tag out, crowd route in) read as a fair trade without a funnel; the three-slot strip fills left to right on its words; "Europe, not here" and "not size-specific" are on screen.

- **A-08 note** seg013. `frames-A/s03-0090.50-inn-hold.png`. Six near-static seconds on "being fair to the system". Keep, or bring the site outline in on "system".
- **A-09 should-fix** seg016, 113.750 to 140.625. `frames-A/s03-0138.00-commission-card.png`. A report page: about ten text blocks, receipts nearly body size, and "Preferred +3 points" and "10 to 20%" that the narration does not say. Fix: receipts to foot size; layer labels to the spoken wording (exact values stay in the C005 receipt).
- **A-10 should-fix** seg017, 140.625 to 174.292. `frames-A/s03-0173.00-three-changed.png`. Three dense cards make a slide, and the middle kicker "BOOKING.COM GENIUS · SECONDARY" names Booking.com as the source of a Houst claim (C006). Fix: kicker "TRADE REPORTING · SECONDARY"; receipts to foot size.
- **A-11 should-fix** seg018, from 178.72. `frames-A/s03-0187.50-who-feels-it.png`. The empty "marketing hook" reads as a capital J next to the word "marketing". Fix: a dashed empty figure outline labelled "marketing hire" beside the desk figure on "no".

## S04 The question (188.667 to 205.083)

Works: one continuous P03 take, mouth closed through the silence before "Which", and no model object hints at the answer.

- **A-28 note** seg019. Placements are index-finger taps; brows gather strongly on the final question. Check tone at speed.

## S05 Earned thesis (205.083 to 236.292)

Works: the dashed empty place after checkout draws on "last", the tag lands on "next booking", and "A job" is the single oxide accent held through the pause.

- **A-12 should-fix** seg020. `frames-A/s05-0226.00-a-job.png`. Hide the labels and the desk figure does nothing: "check-in" and "housekeeping" carry the "not a lapse" point (EP007 r39). The site's pay line is a thick post, and the inn floats unconnected. Fix: drop both labels, slide the seg018 task sheets onto her desk inside the stay span on "not", draw the pay line as a thin line to the "booking" tick with a small tag, and drop the floating inn or seat it above the stay.
- **A-13 should-fix** seg021 P04, about 228.5 to 234.0. `frames-A/s05-0231.00-p04-held-gesture.png`. A flat hand held in the air for about five seconds reads frozen at still level, and this take has the largest drift. Fix: normal-speed check, then a continuous chest-up crop over the hold with no audio cut; regenerate only if that fails.

## S06 How much is rented (236.292 to 305.667)

Works: Cloudbeds and HOTREC stay side by side, not nested; the interest note is present; the cancellation bars are proportional and the card names the dataset; the "30-room inn, United States: not published" dashed box is honest.

- **A-14 should-fix** seg022, 236.292 to 260.0. `frames-A/s06-0238.00-empty-card.png`. Two empty ruled columns for about 3.7 s after the presenter, and the right column stays blank for 24 s. Fix: kicker from the first frame; the right column and divider draw in on "For balance" 259.14.
- **A-15 blocking** seg023 and the seg024 return, from 272.28. `frames-A/s06-0285.80-range-band.png`. Only the half-to-two-thirds band is shaded and tagged, so it says those bookings carry commission. The claim is half to two thirds of all bookings. Fix: shade from the first mark to "half" solid, hatch the extension to "two thirds" as the range, and tag the whole shaded run.

## S07 What the site keeps (305.667 to 368.000)

Works: the guest book is a new, clearly drawn object that goes inside the inn on "That book was the inn's", then slides intact along the line into the site on "now", with no lock, tear or fade; the boundary stops the arrow in front of the relay only, in oxide.

- **A-16 should-fix** seg026, 331.4 to 339.0. `frames-A/s07-0338.50-evidence.png`. The trade-press durations are set in the same headline serif as the primary Booking.com quote, directly under it, which invites reading "about 7 days" as Booking.com's own (C008 prohibited). Fix: body size under the secondary kicker.
- **A-17 should-fix** seg027 end state. `frames-A/s07-0367.50-design-constraint.png`. About twelve labels; the "email tool" card sits on the inn roof like a stray; the daypack guest stands behind the desk in her place. Fix: guest in front of the desk facing the dashed book, email tool card to the lower-left margin at reduced opacity, drop the "the inn's email field" label.

## S08 Fair question (368.000 to 410.042)

Works: P05 is short and closed-mouthed in the lead-in silence; the free-link caveat and "public tool pricing, not a quote" are on screen; the drawn fallback for the failed F06 carries the passage: cards converge on one desk figure, and the list's owner line is an empty oxide dash, which does not read as her failing.

- **A-18 note** seg029. `frames-A/s08-0388.00-parts-cheap.png`. Text-only for 15 s with the right half empty. Optional: receipts smaller.
- **A-19 note** seg030 to seg032. `frames-A/s08-0409.80-list-card.png`. The cards repeat the narration word for word, and the figure stays passive. Keep.

## S09 Already sold at two scales (410.042 to 480.042)

Works: the tiers arrive on their words; the revenue manager's monthly loop is a clear retainer; no line reaches the small inn; the bracket names who pays; P06 closes on first-person finding.

- **A-20 should-fix** seg033, 410.3 to 412.0. `frames-A/s09-0412.50-figure-gone.png`. The innkeeper and her desk fade out just after "the list belongs to nobody", which can read as her leaving and breaks the persistent world. Fix: keep her small beside the list card at the small end.
- **A-21 blocking** seg034, from 455.16. `frames-A/s09-0469.00-scale-busy.png`. "$186.1 billion" and "$119.6 billion" are headline figures while the voice says "more than a hundred billion"; C014 keeps the exact figures in the receipt. The direction plan asked for these tags, so this is a plan versus claims-map conflict for the director. Fix: one line, "more than $100 billion of bookings each, 2025 · by their own filings · blended", with the exact figures in the receipt only.
- **A-22 should-fix** seg033 and seg034. Same frame. About seventeen text blocks with three full receipt lines, and the booking sites sit on the property-size axis. Fix: receipts to foot size; lift the sites onto their own base line at the right labelled "the floor".

## S10 The ceiling (480.042 to 589.875)

Works: the always-on "ILLUSTRATIVE MODEL · a made-up inn · swap in real inputs" and receipt; "my assumption" and "hypothesis nobody has measured" tags; the dashed 10-point slice never turns solid; the model state carries exactly across P07; the ghost ceilings are proportional (double above, half below); the retainer tag sits under the line; the four input boxes light on "four numbers".

- **A-23 blocking** seg036 to seg039. `frames-A/s10-0589.80-final.png`. About 35 text items by the end; each step adds labels and removes none, so the frame is a spreadsheet and the words carry the argument. This is the owner's EP007 r39 return ("busy... the heading is doing most of the work"). Fix: once the panel opens (538.49), fade the left column to 30 percent; in the panel show only the current step's label and replace it on the next cue; end on panel bar, ceiling line and sub-label, retainer tag, dashed hypothesis tag, slip, label and receipt; show the ghost ceilings one at a time with one short label each.
- **A-24 should-fix** seg038, from 556.2. `frames-A/s10-0557.00-caveat-dropped.png`. "3.5% to 5%" and "one vendor's own figure" vanish on "What's left" while the remainder and the monthly ceiling built on them persist. Fix: a small persistent "after 3.5 to 5% direct cost · low end one vendor's figure" under the remainder.
- **A-25 should-fix** seg036 to seg039. `frames-A/s10-0520.30-commission.png`. Seven exact modeled figures sit under the rounded ones and make an illustrative model look measured. Fix: remove them from the canvas; the receipt's ceiling table holds them.
- **A-26 note** seg036, 480.042 to 483.44. The label and receipt are absent for the first 3.4 s. Fix: present from frame one.
- **A-27 note** seam into S11, 589.875 to 590.5. `frames-A/s10-0590.30-seam-s11-dissolve.png`. A two to three frame dissolve double-exposes the dense model over the S05 timeline. Fix: hard cut, or 6 frames through clean paper.

## Across the range

- **A-29 note** presenter set. All seven takes (P01 to P07) use the same wide framing with no editorial crop. Head and hand patterns differ between adjacent takes, and hands move in every take. Consider one continuous emphasis crop where the argument narrows (P04 "is a number", P07 "wrong number").
- No repeated heading entrance between adjacent model scenes. No site-as-villain, no guest book taken back, no checked outcome, no "saved" drawn as a result in this range.
