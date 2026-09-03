# Bounded Step 0 amendment request: Booking.com guest-messaging window durations

Status: **submitted**

Template version: approved `operator-blueprint-v2-step1-v1.5`

Episode or fixture: EP009

Candidate ID: `candidate-2026-09-03-direct-booking-recovery`

Current script revision and SHA-256: v0.3 / `cbe74c03e021998cafc1d11a8b0dff50e6dfaa4d0109fc223c958a6ecc37993c`

Claims-map revision and SHA-256: v0.2 / `2863880e2874184ae23b4b707faacfbd0ebcd116f46539b5cda0433b1846dc50`

Operator-Canvas revision and SHA-256: v0.1 / `ac26ef455272ef63046e181305311bf2754bf18cb19448d2d90d1b0fc4538847`

Episode-Investment-Thesis revision, SHA-256, and Gate E3I status: v0.1 / `293cee76cb0bea309e5d37d629177a21d3cb51082095256005872d2ba95c189c` / drafted, owner approval pending

## Exact proposed public claim

S00: "A week or so after checkout, the relay stops working."

S07: "The trade press puts the messaging window at about seven days after checkout, and Expedia's at about forty five."

The request is to allow S07 to say "Booking dot com's partner help puts the messaging window at about seven days after checkout" if the page confirms it, and to let the cold open's "a week or so" stand on a primary source.

## Why the claim is necessary

Narrative or operating decision that fails without it: the cold open's concrete event is the relay expiring. S07 turns that event into the design constraint (consent capture at the desk). Without a duration the constraint is still true (the alias policy and on-platform instruction are primary via Step 0 amendment 01), but the cold open loses its clock.

Why removal or modeled wording is insufficient: the alias policy alone tells the viewer the inn has no email. The expiring window tells the viewer the inn also has no time. The second is what makes "a guest book of its own" the first design decision rather than one option among several.

## Missing evidence

Population: Booking.com partner properties.

Metric or proposition: the period after checkout during which partner-to-guest messaging remains enabled, and the period after which threads become unreadable.

Geography and period: global partner help, current as of the day it is opened.

Required methodology or source quality: Booking.com Partner Help, "Contacting your guests", with the collapsed FAQ answers expanded and quoted verbatim. Step 0 amendment 01 records that the FAQ list on the page includes "How long is the chat function with guests enabled for?" and "Can I get the guests' contact information?" but the answers were not expanded in the 2026-09-03 session.

Evidence that is explicitly insufficient: the Hospitality Net opinion column of 2026-08-25 and the 2015 Toedt piece (CLM-008), which are the current source for the durations.

## Narrow research question

What do the expanded FAQ answers on https://partner.booking.com/en-gb/help/reservations/contact-extranet/contacting-your-guests say about how long the chat function remains enabled after checkout and whether the guest's contact information is available, on the day they are opened?

## Allowed outcomes

- Approve exact wording with locator and qualification (S07 attributes to partner help, cold open stands).
- Approve narrower wording (for example "the messaging window closes not long after checkout").
- Deny and keep the trade-press attribution as written, recorded as an accepted secondary detail.
- Return unresolved and keep E6 blocked on this item.

## Change impact if approved

Step 0 artifacts requiring amendment: a second entry in the Step 0 evidence amendment record, by reference only. The reviewed research brief is not edited.

Step 1 artifacts invalidated: none if the wording is approved as written. If narrower wording is required, `script.md` (S00, S07), `performance-readthrough.txt`, `claims-map.md` (C008), and every review artifact rehash.

Episode Investment Thesis invalidated: no

Gate E3I disposition required: not applicable

Research refresh date: 2026-12-03

Approver: (Step 0, owner decision pending)

Approval date: (pending)

Approved amendment SHA-256: (pending)

The claim remains attributed to the trade press until the approved amendment and dependent hashes are recorded.
