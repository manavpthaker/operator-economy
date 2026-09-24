# Canvas data contract — per-episode public projection

Status: draft for owner review (step 2 of the approved redesign sequence).
Owner approval of this document is design approval only — no content or production
authorization.

This is a specification, not code. The locked Canvas markdown remains the authority; the
JSON is a downstream projection that stores its source's hash (the no-self-hash rule:
`operator-blueprint-v2/01-editorial/03-canvas/OPERATOR-CANVAS.template.md:394` — "Store it
in dependent artifacts and the editorial lock; do not place a self-hash inside this
file"; a changed upstream field invalidates dependents per `STAGE-GATES.md:283-293`).

Text precedence: locked Canvas text is verbatim authority. Language hygiene, including
voice.md §3 punctuation and contractions, is enforced at Canvas lock (Gate E5V), not
patched in this derivation. Strings the derivation itself authors (labels, receipts,
UI-facing glue) must pass voice.md §2 and §3.

**Validation control: EP007** (`operator-blueprint-v2/episodes/EP007-exit-readiness-prep/01-editorial/operator-canvas.md`,
locked 2026-09-01). EP007 is private Step 1 material: it validates this schema in this
document only and appears on no artboard and no route.

## 1. Files and coexistence

- One file per canvas-bearing episode: `site/data/episodes/<slug>.json`, produced by a
  future Step 7 derivation (`render_canvas.py`, backlog) from the locked Canvas markdown.
- `site/data/episodes.json` stays as the index. Additive fields only:
  `artifact_kind`, `regime`, `authority_state`, `publication_state`, `is_current_revision`,
  `is_latest_eligible`, `canvas_ref` (path to the per-episode file; canvas-bearing entries
  only). Legacy V1 entries keep all existing display fields and never get a canvas file.
- Superseded revisions are immutable: a new revision writes a new file
  (`<slug>.rev-<X>.json` retained alongside the current), and the index's
  `is_current_revision` moves. Old revisions stay reachable and labeled.

## 2. State model

Orthogonal fields; every UI label derives from this matrix, never from a single enum.

| Field | Values | Meaning |
|---|---|---|
| `artifact_kind` | `canvas` \| `legacy_blueprint` | What kind of artifact this is |
| `regime` | `v1` \| `v2` | Which evidence regime governs it |
| `authority_state` | `fixture` \| `draft` \| `locked` \| `superseded` | Editorial authority of the content |
| `publication_state` | `unauthorized` \| `ready` \| `scheduled` \| `live_incomplete` \| `live` | Release status |
| `is_current_revision` | boolean | Whether this file is the current revision |
| `is_latest_eligible` | boolean | Whether this entry may be featured as "Latest" |

Derived answers the spec relies on:

- **"Latest Canvas"** = the canvas-kind entry with `is_latest_eligible: true`,
  `authority_state: locked`, `publication_state: live`, highest publication number.
- **Before the first live V2 Canvas exists**, no entry qualifies; the homepage hero CTA
  falls back to `See how the Canvas works →` → `/method`, and the navy panel features the
  newest live legacy episode.
- **Search visibility:** `noindex` unless `publication_state: live` and
  `authority_state: locked`.
- **№006 dedup:** `direct-booking-recovery` will be recorded as
  `artifact_kind: legacy_blueprint`, `regime: v1` when the fields are added to the index.
  If a design specimen of its canvas is ever published, it would be a *separate* entry
  with `authority_state: fixture`, never a second live episode page. A real
  `/canvas/direct-booking-recovery` requires an explicit V2 port and E3 lock first.
- **Derivation guard:** the Latest-Canvas computation filters to canvas-kind live entries
  *before* comparing numbers — the index currently retains old queue indices on hidden
  `queued` rows (duplicate raw `number` values; cleanup backlogged), so a naive
  max-by-number over all rows is wrong.
- **№006/№005 numbering:** the index carries `number` (publication) and
  `legacy_queue_number` (traceability), reconciled 2026-09-01.

## 3. Schema

Top-level blocks of `site/data/episodes/<slug>.json`:

