# Operator Canvas: Workflow Operations

Status: v0.2 locked for fixture simulation only after the recorded E3 failure and bounded repair

Template version: approved `operator-blueprint-v2-step1-v1.4`

Episode: unassigned fixture

Evidence class for the overall model: adjacent synthesis built on an observed professional-service category

Labels: `OBSERVED`, `PARALLEL`, `MODELED`, and `UNKNOWN` retain their Step 1 meanings.

## 1. Operator

Who can run it: An operations, implementation, product, RevOps, or systems generalist who can observe real work, model state, reason about APIs, test exceptions, document decisions, and communicate with an owner. `PARALLEL`, Step 0 CLM-003 through CLM-010.

Operator work at entry: Sell and conduct discovery, define acceptance, choose the stable path, review AI-assisted work, design failures and recovery, manage access, train the client, and own the commercial decision.

Not required: Building a new automation platform or pretending to be qualified for every regulated or high-impact workflow.

## 2. Buyer and beneficiary

Economic buyer: Owner or operations lead of a small service business using several software systems. `PARALLEL`.

Modeled first segment: Small marketing or creative agencies the operator can reach. `MODELED`.

Day-to-day users: Sales, operations, project, and finance staff carrying a new client from signature to kickoff.

Ultimate beneficiary: The client waiting for a clear start.

Purchase trigger: A repeated consequential handoff depends on manual rescue, lacks visible state or recovery ownership, and the buyer will fund observation before architecture.

Not a fit: Infrequent, unstable, judgment-heavy, inaccessible, high-impact, or consequence-free workflows.

## 3. Costly problem

Job: Move one customer-facing responsibility from one acknowledged business state to the next.

Current friction: Each application completes a local task while people copy information, chase missing fields, remember the next action, and discover failure late.

Cost: Administrative effort, slow cycle time, missed handoffs, error exposure, and customer uncertainty. Exact frequency and recoverable value remain `UNKNOWN` until measured.

Why act: The same handoff repeats, staff keeps rescuing it, and the customer or owner feels the consequence.

Alternatives: A native connection, checklist, internal process owner, general operations consultant, internal developer, or acceptance of the status quo.

## 4. Offer

Plain offer: A paid handoff diagnostic, followed only when justified by a bounded workflow-reliability sprint.

Diagnostic includes: observation, current-state map, baseline, access and exception inventory, acceptance measure, and build, narrow, defer, or no-build recommendation.

Sprint includes: stable-path implementation, representative failure tests, logs and alerts, retry or stop behavior, named recovery owner, runbook, access inventory, training, handoff, and a bounded monitoring period.

Excluded: Unlimited support, every process in the business, unsupported regulated judgment, operator-owned lock-in, and a retainer without a recurring duty.

Time to result: `MODELED`; diagnostic and sprint timing must be replaced by paid operating evidence.

## 5. Buyer result

Result purchased: One named handoff becomes visible, measurable, testable, recoverable, documented, and assigned.

Primary acceptance event: The buyer accepts the agreed state map, test record, recovery route, runbook, access record, and ownership transfer. A business-impact measure is predeclared but not guaranteed.

Possible measures: manual touches, cycle time, missed handoffs, error exposure, or recovery time. The buyer chooses the primary measure before implementation.

Operator influence boundary: The operator can improve system design and response visibility. They cannot guarantee revenue, savings, staff adoption, vendor uptime, or outcomes outside the scoped process.

## 6. Delivery system

1. Qualify the buyer and exclude unsafe or unowned work.
2. Observe the process with the people doing it.
3. Map inputs, states, decisions, systems, access, exceptions, and consequences.
4. Agree on a baseline, primary acceptance measure, completion boundary, and recovery owner.
5. Recommend build, narrow, defer, or no build.
6. For an approved build, implement the smallest stable path in client-controlled accounts where practical.
7. Test ordinary, missing, duplicate, delayed, malformed, access-revoked, and downstream-unavailable cases.
8. Add visible state, logs, alerts, retry or stop behavior, and human escalation.
9. Document, train, transfer access ownership, and monitor for the bounded period.
10. Recommend maintain, expand, redesign, transfer, or retire based on the record.

Human review owns process meaning, access, exceptions, acceptance, and recovery. Manual fallback is documented before launch.

## 7. Capabilities and stack

| Capability | Required job | Possible tool class | Human responsibility | Cost status |
|---|---|---|---|---|
| Discovery | Observe actual work | interviews and process mapping | decide what the process really is | modeled labor |
| Execution | Move stable state | native integration, workflow platform, or code | choose the safest maintainable fit | public pricing or modeled |
| AI assistance | organize notes, draft tests, compare state, prepare documents | model with an API or approved workspace | verify every output and decision | usage based |
| Observability | expose runs and failures | logs, alerts, error workflows | define what requires action | modeled |
| Access | protect and revoke credentials | client accounts and secrets controls | grant least privilege | modeled |
| Handoff | transfer control | runbook, inventory, training | confirm ownership and limits | modeled labor |

