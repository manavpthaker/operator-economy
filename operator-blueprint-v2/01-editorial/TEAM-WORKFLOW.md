# Step 1 team and agent workflow

Status: approved V2 Step 1 v1.4 authority.

Step 1 should behave like a small editorial team even when the work is executed through the CLI. Parallel work is useful only when responsibilities are independent and every worker receives the same frozen inputs.

## Roles

### Owner and executive editor

Human: Manav Thaker.

Owns the viewer promise, Operator Economy point of view, Canvas lock, narrative approval, exact script words, and final script-lock decision. Automated scores and agent consensus cannot replace this approval.

### Editorial lead or showrunner

Owns workflow state, artifact versions, task assignments, dependency order, conflict resolution, and the final integrated draft. This is the only role allowed to update a canonical artifact during a revision round.

### Handoff editor

Verifies the Step 0 promotion record, hashes, refresh dates, public framing, caveats, and blockers. It does not reinterpret research or approve the episode.

### Business-model editor

Develops the Operator Canvas, tests internal consistency, exposes assumptions, and reconciles offer, delivery, capacity, go-to-market, and economics. It does not write public claims beyond the approved evidence boundary.

### Claims editor

Builds the claims map from Step 0 artifacts, checks confidence and qualification, and flags drift. It may request a bounded Step 0 amendment. It may not conduct broad replacement research or upgrade evidence.

For every new script revision, the claims editor also reviews the claim-level diff against the previous accepted hash. A familiar topic does not make a new magnitude, prevalence, price, typicality, demand, causal, outcome, or legal statement pre-approved.

### Investment-thesis editor

Turns the locked Canvas and current claims map into the approved company-level investment case. It separately owns the opportunity thesis, operator thesis, entry-wedge thesis, mature company, short public and spoken name, plain definition, precise internal operating description, opportunity-to-build balance, and affirmative BUILD verdict.

It may synthesize approved evidence into an Operator Economy point of view. It may not turn an adjacent category into proof of demand, transfer high-end economics to the business of one, hide a missing acquisition path, or let a diagnostic or sprint replace the complete company. If an honest BUILD verdict cannot be reached, it returns or parks the candidate before narrative production.

### Narrative editor

Turns the approved contract and Canvas into a causal story. It owns protagonist, constraint, mechanism, proof, decision, resolution, sequence logic, and viewer movement. It does not design scenes or choose production assets.

### Episode-beat editor

Turns the approved narrative into the order a first-time viewer can follow. It separately authors the concrete cold open, silent identity break, fixed brand string, episode promise, context runway, central question, earned thesis, body functions, and ending callback. It owns the first-listen load map and orientation test. It does not write shot direction or use a clever opening to replace missing context.

### Voice architect

Builds the voice-and-comedy map after the episode beat sheet and outline are approved and before the full script. It owns the governing analogy, understated humor, target of any earned contempt, operator rulings, evidence-efficient language plan, Manav language patterns, and cadence shape. It does not rearrange the opening, invent claims, write production direction, or authorize imitation of a named reference.

### Scriptwriter

Writes the exact spoken draft from the approved narrative and claims map. It applies the reviewed Operator Economy house voice and observed Manav spoken-language profile before lock. It does not change the Canvas, invent evidence, or embed visual-production instructions.

### Adversarial editors

Review one immutable script revision independently:

- The operator reviewer tests commercial usefulness and business coherence.
- The story reviewer tests clarity, causality, pacing on the page, and generic-template drift.
- The first-listen reviewer hears or reads the narration once without annotations, then tests orientation, density, term order, and whether the main thesis was earned.
- The claims reviewer tests evidence, qualifiers, economics framing, and prohibited inferences.
- The editorial-voice reviewer tests the exact language against the reviewed Content OS voice and Manav speech-profile identities, quotes evidence from the script, challenges generic report language, and checks for caricature.
- The conviction-and-comedy reviewer tests whether evidence earns a position, humor follows comprehension, the governing analogy maps and develops, contempt has a valid systemic target, and the script avoids both disclaimer spirals and decorative punch lines.
- The performance reviewer reads aloud for breath, rhythm, pronunciation risk, and unnatural language without changing words.

Reviewers write findings. They do not edit the canonical script.

