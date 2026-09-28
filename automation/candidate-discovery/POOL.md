# Operator Economy candidate discovery pool

Updated: 2026-09-28 ET, owner decisions: merged owner-proposed `DISC-2026-09-28-010` from the
remote branch; owner admission recorded for `DISC-2026-09-27-009` and `DISC-2026-09-28-010`.
Earlier 2026-09-28, Monday bench: admitted `DISC-2026-09-27-011` as
`candidate-2026-09-28-records-request-overflow`; added a recheck note to `DISC-2026-09-27-012`.
Previous: 2026-09-27 ET, run 4 (scout rerun under revised rules): adds and shortlists
`DISC-2026-09-27-012` (Medicare WISeR prior-auth desk); strengthens `DISC-2026-09-27-011` with
Methacton SD and Evergreen; rejects PI medical chronologies and truck dispatch. Run 3 revised the
payment test to accept `old-way spend`. Runs 1–2: crash-report research merged; records lead added.

Authority: noncanonical. See `README.md`. Only the Monday research bench may admit a shortlisted
lead into formal Operator Blueprint V2 Step 0.

## Shortlisted

### `DISC-2026-09-27-012` — Medicare WISeR prior-auth and appeal desk for small pain and spine practices

- Status: `shortlisted` (2026-09-27 run 4; priority 2 of 2; now the only shortlisted lead)
- First seen / last checked: 2026-09-27 / 2026-09-27 ET
- Exact question or change: CMS's WISeR model (from 2026-01-01, six years) adds AI-assisted prior
  authorization to Original Medicare in Arizona, New Jersey, Ohio, Oklahoma, Texas and Washington
  for procedures including epidural steroid injections, nerve stimulators, lumbar decompression and
  skin substitutes. Records released 2026-09 show thousands of denials. Who handles the new
  paperwork for small practices?
- Sources: DLA Piper 2026-01 <https://www.dlapiper.com/en/insights/publications/2026/01/cms-wiser-model>;
  CMS FAQ <https://www.cms.gov/priorities/innovation/files/document/wiser-model-frequently-asked-questions>;
  Medicare Rights Center 2026-09-24 <https://www.medicarerights.org/medicare-watch/2026/09/24/new-records-show-medicare-wiser-ai-prior-authorization-model-causing-inappropriate-denials-of-care>;
  Stateline 2025-12-04 (title); DxTx Pain & Spine posting
  <https://painpointhealth.applytojob.com/apply/ZSBbYFRzAs/Prior-Authorization-Coordinator>; Google
  Trends 2026-09-27 ("prior authorization appeal" peaked spring–summer 2026, about a third of peak by
  September). Full ledger: `runs/2026-09-27.md`, run 4.
- Signal types: regulation (federal payment model), operating change, buyer spend, search direction.
- Who appears to care / decision: independent pain, spine and orthopaedic practices in the six
  states deciding how to staff new Medicare prior auth and appeals.
- Buyer / costly problem: procedures that needed no approval now do; denials, week-long peer-to-peer
  delays, postponed procedures and lost revenue.
- Potential offer / observable outcome: a WISeR prior-auth and first-level appeal desk; approval
  rate, days to decision and denials overturned, before and after.
- Delivery mechanism hypothesis: AI reads the chart against each service's published coverage
  criteria, flags gaps, drafts request and appeal; operator submits and tracks; physician signs and
  handles peer-to-peer.
- Why now: live since 2026-01-01; denial records just released; expansion to oncology or cardiac
  care reported (paywalled, unverified).
- **AI-change test: passes, to verify.** AI does the chart-to-criteria reading and drafting a
  $19–21/hr coordinator does by hand, so one operator can serve several practices. Needed: minutes per
  request with and without AI.
- Strongest existing answer / gap: explainers from law firms and vendors; nothing on a WISeR-specific
  small-operator desk.
- Possible OE point of view: the payer's AI denies and is paid to; the practice can answer with AI,
  but someone accountable must stand behind each submission. Showable with a synthetic chart against
  public criteria; no guest needed.
- **Delivery boundary: passes.** Unlicensed staff do prior-auth and appeal preparation today;
  clinical judgment and peer-to-peer stay with the physician; HIPAA business associate agreement
  required. Residual: an unlicensed operator prepares, submits and tracks WISeR requests and
  first-level appeals for the physician to sign.
- **Automated or productised substitute:** practice-management organisations (DxTx), billing and
  revenue-cycle companies, offshore prior-auth staffing, provider-side auth software; prices not
  collected. No free tool does the whole job.
- **Willingness-to-pay signal: `old-way spend`.** DxTx Pain & Spine, a support organisation for
  independent pain physicians, posts a remote Prior Authorization Coordinator at $19–21/hr
  (first-party careers page). No `residual` signal.
