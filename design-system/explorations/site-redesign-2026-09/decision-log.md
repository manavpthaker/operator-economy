# Site redesign 2026-09 — decision log

One dated entry per owner review point or load-bearing decision. This effort is the
**Step 7 web and reader-tool sub-proposal (design only)** — no content or production
authorization. Governing plan: approved by owner 2026-09-01 (session record).

## 2026-09-01 — Effort opened; steps 0–1 executed

**Step 0 — preservation.** `design-system/explorations/rev-d/operator-canvas-lp-mockup.html`
(untracked, 100KB) committed unchanged (`24c4a024`). Harvested for structure only; its
`:root` is off-token drift (see `03-drift-reconciliation.md`). Its keyboard tabs, URL
history, reduced-motion handling, and mobile overflow behavior are non-regression
requirements for the new prototype.

**Step 1 — №006 identity reconciliation** (`9cccb57a`, `site/data/episodes.json`):

- `direct-booking-recovery`: queue index 11 → publication **№006**; `upcoming` → `live`
  (published 2026-08-17 per `release.json` and `launch/links.json`); title was the 40-word
  thesis paragraph → the shipped episode title "Hotels pay 30% to book their own rooms";
  `legacy_queue_number: 11` retained for traceability; `model: Retainers` backfilled.
- `too-small-to-bother`: 10 → publication **№005** (EP007 README records №006 as the last
  assigned number in the series 1–6); `legacy_queue_number: 10` retained.
- Five stale topic-queue rows (small-cohort-business, one-person-media-company,
  recruiting-agency, hospitality-tech, avatar-localization) demoted to hidden
  `status: "queued"` — `topics/queue.md` v4 declares the queue empty by decision. Their
  old queue indices remain on the hidden rows; full cleanup is backlogged.
- `updated: 2026-09-01`; `queue_depth: 1` (one V2 candidate in editorial development).
- **PDF decision:** the site file stays slug-keyed (`/blueprints/direct-booking-recovery.pdf`).
  The local pipeline artifact `Operator-Blueprint-011.pdf` and any №011 branding inside the
  rendered PDF are a pipeline-side regeneration task, backlogged; no PDF is renamed or
  regenerated in this design effort.
- `studio/originate/direct-booking-recovery/release.json` is the pipeline's observation
  record and was deliberately not hand-edited; the next `release_audit.py` pass should
  re-observe `site.status` against the reconciled registry.

**Content authority selected.** EP007 (`exit-readiness-prep`) — the first V2 workspace,
Canvas locked 2026-09-01 — is the **canonical private V2 control** for the data contract.
It appears in the contracts/spec docs only; never on an artboard or route. №006 content
may appear on artboards only as `V1-derived design specimen · not V2 gated`. The AI
Visibility fixture is retired from this effort.

**Typography resolved (owner, 2026-09-01).** Site: Zodiak (display + headings), Supreme
(body/UI), Fragment Mono (evidence, numbers, metadata). Boska is dropped from the site
and retained for PDF covers and brand surfaces.

**Copy authority reset (owner, 2026-09-01).** No old site copy is locked authority. The
generalized `$2–8K/mo` disclosure row is removed; cadence claims re-reviewed; "Model
status" replaces "overall evidence class" in UI naming; leading H1 candidate: "You can
build it now. We help you decide what's worth testing." Rev D's internal line "Human
consequence. Operating clarity." is removed everywhere.

**Scope deviation, owned.** Step 1 as executed went beyond the plan's №006-only scope:
too-small-to-bother was renumbered to №005 and five stale queue rows were demoted to
hidden `queued` status. The registry could not be made internally consistent otherwise —
№005/№006 collided with retained queue indices on rows the plan left for backlog. The
five hidden rows keep their old indices; that residual cleanup stays backlogged.

**Adversarial contract review (3 verifiers, 2026-09-01).** Findings applied: voice.md §3
(em-dash ban, contractions) added to the copy-deck and drift rules after six proposed
strings tripped it; the "Secrets" disclosure row renamed "Held-back material" (HYPE_WORDS
matches substrings, so "secrets" hits "secret"); the `Building got cheap. Deciding
didn't.` H1 candidate struck (§2e duplicate shell of the retained format kicker); the
library empty state de-references EP007; token-name corrections in the drift table
(`--blue-500`, `--blue-900`, `--tracking-heading`); the data contract gained the
no-self-hash citation fix, nullable kill conditions, optional break-even/cash-timing
fields, the 4-identity/18-public-layer field split, and a Latest-Canvas derivation guard.

## 2026-09-01 — Step 3: core prototypes built (B1/B2 + B3)

