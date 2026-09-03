# Experience spec — Operator Canvas site redesign

Status: draft for owner review (step 2 of the approved redesign sequence).
Grammar: **Rev D narrative · Rev C evidence system.** All visuals on Rev C tokens; drift
rules and non-regression behaviors in `03-drift-reconciliation.md`; data shapes in
`02-canvas-data-contract.md`; success definition in `00-product-contract.md`.

Owner approval of this document is design approval only — no content or production
authorization.

## 1. IA and navigation

| Route | State | Purpose |
|---|---|---|
| `/` | changed | Permanent brand surface; short Canvas explainer; never embeds a Canvas |
| `/canvas/[slug]` | new | The public Operator Canvas reader tool. No instance goes live without V2 authority (`authority_state: locked`, `publication_state: live`) |
| `/library` | new | One library, dual-state; filters **All / Canvases / Legacy** only |
| `/episodes/[slug]` | kept | V1 legacy pages, URLs unchanged, + legacy band |
| `/method` | new | How a Canvas is made; canonical evidence-class legend; Model status; versioning and hashes; gates. Every evidence chip links here |
| `/privacy` | new | **Launch requirement** (§6) |
| `/about`, `/newsletter` | deferred | Homepage destinations this phase; no separate pages designed |
| `/api/canvas-download` | named, built later | Tokenized PDF delivery (§6) replacing world-readable files |

**Masthead** (one shared component; replaces the two hand-rolled headers): wordmark ·
`Library` · `Method` · `About` (→ `/#disclosures` this phase) · button `Subscribe`
(→ `/#newsletter`). Plus `Latest Canvas` **only when a live locked V2 Canvas exists**
(state model, contract §2). Sentence case; `Canvas` is a proper noun deck-wide; no
"Episodes"/"Blueprints" split.

**Mobile nav (<900px):** persistent `Menu`/`Close` toggle, full-width disclosure panel,
`aria-expanded`, Escape closes, ≥44px targets (non-regression list).

**Footer:** YouTube ↗ · LinkedIn ↗ · Newsletter · Library · Method. `Build. Own. Operate.`
footer-only. Colophon: `Site rev · <date>` + sources line (the "V1 · date" badge is
retired — it collides with regime vocabulary).

## 2. Homepage anatomy

The Canvas is never embedded here. Target length: ~5 viewports desktop.

1. **Masthead.**
2. **Hero** — Rev C split. Left: kicker `Stop climbing. Start building.` · H1 (owner picks
   from the copy deck, §8) · supporting line (the honest promise, cadence-free) · mono
   proof row `Real companies · Sourced numbers · Honest failure modes` · CTAs. Right: the
   keeper navy panel (`LatestCanvasPanel`), state-aware.
   - **CTA logic:** live locked V2 Canvas exists → primary `Explore the latest Canvas →`
     (to that page). Otherwise → primary `See how the Canvas works →` (to `/method`);
     secondary `Watch on YouTube ↗`. "Conflict" is never a CTA or nav label.
   - **Panel states to mock (B4):** (a) **zero-live-Canvas state = current reality**:
     newest live legacy episode featured + the `/method` CTA (matches the data contract's
     fallback); (b) live V2 Canvas featured + the latest-Canvas CTA. A third state (c),
     no live artifact of any kind (panel shows the five sheets as a method schematic), is
     specified here for completeness but not mocked: it is unreachable while six V1
     episodes are live. The (c) trigger is "no live entry of either artifact kind."
3. **The Operator Canvas — explainer, first below the fold.** What it is (the operating
   model behind every episode, published so the reader can judge the opportunity, not just
   watch it); the five sheets as a miniature rail (Opportunity · System · Evidence ·
   Economics · Guardrails) with structural-count figures only (`4 evidence classes`,
   `low·base·high`, `30-day test`); the four evidence chips in one row, each linking to
   `/method#evidence-classes`; one link onward (`See how the Canvas works →` or the latest
   Canvas when live). Explains and links; nothing more.
4. **Library preview** — heading `The library` + subline `Businesses you could build.`
   (no em dash: voice.md §3); 3 cards (dual-state, §5); `Browse the library →`.
5. **Disclosures** — the №000 engineering-title-block format survives; **rows revised**
   (§8): income promises / course at the end of the funnel / held-back material /
   scarcity timers / evidence classes / business model. The `$2–8K/mo` row is removed;
   the old "Secrets" row is renamed because "secret" is a HYPE_WORDS substring hit
   (eval_script.py matches substrings) — new row copy in §8.
