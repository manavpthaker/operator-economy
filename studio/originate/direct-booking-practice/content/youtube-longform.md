# EP009 long-form: YouTube upload package

Status: **drafted 2026-10-12, not owner-approved.** Nothing uploaded, scheduled or published.
No URL is stated. `{{EPISODE_URL}}` and `{{BLUEPRINT_URL}}` resolve only from
`studio/originate/direct-booking-practice/launch/links.json`, which does not exist yet.

Internal **EP009**, publishing as public **No. 002**. Slug `direct-booking-practice`.
**Not** `direct-booking-recovery`: that is EP006's and its `links.json` holds live IDs.

Source of truth: the owner-accepted r11 cut (20:22, 29,323 frames at 24fps), the locked narration
(`operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/canonical-w.txt`) and
the claims map v0.2 (C001-C037, byte-identical to its 2026-09-03 lock). Claim limits and the
do-not-state list are in the EP009 section of `content-os/facts.md`.

---

## Title

**Owner-selected 2026-10-09: The One-Person Business That Gets Small Hotels Booking Direct** (60 characters)

Pairs with the thumbnail by the division the owner set on No. 001: the thumbnail carries the verb
(`HELP HER KEEP THEM`), the title names the business. "Gets ... booking direct" is the service's
function, not an outcome promise. No figure, no income framing, no claim that the practice recovers
a given share.

Alternates considered and not selected: "The One-Person Business Behind a Hotel's Direct Bookings"
(56), "How to Run the One-Person Business That Wins a Hotel's Guests Back" (65).

## Thumbnail

`studio/originate/direct-booking-practice/launch/thumbnail.png`, 3840x2160. Full record in
`launch/thumbnail-note.md`.

---

## Description

Paste as written. Channel boilerplate is appended by Studio upload defaults; do not paste it again.

```
The free Operator Canvas for this episode, with the four-number model and the thirty-day plan: {{BLUEPRINT_URL}}

An innkeeper with twenty rooms sends a thank you to a guest she liked, and the email on the reservation isn't his. It's a relay. A year later the same guest books the same room through the same website, and she pays the same commission for a guest she already knows by name.

There's a service hiding inside that second commission, and one piece of arithmetic that decides whether it's worth your time to sell it.

This episode builds that job as a one-person direct-booking practice: what the three recurring tasks are, why the guest list has to be the inn's own rather than scraped from a booking site, how to price it off four numbers the owner already knows, and where the ceiling says no.

Cloudbeds, from about ninety million bookings, is the source for the share of independent-hotel reservations running through the sites. HOTREC's study of European hotels is the counterweight, and it is Europe, not the US. Commission bands come from trade reporting, not from the sites themselves.

The economics are a modeled scenario on an invented inn, not observed performance and not an earnings forecast. The size of the mix shift it turns on is a hypothesis nobody has measured, and the episode says so out loud.

Nothing here is legal advice. Guest data runs under each site's own partner terms, the American email law, and European rules for European guests. Check your jurisdiction.

Chapters
0:00 A guest she already knows
0:59 The Operator Economy
1:24 How a small inn fills its rooms
3:05 Who keeps the guest's email
3:53 How much of the business is rented
5:02 What the site keeps
6:04 If the parts are cheap, why doesn't the inn do it
6:46 Somebody would already be selling it
7:56 The model
9:46 The company that does this job
10:45 What the job actually needs
11:32 What the software does, and what you do
12:10 What you sell first
13:12 The retainer
14:09 How the first owner arrives
14:51 Your side of the arithmetic
16:36 What's genuinely hard
17:32 The first thirty days
18:31 Back to the inn
19:23 The verdict
19:52 The first move

The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

---

## Tags (episode-specific, on top of channel defaults)

```
direct booking, independent hotels, hotel commission, booking.com, OTA commission, small hotel marketing, hospitality operations, one person business, solo consulting, AI for small business, guest email list, hotel direct bookings, operator economy
```

No tag states a figure or a claim. "hotel commission" and "OTA commission" are topic tags, not
assertions about a rate.

---

## Pinned comment

```
{{EPISODE_URL}}

Four numbers decide whether this business can exist at a given property: rooms, average nightly rate, occupancy, and the share arriving through the sites. Run them before you pitch anyone. The model in this episode is arithmetic on an inn I made up, and the mix shift it turns on is a hypothesis nobody has measured.
```

---

## AI disclosure

- **Altered or synthetic content: YES.**
- The narration is an AI voice clone of the host's own voice (a Google TTS performance transferred
  onto the accepted Original C clone through ElevenLabs Voice Changer). The presenter footage, the
  innkeeper, the guest and the film plates are all AI-generated.
- The last line of the description carries this in plain language.
- On the API upload path, set `containsSyntheticMedia: true`. In Studio it is the
  **Altered or synthetic content** checkbox, and it is a human step.

---

## Upload checklist (settings that are not defaults)

- [ ] Altered or synthetic content: **YES**
- [ ] Thumbnail: `launch/thumbnail.jpg`
- [ ] Category: Education
- [ ] Audience: not made for kids
- [ ] Chapters: present in the description above, first at 0:00
- [ ] `{{BLUEPRINT_URL}}` and `{{EPISODE_URL}}` resolved from `links.json`, never typed
- [ ] Shorts' Related Video set to this video once it is live
- [ ] **Gate 3**: `studio/config/blueprint.json` still has `autonomy.training_mode: true`, which
      forces the pre-publish episode library review regardless of confidence score. Owner's rule,
      owner's to waive or run.