Data boundary: Client consent, minimum data, controlled testing, documented retention, revocation, and no unreviewed high-impact decision automation.

## 7A. Business-of-one design

AI compresses note organization, test drafting, state comparison, runbook preparation, and repeated reporting. Software executes stable steps and records events.

The operator retains discovery, commercial judgment, access decisions, quality, exception design, recovery, buyer communication, and accountability.

Bounded specialist help is allowed for legal, privacy, security, engineering, or domain review. A hidden support team is not.

Premature-hiring trigger: Delivery, incident response, security review, or support exceeds the owner's declared capacity and cannot be reduced through scope.

Modeled entry capacity: Two new sprints per month at twenty-four delivery hours each, plus sales, administration, and monitoring reserve. Stress case: thirty-two delivery hours each. This is the paid-validation model, not the modeled livelihood case. `MODELED`, not a promise.

Modeled mature capacity ceiling: One hundred direct service and support hours per month, forty hours reserved for sales, administration, and company work, and twenty hours of buffer inside a 160-hour owner month. Four mature client responsibilities at fourteen direct hours each use fifty-six direct hours. `MODELED`.

## 8. Go-to-market path

First segment: A reachable set of small marketing or creative agencies. `MODELED`.

Signal: Repeated manual rescue between signed proposal and acknowledged kickoff ownership.

First prospect set: Twenty-five owners or operations leads from the operator's network, local relationships, former collaborators, relevant communities, or bounded marketplace search. `MODELED`.

Modeled construction-year reachable set: Two hundred identifiable agencies inside one declared geography, relationship graph, or tightly defined service niche. This is a planning target to verify, not evidence that the buyers are reachable, qualified, willing, or likely to convert.

Credibility artifact: A plain process map, failure matrix, diagnostic decision record, and sample runbook that contain no client data.

First conversation: Ask the buyer to walk through one recent handoff as it happened. Do not begin with a tool pitch.

First paid ask: A bounded handoff diagnostic with a useful no-build result.

## 9. Entry wedge and expansion ladder

Short public title: `Workflow Operations`

Short spoken name: `workflow operations company`

Plain definition: Keeps important client work from disappearing between business tools.

Internal description: `business-reliability and outsourced workflow-operations function`

Mature promise: Own the visibility, testing, recovery, documentation, and agreed operation of a focused portfolio of consequential handoffs.

Entry wedge: One agency's signed-proposal-to-kickoff handoff, one paid diagnostic, and one bounded reliability sprint.

Scope invariant: Every responsibility has visible state, an acceptance measure, representative failures, a named recovery route, and a clear owner.

| Stage | Responsibility | Proof required | Capability added | Stop condition |
|---|---|---|---|---|
| Entry | diagnose and, if justified, build one handoff | paid diagnosis, accepted scope, observed labor | delivery record | no paid diagnosis or unsafe scope |
| Next | add an adjacent handoff | first handoff remains supportable and buyer funds the next duty | reusable controls | exception or support load breaks capacity |
| Ongoing | monitor defined incidents | real incident and response duty exists | response routine | no continuing job |
| Mature | operate a focused portfolio | repeatable delivery, acquisition, retention, capacity, and quality | portfolio operations | owner accountability becomes hidden team labor |

## 10. Economics model

Every figure is a fixture-only scenario. It is not a market rate, expected performance, or an earnings forecast. Content OS has not authorized these figures for publication.

Revenue equation: customers multiplied by fixed sprint price equals modeled gross revenue.

Direct-cost equation: owner labor plus tools plus acquisition and overhead equals modeled direct cost.

Capacity equation: available delivery hours divided by total hours per sprint equals modeled maximum active work.

| Assumption | Base | Stress | Class |
|---|---:|---:|---|
| Fixed sprint price | $3,000 | $3,000 | modeled |
| New sprints in one month | 2 | 2 | modeled |
| Delivery hours per sprint | 24 | 32 | modeled |
| Owner-labor allowance | $60 per hour | $60 per hour | modeled |
| Software allocation | $100 per sprint | $100 per sprint | modeled |
| Acquisition and overhead | $300 per client | $300 per client | modeled |

Base entry gross revenue: $6,000. Cash contribution before owner compensation and tax: $5,200. Contribution after the owner-labor allowance: $2,320. Stress contribution at thirty-two hours per sprint: $1,360.

Fixture-only owner-support target before personal tax: $6,000 per month.

