# Step 1 stage gates

Status: approved V2 Step 1 v1.4 authority.

## States

```text
promotion_received
→ editorial_handoff_ready
→ editorial_contract_approved
→ operator_canvas_locked
→ investment_thesis_approved
→ narrative_approved
→ episode_beats_approved
→ script_review
→ editorial_voice_review
→ script_locked
→ narration_handoff_ready
```

Alternate states:

```text
return_to_step0 / revision_required / blocked / parked / cancelled
```

No automated score may advance a human approval state. Automated checks may identify defects and prove consistency; the named owner still approves the meaning and words.

## Fixture mode

Fixture mode may exercise the complete workflow when the user explicitly authorizes a named test candidate. It does not relax a production gate.

- Record the real production result and the simulated test result separately.
- An `eligible` fixture may simulate downstream editorial work, but it still fails production Gate E1.
- Do not assign an episode number, advance the active queue, issue a production lock, or authorize Narration Production.
- Label every output as a fixture or dry run.
- A fixture pass proves only the behavior tested; it does not approve Step 1 as a whole.

## Gate E1: handoff integrity

Decision: Is the promoted Step 0 package current, complete, and safe to use?

Required:

- Current promotion record.
- Six reviewed artifact hashes match.
- Research refresh date is current.
- Public-framing contract and caveats are present.
- Hard blockers are clear.
- Step 0 status is `promoted`, not merely `eligible`.

Failure returns to Step 0. Step 1 may not repair the package invisibly.

## Gate E2: editorial contract

Decision: Are we teaching the right thing to the right viewer for a clear reason?

Required:

- One named viewer/operator.
- The viewer is recognizably a professional exploring independent ownership, rebuilding income, or already building, rather than a generic aspiring entrepreneur.
- One practical end capability.
- One central argument.
- One narrative question.
- One honest working promise.
- A clear entry wedge and aspirational destination when they are not the same.
- Explicit exclusions and prohibited claims.
- A clear statement of how the episode serves the Operator Economy promise: a sustainable business of one using AI, tested without an income guarantee.
- Named human approval.

## Gate E3: Operator Canvas lock

Decision: Does the proposed business make sense as a complete operating model?

Required:

- Buyer, problem, offer, result, delivery, stack, go-to-market, economics, risks, and first test are complete.
- Dependencies and contradictions are resolved or explicitly marked.
- Every material field has an evidence class.
- Modeled economics expose assumptions and equations.
- The public layer cannot be mistaken for an earnings forecast.
- The buyer result has one primary acceptance measure or an explicit reason a single measure would be misleading.
- The first paid transaction, buyer acceptance event, and completion boundary are explicit.
- When a diagnostic determines whether implementation is responsible, the diagnostic, build decision, and implementation offer remain distinct; a no-build recommendation is a valid result.
- Access ownership, human judgment, failure routing, recovery, revocation, and handoff are bounded enough for the first test.
- Price, labor, tools, acquisition, support, and delivery capacity reconcile as observed inputs or explicit test assumptions.
- When the aspirational business is broader than the first offer, the Canvas records the entry wedge, scope invariant, conditional expansion ladder, and proof required before expansion.
- The Canvas identifies what AI compresses or enables, which judgment and accountability remain human, and why one operator can own the initial model.
- The livelihood case counts owner labor, tools, acquisition, support, delivery capacity, and the customers or transactions required. It remains a modeled sustainability test, not an income promise.
- The required buyer share is compared with a sufficiently large and costly problem in a way that can be tested without pretending a total market automatically becomes reachable demand.
- Every unresolved unknown is classified as a safe test question, later-stage blocker, or current lock blocker.
- Named human approval and Canvas hash.

The Step 0 feasibility pass is necessary but does not substitute for this authored Canvas review.

A compelling narrative, analogy, demo, or visual idea cannot satisfy a missing E3 requirement. On E3 failure, Gate E3I is not reached. Preserve promising story material as explicitly quarantined exploration, issue a bounded Canvas revision request, and do not polish the story while the operating model remains blocked.

## Gate E3I: Episode Investment Thesis

