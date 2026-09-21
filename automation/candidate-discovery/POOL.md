# Operator Economy candidate discovery pool

Updated: 2026-09-20 ET (run 2)

Authority: noncanonical. See `README.md`. Only the Monday research bench may admit a shortlisted
lead into formal Operator Blueprint V2 Step 0.

## Shortlisted

### 1. `DISC-2026-09-20-001` — vendor-payment verification setup for small businesses

- Status: `shortlisted`
- First seen / last checked: 2026-09-20 / 2026-09-20 ET
- Editorial priority: first. The loss is concrete, the workflow is showable, and the useful operator
  thesis is process design rather than selling another AI detector.
- Exact question or change: A small business with roughly 40 recurring vendors asked what a company
  without enterprise security staff should do when its only bank-change control is checking that an
  email looks right. A separate small-business thread asked whether owners had encountered AI voice,
  invoice, or video impersonation. The FBI's 2025 report says businesses reported more than $30
  million in BEC losses involving AI.
- Sources and observations:
  - 2026-04-10 Reddit question: <https://www.reddit.com/r/smallbusiness/comments/1shwfpm/just_learned_invoice_fraud_prevention_is_an/>
  - 2026-02-21 Reddit question: <https://www.reddit.com/r/smallbusiness/comments/1racazq/if_you_run_a_small_business_youre_a_target_for_ai/>
  - FBI IC3 BEC guidance, checked 2026-09-20: <https://www.ic3.gov/CrimeInfo/BEC>
  - FBI 2025 Internet Crime Report, published 2026: <https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf>
  - FTC small-business invoice warning, 2026-05: <https://consumer.ftc.gov/consumer-alerts/2026/05/run-small-business-pay-your-bills-not-scammers>
- Signal types: conversation, operating risk, loss, workflow, capability.
- Who appears to care / decision: owner-operators, bookkeepers, controllers, and fractional finance
  leads deciding how to verify invoices and payment-detail changes without enterprise infrastructure.
- Buyer / costly problem: a small company paying recurring vendors; one convincing impersonation or
  account-change request can move unrecoverable funds, while informal trust-based approval leaves no
  reviewable record.
- Potential offer / observable outcome: a fixed-scope vendor-payment verification install. The
  outcome is that every new vendor and bank-detail change follows a documented out-of-band check,
  approval threshold, and incident path, with evidence from a test drill.
- Delivery mechanism hypothesis: map accounts-payable handoffs; establish known-contact records;
  add callback, dual-approval, and exception rules; create a change log and escalation card; run a
  simulated request; review the first 30 days. This is control implementation, not fraud detection,
  insurance, legal advice, or a promise that loss cannot occur.
- Why now: AI makes plausible written, voice, and video impersonation cheaper, while current FBI and
  FTC guidance still relies on human verification steps that many small firms have not operationalized.
- Strongest existing answer / gap: IC3 and FTC provide sound preventive checklists. They do not show
  the bounded service, delivery hours, buyer acquisition, price, liability boundary, or whether an
  owner will pay before suffering a loss.
- Possible OE point of view: the defensible small business is not a deepfake detector. It is the
  accountable operator who installs a boring verification system, tests it, and leaves the buyer
  with recourse and a record.
- Strongest invalidating question: Will firms buy a standalone preventive engagement before a loss,
  or will their bank, accountant, cyber insurer, or accounting software provide enough of the same
  control at no additional fee?
- Evidence still needed: one buyer-paid engagement or procurement signal; comparable service pricing;
  realistic delivery hours; insurer, bank, and accounting-platform substitutes; liability and
  credential-handling boundaries; evidence that the service can be delivered without accessing funds.
- Semantic deduplication: no match in the current Step 0 candidates, EP007-EP009, parked register,
  V2 workspaces, `topics/`, `research/`, or `studio/originate/`. It shares implementation discipline
  with the workflow-reliability candidate, but the buyer trigger, loss event, control set, and outcome
  are different.
- Recheck / expiry: recheck 2026-10-18; hold if no buyer-side spend or paid-engagement evidence is
  found. Step 0 candidate ID: none.

### 2. `DISC-2026-09-20-002` — AI-use evidence pack for small EU-facing suppliers

