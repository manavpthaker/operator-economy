# Step 0 promotion record: Direct booking recovery (legacy EP006 premise)

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-direct-booking-recovery`

Decision date: 2026-09-03

Decision approved by: Manav Thaker

Research cutoff: 2026-09-03

Research refresh date: 2026-12-03 for OTA programme mechanics, tool prices, agency prices, litigation status, and audience snapshots; 2027-03-03 for SEC filings, association studies, and AHLA surveys

Decision: **promoted**

Evidence class: **adjacent synthesis**

## Reviewed artifacts

- Candidate brief: `../01-candidates/candidate-2026-09-03-direct-booking-recovery.md` / `70e5a289bf15f5603f9ebd0cb4d958116852d76bcd5f2e620427f3753c342c9c`
- Research brief: `../02-research/candidate-2026-09-03-direct-booking-recovery.md` / `07c61fa3fca535f9569670dbe73c6e823eaa3ab33ba5e67f7c22519a5194e5d7`
- Analogy map: `../03-validation/candidate-2026-09-03-direct-booking-recovery-analogy-map.md` / `95953ffbad5710907e58d12f849ea95b3c188d1f3dc37c41a2a14f73d3df6a18`
- Opportunity-readiness scorecard: `../03-validation/candidate-2026-09-03-direct-booking-recovery-scorecard.md` / `9955b26c75614ee684d7758e31f0349e870bd5c8e04d34d44d32a0651b60df62`
- Canvas feasibility review: `../03-validation/candidate-2026-09-03-direct-booking-recovery-canvas-gate.md` / `da23ab7ad96039c65afb52268c850bf36219d7dac607da0361db891d231eb4e7`
- Narrative and audience-pull review: `../03-validation/candidate-2026-09-03-direct-booking-recovery-editorial-potential.md` / `dc475e90b057a94563f43fd4284aafe2acdeb6b27f0f31fcbb89e4d750ce6ac8`

Supplementary review considered by the owner (not one of the six bound artifacts):

- Adversarial second review (Reviewer B, 61/100, continue research): `../03-validation/candidate-2026-09-03-direct-booking-recovery-reviewer-b-adversarial.md` / `fa42f54c9130f93431a7a8c91d63e55d3f6b90ced774b5aa4f1c78506e88af23`
- Early disposition record written before the owner review (continue research; now superseded by this record): `../03-validation/candidate-2026-09-03-direct-booking-recovery-disposition.md`

## Decision summary

- Opportunity-readiness score: **70/100** (Reviewer A, the scorecard of record)
- Numeric threshold: **pass** (exactly at the threshold)
- Calibration zone: **65-75** (70)
- Required owner review: **complete** (below)
- Evidence and analogy floor: **pass**
- Canvas feasibility: **pass** (go-to-market weak; economics passes on transparency)
- Narrative engine: **pass**
- Audience pull: **pass**
- POV: **pass** (5/7 under Step 0.3: two years as Director of Customer Experience at Coqui Coqui, bounded, plus one named synthesis finding on the recoverable-commission ceiling)
- Factual and source blockers: **clear for the blueprint**, conditional on opening the Booking.com partner pages before any script lock (carried below)
- Legal, permission, access, or guest blockers: **clear** (OTA partner terms, CAN-SPAM, and GDPR are design constraints handled by consent-first design)

## Owner override

Used: **no**

The score passes the numeric threshold. The override does not waive hard gates or change the evidence class.

## Calibration-zone review

Required: **yes**

Reviewed by: Manav Thaker

Decision date: 2026-09-03

Decision: **promote**

Reason: The owner reviewed the set-level record (`../LEGACY-EPISODE-REVIEW-2026-09-03.md`), the Reviewer A scorecard at 70, and the Reviewer B adversarial pass at 61, and elected to promote. Owner statement of record, 2026-09-03: "Yes let's promote 1 and 6." Both reviewers recommended continue research until the first owner conversation and the Booking.com pages were recorded; the owner chose to carry those items into Step 1 as pre-lock conditions and the episode's first construction step. Every hard gate passed on both reviews. Both reviews agree on the single untested hop, willingness to pay under the ceiling, and on the required disclosure; they disagreed only on whether the threshold should clear before that hop is tested.

## Public framing contract

- Model description: **synthesized from parallels** (outsourced revenue management and independent-hotel marketing agencies, which are bought by larger properties)
- Economics language: **modeled scenario, not observed performance or an earnings forecast**
- Load-bearing assumptions to say plainly:
  1. **The retainer is bounded by the property's recoverable commission.** At a modeled 20-room property (20 rooms, $180 ADR, 70 percent occupancy, 63.4 percent OTA share, 18 to 22 percent all-in commission, 10-point mix shift, 3.5 to 5 percent direct cost) the net recoverable is roughly $1,000 to 1,400 a month. The service must price under that line, and the viewer runs the arithmetic on real inputs. This is the finding the V1 episode never computed.
  2. **No verified operator sells a recovery-first audit-plus-retainer to 20 to 40 room properties at disclosed economics.** The adjacent agencies price at $1,500 to 6,000 and size for larger properties.
  3. **The level of OTA dependence in the US 20 to 40 room band is not independently sourced.** The 63.4 percent figure is global and vendor-published.
  4. **Whether a 20 to 40 room owner pays $600 to 1,250 a month when the recoverable commission is of the same order is the whole business** and is unknown. The viable band may be narrow, or may sit at 40 to 80 rooms.
- Claims the episode may not make:
  - Any RevPAR uplift, commission saved, or direct share gained stated as an observed result.
  - The $135,000 or any commission-line figure without its four inputs and the word "illustrative."
  - Revenue-management vendors' uplift claims.
  - ZipRecruiter salary data as a client price or income figure (retired from the package).
  - "I ran a hospitality business," or that Manav has sold or delivered this service, or was a revenue manager.
  - That the property should leave OTAs. The episode describes a mix shift, never an exit.
- Required source and qualification notes:
  - OTA share and cancellation-by-channel are attributed to Cloudbeds every time; programme mechanics are attributed to Booking.com or Expedia every time; HOTREC's lower European direct-share figure stays visible.
  - The Booking.com partner pages behind CLM-005 and CLM-008 (commission mechanics, guest-data policy) returned HTTP 403 on 2026-09-03 and are currently secondary. They must be opened in a browser and recorded on the day before any script lock.
  - Guest-data use is described only inside OTA terms and consent law: no marketing to masked addresses, on-platform communication where required, CAN-SPAM for the first-party list, GDPR for EU guests.
  - Programme rules, tool prices, and agency prices are time-sensitive; refresh by 2026-12-03.

Before release, public facts and every stated number still require approval under `content-os/facts.md`.

## Caveats carried forward

- **Pre-lock conditions (Step 1 may draft but may not lock a script until these are recorded):** the Booking.com partner pages opened and recorded; and either an independent US source for OTA share and commission profile by property size or the audit data from validation step 1, before the band's dependence is stated as anything other than a global vendor figure.
- **The first construction step is the thirty-day plan:** run the audit on three properties in the band (one unpaid, two at the audit fee), put the ceiling number and a retainer below it in front of each owner, and record the answers. BUILD at E3I must be argued against that test, with the redesign route (40 to 80 rooms, or audit only) stated.
- **Go-to-market is weak.** Referral paths through PMS and channel-manager partner managers and innkeeper associations are hypotheses in the plan, not observed.
- **POV boundary:** two years in boutique hospitality as Director of Customer Experience, bounded. The ceiling arithmetic is credited as synthesis; the guest-record-expiry point reframes a fact published in trade press on 2026-08-25.
- **The V1 episode EP006 remains published** with its own launch record. The rescript must not restate its URL by hand; only `studio/originate/direct-booking-recovery/launch/links.json` may state it.

## Handoff

Editorial development authorized: **yes**

Future episode number: **unassigned**

Episode number assignment is recorded only when the promoted candidate enters `01-editorial/`.

## Invalidation

Package status: **current**

This decision applies only to the six reviewed artifact hashes above. A changed artifact hash or passed research refresh date makes the promotion stale. Mark the active queue row `stale`, stop editorial development, refresh the affected work, and issue a new promotion record before resuming.

## Note

This is the third candidate promoted through Operator Blueprint V2, promoted from the threshold on an explicit owner review. The published V1 episode EP006 keeps its number and its artifacts; this promotion authorizes a V2 rescript under a new number.