- **Switching question (bench question 1):** why would a practice move this work from its
  coordinator, billing company or offshore staff to a small operator?
- Strongest invalidating question: will offshore staffing and billing companies absorb the volume
  more cheaply, and will gold-carding or model changes remove the burden?
- Evidence still needed: approval and overturn rates by service; a practice's staff-hour cost of
  WISeR; substitute prices.
- Semantic deduplication: no match in the repository or pool.
- Bench recheck 2026-09-28 (Monday bench; status unchanged, returned to the scout for re-screening):
  (1) the DxTx/PainPoint posting URL now returns HTTP 410; the $19–21/hr wage survives only in search
  snippets and a third-party job mirror, so the lead's sole willingness-to-pay signal is no longer
  first-party accessible; (2) the House Appropriations Committee advanced language on 2026-06-09 to
  block funding for WISeR (Becker's Payer Issues headline; DelBene FY27 letter, 2026-03-27), and
  FY2027 runs on a continuing resolution to 2026-12-11 (P.L. 119-103), so the model's survival past
  that date is an open political question; (3) CMS's FAQ says WISeR plans a gold-carding exemption in
  2026 and lets providers opt for pre-payment review instead. Not admitted this run.
- Disposition: shortlisted. Decisive reason: a dated federal change with fresh public records, a
  licence-free residual, and a first-party wage for the old way. Recheck 2026-10-25; expires
  2027-01-01 unless expansion is confirmed. Step 0 candidate ID: none.

## New

None.

## Held

### `DISC-2026-09-21-007` — card acceptance cost and surcharging decision install

- Status: `held`
- First seen / last checked: 2026-09-21 / 2026-09-23 ET (2026-09-23: still preliminary approval
  only, per Payments Dive's 2026-06-09 report; no final-approval date found; KBW expects final approval
  late 2026 or early 2027 and appeals possibly into 2029. Reopening condition unchanged.)
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

### `DISC-2026-09-25-009` — manual complex-document remediation for small public entities

- Status: `held`
- First seen / last checked: 2026-09-25 / 2026-09-27 ET (2026-09-27: form-conversion re-aim tested;
  SimpliGov and CivicPlus Form Center cover it; Bluff, UT and Harvard, IL bought platform tools only,
  Bluff discussed keeping just three years of records. No outside buyer found. Still held.)
- Exact question or change: under the DOJ Title II web rule, as extended by the interim final rule at
  91 FR 20902 (2026-04-20), counties, cities, and special districts must make web content and the
  documents they post conform to WCAG 2.1 AA by 2027-04-26 (population 50,000+) or 2028-04-26 (smaller
  entities and special districts). Automated PDF remediation is now cheap; the documents it cannot fix
  — tables, fillable forms, scans — are not.
- Sources and observations (2026-09-25):
  - DOJ interim final rule, primary (already in the pool under lead 004):
    <https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web>
  - Tuscaloosa, Alabama, 2026-03-11, secondary civic summary: $37,720 over 24 months to CivicPlus Doc
    Access to convert city PDFs; automated or manual not stated:
    <https://citizenportal.ai/articles/7788570/Alabama/Tuscaloosa-County/Tuscaloosa-City/City-approves-Doc-Access-contract-to-make-municipal-PDFs-accessible-under-ADA>
  - Cole County, Missouri, 2026-03-24, two secondary civic summaries: conditional approval of CivicPlus
    remediation — $3,000 integration, about $700 per seat, five seats — plus a separately priced
    **outsourcing option for complex pages**, given as $150 per complex page in one summary and "about
    $1.50 per sheet" in the other. Price unverified:
    <https://citizenportal.ai/articles/9427399/Missouri/Cole-County/Commission-conditionally-approves-purchase-of-ADA-documentremediation-subscription-pending-contract-review>
    <https://citizenportal.ai/articles/7895862/Missouri/Cole-County/Cole-County-approves-preliminary-purchase-for-documentremediation-software-amid-staffing-concerns>
  - Fort Smith, Arkansas, 2026-04-17, about $35,000 for 600+ pages and about 6,500 documents (under
    lead 004).
  - Counter-signal: Jurupa Valley, California staff report, 2026-04-16, $74,380 over three years,
    described in the search snippet as using automated tools to avoid large-scale manual remediation
    (PDF not read):
    <https://jurupavalley.org/DocumentCenter/View/5335/26-0416-Staff-Report-CivicPlus-for-Website?bidId=>
  - Google autocomplete, 2026-09-25 (no volume inferred): "ada title ii pdf requirements", "pdf
    remediation for accessibility", "ada compliance for municipal websites", "ada compliance for city
    websites", "title ii ada website accessibility requirements".
- Signal types: regulation (dated deadline), buyer spend, substitute pricing, question signal.
- Who appears to care / decision: clerks and IT or communications staff at counties, small cities,
  and special districts deciding which posted documents to fix, archive, or remove, and whether
  platform software is enough.
- Buyer / costly problem: a small public entity with thousands of posted PDFs, no accessibility
  staff, a fixed federal date, and a software seat that handles simple documents but not the agendas,
  budgets, forms, and scanned records residents actually use.
- Potential offer / observable outcome: a fixed-scope complex-document remediation and triage
  engagement. Outcome: a document inventory classified fix / archive / remove, each fixed document
  passing a named manual check, and a before-and-after count the clerk can show.
- Delivery mechanism hypothesis: crawl and inventory posted documents; run automated remediation on
  the simple ones; manually tag tables, forms, reading order, and alt text on the rest; convert where
  HTML is better; verify with a screen reader; hand the entity a record of what was fixed and what it
  chose to archive. Whether a document falls under an exception is the entity's decision, not the
  operator's.
- Why now: the extended dates are fixed, and entities are appropriating money in 2026.
- Strongest existing answer / gap: platform vendors (CivicPlus Doc Access) and automated remediation
  (advertised from $0.30 per page) sell to the same buyer. Coverage is vendor-written; nothing
  observed addresses the leftover manual work as a small-operator business.
- Possible OE point of view: automation made the easy 80% cheap and left the hard 20% — the documents
  residents need most — to the same understaffed clerk. The operator business, if real, is that
  leftover labor.
- **Delivery boundary: passes.** No licence or credential is needed to remediate a document or test it
  with a screen reader. Residual in one sentence: an unlicensed operator manually remediates and
  verifies the posted documents automated tools fail on, and prepares the fix / archive / remove
  inventory for the entity to decide.
- **Automated or productised substitute:** automated per-page remediation (from $0.30 per page,
  vendor page) and CivicPlus Doc Access seats. The same incumbent quoting a separate outsourced price
  for complex pages indicates the residual is not what the software outputs.
- **Willingness-to-pay signal: none accepted yet.** Nearest: CivicPlus quoting Cole County a separate
  outsourced complex-page tier — but the county bought seats, the tier is an offer rather than an
  observed purchase, and the price conflicts between sources.
- **AI-change test (added 2026-09-25):** plausibly passes, not yet verified. AI remediation has made
  simple documents nearly free, and AI-assisted tagging of tables, forms and scans may let one person
  clear a town's backlog that used to need a remediation firm. Needed: hours per complex page with and
  without AI assistance.
- Owner note, 2026-09-25: the owner called this a good lead. That does not replace the
  willingness-to-pay test; it sets it as the first lead to work on the next run.
- Strongest invalidating question: do small entities keep this work inside the website vendor's
  bundle and staff seats — or archive most documents under the rule's exceptions — leaving nothing an
  outside operator is paid for?
- Evidence still needed: primary minutes or contract for one purchase of manual complex-document
  remediation by a small entity (county, city under 50,000, or special district), with scope and
  price; the rule's exception language checked against current guidance; delivery hours per complex
  page; whether CivicPlus's outsourced tier is human.
- Semantic deduplication: related to held lead `DISC-2026-09-20-004`, which recorded public-entity
  spend as a possible re-aim for the bench. Filed separately because buyer (public entity vs agency or
  ecommerce), deliverable (documents vs web journeys), and substitute differ. The bench may merge them.
  No other match in the repository.
- **Deep dive, 2026-09-25 (run 3, owner request) — lead weakened.** Full ledger in
  `runs/2026-09-25.md`, run 3. In short:
  - The main substitute, CivicPlus DocAccess, says complex pages get human review by accessibility
    specialists "at no extra cost", including scans, handwritten records and multi-column documents.
    The residual as first stated is largely what the substitute already delivers.
  - Observed towns buy the AI tool and do the rest in-house: Bellingham, WA (manual remediation of a
    sample cost over $1,100 in staff time vs $134 in DocAccess), Palm Desert, CA (6,500+ PDFs, all but
    about 300 fixed in-house), Teller County, CO (staff with CommonLook tools). Steuben County, NY
    ($29,932) and Tuscaloosa, AL ($37,720) bought DocAccess. The AI saving goes to the software vendor,
    not an outside operator.
  - Outside-service requests seen are from large buyers: League City, TX RFP #26-008 (population over
    100,000), Utah County (amounts not disclosed), Washington State DES. None is a small entity.
  - Two cracks remain. (1) DocAccess produces an HTML transcript, which the DOJ rule treats as a
    "conforming alternate version", allowed "only when there is a technical or legal limitation"
    (ADA.gov fact sheet). Whether transcripts satisfy the rule is disputed and is a legal question, not
    the scout's to decide. (2) Fillable PDF forms: a read-only transcript is not a working form
    (Bellingham alone lists 140+ online PDF forms). Converting forms into accessible web forms is a
    narrower residual that the transcript approach does not appear to cover.
