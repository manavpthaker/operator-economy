# Topic queue (v4 — search-led intake, opened 2026-08-10)

**The queue is empty by decision, not by accident.** v3 was retired on 2026-08-10 after five
shipped episodes; the full 22-row table and the disposition of every row are in
`archive/2026-08-queue-v3.md`. Guest-dependent episodes are parked in `parked.md`, not dropped.

## What changed and why

v3 scored topics on thesis strength. Five episodes in, thesis strength is not the constraint.
Discovery is:

| Episode | Impressions | CTR | Views |
|---|---|---|---|
| EP002 | 288 | **0.7%** | 3 |
| EP003 | 160 | **0.0%** | 1 |

Healthy is 4% or better. The scripts pass their evals, the cards pass the fact gate, and almost
nobody clicks. So v4 selects for topics that arrive with existing search demand, and the thesis
serves the query rather than the reverse. `scoring.md` carries the re-weight: search demand moved
from 25 to 35 points, funded by dropping affiliate potential and derivation richness to 5 each.

Evidence availability (20) and POV strength (15) are unchanged. Both are hard gates rather than
preferences: no evidence means no video, and the POV pass is the monetization moat and the
inauthentic-content-policy shield.

## Production queue

| # | Episode thesis | Target query (volume/mo) | Low-end evidence | High-end evidence | Score | Status |
|---|---|---|---|---|---|---|
| 006 | Independent hotels pay 18–30% to fill their own rooms — the operator who wins the bookings back | `direct booking hotel` (**volume TBC**) | Freelance hotel revenue mgmt $129K/yr ([ZipRecruiter](https://www.ziprecruiter.com/Jobs/Freelance-Remote-Hotel-Revenue-Management)) — income, not price | Mews $300M Series D, **$2.5B** ([PR Newswire](https://www.prnewswire.com/news-releases/mews-secures-300-million-investment-to-cement-position-as-worlds-leading-hospitality-operating-system-302668120.html)) | 52/65 + owner override | **In production** |

**EP006 is an owner override, recorded as one.** `scoring.md` reserves this
explicitly — *"The rubric ranks candidates; it does not outrank the person
running the channel"* — and requires it be written down so a later re-score does
not read it as a scoring result. It is not a 65+ row and cannot be: search demand
is 35 points and the Ahrefs plan carries no API access. Full intake, including the
three candidates it beat, is in `intake-2026-08-14.md`.

**Why this one over the higher-scoring row.** Ghostwriting scored 53 and was held
the same day: its entire margin was first-party POV, and those figures are not to
hand. This row's POV is 15/15 and already in hand — Manav ran four properties in
the Yucatán and has been the person paying the commission rather than the person
selling the fix. It is the only eligible candidate whose operator experience needs
nothing from anybody else.

**Not guest-dependent.** No hotelier appears and no client is named. Per
`parked.md`, a guest needs browse CTR near 4% and three figures of views before
appearing is worth their time; EP002 ran 0.7% on 3 views.

**Known evidence gap, carried deliberately.** No provider in this market publishes
a per-property retainer — every one checked quotes privately. There is no
equivalent of EP002's "$300–1,000/mo per client" to cite, and the brief instructs
naming that aloud rather than inventing a figure. The opacity is itself part of
the thesis.


## Intake rules

A row may not be written here directly. Candidates enter through the intake and are only promoted
once scored.

1. **Every candidate names its target query and that query's monthly volume.** Search demand is
   35 of 100 and cannot be scored on intuition. `../docs/growth-strategy.md` lists the validated
   patterns already researched: "how [AI company] makes money" at 45 to 65K/mo, "[company]
   business model" at 35 to 50K/mo, "how Cursor makes money" at 5 to 9K/mo.
2. **Both evidence ends carry a source URL at intake.** A low-end operator and a high-end
   venture-scale proof, each with a link. A candidate missing either end is not a candidate.
   `eval_script.py` enforces the same span later; catching it at intake avoids writing a script
   that cannot pass.
3. **Produce at ≥65. Archive below 50.** Unchanged from v3, but harder to reach without real
   query volume, which is the point.
4. **No inherited scores.** Any v3 row may be re-proposed, but it re-enters at intake and is
   scored against the v4 weights. An old score does not transfer.
5. **Guest-dependent theses go to `parked.md`,** not here, until the unblock condition in that
   file is met.

## Held constant across the next five

These are the fix, not experiments, so they do not vary between episodes and are not scored:

- Thumbnail built to `../docs/thumbnail-rubric.md` and passing the mechanical checks (aspect,
  legibility at 120px, contrast). No self-certified waivers.
- Title targets the row's stated query, entity name front-loaded.

Format variables (talking head, on-screen density, runtime) stay frozen until browse CTR clears
roughly 4%, then get tested one per episode. Testing five variables across five episodes teaches
nothing at this sample size.

## Sequencing logic

Replaced with the constraint above: pick the highest-scoring eligible row, ship it with the
constants held, and read CTR by traffic source on the Friday after. Re-sequence only when the
CTR read says something. The v3 archetype review at upload 12 still stands.
