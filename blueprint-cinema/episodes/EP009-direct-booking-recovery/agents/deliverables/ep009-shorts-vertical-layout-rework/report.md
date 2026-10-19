# EP009 Shorts 01, 03, and 04: portrait layout rework

## Finding

The current `context_focus` treatment is not usable for these designed scenes. It enlarges a
16:9 raster to `2.02x` and pans it inside a 900 x 1,200 portrait window. That makes individual
objects larger, but it destroys the relationship between them. Several sampled frames cut words,
labels, people, and diagram endpoints off the canvas. Short 01 also becomes almost blank at 45s.

Keep the locked carrier and exact voice cuts. Replace only the affected designed-scene picture
with simple native 1080 x 1920 HTML/SVG. Use source-video portrait crops only where the film or
presenter already reads cleanly.

## One implementation primitive

Add a native portrait layout branch to `Scene` / `subcomposition_html()`, for example
`layout="native_diagram"` plus a `diagram` identifier. The branch should:

- draw within `x=96..900`, `y=260..1,360`; keep the existing caption rail at `y=1,450`;
- use 48px minimum labels and 72-96px primary numbers/titles;
- use mineral lines/text, oxide only for the active boundary or repeated commission;
- hard-cut at the existing scene times; within a scene, reveal only the next accountable element;
- use only words, numbers, and relationships already present in the locked narration or source
  design; retain `illustrative` / assumption language where the source contains it;
- omit miniature UI chrome, source footnotes, and decorative motion that cannot be read on a phone.

Reusable portrait SVG symbols are enough: `inn`, `guest`, `booking_site`, `guest_book`, `email`,
`rule_boundary`, `commission_tag`, and directional/broken connectors. These can be inline SVG; no
new media is needed.

## Short 01 - The second commission

Exact cut stays `[0.000000, 59.458333)`.

| Scene | Local time | Current result | Reauthoring plan |
|---|---:|---|---|
| 1 | 0.000-3.583 | Presenter is centered and readable. | Keep `presenter`. No layout change. |
| 2 | 3.583-10.500 | Checkout/departure film reads cleanly. | Keep `film_context`. |
| 3 | 10.500-16.833 | Thank-you attempt film reads cleanly. | Keep `film_center`. |
| 4 | 16.833-22.750 | Relay address is enlarged, but it is clipped to `k7m2q9x4@guest.bo`; surrounding UI adds no readable context. | Native `relay_address`: one large outlined field with `k7m2q9x4@guest.booking.com`, a small `RELAY` label, and a connector ending at a rule/boundary. Reveal the field on “string of letters and numbers” and the relay label on “A relay.” |
| 5 | 22.750-27.500 | Inn is readable, but the checkout line and email exit the right edge. | Native `relay_expires`: center the inn and guest; route the relay line between them, then break/fade the line on “the relay stops working.” Keep `A week or so after checkout` as a small timing label only. |
| 6 | 27.500-32.042 | Booking site is visible, but “A year later,” the input path, and the room relationship are cut apart. | Native `repeat_booking`: stack `GUEST -> BOOKING SITE -> INN / SAME ROOM` vertically. Add `A YEAR LATER` above the stack. Reveal the arrows with the spoken order. |
| 7 | 32.042-36.333 | The pan shows fragments and then nearly empty canvas; the repeated commission is not legible. | Native `repeat_commission`: keep the same vertical stack and place two equal oxide `COMMISSION` tags beside `FIRST STAY` and `SECOND STAY`. No percentage or new value. Emphasize the second tag when “same commission” is spoken. |
| 8 | 36.333-40.083 | Innkeeper recognition film reads cleanly. | Keep `film_right`. |
| 9 | 40.083-50.292 | At 45s the accountable visual is almost entirely outside the canvas. This is the most severe failure. | Native `service_and_arithmetic`: large heading `SECOND COMMISSION`; reveal the exact fragments `a service hiding inside it` and `one piece of arithmetic`; end on `WORTH YOUR TIME?`. Keep this typographic and diagrammatic; do not invent a formula or ROI number. |
| 10 | 50.292-59.458 | Presenter question reads cleanly. | Keep `presenter`. |

## Short 03 - The guest book moved

Exact cut stays `[336.250000, 369.833333)`.