```jsonc
{
  "schema_version": 1,

  "identity": {
    "number": 7,                          // publication number; null only for fixtures
    "slug": "exit-readiness-prep",
    "short_public_category_title": "Exit readiness",
    "spoken_company_name": "a sale-readiness practice",
    "one_line_definition": "It makes a small business able to survive a buyer's inspection.",
    "internal_operating_description": "…"  // retained outside first-listen narration
  },

  "provenance": {
    "canvas_rev": "A",
    "lock_date": "2026-09-01",
    "template_version": "operator-blueprint-v2-step1-v1.5",
    "model_status": "adjacent_synthesis",  // observed_model | adjacent_synthesis | frontier_hypothesis
    "canvas_sha256": "<full hash of the locked source markdown>",
    "projection_sha256": "<full hash of this JSON, computed after write, stored in the index>",
    "approval_ref": "operator-blueprint-v2/episodes/EP007-…/01-editorial/operator-canvas.md",
    "revision_history": [
      { "rev": "A", "date": "2026-09-01", "changed": "initial lock" }
    ]
  },

  "state": {
    "artifact_kind": "canvas",
    "regime": "v2",
    "authority_state": "locked",
    "publication_state": "unauthorized",
    "is_current_revision": true,
    "is_latest_eligible": false
  },

  "public_layer": { /* §4 — every field an EvidencedStatement */ },
  "economics":   { /* §5 */ },
  "unknowns":    [ /* §6 */ ],
  "risks":       [ /* §6 */ ],
  "first_test":  { /* §6 */ },
  "sources":     [ /* §7 */ ],
  "required_disclosure": "Modeled scenario, not observed performance or an earnings forecast.",
  "media":       { "youtube_url": null, "audio_url": null, "transcript_ref": null },
  "download":    { "pdf_ref": null, "pdf_sha256": null, "edition_date": null }
}
```

### 4. `EvidencedStatement` — the core type rule

**No material claim is a bare string.**

```jsonc
{
  "text": "Only about 30% of listed small businesses successfully sell.",
  "evidence_class": "OBSERVED",           // OBSERVED | PARALLEL | MODELED | UNKNOWN
  "source_ids": ["CLM-001"],              // required non-empty for OBSERVED
  "assumptions": []                        // required non-empty for MODELED
}
```

`public_layer` carries the template's Public Canvas layer fields
(`OPERATOR-CANVAS.template.md:316`), each as an `EvidencedStatement` or a small structure
of them: `buyer`, `problem`, `offer`, `result`, `delivery_loop` (ordered steps),
`stack_by_capability` (rows: capability, owner: `operator | ai_assisted | licensed_third_party`,
note), `ai_role`, `human_judgment_retained`, `business_of_one_boundary`,
`first_customer_path`, `entry_wedge`, `aspirational_destination`,
`proof_required_before_expansion` (ladder rows: stage, adds, proof_required),
`economics_disclosure`, `modeled_livelihood_requirement` (see §5),
`reachable_share_assumption`, `first_construction_step_and_test`, `biggest_risk`.

The overall `model_status` and per-statement `evidence_class` are different things and are
never merged in data or UI.

### 5. Economics — no headline-number field exists

The schema deliberately cannot carry a `"$2–8K/mo yr 1"`-style string. Structure:

```jsonc
{
  "equations": [
    { "label": "revenue",  "lines": ["customers × price × billing frequency = modeled gross revenue"] },
    { "label": "cost",     "lines": ["labor + tools + vendors + acquisition + delivery overhead = modeled direct cost"] },
    { "label": "capacity", "lines": ["available delivery hours ÷ hours per customer = modeled maximum active customers"] }
  ],
  "assumptions_table": {
    "columns": ["low", "base", "high"],
    "rows": [
      { "assumption": "Price per engagement", "low": "$6,000", "base": "$12,000", "high": "$20,000",
        "evidence_class": "MODELED", "basis": "Transferred from compliance-readiness project pricing" }
      // … one row per assumption; every row labeled
    ]
  },
  "worked_case": { "label": "base case contribution", "lines": ["8 × $12,000 = $96,000 gross", "…", "contribution = $86,000"] },
  "capacity_check": { "lines": ["8 × 85 = 680 delivery hours against ~900 available"] },
  "livelihood": {
    "modeled_owner_compensation": "$120,000",
    "required_customer_count": { "text": "roughly 11 engagements at the base fee, more than the modeled capacity comfortably allows. At 8 engagements the fee must rise to about $16,250.",
                                 "evidence_class": "MODELED", "assumptions": ["base price $12,000", "85 hours per engagement"] },
    "clears_base_case": false              // EP007 control: the base case FAILS and the schema must say so
  },
  "break_even": { "lines": ["roughly 1 engagement per year covers fixed overhead"] },   // optional
  "cash_timing_note": "fixed-fee engagements should stage payments…",                    // optional
  "most_sensitive_assumption": { "text": "Delivery hours per engagement…", "evidence_class": "MODELED", "assumptions": ["owner interview time does not compress"] },
  "disclosure": "Modeled scenario, not observed performance or an earnings forecast."
}
```