Decision: Is there a complete company worth recommending, a credible way for this operator to enter it, and enough evidence for an honest BUILD verdict?

Required:

- Gate E3 is locked and every recorded source hash matches.
- The show thesis, opportunity thesis, operator thesis, entry-wedge thesis, and affirmative BUILD verdict are distinct and mutually consistent.
- A short public category title, short spoken company name, one-sentence plain definition, and precise internal operating description are separately recorded.
- The spoken name can be understood and repeated on a first listen without carrying a stack of abstract nouns.
- The public name is treated as an editorial label unless approved evidence establishes an existing market category.
- The opportunity case names the normal system, market change, costly problem, fair incumbent case, high-end or established proof, what that evidence does not prove, and the missing ownership layer.
- The complete mature company is understandable before the diagnostic, audit, sprint, installation, or other first offer becomes the focus.
- The operator advantage comes from experience, judgment, access, relationships, or operating ability rather than tool access alone.
- AI and software responsibilities remain distinct from operator, buyer, specialist, permission, quality, exception, recovery, and accountability responsibilities.
- The entry wedge has one buyer, purchase trigger, bounded result, acceptance event, completion boundary, and valid no-build or stop route when relevant.
- Go to market identifies a reachable first segment, prospect path, first conversation, credibility artifact, and first paid ask.
- Modeled economics count price, owner labor, tools, acquisition, support, capacity, required customer or transaction count, and the share of a reachable buyer set that would be needed.
- The hard operating, distribution, trust, access, exception, safety, or support constraint is stated plainly.
- The first 30 and 90 days begin constructing the company while replacing the weakest assumptions with paid evidence.
- The narrative commitment gives material weight to both the opportunity case and the operator blueprint, targeting roughly half the episode for each unless the owner approves a reasoned exception.
- The final company-level recommendation is `BUILD`. If the evidence supports only `RETURN` or `PARK`, the candidate does not proceed to narrative development for production.
- `BUILD` remains an editorial recommendation to begin bounded construction, not proof of demand, pricing, recurring purchase, sustainable economics, or income.
- Named human approval and Episode Investment Thesis hash.

Gate E3I failure returns to the Canvas, a bounded Step 0 amendment, thesis revision, or parking. Do not repair a weak investment case by adding tactics, tools, or polished language downstream.

## Gate E4: narrative approval

Decision: Does the episode work as a story rather than a checklist?

Required:

- An approved Episode Investment Thesis tied to the locked Canvas and current claims map.
- A protagonist, goal, constraint, opening, mechanism, proof, decision, and resolution.
- One recurring human situation, transaction, or buyer decision carries the mechanism through the episode.
- Any illustrative thread contains no invented identity, metric, quotation, fact, or outcome. Spoken disclosure is required only when a reasonable viewer could mistake it for a documented or measured case; routine status labeling may live in metadata, a source card, or a visual label.
- The business mechanism causes the promised result in understandable steps.
- Evidence enters where it changes understanding, not as a detached research dump.
- The outline answers all required Canvas questions without following a rigid template merely for symmetry.
- The opportunity case earns the complete company before the entry wedge carries the build story.
- The entry wedge remains a credible entrance without being mistaken for the business ceiling.
- The aspirational destination is earned through conditional expansion logic rather than presented as a simultaneous offer or inevitable roadmap.
- The ending gives a responsible first action and preserves uncertainty.
- The proposed cold open has a concrete person, transaction, workflow, customer consequence, or strange result rather than an abstract thesis.
- The narrative identifies the normal system, what changed, who feels the consequence, why it matters, and which central question the report will answer.
- The main thesis is positioned after the context and evidence required to understand it. It is not delivered as the first explanation.
- The strongest fair counterargument receives an explicit ruling.
- Each major evidence block ends with an operating implication or verdict.
- One governing analogy family maps the mechanism and develops through at least one meaningful callback.
- Any planned humor or contempt clarifies the mechanism, has an explicit valid target, and does not substitute for evidence.
- The ending resolves or reinterprets the opening situation.
- Named human approval.

## Gate E4B: episode beats and outline

Decision: Can a new viewer follow the episode once, in order, before the full script is written?

Required:

