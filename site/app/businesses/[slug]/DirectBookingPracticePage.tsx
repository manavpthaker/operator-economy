import Link from 'next/link';
import { GuideToggle } from '../../components/GuideToggle';
import { NewsletterBand } from '../../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../../components/SiteChrome';
import { EpisodeThumbnail, WatchAction, episodeStatus } from '../../components/WatchAction';
import { AI_DISCLOSURE } from '../../lib/brand';
import { type Operation } from '../../lib/operations';

// EP009 Operator Canvas, web edition (public №002, slug direct-booking-practice).
// Source: operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/operator-canvas.md
// (owner lock 2026-09-03), with claims-map.md v0.2 for attribution and the research brief for source URLs.
// Every figure below is in content-os/facts.md "EP009 research", with its hedge in the same sentence.
// Canvas figures facts.md does not carry (hours per property, the stress case, the tools breakdown,
// the 15-hour audit threshold, the dataset size, the 40-to-80-room redesign band) are left out of this
// page on purpose. Not to be confused with EP006 (direct-booking-recovery, DirectBookingPage.tsx), which
// is archived.

const SOURCES = {
  cloudbeds: 'https://www.globenewswire.com/news-release/2026/03/25/3262232/0/en/',
  hotrec: 'https://www.hotrec.eu/en/news_digital-trends-in-accommodation-hotels-booking-com-and-dma_C2_A0_C2_A0.html',
  bookingAlias: 'https://partner.booking.com/en-gb/help/reservations/contact-extranet/contacting-your-guests',
  messaging: 'https://www.hospitalitynet.org/opinion/4134066/',
  commission: 'https://kimisuite.com/en/blog/booking-com-commissions-explained',
  freeLinks: 'https://support.google.com/hotelprices/answer/10472394?hl=en',
  engine: 'https://www.roommaster.com/blog/littlehotelier-pricing',
  agency: 'https://www.egochi.com/hotel-marketing-agency/',
  staffing: 'https://www.ahla.com/news/65-surveyed-hotels-report-staffing-shortages',
  properties: 'https://www.ahla.com/about/our-industry',
  booking10k: 'https://www.stocktitan.net/sec-filings/BKNG/10-k-booking-holdings-inc-files-annual-report-7fb6c3d1394a.html',
  expedia:
    'https://ir.expediagroup.com/news-and-events/news/news-details/2026/Expedia-Group-Reports-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx',
  parity: 'https://www.hotrec.eu/en/news_collective-action-against-booking-com-over-15-000-hotels-participating.html',
} as const;

const capabilities = [
  ['01 · Audit', 'Recommend a retainer, the audit alone, or not this property', 'Extranet and property-system reports · a booking test on a phone', 'Selling a retainer the ceiling cannot carry', 'A written recommendation, including no'],
  ['02 · Findable', 'Keep what a guest sees current and true', 'Google Business Profile · free booking links through a connectivity partner', 'Free direct placement left unconfigured', 'The direct rate beside the site rates'],
  ['03 · Bookable', 'Fix whatever stops a guest booking direct', 'The property’s own booking engine', 'A direct rate above the site, or a mobile flow that breaks', 'A commission-free way to book'],
  ['04 · Remembered', 'Set the voice and read every sensitive send', 'Consent at check-in and on wifi · a language model drafts · an automation tool schedules', 'A message sent to a masked address', 'A consented guest list that grows'],
  ['05 · Report', 'Explain the number instead of decorating it', 'Property-system reports · a spreadsheet', 'Credit or blame for what the season did', 'Direct share, monthly, against the baseline'],
] as const;

const unknowns = [
  ['U001', 'Will the owner of a 20 to 40 room property pay a retainer priced under the ceiling? The first three audits ask.', 'Safe first test'],
  ['U002', 'What do booking-site share and commission look like for US properties in this band? The figures here are worldwide or European. The audit’s own numbers replace them.', 'Carried, attributed'],
  ['U003', 'Booking.com’s base-commission band and the messaging windows rest on trade reporting. They are attributed every time they appear.', 'Carried, attributed'],
  ['U004', 'Do agencies already serve the band? Ask two agencies what their smallest retained property is.', 'Safe first test'],
  ['U005', 'What are the real audit and retainer hours? Nobody has measured them. Time the free audit.', 'Safe first test'],
  ['U006', 'How many guests consent at check-in, and do they come back direct? Only the first retainer season answers it.', 'Later-stage question'],
  ['U007', 'Cloudbeds (worldwide, vendor) and HOTREC (Europe) describe different levels of dependence. Both stay visible, each with its source.', 'Carried, attributed'],
] as const;

