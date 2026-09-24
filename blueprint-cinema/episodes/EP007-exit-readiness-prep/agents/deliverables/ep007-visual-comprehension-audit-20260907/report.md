# EP007 visual-comprehension audit

Read-only engine-critic packet. It diagnoses meaning and prompt constraints; it does not approve a
shot, change the locked script, or authorize generation, implementation, rendering, or publication.

## Packet identity

All three work-order inputs matched their issued SHA-256 values.

| Input | Recomputed SHA-256 |
| --- | --- |
| `operator-blueprint-v2/episodes/EP007-exit-readiness-prep/01-editorial/script.md` | `e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0` |
| `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r3-relevant-edit/compositions/model-exposure.html` | `0d4fa07954d85e9f70e4f0f5c6405a0c9e479b442ac2fe706f3d9fd7bc6ee82a` |
| `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/GENERATION-PROMPTS.md` | `2940abcb63260bc7b1d50c44a6a8a96d64cd700893fde93107c72b3d93ab6001` |

## Verdict

The current equation is defensible; the stopped-work conclusion is not.

The locked cold open establishes a buyer's month-away question, the owner's inability to answer it
immediately, and an unfavorable mental calculation (`script.md:17-23`). It does not establish a
specific workflow, a stopped task, or total operational shutdown. The ending resolves the callback
through an answer that is written, readable, and checkable, while explicitly saying that nothing
about the business changed (`script.md:409-413`). The episode's durable subject is therefore
**inspectability under owner absence**, not proven cessation of work.

The simplest bounded visual question is:

> Can the buyer verify, from records rather than her memory, what happens during a 30-day owner
> absence?

Keep that question unresolved in the opening. Do not turn it into “the business stops” or even “this
task stops” unless a later, explicitly hypothetical test is labeled as such.

## What the current sketch actually claims

### Established in source

- The typeset equation keeps `BUSINESS AS IT RUNS TODAY - OWNER FOR 30 DAYS = ?`
  (`model-exposure.html:189-204`). This accurately expresses the unanswered test.
- The animation later draws owner-held relationships, undocumented process, and unverifiable
  records; connects all three to one owner checkpoint; moves the owner outside a one-month bracket;
  routes one work token to the now-empty checkpoint; and draws a stop mark
  (`model-exposure.html:208-356,425-467`).
- The moving-plate prompt independently asks a ticket to return to the owner “for action”
  (`GENERATION-PROMPTS.md:66-70`), and the post instruction asks for a
  `ticket -> owner checkpoint -> unfinished leg` route before the graphic cut
  (`GENERATION-PROMPTS.md:80-89`).

### Reasonable viewer inference

Although only one token literally stops, the three concurrent inputs, single trunk, absent owner,
and terminal stop make the frame read as a general owner bottleneck. A viewer can reasonably infer
that all meaningful work depends on her and fails in her absence. That is a visual-comprehension
judgment, not a fact stated by the source.

### Strongest contrary reading

The retained question mark and single token could be read as one hypothetical stress test rather
than a finding about the whole business. That interpretation would be defensible if the graphic
declared the token as a test case and preserved uncertainty. It currently does neither. The
converged dependency map and unqualified stop mark make the broader failure reading more likely.

## Ranked findings

### 1. Blocking for semantic reuse: the animation answers an unanswered question

The script supplies hesitation, not an observed operational failure (`script.md:19-23`). The
animation supplies an `interrupt` outcome: a persistent work item reaches the empty owner checkpoint
and stops (`model-exposure.html:446-467`). Boundary Ledger defines `interrupt` as an actual stopped,
broken, rejected, or unavailable route (`design-system/boundary-ledger/semantic-core.json:61-63`).

**Requirement:** keep the opening state `UNKNOWN`. A later one-item stress test may show a hold only
when the prompt states that it is a hypothetical test, identifies what the item represents, and
forbids extrapolation to the whole business.

### 2. Major: three later alternatives become one simultaneous diagnosis

S09 says the failure appears in three different shapes: relationships, concentration, or records
(`script.md:151-159`). The current sketch substitutes “undocumented process” for concentration and
shows all three conditions operating together through one owner route
(`model-exposure.html:208-292`). This changes both membership and logic.

**Requirement:** prompts must preserve alternatives as alternatives. `Sometimes`, `if`, and “one of
two things” are branching words, not permission to show every branch as simultaneously true.

### 3. Major: a buyer-verification problem becomes a daily-work route

The records case is “no way for a stranger to confirm” that the business makes money
(`script.md:157-161`). That is an inspection and pricing problem. Routing the records node into the
same work trunk as operating process implies that bad records stop ordinary work. The script does
not say that.

**Requirement:** every graphic prompt must name what moves. Evidence, a customer relationship, a
recurring task, and a buyer decision are different persistent objects and may not share one route
merely because they all involve the owner.

### 4. Major: S09 explanation is revealed inside S00