- An approved episode beat sheet and episode outline tied to the same narrative, Canvas, and claims-map revisions.
- The Episode Investment Thesis hash, short spoken company name, plain definition, internal operating description, and BUILD verdict match across the beat sheet and outline.
- A concrete cold open of approximately 20–40 seconds that ends on an unresolved question or consequence and contains no show greeting, abstract thesis, evidence dump, or agenda.
- A distinct silent identity sting, planned at approximately 3–6 seconds, with no narration.
- The exact fixed brand string: “This is The Operator Economy, where we show you how to build, own, and operate a sustainable business of one using AI.”
- One episode-specific promise that names the business, the role of one accountable operator, and the useful viewer result without narrating a table of contents.
- A context runway of approximately 60–120 seconds that explains the normal system, why it exists, what changed, who is affected, and why the issue matters.
- One central investigation question asked only after the viewer has the vocabulary to understand it.
- A main thesis or reveal placed after the context and evidence needed to earn it.
- A recurring human situation, transaction, workflow, or customer consequence that carries the difficult mechanism.
- The incumbent or existing system receives a fair explanation before criticism.
- Abstract explanation alternates with a concrete example, person, transaction, evidence item, or simple mechanism.
- The first-listen load map identifies and revises beats that combine several new abstractions, statistics, analogies, and jokes.
- The body covers the business opportunity, buyer, offer, result, delivery, stack, go-to-market, economics, boundaries, and first test without becoming ten narrated Canvas headings.
- The body contains a visible opportunity-to-build turn. The opportunity side establishes why the mature company matters; the build side establishes how the operator enters and begins construction.
- The mature company appears before the first offer is allowed to define the business.
- The body explains what AI enables, what judgment the operator retains, the modeled conditions for one-person sustainability, and the reachable share of a large costly problem required by the model.
- The ending callback changes or resolves the opening rather than merely repeating a phrase.
- The ending delivers an affirmative, evidence-safe BUILD verdict and a bounded first construction step.
- An approved voice-and-comedy map built from the beat sheet, not used as a substitute for it.
- Named human approval.

Failure returns to beats, outline, or narrative. Do not draft the full script while the opening order, context runway, thesis placement, or episode promise remains unresolved.

## Gate E5: script review

Decision: Are the exact words credible, useful, natural, and faithful to the approved package?

Required:

- Complete claims map.
- Clean read-through without production metadata.
- Content OS fact and voice checks routed correctly.
- No hype, income promise, generic guru phrasing, or unresolved placeholder.
- No new claim outside the Step 0 package or approved amendment.
- A claim-change audit compares the reviewed script hash with the previous accepted script or outline language.
- Every new or changed number, population, prevalence, demand, market-price, typical-performance, company, comparative, causal, outcome, legal, or regulatory claim has an approved locator and wording boundary.
- Modeled scenarios have not been upgraded through words such as `typical`, `conservative`, `realistic`, `reasonable`, or `achievable` without supporting evidence.
- The cold open, silent identity break, fixed brand string, episode promise, context runway, central question, and earned thesis match the approved beat sheet.
- The cold open creates tension without trying to deliver the entire working promise; the brand and episode string state the promise after the identity break.
- A first-listen review identifies any sentence that is understandable on paper but unnatural or overloaded when heard once.
- Independent adversarial read checks clarity, credibility, and assumption drift.
- Every adversarial finding has an accepted, modified, rejected, or preserve disposition against the integrated revision.
- Owner revisions are incorporated before lock.

If E5 finds an unsupported claim, the disposition is either removal or a bounded Step 0 amendment request for the exact wording. Hedging an unsupported claim is not a third path. E5 failure invalidates the derived read-through and prohibits script lock, narration, and downstream production work.

## Gate E5V: editorial voice conformity

Decision: Do these exact words sound like a seasoned, opinionated Operator Economy advisor and plausibly sound like Manav, with informative entertainment, conviction, analogy, and rhythm, without weakening truth or imitating a reference?

Required:

