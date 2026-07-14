# Site copy v2 — APPLIED July 14, 2026

Source: canonical thesis language bank in `positioning.md` (Joanie call, 7/14). Numbers in brackets reference the bank. Every change below is a proposal; current copy shown for diff-ability. Surfaces not listed (chips, format sub, capture h3, ledger, footer tagline) stay as-is — they already align.

---

## Hero

**Kicker** — keep: `Stop climbing. Start building.`
(Alternative if we want the thesis harder in the door: `You already know the problem. That's the qualification.` [3] — probably too long for a kicker; parked.)

**H1** [2]
- Current: `You can build it now. We show you what's worth building.`
- Draft: `It's easy to build now. It's hard to know <em>what</em> to build.`
- Why: names the reader's pain (the blank page problem) instead of our editorial authority. The "we do that part" is implied by the entire page below it. Em moves from *worth* to *what*.

**Lead** [3]
- Current: `Every Monday: one real business one experienced person can build and run — the companies proving it works, the exact stack and what it costs, the honest math. Plus the free Operator Blueprint to build from.`
- Draft: `Every Monday: one real business one experienced person can build and run — the companies proving it works, the exact stack and what it costs, the honest math. You bring the expertise you already have. The free Operator Blueprint is the rest.`
- Why: expertise-as-spec, stated before the CTA. The non-technical 35–55 reader's silent objection is "I can't build things" — this answers it in the same breath as the offer.

## Format band

**Kicker** — keep: `The tools got cheap. The judgment didn't.` (already carries [4]).

## Library

**H2** [5]
- Current: `Businesses you could build.`
- Draft: `One-person businesses you could actually run.`
- Why: "one-person" imports the village-economy frame without the metaphor; "actually run" carries the honest-math register. Softest change in the set — fine to skip.

## Disclosures

**New row, after "Scarcity timers"** [6]
- Label: `Unicorn ambitions`
- Answer: `None. These are livings: $2–8K/mo, honestly ranged.`
- Why: the deadpan disclosure format is the perfect home for the post-unicorn line — it reads as a joke and a promise simultaneously, and it pre-frames the honest-math numbers on every episode card.

## Capture

**Lead paragraph, append one sentence** [7]
- Current: `Every episode ships with an Operator Blueprint: the sourced working doc behind the video — evidence table, tool stack with costs, week-by-week playbook, every citation.`
- Draft: same + `Written so you can execute without a technical background.`
- Why: the blueprint's real product is confidence to execute (Joanie's mirror-back). One sentence, placed at the moment of email commitment.

---

## Held back deliberately

- **The village riff** [5, full version] — episode cold-open / newsletter material, not site chrome. Also the "ordinary businesses" framing language is TBD per positioning.md until the face comes forward.
- **The land metaphor** — script material only.
- **"AI can't solve distribution"** [4] — belongs in every blueprint's playbook/failure-modes section rather than marketing copy; on the site it would read as a caveat before the reader knows what's being caveated.

## Application order (when approved)

All changes live in `site/app/page.tsx` (H1 line ~97, lead ~99–103, library h2 ~212, disclosures ~245+, capture lead ~271). Single commit, no structural changes.
