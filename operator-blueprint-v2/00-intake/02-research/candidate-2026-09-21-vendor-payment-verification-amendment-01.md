# Research amendment 01: desk re-entry pass under the coaching standard

Candidate ID: `candidate-2026-09-21-vendor-payment-verification`

Discovery lead: `DISC-2026-09-20-001`

Date: 2026-10-12 ET (Monday bench)

Purpose: run the desk re-entry set by the 2026-09-28 disposition addendum. Three items: (a) document
the delivery boundary from primary sources, (b) find buyer-side price or spend evidence of an
accepted type (a posted request with a budget, a disclosed engagement, or old-way spend), and
(c) convert the four former field items into a viewer's first test with success and kill signals.

Prior artifacts unchanged: candidate brief, research brief
(`candidate-2026-09-21-vendor-payment-verification-research.md`), and disposition decision history.

## Search scope

Eight web searches (four standard, four extended) and three source reads, all accessed 2026-10-12:

1. Social-engineering-fraud coverage conditions: callback / pre-arranged verification endorsements.
2. Bank originator agreements and 2026 Nacha fraud-monitoring customer notices.
3. Read: Intact Insurance form M350 (03-20) endorsement PDF (text extracted locally).
4. Read: Lowenstein Sandler client alert, 2023-02-27.
5. Posted requests with a budget: freelance job posts for AP vendor-change or internal-control setup
   (general web and `upwork.com`-restricted).
6. Disclosed engagements: council, school-board, or nonprofit approvals of AP / vendor-master
   control reviews with a contract amount.
7. Disclosed engagements after a loss: small public bodies hiring a firm to review controls after a
   vendor-impersonation payment.
8. Read: search-result summaries for Avondale, AZ vendor-master / AP internal audit (2026-01-20).

## Item (a): delivery boundary — documented from primary sources

| Claim ID | Finding | Source and locator | Status | Limit |
|---|---|---|---|---|
| CLM-017 | One US carrier's endorsement covers social-engineering-fraud loss only if, before acting, an employee "verified the Transfer Instruction according to a pre-arranged callback or other established verification procedure", and that verification "must be recorded, logged or otherwise documented". A claim condition requires the insured to furnish a recording or other documentation of the verification. | Intact Insurance, form M350 (03-20) v1, "Social Engineering Endorsement – Call Back Provision", insuring agreement (I) and condition VIII(B)(1)(f): <https://portal.intactinsurance.com/system/files/mydocuments/M350%20%2803-20%29%20v1%20Social%20Engineering%20Endorsement%20-%20Call%20Back%20Provision.pdf> (PDF SHA-256 at access `743343332b95e66d89778834b59a40284cbd6e1b2721b0ade00474f8f4588c2d`) | verified, primary policy form | One carrier, one form, dated 2020; not a universal policy term. Shows the control and its evidence record are what coverage can turn on. |
| CLM-018 | Coverage counsel reports that some social-engineering and fraudulent-instruction policies require independent verification of changed payment instructions, sometimes by a method "other than" the one used to request the change; an email reply may not qualify. | Lowenstein Sandler, Richard F. Connors III, "Call Me, Maybe?", 2023-02-27: <https://www.lowenstein.com/news-insights/publications/client-alerts/call-me-maybe-the-stealth-disappearance-of-social-engineering-and-fraudulent-instruction-coverage-insurance> | verified as law-firm commentary | Commentary, not policy text; three years old. Corroborates CLM-017's pattern across carriers without naming them. |
| CLM-019 | A US community bank's ACH Originator Agreement requires each originating company to comply with the Nacha Operating Rules, so the 2026 fraud-monitoring duty reaches the customer through the bank agreement. | Core Bank, "Preparing for the 2026 Nacha Rule Changes": <https://corebank.com/2026-nacha-rule-changes/> (search-result summary; page not opened) | reported | Bank marketing page, not the agreement text. Allowed inference: the duty is contractual through the ODFI, not just a Nacha talking point. |