6. **Newsletter band** — one email field, tag `newsletter`; cadence copy only as verified
   (§8).
7. **Footer.**

## 3. Canvas page anatomy (`/canvas/[slug]`) — the tool leads, media supports

1. **Titleblock** — №/Rev/lock date/**Model status** (observed model · adjacent synthesis
   · frontier hypothesis, with a one-line gloss + link to `/method#model-status`)/state
   labels (from the state matrix)/copyable full `canvas_sha256`. On the №006 design
   specimen: the label `V1-derived design specimen · not V2 gated` sits in the titleblock,
   baked into markup.
2. **One-screen decision summary** — buyer · offer · result · first test · biggest risk
   (five `EvidencedStatement`s from `public_layer`), each with its chip. A reader who
   stops here can still answer T1.
3. **`Explore the Canvas ↓` anchor + `Guided walkthrough` toggle** — one canvas, full
   workbench by default; the toggle overlays `GuideExplainer` asides (step meta, decision
   question, "What to look at", "Your decision"), progress, Back/Next. **No duplicate
   entry links into the Canvas exist anywhere on the page.** Toggle state and
   current sheet live in the URL hash (deep-linkable, back/forward restorable).
4. **The Canvas — five sheets.**
   - **Sheet 00 · Opportunity** — problem (quantified, chipped, receipted), why now,
     buyer + qualified/unsuitable rules, spoken name + one-line definition, and the
     ladder: aspirational destination → entry wedge → proof required before expansion
     (conditional stages, never a feature list).
   - **Sheet 01 · System** — delivery loop; `CapabilityMap` (capability rows: who/what
     does it, note); AI role vs human judgment retained; business-of-one boundary.
     Tool brands live inside capability details only.
   - **Sheet 02 · Evidence** — claims as `EvidenceCard`s (statement + chip +
     `SourceReceipt`); reachable-share assumption; **`UnknownRegister` co-equal with the
     proof** ("Proof and uncertainty share the same surface").
   - **Sheet 03 · Economics** — `EquationBlock`s; the assumptions table as
     **`ScenarioColumns`: low/base/high side by side on desktop, shared assumption names
     always visible in the left column**; single-pane `ScenarioLens` on mobile only; the
     worked case; capacity check; modeled livelihood requirement + required customer
     count — **a failing base case renders as content, stated plainly, never softened**;
     most sensitive assumption called out; the required disclosure inline. No blended or
     summary total exists in any state.
   - **Sheet 04 · Guardrails** — first-customer path; 30-day plan; success/failure
     signals; kill-or-redesign condition (`Stop or redesign when:` card); biggest risk.
5. **Episode media — supporting material, below the tool.** Video embed + audio + expandable
   transcript. When narrative-first is being tested (Rev D), a visible `Skip to the
   Canvas ↓` action precedes any media band. Missing media state: a plain row naming what
   exists (`Episode: not produced` / `Audio edition: not available`), never an empty
   player.
6. **Disclosure band** — the per-canvas `required_disclosure` string, styled as a design
   element in the disclosures idiom, above the download.
7. **Download** — `DownloadCard`: PDF contents list (full evidence registry, complete
   model, full risk register, test plan — print utility, per the coverage map's
   "Downloadable detail" column); email field + button `Email me the PDF`; **separate
   unchecked consent row** `Also send the newsletter` with its own one-line description.
   Gate statement rendered on the card: *"The page above contains every load-bearing
   source, assumption, risk, unknown, and disclosure. The PDF is the print edition. It
   adds detail, not information you need to judge the opportunity."* PDF hash + edition
   date printed on the card.
8. **Provenance** — `ProvenancePanel`: copyable full hashes (source Canvas · JSON
   projection · PDF), revision history (rev, date, what changed), immutable prior
   revisions linked, `A changed Canvas field creates a new revision` → `/method#versioning`.
9. **Next in the library** (2 cards) + footer.

## 3A. Evidence-class component subsystem

| Component | Role | Rev C base |
|---|---|---|
| `EvidenceChip` | Per-statement 4-class label (replaces the mockup's `vendor-published + modeled`); UNKNOWN gets a designed dashed state, never error styling | Badge |
| `SourceReceipt` | `SOURCE:` receipt + publisher · year · link; onInk variant for navy | CitationChip |
| `EvidenceCard` | Statement + chip + receipt; no figure floats free | Stat + Card |
| `UnknownRegister` | Unknowns table with real visual weight | DataTable + Badge |
| `ScenarioColumns` / `ScenarioLens` | Desktop side-by-side cases / mobile single-pane; no blend slot exists in either API | DataTable + Button tabs |
| `EquationBlock` | Mono equation lines; inherits a MODELED chip | `.oe-mono` + Card |
| `DecisionRail` | Sidebar sheet index / guided-step progress | SheetHeader idiom + Button |
| `GuideExplainer` | Step meta · decision question · what-to-look-at · your-decision | Card + Annotation |
| `CanvasTitleblock` | №/Rev/lock/Model status/state/hash grid | TitleBlock |
| `DisclosureBlock` | №000 table + per-Canvas required disclosure | TitleBlock framing |
| `CapabilityMap` | Capability tabs + detail grid (human judgment / implementation / input / failure mode) | Schematic + DataTable |
| `LatestCanvasPanel` | The keeper navy hero panel, state-aware | Schematic + SchematicNode |
| `DownloadCard` | Gated PDF + separate consent row + state variants | Card + Input + Button |
| `ProvenancePanel` | Copyable full hashes + revision history | TitleBlock row + `.oe-caps` |
| `LibraryCard` | Dual-state card | Card + Badge + GapFigure |

Every state label derives from the state matrix in the data contract (§2 there); no
component invents its own status vocabulary.


### 3B. Boundary Ledger binding (2026-09-02, supersedes the Rev C base column above)

The site is built on Boundary Ledger (`design-system/boundary-ledger/`). The page is
editorial, not a blueprint interface: no grids, dense mono labels, chips, pills, card chrome,
gradients, or gold; blueprint language lives only inside the rough working-model
illustration. Materials carry meaning: paper (human context, the page), deep mineral
(accountable surfaces: the docket, the subscription band), oxide (one commitment per
composition), steel (dependency, navigation, secondary structure), sage (verified live state
only), risk (actual failed conditions only).

| Subsystem role above | Boundary Ledger binding |
|---|---|
| Titleblock / LatestCanvasPanel | `EpisodeFeature`: rail · intro · `AccountableDocket` (mineral, three rows) · `WorkingModel` (whole 3:2, 16px attachment) |
| EvidenceChip | `oe-class` typeset data label (steel monospace), never a badge |
| SourceReceipt / EvidenceCard | `EvidenceReceipt` (source · statement · count) |
| UnknownRegister | `LedgerRow`s with an Unknown data label |
| ScenarioColumns / ScenarioLens | `oe-three` rule-separated columns (desktop); stacked on mobile; no blend slot |
| EquationBlock | monospace lines inside a `LedgerRow` or receipt |
| DecisionRail / GuideExplainer | `bl-anchor-nav` sheet index; guidance as `DecisionNote`s under one toggle |
| DisclosureBlock | `bl-disclosure` rows |
| CapabilityMap | `LedgerRow`s with a three-fact `oe-facts` list per capability |
| DownloadCard | `oe-form` on paper with a separate consent row; the mineral `SubscriptionBand` is the single conversion surface |
| ProvenancePanel | `LedgerRow`s with the three hashes and revision history |
| LibraryCard | `bl-library-row` |
| Stop conditions | `oe-stop` list (the only risk-color use) |

Artboards: `artboards/boundary-ledger/` (homepage, canvas-page, method, library,
legacy-episode, components, pdf) with `site.css` as the site binding.

## 4. `/method` anatomy (B3, desktop + mobile)

1. Titleblock: `Method · how a Canvas is made`.
2. **The pipeline and its gates** — intake → editorial (Canvas + lock) → narration →
   production → publishing, drawn as a Rev C schematic; one sentence per stage; a plain
   reader-terms explanation that a Canvas passes named review gates (evidence checked,
   language checked, owner sign-off) before it locks, and that a failed gate sends it
   back rather than through. No stage claims more authority than the V2 README grants it.
3. **`#evidence-classes`** — the canonical legend. The four chips at full size with the
   template definitions (`OBSERVED` sourced fact · `PARALLEL` transferred from an adjacent
   model · `MODELED` assumption with stated arithmetic · `UNKNOWN` open question) and one
   worked example each drawn from already-published V1 sourced material or structural
   method facts.
4. **`#model-status`** — Model status vs evidence class, in two sentences each; why a
   whole Canvas is classified separately from its statements.
5. **Economics rules** — equations shown, scenarios never blended, failing cases recorded
   as failing, the required disclosure.
6. **`#versioning`** — locks, the three hashes, what a revision is, why old revisions stay.
7. **What we do not publish** — the claims discipline in reader terms (no income promises,
   no modeled figure upgraded by adjectives, unknowns stay visible).

## 5. Library and legacy

**`/library`:** heading `One library. Honest artifact states.` Filters: `All / Canvases /
Legacy` (model filters deferred). Cards:

- Canvas: `№007 · Operator Canvas` + state labels; body = one-line definition; `Explore
  the Canvas →`. (First real instance ships only when a V2 Canvas reaches
  locked + live.)
- Legacy: `№004 · Legacy Blueprint`; body = existing thesis line; note `Canvas migration
  not yet approved.`; `View the episode →`.
- Design specimen (if ever listed): explicit `V1-derived design specimen · not V2 gated`,
  `noindex`, never `Latest`.

**`/episodes/[slug]` (legacy):** existing layout kept + page-top legacy band: `Legacy
Blueprint · V1 standard` + one sentence: *"Published before the Canvas evidence standard.
Sources are listed below; per-claim evidence classes were not assigned."* Site-wide
language fix: label `Realistic yr 1` → `Modeled range · yr 1`. The binary `ESTIMATE` chip
survives on legacy only.

## 6. Consent, download, and privacy

Two records, two choices, never bundled (replaces the bundled capture at
`site/app/episodes/[slug]/EpisodeForms.tsx:80`):

- **Download fulfillment record** — email + slug + timestamp, purpose: deliver this PDF
  and its corrections/revisions for this Canvas only.
- **Marketing consent record** — the newsletter, opt-in unchecked, its own copy, its own
  unsubscribe.

**Flows to design and mock (states on B1's download card):**

| Flow | Behavior |
|---|---|
| First-time download | Submit email → tokenized link emailed (`/api/canvas-download?token=…`); page confirms "Sent to <email>" + resend action. Emailed-link (not immediate) is chosen so fulfillment is verifiable and the address is real; revisit later if testing shows drop-off |
| Repeat download | Same form; a valid prior fulfillment re-sends a fresh link without creating a duplicate record |
| Existing newsletter subscriber | Download form does not re-ask consent; consent row shows `Already subscribed` state |
| Expired/invalid token | Friendly page: what happened + one-click resend to the same address |
| Delivery failure | `download_failed` recorded; page offers retry; repeated failure surfaces a contact path |
| Unsubscribe | Per-tag unsubscribe + a global `stop everything` option; unsubscribing from the newsletter never blocks PDF fulfillment |
| Suppression | A globally suppressed address gets no mail of any kind, including fulfillment — the page then offers no email path and states why |
| Retention/deletion | Fulfillment records kept only as long as the artifact is maintained; deletion honored on request; stated in `/privacy` |

**`/privacy` — launch requirement.** Must state: who operates the site (**the legal
operating entity is an unresolved owner decision in Content OS — launch is blocked on it
and this spec surfaces it rather than working around it**), what is collected (the two
records + measurement events), lawful purpose of each, retention, deletion contact,
processor list (email provider, database, analytics when added), and no sale of data.

**Gate value rule (binding):** the public web Canvas contains every load-bearing source,
assumption, risk, unknown, and disclosure. The PDF adds full detail and print utility.
The email gate must not hide information required to judge the opportunity.

## 7. Accessibility and platform bar

Requirements (tested in sequence step 4; the LP prototype's existing behaviors are the
non-regression floor, `03-drift-reconciliation.md`):

- WCAG 2.2 AA. Complete keyboard operation, visible focus everywhere.
- No hover-only disclosures — receipts and explainers open on click/tap/focus.
- `role="tablist"` semantics + screen-reader announcements for CapabilityMap tabs,
  guided progress ("Step 3 of 5, Evidence"), and scenario changes ("Base case shown").
- Deep links and history: sheet anchors, guided step, and scenario case restorable from
  the URL; back/forward never lose state.
- 200% zoom without loss; 320px and 375px reflow with no horizontal page scroll.
- Transcript readable as text (not canvas/image); PDF edition tagged (headings, reading
  order, alt text).
- Progressive enhancement: with JavaScript off, all five sheets render fully expanded in
  order, all three scenario columns visible, receipts inline — the evidence never needs
  JS to be read. JS adds the guide, lens, and copy-hash conveniences.
- Media lazy-loaded below the fold; performance budget: ≤ 200KB CSS+JS combined for the
  Canvas page shell (fonts and media excluded), Largest Contentful Paint target < 2.5s
  on mid-range mobile.

## 8. Copy deck

Rules: sentence case (`Canvas` is a proper noun deck-wide); UPPERCASE for mono labels
only; ≤ 1 italic per sheet; no term from `content-os/voice.md` §2 lists / `HYPE_WORDS`
(substring matching — "secrets" trips "secret"); no "typical / conservative / realistic /
reasonable / achievable" near a modeled figure; **no em dash in any rendered string**
(voice.md §3 — the #1 AI tell; use a comma, colon, mid-dot, or rewrite) and
**contractions always** (§3); at most one two-beat antithetical construction per viewport
(§2e mirror-shell guard); no number without a source or a structural basis; **no cadence
claim renders unless the owner confirms the operating schedule** (the current site's
"Every Monday" is suspended pending that confirmation — the V1 queue is empty by decision
and V2 has no scheduled episode).

Vocabulary rules (enforced by a shared vocabulary module at implementation):
`Operator Blueprint №NNN` stays on V1 artifacts with the `Legacy` qualifier;
`Operator Canvas` is V2-only; `episode` stays the video noun.

**H1 — owner picks one at this review** (kicker `Stop climbing. Start building.` is
retained as an existing brand mark, but note it is itself §2e-shaped — owner carve-out
recorded in the decision log; it counts as the hero viewport's one antithetical):

1. `You can build it now. We help you decide what's worth testing.` *(leading — the
   review's safer variant)*
2. `You can build it now. Deciding what to build is the hard part.`
3. `One business at a time, examined until you can decide.`
4. `You can build it now. We show you what's worth building.` *(locked v4 — overstates
   what the method establishes; retained for comparison)*

(A `Building got cheap. Deciding didn't.` candidate was struck: it duplicates the
grammatical shell of the retained `The tools got cheap. The judgment didn't.`, which
§2e forbids.)

**Hero supporting line (cadence-free):** `One real business one experienced person could
run: the operating model, the evidence and its limits, the honest economics, and the
first bounded test. The Canvas behind each episode is published here.`

**Reused verbatim (checked against §2 AND §3):** `The tools got cheap. The judgment
didn't.` · `The story opens the door. The Canvas helps you decide.` · `Proof and
uncertainty share the same surface.` · `The first test is bounded. So is the claim.` ·
`One library. Honest artifact states.` · `Build. Own. Operate.` (footer-only brand-mark
carve-out, recorded in the decision log) · the fixed brand string (About/Method opener).

**Adjusted from the mockup (voice.md §3 fixes — em dashes and contractions):**
`Download the Canvas after you have seen what is inside it.` → `Download the Canvas after
you've seen what's inside.` · `The PDF is the print version of this same system — not a
teaser.` → `The PDF is the print edition of this same system, not a teaser.`

**Replaced (gate or accuracy failures):** `Email unlocks the download` → `The PDF arrives
by email. The newsletter is a separate choice.` (the old line reads as gated-content bait
near voice.md §2c's banned "unlocking…" construction, and misstates the consent split) ·
`Get the Blueprints →` → CTA logic in §2 · `Realistic yr 1` → `Modeled range · yr 1` ·
`Switch the lens. Never blend the scenarios.` → desktop shows columns; the mobile lens UI
carries `One case at a time, never blended.` · disclosures row `Unicorn ambitions — none.
These are livings: $2–8K/mo…` → `Unicorn ambitions: none. The economics are modeled per
Canvas, scenario by scenario.` · disclosures row `Secrets — None. Sources instead.` →
label `Held-back material`, body `None. Everything load-bearing is on the page.` ·
`V1 · <date>` badge → `Site rev · <date>`.

**New disclosures row:** `Evidence classes: every material V2 claim carries one.
Observed, parallel, modeled, or unknown.`

**404:** `This sheet doesn't exist.` + library link.

**Newly written copy in this spec** (legacy band, gate statement, method page strings,
state labels, empty/error states) is part of this deck and is checked against every rule
above — §2 lists, §3 punctuation and contractions, casing, and the modeled-figure
adjective ban — before B1 renders it.

## 9. States inventory (every one designed, none discovered in implementation)

Homepage: 3 featured-panel states · zero-live-canvas CTA fallback.
Canvas page: full/guided · desktop columns/mobile lens (low/base/high) · receipts
open/closed · provenance collapsed/expanded · missing video · missing audio · specimen
label · superseded-revision banner (`A newer revision exists →`) · download card: idle,
sent, resend, invalid/expired token, delivery failure, suppressed, already-subscribed.
Library: filters ×3 · empty Canvases state (generic: `The first Canvas is in editorial
development.` — no episode number or slug; naming EP007 publicly would breach its
Step 1 privacy boundary and would need the owner to amend that boundary, not just
approve copy).
Legacy page: legacy band · missing PDF (no download card rather than a 404 link).
Global: 404 (`This sheet does not exist` + library link) · error boundary.
