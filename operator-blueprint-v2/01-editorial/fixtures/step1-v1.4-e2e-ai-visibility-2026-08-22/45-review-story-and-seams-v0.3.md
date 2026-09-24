# Story and narrative-seam review: AI Visibility v0.3

Status: complete independent fixture-role review

Decision: **REVISE**

Reviewed immutable script: `42-script-v0.3-FINAL-CANDIDATE.md`

Reviewed script SHA-256: `b928e5756e11c30595ced4ae874a0bb2969070f40619c8223b8c10e183b66cbf`

Reviewed clean read-through: `43-performance-readthrough-v0.3.md`

Reviewed read-through SHA-256: `19515cca36bd337a09c1fc46651ffbf6baedb6dcc128be630d19e28fbb049301`

Reviewed upstream repair set:

- `38-narrative-spine-v0.2.md`, SHA-256 `60207a7dd5d12aeb9f88a0ab58dae0615e2c3e5abb01bdebce2c3a30423be6dd`
- `39-episode-beat-sheet-v0.2.md`, SHA-256 `73ec19b86ad3620979d7783d5b4003de6746c59f1bcf2df5f44b8a758de7dc44`
- `40-episode-outline-v0.2.md`, SHA-256 `7a2e838a7819263cbc1d43a4af530989ec0c2ab39f3fa3bddd48102075525d02`
- `41-voice-and-comedy-map-v0.2.md`, SHA-256 `71ebd37d7c2257f5496fad718dcc413e2f0a7ab187b61eba79d314a24b26415d`

Proposed v1.5 controls reviewed as a non-canonical test basis:

- `EDITORIAL-VOICE-STANDARD.md`, SHA-256 `c3d8461ba3f12d5c198417338b19110fb841de181390afd9f96001bd24382e15`
- `STAGE-GATES.md`, SHA-256 `af496a3fa888d1263859f3b6e1075af00b968e34a5419317b09ff2543f6901c6`
- `05-script/SCRIPT-STANDARD.md`, SHA-256 `4e55e52f0a7cabe7ee992e56de3ed24e15197d202f4f11c34ac6e19e8df946a0`
- `04-narrative/EPISODE-OUTLINE.template.md`, SHA-256 `daa3c546ff670a60c6de8d42a1c3aee003dca6c5353bb4f91cbbc7c45a131bbd`
- `04-narrative/VOICE-AND-COMEDY-MAP.template.md`, SHA-256 `c9db1a38e4587717f25af70f6a3298378d34b88c717638bbc6ef0e6b842cf4a9`

Review scope: story causality, exact scene seams, company-versus-wedge order, operator-market instruction, company-level BUILD conviction, and opening callback. This review does not assess factual support, arithmetic, citation completeness, voice imitation, or performance direction.

Lexical identity: pass. The narration blocks in the script and read-through are identical. The only raw extraction difference is one final blank line.

## Literal last-two to first-two seam test

Each row reproduces the exact final two narration paragraphs of the outgoing scene and the exact first two narration paragraphs of the incoming scene. Headings are excluded.

