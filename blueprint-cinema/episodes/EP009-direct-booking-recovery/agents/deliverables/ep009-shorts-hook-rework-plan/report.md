# EP009 Shorts hook rework: implementation audit

## Finding

The four r1 compositions are technically sound, but they are built as contiguous excerpts. That
is the wrong editing contract for the new direction. A fast vertical episode hook needs to place
the tension in the first sentence, move through evidence every one to three seconds, and stop before
the episode's useful answer. The locked EP009 carrier does not need to change.

Preserve `EP009-SHORTS-001` as the reviewed r1 record. Build the hook revision under a new
`blueprint-cinema/experiments/EP009-SHORTS-002/` root. This avoids invalidating the hashes in the
r1 `BUILD.json`, the four source contracts, and the existing private review page.

The reference to Cleo Abram should be implemented as observable editing properties rather than a
persona copy: visible motion and a concrete problem on frame one, an immediate spoken curiosity
line, quick alternation among presenter, film, real evidence, and portrait graphics, one clear
causal thread, and an unresolved final question that points to the long episode.

## What the current cuts disclose

| Short | Current range | Assessment |
| --- | --- | --- |
| 01 · Second commission | `[0,1427)`, 59.458 s | It does **not** disclose the four-number model or the service economics. The problem is pace: it spends 27 seconds reaching the repeat booking and feels like the beginning of the full episode rather than a vertical cold open. |
| 02 · Machine vs. judgment | `[16619,17111)`, 20.5 s | Borderline complete. It explains the entire machine half and states the human-half thesis. It still withholds the actual rules for voice, guest selection, consent, and restraint, so it can remain a hook if those rules are named as the missing payoff. |
| 03 · Guest book | `[8070,8876)`, 33.583 s | It reveals the first practical answer: a permissioned guest book at the front desk. It still withholds the operational bottleneck and service opportunity. This is the closest to revealing too much; keep the final `why doesn't the inn just do it?` question prominent and remove slower connective explanation. |
| 04 · Wrong number | `[12150,12690)`, 22.5 s | It withholds recoverable share, net savings, price ceiling, and viable fee. The issue is order: the 10.8-second modeled number arrives before the sharper `It's the wrong number` thesis. |

None of the four ranges gives away the full episode. Shorts 02 and 03 risk feeling complete because
their current last lines land as conclusions. The r2 ending must visually convert those lines into
questions whose answers are explicitly reserved for the full episode.

## Safe r2 edit decision lists

All audio remains exact, unmodified speech from the locked r8 carrier. Frame ranges use
`[in_frame, out_frame_exclusive)` at 24 fps. A separate 24-frame end card follows each edit; it has
no new voiceover and remains review copy until the owner accepts it.

### Short 01 · The repeat guest pays twice

Keep source order, but start at the repeat booking. This removes the 27-second runway while keeping
the unresolved economics.

| Order | Words | Frames | Duration | Purpose |
| ---: | --- | --- | ---: | --- |
| 1 | `W000075–W000088` | `[648,763)` | 4.792 s | `A year later...` immediate temporal jump |
| 2 | `W000089–W000101` | `[780,870)` | 3.750 s | same site commission again |
| 3 | `W000102–W000109` | `[882,941)` | 2.458 s | repeat guest known by name |
| 4 | `W000110–W000123` | `[973,1080)` | 4.458 s | service hidden in the commission |
| 5 | `W000150–W000165` | `[1317,1427)` | 4.583 s | unanswered cost and seller question |
| 6 | end card | 24 authored frames | 1.000 s | `WHAT DID THE SECOND STAY COST?` / `FULL EPISODE · TAP RELATED VIDEO` |

Spoken duration is 20.042 seconds; review duration is 21.042 seconds. The arithmetic setup is also
withheld; the full episode owns both the calculation and its result.

### Short 02 · Cheap drafting, expensive judgment

Use the locked line immediately after the existing excerpt as a cold open, then return to the
machine demonstration. This is a derivative reorder and therefore needs a new r2 source contract.

| Order | Words | Frames | Duration | Purpose |
| ---: | --- | --- | ---: | --- |
| 1 | `W002095–W002101` | `[17458,17515)` | 2.375 s | `The drafting got cheap. The judgment didn't.` |
| 2 | `W002001–W002011` | `[16619,16695)` | 3.167 s | machine-versus-human question |
| 3 | `W002012–W002017` | `[16714,16764)` | 2.083 s | repetitive half |
| 4 | `W002018–W002035` | `[16775,16899)` | 5.167 s | model drafting examples |
| 5 | `W002036–W002044` | `[16913,16980)` | 2.792 s | checkout-date automation |
| 6 | end card | 24 authored frames | 1.000 s | `WHAT DOES THE HUMAN DECIDE?` / `FULL WORKFLOW · TAP RELATED VIDEO` |