- The reviewed `content-os/voice.md` path and SHA-256.
- The reviewed `VOICE-ARCHITECTURE.md` path and SHA-256.
- The reviewed `studio/config/speech-profile.md` path and SHA-256.
- An approved voice-and-comedy map tied to the narrative, claims map, and reviewed authority hashes.
- A clean read-through derived from the same immutable script hash.
- Mechanical support showing zero unresolved em dashes, semicolons, prohibited report vocabulary, acting tags, production notes, or lexical drift, plus a disclaimer audit, hedge review, and cadence diagnostics.
- Quoted evidence for the concrete cold open, exact brand string, context runway, operator-advisor relationship, earned thesis, and at least three act-level implications or verdicts.
- Quoted evidence that reporting structure, business context, plainspoken explanation, operator judgment, and restrained reveal perform distinct jobs.
- A governing analogy with explicit mechanism mapping and at least one meaningful callback.
- At least two distinct observed Manav speech patterns used naturally, including rhythmic variation rather than phrase insertion alone.
- Evidence and uncertainty stated accurately in familiar spoken language without a repeated disclaimer spiral.
- A fair counterargument followed by an explicit ruling.
- Humor that compresses, decodes, or exposes the mechanism rather than decorating it.
- Any sarcasm or contempt has an earned systemic target and protects the viewer, customer, worker, and under-resourced operator.
- A generic-language challenge identifying and resolving passages that could belong unchanged in another explainer.
- A first-listen load challenge identifying any beat with too many new ideas and any elegant sentence a colleague would not naturally say.
- A challenge to the weakest stance line and to any joke or analogy removable without loss of understanding.
- Separate pass decisions for opening orientation, show identity, reporting spine, business context, first-listen clarity, operator-advisor base, business-of-one clarity, Manav voiceprint, conviction, evidence integrity, humor temperature, cadence, ending payoff, and non-imitation.
- Independent editorial-voice reviewer recommendation and named owner decision.

The observed patterns are diagnostic, not a phrase quota. A script fails when it opens with a conclusion before context, repeatedly announces what it cannot prove, refuses to reach a verdict after the evidence, or depends on Step 2 to add conversational words. It also fails when jokes are decorative, analogies do not map, contempt outruns evidence, sentence rhythm becomes a punch-line metronome, or recognizable mannerisms turn the speaker into a parody.

Word-changing corrections return to script revision and rerun claims review, performance read-through, review disposition, and E5V as affected. Step 2 may not repair an E5V failure.

## Gate E6: script lock

Decision: Are these the exact words Step 2 is authorized to perform?

Required:

- Final script and claims-map hashes.
- Hashes for the approved contract, Canvas, Episode Investment Thesis, narrative spine, episode beat sheet, outline, and voice-and-comedy map.
- Named owner, decision, and timestamp.
- Exact spoken-word count, a clean performance read-through with the same words, and an expected-duration range.
- A passed E5V editorial-voice conformity report tied to the final script and reviewed authority hashes.
- No unresolved change request.

After this gate, calculate and record the editorial-lock hash, then create the narration handoff against that frozen lock. Step 2 may add non-lexical performance direction but may not change words.

## Amendment and invalidation rules

- A changed Step 0 source artifact invalidates the editorial handoff and every dependent Step 1 lock.
- A changed Canvas field invalidates the narrative, outline, script, and narration handoff unless a written impact review proves the change non-material.
- A changed Episode Investment Thesis invalidates the narrative spine, beat sheet, outline, voice-and-comedy map, script, and narration handoff unless a written impact review proves the change non-material.
- A changed narrative spine invalidates the beat sheet, outline, voice-and-comedy map, and script.
- A changed beat sheet invalidates the outline, voice-and-comedy map, and script unless an impact review proves the change non-material.
- A changed public or spoken company name, one-sentence definition, BUILD verdict, fixed brand string, episode promise, cold-open order, opportunity-to-build turn, context runway, or thesis placement creates a new beat-sheet and script revision.
- Any added, removed, reordered, or rewritten spoken word creates a new script revision and hash.
- A pronunciation spelling or performance tag may live in the narration layer only if the spoken lexical sequence remains identical.
- If Step 2 discovers an unperformable or misleading sentence, it issues a change request; Step 1 revises and relocks the script before narration resumes.
