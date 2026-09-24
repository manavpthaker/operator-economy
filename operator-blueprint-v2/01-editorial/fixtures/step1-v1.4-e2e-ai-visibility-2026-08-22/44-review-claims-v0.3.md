# Claims, evidence, and economics review: AI Visibility v0.3

Status: complete independent fixture review; **REVISE**

Production public-fact status: **BLOCKED**

Review date: 2026-08-22

Reviewer identity: `fixture-claims-reviewer-v0.3-independent`

Scope: claims, evidence delivery, economics, source boundaries, and narration identity only. Story, voice, comedy, and performance are outside this review except where exact wording changes factual meaning.

## Immutable review inputs

| Input | Expected SHA-256 | Verified SHA-256 | Result |
|---|---|---|---|
| `42-script-v0.3-FINAL-CANDIDATE.md` | `b928e5756e11c30595ced4ae874a0bb2969070f40619c8223b8c10e183b66cbf` | `b928e5756e11c30595ced4ae874a0bb2969070f40619c8223b8c10e183b66cbf` | match |
| `43-performance-readthrough-v0.3.md` | `19515cca36bd337a09c1fc46651ffbf6baedb6dcc128be630d19e28fbb049301` | `19515cca36bd337a09c1fc46651ffbf6baedb6dcc128be630d19e28fbb049301` | match |
| `37-claims-map-v0.2.md` | recorded in script | `5db31c8256bcff8b14ccd5fc713dabc34a21ac20854cff6a7fd5ee44419899ae` | match |
| Step 0 `02-research.md` | frozen handoff | `7c0f8445350445060403cd273b986dbb2934a72c898cacb5cbd9e09917595dce` | match |
| Step 0 `03-analogy-map.md` | frozen handoff | `fe51f4a67277e68b1e4f0ccf6fb4381bd5f7c07e189d236ac8433e386c0202bc` | match |
| Step 0 `04-editorial-potential.md` | frozen handoff | `7c5aacfe2494e2066807ba6eb4dfa421e3b0dd2c523f06867715ab625c4945a5` | match |
| Step 0 `05-scorecard-reviewer-a.md` | frozen handoff | `2960fbd719e6859cc59469ff454d29ffe9529e5b1f29abf6984d320bdfc506bd` | match |
| Step 0 `06-canvas-gate-reviewer-a.md` | frozen handoff | `e8faf093894b357c4b8bfb94dcb0f10b0a5df70ca7fa4ef20331d409cfe8d626` | match |
| Step 0 `07-reviewer-b-adversarial.md` | frozen handoff | `67f8aac9e19afa704ef217994e89f1dc42fe6ce8f6d99475ebb821ff60adb628` | match |
| Step 0 `08-promotion-decision.md` | frozen handoff | `4b7a616277e59dbd9fb2470412810c33252555f616d716d2527def6caae9ead1` | match |
| `../content-os/facts.md` | live authority | `fd337d4013d5d2d8ed83f1ba02e9e211c1263c5e3e8d5f119ff1bc5c7e5a4309` | reviewed; public entries absent |

The proposed v1.5 controls were reviewed at these exact hashes. They remain proposed, not approved history:

| Proposed control | SHA-256 |
|---|---|
| `01-editorial/STAGE-GATES.md` | `af496a3fa888d1263859f3b6e1075af00b968e34a5419317b09ff2543f6901c6` |
| `01-editorial/05-script/SCRIPT-STANDARD.md` | `4e55e52f0a7cabe7ee992e56de3ed24e15197d202f4f11c34ac6e19e8df946a0` |
| `01-editorial/05-script/CLAIMS-MAP.template.md` | `dba363df65f5998dc11960302b5c3193e72b00743cd27ff0d6f59b0b79846557` |

## Decision

| Test | Result | Reason |
|---|---|---|
| Source identity, population, and source-class boundaries | pass for the fixture | The used McKinsey, Clutch, Semrush, Ahrefs, and GEO-paper claims match the Step 0 registry and were still current at review. |
| E001 through E011 arithmetic | pass | Every displayed calculation independently reconciles. |
| Audible modeled-status boundary | revise | Test counts appear as buyer facts before the planning-model qualification. |
| No claim drift from Step 0 | revise | The script weakens the approved thirty-day success gate and introduces unsupported certainty about ownership and first-buyer behavior. |
| Proposed v1.5 three-layer evidence delivery | revise | The map does not supply complete, final receipt and show-note content for every material external fact. |
| Script to read-through narration identity | pass | Both contain the same 2,162 spoken tokens in the same order. |
| Production fact authorization | blocked | The AI Visibility survey, source, product, benchmark, and modeled-economics entries are absent from live `content-os/facts.md`. |

Fixture E5 claims recommendation: **REVISE**

Script lock, narration, and downstream production: **PROHIBITED** until the claim-bearing corrections are integrated, a new read-through is derived, and claims review passes on the new hashes.