- Status: `shortlisted`
- First seen / last checked: 2026-09-20 / 2026-09-20 ET
- Editorial priority: second. A live rule change and procurement questions create urgency, but the
  service must remain an implementation-and-evidence engagement, not an unlicensed compliance promise.
- Exact question or change: Small teams are asking how to prove responsible AI use when employees
  paste business data into general-purpose tools and when a larger customer asks for AI-governance
  evidence. EU AI-literacy and transparency duties are now active, while the Commission states that
  external training or certification is not required and the high-risk timetable is later.
- Sources and observations:
  - 2026-04-21 GDPR discussion: <https://www.reddit.com/r/gdpr/comments/1ss25un/how_are_eu_companies_actually_handling_gdpr/>
  - 2026-08-20 small-company evidence question: <https://www.reddit.com/r/AI_Governance/comments/1vtgd8o/how_do_smaller_companies_handle_eu_ai_act/>
  - 2026 Ask HN operationalization thread: <https://news.ycombinator.com/item?id=47169864>
  - European Commission AI-literacy Q&A, checked 2026-09-20: <https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers>
  - European Commission AI Act overview, checked 2026-09-20: <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai>
  - EU AI Act Service Desk on training and certification, checked 2026-09-20: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/how-can-companies-ensure-ai-competency-eg-employee-training>
  - 2026-09-03 Indie Hackers implementation example: <https://www.indiehackers.com/post/i-built-a-notion-n8n-workspace-so-smes-can-actually-comply-with-the-eu-ai-acts-article-50-tu7ZoCaFDrob7KgWlj2W>
- Signal types: conversation, regulation, procurement, workflow, adoption, buyer problem.
- Who appears to care / decision: small SaaS firms, agencies, and professional-service suppliers with
  EU customers deciding what evidence they need now, what belongs with counsel, and how to answer a
  buyer questionnaire without inventing certainty.
- Buyer / costly problem: the founder or operations lead has AI use scattered across staff and
  contractors, cannot state which data and use cases are permitted, and risks delaying a customer
  review because the evidence is fragmented or absent.
- Potential offer / observable outcome: a fixed-scope AI-use evidence-pack implementation. The
  outcome is a dated, reviewable inventory of tools and use cases, owners, permitted/prohibited data,
  required disclosures, role-specific literacy evidence, open risks, and a counsel handoff list.
- Delivery mechanism hypothesis: interview owners; inventory tools and deployment contexts; map data
  and vendors; identify applicable transparency and literacy actions from authoritative guidance;
  implement a lightweight register, policy, disclosure inventory, and evidence log; separate legal
  judgments for counsel. Do not certify compliance or classify a high-risk system without qualified review.
- Why now: enforcement powers and transparency rules became operative in August 2026, while current
  discussion shows small teams receiving questions and lacking a usable evidence trail.
- Strongest existing answer / gap: Commission guidance explains duties and many tools generate
  checklists or documents. The unresolved business question is whether a small accountable operator
  can turn scattered evidence into a useful buyer-ready system without becoming a law firm or a
  low-trust document generator.
- Possible OE point of view: the product is not fear or a certificate. It is the human work of
  discovering actual AI use, assigning decision rights, preserving evidence, and knowing which
  judgment must leave the operator's boundary.
- Strongest invalidating question: Is this durable paid work, or a short-lived deadline rush that
  cheap software, free Commission templates, and existing privacy or security advisers absorb?
- Evidence still needed: verified buyer-paid engagements; procurement questionnaires; price and
  delivery-time evidence; malpractice and legal-practice boundaries; update burden by jurisdiction;
  evidence that buyers value the pack after the deadline; competitor and substitute mapping.
- Semantic deduplication: no current candidate or episode matches the buyer, evidence-pack outcome,
  or regulatory mechanism. `research/reports/report-1-strategic-evaluation.md` names generic
  "AI compliance & security auditing" as an old idea gap, and the avatar-localization episode uses
  Article 50 only as a disclosure constraint. Neither is an intake candidate for this service.
- Recheck / expiry: recheck 2026-10-04 because official guidance and national enforcement practice
  can change quickly; hold if the service cannot be bounded away from legal advice. Step 0 candidate
  ID: none.

### 3. `DISC-2026-09-20-004` — manual accessibility remediation and evidence service

