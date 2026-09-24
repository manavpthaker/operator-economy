# Claims and structure review: AI Visibility v0.9

Status: complete independent exact-hash fixture review; **REVISE**

Production public-fact status: **BLOCKED**

Review date: 2026-08-23

Reviewer identity: `fixture-claims-structure-reviewer-v0.9-independent`

Scope: exact-hash claims, evidence limits, economics, receipts, scene structure, causal seams, opening, silent sting, ending payload, and script-to-read-through narration identity. Voice match, comedy, owner performance, and production authorization remain separate except where a wording choice changes an immutable claim or structural boundary.

## Immutable inputs

| Input | Expected SHA-256 | Verified SHA-256 | Result |
|---|---|---|---|
| `38-narrative-spine-v0.2.md` | `60207a7dd5d12aeb9f88a0ab58dae0615e2c3e5abb01bdebce2c3a30423be6dd` | `60207a7dd5d12aeb9f88a0ab58dae0615e2c3e5abb01bdebce2c3a30423be6dd` | match |
| `39-episode-beat-sheet-v0.2.md` | `73ec19b86ad3620979d7783d5b4003de6746c59f1bcf2df5f44b8a758de7dc44` | `73ec19b86ad3620979d7783d5b4003de6746c59f1bcf2df5f44b8a758de7dc44` | match |
| `40-episode-outline-v0.2.md` | `7a2e838a7819263cbc1d43a4af530989ec0c2ab39f3fa3bddd48102075525d02` | `7a2e838a7819263cbc1d43a4af530989ec0c2ab39f3fa3bddd48102075525d02` | match |
| `50-claims-map-v0.3.md` | `eb992aba4a4ce75927fdda0b057daef6c365247b03f27eaf5375ceab0b6d9088` | `eb992aba4a4ce75927fdda0b057daef6c365247b03f27eaf5375ceab0b6d9088` | match |
| `89-script-v0.8-FINAL-CANDIDATE.md` | `1e37c5186fcbf68c922cca516f567f85ac85b35f57a04853087c89f719d0dfa1` | `1e37c5186fcbf68c922cca516f567f85ac85b35f57a04853087c89f719d0dfa1` | match |
| `90-performance-readthrough-v0.8.md` | `36a9de4322798aef57f9dabc9226f1437bde1d9870f11e43c05f467be5edb9a5` | `36a9de4322798aef57f9dabc9226f1437bde1d9870f11e43c05f467be5edb9a5` | match |
| `100-voice-only-revision-boundary-v0.9.md` | `43fc8efb34f41ba0e76d9bb93bd9d296a4ce3486e9cabba05df23ee698459f5a` | `43fc8efb34f41ba0e76d9bb93bd9d296a4ce3486e9cabba05df23ee698459f5a` | match |
| `101-voice-and-comedy-map-v0.3.md` | `7c8c8d51a52b4d79bdddb27c455197bba5f5653ae860df1f82eaf3843845c9cd` | `7c8c8d51a52b4d79bdddb27c455197bba5f5653ae860df1f82eaf3843845c9cd` | match |
| `102-script-v0.9-VOICE-CANDIDATE.md` | `8af7df50153dd98775e5fbabbe3c73e19e0711c1944185c010f188915c383085` | `8af7df50153dd98775e5fbabbe3c73e19e0711c1944185c010f188915c383085` | match |
| `103-performance-readthrough-v0.9.md` | `7711daa90f9310559b9b36a4b88599c92d573b84c537de241fa1068f6c2a7526` | `7711daa90f9310559b9b36a4b88599c92d573b84c537de241fa1068f6c2a7526` | match |

## Exact verdict

