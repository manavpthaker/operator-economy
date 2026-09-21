# Operator Economy candidate discovery pool

Updated: 2026-09-21 ET (candidate scout, rerun 2; re-screens both shortlisted leads against the
delivery-boundary and willingness-to-pay tests and holds both. Shortlist is empty.)

Authority: noncanonical. See `README.md`. Only the Monday research bench may admit a shortlisted
lead into formal Operator Blueprint V2 Step 0.

## Shortlisted

None. Both leads previously shortlisted were re-screened on 2026-09-21 against the
delivery-boundary and willingness-to-pay tests and moved to `held`. The Monday research bench must
record `NO_QUALIFYING_SHORTLIST` and stop.

## New

None.

## Held

### `DISC-2026-09-21-007` — card acceptance cost and surcharging decision install

- Status: `held`
- First seen / last checked: 2026-09-21 / 2026-09-21 ET
- Exact question or change: Payment-industry sources report that a revised Visa and Mastercard
  settlement received preliminary approval on 2026-06-09, describing an interchange reduction, a cap
  on standard US consumer credit interchange, and expanded merchant rights to surcharge at brand or
  product level subject to caps and a 30-day processor notice. If those terms take effect, small
  merchants face a real pricing decision they have never had to make deliberately.
- Sources and observations:
  - Official court-authorized settlement site, read 2026-09-21. It documents the Rule 23(b)(3)
    damages class and a second initial partial distribution — moved 2026-05-26, approved by the Court
    2026-06-15, payments rolling in September 2026. It does not document the injunctive-relief rules
    settlement or any surcharging change: <https://www.paymentcardsettlement.com/>
  - Payment-industry publishers, observed 2026-09-21, reporting preliminary approval on 2026-06-09
    and the surcharging and interchange terms, with one stating plainly that preliminary approval is
    not final approval:
    <https://merchantcostconsulting.com/lower-credit-card-processing-fees/visa-mastercard-settlement-update-june-2026/>
    <https://optimizedpayments.com/insights/industry-news/what-merchants-need-to-know-about-the-new-visa-mastercard-interchange-settlement/>
- Signal types: operating change, margin, pricing rights, buyer problem, litigation status.
- Who appears to care / decision: owner-operated retail, restaurant, and service businesses deciding
  whether to surcharge, dual-price, decline premium card categories, or change nothing.
- Buyer / costly problem: card acceptance is one of the largest uncontrolled line items a small
  merchant carries, the decision interacts with state law and processor rules, and the only party
  offering to help is usually the processor whose revenue the decision reduces.
- Potential offer / observable outcome: a bounded acceptance-cost review and implementation. The
  outcome would be a statement-derived effective-rate baseline, a modelled comparison of surcharge,
  dual-price, and no-change options against customer mix, the required processor notice, and the
  point-of-sale and signage changes actually made — not a promised saving.
- Delivery mechanism hypothesis: read processor statements; compute effective rate by card category;
  check applicable state and network rules; model options against the merchant's own mix; file the
  processor notice; configure the point of sale; measure the first cycle. No payment authority, no
  legal opinion, no guaranteed rate.
- Why now: reported settlement movement in June 2026 plus a distribution actually paying out in
  September 2026 puts card economics in front of owners.
- Strongest existing answer / gap: merchant-cost consultants, payment brokers, and processors already
  do this and publish most of the analysis for free as lead generation. Whether an independent
  operator with no processor residual is a distinct purchase is unproven.
- Possible OE point of view: the merchant has never controlled this cost and is advised almost
  exclusively by the party that collects it. The operator value, if any, is independence and a
  decision the owner can defend.
- Strongest invalidating question: If the rules settlement is not final, and processors and merchant-
  cost consultants already deliver the analysis free or on contingency, what is a merchant paying an
  independent operator for?
- Evidence still needed: a primary record of the injunctive-relief settlement's approval status and
  surcharging terms; one buyer-side signal of a merchant paying someone other than its processor;
  state-law and network-rule constraints by geography; customer-churn effects of surcharging;
  delivery hours and price.
- Semantic deduplication: no match anywhere in the repository or the pool. Distinct from the rejected
  AI-tool subscription-consolidation lead, which concerned software spend rather than interchange.