Combined with CLM-002 and CLM-003 (Nacha: risk-based process, payment-change controls as an
example, internal/bank/third-party controls allowed, outsourcing does not move responsibility), the
boundary a viewer can state on screen is:

- **The buyer owns the control.** Nacha keeps responsibility with the originator; the insurer pays
  only if the buyer's employee performed and logged the verification. The operator installs and
  tests the procedure and the log; the buyer's staff run it.
- **The operator never** holds bank credentials, releases or approves payments, confirms an account
  belongs to a payee, certifies Nacha compliance, or interprets the buyer's insurance policy.
- **The deliverable an outsider can name:** a written callback procedure using contact data held
  before the request, a different-channel rule, approval roles, and a verification log a claim
  adjuster or bank could read. CLM-017 makes the log itself the observable state change.
- **What a viewer must have a qualified reviewer confirm before selling:** engagement-letter scope
  and exclusions (attorney), professional-liability coverage for process-design advice (broker), and,
  per client, whether that client's own crime or cyber policy has a verification condition and what
  it says (the client's broker or coverage counsel, not the operator).

Item (a): **satisfied** at desk level. It is a documented boundary, not a legal review.

## Item (b): buyer-side price or spend — not found

| Accepted type | Result |
|---|---|
| Posted request with a budget | **Not found.** No freelance post for AP vendor-change or internal-control setup with a stated budget surfaced. |
| Disclosed engagement | **Not found** for the target buyer or a close small-entity proxy. Avondale, AZ commissioned an internal audit of procurement, vendor data, and AP (UHY, report dated 2026-01-20) as part of a city audit plan; no contract amount was visible, the buyer is a city, and the scope is audit, not install. Pasadena USD and Point Isabel ISD approvals were general consultant or external-audit contracts. |
| Old-way spend | **Not found** as a buyer record. Insurance premiums and bank validation fees are adjacent spend on different jobs and are not counted. |

New labelled context only (does not satisfy item b): a $49 "Vendor ACH Change Fraud Verification
Kit" is sold on Payhip (seller page via search result; no sales shown). Joins the existing
seller-price anchors (CLM-010, CLM-011, CLM-014) as context, not evidence that buyers pay.

Limit: search-engine coverage, not agenda archives or private marketplaces. Absence here is a
bounded-search result, not proof that no such spend exists.

## Item (c): viewer's first test

The four former owner field items become the viewer's plan. None is an owner task.

| Former item | Viewer's test | Success signal | Kill signal |
|---|---|---|---|
| Paid pilot | Offer one fixed-price, fixed-scope install (one workflow, one log, one drill) to ten target buyers reached through an existing bookkeeping or controller relationship. | One accepts at the stated price. | No acceptance after ten asks, or every buyer says the bank, software, or existing adviser already covers it. |
| Boundary review | Before the first sale, have an attorney review the engagement letter's exclusions and a broker quote professional liability for process-design work. | Written scope and a coverage quote that fit inside the fee. | Reviewer says the work needs a credential or license the viewer lacks, or coverage costs more than the margin of the first two engagements. |
| Delivery rehearsal | Run the install end to end on a fictional company with fictional vendors; time every step. | Done in 32 hours or less, with no real credentials or vendor data needed. | Over 32 hours, or a step cannot be done without credentials, payment authority, or real records. |
| Substitute mapping | For three target buyers, list what their bank, accounting software, bookkeeper, MSP, and insurer already provide for vendor changes. | At least two have no tested, logged callback step. | All three already have one through a bank or software feature. |

## Effect on the decision

Items (a) and (c) are complete. Item (b), the one evidence item the coaching standard keeps as
desk work, was not found after a bounded search. The research brief's central gap (CLM-016) stands:
no record shows a target buyer paying an outside operator for this job. The new insurance evidence
strengthens the problem-value case (a logged callback can decide whether a loss is covered) but is
not payment evidence. Recommended disposition: park with item (b) as the unblock condition.