Spoken duration is 15.583 seconds; review duration is 16.583 seconds. The human-half conclusion is
withheld along with its voice, consent, selection, and restraint rules. The real Node-RED close-ups
remain the evidence spine. Do not replace them with a generic software mockup.

### Short 03 · The guest book moved

Keep source order and stop immediately before the practical answer. The hook preserves the rule
boundary and explicitly says an email tool is not first, but it does not reveal what comes first.

| Order | Words | Frames | Duration | Purpose |
| ---: | --- | --- | ---: | --- |
| 1 | `W000941–W000950` | `[8070,8141)` | 2.958 s | guest book now lives at the site |
| 2 | `W000951–W000960` | `[8148,8232)` | 3.500 s | inn served the guest but lacks the email |
| 3 | `W000961–W000974` | `[8250,8361)` | 4.625 s | design constraint before tool |
| 4 | `W000975–W000994` | `[8373,8520)` | 6.125 s | relay and site-rule boundary |
| 5 | `W000995–W001003` | `[8520,8592)` | 3.000 s | what the inn needs first is not an email tool |
| 6 | end card | 24 authored frames | 1.000 s | `IF NOT EMAIL, WHAT COMES FIRST?` / `FULL EPISODE · TAP RELATED VIDEO` |

Spoken duration is 20.208 seconds; review duration is 21.208 seconds. The permissioned front-desk
guest-book answer and the execution bottleneck both stay in the full episode.

### Short 04 · The big number is the wrong number

Cold-open with the correction, show the modeled number, then land on the calculation the episode
still owes the viewer. This is a derivative reorder and therefore needs a new r2 source contract.

| Order | Words | Frames | Duration | Purpose |
| ---: | --- | --- | ---: | --- |
| 1 | `W001447–W001465` | `[12495,12618)` | 5.125 s | `It's the wrong number... It needs the sites.` |
| 2 | `W001401–W001437` | `[12150,12409)` | 10.792 s | 18–22% assumption and $105K–$130K estimate |
| 3 | `W001466–W001475` | `[12618,12690)` | 3.000 s | `what a recovery service can shift` |
| 4 | end card | 24 authored frames | 1.000 s | `WHAT CAN THE INN ACTUALLY SHIFT?` / `FULL MODEL · TAP RELATED VIDEO` |

Spoken duration is 18.917 seconds; review duration is 19.917 seconds. The number sentence needs at
least two visual states: commission band, then annual modeled spend.

## Exact implementation surface

Do not edit `EP009-SHORTS-001/build_previews.py` in place. Copy its reusable native portrait
components into `EP009-SHORTS-002/build_hook_previews.py`, then make these structural changes:

1. Replace the single `Scene(source_in, source_out, ...)` timing model at r1 lines 35–43 with two
   explicit records:
   - `AudioEdit(word_in, word_out, source_in_frame, source_out_frame_exclusive)`
   - `VisualBeat(timeline_in_frame, timeline_out_frame_exclusive, layout, visual_source_in_frame, ...)`
   Audio order and visual order must be independently inspectable.
2. Replace `PROJECTS` at lines 45–103 with the EDL above plus authored visual beats. Every project
   must declare `withheld_payoff`, `end_card`, and `first_frame_hook`.
3. Replace `caption_groups()` at lines 125–192 with `caption_groups_from_edl()`. Group captions
   inside each edit only. Convert every word to the output clock with:
   `timeline_in + (word_time - source_in_time)`. Never merge across an edit boundary.
4. Keep `write_assets()` at lines 208–217 and the exact carrier/lock hash checks at lines 27–31.
   Add the r2 editorial map and the owner clarification source as separately hash-bound inputs.
5. Rewrite `write_brief()` and `write_storyboard()` at lines 220–330. The r2 contract is
   `episode trailer assembled from exact locked words`, not `locked long-form excerpt`. Record every
   reorder and omission; do not claim a contiguous source range.
6. Reuse `native_diagram_html()` at lines 333–476, but add layouts for the four first-frame hooks
   and four tailored end cards. Begin with a legible claim and visible source or graphic motion at
   frame one. Keep the brand as a small bug; do not spend opening time on an identity card.
7. Change `subcomposition_html()` at lines 479–631 to accept output-frame timing separately from
   source media timing. Use hard, motivated cuts every roughly 24–72 frames. Do not add fake cursor
   behavior or fabricate workflow states.
8. Replace the single `<audio>` element in `index_html()` at r1 line 689 with one `<audio>` clip per
   EDL row, each using sequential `data-start`, exact `data-duration`, and exact
   `data-media-start`. Keep all clips on audio track 10. Use sentence boundaries so no crossfade or
   synthetic interpolation is required.