## Blocking findings

| ID | Severity | Script location | Finding | Required disposition |
|---|---|---|---|---|
| CL3-001 | high | S11, lines 281-285 | The approved Step 0 success signal is `at least three of five` buyers, at least one paid acceptance or specific budget-backed condition, and repeatable manual evidence inside 24 hours. The script says only that unspecified `buyers` name a decision and that delivery stays inside 24 hours. It drops the three-of-five threshold and weakens repeatable evidence to time compliance. | Restore the exact decision meaning in plain spoken language: three of five, one paid or budget-backed signal, and repeatable evidence within 24 hours. If the team wants a different gate, return that change to Step 0. |
| CL3-002 | high | S04, line 127 | `That is the part nobody else owns yet` can reasonably be heard as a market-wide incumbent-absence claim. Step 0 establishes a proposed composite and neighboring alternatives; it does not establish that no team, agency, or firm owns this function. | Replace the market absence claim with the responsibility the proposed company would own. A literal `nobody else` claim requires new evidence and a Step 0 amendment. |
| CL3-003 | high | S07 line 175; S08 line 209; qualifier first appears at S09 line 225 | `The first buyer isn't going to... They need...` turns an untested entry design into observed buyer behavior. It also introduces one brand, one market, ten questions, two surfaces, 25 brands, and a three-question screen before C008's required audible model frame. | Present the bounded scope as OE's recommended test, not a fact about what the first buyer will do. Qualify the test model before its first count, not only before the money section. |
| CL3-004 | medium | S03, line 91 | `McKinsey found that roughly half the people it surveyed...` is correctly bounded. The next sentence, `Customers added another doorway`, broadens the subject from surveyed people to customers generally. The screen cannot repair that audio-only scope change. | Keep the follow-on tied to the surveyed group or explicitly say `some customers`. |
| CL3-005 | medium | S06, line 163 | `AI... can't decide` expresses a responsibility rule as a categorical technical incapacity. The approved package says AI may collect, organize, compare, and draft while the operator retains authority, validation, judgment, and the final recommendation. | State who must own the decision rather than claiming that AI is incapable of producing one. |
| CL3-006 | high | `37-claims-map-v0.2.md`, lines 54-76 | The proposed v1.5 delivery contract is not complete. C001 and C002 have partial receipt and show-note rows, but their receipts omit required artifact/date details and their show-note text does not explicitly carry methodology plus known limitation. C004 through C006 have no completed three-layer rows; the catch-all pointer to Step 0 is not a release-ready show-note registry. | Complete the evidence-delivery registry for every used external claim. Supply exact receipt copy and full show-note copy for C001, C002, C004, C005, and C006. Split a claim if two vendor sources cannot be represented clearly in one row. No new research is required unless the intended wording exceeds the existing source boundaries. |

CL3-001 through CL3-003 and CL3-006 independently require a **REVISE** result. CL3-004 and CL3-005 should be repaired in the same bounded pass because they affect audio-only honesty.

## Claim-by-claim audit

