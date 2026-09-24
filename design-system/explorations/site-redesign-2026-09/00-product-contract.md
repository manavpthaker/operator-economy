# Product contract — Operator Canvas reader tool

Status: draft for owner review (step 2 of the approved redesign sequence).
Scope: governs the site redesign and the Step 7 web and reader-tool sub-proposal.
Owner approval of this document is design approval only — no content or production authorization.

## 1. Primary reader job

A capable professional arrives with "I see a problem or trend" and uses the Canvas to
**determine whether to test, revise, or reject the opportunity.**

The page is a decision instrument, not a landing page. Its success is a reader who can
explain the mature company to someone else, identify its weakest assumption, and name the
first bounded construction step and its stop conditions (the Step 1 transformation
contract, `operator-blueprint-v2/01-editorial/EDITORIAL-STANDARD.md:191-208`).

## 2. Core comprehension tasks

The design is correct only if a representative reader, on the Canvas page, can:

| # | Task | Pass condition |
|---|---|---|
| T1 | Identify the buyer, the offer, and the first test | States all three unprompted after reading the decision summary + Sheet 00/04 |
| T2 | Distinguish `OBSERVED / PARALLEL / MODELED / UNKNOWN` | Correctly classifies two shown statements and explains why one figure is "not a fact" |
| T3 | Find the most sensitive assumption and the stop condition | Locates both on Sheets 03/04 without assistance |
| T4 | Understand that downloading the PDF does not subscribe them to the newsletter | States it before submitting the download form |

Failure of any task by a majority of testers blocks expansion (sequence step 5) until the
design is revised and retested.

## 3. Testing protocol

- **Who:** 5–7 representative readers — employed professionals considering an independent
  path, between roles, or already building (the three core-viewer situations named in the
  editorial standard). Not designers, not repo contributors.
- **When:** after the core Canvas desktop/mobile prototype (B1/B2) and Method (B3) exist,
  before any other screen is designed (sequence step 4).
- **How:** moderated task-based sessions against T1–T4, thinking aloud; plus separate
  keyboard-only, screen-reader, and 375px-mobile passes run against the accessibility bar
  in `01-experience-spec.md`.
- **Fallback (recorded as weaker evidence):** if 5–7 external readers cannot be recruited,
  moderated internal passes may substitute, flagged explicitly in `decision-log.md`.
- **Output:** findings logged in `decision-log.md`; revisions are made from observed
  failures, not taste, and retested where a task failed.

## 4. Measurement schema

Defined now; instrumented in the later implementation effort. The schema is part of this
contract so the redesign's purpose (Canvas use and honest capture) is measurable from
launch, not retrofitted. Analytics implementation choice (platform, consent handling) is
an implementation-phase decision bounded by the privacy contract in `01-experience-spec.md`.

Event names are stable identifiers; properties in parentheses.

**Reading and tool use**
- `canvas_enter` (slug, referrer_class: home | library | direct | external)
- `sheet_view` (slug, sheet: 00–04, max_depth_reached)
- `guide_start`, `guide_step` (step 1–5), `guide_complete`, `guide_exit` (last_step)
- `source_receipt_open` (slug, claim_id)
- `unknown_register_open` (slug)
- `scenario_interact` (slug, view: columns | lens, case: low | base | high)
- `provenance_expand` (slug), `hash_copy` (slug)
- `method_enter` (referrer_class), `evidence_legend_view`

**Conversion and delivery**
- `download_request` (slug), `download_delivered` (slug), `download_failed` (slug, reason)
- `newsletter_optin` (context: download_form | newsletter_band) — distinct from download
- `unsubscribe` (tag_scope: single | global)

**Exits**
- `youtube_exit` (slug, position: hero | episode_band | footer)

**Derived measures reviewed per episode:** qualified readership (canvas entries with
sheet_view depth ≥ 3), reader-tool use (any of receipt/unknown/scenario events), guided
completion rate, download-to-optin separation rate (proves the consent split is real),
delivery failure rate.

## 5. Success framing

Inherits the portfolio charter's institutional measures
(`content-os/strategy/portfolio-charter.md:92`): source quality, corrections, qualified
readership, reader-tool use, and evidence that a thesis claim strengthened or weakened —
plus evidence that a reader changed a decision (a reported test, revise, or reject).
The charter's remaining institutional measures, episode CTR and retention, are inherited
by the channel rather than this tool. Raw traffic and subscriber totals are not success
measures for this tool.