- Disposition / reopening condition: held until a primary record confirms the rules settlement's
  status and terms, **and** one buyer-side source shows a merchant paying an independent operator for
  the acceptance decision. Recheck 2026-11-01. Step 0 candidate ID: none.

### `DISC-2026-09-20-002` — AI-use evidence pack for small EU-facing suppliers

- Status: `held`
- First seen / last checked: 2026-09-20 / 2026-09-21 ET
- Re-screened: 2026-09-21 against the delivery-boundary and willingness-to-pay tests added that
  day. Moved from `shortlisted` to `held`. Full screening: `runs/2026-09-21.md`, run 2.
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
  can change quickly. Step 0 candidate ID: none.
- **Delivery boundary:** the residual is statable. What remains for an unlicensed operator is
  discovering which AI tools and embedded AI features staff and contractors actually use, writing
  that into a dated register with named owners and permitted or prohibited data, capturing
  role-specific literacy-training evidence, and assembling the answers to a customer's AI
  questionnaire. Legal classification of a system, any conformity determination, and contract terms
  remain with counsel or qualified review. The lead therefore does not fail on "delivery boundary
  unresolved."
- **Automated or productised substitute and published price:** Legalithm
  (<https://www.legalithm.com/en/pricing>, read 2026-09-21), an EU-built AI-Act-native self-serve
  product. Free tier provides assessment and document generators with no account required. Paid tiers
  "from€1,500/year per product" in two variants — "Your products" and "Your clients' products," the
  latter aimed at advisory firms serving several clients. Billing is not live; payment is expected to
  commence in 2027. It produces a hosted record per product covering the AI Act, CRA and EAA, lets the
  user sign a determination and hand over the proof, and cites obligations to the Official Journal.
  Applicability scoping, risk classification and the technical-documentation artifact — a large share
  of the proposed evidence pack — are what this substitute already outputs, and the advisory-firm tier
  targets the exact intermediary this lead proposes to become.
- **Willingness-to-pay signal:** **none found.** Excluded on inspection: AI-governance compliance
  software buyer's guides quoting monthly and annual tiers (vendor and comparison-site marketing); SME
  compliance guides recommending a "$5,000–$20,000" outside-counsel budget (cost-explainer content
  marketing, and it routes the money to the regulated professional rather than the residual); and
  employment listings for in-house EU AI Act compliance officers (an employer hiring staff is not the
  target buyer paying an independent provider). No buyer-described payment, budgeted service request,
  disclosed engagement, observed marketplace transaction, or incumbent charging a named buyer for the
  discovery-and-evidence residual.
- Disposition / reopening condition: held on two named conditions, both of which must be met. First,
  one accepted willingness-to-pay signal for the residual. Second, a statement of what the operator
  delivers that Legalithm's free tier does not already output. Until both are recorded the lead is not
  eligible for admission by the Monday bench.

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

### `DISC-2026-09-20-004` — manual accessibility remediation and evidence service

- Status: `held`
- First seen / last checked: 2026-09-20 / 2026-09-21 ET
- Re-screened: 2026-09-21 against the delivery-boundary and willingness-to-pay tests added that
  day. Delivery boundary passes; willingness to pay does not. Moved from `shortlisted` to `held`.
  Full screening: `runs/2026-09-21.md`, run 2.
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
- Recheck / expiry: recheck 2026-10-18. Step 0 candidate ID: none.
- **Delivery boundary: passes.** No licence or credential is required to test a website with a
  keyboard and a screen reader or to change source code, so the residual is the whole offer — manual
  keyboard and assistive-technology testing of named customer journeys, source-code fixes, and a dated
  retest record. A primary document settles the substitute question. In the United States' settlement
  agreement with Hy-Vee, Inc. (<https://www.justice.gov/crt/case-document/file/1468451/dl>, PDF read
  locally 2026-09-21), paragraph 16 requires an automated accessibility testing tool acceptable to the
  United States, run as a routine part of content development; paragraph 18 then requires that, by the
  conformance date and every 30 days thereafter, accessibility be tested "by at least one person with
  a disability who uses a screen reader for reasons related to their disability and at least one
  person with a disability who cannot use a mouse," across named real journeys, with nonconformance
  resolved within ten business days. The federal remedy does not treat the automated tool as
  sufficient. With the FTC accessiBe order, the residual is demonstrably not what an overlay or a
  scanner outputs.
- **New delivery condition recorded:** the human testing the federal remedy compels is performed by
  people with disabilities who use assistive technology. An operator who is not an assistive-technology
  user cannot personally produce that evidence and must contract or partner for it. This is a staffing
  and delivery-cost condition, not a licence, so it does not fail the boundary test — but it changes
  the shape of a deliberately small operator business and belongs in front of the bench.
- **Automated or productised substitute:** overlay widgets and automated scanners, which the FTC
  accessiBe final order and the Hy-Vee agreement's pairing of automated with human testing both show
  cannot produce the residual.
- **Willingness-to-pay signal:** **none found for the buyer this lead names.** Three near misses,
  recorded with the reason each falls short. (1) Enterprise engagements compelled by federal
  enforcement — the Hy-Vee agreement above, and DOJ's H&R Block consent decree requiring the company
  to hire an approved outside consultant for annual independent evaluations of its online
  accessibility. These are disclosed contracts naming buyers who pay independent providers for exactly
  the residual, but they are national enterprises under a government remedy, not the target buyer, and
  neither discloses a price. (2) A named small public buyer with an approved budget — on 2026-04-17 the
  Fort Smith, Arkansas City Board of Directors approved approximately $35,000 of unobligated
  general-fund money, 7–0, to address ADA digital accessibility gaps across more than 600 web pages and
  roughly 6,500 documents, covering tools to remediate existing content, live captioning and staff
  training; this is a secondary civic-meeting report rather than the minutes, the appropriation is
  tools-led rather than labor-led, and the vendor named in the discussion is the city's incumbent
  platform provider. (3) Agency pricing pages, "ADA website compliance cost 2026" explainers,
  remediation calculators and lawsuit-settlement-average posts, all excluded source types; several
  weak sources repeating a number do not become one strong source. The channel most likely to carry an
  accepted signal — a marketplace posting with a budget — was unreachable on Upwork, PeoplePerHour and
  Freelancer.com this run.
- **Timing evidence upgraded to primary:** DOJ's interim final rule at 91 FR 20902, published and
  effective 2026-04-20, extends the Title II web and mobile-app compliance date for public entities
  with a population of 50,000 or more from 2026-04-24 to 2027-04-26, and for entities under 50,000 and
  special district governments from 2027-04-26 to 2028-04-26, against WCAG 2.1 Level AA. A second
  interim final rule published 2026-05-11 extends corresponding dates for recipients of Departmental
  financial assistance. <https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web>
- **Possible re-aim, for the bench to decide, not the scout:** the only buyer-side money observed in
  this run belongs to a small public entity working to a dated federal deadline, not to the boutique
  agency or ecommerce business this lead names.
- Disposition / reopening condition: held until one accepted willingness-to-pay signal exists from the
  buyer the lead names — a marketplace posting carrying a budget, a buyer describing a payment with
  identifiable scope, or a disclosed small-business engagement for manual remediation of named flows.

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

### `DISC-2026-09-21-006` — cross-border duty and landed-cost system for small importers

- Status: `admitted`
- First seen / last checked: 2026-09-21 / 2026-09-21 ET
- Admission: admitted by the 2026-09-21 weekly research bench (rerun 2) as
  `candidate-2026-09-21-import-landed-cost-decision`. Admission is not eligibility, promotion, or
  editorial authorization. The Step 0 disposition is `parked`.
- Exact question or change: US duty-free de minimis treatment is suspended, CBP has modernised
  low-value shipment processing so that low-value parcels need an appropriate entry rather than the
  old informal path, and marketplaces are pushing the duty obligation onto sellers. Small importers
  who never needed precise classification now carry duty exposure that is a direct function of HTS
  code and country of origin, while the importer of record keeps the liability.
- Sources and observations:
  - CBP national media release, 2026-06-24, read 2026-09-21. De minimis suspended by executive order
    effective 2025-08-29; imports at or under $800 lose duty-free status; shipments valued at $2,500
    or less are subject to applicable duties; narrow gift and personal-article exceptions remain:
    <https://www.cbp.gov/newsroom/national-media-release/cbp-modernizes-low-value-shipment-processing>
  - Federal Register, published 2026-06-24, interim final rule indexed effective 2026-07-24, non-postal
    modes. Document page redirected and was not read directly:
    <https://www.federalregister.gov/documents/2026/06/24/2026-12670/indefinite-suspension-of-the-de-minimis-exemption-for-merchandise-arriving-through-all-modes-other>
  - Federal Register, published 2026-06-24, mail shipments and new postal informal entry process.
    Same access limitation:
    <https://www.federalregister.gov/documents/2026/06/24/2026-12669/indefinite-suspension-of-the-de-minimis-exemption-for-mail-shipments-and-new-postal-informal-entry>
  - Etsy Seller Handbook, article dated 2026-06-09, read 2026-09-21: "Starting July 9, 2026, DDP will
    be required for orders shipped to US buyers in order to qualify for Etsy Purchase Protection,"
    and "As of August 29, 2025, there is no longer a de minimis exemption for goods entering the
    United States": <https://www.etsy.com/seller-handbook/article/1355662653395>
  - 19 CFR Part 111 (eCFR), checked 2026-09-21. Classification and valuation are named as customs
    business; unlicensed performance exposes a person to penalties:
    <https://www.ecfr.gov/current/title-19/chapter-I/part-111>
  - Google SERP observation, 2026-09-21, r/smallbusiness thread indexed at roughly nine months old,
    "10+ comments", "16 answers", top-answer snippet "I use ChatGPT. I've never noticed an issue."
    The thread could not be opened; this is a search-result rendering, not a read thread:
    <https://www.reddit.com/r/smallbusiness/comments/1pf3w1p/small_importers_how_do_you_pick_hshts_codes_for/>
  - Google People Also Ask and related searches, observed 2026-09-21, recurring on how to find the
    correct HS/HTS code for a product. Recurrence of formulation only; no volume claim.
  - Supply-side observation, 2026-09-21: forwarders, customs technology vendors, DHL, Avalara, and
    cross-border shipping platforms are publishing merchant guidance, with at least one offering free
    HS classification advisory as an acquisition device.
- Signal types: operating change, regulation, platform change, buyer problem, workflow, margin, search
  direction.
- Who appears to care / decision: owner-operated DTC brands, marketplace sellers, and small importers
  deciding which SKUs still work, what to charge, whether to consolidate shipments, and whether the
  classification they are using can survive scrutiny.
- Buyer / costly problem: a small importer whose per-parcel entry, brokerage, and duty costs can now
  exceed the duty itself on low-value goods, whose HTS codes were approximate because everything used
  to land under the threshold, and who remains the importer of record when a code or origin claim is
  wrong.
- Potential offer / observable outcome: a fixed-scope import cost-and-data engagement. The outcome is
  a SKU-level record — classification rationale and source, supplier-supplied country-of-origin
  evidence, applicable duty treatment, and a landed-cost model per shipping mode — plus a decision
  record on which SKUs and which channels still clear margin, and a clean handoff pack for the
  licensed broker who files.
- Delivery mechanism hypothesis: inventory SKUs and suppliers; collect and file origin documentation;
  assemble classification evidence with sources and open questions; build landed cost per unit and per
  shipping mode; model consolidation against direct parcel; recompute prices and channel economics;
  hand unresolved classification determinations and all filing to a licensed customs broker. The
  operator does not file entries, does not determine another company's classification for
  compensation, and does not promise duty savings or customs outcomes.
- Why now: the suspension has been in force since 2025-08-29, CBP published modernised entry rules on
  2026-06-24, and Etsy began requiring DDP for US-bound orders on 2026-07-09. The cost is already on
  the buyer's books this quarter.
- Strongest existing answer / gap: brokers, forwarders, and customs software already classify, file,
  and calculate duty, and several give classification advisory away to win freight. Public YouTube
  coverage is beginner HS/HTS explainers, one to four years old. What no observed source establishes
  is who owns the merchant's own data and margin decision when the free advisory is wrong and the
  merchant is still the importer of record.
- Possible OE point of view: the tariff is not the interesting part. The interesting part is that a
  merchant can be told a code by a chatbot or a forwarder's free tool and still be the one who pays
  when it is wrong. The operator business, if it exists, is owning the evidence and the margin
  decision, and refusing the one determination that is not the operator's to make.
- Strongest invalidating question: Classification and valuation are named as customs business under
  19 CFR 111.1. Is there a version of this service that a small unlicensed operator can legally and
  safely deliver — and if it stops short of classification, will a buyer pay for the data, origin
  evidence, and margin model alone, when forwarders give adjacent work away free to win the freight?
- Evidence still needed: qualified review of the customs-business boundary and any licensing or
  penalty exposure; one buyer-paid engagement or purchase commitment; realistic delivery hours for a
  catalog of a stated size; price evidence; the true substitution rate against brokers, forwarders,
  and customs software; whether demand persists after the first re-pricing or is one-off; insurance
  and indemnity posture; whether a narrower first niche (one platform, one product category, one
  origin country) is required.
- Full claim registry:
  `../../operator-blueprint-v2/00-intake/02-research/candidate-2026-09-21-import-landed-cost-decision-research.md`
- Semantic deduplication: no match in current candidates, the canonical queue, promotion or
  disposition records, EP006-EP009, `studio/originate/` workspaces, parked or archived topics,
  `research/`, or the existing pool. Nearest neighbour is `DISC-2026-09-20-003` agentic-commerce
  readiness; that lead's failure event is an agent misreading a catalog and its outcome is a
  transaction test record, while this lead's failure event is a duty bill and its outcome is
  classification evidence and a landed-cost model.
- Recheck / expiry: parked. Both unblock conditions in the Step 0 disposition must be met before
  re-entry, and a negative qualified review is a reject rather than a re-park. Otherwise reviewed at
  the research refresh date of 2026-12-21. Step 0 candidate ID:
  `candidate-2026-09-21-import-landed-cost-decision`.

### `DISC-2026-09-20-001` — vendor-payment verification setup for small businesses

- Status: `admitted`
- First seen / last checked: 2026-09-20 / 2026-09-21 ET
- Admission: admitted by the 2026-09-21 weekly research bench as
  `candidate-2026-09-21-vendor-payment-verification`. Admission is not eligibility, promotion, or
  editorial authorization. The Step 0 disposition is `continue research`.
- Exact question or change: A small business with roughly 40 recurring vendors asked what a company
  without enterprise security staff should do when its bank-change control is checking that an email
  looks right. Nacha Phase 2 now requires covered non-consumer ACH Originators and related parties to
  use risk-based processes and procedures, reviewed annually, and names controls around vendor and
  payroll payment changes as one possible implementation.
- Sources and observations:
  - 2026-04-10 Reddit question: <https://www.reddit.com/r/smallbusiness/comments/1shwfpm/just_learned_invoice_fraud_prevention_is_an/>
  - 2026-02-21 Reddit question: <https://www.reddit.com/r/smallbusiness/comments/1racazq/if_you_run_a_small_business_youre_a_target_for_ai/>
  - Nacha Phase 2 rule guidance, checked 2026-09-21: <https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2>
  - Nacha implementation tips, checked 2026-09-21: <https://www.nacha.org/news/tips-originators-comply-2026-risk-management-rules>
  - AFP 2025 Payments Fraud and Control Survey release, checked 2026-09-21: <https://www.financialprofessionals.org/about/learn-more/press-releases/Details/survey-79-percent-of-organizations-were-victims-of-attempted-or-actual-payments-fraud-activity-in-2024>
  - FBI IC3 BEC guidance, checked 2026-09-20: <https://www.ic3.gov/CrimeInfo/BEC>
  - FBI 2025 Internet Crime Report, published 2026: <https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf>
  - FTC small-business invoice warning, 2026-05: <https://consumer.ftc.gov/consumer-alerts/2026/05/run-small-business-pay-your-bills-not-scammers>
  - Full claim registry:
    `../../operator-blueprint-v2/00-intake/02-research/candidate-2026-09-21-vendor-payment-verification-research.md`
- Signal types: conversation, operating risk, loss, regulation, workflow, capability.
- Who appears to care / decision: small-business owners, bookkeepers, controllers, and fractional
  finance leads deciding how to implement and evidence vendor-onboarding and bank-change controls
  without enterprise infrastructure.
- Buyer / costly problem: a covered small US business originating ACH payments to recurring vendors;
  a convincing impersonation or account-change request can move funds, while an informal approval
  leaves no reviewable control record.
- Potential offer / observable outcome: a fixed-scope vendor-payment verification install. The
  outcome is a documented and tested process for vendor onboarding and payment-detail changes,
  including verification, approval, exceptions, and an evidence record.
- Delivery mechanism hypothesis: map AP handoffs; establish trusted-contact verification; add
  separation-of-duties, dual-approval, and exception rules where appropriate; create a change log
  and escalation path; run a synthetic drill; review the first 30 days. The operator does not access
  funds, release payments, validate account ownership, certify compliance, or promise fraud prevention.
- Why now: Nacha Phase 2 became practically effective June 22, 2026 for covered non-consumer
  Originators and related parties. AI-assisted impersonation increases salience, but the rule change
  is the stronger current implementation trigger.
- Strongest existing answer / gap: Nacha, IC3, FTC, banks, insurers, and software provide controls
  and guidance. Adjacent sellers offer AP consulting and verification tools. None of the checked
  independent evidence establishes target-small-business purchases of this exact bounded service,
  safe provider qualifications, delivery hours, acquisition cost, or contribution margin.
- Possible OE point of view: the opportunity is not another detector. It is installing the minimum
  testable finance control where payment instructions change, while refusing payment authority and
  false compliance or fraud-prevention claims.
- Strongest invalidating question: Will a target buyer pay an independent operator before a loss, or
  will its bank, accountant, bookkeeper, MSP, insurer, AP consultant, or low-cost software provide
  enough of the same control with greater trust?
- Evidence still needed: one target-buyer paid pilot or equivalent purchase commitment; qualified
  payments/compliance and insurance boundary review; actual delivery hours from a synthetic
  rehearsal; and direct target-buyer mapping of bank, software, accounting, MSP, and insurer
  substitutes.
- Semantic deduplication: no semantic match in current candidates, the canonical queue, promotion
  records, EP007-EP009, parked work, archives, research, or production workspaces. The closest
  candidate is the workflow-reliability service, but it has a different buyer problem, failure
  event, mechanism, and observable outcome.
- Recheck / expiry: remain in research until the disposition's reopening evidence exists; refresh
  rule guidance, seller offers, and software alternatives by 2026-12-21. Step 0 candidate ID:
  `candidate-2026-09-21-vendor-payment-verification`.

## Rejected index

- 2026-09-20 — Generic "AI-powered services": duplicate of the promoted AI-implementation-service
  thesis and too broad to define a buyer, outcome, or invalidating test.
- 2026-09-20 — AI-tool subscription-consolidation audit: conversation exists, but observed savings
  are small, self-service is easy, and no independent paid-service signal was found. Reopen only with
  a buyer-paid engagement tied to material spend or a recurring governance burden.
- 2026-09-20 — AI search or GEO optimization: renamed duplicate of the parked AI-visibility
  diagnostic. Reopen only through that candidate's recorded re-entry conditions.
- 2026-09-21 — Employment-AI decision-record service (Colorado SB 26-189): duplicative of the AI-use
  evidence pack in buyer, mechanism, and artifact, and its obligations were postponed to 2027-01-01.
  Reopen only with a buyer-paid engagement producing a decision-explanation and reconsideration record
  that the evidence pack demonstrably does not produce.
- 2026-09-21 — HIPAA Security Rule readiness service: no live operating change. The overhaul is
  reported as unfinalised with a target around July 2027 and implied compliance around March 2028, and
  the inventory-and-evidence artifact duplicates existing leads. Reopen only when a final rule
  publishes with a dated compliance deadline and a distinct delivery boundary exists.
- 2026-09-20 — Broad e-invoicing transition service: current mandates are real, but country,
  platform, tax, and deadline differences make this several businesses rather than one candidate,
  while accounting vendors can absorb setup. Reopen only as one country plus one platform with a
  buyer-paid implementation request and a non-legal delivery boundary.

- 2026-09-21 — Subscription auto-renewal and cancellation-compliance install: no live operating
  change. The Eighth Circuit vacated the FTC Negative Option ("click-to-cancel") Rule in July 2025 and
  the FTC is back at ANPRM stage, announced 2026-03-11 with comments due 2026-04-13, so there is no
  final rule and no dated compliance deadline; California's AB 2863 took effect 2025-07-01 and is not
  a fresh trigger. No accepted willingness-to-pay signal was found for the implementation residual as
  distinct from counsel review. Reopen only when a final negative-option rule publishes with a dated
  compliance deadline **and** one accepted willingness-to-pay signal exists for the implementation
  work specifically.

Full evidence and screening: `runs/2026-09-20.md`, `runs/2026-09-21.md`.