| Claim | VO use | Source, population, and caveat finding | Evidence-delivery finding | Result |
|---|---|---|---|---|
| C001 | S03 | McKinsey attribution, `roughly half`, and `people it surveyed` accurately preserve the August 2025 representative U.S. consumer-panel result, n=1,927. The immediate plural `Customers` sentence overgeneralizes. The finding does not establish universal behavior or service demand. | Conversational attribution is good. The proposed receipt and show-note content are incomplete under v1.5. | revise |
| C002 | S03 | The source mix is correctly presented as variable by question, category, and platform. No universal source rule, controllability claim, or optimization result is stated. | Audio is honest. The receipt needs exact artifact and publication details; the show-note entry needs explicit method and limitation. | revise package only |
| C003 | not used | The small CMO sample and 16 percent figure are omitted, as allowed. | No delivery row is needed while omitted. | pass |
| C004 | S04 | Clutch supports the neighboring SEO purchase forms. The script explicitly says this does not prove demand for this offer or transfer SEO pricing. | No completed exact receipt or full show-note row exists. | revise package only |
| C005 | S04, S06 | Semrush and Ahrefs support prompt, mention, competitor, citation, and source-pattern collection features. The script does not infer buyer value, demand, service quality, or client outcome from them. | No completed exact vendor receipts or full show-note entries exist. | revise package only |
| C006 | S04, S06 | The GEO paper supports measurability in its benchmark and domain-varying effects. The script does not use the paper as a current-engine or client-outcome guarantee. | No completed benchmark receipt or full show-note entry exists. | revise package only |
| C007 | S02, S04-S08, S10, S12 | The company is generally presented as OE's proposed build. The `nobody else owns yet` phrase crosses into unsupported market-wide certainty, and `AI can't decide` blurs authority with capability. | Label the company as OE synthesis on screen as already required. | revise |
| C008 | S07-S12 | All money and capacity arithmetic stays modeled, with unknown price, reach, workload, and tax or unlisted-cost limits audible. The early test counts are unqualified, and the Step 0 success gate changes meaning. | Every displayed model must remain labeled `MODELED` with arithmetic and exclusions on the same screen. | revise |
| C009 | not used | Search volume remains unknown and receives no unsupported inference. Omission is allowed. | No delivery row is needed while omitted. | pass |
| C010 | S12 | BUILD remains an editorial recommendation to construct and test a bounded company. It is not presented as proof of demand, outcomes, sustainability, or income. | Preserve `OE EDITORIAL VERDICT: BUILD` on screen. | pass |

## Independent E001-E011 reconciliation

| ID | Independent reconstruction | Script result | Finding |
|---|---|---|---|
| E001 | $2,000 validation diagnostic | $2,000 | pass as modeled input, not accepted or market price |
| E002 | 16 hours x $60 = $960 | $960 | pass |
| E003 | $99 software + $300 listed acquisition and overhead = $399; two projects use $198 and $600 | same | pass; cost list remains incomplete and modeled |
| E004 | $2,000 - $960 - $99 - $300 = $641 | $641 | pass; `before tax and unlisted costs` is audible |
| E005 | Per working project: 24 x $60 = $1,440; $3,000 - $1,440 - $399 = $1,161. Two projects: $6,000 - $2,880 - $198 - $600 = $2,322. | $1,161 and $2,322 | pass; not capacity, margin, or earnings evidence |
| E006 | Five interviews, 25 prospects, ten questions, two surfaces, and 24-hour boundary | same counts | arithmetic not applicable; test meaning fails because the three-of-five and repeatability conditions are missing |
| E007 | $48,000 annual owner-support target | $48,000 | pass as fixture planning input only; not expected income |
| E008 | 20 hours x 48 weeks = 960 hours; 2 diagnostics x 12 months = 24; 24 x 24 hours = 576; 19 x 24 hours = 456; 960 - 456 = 504 | 960, 24, 576, 456, and 504 | pass; utilization and total workload remain unproven |
| E009 | $3,000 - $99 - $300 = $2,601 available for owner labor and support | $2,601 | pass; not contribution margin or take-home pay |
| E010 | $48,000 / $2,601 = 18.454440599769; round up = 19 | 19 | pass; not expected sales or demand |
| E011 | 19 / 250 x 100 = 7.6 percent | 7.6 percent | pass; travel is only the arithmetic carrier, 250 is not an addressable market, and 7.6 percent is not a conversion forecast |

Arithmetic verdict: **PASS**

Meaning and disclosure verdict: **REVISE** because E006 is changed and C008's model frame arrives after the first modeled test counts.

## Exact narration identity

The narration blocks were independently extracted from both frozen files and tokenized on whitespace.

- Script spoken-token count: 2,162.
- Read-through spoken-token count: 2,162.
- Ordered-token SHA-256 for each: `196473342d21ffad2cb3210327086e8762eb7ad62142bec2cd0906fe522fcf98`.
- Ordered-token comparison: identical.
- Raw extracted-text comparison differs only by one final blank line after the script's last narration block. It changes no spoken word.

Narration identity verdict: **PASS**

## Production boundary

The fixture evidence is traceable, and the linked source content matched the Step 0 descriptions at review. That does not create production authority.

The live `../content-os/facts.md` contains no approved AI Visibility entries for the McKinsey survey, source analysis, Clutch parallel, Semrush or Ahrefs capabilities, GEO benchmark, or E001-E011 model. Therefore:

- Production facts remain **BLOCKED**.
- This review does not approve publication, narration, recording, or downstream production.
- A later real episode must refresh sources at the recorded dates, route every used fact through Content OS, and preserve the approved receipt and show-note copy.

## Bounded revision path

1. Restore the Step 0 three-of-five, paid-or-budget-backed, and repeatable-within-24-hours success gate.
2. Replace the unsupported `nobody else owns yet` wording with the responsibility this proposed company would own.
3. Frame the first offer and its counts as the bounded OE test before the first modeled number appears.
4. Keep the McKinsey follow-on sentence inside the surveyed-population boundary.
5. Express the AI and human split as decision ownership and accountability, not categorical incapacity.
6. Complete v1.5 evidence-delivery rows for C001, C002, C004, C005, and C006.
7. Derive a new read-through from the revised script and rerun claims review against both new hashes.

These corrections do not alter the approved company thesis, BUILD doctrine, market-selection lesson, economics inputs, or arithmetic. No Step 0 amendment is needed if the wording is narrowed back to the approved package. A Step 0 amendment is required only if the team intends to retain the market-wide ownership claim or weaken the approved validation gate.

## Final disposition

Fixture E5 claims decision: **REVISE**

Production E5 facts decision: **BLOCKED**

Script lock: **PROHIBITED**

Owner decision: pending after bounded revision and fresh review
