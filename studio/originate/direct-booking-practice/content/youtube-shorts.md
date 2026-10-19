# EP009 Shorts: YouTube publication copy

Status: **drafted 2026-10-12, not owner-approved.** Nothing uploaded, scheduled or published.
No URL is stated. `{{EPISODE_URL}}` resolves only from
`studio/originate/direct-booking-practice/launch/links.json`, which does not exist yet. If the
launch gate has not filled it, the pinned comment does not post.

Internal **EP009**, publishing as public **No. 002**. Slug `direct-booking-practice`.
**Not** `direct-booking-recovery`: that is EP006's and its `links.json` holds live IDs.

Scope: the four owner-locked Shorts in `shorts-net-new/STANDALONE-SCRIPTS-V1.json`, accepted as
assembled 2026-10-09. Claims are limited to the episode's claims map (v0.2, C001-C037) and the
EP009 section of `content-os/facts.md`. Register: Operator Economy documentary. No hashtags, by
decision. No questions as titles. No figures in titles.

## Related Video (all four)

Set **Related Video = the EP009 long-form**, resolved from `links.json` at schedule time, never
typed by hand. Additive routing only: every Short resolves its own answer before any link. If the
long-form is not live when a Short is scheduled, leave Related Video empty and backfill it the day
the episode goes live.

Suggested order: **02, 01, 04, 03.** 02 orients a cold viewer to what the service is. 01 hands them
the first tool. 04 tests whether the business can pay. 03 carries the legal boundary and benefits
most from the other three having established what the practice is.

## AI disclosure (all four)

- **Altered or synthetic content: YES** on every Short, same as the long-form.
- What is synthetic: the narration is an **AI voice clone of the host's own voice** (Google TTS
  performance transferred onto the accepted Original C clone through ElevenLabs Voice Changer), and
  the presenter footage is AI-generated (Seedance 2.5 from the owner-picked still, repaired with
  fal react-1).
- Last line of every description, below the episode line:

```
The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

- On the API upload path, set `containsSyntheticMedia: true`.

---

## Short 01: Book Your Own Room

**Title:** Audit a small hotel's direct booking from the guest side (56 chars)

**Description:**

```
A practice can help a small hotel get its returning guests to book direct, instead of paying a booking site to meet them again. The first piece runs tonight, on a phone.

Pick an independent property near you, twenty to forty rooms, and search for it the way a guest would. Does a free link to the hotel's own site show up beside the site rates? Google shows one for a property connected through a partner, and charges nothing for it. Compare the direct rate to the site's, then try to finish a direct booking yourself.

Whatever breaks is your finding: not findable, not bookable, or a direct rate that costs the guest more. Ten minutes, and you have half an audit.

Full episode, with the other half and what the written recommendation contains: {{EPISODE_URL}}

The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode runs the other half of the audit: the ceiling on the property's own numbers, what the written recommendation contains, and a modeled look at whether one person can make this pay. The model is arithmetic on an invented inn, and the episode says so out loud.
```

---

## Short 02: It Sounds Like Marketing. It's Operations.

**Title:** Getting a small hotel booking direct is operations work (55 chars)

**Description:**

```
A service can get a small hotel's returning guests to book direct, instead of paying a booking site to meet them again. It sounds like marketing. The work is operations.

At a twenty room inn, the person who would write the thank you is the one checking in a guest and finding a plumber. The direct path is not a system, it is a list of small jobs, and the list belongs to nobody. The drafting got cheap: a language model writes the message, an automation tool schedules it. The judgment did not. Who gets one, and what you tell the owner, is the part you sell.

The qualification is not hotel marketing. It is owning a list of small recurring jobs in a business you do not own. Rates and revenue management stay outside.

Full episode: {{EPISODE_URL}}

The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode covers the three jobs in full, the one number worth reporting monthly, and where in the room count the work starts to pay. It also names the kill condition: if agencies already retain thirty room inns, this is not a business.
```

---

## Short 03: The Guest Book

**Title:** The guest list a small hotel can actually work with (51 chars)

**Description:**

```
You can build a direct-booking practice for small hotels. Get one constraint right before you pick a tool.

Booking.com's own partner help says it does not share private guest email addresses. Both sides see an alias ending at guest.booking.com, and partners are asked to keep the conversation on the platform. So you cannot win a guest back from a relay address, and you are not supposed to try.

What the inn needs first is not an email tool. It is a guest book of its own, at the front desk, that the guest chooses to sign. The registration card and the wifi login ask for the guest's own email. That list runs under the American email law, and European rules for European guests. Check your jurisdiction. This is not legal advice.

Full episode: {{EPISODE_URL}}

The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode covers what an outside operator may and may not do with that list under each site's own partner terms, and where the messaging window closes. Still not legal advice: check your own jurisdiction before you collect anything.
```

---

## Short 04: Four Numbers

**Title:** Price a direct booking service off four numbers (47 chars)

**Description:**

```
You can build a direct-booking practice, and price it honestly off four numbers you ask the owner for: rooms, average nightly rate, occupancy, and the share of bookings arriving through the sites.

That gives you the revenue the sites carry. Apply a commission band and you have the annual cost. Then assume a shift in the mix, and say out loud that the size of that shift is a hypothesis nobody has measured. Subtract what running direct costs. What is left is the recoverable amount, a month. That is the ceiling, and your fee lives under it.

On an illustrative twenty room inn at a hundred and eighty a night and seventy percent occupancy, it lands near a thousand to fourteen hundred dollars a month. That is a modeled ceiling, not commission the service saves, and the low end of the direct-cost band is one vendor's own figure. Some properties cannot fund this. The arithmetic tells you which, before you quote.

Full episode: {{EPISODE_URL}}

The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode runs the arithmetic end to end on the illustrative inn and shows what is left after the work, including the case where the model does not clear its own target. Every figure in it is arithmetic on an invented property, with the assumptions stated.
```

---

## Claim boundaries applied

- **C009 (Google free booking links)** keeps its required hedge, "connected through a partner",
  in Short 01's description.
- **C007 (Booking.com relay)** keeps "partner help" named in Short 03.
- **C026 (guest data)** keeps "this is not legal advice" in both Short 03's description and its
  pinned comment.
- **C020 (the recoverable ceiling)** is the one the Shorts tightened. The spoken layer says "it
  lands near a thousand to fourteen hundred dollars a month" with "illustrative" and the
  assumptions aloud. The description adds the two hedges the registry attaches and the Short's
  audio does not: that it is a modeled ceiling rather than commission the service saves, and that
  the low end of the direct-cost band is one vendor's own figure. This closes the W1 finding from
  the 2026-10-09 red team without re-cutting narration.
- No figure appears in any title. No income framing anywhere. No superlative about the channel.
