# EP009 Shorts: copy package

Written 2026-09-21. Copy only. No cut was changed, no provider was called, nothing was spent,
nothing was committed. Status: **draft for owner review.** Owner creative acceptance of the four
r3 cuts is still outstanding (`REVIEW-PACKAGE.json`, `owner_approved: false` on all four), and this
package does not change that.

Standard applied: `content-os/AGENTS.md`, `editorial-checklist.md`, `facts.md` (including Do not
state and UNRESOLVED), `voice.md`, `rubric.md` (`operator_economy` register profile, Family O
routing for OE video), `strategy/portfolio-charter.md`, `strategy/editorial-system.md`, `flow.md`;
plus `operator-economy/docs/content-rubric.md`, `docs/kill-criteria.md`,
`docs/packaging-process.md`, `docs/growth-strategy.md`, and the EP009 claims map and Step 0
promotion record.

Register: **Operator Economy documentary.** Not Manav's first-person signed register. The page is
not a person, so there is no personal anchor by quota and no performed voice.

---

## Two dependencies that gate this copy

**1. There is no EP009 URL, and there must not be one yet.**

EP009 has no slug and no launch record of its own. The slug `direct-booking-recovery` already
belongs to the **live August EP006 episode**, whose real URL is recorded in that episode's own
`launch/links.json` and is deliberately not restated here: `content-os/AGENTS.md` hard rule 3 says
prose references an episode URL and never originates one. No copy below may resolve to, reuse, or
be "helpfully completed" with that existing EP006 URL. Every reference is the literal placeholder
`[EPISODE_URL]`, and only `studio/originate/<slug>/launch/links.json` may ever originate the real
one; the launch gate renders it. This is `content-os/AGENTS.md` hard rule 3 and it exists because
on 2026-08-03 a video ID written nine hours before the upload ran shipped into every LinkedIn post
for an episode that did not exist.

**2. The pinned comment has to carry a clickable URL, not a routing phrase.**

