# Operator Canvas: workflow-reliability service

Status: locked for dry-run testing only

Episode: unassigned fixture

Overall evidence class: observed model

## Operator

An operations, implementation, product, RevOps, or systems generalist who can interview users, map state, reason about data and APIs, configure fit-for-purpose tools, test exceptions, document the system, and communicate with a business owner. `OBSERVED/PARALLEL`: candidate, CLM-003 through CLM-010.

The operator should refuse regulated, high-impact, or materially ambiguous workflows without qualified domain and legal review.

## Buyer and first workflow

Economic buyer: The owner or operations lead of a 10-100-person small service business using several SaaS systems. `PARALLEL`: CLM-001 through CLM-006.

First test segment: Small marketing or creative agencies reachable through the operator's existing network. `MODELED`: one example within the Step 0 permitted small-agency or professional-service starting territory.

First workflow: Signed proposal to client kickoff. `MODELED`: a bounded example connecting acceptance, intake, project creation, scheduling, billing, and internal ownership.

Beneficiaries: Staff preparing the account and the client waiting for a confident start.

## Costly problem

A proposal is accepted, but the next state is fragmented across email, CRM, intake forms, calendars, project tools, and billing. People copy data, chase missing fields, remember the next action, and discover failures only when the client asks what happens next.

The exact frequency and cost are `UNKNOWN` until measured. Institutional research supports broader administrative burden and adoption friction; it does not prove this workflow's recoverable value.

## Offer

One workflow reliability sprint covering:

- Discovery and current-state observation.
- Baseline and acceptance measures.
- State, system, access, and exception map.
- One minimum safe production workflow.
- Representative test suite.
- Logs, alerts, retry or stop behavior.
- Runbook, access inventory, training, and ownership transfer.
- Thirty days of bounded monitoring.
- Maintain, expand, redesign, or retire recommendation.

Ongoing monitoring is excluded unless incidents, response responsibility, and buyer willingness establish a separate recurring job.

## Buyer result

One named workflow moves from undocumented manual bridging to a tested and observable handoff with:

- A current-state and future-state map.
- A named owner.
- A visible log and alert path.
- Representative normal and failure tests.
- A recovery route.
- A client-controlled runbook and access record.
- Before-and-after measures agreed with the buyer.

Possible measures include manual touches, cycle time, missed handoffs, error exposure, and recovery time. No savings, revenue, or customer result is guaranteed.

## Delivery system

1. Observe the onboarding process with the people doing the work.
2. Record inputs, states, decisions, systems, credentials, exceptions, and consequences.
3. Choose the stable, high-frequency path and keep ambiguous or material decisions human.
4. Build in client-controlled accounts where practical with least-privilege access and test data.
5. Test ordinary, missing, duplicate, delayed, malformed, and downstream-unavailable cases.
6. Add logs, alerts, retry or stop behavior, and a named human exception owner.
7. Train the team, transfer documentation and access ownership, and monitor for thirty days.
8. Recommend maintain, expand, redesign, or retire based on evidence.

## Capabilities and stack

| Capability | Required job | Tool class | Human responsibility | Status |
|---|---|---|---|---|
| Process discovery | Observe actual work and ownership | Interview and mapping tools | Define reality before architecture | `PARALLEL` |
| Workflow execution | Move stable state between systems | Zapier, Make, n8n, native integration, or code | Select simplest safe fit | `OBSERVED` component capability |
| Access control | Protect credentials and data | Client accounts, secrets controls | Least privilege and revocation | `MODELED` delivery requirement |
| Testing | Exercise ordinary and failure paths | Test records and controlled data | Define acceptance and stop rules | `MODELED` service work |
| Observability | Expose state, incidents, and recovery | Logs, alerts, error workflows | Name exception owner | `OBSERVED/MODELED` |
| Handoff | Return control to client | Runbook, training, inventory | Confirm ownership and support boundary | `OBSERVED/PARALLEL` |

## Go-to-market path

1. Interview ten owners or operations leads in one reachable agency segment.
2. Require a real process walk-through, not an abstract pain interview.
3. Produce three current-state maps and reject workflows with unstable rules, high-risk judgment, inaccessible systems, or no measurable baseline.
4. Offer two bounded paid diagnostics.
5. Seek one paid reliability sprint at the predeclared modeled price and scope.
6. Track outreach, discovery, proposal, delivery, failures, support, and buyer acceptance.

Partner directories and marketplaces are secondary channels. They prove procurement paths exist, not that a new operator will convert.

## Economics

The test model assumes a $3,000 fixed sprint, two new sprints per month, and 24 delivery hours per sprint.

At two sprints, modeled gross revenue is $6,000. After $200 of software and $600 of acquisition and listed overhead, modeled cash contribution is $5,200 before owner compensation and tax.

After assigning 48 hours of operator labor at a modeled $60 allowance, economic contribution is $2,320. If each sprint takes 32 hours, it falls to $1,360.

Every commercial input is modeled. The old EP003 prices, retainers, margins, and income ranges are prohibited. This is a modeled scenario, not observed performance or an earnings forecast.

Most sensitive assumption: The buyer will pay for the full reliability job—including discovery, exceptions, documentation, and handoff—rather than software access or a quick connection.

## Risks and kill conditions

- No recurring, consequential workflow in the selected segment.
- Buyer will not authorize process observation or scoped access.
- Workflow depends on high-risk or ambiguous judgment.
- Exception volume or system condition makes fixed scope unsafe.
- New operator lacks trust, certification, security posture, or support capacity.
- Tool limits, rate changes, credits, connectors, or platform terms break the system.
- Maintenance is assumed without a real recurring response duty.
- Operator-owned infrastructure creates lock-in or unsafe credential custody.

## First 30-day test

Interview ten buyers, map three workflows, sell two bounded diagnostics, and seek one paid sprint. Continue only if buyers expose recurring consequential handoffs, authorize safe discovery, and at least one funds a bounded implementation whose measures and exceptions can be predeclared.

Stop or narrow after fifteen targeted conversations if no qualified buyer reveals a costly handoff, no buyer pays, or available workflows require unsafe access, high-risk judgment, unmanageable exceptions, or support obligations that break the capacity model.

## Dry-run Canvas verdict

Internal coherence: pass

Historical-economics rejection preserved: pass

Production lock: prohibited by fixture boundary