## Safe parallel plan

```text
E1 handoff verified
        │
        ▼
E2 editorial contract approved
        │
        ├───────────────┐
        ▼               ▼
Canvas draft       claims-map draft
        └───────┬───────┘
                ▼
          E3 Canvas lock
                │
                ▼
       episode investment thesis
                │
                ▼
             E3I approval
                │
                ▼
          narrative spine
                │
                ▼
        episode beat sheet
                │
                ▼
          episode outline
                │
                ▼
       voice-and-comedy map
                │
                ▼
          first script draft
                │
      ┌─────────┼─────────┬─────────┬─────────┬─────────┬─────────┐
      ▼         ▼         ▼         ▼         ▼         ▼         ▼
  operator    story   first-listen claims    voice   conviction  performance
   review     review     review    review    review    + comedy      read
      └─────────┼─────────┴─────────┴─────────┴─────────┴─────────┘
                ▼
      showrunner integration
                │
                ▼
     affected reviews rerun on
      the integrated script hash
                │
                ▼
      E5 + E5V recommendations
                │
                ▼
         owner script review
                │
                ▼
          E6 script lock
```

The Canvas and claims map may develop in parallel because both consume the same frozen Step 0 package. The Investment Thesis begins only after the Canvas locks and consumes the same current claims map. Narrative exploration may exist earlier, but narrative approval requires one approved Investment Thesis hash. The episode beat sheet requires an approved narrative, current Investment Thesis, and current claims map. The outline and voice-and-comedy map must use the approved beat sheet. Scriptwriting cannot begin from competing company definitions, category names, outlines, or an unresolved opening. Adversarial reviews may run in parallel only against the same immutable script hash. First-listen, voice, conviction-and-comedy, and performance are separate reviews: first-listen tests comprehension and order; voice and conviction judge the actual wording; performance tests whether those words can be spoken naturally.

## Premature-story quarantine

When a strong story emerges before Gate E3:

- Mark it `exploratory; created before Canvas lock` and preserve its hash.
- Do not use it to fill a missing buyer, offer, result, delivery, safety, economics, capacity, or expansion decision.
- Do not approve, outline, script, scene-plan, or polish it while E3 is failed.
- Issue a bounded Canvas revision request that names the operating decisions required.
- After E3 passes, compare the story with the locked Canvas. Keep only the elements that remain truthful and coherent.
- A Canvas pass permits narrative work to resume; it never approves the exploratory story retroactively.

## Assignment contract

Every CLI or agent assignment must state:

- Role.
- Exact objective.
- Input paths and hashes.
- Allowed output path.
- Files the worker may edit.
- Files the worker must not edit.
- Evidence boundary.
- Expected artifact or review format.
- Stop conditions.
- Approval the worker is not authorized to grant.

An assignment without exact inputs or edit boundaries is not production-ready.

## Canonical-write rule

- One role owns each canonical file during a revision round.
- Reviewers never patch the canonical file directly.
- Review findings use stable IDs, severity, exact location, reason, and recommended correction.
- The showrunner accepts, rejects, or modifies each finding in a disposition log.
- Positive findings that must survive integration receive a `preserve` disposition.
- A new integrated revision receives a new hash before another parallel review round.
- Agents do not resolve a human editorial disagreement by majority vote.

## Stop and return rules

Stop the affected lane when:

- A required Step 0 artifact or hash is missing.
- A new load-bearing claim is required.
- Canvas assumptions cannot reconcile.
- The mature company, entry wedge, or required-share logic cannot support an honest BUILD verdict.
- The short spoken company name or plain definition remains unresolved.
- The narrative needs a fact the approved package cannot support.
- A reviewer discovers legal, permission, access, guest, or truth risk.
- The owner's point of view or intended public framing is ambiguous.
- Two canonical drafts exist for the same revision.

Return a bounded question or amendment request. Do not guess, broaden scope, or polish downstream artifacts around an unresolved decision.

## Dry-run protocol

An explicitly authorized fixture may simulate the roles above against an eligible candidate. The handoff editor records both truths: the fixture may proceed for test purposes while production Gate E1 remains failed. Every assignment and output must say that it cannot grant owner approval, create an episode, issue a script lock, or authorize narration.