`artboards/B1-canvas-page.html` — the Canvas page prototype, desktop and mobile in one
responsive file (B1 and B2 per the spec's one-file note). №006 content re-rendered from
the LP mockup onto real tokens, `V1-derived design specimen · not V2 gated` baked into
the titleblock. Working interactions: guided-walkthrough toggle (URL-hash synced,
back/forward restorable), capability tabs (roving focus, arrow keys), mobile-only
scenario lens (desktop shows all three columns side by side), mobile nav (Escape closes,
aria-expanded), screen-reader announcements via a live region. `artboards/B3-method.html`
— the Method page with pipeline + gates schematic, the canonical evidence-class legend,
Model status vs economics rules, versioning with the copy-hash demo, and the
claims-discipline card.

Build decisions:
- Tokens are **inlined verbatim** into each artboard (the five token files, source of
  truth unchanged) because the review environment loads pages in ways that break relative
  stylesheet links. The inlined token files carry their original comments, including em
  dashes — those are CSS comments, not rendered strings; the rendered-text gate check was
  run on the live page text and is clean.
- Verified in-browser: desktop 1280 render, guided mode on/off, 375px and 320px reflow
  with zero horizontal page scroll (fixed a grid min-content overflow with `min-width: 0`
  on shell children + wrappable chips under 720px), mobile menu open/close.
- Preview: `python3 -m http.server 8899` from the repo root (`.claude/launch.json`
  "artboards" entry), then
  `http://localhost:8899/design-system/explorations/site-redesign-2026-09/artboards/B1-canvas-page.html`.

Awaiting owner review of the contracts (step 2) and prototypes (step 3) before step 4
(reader, keyboard, screen-reader, and mobile testing) and step 5 (expansion artboards).

**Carve-outs recorded (pending owner confirmation at the step-2 review):**
- Kicker `Stop climbing. Start building.` is §2e-shaped (mirror-image imperative pair).
  Retained as an existing brand mark; it consumes the hero viewport's one-antithetical
  budget. Owner may instead retire it.
- `Build. Own. Operate.` is a rule-of-three brand mark, footer-only; exempt from the §2e
  structural-tell pass by this recorded decision.

## 2026-09-01 — Step 4: internal testing passes (fallback mode, weaker evidence)

External readers were not recruited; per the product contract's fallback, moderated
internal passes substituted, **flagged here as weaker evidence than real-reader testing**.
Method: three fresh-context reader simulations (personas from the editorial standard's
three core-viewer situations) answering the T1–T4 comprehension tasks against the
prototype's verbatim rendered text, plus a hostile accessibility/progressive-enhancement
source audit and live keyboard/history/mobile passes in the browser.

**Comprehension results: T1–T4 passed by all three readers.** All identified buyer, offer,
and first test from the decision summary; all correctly explained the evidence classes and
stated plainly that the $135K figure is arithmetic, not a fact; all located stop
conditions; all answered that downloading does not subscribe them to the newsletter,
citing the unchecked consent row.

**Reader findings applied to B1:** PARALLEL was referenced but unlearnable on-page →
definitions link added to the rail status block; specimen/status jargon opaque →
plain-language explainer added under the titleblock chip; disabled download card read as
contradictory → "preview only, controls inactive" caption added; the page never named its
most sensitive assumption → a Most-sensitive-assumption callout added to Sheet 03 (the
data contract already carries the field); the cancellation figure reworded to plain rates.

**Reader findings noted, not actioned here:** every observed figure traces to one
vendor-published source (honest but thin — an editorial matter for real Canvases, where
Step 0 sourcing rules apply); the №006 episode title uses the top of the page's own
18–30% observed band — recorded as a packaging-fidelity concern for the Step 7 proposal.

**Accessibility audit: 2 blockers + 12 should-fixes, all applied to B1** (mobile no-JS
scenario columns un-clipped; observed-chip text moved to ink-700 with sage border/dot;
undefined --text-primary/--text-secondary aliased in every artboard; lens tablist
aria-controls/roving tabindex/dynamic tabpanel roles; no-JS hides dead controls and shows
the mobile nav; duplicate live region removed; rail links preserve guide state in the
hash; navy focus outline; scroll margins; heading order h4→h3; focusable tabpanels;
provenance Expand/Collapse state label; new-tab sr text; table name; nav target padding;
announce-noise guard; Home/End keys; resize fallback for the lens media query). Verified
live after fixes: keyboard, history restore, 375/320 reflow, mobile lens semantics, zero
console errors.

**Token-layer recommendation (design-system owner's call, not made here):** --sage-700
(#5E7F6A) fails AA as 12px text on paper (4.19:1 on paper-0). The artboards route around
it; the audit suggests darkening toward ~#557463 in design-system/tokens/colors.css.

## 2026-09-01 — Step 5: expansion artboards built

B4/B5 homepage (responsive; featured-panel states a and b, state c specified not mocked;
leading H1 candidate rendered pending the copy-deck pick), B6 library (All/Canvases/Legacy
filters, six legacy cards in publication order, empty-Canvases state), B7 legacy episode
(№002 real data; legacy band; "Modeled range · yr 1" fix with the surviving ESTIMATE chip;
null-url source rendered unlinked and annotated), B8 component sheet (all subsystem
components on paper and navy with the per-surface gold ramp; the provenance sample hash is
the SHA-256 of an empty file, labeled as such), B9 PDF cover + Public-layer spread (Boska
permitted on the cover). All token-inlined, voice-gate greps clean, verified in-browser.