| Seam | Exact outgoing final two spoken lines | Exact incoming first two spoken lines | Inherited unit and advance | Reset or redefinition check | Decision |
|---|---|---|---|---|---|
| S00 to S02 across silent S01 | `The dashboard is still green.`<br><br>`So what part of the customer's decision can that report not see?` | `This is The Operator Economy, where we show you how to build, own, and operate a sustainable business of one using AI.`<br><br>`We're building an AI visibility company. It helps brands understand how they appear in AI answers and decide what deserves action. By the end, you'll know what one operator owns, how to choose the first market, and what the first paid version has to prove.` | The silent sting and brand string are the recorded exception. The episode promise converts the missing-view question into a promised company and viewer outcome. | Approved identity and brand reset. No unrelated topic enters. | **PASS, recorded exception** |
| S02 to S03 | `This is The Operator Economy, where we show you how to build, own, and operate a sustainable business of one using AI.`<br><br>`We're building an AI visibility company. It helps brands understand how they appear in AI answers and decide what deserves action. By the end, you'll know what one operator owns, how to choose the first market, and what the first paid version has to prove.` | `To see the opening, start with the report that's already green.`<br><br>`A customer types a question into search. A page appears, they click it, and the visit shows up in analytics. Maybe they buy something. Now the marketing team has a trail it can follow.` | `To see the opening` returns to the green-report image preserved across the approved brand reset and begins the evidence needed to define what the promised company owns. | No deck heading. The opening scene is resumed rather than restarted. | **PASS** |
| S03 to S04 | `So this isn't a story about regular search dying. The missing view is the opening, but an opening isn't a company.`<br><br>`What should one operator own between the answer a customer sees and the decision the buyer has to make?` | `To answer that, separate what the tools can collect from what the buyer still needs.`<br><br>`Products already track prompts, brand mentions, competitors, citations, and source patterns. Researchers were able to measure this surface, but the effects they found varied by domain.` | S04 explicitly answers the ownership question by separating collection from the buyer's remaining need. | No reset. The promised BUILD is preserved because the question concerns owned responsibility, not whether the episode has a company to deliver. | **PASS** |
| S04 to S05 | `The company records what appeared, checks the important facts and sources, separates what the client controls from what it can only watch, and tells the buyer what deserves action.`<br><br>`You aren't selling control of the answer. You're selling a better decision about it.` | `That missing responsibility tells us what the full company has to look like. Not the first report. The thing you're actually trying to build.`<br><br>`The AI visibility company works with a small group of brands. It keeps track of the questions that matter, records how the agreed answers and sources change, and checks important statements against facts the client has approved. Then it connects the evidence to a content, reputation, planning, or measurement decision.` | `That missing responsibility` inherits the correct noun, but S04 has already defined the company, its operating actions, and its value. S05 announces that it will now define the full company and restates the same operating loop. | **Redefinition failure.** The listener finishes one company definition and immediately hears a second company-definition opening. This is the deck-reset behavior the v0.3 repair was meant to remove. | **REVISE** |
| S05 to S06 | `One operator stays accountable for that loop. AI helps collect and compare the material. Software keeps the record. The buyer approves the facts. A specialist steps in when the work crosses into expertise the operator shouldn't pretend to have.`<br><br>`The operator owns the judgment. Which is why the operator's experience matters more than the software account.` | `The judgment has to come from somewhere. So where should that experience come from?`<br><br>`If you've worked in search, content, digital strategy, or intelligence, you know a result can be interesting and useless. A source can look authoritative and answer the wrong question. And the buyer's decision matters more than the amount of data in the report.` | `Judgment` and `experience` cross the seam literally. S06 advances from responsibility allocation to the operator's earned advantage. | No reset or company redefinition. | **PASS** |
| S06 to S07 | `Use that judgment in a field where you've earned context or a path to the buyer. That may come from industry experience, adjacent client work, or a network that opens the conversation.`<br><br>`That is the advantage, not the software account. Now turn it into something the first buyer can inspect.` | `The first buyer isn't going to hand you the whole function. They need a smaller, complete piece: one brand, one market, ten questions the buyer approves before collection, and two answer surfaces.`<br><br>`What are they buying?` | `First buyer`, `inspect`, and the complete function cross into the bounded first purchase. | No reset. The full company has already been established before the wedge appears. | **PASS** |
| S07 to S08 | `Implementation and monitoring are separate decisions. Neither one sneaks into the first invoice because it looks good in a revenue model.`<br><br>`That gives you a bounded offer. It still needs a buyer you can actually reach.` | `Start where you already have a reason to be useful. You need to understand the buyer's decision, speak the language, and have a credible way to reach the person responsible.`<br><br>`Travel is the example here because it makes the customer journey clear. It isn't the market recommendation.` | `Buyer you can actually reach` becomes the operator-market selection rule. Travel is then classified as the illustration rather than the instruction. | No reset. The example does not replace the reusable rule. | **PASS** |
| S08 to S09 | `If the answer is yes, ask what decision changes and who owns it. Then offer the complete paid diagnostic.`<br><br>`Demand needs a buyer. A product launch and a busy category can't stand in for one. And buyer access still doesn't prove one operator can carry the work.` | `Here's the planning model we're testing. Assumptions, not results, and not an earnings forecast.`<br><br>`The smaller case charges two thousand dollars and allows 16 delivery hours. Set aside 960 for the owner's time, 99 for software, and 300 for finding the client and listed overhead. That leaves 641 dollars before tax and unlisted costs.` | The unresolved consequence is whether one operator can carry the work. The planning model begins testing that exact condition. | The opening phrase is generic in isolation, but the preceding sentence creates a specific capacity question that the model answers. No topic is redefined. | **PASS, lowest-strength passing seam** |
| S09 to S10 | `That is a demanding sales test. We don't know whether the operator reaches those buyers, whether 504 hours cover the rest of the job, or whether anybody pays the modeled price.`<br><br>`The arithmetic works. The business doesn't become proven because the spreadsheet stopped arguing with itself.` | `The spreadsheet can fit and the company can still fail.`<br><br>`Maybe the buyer sees ordinary SEO work and won't pay separately. Maybe the sample moves too much to support a responsible comparison. Or maybe a tool gives the buyer the whole decision. If your judgment adds nothing, a report and a meeting don't create a company.` | `Spreadsheet`, `fit`, and the unproven business cross literally. S10 turns the remaining unknowns into failure modes. | No reset. This is a strong causal seam. | **PASS** |
| S10 to S11 | `If the hours break the model, narrow the scope, change the price, or stop. If every job needs several specialists, choose a narrower market or admit the model needs a team. Another month on the calendar doesn't earn a monitoring fee.`<br><br>`Each failure tells you what the first 30 days have to test.` | `Build the test around those failures.`<br><br>`In the first 30 days, make the question template, evidence record, delivery boundary, three-question screen, and first prospect list.` | `Failure`, `first 30 days`, and `test` cross literally. S11 converts the failure modes into construction work. | No reset. This remains the positive-control seam. | **PASS** |
| S11 to S12 | `That is construction. You're building the assets, making the offer, doing the work, and replacing assumptions with paid evidence.`<br><br>`Which brings us back to the green report.` | `The search report can stay green. It wasn't necessarily wrong. It was watching one doorway while the customer used another.`<br><br>`The company worth building sits between that missing view and the decision the buyer has to make.` | `Green report` crosses literally. S12 resolves the original contradiction and connects the missing view to the company responsibility. | No reset. The callback changes the opening from a mystery into an operating boundary. | **PASS** |