- Status: `shortlisted`
- First seen / last checked: 2026-09-20 / 2026-09-20 ET
- Editorial priority: third. The work is showable and current rules expose the limit of automated
  scans, but the buyer and qualification boundary need tighter proof before formal intake.
- Exact question or change: Small-business owners and developers are asking what meaningful website
  accessibility work to buy, what a developer should deliver, and whether automated checks are
  enough. The European Accessibility Act is active for covered services, United States public-entity
  deadlines now begin in 2027 rather than 2026, and the FTC has acted against claims that an
  automated widget can make any site compliant.
- Sources and observations:
  - 2026-08-24 small-business discussion: <https://www.reddit.com/r/smallbusinessUS/comments/1vwzygq/has_anyone_here_actually_gotten_one_of_those/>
  - 2026-02-15 developer discussion: <https://www.reddit.com/r/webdev/comments/1r50svh/is_or_should_web_accessibility_be_mandatory_2026/>
  - 2026-01-29 buyer question with a $500 budget: <https://www.reddit.com/r/webdev/comments/1qqbfyh/what_should_i_ask_a_web_developer_for_if_i_want/>
  - EU business guidance and microenterprise boundary, checked 2026-09-20: <https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/accessibility/index_en.htm>
  - FTC accessiBe final order, 2025: <https://www.ftc.gov/legal-library/browse/cases-proceedings/2223156-accessibe-inc>
  - United States Access Board testing baseline: <https://www.access-board.gov/news/2021/08/04/u-s-access-board-launches-new-site-for-the-ict-testing-baseline-for-web-accessibility/>
  - ADA.gov revised Title II timeline, checked 2026-09-20: <https://www.ada.gov/resources/web-rule-first-steps/>
  - YouTube result observed 2026-09-20: <https://www.youtube.com/watch?v=4xIJIu4UhaE>
- Signal types: conversation, regulation, procurement, workflow, capability, coverage gap.
- Who appears to care / decision: boutique web agencies and covered ecommerce or service businesses
  deciding whether to buy a scanner, a widget, code remediation, manual testing, or legal review.
- Buyer / costly problem: an agency or site owner can identify automated failures but still cannot
  verify that named customer journeys work with a keyboard and assistive technology, assign code
  fixes, or produce a reliable retest record for a client or procurement review.
- Potential offer / observable outcome: a fixed-scope accessibility remediation engagement for named
  critical flows. The outcome is a documented manual-and-automated baseline, implemented source-code
  fixes, retest evidence, known limitations, and a regression checklist—not a guarantee of legal
  compliance or immunity from claims.
- Delivery mechanism hypothesis: agree the applicable site and flows; run automated checks plus
  keyboard and screen-reader tests; reproduce and prioritize barriers; remediate source code and
  content; retest with evidence; hand off unresolved legal and specialist judgments; optionally
  provide white-label delivery to an agency.
- Why now: current rules are producing buyer questions while regulators and accessibility authorities
  make the limits of one-click automation explicit. Agencies can sell accountable remediation after
  cheap scans have commoditized issue discovery.
- Strongest existing answer / gap: accessibility specialists, agencies, platform tools, and free
  testing guidance already exist. Most current public coverage explains risk or sells scanning; it
  does not establish the economics and delivery boundary of a deliberately small, manual remediation
  service.
- Possible OE point of view: automation makes the list of suspected failures cheap. The operator
  business is the accountable human work of testing real journeys, changing the source, documenting
  the result, and refusing a false compliance guarantee.
- Strongest invalidating question: Will qualified buyers pay a small independent operator for manual
  remediation before a legal or procurement trigger, or will incumbent web agencies, accessibility
  specialists, platform vendors, and counsel absorb the work?
- Evidence still needed: buyer-paid engagements and price ranges; realistic delivery hours; repeat
  demand and regression burden; insurance, training, and legal-practice boundaries; accessibility-
  specialist substitution; a narrower initial platform or agency niche; proof that the work remains
  small-operator deliverable.
- Semantic deduplication: no matching candidate, episode, parked idea, archive, topic, research
  package, or production workspace was found. Internal WCAG checks govern OE's own visual work but do
  not propose this buyer, offer, or outcome.
- Recheck / expiry: recheck 2026-10-18; hold if buyer-paid evidence or a credible qualification path
  is still absent. Step 0 candidate ID: none.