`facts.md` records the finding verbatim: **"403 short views produced 3 episode views."** The cause
was EP002's pinned comments saying "link in bio" with no clickable URL. The superseded r2 draft at
`EP009-SHORTS-002/PUBLICATION-DRAFT.json` repeated that exact mistake on all four Shorts ("Open the
related video", no link). So every pinned comment below **opens on the URL, on its own line,**
before any prose. If the launch gate has not filled `[EPISODE_URL]`, the comment does not post.

---

## A standard conflict the owner has to rule on

`docs/content-rubric.md` says two different things depending on whether you read the commit or the
disk.

| | Committed at HEAD | Working tree, uncommitted |
|---|---|---|
| Shorts must | end on a `cliffhanger_line` | declare `cold_viewer_context` and resolve a `standalone_payoff` |
| Kill-list item | "Shorts with ... complete answers (cliffhanger Shorts convert 3 to 5x better)" | "Shorts with ... no cold-viewer context, or no standalone narrow payoff" |
| `cliffhanger_line` | required | **"retired and does not satisfy the gate"** |

The four r3 cuts were directed to the committed standard: `DIRECTION.md` says "Withhold the
calculation" for 01, 02 and 04 and "Withhold the service design" for 03. Under the working-tree
standard, a Short that withholds its own answer fails. Copy cannot reconcile that. Each Short below
carries a **kill check against both readings**, and I have not smoothed either one into a pass. The
machine gate that would decide this, `studio/scripts/originate/shorts_contract.py`, never consults
`cliffhanger_line` at all.

---

## On-screen text: the design budget

**Maximum 32 characters per line.** Measured, not guessed: the longest legible overlay already in
the r3 cuts is 30 characters ("Same guest. Second commission." and "TOTAL BOOKING-SITE
COMMISSIONS"), verified by pulling frames at phone width. Small-type source labels and the
disclosure line in 02 run longer by design and are not hook lines.

Each line below is marked **keep** (already in the cut at those seconds), **replace**, or **add**.
Replace and add are copy specifications. Applying them is a composition rebuild, which is out of
scope here.

---

# Short 01: the second commission

**13.46 s.** Presenter question, proof card, presenter on the missing arithmetic.

### Title

**When the guest returns, the commission does too** (47 characters)

Shape: temporal clause, then the consequence. Curiosity comes from the mechanic itself, not from a
withheld promise, and the episode pays it off.

### On screen

| Seconds | Line | Chars | Action |
|---|---|---|---|
| 0.000 to 4.125 | Same guest. Second commission. | 30 | keep |
| 4.125 to 7.875 | Booked again. Billed again. | 27 | **replace** |
| 4.125 to 7.875 | Illustrative small-inn story | 28 | keep (required boundary) |
| 7.875 to 11.208 | The missing arithmetic. | 23 | keep |

The opening line is the hook and it already works: a cold viewer has "guest" and "commission"
before a word is spoken. The replacement at 4.125 fixes a duplication. Right now the proof card's
headline repeats the opening line verbatim on a second track, which spends the one new surface in
the Short on something already on screen. "Booked again. Billed again." traces the repeat charge
instead. The footer stays: the inn is modeled, and the copy says so.

### Cliffhanger

Spoken, ending at 11.11 s: **"I couldn't find anyone selling it who'd done that arithmetic."**
Reinforced by the existing end card, "What could the inn actually pay? The calculation in EP009."

**Strong enough: yes.** The withheld object is one specific computable number, and the absence it
rests on is the episode's own verified finding (C022, "I could not find"). No change needed.

### Pinned comment

```
[EPISODE_URL]

The arithmetic this Short stops short of: the inn's four modeled inputs, the reported commission
band, and the ceiling that caps what an outside operator could charge for the work. Commission
mechanics are from Booking.com's own partner help, which says commission is a set percentage of
the whole booking, charged at checkout.
```

### Description

```
A small inn takes a booking through a booking site, pays commission, and then the same guest books
the same way again.
Commission is charged per booking, so the second stay costs the inn what the first one did.
Booking.com's own partner help describes that mechanic.
Nobody selling a fix for it has published the arithmetic. EP009 runs it on an illustrative 20-room
inn.
Full episode: [EPISODE_URL]
```

**Hashtags: none.** See the note at the end; no OE packaging document supports them.

### Kill-criteria check

Does it answer its own question completely? **No.** Committed standard: **pass.** Working-tree
standard: **partial**, because the Short does deliver one bounded fact inside itself, that
commission recurs per booking, even though it withholds the arithmetic.

Must stay withheld: the net recoverable ceiling (C020, about $996 to $1,418 a month at the modeled
inn); any commission dollar figure or percentage band (C017, C018), which cannot carry its four
inputs and the word "illustrative" inside 13 seconds; the audit fee and retainer (C024, C028); and
any commission saved, direct share gained, or earnings figure.

Claims cited: C004, C016, C022.

---

# Short 02: cheap tools

**17.79 s.** Presenter question, real drafting-tool proof, presenter on recovered value.

### Title

**Cheap parts, and a job still left to sell** (41 characters)

Shape: paired noun phrase on a comma pivot. Matches the cut's own opening words.

### On screen

| Seconds | Line | Chars | Action |
|---|---|---|---|
| 0.000 to 3.875 | Cheap parts. The job isn't. | 27 | **replace** |
| 3.875 to 9.042 | The tool can draft. | 19 | keep |
| 3.875 to 9.042 | Node-RED + OpenAI · recorded workflow | 37 | keep (source label, small type) |
| 3.875 to 9.042 | Fictional guest. Awaiting human review. No sending available. | 61 | keep (disclosure, do not trim) |
| 11.358 to 13.178 | Priced to what it recovers | 26 | **add** |

The cut currently opens on "Why pay for cheap tools?", which points the question at the viewer's
wallet. The spoken line asks something else: why the inn does not just do it itself. The
replacement matches the speech.

The added line at 11.358 lands on the spoken "But only for what it recovers." That 6.5 second
presenter return currently carries no overlay at all, and this is the load-bearing boundary: the
price is capped by the recoverable amount. Without it, "it can be sold from outside" drifts toward
an earnings claim.

### Cliffhanger

Spoken, ending at 15.38 s: **"and what it recovers is a number."** Reinforced by the existing end
card, "What work would an inn pay for? The service and the calculation in the full episode."

**Strong enough: yes, and it is the best of the four.** It names the withheld object exactly, after
the Short has already handed over something usable: the drafting is cheap, the sellable work is the
judgment around it, and the price is capped by what it recovers.

### Pinned comment

```
[EPISODE_URL]

The drafting step you are watching is Node-RED calling a language model on a fictional guest, with
nothing sent. The full episode builds the rest of the job around it and prices the retainer against
the recoverable amount rather than the commission total.
```

### Description

```
The parts of a post-stay follow-up are cheap. A language model drafts the thank you and the review
request; an automation tool schedules them.
The screen recording is that drafting step running in Node-RED, on a fictional guest, with nothing
sent and every draft awaiting human review.
So the question is what work is left for an outside operator to sell, and what caps its price.
EP009 works that out.
Full episode: [EPISODE_URL]
```

**Hashtags: none.**

### Kill-criteria check

Does it answer its own question completely? **No.** Committed standard: **pass.** Working-tree
standard: **pass.** This is the one Short that satisfies both readings: it delivers a bounded
distinction inside itself and still withholds the number.

Must stay withheld: the recoverable ceiling and the retainer (C020, C028); tool pricing (C010),
which at this length would read as the cost of the business rather than as public tool pricing; and
any claim that the language model moves direct share, since C023 is a capability, not an outcome.

Claims cited: C020, C022, C023.

---

# Short 03: the guest relationship

**16.17 s.** Presenter carries the causal question with brief relationship overlays.

### Title

**The booking site keeps the guest's email** (40 characters)

Shape: flat declarative mechanic, verified at source (C007).

An earlier draft titled this one "Who at the inn owns the second booking?" I rejected it. The
`operator_economy` profile in `content-os/rubric.md` fails questions used as hooks, and the Short's
own end card already asks that question. A declarative title also had to stay inside the claims
map: "Nobody at the inn owns the second booking" would assert as fact something C022 only supports
as an absence in the operator market, not as a staffing fact about properties.

### On screen

| Seconds | Line | Chars | Action |
|---|---|---|---|
| 0.000 to 2.500 | A small inn. A repeat guest. | 28 | **add** |
| 0.083 to 3.583 | Booking site → Guest's email | 28 | keep (relationship cue) |
| 5.250 to 9.350 | Returning guest → The inn? | 26 | keep |

This cut has **no hook line at all** in the first three seconds. The only element is a two-word
relationship diagram, so a cold viewer gets no subject until speech arrives, and
`docs/content-rubric.md` wants a cold viewer oriented immediately. The added line supplies the
missing context without restating the caption below it or the end card above the fold.

It deliberately says "a small inn" rather than "a 20-room inn": the room count is a modeled input
(C016) and on screen, stripped of "illustrative" and its three companion inputs, it would read as a
factual property.

### Cliffhanger

Spoken, ending at 13.92 s: **"can somebody from outside get paid to do it?"** Reinforced by the
existing end card, "Who owns the second booking?"

**Strong enough: no.** All sixteen seconds are three stacked questions and the Short resolves none
of them, so the withheld thing is the entire subject rather than a specific object. The end card
then repeats the question the speech just asked instead of advancing it.

**What to add, and where.** Copy cannot fix this, because the answer is one excluded word away:
`source-contract.json` records `next_word_excluded` as W000584, **"Nobody"**, cut at 201.833 s in
the master. Extending the cut by that single beat would give the Short a resolved fact to stand on
and leave the service design as the withheld object. That is a re-cut decision for the owner, not a
copy change.

If the cut stays exactly as it is, change the end-card headline from "Who owns the second booking?"
to **"Nobody is, yet."** (16 characters) at 13.917 to 16.167 s, so the card advances the thought
rather than echoing it.

### Pinned comment

```
[EPISODE_URL]

Booking.com's own partner help says it does not share private guest email addresses: both sides see
an alias ending @guest.booking.com, and partners are asked to keep the conversation on the
platform. The full episode covers what an outside operator can and cannot legally do with a guest
list under those terms.
```

### Description

```
A guest books a small inn through a booking site. The site introduces the guest and holds the
contact address. Booking.com's partner help says it does not share private email addresses, and
both sides see an alias.
When that guest comes back, nobody at the inn is paid to make sure the second booking comes to the
inn instead.
EP009 asks whether somebody outside the property can be, and what the job is worth.
Full episode: [EPISODE_URL]
```

**Hashtags: none.**

### Kill-criteria check

Does it answer its own question completely? **No, and that is the problem here.** Committed
standard: **pass.** Working-tree standard: **fail**, on the kill-list item "no standalone narrow
payoff." The viewer leaves with a question and no fact. Recorded as a fail, not softened.

Must stay withheld: the service design and the three jobs; the retainer and the recoverable ceiling
(C020, C028); any suggestion that the site hides or sells guest data for commercial motive, since
C007 is a neutral mechanic; and any suggestion that the property should leave the booking sites.

Claims cited: C007, C008, C022.

---

# Short 04: the wrong number

**16.54 s.** Presenter carries the distinction between the total and the recoverable amount.

### Title

**The commission total is the wrong number** (40 characters)

Shape: correction of a number the viewer already has.

### On screen

| Seconds | Line | Chars | Action |
|---|---|---|---|
| 0.000 to 3.625 | TOTAL BOOKING-SITE COMMISSIONS | 30 | keep |
| 1.125 to 3.625 | ≠ Recoverable opportunity | 25 | keep |
| 5.167 to 8.375 | How much can actually shift? | 28 | keep |
| 9.540 to 11.000 | Capped by what it recovers | 26 | **add** |

This is the strongest hook already in the cut, and it needs nothing: the wrong number is named in
frame one and the correction arrives on the spoken "because." The added line at 9.540 lands on
"what the job recovers" and fills the 5.7 second constraint segment, which currently has no
overlay. It is what keeps the affordability point from reading as a price.

### Cliffhanger

Spoken, ending at 14.29 s: **"and nobody selling this has published what that is."** Reinforced by
the existing end card, "What can this inn actually afford? The full calculation in EP009."

**Strong enough: yes.** The Short hands the viewer a correction they can use immediately, that the
commission total is not the addressable amount, then withholds the figure and grounds the
withholding in a verified absence (C022) rather than in a tease.

### Pinned comment

```
[EPISODE_URL]

The full episode runs this on an illustrative inn: 20 rooms, $180 average daily rate, 70 percent
occupancy, and the booking-site share Cloudbeds reports worldwide. It shows why the recoverable
amount, not the commission total, sets what the inn can pay, and what is left after the work.
```

### Description

```
Total booking-site commissions is the easy number to reach for. It is the wrong one, because a
small inn is never going to move all of it. It needs the sites.
The number that matters is what a recovery service can actually shift, and that is what caps what
the inn can pay for the job.
Nobody selling this work has published that figure. EP009 calculates it on an illustrative 20-room
inn.
Full episode: [EPISODE_URL]
```

**Hashtags: none.**

### Kill-criteria check

Does it answer its own question completely? **No.** Committed standard: **pass.** Working-tree
standard: **pass.** The correction is the standalone payoff; the figure is the withheld object.

Must stay withheld: the net recoverable ceiling (C020, about $996 to $1,418 a month), which is the
episode's payoff; the modeled annual commission band (C018, about $104,968 to $128,294), which the
superseded r2 draft published as "$105K to $130K" in a Short description without its four inputs;
the 10-point mix shift (C019), a hypothesis nobody has measured; and any commission saved or direct
share gained stated as a result.

Claims cited: C014, C018, C020, C022.

---

# Cross-Short check

## Four shapes, no repeat

| Short | Title | Shape |
|---|---|---|
| 01 | When the guest returns, the commission does too | temporal clause, then the consequence |
| 02 | Cheap parts, and a job still left to sell | paired noun phrase on a comma pivot |
| 03 | The booking site keeps the guest's email | flat declarative mechanic, verified at source |
| 04 | The commission total is the wrong number | correction of a number the viewer already has |

No two titles share a content word except "commission," which appears in 01 as a recurring charge
and in 04 as a mistaken total. None opens on the same construction. None is a question. None
carries a figure, which is deliberate: a figure in a title that the cut never speaks breaks the
match between copy and picture, and every EP009 figure needs a boundary a title cannot hold.

No hype-lexicon term, no income promise, no superlative about the channel, no em dash, no emoji.

## Publish order: 01, then 04, then 02, then 03

**01 first.** It establishes in thirteen seconds the premise the other three assume, that the
charge repeats per booking. It is the fastest cold-viewer orientation in the set and the only one
whose hook works with the sound off.

**04 second.** Its correction only lands once the viewer accepts that the charge repeats. Run
before 01, "the commission total is the wrong number" corrects a number the viewer has not been
given yet.

**02 third.** The most technical of the four and the best mid-run piece for someone who already has
the premise. It is also the strongest standalone unit, so it is the one to lean on if the run needs
something to carry.

**03 last.** It resolves nothing, so it benefits most from the episode already being live and from
the other three having supplied its context, and it costs least if it underperforms.

## The weakest Short, honestly: 03

Not because the performance is weak. Because of four things:

1. No on-screen hook in the first three seconds. A two-word relationship diagram is not a hook.
2. Sixteen seconds of three stacked questions with no resolved beat. Against the working-tree
   `docs/content-rubric.md` that is the kill-list item "no standalone narrow payoff."
3. The end card repeats the question the speech just asked.
4. The answer is one excluded word away, and that word is already in the master. Which means the
   weakness is a cut decision, cheap to fix, and not mine to make.

If only one of these four gets held back, hold 03.

## Claims I had to drop

| Claim | Value | Why it is not in any Short |
|---|---|---|
| C020 | net recoverable about $996 to $1,418 a month | It is the episode's payoff, it cannot carry its modeled inputs inside a Short, and published bare it reads as commission saved, which the Step 0 promotion record prohibits. |
| C018 | about $104,968 to $128,294 a year all-in | The superseded r2 draft published this as "$105K to $130K" in a Short description without the four inputs. Dropped on exactly those grounds. |
| C001 | 63.4 percent booking-site share | Verified and attributable to Cloudbeds, but none of the four cuts speaks it. Referenced without the number in 04's pinned comment, with Cloudbeds named. |
| C019 | 10-point mix shift | A hypothesis nobody has measured. No Short has room for that boundary. |
| C024, C028 | audit $1,200, retainer $600 to $1,250 | Modeled prices. Stated without the model they read as market rates. |

## Hashtags

**None, on all four, by decision.** No OE packaging document supports hashtags on Shorts.
`docs/content-rubric.md`'s kill list blocks hashtag walls and keyword stuffing, and the
`operator_economy` profile ends on the finding rather than on discovery furniture. Recorded as an
empty array in `COPY-PACKAGE.json` so it reads as a decision, not an omission.

---

# Review record

Reviewer: agent (writer's assessment). **This is not the owner's approval, and it is not a passed
gate.** `content-os/editorial-checklist.md` and the `operator_economy` register profile in
`rubric.md` W.3, applied to the exact copy above.

## Route

`rail`/`format` derive **Family O (`oe_video`)**; desk derives profile **`operator_economy`**. Per
`rubric.md` Family O, Content OS does not rescore an OE Short, so there is no Family W score here
and I did not manufacture one. The shared checklist checks and the register profile do apply, and
`voice.md` sections 2 through 5 are universal.

## Shared checklist

| Check | Finding |
|---|---|
| Rehearsed spontaneity | **Not applicable, by route.** The checklist routes OE page copy to its documentary profile rather than the personal spontaneity check. Recorded so the omission is visible. |
| No specification-like phrasing | **Pass.** Every line names a party and a consequence: the inn pays, the site holds the address, the job is capped. "Recovery service" is retained because it is the cut's own spoken wording; "guest recovery platform" and similar substitutions are prohibited by the claims map and are not used. |
| One useful point | **Pass on 01, 02, 04. Weak on 03.** 01 gives the recurring charge, 02 gives the cheap-parts and expensive-judgment split, 04 gives the total-versus-recoverable correction. 03's useful point is a question, which is the finding recorded above. |
| Truth and scope | **Pass.** `facts.md` read this session, including Do not state and UNRESOLVED. No figure appears in any title or on-screen line. Every figure that survives into a pinned comment carries its boundary: C016's inputs are stated with "illustrative," C001 is named to Cloudbeds without the number, C004 and C007 are attributed to Booking.com's own partner help. No Short states commission saved, direct share gained, a typical fee, earnings, or that a property should leave the booking sites. No `grapevines.ai` URL. |
| Natural language and shape | **Pass.** No em dash anywhere in either output file, verified mechanically. No emoji, no exclamation mark, no banned opener, no hype term, no income-promise construction. Opening words across the four titles are "When," "Cheap," "The," "The"; 03 and 04 share "The," which is within tolerance for four unlike shapes but is the one cadence note worth watching if a fifth Short is added. |

## `operator_economy` profile

| Rule | Finding |
|---|---|
| Open on a verified finding, contradiction, mechanic, or reported scene | **Pass.** 01 mechanic (C004), 02 mechanic (C023), 03 verified-at-source mechanic (C007), 04 contradiction. |
| Questions as hooks fail | **Pass after a correction.** 03's first title was a question and was replaced. Retained here rather than quietly fixed. Note that the cuts themselves open 01 and 02 on spoken questions and 04 carries the on-screen question "How much can actually shift?"; those are locked picture, not this copy, and they are worth the owner's attention when the Shorts go to Family O review. |
| Guru-funnel promises fail | **Pass.** No outcome is promised. Each description ends on the finding or the absence, then the link. |
| Evidence class and confidence legible | **Pass.** "Illustrative," "modeled," "reported," "fictional guest," "awaiting human review," and "nobody has published" all survive into the copy. |
| End on the finding, not an engagement question | **Pass.** No description or pinned comment asks the viewer a question. |
| No first-person founder performance | **Pass.** No "I" in any title, description, or pinned comment. The spoken "I couldn't find anyone" stays in the cut, where it is the host. |

## Checks I could not complete

1. **Family O pass.** `rubric.md` requires authenticated, commit-bound references to the external
   standard, the exact external review result, and evidence that quality review, hard blocks and
   release assets all passed. None of that exists: `owner_approved: false` on all four cuts,
   `published: false`, `related_video_bound: false`. **No `oe_video` pass is claimed.**
2. **`shorts_contract.py`.** Not run. `COPY-PACKAGE.json` is not a `shorts_briefs` or `scripts`
   manifest, and the validator requires a `standalone_payoff` per record. I cannot truthfully
   declare one for 01 or 03, so running it against a synthesized manifest would either fail on
   those two or require me to invent a payoff the cuts do not contain. Recorded as not run rather
   than as a pass.
3. **The cliffhanger-versus-standalone-payoff conflict.** An owner ruling, not a writer's call. The
   package reports both readings per Short.
4. **`cadence.py`.** Not run. `voice.md` section 4b scopes it to a publishable body extracted from
   a package front matter or a `## Script` section; this file is a per-Short copy package and has no
   such body. The cross-piece opener comparison was done by reading instead, and its one finding is
   recorded above.
5. **Phone legibility of the three added and two replaced lines.** Character counts were designed
   against overlays measured in the existing cuts, not rendered. Nothing new has been composited,
   so no line here has been read at 390 by 844.
6. **Conversion.** Unmeasured and unmeasurable from here. The EP002 finding tells us what a missing
   URL costs; it does not tell us what these four will do.

## The decisive finding

The strongest passage in the package is 04's pinned comment, because it is the only one that hands
a cold viewer something genuinely additive (the four modeled inputs and the named vendor source)
without touching the figure the episode exists to deliver. The strongest remaining weakness is
Short 03, which no wording can repair, and which I would hold rather than publish against the
working-tree standard.
