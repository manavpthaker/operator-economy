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

**Carve-outs recorded (pending owner confirmation at the step-2 review):**
- Kicker `Stop climbing. Start building.` is §2e-shaped (mirror-image imperative pair).
  Retained as an existing brand mark; it consumes the hero viewport's one-antithetical
  budget. Owner may instead retire it.
- `Build. Own. Operate.` is a rule-of-three brand mark, footer-only; exempt from the §2e
  structural-tell pass by this recorded decision.