## New

None.

## Held

### `DISC-2026-09-20-003` — agentic-commerce transaction-readiness audit

- Status: `held`
- First seen / last checked: 2026-09-20 / 2026-09-20 ET
- Exact question or change: Shopify and Google made agent-to-catalog-to-checkout infrastructure
  available in 2026, while merchants are asking how to make stores legible to shopping agents and
  whether agentic commerce is producing real results.
- Sources and observations:
  - Google UCP release, 2026-01-11: <https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/>
  - Shopify developer release, 2026-06-17: <https://www.shopify.com/news/spring-26-edition-dev>
  - Shopify operating claims, 2026-06-18: <https://www.shopify.com/blog/how-agentic-commerce-works>
  - 2026-02-27 merchant question: <https://www.reddit.com/r/ecommerce/comments/1rg50pe/has_anyone_had_success_with_agentic_commerce_yet/>
  - 2026-05-18 merchant implementation question: <https://www.reddit.com/r/EcommerceWebsite/comments/1tgsptk/how_do_i_optimize_my_ecommerce_d2c_website_for_ai/>
- Signal types: platform change, capability, adoption claim, conversation, workflow.
- Who appears to care / decision: ecommerce founders and operators deciding whether to invest in
  product-data and checkout work for a channel whose current transaction contribution is uncertain.
- Buyer / costly problem: a merchant may be discoverable yet still present stale inventory,
  ambiguous policies, unusable variants, or broken checkout paths to an agent, causing inaccurate
  recommendations or failed purchases in a channel the merchant does not control.
- Potential offer / observable outcome: a transaction-readiness audit that tests catalog, policy,
  inventory, variant, tax, payment, return, and attribution behavior through agent-compatible paths.
  The bounded outcome would be a test record and prioritized fixes, not traffic or revenue growth.
- Delivery mechanism hypothesis: inspect structured product data and feeds; test UCP or relevant
  platform paths; run controlled browse-to-checkout cases; reconcile displayed terms with source
  systems; document failures, ownership, and retest criteria.
- Why now: UCP and Shopify's self-serve developer access are material infrastructure changes, and
  Shopify reports rapid growth in AI-referred sessions and orders. Those are seller-reported platform
  figures, not independent merchant economics.
- Strongest existing answer / gap: Shopify documents enablement and Google documents the protocol.
  Current coverage does not establish who needs an independent audit, what it costs, or whether
  non-Shopify complexity supports a small operator.
- Possible OE point of view: this is potentially QA for a new transaction surface, not "AI SEO."
  The operator value would be testing what the platform says is automatic and preserving merchant
  truth, ownership, and recourse when the agent journey fails.
- Strongest invalidating question: If Shopify enables UCP and catalog distribution by default, and
  agent-originated transactions remain immaterial for most merchants, what is left that a buyer will
  pay an independent operator to do?
- Evidence still needed: merchant-side order and failure logs; a paid request or procurement signal;
  non-Shopify implementation burden; independent adoption data; service pricing; a clean boundary
  from the parked AI-visibility diagnostic.
- Semantic deduplication: materially adjacent to
  `candidate-2026-09-01-ai-visibility-diagnostic`. The proposed buyer can differ and the outcome is a
  completed, accurate transaction rather than a citation baseline, but the current public evidence
  does not yet prove that the market experiences them as separate purchases.
- Disposition / reopening condition: held until one buyer-side source shows a paid transaction-QA
  problem distinct from visibility, or a non-Shopify implementation demonstrates material delivery
  work. Recheck 2026-10-18. Step 0 candidate ID: none.

### `DISC-2026-09-20-005` — AI-agent access and kill-switch review

- Status: `held`
- First seen / last checked: 2026-09-20 / 2026-09-20 ET
- Exact question or change: Teams deploying agents through MCP and other connectors are asking what
  those agents should be able to read, which actions require approval, how permissions should expire,
  and how to revoke access after a failure. MCP authorization has hardened during 2026, and ChatGPT
  business products are exposing fuller MCP write actions and admin-vetted apps.