| Review surface | Verdict | Finding |
|---|---|---|
| Exact v0.9 pair | pass | Both expected file hashes match the reviewed files. |
| Scene identity and order | pass | S00 through S12 remain present, separate, titled, and ordered exactly as in v0.8. |
| Claim-ID routing | pass | The scene-level claim-ID sequence is unchanged. |
| C001-C010 | **revise** | C001-C004 and C006-C010 stay within their rails. C005 loses its required capability-only, no-buyer-value, and no-service-result limit in S04. |
| E001-E011 | pass | Every input, equation, threshold, remainder, capacity figure, and reach figure independently reconciles and remains modeled. |
| Exact continuation gate | pass | Three of five, paid acceptance or a specific budget-backed purchase condition, and repeatable evidence within 24 hours remain intact. |
| Required model receipts | pass | Eight non-spoken receipt lines are byte-for-byte identical to v0.8. |
| Script-to-read-through narration identity | pass | Both files contain the same 2,355 spoken tokens in the same order. |
| S00 opening | pass | All six spoken movements remain in order and stay illustrative. |
| S01 silent sting | pass | S01 remains a distinct scene with no narration. |
| S02 brand string | pass | The exact approved brand string is present in both files. |
| S07 first-offer boundary | **revise** | The completion and buyer-acceptance boundary has been deleted. |
| S08 to S09 transition | **revise** | S09 opens with a prohibited second `Okay` and chapter reset instead of inheriting the delivery question. |
| S12 ending payload | **revise** | The required `not another dashboard` contrast has moved out of the ending. |
| Final CTA | pass | The exact approved final sentence is present in both files and no material follows it. |

Fixture claims and structure decision: **REVISE**

Word-changing blockers: **four**

Production fact authorization: **BLOCKED**

Owner approval: **PENDING A NEW COLD READ AFTER REPAIR**

This review authorizes no editorial lock, recording, narration generation, Step 2 handoff, production, or publication.

## Blocking findings

### CS104-001: C005 loses its required evidence limit

The claim map limits C005 to vendor-described collection capability. Its approved spoken treatment says that products can collect prompts, mentions, competitors, citations, and source patterns, but that this does not establish what a buyer values or what result the service can produce (`50-claims-map-v0.3.md:62`). The voice-only boundary freezes the same limit (`100-voice-only-revision-boundary-v0.9.md:108`).

V0.8 states the limit explicitly:

> That shows collection is possible. It doesn't show what a buyer will value or what result the service can produce.

V0.9 replaces it with:

> That's useful. It just isn't the business.

The replacement at `102-script-v0.9-VOICE-CANDIDATE.md:113` does two things the boundary does not permit:

- It makes an unqualified positive value judgment about the capability.
- It removes the explicit no-buyer-value and no-service-result limits.

The later sentence that the benchmark cannot predict a client result belongs to C006. It does not restore C005's separate buyer-value and service-result boundary.

Required repair: restore an audible capability-only limit inside S04 without changing C005's source class or expanding the claim. Because this changes words, the revised pair requires a new exact-hash review.

### CS104-002: S07 loses its immutable completion boundary

The voice-only boundary requires S07 to define the bounded purchase, delivery record, four decision categories, completion boundary, and valid no-action result (`100-voice-only-revision-boundary-v0.9.md:64`). The outline independently requires buyer acceptance and completion (`40-episode-outline-v0.2.md:147-155`).

V0.8 made the boundary explicit:

> The job ends when that record is clear enough for the buyer to use.

V0.9 preserves the record, the four recommendations, the valid no-action result, and the exclusion of implementation and monitoring. It then says `That's the first offer` at `102-script-v0.9-VOICE-CANDIDATE.md:215`. It never says when the diagnostic is complete or what buyer-use condition closes the job.

Excluding later services defines what is outside the invoice. It does not define delivery acceptance or completion.

Required repair: restore a buyer-use or buyer-acceptance completion boundary inside S07. Because this changes words, the revised pair requires a new exact-hash review.

### CS104-003: the ending loses the `not another dashboard` contrast

The v0.9 boundary prohibits relocating a narrative turn (`100-voice-only-revision-boundary-v0.9.md:53`). Its immutable ending payload says the company is not another dashboard and supplies a clear call on what deserves action and what does not (`100-voice-only-revision-boundary-v0.9.md:87`). V0.8 keeps both halves together in S12.

V0.9 moves the negative contrast into S07 as `Not a prettier dashboard` at `102-script-v0.9-VOICE-CANDIDATE.md:197`. S12 retains only the positive half at line 387: the company records the answer, checks the evidence, and gives the buyer a clear action call.

