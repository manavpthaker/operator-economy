# Step 0: opportunity intake and validation

Status: approved V2 Step 0 authority; Step 0.2 locked 2026-08-21; active queue empty.

Approval record: `STEP0.2-APPROVAL.md`

Step 0 decides whether a business opportunity is strong enough and editorially compelling enough to become an Operator Economy episode. It does not assign an episode number, write a script, generate narration, or begin visual production.

## Lifecycle

```text
candidate
-> researching
-> validation
-> eligible
-> promoted

Alternate exits: blocked / parked / archived
```

## Required artifacts for eligibility and promotion

1. A candidate brief based on `01-candidates/CANDIDATE.template.md`.
2. A sourced opportunity brief based on `02-research/RESEARCH-BRIEF.template.md`.
3. An analogy map based on `03-validation/ANALOGY-MAP.template.md`.
4. An opportunity-readiness scorecard based on `03-validation/SCORECARD.template.md`.
5. A passing Canvas feasibility review against `03-validation/CANVAS-FEASIBILITY-GATE.md`.
6. A passing narrative and audience-pull review against `03-validation/EDITORIAL-POTENTIAL-GATE.md`.
7. A promotion record based on `04-queue/PROMOTION-RECORD.template.md`.

An obvious early exit does not require seven artifacts. Step 0 should stop when the next artifact cannot change the decision responsibly.

## Early-disposition path

- **Archive at intake:** Use the completed candidate brief plus `03-validation/DISPOSITION-RECORD.template.md` when the idea has no operator business, duplicates an existing candidate, or belongs to another format.
- **Continue research, block, or park:** Use the candidate brief, research completed so far, any preliminary analogy review, and the disposition record. State exactly what would reopen the candidate.
- **Eligibility or promotion:** Complete all seven artifacts. Only this path can create an active queue row or authorize editorial development.

A low score alone is not an archive instruction. A coherent but incomplete opportunity should remain `continue research`. Archiving is for an out-of-scope, structurally invalid, superseded, or deliberately retired candidate.

## Artifact path and version contract

Use the same candidate ID in every filename and inside every artifact:

```text
01-candidates/<candidate-id>.md
02-research/<candidate-id>.md
03-validation/<candidate-id>-analogy-map.md
03-validation/<candidate-id>-scorecard.md
03-validation/<candidate-id>-canvas-gate.md
03-validation/<candidate-id>-editorial-potential.md
03-validation/<candidate-id>-disposition.md  # early exits only
04-queue/<candidate-id>-promotion.md
```

Every completed artifact records its template version, candidate ID, upstream paths, upstream SHA-256 hashes, and review date. Template changes do not silently update completed artifacts; the recorded version remains part of the decision history.

## Promotion rule

A candidate may be promoted only when:

- it scores at least 70/100 under the Step 0.2 opportunity-readiness rubric, or an owner override is explicitly recorded;
- the evidence and analogy floor passes;
- every required Canvas feasibility item passes;
- both the narrative-engine and audience-pull gates pass;
- it has a real, bounded Operator Economy point of view;
- no unresolved factual, source, legal, permission, guest, or access blocker prevents honest production.

The exact business does not need an operating precedent. A novel candidate may qualify as an `adjacent synthesis` or `frontier hypothesis` when verified direct, adjacent, and component evidence forms a valid transfer chain under `03-validation/EVIDENCE-STANDARD.md`.

An owner override may bypass only the numeric threshold. It cannot waive evidence integrity, analogy validity, Canvas completeness, narrative potential, audience pull, truth constraints, or a material permission, legal, or source blocker.

Evidence is usable only when it passes `03-validation/EVIDENCE-STANDARD.md`. Search volume is one demand signal, not a universal gate. When exact-query measurement is unavailable, the audience review requires a documented attempt plus independent proxy signals.

## Calibration zone and owner decision

The numeric promotion threshold remains 70/100. Scores from 65 through 75 form a mandatory owner-review calibration zone:

- `65-69`: below the numeric threshold; promotion requires both an explicit owner override and passing every hard gate.
- `70-75`: passes the numeric threshold but cannot be promoted without an explicit owner review recorded in the promotion record.
- `76-100`: outside the calibration zone, but promotion still requires a completed promotion record and named approval; a score never creates a queue row by itself.

`Eligible` means the research package passes the score and hard gates. `Promoted` means the owner-approved promotion record authorizes editorial development and the queue records the handoff. No candidate auto-promotes.

## Evidence classes and disclosure

- `observed model` - the same or substantially same business has direct operating evidence.
- `adjacent synthesis` - the proposed business combines valid neighboring business components.
- `frontier hypothesis` - the opportunity is more novel and carries additional testable assumptions.

Promotion approves an editorially defensible blueprint, not an earnings promise or a guarantee that the business will work. Every promoted package states what is observed, transferred, modeled, and hypothetical. Modeled economics must show formulas, costs, sensitivities, and the disclosure `modeled scenario, not observed performance or an earnings forecast`.

Before release, every public number remains subject to `content-os/facts.md`.

## Narrative and audience boundary

A complete Canvas is not automatically an episode. The operator must have a causal journey through a starting system, inciting change, mechanism, build, tradeoff or test, and measurable end state. A tool list, market overview, or slide taxonomy fails unless those elements create a story.

Audience pull can be established through exact or adjacent search demand, buyer behavior, transactions, adoption, spending, recurring questions, community demand, or credible category research. At least two independent signals are required, including one usable signal of consequential behavior, spend, adoption, or risk.

## Invalidation rule

A promotion record approves the exact candidate, research, analogy-map, scorecard, Canvas-gate, and editorial-potential hashes named in it. If any reviewed artifact changes, the promotion becomes `stale`, the active queue records that state, and editorial development stops until Step 0 is reviewed and approved again. Passing a research refresh date has the same effect for any load-bearing time-sensitive claim.

## Numbering and handoff

Candidates use stable descriptive IDs, not episode numbers. An `EP###` identity is assigned only after promotion into `01-editorial/`. Promotion authorizes editorial development; it does not approve a script, narration, visual plan, production asset, release, or URL.

## Reference boundary

Everything under a `references/` directory or `05-archive/` is frozen V1 material. It may inform a new artifact but is never V2 canon by location alone. Old search estimates, status labels, faceless-production assumptions, Remotion guidance, and other time-bound statements must be revalidated before use.

See `AUTHORITY-MAP.md` for shared authorities and `PORTING-MANIFEST.md` for exact provenance.

## Test fixtures

Packages under `fixtures/` exercise the workflow without creating an active candidate, queue entry, or episode. A fixture must be labeled test-only in every artifact and may never be promoted into editorial development. A real opportunity must start again under the normal artifact path contract with current research.

The frozen Step 0.2 acceptance set is defined in `fixtures/ACCEPTANCE-SET.md`. A semantic change to a Step 0 rule, score, hard gate, evidence class, template contract, disposition, calibration band, or promotion boundary requires a new Step 0 version and a rerun of the acceptance set. Do not edit a frozen fixture to make a changed rule pass; preserve it and add a new dated test when current evidence is required.
