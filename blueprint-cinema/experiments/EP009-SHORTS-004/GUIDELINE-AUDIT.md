# EP009-SHORTS-004 audited against the locked shorts guidelines

Owner finding, 2026-10-08: "These aren't following the new guidelines for shorts."

This is the audit. It reads the actual guideline sources rather than the r4 pass's own
self-report, and it finds the r4 pass judged itself against the wrong document.

## What the r4 pass measured itself against

`STANDARD-JUDGMENT.md` cites exactly one authority: the `docs/content-rubric.md` Shorts
addendum. That addendum is a true constraint but it is the *eval gate* — the machine-checkable
floor. The r4 pass treated passing the gate as satisfying the standard, replaced four end
cards, extended one beat by one sentence, and shipped.

## What the guidelines actually are

The governing standard is the owner-locked EP007 standalone-Shorts decision, which the owner
closed with "Yes lock the scripts and update the gate" and "Make sure to save the decisions and
update the skills based on these shorts chats" — i.e. explicitly portable, not EP007-local.

Sources, in authority order:

| Source | What it binds |
|---|---|
| `EP007/review/decisions/ep007-four-standalone-scripts-owner-lock-20260921.json` | the ten ordered owner messages and the bounded contract |
| `EP007/review/decisions/ep007-four-standalone-scripts-v6.json` | the decision event, marked `reuse.kind: conditional_precedent` |
| `studio/originate/exit-readiness-prep/shorts-net-new/STANDALONE-SCRIPTS-V3.md` | the four locked exact scripts, as built evidence of the form |
| `EP007/.../ep007-short01-clean-frame-owner-lock-20260922.json` | "good lock it. **let's do the same for the other videos**" — the picture grammar |
| `.agents/skills/oe-video-direction/references/precedent-index.md` L29, L40-55 | the portable lesson as recorded in the skill |
| `docs/content-rubric.md` Shorts addendum + `shorts_contract.py` | the eval floor only |
| `EP009/review/source-records/2026-09-21-owner-shorts-rulings.json` | EP009 adopts the standalone-payoff standard |

## The root cause

**EP007's accepted Shorts are net-new purpose-written scripts. EP009-SHORTS-004 is a window
cut out of the locked episode narration.** Every other failure below follows from that.

| | EP007 (accepted) | EP009-SHORTS-004 |
|---|---|---|
| Source of words | four scripts written for the Short, owner-locked | non-contiguous sentences lifted from `word-transcript.json` |
| Duration | 43.5 / 45.4 / 39.6 / 48.1 s | 16.7 / 24.3 / 17.2 / 16.5 s |
| Address | second person to the prospective operator ("You can build a service that…") | third person about an inn and "her" |
| Opening job | name the opportunity, then the mechanism | ask a diagnostic question |
| Close | a working tool the viewer can use | an absence ("nobody selling this has published what that is") |

A 16.7-second excerpt physically cannot carry topic context + opportunity framing + authority +
a completed narrow answer. The r4 pass hit this wall and recorded it as a trade-off
(presenter share 0.665 → 0.516 to buy one completing sentence) rather than as the form being
wrong.

## Violation by guideline

### 1. Cold-viewer topic context must be spoken, not overlaid

Owner, twice: *"isnt this jumping into something? whats the context? they edont know that were
building a sales readiness practice or anything"* and *"no we still need the intro - this is the
same issue as before of jumping right into it"*, then *"They all still need to into the topic -
getting a business ready to sell looks like m and a… etc"*.

The committed rubric says it in writing: *"The viewer must not need the caption … to understand
the context."*

- **01** opens *"what did that second stay actually cost her, and who gets paid to stop it?"* —
  lowercase mid-sentence, three pronouns with no antecedent. `STANDARD-JUDGMENT.md` admits the
  orientation "was carried entirely by one overlay." r4 did not fix this; it only changed the
  end card.
- **02** opens *"It helps a small hotel get its returning guests to book direct"* — "It" has no
  referent. The r4 report concedes this.
- **04** opens *"It's the wrong number, because the inn is never going to move all of it."* —
  two unbound pronouns and a number never stated.
- **03** is the only one whose first line stands alone.

Not one of the four names a direct-booking practice as a buildable service in its opening
speech. **Fails. 01, 02, 04 hard; 03 partially.**

### 2. Conversational, aspirational invitation — not a diagnostic being administered

Owner: *"I think it has to be more curiousity and aspirational up beat. How do you help someone
sell their business? Or helping someone sell their business is a big opportunity. We have to
bring people in like a conversation."*

All four EP009 Shorts open on an interrogative about a cost or a wrong number. This is the exact
register the owner rejected on EP007 and had to reject twice. **Fails, all four.**

### 3. Authority — "you can build a business like this"

Owner: *"exploring feels like it's… It has to be like you can build a business like this. More
authority."* The lock's bounded reading: the host may state with authority that the service is
buildable, while demand and pricing stay open.