The entry model misses that target by $3,680. At $1,160 contribution per sprint, it would require six monthly sprints. Six sprints require 144 delivery hours before sales, administration, monitoring, support, and recovery, so the entry model cannot be described as sustainable inside the declared two-sprint capacity.

Conditional mature model, to be tested only after the entry work proves a continuing duty:

| Assumption | Base | Stress | Class |
|---|---:|---:|---|
| Active buyers funding a defined ongoing responsibility | 4 | 4 | modeled |
| Monthly price per responsibility | $3,000 | $3,000 | modeled |
| Direct owner hours per client | 14 | 18 | modeled |
| Owner-labor allowance | $60 per hour | $60 per hour | modeled |
| Tools and vendors per client | $150 | $150 | modeled |
| Acquisition, support, and overhead per client | $350 | $350 | modeled |

Mature base gross revenue: $12,000. Owner-labor allowance: $3,360. Tools and vendors: $600. Acquisition, support, and overhead: $1,400. Modeled contribution before personal tax: $6,640.

Mature stress contribution at eighteen direct hours per client: $5,680. The stress case misses the declared owner-support target, so observed support time is a kill-sensitive input.

Most sensitive assumption: Buyers pay for the complete reliability job and delivery stays inside the bounded hours.

Modeled livelihood requirement: $6,000 per month before personal tax as a fixture planning target. This is not a statement about the owner's actual needs, a recommended income, or a public promise.

Customers required in the mature base scenario: four active buyers, each funding a real defined ongoing responsibility.

Modeled reachable buyer set: 200 identifiable agencies inside one declared geography, relationship graph, or tightly defined service niche over the construction year.

Implied active share: four divided by 200, or 2 percent.

Capacity reconciliation: Four clients at fourteen hours each require fifty-six direct hours, inside the modeled one-hundred-hour service and support ceiling. A new implementation or large incident may consume the buffer and must be scheduled or refused.

Reachability boundary: The 200-buyer set, 2-percent share, four-client count, price, retention, acquisition, and hours are all modeled. They do not establish contactability, demand, conversion, recurring purchase, or sustainable income. The operator must replace them with paid evidence and stop if observed acquisition or support cannot support four active responsibilities.

## 11. Risks and failure modes

| Risk | Early warning | Mitigation | Kill condition |
|---|---|---|---|
| no consequential handoff | buyers describe minor or rare friction | change segment or stop | no qualified process after bounded outreach |
| no paid willingness | interest but no diagnostic purchase | narrow buyer and job | no paid diagnosis after declared test |
| unsafe access | broad credentials or unclear permission requested | least privilege and qualified review | access cannot be bounded |
| unstable rules | exceptions dominate the process | keep human or redesign | stable path cannot be defined |
| hidden support | incidents and changes consume owner time | explicit duty and limits | model breaks owner capacity |
| vendor dependency | rate, connector, or term changes | fallback and ownership | workflow cannot be maintained safely |
| category overclaim | editorial label spoken as proven market | claims review | cannot explain category boundary honestly |

## 12. First construction cycle

First thirty days, modeled: Build the diagnostic artifact and delivery boundary, reach a bounded agency prospect set, observe three real handoffs, offer two paid diagnostics, and seek one funded reliability sprint.

Days thirty-one through ninety, modeled: Deliver funded work, record every hour, access task, failure, exception, tool cost, support request, and buyer acceptance decision. Offer a second responsibility only after the first record supports it.

Success: Paid buyer access, safe bounded scope, accepted delivery, and observed economics that justify another construction cycle.

Failure: No paid diagnosis, no safe workflow, delivery or support breaks capacity, or the buyer does not value the complete reliability job.

Maximum risk: Must be declared before a production candidate proceeds. The Step 0 fixture did not authorize a public or production spend.

## 13. Unknowns and contradictions

| ID | Unknown | Resolution | Blocks production lock? |
|---|---|---|---|
| U001 | whether the modeled 200-buyer set is identifiable, contactable, qualified, and sufficient to support four active clients | bounded prospect and sales test | yes for sustainability claim |
| U002 | accepted price | paid proposal | yes for market-price language |
| U003 | true delivery and support load | funded work record | yes for capacity claim |
| U004 | scorecard hash mismatch | Step 0 refresh | yes |
| U005 | Content OS eligibility of fixture numbers | facts-ledger route | yes for publication |

## E3 fixture decision

Business-model coherence: pass for simulation

Business-of-one transparency: pass for simulation

Economics and capacity: reconciled as a fixture model after rejecting the broken entry-only predecessor; owner target, four-client count, 200-buyer set, 2-percent share, price, retention, hours, and demand remain unproven planning assumptions

Decision: lock for fixture simulation only

Approved by: E2E business-model editor, not the owner

Production lock: prohibited
