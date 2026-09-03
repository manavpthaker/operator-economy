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

## 2026-09-01 — Step 6: Step 7 sub-proposal drafted

`operator-blueprint-v2/07-publishing/STEP7-v0.1-CHANGE-PROPOSAL.md` written in the house
proposal pattern (status proposed, production authorization none, explicit "It does not"
list, hash snapshot over the four contracts + eight artboards + the historical LP mockup,
approval template included). It ports only the web and reader-tool sub-scope; title,
thumbnail, captions, metadata, upload handoff, and release validation stay boundary-only.
The Step 7 README gained a one-line pointer without any status change. External reader
testing (5–7 readers) is recorded in the proposal as still owed before the implemented
site ships. Step 7 of the effort sequence — recording owner approval — is the owner's
act and remains open.

## 2026-09-01 — Owner review of B4: display typography reverted

The owner reviewed the homepage artboard and preferred the old homepage's large bold
headings; the Zodiak-only direction read flat. The drop-Boska decision is superseded:
**Boska returns as the site's display layer** (one display heading per page, never below
its 40px floor — 62px hero / 60px page titles on desktop, 42–44px on mobile), with
Zodiak, Supreme, and Fragment Mono unchanged beneath it. Applied across B1/B3/B4/B6/B7;
the B4 hero also regained the margin revision rail (site rev badge, sources line,
recomputed note, "estimates marked" note) and its single italic word, and the Canvas
explainer heading rose to Zodiak's 44px ceiling. Mobile display overrides were raised
from 32px to 42–44px so the Boska floor is never violated. Re-verified in-browser at 1280
and 375 (no overflow; Boska rendering confirmed). The Step 7 proposal's hash snapshot was
refreshed for the changed artboards; the proposal remains unapproved, so the refresh
changes no authority.

## 2026-09-01 — Owner review round 2: hero H1 reverted; surface variation added

The owner kept the old homepage's H1: the hero now renders the live site's "It's easy to
build now. It's hard to know *what* to build." (the italic moves to "what", staying inside
the one-italic budget; "easy" is a context-reviewed word the live site already ships and
the owner has now explicitly re-chosen — the H1 candidates list is closed). The fresh
candidates remain in the copy deck as history only.

"Things blending together": the flat single-surface treatment was replaced with the old
homepage's surface rhythm. The Canvas explainer's paper mini-rail became a **navy
schematic format band** (sheet tag, Running pulse, wired nodes with gold counts, navy
chip variants, gold onward link) mirroring the live format band; library and B6 cards
gained the design system's sheet idiom (2px drafting-blue top rule); the disclosures
table gained sunken zebra rows and stronger answer text; on the Canvas page, sheet tags
became drafting-blue with a rule accent, decision-summary cells gained the top rule, the
unknown register gained ledger zebra rows, and the titleblock spec grid sits sunken.
One accent per composition holds: blue carries structure on paper, gold carries the one
highlight per navy band. Verified at 1280 and 375 (no overflow; Boska hero at 42px on
mobile). Step 7 proposal hashes refreshed for B1/B4/B6 (proposal remains unapproved).

## 2026-09-01 — H1 settled: locked v4

After seeing the live-site line rendered, the owner selected the locked v4 H1: "You can
build it now. We show you what's worth building." (italic on "worth", the hero's one
italic). This closes the H1 question with the line brand/copy.md always recorded as
locked; the review's fresh candidates stay in the copy deck as history. B4 hash refreshed
in the Step 7 proposal (still unapproved).

## 2026-09-01 — Owner review round 3: the canvas grammar

The owner flagged that the drafting line grid ("checkered") is Blueprint-era language
while the V2 artifact is a Canvas, and that surfaces still blended. An exploration-level
grammar shift was applied (tokens untouched; recorded for the design-system owner as a
Rev-direction candidate):

- **Texture states the regime.** Legacy/V1 surfaces keep the 36px blueprint line grid
  (the homepage hero panel, featuring the №006 Legacy Blueprint, deliberately keeps it).
  Canvas/V2 surfaces get a **dot grid** (radial points at 32px on navy via --schem-wire,
  28px on paper via --rule): plotting points and canvas weave instead of drafting lines.
  Applied to the format band, newsletter band, capability map, and the Canvas shell.
