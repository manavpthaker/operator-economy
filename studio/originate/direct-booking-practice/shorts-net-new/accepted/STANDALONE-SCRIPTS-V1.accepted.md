# EP009 standalone Shorts: net-new scripts V1 (proposed, not locked)

Episode: EP009, a direct-booking practice. Slug `direct-booking-practice`.

Status: **agent proposal awaiting owner script lock.** Nothing here is approved copy, claim
clearance, narration authorization or provider spend. The EP007 sequence is the model: the owner
locks the exact words first, then narration and performance are separately gated.

## The form these follow

Built to the owner-locked EP007 standalone contract
(`ep007-four-standalone-scripts-v6`, owner lock
`ep007-four-standalone-scripts-owner-lock-20260921.json`), carried forward per
`GUIDELINE-AUDIT.md` in `blueprint-cinema/experiments/EP009-SHORTS-004/`:

- Line one names the buildable practice and the topic, so a cold viewer is oriented in speech,
  not by an overlay.
- The register is a conversational invitation into an opportunity, not a diagnostic being
  administered.
- Authority sits on what can be built and how to begin. Demand, pricing, channel behavior and
  legal status stay bounded unknowns.
- Each Short completes one narrow answer and hands the viewer an instrument they can use before
  they talk to anyone.
- The episode adds breadth, economics and falsifiers. It never supplies a withheld answer.
- Each must survive the strip test: remove every episode cue, CTA, caption, comment and series
  reference, and the topic, mechanism and conclusion still stand.

Every mechanism below is taken from the locked EP009 editorial, not invented here. Claim IDs
reference `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/claims-map.md`.
Hedges marked **required** are the claims map's own attribution conditions and may not be dropped
in performance.

## Runtime and gate status

Word counts are the spoken copy only. Two pace estimates, because the right one is not yet
measured for this material: the EP007 accepted Shorts ran at 2.54 words a second, and EP009's own
locked long-form runs at 2.76.

| # | Title | Words | At EP007 pace | At EP009 pace |
|---|---|---|---|---|
| 1 | Book Your Own Room | 125 | 49.3 s | 45.4 s |
| 2 | It Sounds Like Marketing. It's Operations. | 134 | 52.8 s | 48.6 s |
| 3 | The Guest Book | 135 | 53.2 s | 49.0 s |
| 4 | Four Numbers | 138 | 54.4 s | 50.1 s |

EP007's accepted four ran 43.5, 45.4, 39.6 and 48.1 seconds. These sit at or slightly above that
band at the slower pace and inside it at the faster one. If you want them shorter, Short 3 is the
one that cannot easily give: the Booking.com partner-help attribution is 36 words and C007 requires
it in full. Shorts 2 and 4 can each lose a sentence without losing the instrument. Say the word and
I will cut rather than guess.

Machine-readable form: `STANDALONE-SCRIPTS-V1.json`, which passes
`studio/scripts/originate/shorts_contract.py --mode direct`, with and without
`--require-pinned-comment`. The `payoff_line` anchors in that file are set deliberately per script
rather than taken positionally, because the penultimate sentence is not the payoff in Shorts 3 and
4. Positional extraction is how EP009-SHORTS-004's Short 03 passed the gate while answering the
wrong question.

A passing contract check is not the standard. It confirms the declared fields and the exact-phrase
relationships. Whether a cold viewer actually leaves with the answer is the human strip test below.

## The strip test

Remove the title, caption, pinned comment, end card, Related Video and any series reference. What
survives, read aloud:

| # | Topic a cold viewer has | Instrument they leave with | Honest unknown left standing |
|---|---|---|---|
| 1 | a small hotel pays a site to meet its own returning guests | the guest-side phone test, runnable tonight | whether the owner pays to fix it |
| 2 | that recovery work is operations, not marketing | what the job actually is and where its edge sits | whether an owner buys it from outside |
| 3 | the site holds the guest's contact behind an alias | build the property's own consented guest book | consent rates, and per-site terms |
| 4 | the commission total is not the addressable amount | the four-input ceiling, and the fee sitting under it | the retainer price, and whether anyone says yes |

Each row's instrument is usable without the episode. Each unknown is named in the Short rather
than deferred to it.

## 1. Book Your Own Room

> You can build a practice that helps a small hotel get its returning guests to book direct,
> instead of paying a booking site to meet them again.
>
> You can run the first piece tonight, on your phone.
>
> Pick an independent property near you, twenty to forty rooms. Search for it the way a guest
> would. Does a free link to the hotel's own site show up beside the site rates? Google shows one
> for a property connected through a partner, and charges nothing for it.
>
> Compare the direct rate to the site's. Try to finish a direct booking yourself.
>
> Whatever breaks is your finding. Not findable, not bookable, or a direct rate that costs the
> guest more.
>
> Ten minutes, and you have half an audit.

Standalone payoff: the viewer can run the findable-and-bookable half of a direct-booking audit on
any property tonight, from the guest side, and read the result.

Instrument source: the audit's phone side test, `01-editorial/script.md` S14 ("test the direct
path as a guest, on your phone") and the three jobs at S12.

Claims: C009, C022.
Required hedges: "connected through a partner" (C009 forbids implying every small property is
eligible without one).
Left open: whether the owner will pay to fix what the test finds.

## 2. It Sounds Like Marketing. It's Operations.