- **Willingness-to-pay test (run 3): still not met.** No small entity was seen paying an independent
  provider for manual remediation.
- **Re-screen 2026-09-27 (run 3, revised payment test):** `old-way spend` exists (Bellingham: over
  $1,100 of staff time for a manual sample), but the substitute check still holds it — towns move
  that spend to DocAccess seats with human review included, not to an operator.
- Disposition / reopening condition: held. Reopen on either (a) a disclosed purchase by a small public
  entity of manual remediation or PDF-form-to-web-form conversion from a non-platform provider, or
  (b) DOJ guidance or an enforcement action saying HTML transcripts do not satisfy the rule. Next run:
  form-conversion re-aim tested 2026-09-27, no buyer found. Recheck 2026-10-18 alongside lead 004. Step 0
  candidate ID: none.

## Admitted to Step 0

### `DISC-2026-09-28-010` — admissions and enrollment analysis for small private schools

- Status: `admitted` (owner admission 2026-09-28; was `held`)
- Step 0 candidate ID: `candidate-2026-09-28-private-school-enrollment-analysis` (decision: continue
  research, then **archived by owner decision 2026-09-28** — "drop the private school"). Do not re-screen. Admission is not eligibility or promotion.
- Owner admission decision 2026-09-28: owner directed this held lead into Step 0 (see
  `operator-blueprint-v2/00-intake/OWNER-DECISION-2026-09-28-COACHING-STANDARD.md`).
