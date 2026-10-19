# EP009 — Gate 3, pre-publish episode library review

Run 2026-10-12 because `studio/config/blueprint.json` has `autonomy.training_mode: true`, which
forces this review regardless of confidence score. Against `docs/content-rubric.md` (publish gate
80 of 100, zero kill-list hits) and its Shorts addendum.

Everything marked AUTO below was executed against the artefacts, not recalled. Everything marked
HUMAN is yours.

---

## The one finding that needs your decision

**The episode's only subscribe prompt is at 20:20, the last line.** There is no mid-roll CTA and
the Operator Canvas is never mentioned in the narration at all. The rubric's kill list includes
"end-only CTA as sole CTA", and section VI asks for one subscribe prompt after the first major
evidence payoff plus a soft blueprint mention at 55 to 75 percent of runtime.

**It is not an EP009 regression.** No. 001 is identical: its only `subscribe` is at 18:57, 100
percent of runtime, and it never says blueprint or canvas either. That episode published on
2026-10-05. So this is a standing deviation that already shipped once, not a new fault.

Three ways to take it:

1. **Ship consistent with No. 001.** The deviation is already live on the channel. The Canvas link
   is in the description's first line and the pinned comment, which is the other half of the
   rubric's CTA requirement and is satisfied.
2. **Fix it in EP009.** Means re-cutting narration to add a mid-roll line, which is paid VO plus a
   presenter regeneration for that span, and re-conforming the master.
3. **Amend the rubric.** If two episodes have now shipped against this rule, the rule may be wrong
   for this format rather than the episodes being wrong. That is a deliberate change, not a waiver.

My read: option 1 for this episode, option 3 as the real decision, because a kill-list item that
both published episodes violate is a rule nobody is actually using. But it is a rule you set.

---

## AUTO results

| Check | Result |
|---|---|
| Banned openers (hey / welcome / today / in this video) | **none** |
| Wrap-up signals (in conclusion / thanks for watching / that's how) | **none** |
| Kill-list phrases (you won't believe / shocking / hey guys / welcome back) | **none** |
| Income-promise patterns | **none** |
| Premise stated by 0:15 | **yes** — the relay email lands at 0:08 and the thesis question by 0:40 |
| Thumbnail text duplicates title words | **no** — HELP HER KEEP THEM shares no content word with the title |
| Thumbnail overlay word count | **4** — the rubric's stated maximum (target is 3). No. 001 was 3 |
| Shorts: hashtag walls | **none** |
| Shorts: cold-viewer context and standalone payoff | **PASS**, `shorts_contract.py --mode derived`, all four |
| Banned lexicon and em dashes across all five surfaces' copy | **clean** against the current voice.md |
| Hand-typed URLs in any copy | **none**; `{{EPISODE_URL}}` and `{{BLUEPRINT_URL}}` only |
| Loudness | long-form and all four Shorts at **-14.0 LUFS**, two-pass linear |
| Captions | 368 cues from forced alignment; no malformed blocks, no overlaps |

## Judgment calls, flagged rather than decided

**Chapters.** I wrote 21. The rubric's own conflict resolution says chapters are optional for this
lane and can hurt narrative content by letting viewers skip the build, and to use them only when
non-spoilery on framework-heavy episodes. EP009 is a hybrid: a narrative cold open and a
framework-heavy middle. Two chapter names are arguably spoilery, "The verdict" and "The first
move". Cutting the chapter list entirely is defensible; so is trimming those two.

**Thumbnail at four words.** Allowed, at the ceiling, and one more than No. 001. The series
formula you ratified puts HELP plus a pronoun in two of the four, so the verb slot is where the
count gets decided. REBOOK would have made it three.

## HUMAN items, for you

- Hook: is the archetype named and the tension real in the first two sentences?
- Does the previewed-payoff arc hold, or does it read as a data dump?
- Voice: does the cloned narration read as directed rather than monotone?
- Material variation from No. 001: different enough not to read as the same video?
- Thumbnail: single focal point, legible at 180 to 320px. The shrink test is in
  `EP009-PACKAGING-001/review/`.

## Not in scope of this gate

The altered-or-synthetic-content disclosure is a Studio step at upload and is on the checklist in
`content/youtube-longform.md`. The Shorts' Related Video is set after the episode is live.

---

## Resolution of the CTA finding (2026-10-12)

Owner chose to fix it in the episode rather than ship the deviation or amend the rubric. The
spoken fix was scoped first and rejected on cost once its real shape was clear: inserting a line
shifts every segment after it, which means rebuilding the r3 to r11 assembly chain and reopening
narration locked at N7 behind its own gate.

**What shipped instead:** a five-second Operator Canvas card at **12:39**, 62 percent of runtime,
inside the "What do you sell first?" beat. Mineral ground with paper text and an oxide rule,
matching the Shorts' bridge cards. No narration change, no timing change, no re-cut.

Placement was measured, not chosen by eye. Seven candidate stretches between 55 and 75 percent were
sampled for how much content sits in the card's area across the full five seconds. seg050 at frame
18224 returns 0.0 percent at every sample; the next best was 2.5. An earlier placement at 13:15 was
built and discarded because the diagram underneath finished building and the card covered its
"front desk" element.

This satisfies section VI's position requirement. The framing is the owner's to accept.

**Still open as a standing question:** the rubric's kill-list item "end-only CTA as sole CTA" now
has two published episodes against it, No. 001 unmodified and this one fixed by an overlay rather
than by the spoken prompt the rubric describes. The rule is worth revisiting on its own terms.