The model code explicitly reveals the three explanatory conditions as the “second half” of the
cold-open sentence (`model-exposure.html:425-444`), but those conditions are not narrated until S09
(`script.md:147-161`). This is not useful anticipation; it prematurely diagnoses the woman and asks
the audience to parse a later framework before the episode has earned it. Boundary Ledger requires
text to label or land meaning rather than animate the narration ahead of itself
(`design-system/boundary-ledger/semantic-core.json:89-98`, especially `U-06`).

**Requirement:** attach a `not_before` cue to every factual label, number, branch, and result. No
later mechanism or taxonomy may appear in the cold open merely because it will eventually be
explained.

### 5. Major: illustrative props are doing evidentiary work

The shared continuity prompt invents a workshop, employee, binder, keys, ticket, and work surface
(`GENERATION-PROMPTS.md:31-43`). A generated world may use invented continuity detail, but the
employee and returning work ticket are not neutral once the scene asks whether the business runs
without the owner. They can imply staffing, delegation, and a specific operating route that the
script never establishes. Generated footage is illustration, not evidence, and may not invent story
logic (`.agents/skills/oe-film-direction/references/generated-plates.md:1-4`).

**Requirement:** distinguish `continuity_only` props from `meaning_bearing` objects. An invented prop
may texture the world; it cannot prove the dependency under examination. Freeze or omit background
action that implies an answer.

### 6. Major: the physical-page carrier can look owner-authored

The historical post instruction places an explanatory route beneath the owner's hand before carrying
it into the Working Model (`GENERATION-PROMPTS.md:80-89`). That can make the analysis look like a
diagram the owner physically drew or endorsed. The current model instead declares a hard editorial
cut with no physical-page carrier (`model-exposure.html:187`), which more honestly separates an
illustrative observation from editorial analysis.

**Requirement:** generated documents remain blank and non-evidentiary. Introduce exact analysis on a
clearly authored graphic surface after the cut unless a real, identity-preserving carrier exists.
Do not preserve a transition for elegance when it changes who appears to be making the claim.

## Whole-script prompt guardrails

These are minimum constraints for the proposed Phase 2 to Phase 3 prompt pack. They are not shot
designs.

| Script scope | Failure to block | Minimum prompt requirement |
| --- | --- | --- |
| S03-S05, `script.md:55-89` | Broker or success-fee system becomes a villain before its useful job is established | Show the useful current system first. Treat compensation as structure, not greed. Do not use risk color, hostile blocking, or crisis performance. |
| S06-S07, `script.md:99-123` | Directional `3 in 10`, offer counts, and source bias become verified universal facts | Keep source identity and “directional” caveat attached to each number. Generated businesses, offers, or charts cannot serve as proof. Do not reveal the comparison result before both inputs and caveats land. |
| S08-S09, `script.md:133-161` | Conditional owner dependence becomes certain shutdown; alternatives become a combined diagnosis | Preserve `if`, `sometimes`, uncertainty, and branch exclusivity. Do not literalize “machine” as a generic mechanism. Keep relationships, concentration, records, task flow, and buyer pricing as distinct objects and consequences. |
| S10-S12, `script.md:171-229` | The five Ds become sensational imagery; professionals look negligent; adjacent practices become proof of this exact business | Keep sensitive exits abstract and sourced. Preserve each professional's legitimate job and compensation timing. Treat the three comparison professions as analogies, not proof that the proposed small-owner practice already exists. |
| S13-S14, `script.md:239-263` | The proposed mature practice looks operationally proven; the narrator appears credentialed for transaction work; licensure becomes a categorical map | Mark the company as a proposed model. Preserve the narrator's explicit limits. Do not depict deal credentials, legal clearance, or state-by-state certainty not present in source. |
| S15-S18, `script.md:273-335` | AI appears to judge buyers, fix structural problems, or deliver a sale; a signed checklist reads as verified sale readiness | AI may draft, organize, and assemble. Human judgment owns discount, fixability, scope, and the difficult owner conversation. Keep valuation, buyer search, negotiation, and transaction advice outside the service. A signature accepts the checklist deliverable; it does not verify a sale or legal compliance. |
| S19, `script.md:345-353` | Referral channels look validated and broker-free preparation looks proven | Keep broker access and free incumbent service as unresolved market tests. Do not show a working referral funnel, booked pipeline, or available front door as an observed result. |
| S20, `script.md:363-381` | Modeled arithmetic becomes revenue evidence or an earnings promise | Keep `MODELED SCENARIO`, assumptions, and tax/pay caveats visible with the numbers they govern. Reveal values only after their spoken cue. Never use verified-state styling. Keep `85 hours` as the central unknown, not a settled parameter. |
| S21, `script.md:391-399` | Two kill conditions are depicted as already true or collapsed into one dramatic failure | Preserve them as independent falsifiers: owner deferral and brokers already doing the work free. Show neither as fact without evidence. |
| S22-S25, `script.md:409-449` | The callback shows a transformed or newly profitable business; `BUILD` reads as proof; the free diagnostic reads as a customer success | Resolve inspectability, not operations or revenue. Preserve “nothing about the business changed.” `BUILD` means construct a test despite an uncleared base case. The first diagnostic exists to measure hours, not prove demand, readiness, or earnings. |