- Origin: owner-proposed 2026-09-28 as "private school admissions analysis", not a scout find. The
  owner did not name the buyer. Filed on the school side (the school pays to understand its own
  admissions funnel). The family side, consultants helping parents get a child admitted, is a
  saturated consulting market with only seller price pages as evidence; reopen it separately if that
  was the intent.
- First seen / last checked: 2026-09-28 / 2026-09-28 ET
- Exact question or change: can an operator sell a small private school a fixed-scope analysis of its
  own admissions data (inquiry to application to enrollment, yield, re-enrollment, aid) that tells it
  where it loses families and what to change, now that school-choice money is changing who applies?
- Sources and observations (2026-09-28):
  - Texas Education Freedom Accounts: $1 billion first year, up to 90,000 students, up to $10,474
    per student, starting 2026-27; nearly 800 private schools registered. Fort Worth Catholic diocese
    reported 400 to 600 new students (secondary report):
    <https://www.cbsnews.com/texas/news/texas-education-freedom-accounts-private-school-growth-8-11-2026/>
    · <https://communityimpact.com/austin/south-central-austin/texas-legislature/2026/01/12/over-700-texas-private-schools-pre-k-providers-approved-for-education-savings-account-program/>
  - Federal Tax Credit Scholarship (P.L. 119-21, July 2025) starts 2027-01-01; up to $1,700 credit per
    donor; families under 300% of area median income eligible; 31 states planned to opt in as of May
    2026: <https://www.congress.gov/crs-product/R48724> ·
    <https://www.edweek.org/policy-politics/federal-program-will-bring-private-school-choice-to-at-least-4-new-states/2026/01>
  - Demand side: births fell about 16% from 2007 to 2024; a 13% private-school enrollment decline is
    projected 2024 to 2031 (search summary, source not opened). NAIS reports member enrollment stable
    since 2019 and average aid of $19,589 per aided student in 2025-26:
    <https://www.k12dive.com/news/a-snapshot-of-private-school-trends-in-4-charts/821686/>
  - Existing providers of enrollment audits: ISM, Carney Sandoe, The Gowan Group (seller pages):
    <https://www.isminc.com/consulting/onsite-consulting/admission-enrollment-management> ·
    <https://thegowangroup.com/school-consulting/enrollment>
  - Enrollment Management Association on schools' weak funnel data:
    <https://www.enrollment.org/articles/save-the-funnel-independent-schools-quest-for-better-data>
- Signal types: regulation (school-choice funding), demographic change, workflow.
- Who appears to care / decision: heads of small private and religious schools, often with one
  part-time admissions person, deciding whether to add seats, change tuition relative to the voucher
  amount, or change how they follow up with inquiries.
- Buyer / costly problem: each lost family is a year of tuition, often $10,000 or more, and most
  small schools cannot say where in the funnel families drop out or why.
- Potential offer / observable outcome: a fixed-fee funnel analysis: a cleaned multi-year dataset
  from the school's own records, conversion and yield by stage, grade and source, a re-enrollment
  risk list, a tuition-versus-voucher comparison, and three changes to test next cycle.
- Delivery mechanism hypothesis: export from the school's admissions system (Blackbaud, Finalsite,
  Veracross, or spreadsheets); AI cleans and matches records; operator builds the funnel and writes
  the findings. Family records are handled under a data agreement; nothing is shared outside the school.