Seam count: 10 pass, 1 revise. The silent S01 identity sting is recorded as the approved exception rather than counted as a narrated seam.

## Story architecture decisions

| Test | Evidence | Decision |
|---|---|---|
| Concrete cold open | The green report, missing or stale answer, and unresolved missing view create one recognizable buyer problem. | pass |
| Promised company and BUILD posture | S02 says `We're building an AI visibility company`; S03 asks what the operator should own rather than whether the company exists; S12 lands `Build the AI visibility company.` | pass |
| Incumbent fairness | S03 says the existing search system remains useful and S04 says nobody has to be doing a bad job. | pass |
| Opportunity-to-build movement | S03-S05 establish the missing view and company; S06 begins operator fit; S07-S11 construct offer, market, economics, boundaries, and test. | pass |
| Complete company before wedge | The mature portfolio responsibility is stated in S05 before S07 introduces the first purchase. The order passes even though the S04-S05 boundary repeats the definition. | pass on order; seam revise |
| Operator-market fit | S06 instructs the viewer to use earned context or buyer access. S08 leads with usefulness, buyer language, and reach, then says travel is an example and not the recommendation. | pass |
| Travel as carrier, not prescription | Travel appears in the opening, is explicitly bounded in S08, remains the concrete arithmetic carrier in S09, and does not become universal advice. | pass |
| Entry wedge remains an entrance | S07 says the first buyer will not hand over the whole function and defines a smaller complete piece. S12 says the responsibility is larger than one diagnostic. | pass |
| Recurring human and mechanism thread | The marketing lead and green report carry S00, return in S04, ground the travel example in S08, and resolve in S12. | pass |
| Opening callback and final action | S12 explains why the report can remain green, locates the company between the missing view and buyer decision, and ends with one paid diagnostic in a reachable market. | pass |

## Blocking finding

`S04 to S05` fails the exact narrative-seam rule. S04 already tells the listener where the company begins, what it records, what it checks, what it classifies, what it tells the buyer, and what it sells. S05 then announces `what the full company has to look like` and restates the same loop. The incoming scene inherits the right concept but does not advance it before redefining it.

This is a word-changing issue. It cannot be treated as a performance note or repaired in Step 2. The next revision must give the company definition one clear home: either S04 stops at the unowned responsibility and S05 defines the mature company, or S04 owns the definition and S05 advances to a genuinely new consequence. The exact remedy belongs to script revision.

## Verdict

Story architecture: mostly coherent

Narrative seams: **REVISE**

Overall story-role recommendation: **REVISE**

Editorial lock: no

Step 2 authorization: no

Reviewer: independent fixture story and narrative-seam role

Review date: 2026-08-22