9. Replace `write_contract()` at lines 707–729 with schema `oe-ep009-short-source-contract-v2`.
   Store ordered EDL rows, exact output frame spans, word ranges, omissions, reordered status,
   withheld payoff, end-card review copy, carrier hash, final-lock hash, and authorization limits.
   Remove the inaccurate r1 line `No narration rewrite or source reordering`; use `No new spoken
   words; every audio edit is an exact locked-carrier range`.
10. Keep r1 `BUILD.json` unchanged. Create `EP009-SHORTS-002/BUILD.json` only after all four r2
    checks pass and bind every new index, source contract, check report, animation map, contact
    sheet, review-page source, and owner clarification record.

Short 02's r1 project was authored outside the common generator and promoted into the selected
root. For r2, either normalize it into `build_hook_previews.py`, or copy it once into the r2 root
and add the cold-open and end card there. The first option is safer because all four EDLs then use
one provenance contract and one caption compiler.

## Visual pacing contract

- A muted viewer must understand the problem from the first frame.
- Put the sharpest exact spoken line at timeline zero. No logo animation, setup card, or pause.
- Alternate among locked avatar/presenter, generated hospitality film, native portrait evidence,
  and real Node-RED captures. Change the accountable focus every one to three seconds; do not move
  merely to keep the frame busy.
- Use large sentence fragments as evidence labels, while the lower caption rail remains verbatim.
- Keep captions, the Node-RED truth ribbon, model qualifiers, and fictional/no-send boundaries
  readable at a 390-by-844 phone viewport.
- The end card must identify the withheld payoff and point to the full episode. Animate the
  question and action within the one-second card; do not leave a dead hold. Do not show a URL. At
  publication, configure the YouTube related-video action and source any pinned-comment URL only
  from `launch/links.json`. The visible `TAP RELATED VIDEO` instruction is valid only if that action
  is actually configured at publication.
- No new provider generation is needed. The locked carrier, existing film, avatar footage, native
  portrait graphics, and real tool capture are sufficient.

## Review-page revision

Create a versioned `ep009-shorts-r2` review package. Do not overwrite
`assembly/qa/ep009-shorts-r1/`.

Change `build_mobile_review.py` lines 13–23 so:

- `OUTPUT` is `assembly/qa/ep009-shorts-r2`.
- all four sources resolve from `EP009-SHORTS-002`; remove the special Short 02 path into the agent
  deliverable.
- every card receives a hook line, reveal, withheld payoff, exact duration, and contact sheet.
- the page labels these as `full-episode hook cuts`, not excerpt compositions.

The r1 page at lines 70–99 is a contact-sheet review and cannot prove pace. The r2 page should keep
contact sheets as visual fallbacks, then add a `Play motion preview` link for each checked project.
Serve each project with `hyperframes play` on a local port and add tailnet-only Tailscale Serve
paths under the existing `:3071` host. This permits phone playback without treating a draft render
as an approved final MP4. The page should state that approval covers hook structure and vertical
composition only; render, upload, release, publication, title, pinned comment, and related-video
selection remain separate.

## QA commands

Run from each of the four r2 project directories. Keep one `HYPERFRAMES_RUN_ID` for a project's
verification pass.

```bash
npx hyperframes@latest upgrade --project . --check --json
npm run check -- --json --samples 15 --at-transitions \
  --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error;seek=.25,1" \
  --frame-check > check-hook-r2.json
npm run check -- --snapshots --samples 15 --at-transitions \
  --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error;seek=.25,1" \
  --frame-check
npx hyperframes snapshot --at <first-frame>,<every-edit-midpoint>,<end-card-midpoint>
npx hyperframes keyframes . --json > animation-map-hook-r2.json
npx hyperframes play --port <dedicated-port>
```

The upgrade probe is read-only. Apply an upgrade only if it reports a stale pin, and rerun `check`
after any version change. Do not run `render` until the owner reviews and accepts the motion
previews.

Add three source-level checks before HyperFrames QA:

1. Recompute every EDL frame span from the first and last word times and require all words to fit.
2. Assert that concatenated caption tokens equal the ordered EDL transcript exactly.
3. Assert that r8 carrier SHA-256 remains
   `cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e` and the final lock
   manifest remains `b9d107718c0d760e388c1a5167bcaf7e06ebfb29504ed469fac385aa2aa54cd2`.

For manual phone review, inspect the first 1.0 second muted, each audio cut, every real-tool zoom,
the last spoken line, and the one-second end card. Reject a cut if the first frame needs prior
context, an edit produces a clipped phoneme/click, a source qualifier disappears, a visual beat
holds longer than its idea, or the end card answers its own question.

## Authority boundary

The user's new instruction changes the four Shorts direction. It does not reopen or alter the
owner-locked long-form r8 carrier. It authorizes local derivative re-editing and private review;
it does not authorize final MP4 rendering, upload, release, publication, public title/copy, or a
hand-typed episode URL.