const included = [
  'Booking mix, commission line and cancellations by channel',
  'The ceiling, calculated on the property’s own numbers',
  'A direct-booking test as a guest, on a phone',
  'A check of whether the registration card asks for the guest’s own email',
  'Findable: Google Business Profile, free booking links, photos and offers',
  'Bookable: direct rate parity, the mobile booking flow, a missed-call fallback',
  'Remembered: consent capture, a thank-you, a review request, a seasonal return offer, a referral prompt',
  'A monthly scorecard: direct share of bookings against the audit baseline',
];

const excluded = [
  'Pricing strategy and revenue management',
  'Paid advertising or metasearch spend',
  'Any marketing to a masked booking-site address',
  'Any advice to leave the booking sites',
  'Reselling software',
  'Legal advice',
];

function SectionMark({ name }: { name: 'buyer' | 'workflow' | 'evidence' | 'economics' | 'test' }) {
  return <svg className="oe-section-mark" aria-hidden="true"><use href={`/illustration/system/icons.svg#${name}`} /></svg>;
}

function GuideNote({ step, title, children }: { step: number; title: string; children: React.ReactNode }) {
  return (
    <aside className="bl-decision-note oe-guide" aria-label={`Walkthrough, step ${step} of 5`}>
      <strong>{title}</strong>
      {children}
    </aside>
  );
}

function Source({ href, children }: { href: string; children: React.ReactNode }) {
  return <a href={href} target="_blank" rel="noreferrer">{children}<span className="oe-sr"> (opens in new tab)</span></a>;
}

