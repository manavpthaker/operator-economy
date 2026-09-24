# Step 0 evidence amendment 01: Booking.com partner pages opened at source

Status: recorded

Template version: `operator-blueprint-v2-step0.2` (amendment record; the reviewed research brief is unchanged so the promotion hashes still hold)

Candidate ID: `candidate-2026-09-03-direct-booking-recovery`

Research brief amended (by reference only): `candidate-2026-09-03-direct-booking-recovery.md` / `07c61fa3fca535f9569670dbe73c6e823eaa3ab33ba5e67f7c22519a5194e5d7`

Promotion record: `../04-queue/candidate-2026-09-03-direct-booking-recovery-promotion.md`

Recorded: 2026-09-03

Recorded by: the Step 1 showrunner process, on the pre-lock condition carried in the promotion record

## Why this record exists

The promotion record carries a pre-lock condition: the Booking.com partner pages behind CLM-005 and CLM-008 returned HTTP 403 to the research process on 2026-09-03 and had to be opened in a browser and recorded before any script lock. They were opened in a browser session on 2026-09-03 and both loaded. This record captures what they said on the day. It does not edit the reviewed research brief, so the six promotion hashes remain valid.

## CLM-008: guest contact policy (opened at source)

Source: Booking.com for Partners, Partner Help, "Contacting your guests" — https://partner.booking.com/en-gb/help/reservations/contact-extranet/contacting-your-guests

Page state: "Updated 2 months ago" as of 2026-09-03. Accessed 2026-09-03.

What the page states, in the Privacy section:

- "To protect your and your guests' privacy, we don't share private email addresses. Both you and your guests will only ever see an anonymous alias ending in @guest.booking.com or @partner.booking.com."
- "Please use only the Booking.com platforms, extranet and Pulse app to continue communicating with your guests securely."
- Messages sent through the platform are stored and may be accessed by Booking.com for legal, fraud, service-improvement, and spam-detection reasons.
- If suspicious activity is detected, the property's ability to include links in guest messages is disabled.

The FAQ list on the page includes "How long is the chat function with guests enabled for?" and "Can I get the guests' contact information?"; the answers are collapsed and were not expanded in this session, so the seven-day and one-year windows in CLM-008 remain sourced from the Hospitality Net pieces, not from this page.

Status change: CLM-008 moves from `verified (medium-high), secondary` to **verified at source (primary)** for the alias policy and the on-platform instruction. The messaging-window durations remain secondary.

## CLM-005: commission mechanics (opened at source)

Source: Booking.com for Partners, Partner Help, "Understanding your commission" — https://partner.booking.com/en-gb/help/commission-invoices-tax/commission/understanding-our-commission

Page state: "Updated 1 week ago" as of 2026-09-03. Accessed 2026-09-03.

What the page states:

- "Commission is a set percentage of the total booking amount that we charge for each reservation received through our platform. This includes the room rate as well as any additional fees you charge — such as cleaning fees, service fees, and costs for no-shows or cancellations — and is applied once the guest checks out."
- Commission is charged on confirmed stays, non-refundable and partially refundable bookings regardless of stay, charged no-show and cancellation fees, and overbookings.
- "The exact percentage depends on your country, property type and the accommodation agreement you signed when you joined us."
- "If the commission percentage stated on the reservation statement is higher than the percentage listed on your contract, you may be participating in one of our marketing programmes like Preferred Partner or Visibility Booster."
- Commission is not charged on local taxes such as city tax, but in most countries is charged on VAT or GST.
- Invoices are monthly, covering reservations where the guest checked out in the previous month.

What the page does **not** state: any numeric base commission rate. The page explicitly says commission varies by country and property type and directs prospective partners to the registration process to see their rate.

Status change: CLM-005's **mechanics** (percentage of total booking amount including fees, charged at checkout, raised by Preferred Partner and Visibility Booster participation, charged on non-refundable bookings and charged cancellation fees) move to **verified at source (primary)**. The **base rate band (~15 percent, 12 to 17 percent by market)** remains **secondary and qualified**; Booking.com publishes no number on this page. The all-in band used in the ceiling model stays a `qualified model` input.

## Effect on the episode

- The script may state, attributed to Booking.com's own partner help, that commission is a percentage of the whole booking including fees, that it is charged at checkout, that it rises with the visibility programmes, and that the platform hides guest email addresses behind aliases and asks partners to keep communication on-platform.
- The script may **not** state a Booking.com base commission percentage as Booking.com's own figure. Any percentage remains attributed to secondary sources and labeled a range.
- The ceiling arithmetic keeps its `modeled scenario, not observed performance or an earnings forecast` label; the commission input is now anchored in verified mechanics but still an assumed rate.
- The pre-lock condition on opening the pages is **satisfied**. The second pre-lock condition (an independent US source for OTA share and commission profile by property size, or audit data from validation step 1) is **not** addressed by this record and remains open.

## Snapshot

Page text was read in a browser session on 2026-09-03 and the passages above are quoted verbatim from that session. No local copy of the full page was saved; the URLs above are the locators.