- Why now: Texas money arriving in the 2026-27 year and the federal credit in 2027 bring new
  applicant groups to schools that have never had them, while the birth decline shrinks the base.
- Strongest existing answer / gap: enrollment consulting firms (ISM, Carney Sandoe, Gowan) and the
  admissions systems' own reports. The firms are priced and staffed for larger independent schools;
  the gap, if any, is small religious and micro schools newly on the voucher lists.
- Possible OE point of view: none supplied. Do not claim owner experience in school admissions.
- **Delivery boundary:** no licence is needed for data analysis. Student records may fall under
  FERPA only where a school takes federal funds; most private schools do not, but state student-privacy
  laws and the voucher programs' own rules may apply. Residual in one sentence: an operator turns a
  school's own admissions records into a funnel analysis and a short list of changes, which the
  school decides whether to make.
- **Automated or productised substitute:** reporting inside Blackbaud, Finalsite and Veracross;
  Enrollment Management Association benchmarks. Prices not published. None writes the findings for
  the school.
- **Willingness-to-pay signal: none found.** Consulting firms advertise enrollment audits, but that
  is seller copy. No school was found describing a paid engagement, and private schools do not
  publish contracts the way public bodies do.
- Strongest invalidating question: will a small school with a tight budget pay an outside operator
  for analysis when its admissions system already has reports and new voucher families are arriving
  anyway?
- Evidence still needed: one school or diocese describing a paid enrollment analysis with scope and
  price; how many Texas voucher-list schools have fewer than 200 students; what data those schools
  actually keep; the source for the 13% projection.
- Semantic deduplication: no match in candidates, queue, episodes, `studio/originate/`, `topics/`,
  `research/`, parked or rejected work, or the pool.
- Disposition / reopening condition: held on willingness to pay. Reopen when one school, diocese or
  school network is found paying an outside provider for admissions or enrollment analysis, with
  scope. Recheck 2026-10-28. Step 0 candidate ID: `candidate-2026-09-28-private-school-enrollment-analysis` (admitted 2026-09-28).

### `DISC-2026-09-27-009` — crash-report lead generation and compliant mailers for personal-injury attorneys

- Status: `admitted` (owner admission 2026-09-28; was `held`)
- Step 0 candidate ID: `candidate-2026-09-28-crash-report-mailers` (decision: continue research). Admission is not eligibility or promotion.
- Owner admission decision 2026-09-28: owner directed this held lead into Step 0 (see
  `operator-blueprint-v2/00-intake/OWNER-DECISION-2026-09-28-COACHING-STANDARD.md`).
- Origin: owner-proposed 2026-09-27, not a scout find. First filed the same day as police-report
  review for criminal defense attorneys, which was a misreading; the owner meant crash reports and
  personal-injury firms. The defense-attorney version is recorded in the rejected index.
- First seen / last checked: 2026-09-27 / 2026-09-27 ET
- Exact question or change: can an operator sell personal-injury firms a system that pulls new crash
  reports, picks the ones likely to become cases, and sends compliant letters to the people involved
  once the state's waiting period ends, faster and better targeted than the mail houses doing it now?
- Sources and observations (2026-09-27):
  - Garey v. James S. Farrin, P.C., 4th Cir. No. 21-1478, 2022-06-03: North Carolina injury firms
    got crash reports from police agencies and from private data brokers they subscribed to, then
    mailed the drivers. The court held the federal Driver's Privacy Protection Act did not apply,
    because the data did not come from the DMV. Scope: Fourth Circuit only.
    <https://law.justia.com/cases/federal/appellate-courts/ca4/21-1478/21-1478-2022-06-03.html>
  - Maracich v. Spears, 570 U.S. 48 (2013): lawyers who pulled DMV records to mail 34,000 people
    violated that Act; solicitation is not a permitted use of DMV data:
    <https://supreme.justia.com/cases/federal/us/570/48/>
  - Florida Bar v. Went For It (1995) upheld a 30-day ban on targeted mail after an accident.
    The wait is not universal: the 2026-09-27 state map found none in Pennsylvania, Illinois, Ohio,
    North Carolina, New Jersey, Virginia, Washington, Arizona or California, and New York removed
    its wait on 2026-06-01. Most states still require an advertising label. North Carolina State Bar on targeted mail:
    <https://www.ncbar.gov/for-lawyers/ethics/ethics-articles/youve-got-mail/>
  - Reflector (Greenville, NC) on access to crash reports shrinking after the litigation:
    <https://www.reflector.com/news/local/information-on-crashes-limited-as-access-to-reports-shrinks/article_9ca5eb2f-a3af-5dc5-b156-9d25e9a1eac0.html>
  - Seller-published car-accident lead prices, $200 to $400 per exclusive lead, $35 to $90 for shared
    crash-data leads (not accepted as willingness-to-pay evidence under the pool rules; context only):
    <https://www.masstortmarketingagency.com/blogs/motor-vehicle-accident-leads-guide>
  - Law-firm mail houses advertising this service:
    <https://www.mailpro.org/post/direct-mail-advertising-for-law-firms/>
    <https://directmk.com/personal-injury-attorney-direct-mail-how-to-reach-accident-victims-before-the-insurance-adjuster-do/>
