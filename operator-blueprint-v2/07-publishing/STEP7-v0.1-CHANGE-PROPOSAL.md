# V2 Step 7 v0.1 change proposal: the web and reader-tool sub-scope

Status: **proposed. Not approved. Not authoritative.**

Proposal date: 2026-09-01

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
| `design-system/explorations/site-redesign-2026-09/01-experience-spec.md` | `6c1dbf68f3a36188ea4dc8983ddc7f385f7b11348492bf619662086d581e8ee8` |
| `design-system/explorations/site-redesign-2026-09/02-canvas-data-contract.md` | `20dcd546b855b60b35d53e99ab9dc518f7a893245a84e21cfa1ec339945a366d` |
| `design-system/explorations/site-redesign-2026-09/03-drift-reconciliation.md` | `a10f427abc1ca4f820e751fcf5f8442c6c279be8d246510da5232b3ebf06e3bb` |
| `…/artboards/B1-canvas-page.html` | `71e2d820eb2e3a48d9b188a948e71050f04ada00d6f4d71ccb198bdc9ab96613` |
| `…/artboards/B3-method.html` | `30a2088a375679c8b0d94bfd1ff43a6592a9c12b2d5e82ea2edf751d54edcc8e` |
| `…/artboards/B4-homepage.html` | `41e0ad9c1328a4549dc743c4a9942e66d5aa304785b262f8bb4275c0954b9f1e` |
| `…/artboards/B6-library.html` | `4be5cc33078ccacf5083a3a51e1a67a0513b4c71d05454e242eca49fdc6d5c08` |
| `…/artboards/B7-legacy-episode.html` | `014ebc33502ba3eff4f3f31ca7be57c7342450c28979b09b9a49a707dbbe9a62` |
| `…/artboards/B8-components.html` | `2e0c321df0517f41eac6d89ade7a119e7b8875dd36ee377a16836fcf1915c3fa` |
| `…/artboards/B9-pdf.html` | `003cb9fca277fac0287fcf5c2706d6515ae8474c14504349507d89560d903e31` |
| `design-system/explorations/rev-d/operator-canvas-lp-mockup.html` (historical input) | `c8a1dd0cbb7a74ae3d769dc1f08bb23e1db064a95a611c04b8f6417b64ed24f9` |

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
- Promote Rev D (its validation items remain design-system's own gate; artboards B1/B2
  are offered as evidence toward its episode-page-scroll item, nothing more).
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
