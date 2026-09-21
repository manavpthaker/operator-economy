# Candidate: Vendor-payment verification install for small ACH originators

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: candidate

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-21-vendor-payment-verification`

Discovery lead: `DISC-2026-09-20-001`

Created: 2026-09-21

Owner: unassigned

Proposed evidence class: adjacent synthesis

## Opportunity in one sentence

An experienced AP or payments operator sells a fixed-scope control-install sprint to a small US
business that originates ACH payments, leaving it with a documented and tested process for vendor
onboarding and payment-detail changes without taking custody of funds or payment-release authority.

## Viewer outcome

- Viewer promise: Understand the controls, delivery boundary, substitutes, and evidence required to
  decide whether this can be a narrow operator business.
- Operator decision: Test, adapt, or reject the service based on buyer payment, provider
  qualification, delivery time, and substitution evidence.
- Practical capability: Outline a synthetic before/after payment-change workflow, a first paid-pilot
  test, and the claims that must remain excluded.
- Expected Operator Canvas: Buyer, costly job, bounded offer, control workflow, professional
  boundary, acquisition path, fixed-fee economics, and falsification threshold.

## People

- Viewer/operator: An experienced AP, bookkeeping, controllership, treasury-operations, payments, or
  cyber-risk practitioner who already understands vendor onboarding and payment-change workflows.
  This is not safe for a generic automation novice.
- Buyer: The owner or controller of a small US business that originates ACH payments to recurring
  vendors, has no dedicated treasury or fraud-operations team, and lacks a documented, tested
  payment-change process.
- End customer or beneficiary: The buyer's finance staff, bookkeeper, approver, vendors, and bank.
- Guest or outside participant required: no

## Problem

- Costly problem: Staff may act on a fraudulent or compromised vendor-onboarding or bank-detail
  change, especially when approval is based on an email that appears legitimate.
- Why it matters: One false instruction can authorize a consequential payment and leave no
  reviewable evidence that the request was independently verified.
- Why now: Nacha Phase 2 became practically effective June 22, 2026. It brings all non-consumer
  Originators, Third-Party Senders, and relevant Third-Party Service Providers into a risk-based
  fraud-monitoring obligation with annual review. Nacha names vendor and payroll payment-change
  controls as one possible implementation.
- Existing alternatives and budget: Bank dual controls and account-validation tools; an internal
  callback and dual-approval policy; a bookkeeper, CPA, fractional controller, MSP, insurer, or AP
  consultant; and vendor-verification software. The current buyer budget is unknown.

## Proposed business

- Offer: A fixed-scope vendor-payment verification and control-install sprint.
- Customer outcome: A documented and tested process for vendor onboarding and payment-detail changes,
  including trusted-contact verification, approval roles, exceptions, a change log, an incident path,
  and an annual-review checklist.
- Delivery hypothesis: Map the workflow, install risk-based procedures, create the evidence record,
  run one synthetic tabletop, and hand ownership back after a short follow-up. The operator does not
  open accounts, validate ownership as a bank would, approve or release payments, store credentials,
  promise fraud prevention, or certify legal or Nacha compliance.
- Revenue hypothesis: One fixed fee per business and defined payment workflow. A later annual review
  may be a separate project; continuous monitoring is not assumed.
- Most important unproven assumption: The buyer will pay an independent operator before a loss rather
  than treat its bank, bookkeeper, CPA, MSP, insurer, AP consultant, or software as sufficient.

## Initial synthesis hypothesis

- Parallel A: AP and procure-to-pay consulting may support the assessment, workflow-mapping,
  documentation, and fixed-project delivery components.
- Parallel B: BEC incident response and control hardening may support the attack-path review and
  combination of operational and technical boundaries.
- Parallel C: Insurer questionnaires and Nacha guidance may support recognizable control questions,
  evidence artifacts, and an annual review.
- New combination: A preventive, small-business-scale implementation of the minimum testable control
  at the point where payment instructions change, deliberately separated from payment authority,
  cybersecurity assurance, and compliance certification.
- Suspected transfer risk: The adjacent engagements are broader, post-incident, mid-market, or
  security-led. Banks and software may absorb the narrow work before an independent operator can sell
  it profitably.

These are research directions, not evidence. The completed research brief and analogy map decide
whether the transfers are valid.

## Narrative potential

- Starting state: A small finance team accepts vendor details and change requests through ordinary
  email and informal trust.
- Inciting change: A convincing impersonation arrives while a current Nacha obligation makes the
  missing process visible.
- Causal mechanism: The same channel carries both the request and the supposed confirmation, one
  person can act alone, and no trusted-contact or exception record exists.
- Operator build: A narrow verification, approval, evidence, and escalation system.
- Stakes and tradeoffs: The buyer may prevent a high-consequence error, but excessive process can
  slow legitimate payments and the operator can create liability by crossing the wrong boundary.
- End state: A synthetic change request is handled through the new control, and the viewer can decide
  whether the service merits a paid pilot.
- Visual evidence: Before/after control map, fictional vendor record, trusted-contact script,
  separation-of-duties matrix, change log, exception card, tabletop drill, and boundary map.

## Audience pull

- Exact or adjacent viewer questions: How should a small business verify vendor bank changes? What
  does Nacha Phase 2 require of a small ACH originator? Is a callback, dual approval, bank tool, or
  software enough? Can an AP operator sell the implementation?
- Initial interest signals: Two small-business discussion threads, current Nacha rule guidance,
  corporate payments-fraud survey data, government warnings, insurer-control questions, adjacent
  seller offers, and software substitutes.
- Timely tension: A live implementation duty is flexible enough to create work but also flexible
  enough for banks, software, and existing advisers to absorb it.
- Coverage gap: Public guidance explains controls; it does not establish the buyer, price, safe
  provider boundary, delivery hours, acquisition path, or contribution margin of a deliberately
  small service.
- Honest working premise: Can a qualified operator install a useful vendor-payment control without
  becoming the payment approver, cybersecurity assessor, or compliance certifier?

## Discovery and POV

- Search-volume status: not attempted in this bench; the upstream scout's conversation sources are
  qualitative, not volume evidence
- Operator Economy POV: A current research synthesis: the opportunity is not another fraud detector.
  It is installing the minimum testable finance control where a payment instruction changes, while
  preserving buyer authority and explicit recourse.
- POV evidence: Nacha's technology-neutral, risk-based requirement; its payment-change-control
  example; adjacent AP and BEC-control engagements; insurer-control questions; and software
  substitutes.
- POV boundary: No owner experience has been supplied. Do not state that the owner has implemented
  these controls, suffered this fraud, advised affected businesses, or owns a proprietary method.

## Initial evidence status

- Buyer-problem evidence: usable adjacent
- Budget or current-alternative evidence: lead found
- Offer and delivery parallel: usable
- Economics or capacity inputs: modelable
- Audience-interest signals: triangulated
- Narrative engine: strong

## Known blockers

- Independent target-buyer payment evidence is missing.
- Price, acquisition, delivery hours, and contribution margin are unverified.
- Professional qualifications, insurance, contract language, and liability boundaries are unresolved.
- The buyer segment may still be too broad.
- The service may collapse into existing AP consulting, cybersecurity work, bank controls, or
  software implementation.
- A useful assessment must avoid real credentials, payment authority, and unnecessary sensitive data.

## Intake decision

Decision: research

Reason: The current rule, material failure mode, adjacent delivery models, and showable workflow
justify formal research. They do not establish eligibility or promotion.
