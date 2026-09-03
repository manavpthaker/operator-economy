# V2 Step 7 v0.1 change proposal: the web and reader-tool sub-scope

Status: **proposed. Not approved. Not authoritative.**

Proposal date: 2026-09-01 (hash snapshot refreshed 2026-09-02 after the rebuild on Boundary Ledger)

Prior authority: the Step 7 boundary stub (`README.md`, "boundary only; not yet ported or
authoritative")

Production authorization: **none**

## Why v0.1 is required

Step 7 owns "episode page, public Operator Canvas, metadata, captions, upload handoff, and
release validation" and is a five-line stub. Meanwhile the site redesign effort
(`design-system/explorations/site-redesign-2026-09/`) has produced a tested experience
architecture, a Canvas data contract validated against the first locked V2 Canvas (EP007),
and nine reviewed artboards. That work is the de-facto standard for how a Canvas reaches a
reader on the web. Leaving it as a site-side convention outside V2 governance would let
the delivery surface drift from the editorial system it serves. This proposal ports
**only the web and reader-tool sub-scope** of Step 7 out of boundary status, so the
standard can be adopted or corrected upstream.

## Proposed scope (the partial port)

If approved, Step 7 gains authority over exactly four things:

1. **Episode/Canvas page anatomy.** The canonical scroll: titleblock with Model status and
   provenance → one-screen decision summary → the Canvas as five sheets (Opportunity /
   System / Evidence / Economics / Guardrails) with a single guided-walkthrough toggle →
   episode media as supporting material below the tool → per-Canvas required disclosure →
   gated PDF download with separate newsletter consent → provenance panel. Defined in
   `01-experience-spec.md` §3; prototyped in artboards B1/B2.
2. **Public Canvas delivery.** The web rendering is public and carries every load-bearing
   source, assumption, risk, unknown, and disclosure; the PDF is the email-gated print
   edition that adds detail, never information required to judge the opportunity. Download
   fulfillment and marketing consent are separate records and separate choices, opt-in
   unchecked. Flows (first-time, repeat, expired link, failure, suppression, deletion) per
   `01-experience-spec.md` §6. `/privacy` is a launch requirement; the unresolved legal
   operating entity is an owner decision that blocks launch and may not be worked around.
3. **The Canvas data contract.** The per-episode JSON projection
   (`02-canvas-data-contract.md`): EvidencedStatement as the core type (no material claim
   is a bare string), an economics block with no headline-number field, the orthogonal
   state matrix (`artifact_kind` / `regime` / `authority_state` / `publication_state` /
   revision flags), and triple-hash provenance (source Canvas markdown, JSON projection,
   PDF binary). Validated by lossless transcription of EP007's locked Canvas, including
   its failing base case.
4. **Artifact states and labeling.** `Legacy Blueprint` for V1 artifacts (never
   retroactively relabeled), `Operator Canvas` for locked-and-live V2 artifacts,
   `V1-derived design specimen · not V2 gated` for design specimens (noindex, no canvas
   lock, no canonical hash, no published PDF), and superseded revisions kept published,
   labeled, and unchanged.

**Remaining boundary-only** (unchanged by this proposal): final title and thumbnail,
captions, metadata, upload handoff, and release validation.

## Evidence behind the proposal

- The product contract (`00-product-contract.md`) defines the reader job, four
  comprehension tasks, a testing protocol, and the measurement schema.
- Internal testing (2026-09-01, fallback mode, recorded as **weaker evidence** than
  real-reader testing): three fresh-context reader passes cleared all four comprehension
  tasks on the B1 prototype; an adversarial accessibility audit's two blockers and twelve
  should-fixes were applied and re-verified live. Full record in `decision-log.md`.
- Reader-testing with 5–7 representative external readers remains owed before the
  implemented site ships; this proposal does not substitute for it.
- Packaging-fidelity note surfaced by testing, for future Step 7 packaging work: the №006
  episode title uses the top of its own reported 18–30% commission band. Step 1's locked
  promise binds final packaging (`EDITORIAL-STANDARD.md:245-247`); title/thumbnail
  authority stays boundary-only, but the observation is recorded.

## Normative references

| Artifact | SHA-256 |
|---|---|
| `design-system/explorations/site-redesign-2026-09/00-product-contract.md` | `b09ca647ae0fb14da8a5d0fd24f5f34db57d7d34f7fdb3ab89a16899f72cca67` |
| `design-system/explorations/site-redesign-2026-09/01-experience-spec.md` | `79004940bb7507dd1a3870804354960b10750ae8750a0d8f18738c59827a1174` |
| `design-system/explorations/site-redesign-2026-09/02-canvas-data-contract.md` | `20dcd546b855b60b35d53e99ab9dc518f7a893245a84e21cfa1ec339945a366d` |
| `design-system/explorations/site-redesign-2026-09/03-drift-reconciliation.md` | `087fca70ec91d307a1be7427766adee97f7942548f023665c556a1b3b0182e52` |
| `…/artboards/B1-canvas-page.html` | `f338ab78188aebcff47180ce4a36a33da2b223d8601743667b542ffca526798a` |
| `…/artboards/B3-method.html` | `0d2dacf47d15d871e120fe9f61f355829352bcc2b79feae1ef14b81fe2f97c6f` |
| `…/artboards/B4-homepage.html` | `ecff362822b47523907c8694a4d59a70a9a5a4f03608b5596ffdb356bdd07755` |
| `…/artboards/B6-library.html` | `17b568705f9b9d492d7d8bd3c2753349dbf835897a0ae9a79d00a3544b657b1a` |
| `…/artboards/B7-legacy-episode.html` | `3f7119da42f435a88b5230aa7eaa0c428ba1ad8e5f8da3d8b35a5e8f6564af45` |
| `…/artboards/B8-components.html` | `2e0c321df0517f41eac6d89ade7a119e7b8875dd36ee377a16836fcf1915c3fa` |
| `…/artboards/B9-pdf.html` | `003cb9fca277fac0287fcf5c2706d6515ae8474c14504349507d89560d903e31` |
| `design-system/explorations/rev-d/operator-canvas-lp-mockup.html` (historical input) | `c8a1dd0cbb7a74ae3d769dc1f08bb23e1db064a95a611c04b8f6417b64ed24f9` |

**Boundary Ledger artboards (current proposed standard, 2026-09-02):**

| Artifact | SHA-256 |
|---|---|
| `…/artboards/boundary-ledger/site.css` | `851a0544e38c1faeafda0eed9b9b52824381eef0c9f2bbdec1f6d558cc788605` |
| `…/artboards/boundary-ledger/homepage.html` | `22c4e5932ed5d596d65bda25b77472af7115af51d03533396f33c29ae8dc72fb` |
| `…/artboards/boundary-ledger/canvas-page.html` | `d35a7d61113aa09e588963081af92507929b821c6fecadef2f98ebfe12e5e531` |
| `…/artboards/boundary-ledger/method.html` | `61aae71026f9f4c98075de3150ba82bb29e6b4f5bd131235161d4b457c060add` |
| `…/artboards/boundary-ledger/library.html` | `fce1462867cbb09363c2b5ea79ab0ff6e5b6614bbee79dd8cfdf62a30ca876cd` |
| `…/artboards/boundary-ledger/legacy-episode.html` | `c2d5ee95cdfc6fc8f2d8700b33298997cada4ef577ba5a93da5bb0106cfae830` |
| `…/artboards/boundary-ledger/components.html` | `bc4545060e6308e3af851c861a14ff9926a22450f757b80fc4ad8ee61571979c` |
| `…/artboards/boundary-ledger/pdf.html` | `11f3b58cf14b2b2917c56758fd6142fe862550659fe1b28381bd33d21d9cd663` |
| `design-system/boundary-ledger/styles.css` (dependency) | `94d14ca688ba02da44b2b27696dfdc6de1a59ac09083360576c4df5bd0d3d65f` |
| `design-system/boundary-ledger/tokens.css` (dependency) | `d46f7af89baef4f2c6fd70c0dfa598f01ae1e8eb9775eaf92d1a56cbeacf5522` |
| `design-system/boundary-ledger/components.css` (dependency) | `692d07e867ee198f2107b3c2bbe4fb8f1291f53d57c2b234957424949e7d6b8d` |
| `design-system/boundary-ledger/illustration/episode-006/hotel-working-model.jpg` (locked reference) | `083533f79798ef04d66b112fa1a2275e1e181074c6e80c22591fc67ea54c6712` |
| `design-system/boundary-ledger/illustration-system.html` (draft support system) | `36052d2241bbd8336924acc97087ceb5b6c57aea1e7feb1b44f8ab6f480e196c` |
| `design-system/boundary-ledger/illustration-system.css` | `f2963f3018737bc223188425c14a4a6deeeac437339648af0bc0b1f432f2ad1f` |
| `design-system/boundary-ledger/illustration/system/manifest.json` | `939676d2fa2534f0085c00692461eb5481723d1a1894373d5a7eda5ff99ed9b3` |
| `design-system/boundary-ledger/illustration/system/icons.svg` | `02c6f0c7546db5f068e8588eb1ef0f2809209f0ed18787a1da03a4e98cffbb09` |
| `design-system/boundary-ledger/illustration/system/owned-route.svg` | `9dc40f1c46957c5a5f8e42a68b75fc9bf90f46632cc54c4cd02e56d708f40cd9` |
| `design-system/boundary-ledger/illustration/system/evidence-pin.svg` | `e62d19bf819ea4f69eaabc19328b363c8ec27bf35de49fedbe21b47233b7de14` |
| `design-system/boundary-ledger/illustration/system/operator-loop.svg` | `4b5bc4fcbae2d44979ba9edf00462959ffe21ec6095cb051b0aec60028d6b5b9` |
| `design-system/boundary-ledger/illustration-language.md` | `822c94245b80eb295e06c18198f66fac1993b7649f1244a31401808461264db0` |
| `design-system/boundary-ledger/README.md` | `4a3615c7f0623e29951898780e61d7a8e3e7bf9d92b005e7f88e8f4399789599` |
| `design-system/boundary-ledger/manifest.json` | `ea0adb6da7403365d0d6f0bd82b167cdeeb7f40b8c8dbfc634ef92fa414c58aa` |

The B-series artboards (`B1`–`B9`) listed above are retained as **historical input** from
the Rev C round; they are no longer the proposed standard. Visual authority for the
proposed anatomy is Boundary Ledger (`design-system/boundary-ledger/README.md`); this
proposal claims no authority over that system.

`decision-log.md` in the same directory is the living review record and is referenced
without a hash.

## It does not

- Promote, number, or create any episode, or alter EP007's private Step 1 status.
- Clear any public fact, named-company claim, modeled economic statement, price, demand,
  outcome, or income claim. Content OS production facts remain blocked where the standing
  approvals say so.
- Alter Step 1's authority over Canvas content, the editorial locks, or the
  locked-promise fidelity rule binding final packaging.
- Claim the boundary-only Step 7 duties: final title and thumbnail, captions, metadata,
  upload handoff, release validation.
- Change Boundary Ledger's semantic core, role meanings, palette, type, or locked EP006 reference.
  The draft supporting illustration library extends the existing Working Model language and remains
  unapproved; the site binding (`site.css`) adds page-level pieces on BL tokens only.
- Relabel, modify, or migrate any V1 artifact.
- Change the design-system token layer (the sage-700 AA finding is recorded as a
  recommendation for the design-system owner, not enacted).
- Authorize implementation, publishing, or release. Building the Next.js site from this
  standard is a separate effort; putting any `/canvas/` route live requires a locked,
  release-authorized V2 Canvas.

## Follow-on backlog (recorded so it survives the effort boundary)

Site implementation of the approved spec (routes, mobile nav, shared primitives,
vocabulary module, decoupling `api/subscribe` from the view layer); external reader
testing (5–7 representative readers) before ship; real gate infrastructure
(`/api/canvas-download` tokenized delivery — today's `/blueprints/*.pdf` files are
world-readable); remaining `episodes.json` hygiene (hidden queued-row indices, missing
`model` fields, `too-small-to-bother.pdf` 404, Neon-vs-Supabase doc mismatch, LinkedIn
URL mismatch); platform basics (OG images, sitemap, robots, 404, analytics per the
measurement schema, version pinning, self-hosted Fragment Mono); pipeline work
(`render_canvas.py` deriving contract JSON + PDF from a locked Canvas, `release_audit.py`
extension to canvas hashes, `publish_mon.sh` dead repo path); №006 PDF regeneration with
№006 branding; the sage-700 token recommendation; legal-entity decision for `/privacy`.

## Approval mechanics

The owner reviews this proposal with the referenced artifacts. On acceptance, an
owner-signed `STEP7-v0.1-APPROVAL.md` records the decision and the hash snapshot, and the
Step 7 `README.md` status line changes to name the approved sub-scope. **Owner approval
of this proposal is design approval only: it authorizes no content, no production, no
publishing, and no release.**

### Approval template (to be completed by the owner, not before)

```markdown
# V2 Step 7 v0.1 approval: web and reader-tool sub-scope

Decision: approve / revise / reject

Approved by:

Approval date:

Scope approved: episode/Canvas page anatomy · public Canvas delivery ·
Canvas data contract · artifact states and labeling (per the v0.1 proposal)

Hash snapshot: as recorded in STEP7-v0.1-CHANGE-PROPOSAL.md

This approval is design approval only. It authorizes no content, no
production, no publishing, and no release.
```