- Sources and observations:
  - 2026-07-30 enterprise access question: <https://www.reddit.com/r/cybersecurity/comments/1vajgxz/how_do_companies_decide_what_internal_ai_agents/>
  - 2026-09-17 MCP-control discussion: <https://www.reddit.com/r/cybersecurity/comments/1wiu316/the_3_key_enterprise_security_controls/>
  - 2026-03-10 small-business adoption question: <https://www.reddit.com/r/AiForSmallBusiness/comments/1rptg2x/anyone_actually_using_ai_agents_in_a_small/>
  - MCP 2026 release candidate: <https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/>
  - MCP enterprise-managed authorization: <https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/>
  - OpenAI MCP apps and admin controls, checked 2026-09-20: <https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt>
  - OWASP AI Agent Security Cheat Sheet, checked 2026-09-20: <https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html>
  - YouTube search snapshot, 2026-09-20: <https://www.youtube.com/results?search_query=AI+agent+permissions+MCP+security+2026>
- Signal types: conversation, capability, platform change, operating risk, workflow.
- Who appears to care / decision: small SaaS, agency, and operations teams deciding what tool-using
  agents may access, which actions can run unattended, and how to recover when an agent or connector
  behaves incorrectly.
- Buyer / costly problem: tool-using agents can inherit broad OAuth access and act on untrusted
  content, while owners lack one inventory of identities, scopes, approval points, logs, and an
  exercised revocation path.
- Potential offer / observable outcome: a fixed-scope agent-access review and control install. The
  outcome would be an agent and connector inventory, reduced scopes, explicit approval gates for
  consequential actions, logging ownership, and a tested kill-switch or revocation drill.
- Delivery mechanism hypothesis: enumerate agents, connectors, service accounts, tokens, scopes, and
  actions; map data and irreversible effects; separate read and write authority; reduce or time-box
  permissions; add human approval and logs; run a revocation and recovery exercise. No penetration
  test, security certification, or guarantee against compromise.
- Why now: agents are moving from chat to write-capable tool use while the underlying authorization
  standards and enterprise controls are still changing.
- Strongest existing answer / gap: OWASP and platform documentation describe sound controls, and
  security vendors increasingly package agent identity. Public evidence does not yet show that small
  teams buy this as a standalone operator service rather than expect an MSP, security consultant, or
  platform administrator to handle it.
- Possible OE point of view: the useful unit is not another agent demo. It is a digital worker with
  keys, decision rights, supervision, an audit trail, and an offboarding path.
- Strongest invalidating question: Is the work too security-sensitive, technically demanding, and
  liability-heavy for a small generalist operator—and is it already a feature of identity platforms,
  managed service providers, or existing security engagements?
- Evidence still needed: small or mid-market buyer-paid reviews; delivery-time and price evidence;
  required technical qualifications and insurance; common failure and recovery records; platform and
  MSP substitute mapping; proof that a safe scope is distinct from the AI-use evidence pack.
- Semantic deduplication: distinct from the AI-use evidence pack's policy and procurement artifact,
  but materially adjacent to the workflow-reliability candidate's least-privilege and revocation
  controls. No current candidate owns agent-specific permission inventory and kill-switch testing.
- Disposition / reopening condition: held until one buyer-side source shows a paid, agent-specific
  permission or revocation review that a small accountable operator can deliver within a bounded
  security scope. Recheck 2026-10-18. Step 0 candidate ID: none.

## Admitted to Step 0

None.

## Rejected index

- 2026-09-20 — Generic "AI-powered services": duplicate of the promoted AI-implementation-service
  thesis and too broad to define a buyer, outcome, or invalidating test.
- 2026-09-20 — AI-tool subscription-consolidation audit: conversation exists, but observed savings
  are small, self-service is easy, and no independent paid-service signal was found. Reopen only with
  a buyer-paid engagement tied to material spend or a recurring governance burden.
- 2026-09-20 — AI search or GEO optimization: renamed duplicate of the parked AI-visibility
  diagnostic. Reopen only through that candidate's recorded re-entry conditions.
- 2026-09-20 — Broad e-invoicing transition service: current mandates are real, but country,
  platform, tax, and deadline differences make this several businesses rather than one candidate,
  while accounting vendors can absorb setup. Reopen only as one country plus one platform with a
  buyer-paid implementation request and a non-legal delivery boundary.

Full evidence and screening: `runs/2026-09-20.md`.