## Reusable Phase 2 to Phase 3 prompt contract

Prompt optimization here means constraining meaning before adding cinematic detail. Every scene or
graphic prompt should carry these fields:

1. `narration_lock`: exact script path, line range, and word/time range when available.
2. `picture_audio_mode`: one declared mode and language carrier.
3. `visual_proposition`: one sentence stating the only claim the picture may make.
4. `epistemic_status`: `observed`, `reported_directional`, `modeled`, `hypothetical`, or `unknown`.
5. `forbidden_inferences`: the two or three most likely unsupported conclusions.
6. `primary_object`: one persistent customer, task, record, number, claim, or decision. Never “the
   business” when the source supports only one test case.
7. `before_state`, `operation`, `after_state`, `settle`: finite and causally linked. Use `unknown` as
   an end state when the narration has not answered the question.
8. `continuity_only` and `meaning_bearing` objects: separate lists. Continuity detail may not quietly
   become evidence.
9. `what_stays_still`: the world, inactive branches, landed evidence, and settled marks unless the
   one operation changes them.
10. `not_before` and `clear_by`: exact cue for each label, number, branch, result, and evidence pin.
11. `evidence_binding`: source/claim ID and caveat, or explicit `none`. Generated media never fills a
   missing evidence slot.
12. `visible_text`: exact typeset text only. No invented generated documents, interfaces, figures,
   or handwriting carrying claims.
13. `mute_test` and `audio_only_test`: picture cannot solicit unheard dialogue; narration cannot
   require the graphic to carry a principal risk or qualifier.
14. `reject_if`: deterministic semantic failures first, then continuity and aesthetic failures.

Global rejection language should include: reject if a conditional becomes certain; alternatives
appear simultaneous; an illustration looks evidentiary; a result arrives before its spoken premise
or caveat; a useful dependency becomes a villain; an unknown receives verified or success styling;
an invented prop changes the business logic; or motion continues after the accountable change has
settled.

## Follow-up review of the proposed prompt handoff

Inspected the corrected follow-up inputs:

- `prompt-handoff-review/PROMPTS.md` at SHA-256
  `9aa1faac090346bf65616dba3f776c5312080cbade6e46fd1bbcecda1d1c6a5a`
- `prompt-handoff-review/EP007-BEAT-INTENT.md` at SHA-256
  `f1e1197d6ed0a49ca171eebf1b4ca437ef28087faa3c052b11fac51068333b0b`

The proposed pack fixes the central comprehension defect: it states that `UNKNOWN` is not failed,
protects reveal order, rejects the current premature condition list and stopped-work inference, and
keeps all 3,186 W tokens in contiguous section spans. The silent S01 interval is separately retained.
The follow-up also now supplies the named `AUDIT.md`, distinguishes continuity-only props from
meaning-bearing objects (`PROMPTS.md:45-48`), states that episode V7 remains future
(`PROMPTS.md:185-188`), describes the practice as a test (`EP007-BEAT-INTENT.md:10-13`), names the
three S12 analogues literally (`EP007-BEAT-INTENT.md:51`), and avoids turning the modeled `$86k`
balance into an accounting category (`EP007-BEAT-INTENT.md:59`). No substantive meaning gap or
overstatement remains in those corrected passages. The final intake prompt also distinguishes the
legacy transcript validator incompatibility from byte, word, and timing correctness
(`PROMPTS.md:72-75`) and carries the 16-bit/24-bit and independent-listen mismatches without claiming
they were resolved (`PROMPTS.md:95-103`).

The per-act approval instruction at `PROMPTS.md:138-161` is valid. The governing gate explicitly
requires V4 review and named human approval per act, and returns only the rejected act
(`operator-blueprint-v2/03-visual-translation/STAGE-GATES.md:104-124`). The earlier contrary audit
note is withdrawn.

The prior spacing defect at `EP007-BEAT-INTENT.md:67-69` is resolved. A final full read at the hashes
above found no new substantive comprehension gap or overstatement. These are supplemental review
sources only; the three issued work-order input pins remain unchanged.

## Limits and unresolved authority

- The exact c03 prompt is referenced at `GENERATION-PROMPTS.md:3-7` but is not one of this work
  order's hash-pinned inputs. This packet does not claim an exact c03 prompt audit.
- No real company workflow, task identity, or month-away result is supplied. A specific stopped task
  would therefore remain hypothetical even if the prompt labels it honestly.
- No encoded review movie or snapshot was pinned. This is a source-semantics and prompt audit, not a
  playback, timing, compression, or final-composition approval.
- The supplemental prompt documents and this ad hoc reviewer packet are not production-dispatch
  validated. Their repository-relative input/output routing does not satisfy the Blueprint-Cinema-
  relative dispatcher contract; validation stopped at that routing/precheck boundary. This does not
  invalidate the read-only findings, but it grants no production or gate approval.
- Nothing found requires rewriting the locked narration. The defects are downstream visual claims,
  sequencing, and prompt boundaries.