- **Zone accents.** Each Canvas sheet is a color zone from the existing palette:
  Opportunity drafting-blue, System blue-500, Evidence sage, Economics gold, Guardrails
  brick. Carried by the 3px sheet top border, the tag bar (tag text colored only where it
  passes AA at 12px; Evidence keeps ink text over a sage bar), tinted rail indices, and
  zone underlines on the homepage format-band nodes. One accent per composition holds
  per zone.
- **Ghost numerals.** Library cards carry their publication number as a large paper-200
  mono numeral (data-num), giving cards identity without new color.

Verified at 1280 and 375, no overflow. Step 7 proposal hashes refreshed for B1/B4/B6
(proposal remains unapproved).

## 2026-09-01 — Owner review round 4: navy kept, palette spent harder

Asked whether to change the dark blue or add accents, the recommendation (applied) was
neither: the navy is a cross-surface brand constant and new hues would break the
one-accent rule and dilute the evidence-class color coding. Instead the existing system
was used at greater intensity:

- **Deep-navy layering.** Proposed token candidate `--blue-950: #0D1A2C` (the LP mockup's
  navy-deep, previously flattened away). Page-level canvas bands (format band, newsletter
  band, capability map) drop to the deep layer; nodes and tabs sit on solid `--blue-900`,
  producing real depth inside navy. Declared artboard-locally as `--blue-950-candidate`;
  adopting it into `design-system/tokens/colors.css` is the design-system owner's call.