The concept remains somewhere in the episode, but the frozen ending turn does not. The ending no longer closes the dashboard-versus-decision distinction in the form the boundary requires.

Required repair: restore the `not another dashboard` contrast in S12 while preserving the existing green-report callback, first action, earned expansion, business-of-one principle, and exact final CTA. Because this changes words, the revised pair requires a new exact-hash review.

### CS104-004: S09 violates the exact opener and marker controls

S08 ends by asking whether the work fits inside one person's week (`102-script-v0.9-VOICE-CANDIDATE.md:249`). The outline requires S09 to open directly from that delivery question, `not with Okay or a chapter reset` (`40-episode-outline-v0.2.md:172-176`). The beat sheet permits at most one purposeful `Okay` in the full script and says a personal marker may not become a section label (`39-episode-beat-sheet-v0.2.md:106-112`).

V0.9 uses `Okay, so` to open S05 at line 143, then opens S09 with `Okay. Now put money around the test` at line 261. Both are scene-opening markers. The S08-to-S09 meaning remains causal, but the exact transition form fails.

Required repair: make the first words of S09 inherit the one-person delivery question directly. Do not add another marker elsewhere. Because this changes words, the revised pair requires a new exact-hash review.

## Full C001-C010 regression

| Claim | Result | Finding |
|---|---|---|
| C001 | pass | `Roughly half the people it surveyed` keeps the population audible. Regular search remains active, and surveyed behavior is not converted into demand. |
| C002 | pass | Source composition remains variable by question, category, and platform. No fixed source rule, source share, or control lever is inferred. |
| C003 | pass by omission | The small sampled 16-percent claim remains omitted. |
| C004 | pass | SEO is used only as an adjacent purchase form. The narration explicitly denies demand and price transfer. |
| C005 | **revise** | Collection capability remains, but the required no-buyer-value and no-service-result boundary is missing. `That's useful` is not an adequate or neutral replacement. |
| C006 | pass | One benchmark remains bounded by domain variation and an audible no-client-result limit. |
| C007 | pass | The company remains Operator Economy synthesis. Human judgment, authority, accountability, and specialist boundaries remain audible without a categorical AI-incapacity claim. |
| C008 | pass | Model qualifiers precede the first offer counts and all money. Travel stays illustrative. Counts, prices, hours, capacity, reach, and validation thresholds remain assumptions. |
| C009 | pass by omission | Unknown search volume produces no inference about demand. |
| C010 | pass | BUILD remains a bounded recommendation to construct and test one paid diagnostic, not evidence of demand, sustainability, outcome, or income. |

Claims regression verdict: **REVISE ON C005**

## Exact E006 continuation gate

The spoken gate preserves all three required conditions:

1. At least three of five buyers independently describe the problem as consequential.
2. At least one accepts a paid diagnostic or names a budget and what would have to be true for approval.
3. Manual delivery produces repeatable evidence within 24 hours of work.

The script keeps a budget-conditioned manual test separate from paid acceptance and says that it is not paid demand. The non-spoken receipt also says the gate is not an expected conversion rate.

E006 continuation-gate verdict: **PASS**

## Independent E001-E011 reconciliation

| ID | Independent reconstruction | V0.9 treatment | Result |
|---|---|---|---|
| E001 | $2,000 validation diagnostic | `Two grand` plus exact receipt | pass as a modeled input, not an observed price |
| E002 | 16 x $60 = $960 | $960 | pass as an owner-time allowance, not owner income |
| E003 | $99 + $300 = $399; two projects use $198 and $600 | same | pass; the $99 source component is observed, while allocation and $300 are modeled and costs remain incomplete |
| E004 | $2,000 - $960 - $99 - $300 = $641 | $641 | pass; before tax and unlisted costs |
| E005 | 24 x $60 = $1,440; $3,000 - $1,440 - $99 - $300 = $1,161; two projects leave $2,322 | $1,161 and $2,322 | pass; not capacity, margin, or earnings evidence |
| E006 | Five interviews, 25 prospects, ten questions, two surfaces, and a 24-hour boundary | same | pass as test design, not expected conversion or performance |
| E007 | $48,000 owner-labor-and-support target | $48,000 | pass as a fixture planning input before tax and unlisted costs, not promised income |
| E008 | 20 x 48 = 960 hours; 19 x 24 = 456; 24 x 24 = 576; 960 - 456 = 504 | 960, 456, and 504 in narration; all four in the receipt | pass; not observed safe workload |
| E009 | $3,000 - $99 - $300 = $2,601 | $2,601 | pass as arithmetic for owner labor and support, not take-home pay or observed contribution |
| E010 | $48,000 / $2,601 = 18.4544; 18 x $2,601 = $46,818; 19 x $2,601 = $49,419 | 18 falls short and 19 clears the target | pass as a required modeled count, not forecast demand |
| E011 | 19 / 250 x 100 = 7.6 percent | 7.6 percent | pass as an example-list hurdle, not TAM, conversion, or proof of reachability |

