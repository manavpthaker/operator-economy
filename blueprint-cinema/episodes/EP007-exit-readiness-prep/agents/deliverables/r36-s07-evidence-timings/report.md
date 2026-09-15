# R36 S07 evidence and timing audit

All three issued input hashes match. The exact 87% / 33% claims are verified in the original public Q2 2026 announcement. The complete Q2 survey results are not publicly accessible, so subgroup counts and raw response validation remain unavailable. This is a bounded audit, not a creative acceptance or publication gate.

## Evidence result

The original [Q2 2026 Market Pulse announcement](https://www.prnewswire.com/news-releases/the-market-pulse-survey-q2-2026-reports-the-latest-trends-in-business-sales-up-to-50m-302858664.html), published August 25, reports 87% receiving at least three offers and 33% receiving ten or more in the over-$5M segment. It describes 255 responding advisers and 181 completed transactions overall; neither is the denominator of this specific size band. Do not use either count to draw a measured cohort.

The local CLM-003 record at `operator-blueprint-v2/00-intake/02-research/candidate-2026-09-01-exit-readiness-prep.md:148` points to that release, although its locator says “Quarterly executive summary.” Retain the actual retrieved source type as a public announcement; do not call it an inspected full report.

The original [IBBA Q2 highlights PDF](https://www.ibba.org/wp-content/uploads/2026/08/mp-highlights-q2-2026.pdf) labels the upper studied band $5M–$50M. It does **not** contain the 87% / 33% offer figures. Its buyer-interest chart explicitly concerns adviser sentiment rather than completed transaction activity; that chart cannot serve as evidence for C005's offer percentages.

[IBBA's research page](https://www.ibba.org/resource-center/industry-research/) restricts the executive report and complete results to participants. The public [participation guide](https://www.ibba.org/resource-center/industry-research/participate/) says the wider survey also includes pending deals and market trends. Therefore, say these are the reported closed-deal figures, not that every survey question measures closings. The currently linked [sales tracker](https://www.ibba.org/wp-content/uploads/2024/04/quarterly-sales-tracker.xlsx) places offers beside final sale price and time-to-close fields; it supports the transaction context but is a generic earlier template, not the Q2 microdata.

The closed-deal restriction matches approved C005 and this transaction context; the exact Q2 question-level inclusion rule cannot be independently reconstructed from the public highlights or press release alone. Preserve the restriction while reporting this verification limit.

## Same denominator, nested thresholds

The release's two percentages describe the same size-restricted cohort. Receiving ten or more offers necessarily satisfies receiving at least three. A nested visual is valid if its areas preserve that common denominator:

- 87% of the displayed whole meets the 3+ threshold.
- 33% of the **same whole** meets the 10+ threshold, inside the 87% group.
- Do not add 87% and 33%. Do not portray 33% as a fraction of the 87% group.
- If the inner segment is sized relative to an already shortened 87%-width parent, its width would need to be 33/87 of that parent, not 33%. Prefer a shared 100%-width coordinate system to avoid this implementation trap.

This is a logical nesting inference from the thresholds and common reported population, not a new empirical estimate. Rounding, exact subgroup sample size, response exclusions, weighting, and the original offer-category table were not accessible. Avoid deriving an exact number of deals, confidence interval, or additional displayed percentage from these rounded summaries.

Keep the labels **reported closed deals over $5M**, **Q2 2026**, and **IBBA / M&A Source** attached while the statistics are visible. The study's upper scope is $50M; a compact $5M–$50M band label preserves that context. The locked narration's “above five million” should not be rewritten here. Preserve “adviser-reported; directional” in the evidence treatment.

## What the contrast does and does not show

S06 concerns businesses listed for sale; S07 concerns the selected reported closings in a larger transaction band. These are different populations and different sources. The contrast can show that strong buyer competition exists in one part of the market while many listings fail to sell. It cannot prove a shared funnel, a causal reason for non-sale, that every small-business listing has bidders, or that this seller will receive these offers. Do not transition the same countable business objects from the S06 denominator into S07.

The final “when somebody finally looks” can hand attention to inspection. It is an interpretive narration turn, not an observed buyer verdict. Departure remains a later S09 alternative; no sale, rejection, or readiness-caused success should be invented in S07.

## Timing recommendation

S07 speech spans W000595–W000720, master **203.32–250.22**, review **200.32–247.22**. The retained prefix ends at master203.125 / review200.125. The next section begins with W000721 at master250.98 / review247.98.

A convenient 24fps proposed section boundary is master **250.625**, review **247.625**, within the transcript gap before S08. That gives an extension of **47.5 seconds / 1,140 frames** from the retained prefix. This is not a waveform-verified clean cut. Root must check the source audio and select a silent frame if an excerpt stops there; when continuing S08, preserve the original gap and narration unchanged.

The caveat is W000646–W000660, master **223.08–228.71**, review **220.08–225.71**. “Side by side” begins W000661 at master229.5 / review226.5; the interpretation should not erase the cohort labels. “Finally looks” ends at master250.22. `cues.json` provides sentence and reveal word ranges, exact source/review timestamps, and nearest-frame proposed visual anchors. Numerical reveal anchors occur on the spoken number or threshold; establish the population before them.

## Provenance and limitations

Five primary source artifacts were retrieved into this owned packet and hashed in `retrieved-source-manifest.json`. A transcript-derived cue file is included. The failed web PDF screenshot attempt added no evidence; the public PDF's text and original file were retrieved. No restricted report was accessed, no survey was submitted, and no provider/paid work, runtime, narration, skill, or decision-history edit occurred. Full report access remains unavailable, but that does not negate the directly accessible public numeric announcement.