Rendering rules bound to this structure: desktop shows the low/base/high columns side by
side with shared assumptions always visible; single-pane switching is mobile-only; no
blended or summary total exists in any state; `clears_base_case: false` renders as
content, never softened.

### 6. Unknowns, risks, first test

```jsonc
"unknowns": [
  { "id": "U001", "unknown": "Will an owner pay before a deadline exists?",
    "classification": "safe_first_test" }   // safe_first_test | later_stage_blocker
    // The template's third class, "current E3 blocker", is unreachable here by
    // construction: a canvas with an E3 blocker cannot reach authority_state: locked.
],
"risks": [
  { "risk": "Owners will not pay before a deal exists", "why_it_matters": "…",
    "early_warning": "…", "mitigation": "…",
    "kill_condition": "…",                 // nullable — EP007's sixth risk records none
    "evidence_class": "UNKNOWN" }
],
"first_test": {
  "thirty_day": [ { "step": "Build the checklist and publish it.", "note": "…" } ],
  "success_signal": "…", "failure_signal": "…", "kill_or_redesign_condition": "…"
}
```

`unknowns` is required and non-empty for any locked canvas — UNKNOWN is designed content.

### 7. Sources

```jsonc
{ "id": "CLM-001", "title": "…", "publisher": "…", "date": "…",
  "url": "https://…",            // non-null REQUIRED — closes the V1 `url: null` gap
  "accessed": "2026-09-01", "receipt_text": "SOURCE: <publisher> · <year>" }
```

Every `source_ids` reference must resolve. Satisfies the exact on-screen receipt + full
show-note citation obligation (`STAGE-GATES.md:215`).

## 8. Validation rules (enforced by the future derivation, checkable by `release_audit.py`)

1. Every `MODELED` statement has ≥ 1 assumption.
2. Every `OBSERVED` statement has ≥ 1 resolving `source_id`.
3. Every `UNKNOWN`-class statement **that projects into this JSON** maps to an `unknowns`
   row. (Canvas-internal UNKNOWN notes that stay in the source markdown, like EP007's
   excluded multiple-uplift figures, are out of the projection's scope.)
4. No modeled figure text contains "typical", "conservative", "realistic", "reasonable",
   or "achievable" (Gate E5, `STAGE-GATES.md:208`).
5. All text passes the `HYPE_WORDS` / `voice.md` §2 lexicon check.
6. `required_disclosure` is non-empty and matches the locked Canvas.
7. `canvas_sha256` matches the locked source file; `projection_sha256` matches the JSON;
   `download.pdf_sha256` matches the PDF binary — three separate hashes, all displayed.
8. `sources[].url` is non-null.
9. A `publication_state: live` entry requires `authority_state: locked` and an
   `approval_ref`.
10. Derivation-authored strings (labels, receipt text, UI glue — not locked Canvas text)
    pass voice.md §3: no em dashes, contractions used (see the precedence note in the
    header; locked text is verbatim and §3-clean by Gate E5V at lock time).

## 9. EP007 control check (manual transcription pass, 2026-09-01)

EP007's locked Canvas transcribes losslessly: three equations → `equations`; the 5-row
low/base/high table with per-row labels → `assumptions_table`; the failing base case →
`livelihood.clears_base_case: false` with the $16,250 alternative in
`required_customer_count`; the break-even line and cash-timing risk → the optional
`break_even` / `cash_timing_note` fields; five unknowns with classifications →
`unknowns`; six risks, five with kill conditions (the sixth records none — nullable) →
`risks`; CLM-001–004 → `sources` (urls carried from the Step 0 claim registry at
derivation time); the required disclosure string matches verbatim; the Public Canvas
layer's 22 fields all land in the projection — 4 in `identity` (category title, spoken
name, one-line definition, internal description) and 18 in `public_layer` — with their
inline labels preserved. Nothing in EP007 required a field the schema lacks; the schema's
no-headline rule required nothing EP007 contains to be dropped.