Every spoken remainder and owner-support figure retains `before tax and unlisted costs`.

Arithmetic verdict: **PASS**

## Receipt regression

The eight required non-spoken model receipt lines are byte-for-byte identical between v0.8 and v0.9.

- V0.8 ordered receipt-line SHA-256: `7e999849d406e9b5890daa7f09c5bf3c430205ae7e6b939ba2541724cb85c87a`
- V0.9 ordered receipt-line SHA-256: `7e999849d406e9b5890daa7f09c5bf3c430205ae7e6b939ba2541724cb85c87a`
- Receipt line count in each script: 8

The source-receipt and complete show-note records remain unchanged through the immutable claims-map hash `eb992aba4a4ce75927fdda0b057daef6c365247b03f27eaf5375ceab0b6d9088`.

Receipt verdict: **PASS**

## Scene and structural regression

| Scene | Result | Finding |
|---|---|---|
| S00 | pass | The hotel, missing or stale answer, green dashboard, blind spot, one-operator paid-diagnostic opening, and blueprint handoff remain in order. |
| S01 | pass | The identity sting remains separate and silent. |
| S02 | pass | Show identity, company name, plain job, ownership question, market selection, and first paid proof remain present. |
| S03 | pass | Conventional search is treated fairly before the bounded second doorway, source variation, report gap, and paid-job question. |
| S04 | **revise** | The collection, benchmark, adjacent purchase, and responsibility sequence remains, but C005's mandatory evidence limit is missing. |
| S05 | pass | The mature company remains defined before the first offer. |
| S06 | pass | Earned context and buyer access remain the reusable market-selection advantage; travel is not prescribed. |
| S07 | **revise** | The bounded offer, record, four decisions, no-action result, and exclusions remain, but buyer acceptance and completion are absent. |
| S08 | pass | Experience-led market selection, buyer access, travel illustration, prospect model, preview, decision question, and paid-diagnostic ask remain. |
| S09 | **revise** | All model layers and arithmetic remain, but the opener violates the exact S08-to-S09 transition rule. |
| S10 | pass | Failure modes retain the attached stop, refusal, narrowing, pricing, specialist, and monitoring rules. |
| S11 | pass | Failure modes become the 30-day tests, exact continuation gate, and funded-work discipline. |
| S12 | **revise** | The green-report callback, decision value, first action, earned expansion, business-of-one principle, and CTA remain. The required `not another dashboard` contrast does not. |

No scene was added, removed, merged, split, or reordered. No claim ID, model, proof burden, receipt, or arithmetic item moved. The four wording findings above are nevertheless outside the frozen v0.9 boundary.

The v0.9 opportunity/build count is 845/1,510, or 35.9/64.1 percent. The totals independently reconcile to 2,355 words. The voice-only boundary permits word-count change as a consequence of natural phrasing, so the ratio is not an additional blocker in this review. It remains a pacing watch against the approximately equal target in the narrative spine and should be recalculated after repair.

Structural verdict: **REVISE**

## Causal seam audit