EP009 inverts it. The *unresolved* parts are stated with confidence and the buildable service is
left implicit:

- 01 closes *"I couldn't find anyone selling it who'd done that arithmetic."*
- 02 closes *"and what it recovers is a number."*
- 03 closes *"Nobody at the inn is."*
- 04 closes *"and nobody selling this has published what that is."*

Four Shorts, four closes on an absence. **Fails, all four.**

### 4. One complete narrow answer the viewer can act on

EP007's payoffs are instruments: make a dependency map; distinguish preparation from
transaction work and see the engagement boundary; a fixed-fee model plus the right legal check;
a broker interview script with an interpretation rule.

EP009's payoffs are observations about someone else's inn — a second commission is charged, the
site holds the email, the total is the wrong target. True, sourced, and nothing the viewer can
do. **Fails, all four.**

### 5. Coherent as spoken, end to end

03's `spoken_copy` stitches: *"…who at the inn is paid to make sure the second booking comes to
the inn? And if the answer is nobody, can somebody from outside get paid to do it? Nobody at the
inn is."* The payoff answers the first question but is spoken immediately after the second, so it
plays as answering "can somebody from outside get paid?" with "Nobody at the inn is." The
`last_line` and `payoff_line` fields are identical, which is how the contract validator missed
it. **Fails on 03.** 01 has the same class of seam: *"…who gets paid to stop it? And she pays the
site…"* joins a question to an `And` clause from elsewhere in the episode.

### 6. Picture grammar: presenter → full-screen working screens → presenter

Owner on EP007 Short 01: *"i dont think my face has to be there through the whole thing. the
previews cut to screens which i tihnk made sense"*, then after the revision *"good lock it.
let's do the same for the other videos"*, plus *"do we need the heading through the whole thing?
do we want to make it seem more natural less produced"* → the clean-frame lock.

`EP009-SHORTS-003/DIRECTION.md` directs the opposite: *"keep the face large… use short proof
inserts only where they add information, and return to the presenter before the episode
question."* r4 then treats the screen insert growing to 7.0 s as a regression to flag.

**Conflict, not a clean failure.** EP009 has its own owner record —
`2026-09-20-owner-avatar-forward-shorts.json`, *"lets rework this. avatar forward like cleo
abrams"* — dated two days before the EP007 clean-frame lock. These are reconcilable (the
presenter still opens and closes in the EP007 grammar) but EP009's direction document reads
avatar-forward as "face large throughout," which the EP007 lock had already moved away from.
**Owner call required.** Flagged, not assumed.

### 7. The ~2 s declarative full-episode end bridge

EP007 locked a 2.0 s visual-only card after the payoff completes — BUILD THE FULL PRACTICE /
SCOPE IT · PRICE IT · TEST IT / WATCH THE FULL EPISODE — carried in on the existing oxide
bracket, no dissolve.

r4 replaced EP009's interrogative end cards with declarative ones, which is the right direction
and the one real improvement in the pass. It is not the locked bridge form. **Partial.**

### 8. Episode link must not have been the carrier of the answer

`episode_extension` on all four is now genuinely additive (the four modeled inputs, the partner
terms, the computed cap). This is the part of the standard r4 did satisfy. **Passes.**

## Verdict

Eight guidelines. Five hard failures on all four Shorts, one hard failure on 03 specifically,
one conflict needing an owner call, one pass.

The r4 cuts are not repairable by re-cutting. Guidelines 1 through 4 require words that are not
in the locked episode narration — a cold-viewer topic intro, an opportunity invitation, an
authority statement, and an actionable instrument. Carving a different window out of EP009's
master cannot produce them, which is why three successive EP009 revisions have each fixed the
symptom at the end card and left the opening intact.

EP007's answer to the same problem was to stop deriving and write four net-new scripts. That is
the precedent the owner locked and asked to be carried forward, and it is what EP009 has not
done.

## What a compliant EP009 pass requires

1. Four net-new exact scripts, written to the EP007 form: second person to the prospective
   operator, the direct-booking practice named as buildable in the first lines, one working
   instrument delivered, adjacent unknowns left honestly open. ~40-48 s each. Owner script lock
   before any production, per the EP007 sequence.
2. Fresh narration — the words do not exist in the locked master, so the `n3-two-stage-acted-
   guide-v2` chain runs again. Provider spend, needs authorization.
3. Presenter performance matched to the new words. Also provider spend. The accepted EP009
   chambray look (`presenter-regen/look/LOOK-LOCK.json`) carries over.
4. Picture grammar resolved per guideline 6 before storyboard.
5. The 2 s declarative bridge, with Related Video still unbound — EP009's slug is
   `direct-booking-practice` and no `launch/links.json` exists yet, so `[EPISODE_URL]` stays a
   placeholder.

Steps 2 and 3 are paid and are not covered by any current authorization. Nothing here is owner
acceptance; EP009-SHORTS-004 remains unaccepted and unpublished.

No em dashes in this document.