- **Tint washes.** The Canvas page's decision summary sits on a `--blue-tint` band.
- **The gold gap figure.** The design system's licensed big-accent idiom, previously
  unused on any artboard: `5 sheets → 1 decision` in gold mono bridges the explainer into
  the format band (a structural method figure, no sourcing burden; the paper
  composition's single gold accent).

Verified at 1280; hashes refreshed in the Step 7 proposal (still unapproved).

## 2026-09-02 — Boundary Ledger landing-page direction locked

After reviewing the palette, page-density, photography, and illustration iterations, the owner
selected **Boundary Ledger** as the landing-page visual direction and approved the rough hotel,
OTA, and guest working model as the reference episode treatment.

The lock preserves a clean editorial page around one expressive episode illustration. Blueprint
and wireframe language lives inside the deliberately imperfect hand-drawn model rather than in a
checkered page background or dense label system. The dark mineral latest-episode card remains the
accountable docket, attached to the drawing's blank top edge without covering the oxide direct-
return loop. The full 3:2 drawing remains uncropped on desktop and mobile.

The frozen invariants and change boundary are recorded in `palette-options/LOCK.md`. Signal Ledger,
the clean-layout study, and the photographic Working Plate remain historical alternatives. This is
an exploration-level visual lock only: no production tokens, source artboards, Content OS issue
structure, deployment state, editorial approval, or publication authority changed.

## 2026-09-02 — Boundary Ledger design system established

The owner clarified that Boundary Ledger—not the alternate palette—is the sole forward direction
and asked for a design system around the locked working-model illustration language.

`design-system/boundary-ledger/` is now the canonical reference package for new OE web and episode-
illustration work. It contains scoped and honestly named tokens, framework-neutral component
contracts, the accountable docket and working-model composition, page patterns, a browsable field
manual, a self-contained font set, and an episode-art manifest schema. The approved EP006 hotel
model is copied into the package, fixed at 1536 × 1024, and SHA-256 pinned. Its visual-language lock
does not waive the separate manual review required for handwritten facts before publication.

The active palette review now exposes Boundary Ledger only and canonicalizes obsolete palette or
comparison URL state back to the locked direction. The package was verified at 1280, 933, 390, 373,
and 320 CSS pixels: no horizontal overflow, exact 16px docket attachment, complete 3:2 art,
24px mobile docket gutters, full-bleed mobile paper, and 44px key link targets.

This establishes design authority, not a production migration. Root Rev C files remain the current
implementation for existing site, studio, video, Canvas, PDF, and publication consumers until a
separately scoped migration is implemented and verified.

## 2026-09-02 — Boundary Ledger promoted to cross-media semantic authority

The owner clarified that Boundary Ledger’s durable asset is the meaning assigned to material—not
the palette or landing-page composition. Warm paper carries human context and unresolved work;
deep mineral carries accountable evidence; steel carries dependency and rented capability; oxide
carries one commitment, exception, correction, or owned thesis path. Those roles now form a
versioned semantic core with separate color, motion, and sound bindings.

The original landing-page lock remains historical and its 16px docket attachment, 24px mobile
gutter, 3:2 static master, and browser behavior remain web-specific. The portable rule is that the
surface establishes a stable hierarchy, one accountable change is active at a time, and the result
settles. A dramatic opening may begin inside a failure or reroute; the business operation supplies
the energy.

Rev C is retired as forward design authority and remains compatibility implementation only for
named unmigrated consumers. Rev D is retired as an active design direction and retained as narrative
research; its human stakes, reversal, agency, and structural silence survive, while cobalt/gold
semantics, sinkholes, glow, orbit, generic node builds, and runtime promotion do not.

Boundary Ledger 2.0 adds a cross-media authority record, invariant register, semantic core, color /
motion / sound bindings, runtime-neutral scene contracts, motion-ready asset schema, audio-led clip
contract, retirement manifest, and dependency-free cross-file validator. A real 30.405-second EP006
voice excerpt provides model-led and text-led browser references across 9:16, 1:1, and 16:9 using a
precomputed actual-PCM trace. That reference does not claim a layered motion-ready illustration,
encoded master, final mix, cross-category validation, production migration, or publication approval.

## 2026-09-02 — Site rebuilt on Boundary Ledger (owner direction)

The owner directed the rebuild onto Boundary Ledger, the cross-media semantic authority
for new web work (`design-system/boundary-ledger/`). The Rev C artboards (B1–B9) had been
built from the grammar the landing lock forbids outside the illustration: drafting and dot
grids, dense mono labels, engineering title blocks, gold and zone accents. They are
retained unchanged as history (the lock names B4 as its untouched source) and are no
longer the proposed standard.

**New artboard set:** `artboards/boundary-ledger/` — `homepage.html`, `canvas-page.html`,
`method.html`, `library.html`, `legacy-episode.html`, `components.html`, `pdf.html`, plus
`site.css`, a 347-line site binding that adds only what the field manual lacks
(navigation, forms, filters, the guided walkthrough, evidence-class data labels, the
three-view economics grid, the risk-ruled stop list). Every page links the real
`design-system/boundary-ledger/styles.css` and sets `data-oe-theme="boundary-ledger"`;
every value is a `--bl-*` token; no Rev C token, grid, chip, pill, card chrome, gradient,
or gold appears. Fonts and the accountable data face come from the BL binding (system
monospace by design).

**Grammar applied.** Paper carries the page and unresolved work; deep mineral carries the
accountable docket and the one subscription band; oxide marks one commitment per
composition (the hero's italic word, a decision-note edge, the pressed filter, focus);
steel carries navigation, secondary structure, and the evidence-class labels; sage appears
only on the docket's Live dot; risk color appears only on the stop-conditions list. The
homepage and Canvas page open with the EpisodeFeature (rail, thesis, docket attached
exactly 16px into the locked EP006 working model's quiet top edge, the whole 3:2 drawing
uncropped). Evidence classes are typeset `oe-class` data labels, never badges. Cards
became ledger rows; the navy node band became a numbered anatomy list; economics views are
three rule-separated columns; the most-sensitive assumption is a DecisionNote; the
required disclosure is a DisclosureBlock.

**Guided walkthrough** survives as one toggle whose guidance renders as DecisionNotes per
sheet, hash-synced, with a live region; the anchor nav tracks the current sheet.

**Verification.** Rendered over the repo-root server: BL fonts loaded, docket overlap
measured at 16px, image 1536 × 1024 at `object-fit: contain`, zero horizontal overflow at
1280/375/320 on the two core pages; the five builder agents each ran the same overflow,
token, em-dash, banned-word, EP007, and link checks on their pages and rendered them
live. Mechanical gate pass over all seven pages and `site.css`: 0 em dashes in rendered
text, 0 banned words, 0 non-`--bl-` tokens, 0 EP007 references.

**Records.** `03-drift-reconciliation.md` is now historical (Rev C port notes); the BL
binding governs. `01-experience-spec.md` §3A gains the Boundary Ledger component mapping.
The Step 7 proposal's normative references now list the BL artboards and the BL package
files they depend on; the Rev C artboards remain listed as historical input. Boundary
Ledger's own status is unchanged by this work: the production site remains an unmigrated
Rev C consumer until a separately scoped migration is implemented and verified.

## 2026-09-03 — Public hierarchy and copy pass

The Boundary Ledger palette and type system remain unchanged. The artboards were reorganized
around the reader's decision instead of the site's production system.

The homepage now moves from the promise to the latest investigation, three decisions the Canvas
supports, the business list, the trust standard, and subscription. The Canvas page leads with a
three-question decision summary and uses those questions as its section architecture. Method was
reduced to the reader-facing explanation of decisions, evidence labels, process, publication
standard, and revision history. The library is now `Businesses`; artifact-state explanation is a
single formats note. The legacy page carries one disclosure, then moves directly through watch,
business model, economics, sources, and download.

This is an artboard and experience-spec revision only. It does not migrate the production site,
approve №006 as a V2 Canvas, authorize content, or clear any release gate.

## 2026-09-03 — Integrated operation sheet and naming hierarchy

The owner removed the homepage's three decorative research labels and asked for clearer material
separation. The hero now speaks directly to the reader, and the accountable docket and rough
working model are joined into one bordered operation sheet. Raised paper, inset paper, mineral,
and explicit rules now separate major chapters without assigning color decoratively.

The site now distinguishes a stable operation name from release packaging. `Direct Booking
Recovery` leads the site; `Hotels pay 30% to book their own rooms` remains the episode title in
secondary metadata. The same naming model is applied to the other library specimens.

The Operator Economy thesis is removed from the homepage and Businesses because it is not a
buildable operation. Its durable premise is synthesized into Method under `Why this exists`.
This does not delete or alter the historical episode record.

## 2026-09-03 — Material hierarchy extended across the artboard set

The homepage's material hierarchy now governs Canvas, Method, Businesses, Legacy, the component
sheet, and the print specimen. Canvas separates summary, evidence, first test, media, and download;
Method separates purpose, evidence, standards, and revisions; Businesses separates orientation
from the operation ledger and format boundary; Legacy separates the historical boundary, media,
economics, and download. The component sheet now documents `OperationSheet` as the integrated
docket-and-working-model component, and the print specimen removes decorative opening labels.

Colors are assigned by Boundary Ledger role rather than alternated mechanically. This remains an
artboard-system change, not a production-site migration or release approval.

## 2026-09-03 — Working-paper icon and accent language drafted

The owner requested a reusable illustration and iconography language derived from the locked EP006
Working Model. A draft support system now provides nine SVG symbols and three editorial accents for
actors, places, workflows, evidence, economics, tests, stop conditions, routes, and operator loops.
Method and Businesses use hero accents; Canvas uses small section icons. The homepage retains the
full Working Model as its hero illustration rather than adding a competing accent.

Roughness is authored through doubled contours, construction passes, open joins, overshoots, and
sparse hatching; no wobble filter is used. Typeset copy continues to own labels, evidence, status,
and attribution. Oxide appears only on a decision, pin, test, correction, or owned route. The draft
explicitly rejects generic innovation icons and cannot serve as evidence.

The library is reviewable at `design-system/boundary-ledger/illustration-system.html`. Assets and
hashes are recorded in `illustration/system/manifest.json`. Status remains draft for owner review;
the EP006 reference remains unchanged and locked.

## 2026-09-03 — Pencil study 03 after roughness review

The owner found the first two support-system passes too smooth and requested a rougher,
sketch-like hand. All nine marks and three editorial accents have been redrawn. The marks now
use independently authored broken contours, uneven retraces, pressure fragments, construction
overshoots, and selective hatching. Automatic stroke-dash roughness and paper filters are removed.
Full-body actors replace the UI-style busts; an arithmetic sheet replaces the economics growth
arrow; a bounded checklist replaces the experiment flask. Enlarged sheet strokes are rebalanced
so they remain pencil-weight rather than becoming marker outlines.

The draft specimen has shorter headings so the visual studies are easier to review. Site page
layout, publication status, and the locked EP006 illustration are unchanged. The browser check
covered the specimen plus Method, Businesses, and Canvas at 1280, 375, and 320 CSS pixels:
all referenced images loaded and no horizontal overflow was detected. This verifies the
implementation, not owner approval of the drawing language.

## 2026-09-03 — Supporting drawings sit directly on the page

After accepting the pencil-study direction, the owner requested no borders or backgrounds around
the supporting illustrations. Removed the solid SVG canvas fills and the hero illustration's
panel color, frame rules, mat padding, and multiply blend mode. The supporting-art specimen also
removes its icon-cell and illustration frames. Section separators and the locked EP006 working
paper remain unchanged. Method and Businesses were checked at 1280, 375, and 320 CSS pixels:
transparent containers, zero border/padding, loaded images, and no horizontal overflow.