| Scene | Local time | Current result | Reauthoring plan |
|---|---:|---|---|
| 1 | 0.000-2.792 | Booking site is cut on the right and the supposed guest-book evidence is not visible. | Native `guest_book_at_site`: center a booking-site card with a large guest-book icon inside it and label both. The relationship should be readable in one glance. |
| 2 | 2.792-8.750 | Booking site and guest-book label are readable, but the absent inn/email relationship is not. | Native `inn_without_email`: two columns, `INN + GUEST` on the left and `BOOKING SITE` containing an `EMAIL` card on the right; stop the connector at an oxide boundary. Add `NO DIRECT EMAIL` beneath the inn only when the narration says it. |
| 3 | 8.750-13.750 | Huge clipped title and inn; the design constraint is not a complete thought. | Native `constraint_before_tool`: full-width title `A DESIGN CONSTRAINT` with a smaller second line `before a tool`; below it, show the inn facing the boundary. Avoid any source-raster zoom. |
| 4 | 13.750-19.750 | The title, inn, booking site, relay, and connector cannot fit after zoom; every edge is clipped. | Native `relay_rule_boundary`: large relay-address card above a clear line labeled `THE SITE'S RULES`; an attempted arrow toward the inn stops at that line. Use no prohibition copy beyond the locked narration. |
| 5 | 19.750-25.750 | Booking site/email are visible, but the heading is clipped and the “own guest book” answer is absent. | Native `own_guest_book`: small subdued `EMAIL TOOL` card, then a larger `GUEST BOOK OF ITS OWN` card placed at a front-desk/inn symbol. The second card becomes active on “It's a guest book of its own.” |
| 6a | 25.750-28.750 | The current wide diagram still privileges the booking-site email; the guest's voluntary action is not shown. | Native `guest_chooses`: guest beside a front-desk guest book with an unforced pen/sign action; label only `GUEST CHOOSES TO SIGN`. |
| 6b | 28.750-31.750 | “Fair question here” and “If the parts...” sit over a diagram that is answering a different point. | Split the existing scene without changing voice time. Use a native question card: `FAIR QUESTION` then `IF THE PARTS ARE CHEAP...` as the lead-in. |
| 7 | 31.750-33.583 | Presenter is pushed to the right and half the face is cut off. | Add/use `presenter_right` with source crop `x=560..1280` mapped to the 1,080 x 1,080 panel. Keep the final spoken question and hand movement. |

## Short 04 - The commission number is wrong

Exact cut stays `[506.250000, 528.750000)`.

| Scene | Local time | Current result | Reauthoring plan |
|---|---:|---|---|
| 1 | 0.000-5.750 | `ILLUSTRATIVE MODEL`, `Commission 18% to 22%`, and the bar are clipped on the left; the caveat is too small to read. | Native `commission_band`: top label `ILLUSTRATIVE MODEL`; large `18%-22%`; supporting line `commission assumption from the reported bands`; one simple vertical bar with the commission slice in oxide. |
| 2 | 5.750-10.250 | The annual amount is clipped and split across the raster; evidence is not phone-readable. | Native `annual_commission`: large `$105K-$130K / YEAR`, label `ROUGH SITE COMMISSION`, and small `illustrative estimate`. Preserve the voice hedge; do not add a new calculation. |
| 3 | 10.250-14.167 | The source transitions from the wide model to a presenter while the zoom is active, producing a half face at 13s. | Native `old_argument_stops`: hold the annual range at reduced size, add `THE OLD ARGUMENT STOPS HERE`, and end on `THE WRONG NUMBER` as the voice reaches the correction. This removes the mixed raster/presenter zoom entirely. |
| 4 | 14.167-22.500 | Once this scene begins, the default presenter crop is centered and readable at the sampled 17s and 21.5s frames. | Keep `presenter`. If a check at exactly 14.2s shows the face entering from the edge, use a 0.35s wider `film_context` lead-in before the current presenter crop; do not retime audio. |

## Acceptance checks

- At every contact-sheet sample, no primary word, number, face, icon, or connector endpoint crosses
  `x=96..900` or collides with the caption rail.
- `k7m2q9x4@guest.booking.com`, `18%-22%`, and `$105K-$130K / YEAR` are fully readable at phone size.
- Short 01 at 45s shows the service/arithmetic relationship, not blank paper.
- Short 03 at 32.5s shows a complete presenter face.
- Short 04 at 13s never shows a zoomed half face.
- Source cut times, caption timing/text, locked carrier hash, and narration remain unchanged.
- No render, upload, publication, or Short approval is implied by this rework.

