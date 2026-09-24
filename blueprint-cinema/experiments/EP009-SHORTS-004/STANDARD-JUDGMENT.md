# EP009 Shorts — judgment against the standalone-payoff standard

Standard, as committed in `docs/content-rubric.md`:

> Hook in 1–2 seconds, orient a cold viewer to the topic immediately, visible movement
> frame one, and resolve one bounded promise inside the Short. The viewer must not need the
> caption, another Short, or the episode to understand the context or takeaway. A pinned
> comment and Related Video may offer broader, distinct depth; they cannot carry the missing
> conclusion.

Kill list item, same file: *"Shorts with … no cold-viewer context, or no standalone narrow
payoff."* `cliffhanger_line` is retired and does not satisfy the gate
(`docs/content-rubric.md`, Shorts derivative checks).

Owner ruling governing this pass: decision event `ep009-owner-shorts-standard-ruling-v1`,
source record
`blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/2026-09-21-owner-shorts-rulings.json`.

Judged against the four playable r3 cuts in `EP009-SHORTS-003`, not against their briefs.

---

## The finding that runs through all four

Every r3 Short ended on an **interrogative end card that routed its conclusion to the
episode**:

| Short | r3 end card headline | r3 routing line |
|---|---|---|
| 01 | "What could the inn actually pay?" | "The calculation in EP009" |
| 02 | "What work would an inn pay for?" | "The service and the calculation in the full episode." |
| 03 | "Who owns the second booking?" | "Full episode · EP009" |
| 04 | "What can this inn actually afford?" | "The full calculation in EP009" |

Under the retired cliffhanger standard that was the point. Under the committed standard it is
the failure mode the rubric names exactly: the last thing on screen asks a question the Short
does not answer and tells the viewer the answer is elsewhere. All four end cards are replaced
with declarative cards that state what the Short resolved; the routing line now names what the
episode *adds*.

---

## Short 01 — the second commission

**r3: partly compliant.**

What a cold viewer got. Frames 0–98 (`W000151..W000165`, master f1328..f1427): *"what did
that second stay actually cost her, and who gets paid to stop it?"* Two questions, three
pronouns with no antecedent — "that second stay", "her", "it" — and no hotel, booking site or
commission named in speech. The orientation was carried entirely by one overlay,
"Same guest. Second commission.", which the proof card then **repeated verbatim as its own
headline** on a second track at frames 99–188.