| Seam | Semantic result | Finding |
|---|---|---|
| S00 to S02 | pass | Paid diagnostic and blueprint hand off through the silent sting to the named show and company. |
| S02 to S03 | pass | Promised ownership and proof lead into the changed research path. |
| S03 to S04 | pass | The paid-job question leads into the separation of tools from responsibility. |
| S04 to S05 | pass | The identified human responsibility becomes the mature company. |
| S05 to S06 | pass | The judgment business leads into earned operator judgment. |
| S06 to S07 | pass | The need for an inspectable first purchase leads into the bounded test model. |
| S07 to S08 | pass | The first offer asks who can buy, leading into market and buyer access. |
| S08 to S09 | **revise on exact control** | The one-person workload question does lead semantically into economics and capacity, but the prohibited `Okay. Now` reset fails the required opener form. |
| S09 to S10 | pass | Unknowns left by the arithmetic become the concrete business failure modes. |
| S10 to S11 | pass | Failure questions become first-30-day tests. |
| S11 to S12 | pass | The explicit green-report return resolves the opening image. |

All eleven seams pass the semantic last-two-to-first-two inheritance test. S08 to S09 separately fails its exact opener rule.

## Opening, sting, brand, and ending audit

### Opening and sting

S00 preserves all six required spoken movements:

1. A guest asks AI where to stay.
2. The hotel is missing or appears with an unrecognized description.
3. The dashboard remains green.
4. The blind spot becomes the business opening.
5. One operator can map answers, check sources, and turn the gap into a paid diagnostic.
6. The narration hands off to the blueprint.

S01 remains a distinct silent scene. No narration or claim has entered the sting.

Opening and sting verdict: **PASS**

### Brand string

The following byte-exact string appears in both v0.9 narration surfaces:

> This is The Operator Economy, where we show you how to use AI to build, own, and operate a sustainable business of one.

Brand-string verdict: **PASS**

### Ending

S12 preserves:

- the green report as useful rather than false;
- the one-doorway callback;
- the company's clear action or no-action decision value;
- one paid diagnostic in a market the operator understands and can reach;
- buyer use before larger responsibility;
- the business-of-one principle as a conditional construction target;
- no new evidence, income promise, question, next-episode tease, or disclaimer retreat after the ruling;
- the exact final CTA.

S12 does not preserve the required negative contrast that the company is `not another dashboard`. Moving a similar line to S07 does not satisfy the immutable ending payload.

Ending verdict: **REVISE**

The exact final sentence remains:

> If you want another business worth testing, like the video and subscribe to The Operator Economy.

No narration or material follows it.

## Exact narration identity

Narration tokens were independently extracted from every `### Narration` block, stopped at the next level-two or level-three heading, split on whitespace, and written one token per line.

- Script spoken-token count: 2,355.
- Read-through spoken-token count: 2,355.
- Ordered one-token-per-line SHA-256 for each: `20310efa5cf66734e5e322c64de6740474726282a0e55de6e8748a426f568ddc`.
- Token-stream comparison: identical.

Narration identity verdict: **PASS**

## Production and revision boundary

The exact v0.9 pair passes file identity, scene order, claim routing other than C005's missing limit, arithmetic, receipt continuity, semantic causal seams, opening sequence, silent sting, brand string, continuation gate, final CTA, and script-to-read-through lexical identity.

It fails the authorized voice-only boundary on four word-changing issues:

1. Restore C005's capability-only, no-buyer-value, and no-service-result limit in S04.
2. Restore the buyer-use or buyer-acceptance completion boundary in S07.
3. Restore the `not another dashboard` contrast inside S12.
4. Replace S09's prohibited second `Okay` and chapter reset with a direct inheritance from S08's delivery question.

Any repair changes the script and read-through hashes. A corrected pair must receive a new exact-hash claims and structure review. This artifact may remain as the immutable v0.9 failure record.

The fixture's public factual claims also remain blocked from production until the live Content OS fact authority contains the required entries and the production gate passes. This review does not approve those facts, an owner cold read, narration generation, Step 2, or publication.

## Final disposition

Fixture claims decision: **REVISE**

Fixture economics decision: **PASS**

Fixture receipt decision: **PASS**

Fixture structure decision: **REVISE**

Production public-fact decision: **BLOCKED**

Owner decision: **PENDING A NEW COLD READ AFTER A CORRECTED PAIR EXISTS**

Recording, narration generation, editorial lock, Step 2 handoff, production, and publication: **NOT AUTHORIZED**