> You can build a service that gets a small hotel's returning guests to book direct, instead of
> paying a booking site to meet them again. It sounds like marketing. The work is operations.
>
> At a twenty room inn, the person who would write the thank you is the one checking in a guest and
> finding a plumber. The direct path is not a system, it is a list of small jobs, and the list
> belongs to nobody.
>
> The drafting got cheap. A language model writes the message, an automation tool schedules it. The
> judgment did not: who gets one, and what you tell the owner.
>
> So the qualification is not hotel marketing. It is owning a list of small recurring jobs in a
> business you do not own. Rates and revenue management stay outside.

Standalone payoff: the viewer can tell this work apart from hotel marketing, locate the actual
skill it needs, and see the engagement boundary that keeps it small enough to sell.

Instrument source: the front-desk obstacle at `script.md` S10 ("it's a list of small jobs, and
the list belongs to nobody"), the retained-judgment list in the editorial contract, and the
three-jobs scope at S12.

Claims: C013, C023, C022.
Required hedges: C023 is a capability, not an outcome. The script must not imply that the
language model moves direct share. The staffing-shortage line, if performed, must name the
American Hotel and Lodging Association.
Left open: whether an owner in the band buys an outside operator for it.

## 3. The Guest Book

> You can build a direct-booking practice for small hotels. Get one constraint right before you
> pick a tool.
>
> Booking.com's own partner help says it does not share private guest email addresses. Both sides
> see an alias ending at guest dot booking dot com, and partners are asked to keep the conversation
> on the platform.
>
> So you cannot win a guest back from a relay address, and you are not supposed to try.
>
> What the inn needs first is not an email tool. It is a guest book of its own, at the front desk,
> that the guest chooses to sign. The registration card and the wifi login ask for the guest's own
> email.
>
> That list runs under the American email law, and European rules for European guests. Check your
> jurisdiction. This is not legal advice.

Standalone payoff: the viewer learns the constraint that shapes the whole service, where a
workable guest list actually comes from, and the correct next legal check.

Instrument source: `script.md` S07 ("What the inn needs first isn't an email tool. It's a guest
book of its own, at the front desk, that the guest chooses to sign") and S12 ("The registration
card and the wifi login ask for the guest's own email").

Claims: C007, C026.
Required hedges: attribute to "Booking.com's own partner help". C007 forbids implying the site
hides data for commercial motive. The legal line is a jurisdiction check, never advice.
Left open: consent rates, and what an outside operator may do with the list under each site's
terms.

## 4. Four Numbers

> You can build a direct-booking practice, and price it honestly off four numbers you ask the owner
> for.
>
> Rooms. Average nightly rate. Occupancy. And the share of bookings arriving through the sites.
>
> That gives you the revenue the sites carry. Apply a commission band and you have the annual cost.
>
> Then assume a shift in the mix, and say out loud that the size of that shift is a hypothesis
> nobody has measured. Subtract what running direct costs. What is left is the recoverable amount,
> a month.
>
> That is the ceiling, and your fee lives under it. On an illustrative twenty room inn at a hundred
> and eighty a night and seventy percent occupancy, it lands near a thousand to fourteen hundred
> dollars a month.
>
> Some properties cannot fund this. The arithmetic tells you which, before you quote.

Standalone payoff: the viewer can compute a property's recoverable ceiling from four inputs and
knows their fee has to sit under it, including when the answer is that this property cannot fund
the work.

Instrument source: the episode's own stated promise at `script.md` S01 ("take four numbers from a
small property and know what it can honestly pay for the job"), the S13 model, and the S14 audit
recommendation including "not this property".

Claims: C016, C017, C018, C019, C020, C022.
Required hedges: "illustrative" plus the four inputs (C016). The mix shift must be spoken as a
hypothesis nobody has measured (C019). The commission band is deliberately unquantified here; if
a figure is added it becomes C018 and must carry "my assumption from the reported bands". The
ceiling wording "a thousand to fourteen hundred dollars a month" is the claims map's own approved
spoken form of C020.
Left open: the retainer price, the audit fee, and whether any owner says yes.

## What these four deliberately do not do

- No spoken episode CTA. Routing is additive metadata, per the EP007 lock.
- No commission percentage attributed to Booking.com (C004's prohibited inference).
- No claim that the practice is an existing market or that buyers recognise it (naming-registry
  prohibited inference).
- No income figure, no earnings framing, and no implication that the modeled economics are
  achieved results.
- No reuse of EP009's locked long-form narration. These are net-new words and will need their own
  narration pass.

## Fifth candidate, not written as a Short here

The broker-equivalent channel test has strong support and would fill the EP007 "Test the Front
Door" slot: call two agencies selling direct-booking work and ask what their smallest retained
property is, against one agency's published fifteen hundred dollar a month entry price, with most
quoting privately. That is C011, C012, C027 and the C034 kill condition. It is the natural fifth
if you want one, or a swap for any of the four above. Flagged rather than written, because four
were asked for.

## Production consequences if these are locked

1. Fresh narration. None of these words exist in the locked master, so the
   `n3-two-stage-acted-guide-v2` chain runs again. Paid, unauthorized.
2. Presenter performance matched to the new words. Paid, unauthorized. The accepted EP009 chambray
   look in `blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-regen/look/LOOK-LOCK.json`
   carries over.
3. Picture grammar needs the owner call flagged in `GUIDELINE-AUDIT.md` guideline 6, before
   storyboard: EP007's locked presenter-to-screens-to-presenter against EP009's avatar-forward
   direction.
4. Related Video stays unbound. There is no `launch/links.json` for `direct-booking-practice`, so
   `[EPISODE_URL]` remains a placeholder.

No em dashes in this document.