- Signal types: buyer spend, workflow, regulation, litigation.
- Who appears to care / decision: small and mid-size personal-injury firms deciding how much to spend
  on crash-report mail versus search ads and bought leads.
- Buyer / costly problem: a car-accident case is worth thousands in fees, and bought leads run
  hundreds of dollars each. Mail from crash reports is cheaper per contact but untargeted: most
  reports are fender-benders with no injury, and every firm in town mails the same people on the
  same day.
- Potential offer / observable outcome: a monthly service. The firm gets a filtered list (injury
  noted, other driver at fault, commercial vehicle, inside the firm's area), letters mailed on the
  first lawful day, and a report of calls and signed cases per 1,000 letters.
- Delivery mechanism hypothesis: buy or request reports where the state allows it; AI reads each
  report and scores it for injury and fault; the attorney approves one letter template; a print
  vendor mails it; calls are tracked by number. The operator never contacts anyone by phone or in
  person and never pays for referrals.
- Why now: AI can read scanned crash-report forms cheaply, which makes scoring every report
  practical where mail houses mail everything.
- Strongest existing answer / gap: crash-data brokers and law-firm mail houses already do the pull
  and the mailing (Garey shows firms subscribing to brokers). The only visible gap is targeting:
  scoring which reports are likely cases.
- Possible OE point of view: none supplied. Do not claim owner experience in legal marketing.
- **Delivery boundary:** the attorney owns the letter, its bar compliance and every client contact.
  Data handling, scoring and mailing need no licence. Residual in one sentence: a nonlawyer operator
  obtains lawfully available crash reports, scores them for likely injury claims, and mails the
  attorney's approved letter after the waiting period.
- **Legal risk, load-bearing:** state rules decide the business. Of 24 states researched
  2026-09-27 (`runs/2026-09-27.md`), 6 are open (Ohio, New Jersey, Indiana, Missouri, Nevada,
  Massachusetts at low confidence), 9 restricted, and 9 closed, including California and
  Pennsylvania. Maryland makes it a crime for a nonlawyer to access reports to solicit, and several
  states release reports only to attorneys or on a sworn statement, so the firm must be the
  requester and the operator only processes what the firm obtains. Outside the Fourth Circuit,
  whether the Driver's Privacy Protection Act reaches crash-report data is not settled; it carries
  $2,500 statutory damages per violation.
- **Automated or productised substitute:** crash-data brokers and mail houses; published prices not
  found this run.
- **AI-change test (scout note, 2026-09-27 run 2): plausibly passes, unverified.** AI reads and scores
  scanned crash reports for injury and fault; before, mail houses mailed every report because reading
  them cost too much. Needed: scoring accuracy against signed cases.
- **Willingness-to-pay signal: found, court record.** Garey records North Carolina injury firms
  paying private data brokers for crash reports used for mailers. That shows firms pay for the data
  and mailing. No signal yet that a firm pays extra for scoring, which is the operator's only edge.
- Strongest invalidating question: if brokers and mail houses already deliver the reports and the
  letters, will a firm pay more for scoring, and does scoring raise signed cases per 1,000 letters
  enough to cover it?
- Evidence still needed: one firm's cost and signed-case rate per 1,000 crash-report letters; broker
  and mail-house prices; any post-Garey Driver's Privacy Protection Act rulings in other circuits.
  State map done for 24 states (2026-09-27).
- Semantic deduplication: no match in candidates, queue, episodes, `studio/originate/`, `topics/`,
  `research/`, parked or rejected work, or the pool.
- **Re-screen 2026-09-27 (run 3, revised payment test):** payment passes as `old-way spend` — Garey
  shows firms paying brokers for the reports that feed their mail. Switching question: would a firm
  pay a scoring operator instead of, or on top of, its broker and mail house? Still held on test 1:
  no dated operating change and no independent question signal from firms; search found only
  mail-house marketing and victim-side questions ("why do I receive letters from lawyers").
- Disposition / reopening condition: held. The state condition is met (Ohio, New Jersey, Indiana,
  Missouri and Nevada are open). Reopen when one source shows a firm's per-letter cost and
  signed-case rate, and that the firm would pay for scoring. Recheck 2026-10-27. Step 0 candidate ID: `candidate-2026-09-28-crash-report-mailers` (admitted 2026-09-28).

### `DISC-2026-09-27-011` — public-records request processing for small agencies

- Status: `admitted` (Monday bench 2026-09-28; was `shortlisted`, 2026-09-27 run 3, priority 1)
- Step 0 candidate ID: `candidate-2026-09-28-records-request-overflow` (decision: continue research;
  see `automation/runs/oe-weekly-research/2026-09-28.md`). Admission is not eligibility or promotion.
- First seen / last checked: 2026-09-27 / 2026-09-27 ET
- Exact question or change: records-request volume is rising sharply at small agencies, partly
  because AI services file requests at scale, while each agency still has one records officer and
  statutory deadlines. Who does the overflow work, and does anyone pay a non-lawyer to do it?
- Sources and observations (2026-09-27; full ledger in `runs/2026-09-27.md`, run 2):
  - Longview School District, WA, board meeting 2026-09-14 (Citizen Portal AI-written summary): 151
    requests in the first eight months of 2026 vs 53 in 2025; $96,556.58 outside legal support for
    records processing through 2026-08-31; added "a dedicated contractor" (scope and cost not
    disclosed). The district is also under a public investigation, so the surge may be event-driven:
    <https://citizenportal.ai/articles/10078311/washington/school-districts/longview-school-district/interim-superintendent-public-records-requests-nearly-tripled-and-legal-review-costs-spiked>
  - GovTech 2024-08-14: Pennsylvania counties flooded by an AI request service, adopted
    anonymous-request bans:
    <https://www.govtech.com/artificial-intelligence/governments-adjust-policies-amid-flood-of-ai-record-requests>
  - Michigan FOIA, MCL 15.234 (primary): an agency with no employee able to separate exempt material
    may use "contracted labor", capped at six times minimum wage, naming the "contracted person or
    firm" on the fee itemization: <https://legislature.mi.gov/Laws/MCL?objectName=mcl-15-234>
- Signal types: operating change (volume surge), buyer spend (outside legal), regulation (contracted
  labor provision).
- Who appears to care / decision: records officers and superintendents or clerks at school districts,
  townships and small cities deciding between overtime, counsel, software, fee and request-policy
  changes.
- Buyer / costly problem: one records officer, a tripled request load, statutory response deadlines
  with penalties (WA RCW 42.56.550), and counsel bills rising tenfold.
- Potential offer / observable outcome: overflow records processing under the agency's records
  officer. Outcome: backlog count and days-to-installment before and after, counsel hours per request.
- Delivery mechanism hypothesis: collect and de-duplicate responsive email and files, AI
  responsiveness review and first-pass redaction, installment packaging and a draft exemption log;
  the records officer and counsel approve every release and denial.
- Why now: AI-filed requests raise volume; AI review tools make one person able to process much more.
- **AI-change test: plausibly passes.** AI does the bulk reading for responsiveness and exempt content,
  which used to take paralegal or attorney hours; that is what lets one operator serve several
  agencies. Not verified: hours per request with and without AI.
- Strongest existing answer / gap: portals (GovQA, NextRequest, JustFOIA) and AI redaction or review
  software (CaseGuard, Logikcull, Polimorphic) are sold to staff; coverage is requester rights and
  agency policy. Nothing observed treats the overflow labor as a small-operator business.
- Possible OE point of view: AI made asking nearly free and left the cost on the one clerk who
  answers; who is accountable for AI-processed releases is the real question. Earned only with a
  buyer record.
- **Delivery boundary: passes, with a named line.** Exemption decisions and denials stay with the
  records officer and counsel. Residual in one sentence: an unlicensed operator gathers, de-duplicates,
  AI-reviews and pre-redacts responsive records and drafts the installment and exemption log for the
  records officer and counsel to approve. Scope out police records (CJIS); school records need a
  FERPA school-official designation.
- **Automated or productised substitute:** the portals and redaction tools above; prices not
  collected yet. They are staff tools; the residual is labor.
- **Willingness-to-pay signal: passes as `old-way spend` (re-screen 2026-09-27, run 3).** Longview
  School District reported $96,556.58 in outside legal support "for records processing" through
  2026-08-31, plus a dedicated contractor and overtime (secondary, AI-written summary of the
  2026-09-14 board meeting; bench must confirm in the primary board packet). Albuquerque added 15
  records staff to cut its backlog (Yahoo News, large city, context only):
  <https://www.yahoo.com/news/city-albuquerque-public-records-backlog-050000411.html>. No `residual`
  signal yet: Longview's contractor has no disclosed scope or price.
- **Switching question (bench question 1):** why would a records officer move overflow spend from
  counsel and overtime to an outside non-lawyer operator, rather than buying review software for its
  own staff? Longview already bought a tracking system and still paid counsel and a contractor, which
  suggests software alone did not absorb the work.
- Audience / question signal added in run 3: `site:quora.com` titles show requesters stuck on
  unresponsive agencies, e.g. "if a government agency is not responding (literally ignoring you) to a
  public records request, what's the most effective way to get their attention?"
  <https://www.quora.com/In-the-U-S-if-a-government-agency-is-not-responding-literally-ignoring-you-to-a-public-records-request-whats-the-most-effective-way-to-get-their-attention>
  (SERP title only; answers not read).
- Strongest invalidating question: do agencies absorb the surge with fees, anonymous-request bans,
  portal software and counsel, leaving no paid non-lawyer processing work — and is the surge durable
  or event-driven?
- Evidence still needed: a primary board packet, contract, or Michigan fee itemization naming a
  non-law contractor paid for records processing, with scope and rate; more small agencies reporting
  surges with numbers; substitute prices.
- Semantic deduplication: no match in the repository. Shares the small-public-entity buyer with
  `DISC-2026-09-25-009`; different deliverable and substitute.
- Run 4 additions (2026-09-27): Methacton School District, PA, 2025–26 (meeting 2026-07-22): 64
  requests; Right-to-Know specialist $70,119, assistant superintendent $24,872, legal $31,635,
  total $126,626.60, about $2,000 a request:
  <https://citizenportal.ai/articles/9813637/Pennsylvania/School-Districts/Methacton-SD/Superintendent-details-Right-to-Know-workload-and-costs-for-202526>.
  Evergreen Public Schools, WA: requests up about 52% (snippet). Lawrence, KS district ordered to pay
  $113,000 for violating the open records law (title). Longview primary packet still not found.
- Disposition: shortlisted 2026-09-27 (run 3) under the revised payment test. Decisive reason: a
  dated, costed surge at a small buyer, a licence-free residual, and AI doing the bulk of the review.
  Main risks: the only cost figure is secondary, and Longview's surge may be event-driven. Recheck
  2026-10-25. Step 0 candidate ID: `candidate-2026-09-28-records-request-overflow` (admitted
  2026-09-28).

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

- 2026-09-23 — No-tax-on-tips W-2 reporting install for small restaurants: a live, dated change (2026
  W-2s carry qualified tips in Box 12 code TP and the Treasury Tipped Occupation Code in Box 14b), but
  the residual — occupation-code mapping and separating voluntary tips from service charges — is
  substantially what payroll providers (Gusto) and a productised tool (TipCompliance, $79–$149/mo)
  already output. Reopen only with an accepted willingness-to-pay signal for a service-charge-to-tip
  pricing decision that software does not make.

- 2026-09-25 — EU PPWR obligations for non-EU small sellers: live since 2026-08-12, but the core role
  (an EU authorised representative for EPR in each member state) must be EU-established, the remaining
  packaging-data work is bundled by those representative services, and exiting the EU market is a
  self-serve alternative. Reopen only with an accepted willingness-to-pay signal for SKU packaging-data
  work bought separately from the representative.

- 2026-09-25 (run 2) — `DISC-2026-09-23-008` unknown service-line verification for small water
  systems: rejected by owner decision on the AI-change test. The business is pipe inspection and
  record-keeping; AI appeared only as photo triage, and the work would run the same without it.
  Evidence (LCRI deadline, Victoria / O'Fallon / Ladd / Arlington engagements) is preserved in
  `runs/2026-09-23.md` and `runs/2026-09-25.md`. Reopen only if AI demonstrably changes who can
  deliver it or what it costs.

- 2026-09-27 — Police-report and discovery review for criminal defense attorneys: a misreading of the
  owner's crash-report idea, researched before the correction. Police reports in pending criminal
  cases reach the defense through discovery, not public records; JusticeText ($1,200 per attorney per
  year, reported) already reads them; the only buyer rate found was Sacramento County's $25.47/hr for
  appointed-counsel paralegals. Reopen only with a private defense attorney paying an outside provider
  per case for discovery review.

- 2026-09-27 (scout run 2) — AI-drafted minutes for small public boards: the AI change is real, but
  ClerkMinutes offers free AI minutes to clerks and reports 400+ municipalities using it; the
  residual (checking the AI draft) is what the clerk now does. Towns pay only employees (part-time
  board secretaries). Reopen only with a town or district paying an outside, non-employee provider
  per meeting for verified minutes.

- 2026-09-27 (run 4) — Medical-record chronologies for personal-injury firms: old-way spend exists,
  but AI vendors (EvenUp, Eve, Supio), case software (CasePeer) and offshore firms already sell the
  job. Reopen only with a buyer showing those options fail for a named case type.

- 2026-09-27 (run 4) — Owner-operator truck dispatch: AI dispatch software already sells the job
  at a flat fee. Reopen only with evidence carriers pay a human for something that software drops.

Full evidence and screening: `runs/2026-09-20.md`, `runs/2026-09-21.md`, `runs/2026-09-23.md`,
`runs/2026-09-25.md`, `runs/2026-09-27.md`.