export function DirectBookingPracticePage({ operation }: { operation: Operation }) {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="businesses" />
      <main id="main">
        <section className="bl-opening bl-shell" aria-labelledby="business-title">
          <div className="oe-hero">
            <div className="bl-episode-feature__intro">
              <p className="bl-chapter__number">Operator Canvas</p>
              <h1 id="business-title">{operation.name}</h1>
              <p>It helps a small hotel get its returning guests to book direct, instead of paying a booking site to meet them again. One operator, a fixed-fee audit first, then a flat monthly retainer priced under what the property could recover.</p>
              <p className="oe-page-note">
                Built from the episode&apos;s locked Operator Canvas. Scope: findable, bookable, remembered. It never tells a property to leave the booking sites and never markets to a masked guest address.{' '}
                <Link className="bl-text-link" href="/method">How the Canvas works</Link>
              </p>
            </div>
          </div>

          <article className="oe-operation-sheet oe-operation-sheet--episode" aria-labelledby="docket-title">
            <aside className="bl-docket">
              <div className="bl-docket__head"><span>Operator Canvas · locked</span><span>{episodeStatus(operation.slug)}</span></div>
              <div className="bl-docket__body">
                <span className="bl-docket__identity">{operation.audience}</span>
                <h2 id="docket-title">{operation.question}</h2>
                <p>Judge the problem, the work, the arithmetic, and the test that should come before any bigger claim.</p>
              </div>
              <dl className="bl-docket__rows">
                <div className="bl-docket__row"><dt>Buyer</dt><dd>Owner-run, roughly 20 to 40 rooms</dd></div>
                <div className="bl-docket__row"><dt>Entry offer</dt><dd>One fixed-fee audit</dd></div>
                <div className="bl-docket__row"><dt>First test</dt><dd>Three audits, one of them unpaid</dd></div>
              </dl>
            </aside>
            <figure className="oe-episode-art">
              <EpisodeThumbnail
                slug={operation.slug}
                thumbnail={operation.thumbnail!}
                sizes="(max-width: 900px) calc(100vw - 3rem), (max-width: 1600px) 62vw, 58rem"
                priority
              />
              <figcaption><span>Episode thumbnail. Everyone pictured is AI-generated.</span><span>{operation.published}</span></figcaption>
            </figure>
          </article>
        </section>

        <section className="oe-value oe-band-raised bl-shell" id="summary" aria-labelledby="summary-title">
          <div className="oe-value__intro">
            <p className="bl-chapter__number">Start here</p>
            <h2 id="summary-title">The case in three decisions.</h2>
            <p>Read these first. The sheets below hold the evidence, the assumptions, the arithmetic and the stop conditions behind each answer.</p>
          </div>
          <ol className="oe-decision-list" aria-label="Decision summary">
            <li><span>01</span><div><strong>Is the problem worth solving?</strong><p>Most of a small hotel&apos;s reservations arrive through booking sites with a commission attached, and the site hides the guest&apos;s email behind an alias. So the property pays again to meet its own regulars. Cloudbeds, which sells hotel software, reports that 63.4% of independent-hotel bookings went through the sites in 2025, worldwide. Read it as a vendor&apos;s view, not a US figure.</p><span className="oe-class"><Link href="/method#evidence-classes">Reported premise · vendor, worldwide</Link></span></div></li>
            <li><span>02</span><div><strong>Can one operator deliver it?</strong><p>A language model drafts the post-stay messages and an automation tool schedules them. The voice, the offer, consent and who receives a message stay with the operator. In the model, a practice built on six 20-room properties is a foothold, not a living.</p><span className="oe-class"><Link href="/method#evidence-classes">Modeled offer · thin at 20 rooms</Link></span></div></li>
            <li><span>03</span><div><strong>What should I test first?</strong><p>Build the audit and run it on three properties you can visit, one of them unpaid. Put a retainer priced under each property&apos;s own ceiling in front of its owner. Stop if no owner in the band will fund the modeled $600 a month.</p><span className="oe-class"><Link href="/method#evidence-classes">Modeled test · unknown result</Link></span></div></li>
          </ol>
          <div className="oe-actions" style={{ alignItems: 'center' }}>
            <a className="bl-action" href="#sheet-00">Explore the Canvas</a>
            <GuideToggle />
          </div>
        </section>

        <nav className="bl-anchor-nav bl-shell" aria-label="Canvas sections">
          <a href="#sheet-00">00 · Opportunity</a><a href="#sheet-01">01 · System</a><a href="#sheet-02">02 · Evidence</a><a href="#sheet-03">03 · Economics</a><a href="#sheet-04">04 · Guardrails</a><a href="#download">05 · Download</a>
        </nav>

        <div id="working-paper-shell">
          <section className="bl-chapter bl-shell" id="sheet-00" aria-labelledby="h-00">
            <header className="bl-chapter__head"><p className="bl-chapter__number">00 / Opportunity</p><div><SectionMark name="buyer" /><h2 id="h-00">Is the problem worth solving?</h2><p>The site keeps the guest&apos;s contact and the front desk has no time to build a list. So the property pays the same introduction fee for the same guest&apos;s next stay. Keeping that guest is the job.</p></div></header>
            <GuideNote step={1} title="Start with who holds the guest's address."><p>Notice that the booking site keeps the guest&apos;s contact and asks the hotel to stay on its platform. Then ask what it costs the property to meet the same guest again, and who is paid to fix that.</p></GuideNote>
            <div className="bl-split">
              <div className="bl-prose">
                <h3>Who buys</h3>
                <p>The owner of a US independent property of roughly 20 to 40 rooms, with no marketing or revenue hire, most bookings coming through the sites, and no consented guest list. The American Hotel and Lodging Association counts more than 33,200 small-business lodging properties. Nobody has counted how many sit in this band.</p>
                <h3>Who does not</h3>
                <p>A property under roughly 20 rooms. One on base commission with a low share through the sites, where the model recovers only a few hundred a month. One already retaining an agency, one that is chain affiliated, or an owner who will not grant access to the extranet, the property system and the front desk.</p>
                <h3>What the owner receives</h3>
                <p>A documented baseline, a tested and fixed direct path, a consented guest list that grows every month, and one number reported monthly: direct share of bookings against the audit baseline. The operator can influence whether that number moves. The operator cannot promise it.</p>
              </div>
              <ul className="bl-rule-list" aria-label="Entry wedge and expansion">
                <li><strong>Entry wedge.</strong> One fixed-fee audit for one property.</li>
                <li><strong>Proof before expansion.</strong> One paid audit, and one owner&apos;s yes to a retainer under the ceiling.</li>
                <li><strong>Aspirational destination.</strong> A handful of properties, growing up the band as audits show where the ceiling clears the operator&apos;s time.</li>
                <li><strong>Scope that must hold at every stage.</strong> Priced under the property&apos;s own ceiling. Guest data used only with consent and inside the sites&apos; rules. Never told to leave the sites.</li>
              </ul>
            </div>
            <div className="oe-scope" aria-label="Scope">
              <div><h3>Included</h3><ul>{included.map((item) => <li key={item}>{item}</li>)}</ul></div>
              <div className="oe-scope__out"><h3>Never included</h3><ul>{excluded.map((item) => <li key={item}>{item}</li>)}</ul></div>
            </div>
            <aside className="bl-disclosure"><strong>Scope boundary</strong><span>The practice works inside the property&apos;s own accounts and inside the booking sites&apos; rules. It does not set prices, run ads or sell software. When the audit finds a property on base commission with a low share through the sites, the honest recommendation is the audit alone, or not this property.</span></aside>
          </section>

          <section className="bl-chapter bl-shell" id="sheet-01" aria-labelledby="h-01">
            <header className="bl-chapter__head"><p className="bl-chapter__number">01 / System</p><div><SectionMark name="workflow" /><h2 id="h-01">What must one operator run?</h2><p>The audit comes first, and it can say no. The retainer covers three jobs: findable, bookable, remembered. One number reports whether it is working.</p></div></header>
            <GuideNote step={2} title="Where does AI help, and where does it not?"><p>A language model drafts the thank-you, the review request, the seasonal offer and the referral prompt in the property&apos;s voice, and an automation tool schedules them off checkout dates. The drafting got cheap. The voice, the offer, consent and who receives a message did not.</p></GuideNote>
            <div aria-label="Capabilities">
              {capabilities.map(([name, judgment, implementation, failure, result]) => (
                <div className="bl-ledger-row" key={name}>
                  <span className="bl-ledger-row__name">{name}</span>
                  <dl className="oe-facts"><div><dt>Human judgment</dt><dd>{judgment}</dd></div><div><dt>Implementation</dt><dd>{implementation}</dd></div><div><dt>Failure mode</dt><dd>{failure}</dd></div></dl>
                  <span className="bl-ledger-row__value">{result}</span>
                </div>
              ))}
            </div>
            <aside className="bl-decision-note" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Routed out, every time</strong><p>Anything touching rate-parity contract terms, consumer law on rate display, or European guest data beyond consent-first handling goes to the owner&apos;s own counsel. The property owns every account, every list and every message template, and access ends the moment the owner asks.</p></aside>
          </section>

          <section className="bl-chapter oe-band-inset bl-shell" id="sheet-02" aria-labelledby="h-02">
            <header className="bl-chapter__head"><p className="bl-chapter__number">02 / Evidence</p><div><SectionMark name="evidence" /><h2 id="h-02">What do we know, and what remains uncertain?</h2><p>Much of the evidence comes from companies that sell to hotels, and much of it is European. Each receipt says who published it and where it applies.</p></div></header>
            <GuideNote step={3} title="Read the hedge before the number."><p>Check who published each figure and where it applies. None of it shows that an owner in this band will pay, or that the service moves direct share.</p></GuideNote>
            <div style={{ display: 'grid', gap: 'var(--bl-space-4)' }} aria-label="Evidence receipts">
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.cloudbeds}>Cloudbeds, 2026 State of Independent Hotels</Source></span><p>Cloudbeds reports that <strong>63.4%</strong> of independent-hotel bookings went through the booking sites in 2025, worldwide. In the same Cloudbeds data, site bookings were cancelled at <strong>21.8%</strong> against <strong>10.6%</strong> for direct. Cloudbeds sells hotel software and reports on its own customers. Neither figure is a US figure or a figure for this band.</p><span className="bl-evidence-receipt__count">vendor · worldwide</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Verified for Europe · <Source href={SOURCES.hotrec}>HOTREC</Source></span><p>HOTREC, the European hotel association, found direct channels still carried <strong>50.9%</strong> of European overnight stays in 2023. Europe only, all property sizes. It sits beside the Cloudbeds figure and is never blended with it.</p><span className="bl-evidence-receipt__count">Europe</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Verified at source · <Source href={SOURCES.bookingAlias}>Booking.com partner help</Source></span><p>Booking.com&apos;s own partner help says it does not share private email addresses. Both sides see an alias ending <strong>@guest.booking.com</strong>, and partners are asked to keep the conversation on the platform.</p><span className="bl-evidence-receipt__count">primary</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.messaging}>the trade press, Hospitality Net</Source></span><p>The trade press puts Booking.com&apos;s messaging window at about <strong>seven days</strong> after checkout, and Expedia&apos;s at about <strong>45 days</strong>. Reported durations, not figures either site publishes as its own.</p><span className="bl-evidence-receipt__count">secondary</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.commission}>trade reporting on Booking.com commission</Source></span><p>Trade reporting puts base commission around <strong>15%</strong> in most European markets. The Preferred badge adds about <strong>3 points</strong>, and Genius is a <strong>10 to 20%</strong> guest discount the hotel funds. Booking.com publishes no base rate of its own.</p><span className="bl-evidence-receipt__count">secondary</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Verified · <Source href={SOURCES.freeLinks}>Google Hotel Center help</Source></span><p>Google shows a free booking link beside the site rates for a property connected through Hotel Center or an integration partner, and charges <strong>no fee</strong> for it. The connection is the step the operator sets up.</p><span className="bl-evidence-receipt__count">primary</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Public pricing · <Source href={SOURCES.engine}>Little Hotelier pricing, via Roommaster</Source></span><p>One small-property booking engine is listed at about <strong>$29 to $39 a month plus 1%</strong>, or about <strong>$109</strong> a month flat. Public tool pricing as reported at research time. Check the vendor&apos;s own page before relying on it.</p><span className="bl-evidence-receipt__count">public pricing</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Self-published · <Source href={SOURCES.agency}>one hotel marketing agency</Source></span><p>One agency publishes its entry price, <strong>$1,500 a month</strong>, for independents, inns and small resorts. That is its own price. It is not evidence that agencies serve this band, or of what any agency achieves.</p><span className="bl-evidence-receipt__count">own price</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Verified · <Source href={SOURCES.staffing}>American Hotel and Lodging Association</Source></span><p><strong>65%</strong> of the <strong>282</strong> hotels the association surveyed reported staffing shortages. A member survey, not specific to small properties. It explains why the desk has no time to build a list.</p><span className="bl-evidence-receipt__count">survey</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Verified · <Source href={SOURCES.booking10k}>Booking Holdings</Source> and <Source href={SOURCES.expedia}>Expedia Group</Source> filings</span><p>By their own filings, Booking Holdings ran <strong>$186.1 billion</strong> and Expedia <strong>$119.6 billion</strong> of gross bookings in 2025, blended across everything they sell. Worldwide, not hotel commission, not US figures, and not to be added together. Size is not the constraint here.</p><span className="bl-evidence-receipt__count">filings</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Verified · <Source href={SOURCES.parity}>HOTREC</Source></span><p>In Europe, more than <strong>15,000</strong> hotels registered for a collective damages action against Booking.com over price parity clauses. That is Europe, not here, and registering is not proof of damages.</p><span className="bl-evidence-receipt__count">Europe</span></aside>
            </div>
            <aside className="bl-disclosure" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Excluded on purpose</strong><span>Vendors&apos; claims about what direct-booking tools do to revenue are not used here in any form. Outsourced revenue managers mostly quote privately, so no revenue-management price or result appears either. And nobody has built this practice and published what it earns.</span></aside>
            <div style={{ marginTop: 'var(--bl-space-7)' }} aria-label="Unknown register">
              <p className="bl-chapter__number" style={{ marginBottom: 'var(--bl-space-3)' }}>Unknown register · open questions carried, not hidden</p>
              {unknowns.map(([id, statement, classification]) => <div className="bl-ledger-row" key={id}><span className="bl-ledger-row__name">{id}</span><p>{statement}</p><span className="oe-class">Unknown · {classification}</span></div>)}
            </div>
          </section>

          <section className="bl-chapter bl-shell" id="sheet-03" aria-labelledby="h-03">
            <header className="bl-chapter__head"><p className="bl-chapter__number">03 / Economics</p><div><SectionMark name="economics" /><h2 id="h-03">Could the economics work?</h2><p>Modeled scenario, not observed performance or an earnings forecast. Every figure in this section is arithmetic on an illustrative inn, shown so you can replace the inputs with a real property&apos;s. The bottom of the band is shown as thin because it is.</p></div></header>
            <GuideNote step={4} title="Find the number nobody has measured."><p>Follow the ceiling back to the ten-point shift from the sites to direct. It is a hypothesis nobody has measured, and everything on the buyer&apos;s side rests on it.</p></GuideNote>
            <div className="oe-three" aria-label="Three views, never blended">
              <article><span className="oe-class">Modeled · the property&apos;s ceiling</span><h3>$996 to $1,418</h3><p>A month, in the model: what an illustrative 20-room inn could recover if a ten-point shift to direct happened, a shift nobody has measured. It is the ceiling the fee must sit under, not commission the service saves.</p><dl><div><dt>Illustrative inn</dt><dd>20 rooms · $180 a night · 70% occupied</dd></div><div><dt>Room revenue, modeled</dt><dd>about $919,800 a year</dd></div><div><dt>Through the sites, at 63.4%</dt><dd>about $583,153</dd></div></dl></article>
              <article><span className="oe-class">Modeled · the arithmetic</span><h3>$16,556 to $20,236</h3><p>A year of commission saved in the model, if that unmeasured ten-point shift moved about $91,980 of revenue to direct at 18 to 22% all-in commission. Less a direct cost of 3.5 to 5%, the low end being one vendor&apos;s own figure, it nets about $11,957 to $17,017 a year in the model.</p><dl><div><dt>Commission, modeled</dt><dd>about $104,968 to $128,294 a year</dd></div><div><dt>A five-point shift</dt><dd>halves it: $498 to $709 a month</dd></div><div><dt>A 40-room property</dt><dd>doubles it: $1,993 to $2,836 a month</dd></div></dl></article>
              <article><span className="oe-class">Modeled · the operator</span><h3>about $20,000</h3><p>Left in the model at the bottom of the band, after pricing the operator&apos;s time at an imputed $60 an hour. A foothold, not a living, and the Canvas does not adjust the inputs until it passes.</p><dl><div><dt>Audit, modeled</dt><dd>$1,200, about 12 hours</dd></div><div><dt>Retainer, modeled</dt><dd>$600 at 20 rooms to $1,000 to $1,250 at 40 · $800 blended</dd></div><div><dt>Six properties, modeled gross</dt><dd>$64,800</dd></div><div><dt>Tools and overhead, modeled</dt><dd>about $6,000</dd></div><div><dt>Before owner pay and tax</dt><dd>$58,800</dd></div></dl></article>
            </div>
            <aside className="bl-decision-note" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Most sensitive assumption</strong><p>Whether an owner in the band pays at all, then delivery hours per property. Nobody has measured either. In the model, six 20-room properties at $600 a month is $43,200 a year of retainer, and six 40-room properties at $1,250 is $90,000 a year of retainer before costs. Neither is a forecast, and neither says a 40-room owner will pay.</p></aside>
            <aside className="bl-disclosure"><strong>Economics boundary</strong><span>Modeled scenario, not observed performance or an earnings forecast. No operator has published what this practice earns. The audit fee and retainers are assumptions set under each property&apos;s ceiling, not market rates or typical prices.</span></aside>
          </section>

          <section className="bl-chapter oe-band-raised oe-active-chapter bl-shell" id="sheet-04" aria-labelledby="h-04">
            <header className="bl-chapter__head"><p className="bl-chapter__number">04 / Guardrails</p><div><SectionMark name="test" /><h2 id="h-04">What should you test first?</h2><p>The first move is the audit, sold as a product. It returns the ceiling, what breaks on the direct path, and a recommendation that is allowed to be no.</p></div></header>
            <GuideNote step={5} title="What can you learn before you sell anything?"><p>Run the audit unpaid for an owner you already know, and time it. Ask two agencies what their smallest retained property is. If they already serve the band at prices owners prefer, that is the answer.</p></GuideNote>
            <div className="bl-split">
              <div className="bl-anatomy"><h3>The first 30 days</h3><ol>
                <li><span>Build the audit: the checklist, the ceiling calculator, the booking test on a phone and the consent check, written so you could hand it to someone.</span></li>
                <li><span>Run three audits on properties you can visit: one unpaid for an owner you already know, two at the fee.</span></li>
                <li><span>Put the ceiling, and a retainer priced under it, in front of each owner. Write down the answer, the objection, and how they handle the commission line today.</span></li>
                <li><span>Ask two independent-hotel agencies their smallest retained property. Ask booking-software partner managers and an innkeeper association whether they would refer.</span></li>
              </ol>
              <p className="oe-page-note">Do not build the post-stay messages, the automation or the scorecard yet. They follow the first yes. Success looks like one owner paying for the audit, one owner agreeing to a retainer at or under the ceiling, and an audit delivered close to its modeled hours.</p></div>
              <div className="bl-boundary-list oe-stop"><h3>Stop or redesign when</h3><ul>
                <li>No owner in the band will fund the modeled $600 a month.</li>
                <li>Agencies already serve the band at prices owners prefer.</li>
                <li>Audit after audit finds base commission and a low share through the sites, so the recoverable sits below the model.</li>
                <li>Your recorded hours run past the model. Then move up to larger properties, or sell the audit alone.</li>
              </ul></div>
            </div>
            <aside className="bl-disclosure"><strong>Not legal advice</strong><span>Guest data stays inside the booking sites&apos; terms, US email law for the property&apos;s own list, and European rules for European guests, with consent recorded at capture and a stated purpose. This is not legal advice. Anything touching rate-parity terms or how rates must be displayed goes to the owner&apos;s counsel.</span></aside>
          </section>
        </div>

        <section className="bl-chapter oe-band-inset bl-shell" id="episode" aria-labelledby="episode-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">Supporting material</p><div><h2 id="episode-title">Watch the investigation.</h2><p>The episode carries the argument, the evidence and the modeled arithmetic, including the part that comes out thin.</p></div></header>
          <div className="oe-media">
            <div className="oe-media__watch"><WatchAction slug={operation.slug} /></div>
            <div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Episode</span><p>{operation.episodeTitle}</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Status</span><p>{episodeStatus(operation.slug)}</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Host</span><p>The host spent over a decade in hospitality, including Ace Hotel and Standard Hotels. He has not run this practice, and the episode does not pretend otherwise.</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">AI disclosure</span><p>{AI_DISCLOSURE}</p></div>
            </div>
          </div>
        </section>

        <section className="bl-chapter oe-band-raised bl-shell" id="download" aria-labelledby="download-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">05 / Download</p><div><h2 id="download-title">Take the Operator Canvas with you.</h2><p>The print edition of this Canvas, transcribed from the locked version: the scope boundary and acceptance measure, the delivery system, the ceiling and the operator model with its low, base and high cases, the risk register, the 30-day test plan, the unknowns and every source note.</p></div></header>
          <aside className="bl-disclosure"><strong>Required disclosure</strong><span>Modeled scenario, not observed performance or an earnings forecast. Other figures are reported by their named sources and carry their hedges. Nothing here is legal, tax or financial advice, and nothing predicts what any property will recover.</span></aside>
          <a className="oe-direct-download" href={operation.pdfUrl}>Download the Operator Canvas PDF</a>
          <p className="oe-page-note">Downloading does not subscribe you to the newsletter.</p>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