What resolved. Frames 99–188 (`W000089..W000101`, master f780..f870): *"And she pays the site
the same commission she paid the first time."* That is a real bounded fact, which is why the
copy pass read 01 as partial rather than a fail. But it stopped mid-thought: the sentence that
completes it, `W000102..W000109` *"For a guest she already knows by name."*, was outside the
cut, and the Short then closed on an absence (`W000140..W000149`, *"I couldn't find anyone
selling it who'd done that arithmetic."*) followed by the cost question asked a second time on
the end card. A viewer was asked what the second stay cost, twice, and never told.

**Re-cut.** The proof beat extends from master f870 to **f948** — one sentence,
`W000102..W000109`. The payoff now resolves out loud: the second booking costs the inn the
same commission as the first, *on a guest the inn already had*. The out point is in measured
silence: the word ends at f940.1, f944 measures −72.3 dBFS and f948 −76.1 dBFS, and the next
word `W000110` begins at f973.4. Presenter picture is unchanged (seg009 native 121..220 and
13..93, same 760×1080 crop at x570).

**r4: compliant.** Hook question → resolved fact with its completing clause → the verified
absence → a card that states the fact.

**The cost.** Presenter share of speech falls from **0.665 to 0.516**. The Short still opens
and closes on the presenter and the presenter still carries the majority of the speech, but the
proof insert is now 7.0 s and is the longest single beat. That is a direction trade against
"avatar forward … use short proof inserts only where they add information"
(`EP009-SHORTS-003/DIRECTION.md`), and it is the one judgment in this pass the owner may want
to return. The alternative — dropping the added sentence — keeps 0.665 but leaves the payoff
stopping mid-thought.

## Short 02 — cheap parts, and a job still left to sell

**r3: failed cold-viewer context; payoff was already sound.**

The r3 cut opened on `W001024..W001038` (master f8790..f8883): *"If the parts to fix this are
cheap, why doesn't the inn just do it?"* — "this", "the parts", "the inn", none introduced.
Frames 93–216 then showed a Node-RED graph. A cold viewer four seconds in had an automation
diagram and an overlay reading "Why pay for cheap tools?", which pointed the question at the
viewer's wallet rather than at the inn. Nothing in the Short said *small hotel*, *returning
guest*, *direct booking* or *commission*. That is the kill-list item "no cold-viewer context".

The payoff was fine: `W000646..W000666` (master f5360..f5516) resolves the distinction — the
drafting is cheap, the job around it is what can be sold, and its price is capped by what it
recovers.

**Re-cut.** A presenter orientation beat is added in front: master **f1687..f1842**, seg012
native 0..155, `W000195..W000216` — *"It helps a small hotel get its returning guests to book
direct, instead of paying a booking site to meet them again."* This is the only passage in the
locked narration that names the whole situation in one breath *and* has accepted presenter
coverage (seg012 covers output frames 1687..2030). The out point f1842 sits in the gap after
"again." — audible content decays by f1840, f1842 measures −41.9 dBFS, and "By" begins at
f1843.9. It is a three-frame gap and the tightest join in the package.

**r4: compliant.** Presenter share of speech *rises* from 0.668 to **0.765**.

**The weakness.** The added beat still opens on an unresolved pronoun: "**It** helps a small
hotel…". The on-screen line "A direct-booking practice" (25 chars) supplies the referent, which
means the first two words lean on the design. The topic itself — small hotel, returning guests,
direct booking, booking-site commission — is entirely in the speech, so the rubric's
"must not need the caption to understand the context" is satisfied for the *topic*; the
*pronoun* is not. There is no locked alternative that fixes this without generating speech.

## Short 03 — the booking site keeps the guest's email

**r3: failed. This is the Short the owner ruled on.**

Sixteen seconds, three stacked questions, nothing resolved:

| short time | words | line |
|---|---|---|
| 0.06–3.38 | `W000538..W000547` | The site introduces the guest and keeps the guest's email. |
| 3.83–8.98 | `W000548..W000568` | When that guest comes back, who at the inn is paid to make sure the second booking comes to the inn? |
| 9.79–14.09 | `W000569..W000583` | And if the answer is nobody, can somebody from outside get paid to do it? |

Then an end card reading "Who owns the second booking?" — the question the speech had asked
4.3 seconds earlier. And the answer was one word past the out point: the r3
`source-contract.json` recorded `next_word_excluded: W000584 "Nobody"`, cut at 201.833 s.

**Re-cut, per the ruling.** The cut extends from master f4844 to **f4890**, taking
`W000584..W000588` — *"Nobody at the inn is."* The sentence ends at f4880.4, f4890 measures
−65.8 dBFS, and the next word `W000589` "And" begins at f4895.8. The interrogative end card is
gone; in its place an answer card states "Nobody at the inn is." and reveals as the line is
spoken, with the routing copy arriving afterwards in silence.

**r4: compliant.** The payoff and the last spoken line are the same sentence, which is the
honest shape here: this Short's narrow answer *is* its ending.

**The weakness, stated plainly.** The answer beat has **no presenter picture**. seg019's
look-transfer coverage ends at output frame 4844 and seg019b's native runs out at global 4851,
so master 4851..4890 has no lip-synced frames and none were generated. Timeline frames 334–380
therefore carry the spoken answer under a designed card — the `silent_graphic` picture/audio
mode already accepted in this revision's Short 01 proof insert — and the Short's presenter
picture ends 1.9 s before its speech does. An owner who wants the answer *on the presenter's
face* needs a new recording; that is a deferred item, not something this pass can fix.

Two further notes. Timeline frames 334–335 carry only the brand mark on pine before the
headline reveals: a two-frame stillness before the answer, deliberate. And the answer line is
**not** railed as a burned-in caption while the card carries those exact words — that would be
the edit kill-list item "caption text duplicating a quote card verbatim while the card is up".
It is present in `captions.srt` and `captions.vtt`.

## Short 04 — the commission total is the wrong number

**r3: compliant on the cut. Not re-cut.**

Frame one names the wrong number on screen ("TOTAL BOOKING-SITE COMMISSIONS") and the spoken
correction lands on it at 1.125 s ("≠ Recoverable opportunity"). `W001447..W001475` (master
f12495..f12696) delivers the correction — the inn is never going to move all of it, it needs
the sites, the real question is what a recovery service can shift — and `W001305..W001322`
(master f11307..f11449) resolves it: the inn can only pay what the job recovers. That is one
bounded answer, resolved inside, with 0.982 of the speech on the presenter. Nothing in the
locked material improves it.

**Changed anyway.** The end card (interrogative → declarative, gaining 6 frames so the longer
headline holds), and the price-boundary overlay "Capped by what it recovers" added at 9.54 s on
the spoken "what the job recovers" — the r3 constraint beat carried no overlay at all for 5.7 s.
Audio now comes from the locked narration WAV by sample boundary; r3 pulled it from the carrier
MP4's audio track. Same content, auditable fingerprint, and it is what makes the correlation
check in `VERIFICATION.json` meaningful.

**The weakness.** "It's the wrong number" only has a referent because the design puts the
number on screen. The speech alone never names a small hotel. This is the Short most dependent
on its frame-one design, and the one whose compliance would break first if the overlay were
cut.

---

## What no one here can judge

- Perceptual lip sync on every presenter beat. The picture slices are the accepted r3 native
  frames with no retime, but that is an argument from provenance, not a measurement.
- Whether a cold viewer actually leaves with the payoff. `shorts_contract.py` validates
  declared fields and exact-copy order; it cannot validate comprehension. That is the human
  isolation review the validator's own docstring points at.
- Physical-phone playback. Verified in a browser at 390×844 only.
- Short 01's presenter-share trade. Recorded above as an owner question, not resolved here.
