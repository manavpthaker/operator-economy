import Image from 'next/image';
import Link from 'next/link';
import { GuideToggle } from '../../components/GuideToggle';
import { NewsletterBand } from '../../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../../components/SiteChrome';
import { type Operation, padOperationNumber } from '../../lib/operations';

const capabilities = [
  ['01 · Find', 'Approve what is true and current', 'Google Business Profile · OTA listings', 'Inconsistent or stale promises', 'Keep discovery accurate'],
  ['02 · Convert', 'Own exceptions and guest experience', 'Hotel site · booking engine · phone', 'Outreach sends demand into a broken path', 'Complete the promise'],
  ['03 · Remember', 'Approve consent, context, and tone', 'Guest list · CRM · permission record', 'Privacy breach or generic outreach', 'Earn useful context'],
  ['04 · Return', 'Choose the offer and approve the message', 'Email delivery · workflow automation', 'Discounting without relationship value', 'Create relevance'],
  ['05 · Measure', 'Interpret the result and redesign the flow', 'Booking reports · monthly scorecard', 'Activity rises while the outcome stays flat', 'Prove the mix moved'],
] as const;

const unknowns = [
  ['U001', 'What a hotel will pay for this specific service. Five providers were scanned; no public price was found. A first paid conversation would test it.'],
  ['U002', 'Delivery hours per property at a defensible standard. Measure this in the first engagement.'],
  ['U003', 'Whether a property renews after the first measured period. Track this after the first quarter.'],
] as const;

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

export function DirectBookingPage({ operation }: { operation: Operation }) {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="businesses" />
      <main id="main">
        <section className="bl-opening bl-shell" aria-labelledby="business-title">
          <div className="oe-hero">
            <div className="bl-episode-feature__intro">
              <h1 id="business-title">{operation.name}</h1>
              <p>A working model for helping independent hotels turn first-time OTA guests into direct repeat customers.</p>
              <p className="oe-page-note">
                This public working paper is based on a published V1 episode. It is not an approved V2 Canvas.{' '}
                <Link className="bl-text-link" href="/method">What that means</Link>
              </p>
            </div>
          </div>

          <article className="oe-operation-sheet" aria-labelledby="docket-title">
            <aside className="bl-docket">
              <div className="bl-docket__head"><span>Working paper · V1-derived</span><span>Not V2 approved</span></div>
              <div className="bl-docket__body">
                <span className="bl-docket__identity">№{padOperationNumber(operation.number)} · {operation.audience}</span>
                <h2 id="docket-title">Could one operator make repeat bookings direct?</h2>
                <p>Judge the opportunity, the work required, and the test that should come before a larger claim.</p>
              </div>
              <dl className="bl-docket__rows">
                <div className="bl-docket__row"><dt>Buyer</dt><dd>{operation.audience}</dd></div>
                <div className="bl-docket__row"><dt>Entry offer</dt><dd>{operation.offer}</dd></div>
                <div className="bl-docket__row"><dt>First test</dt><dd>One property</dd></div>
              </dl>
            </aside>
            <figure className="bl-working-model">
              <Image src="/illustration/episode-006/hotel-working-model.jpg" alt="A rough hand-drawn working model showing a guest's first hotel stay routed through an OTA toll booth and the second stay returning directly to the hotel." width="1536" height="1024" sizes="(max-width: 900px) calc(100vw - 3rem), (max-width: 1600px) 62vw, 58rem" />
              <figcaption><span>The first stay passes through the OTA toll. The second stay, in oxide, returns directly to the hotel.</span><span>3:2 · complete composition</span></figcaption>
            </figure>
          </article>
        </section>

        <section className="oe-value oe-band-raised bl-shell" id="summary" aria-labelledby="summary-title">
          <div className="oe-value__intro">
            <p className="bl-chapter__number">Start here</p>
            <h2 id="summary-title">The case in three decisions.</h2>
            <p>Read these first. Use the working paper for the evidence, assumptions, economics, and stop conditions behind each answer.</p>
          </div>
          <ol className="oe-decision-list" aria-label="Decision summary">
            <li><span>01</span><div><strong>Is the problem worth solving?</strong><p>Independent hotels pay for discovery, then often pay again to reach a guest they already served.</p><span className="oe-class"><Link href="/method#evidence-classes">Observed premise</Link></span></div></li>
            <li><span>02</span><div><strong>Can one operator deliver it?</strong><p>The entry offer combines booking-path repair, guest permission, return campaigns, and measurement for one property.</p><span className="oe-class"><Link href="/method#evidence-classes">Modeled offer</Link></span></div></li>
            <li><span>03</span><div><strong>What should be tested first?</strong><p>Use one property&apos;s baseline to test whether direct share moves. Stop if activity rises and the outcome does not.</p><span className="oe-class"><Link href="/method#evidence-classes">Modeled test · unknown result</Link></span></div></li>
          </ol>
          <div className="oe-actions" style={{ alignItems: 'center' }}>
            <a className="bl-action" href="#sheet-00">Explore the working paper</a>
            <GuideToggle />
          </div>
        </section>

        <nav className="bl-anchor-nav bl-shell" aria-label="Working-paper sections">
          <a href="#sheet-00">00 · Opportunity</a><a href="#sheet-01">01 · System</a><a href="#sheet-02">02 · Evidence</a><a href="#sheet-03">03 · Economics</a><a href="#sheet-04">04 · Guardrails</a><a href="#download">05 · Download</a>
        </nav>

        <div id="working-paper-shell">
          <section className="bl-chapter bl-shell" id="sheet-00" aria-labelledby="h-00">
            <header className="bl-chapter__head"><p className="bl-chapter__number">00 / Opportunity</p><div><SectionMark name="buyer" /><h2 id="h-00">Is the problem worth solving?</h2><p>OTAs do discovery well. The opportunity appears when the hotel pays again to reacquire a guest it has already served.</p></div></header>
            <GuideNote step={1} title="Start with the tension, not the tools."><p>Ask who already solves discovery, where the relationship breaks after the stay, and what changes if the second booking becomes direct.</p></GuideNote>
            <div className="bl-split">
              <div className="bl-prose"><h3>What already works</h3><p>The first booking can come through an OTA. Distribution gives an independent property reach it could not efficiently reproduce alone.</p><h3>What the operator changes</h3><p>Earn the second booking direct through permission, useful guest context, a relevant reason to return, and a destination that completes the promise.</p></div>
              <ul className="bl-rule-list" aria-label="Entry wedge and expansion"><li><strong>Entry wedge.</strong> One property: install the recovery stack and measure its direct share.</li><li><strong>Proof before expansion.</strong> The property&apos;s direct share moves against its own baseline.</li><li><strong>Aspirational destination.</strong> A guest-relationship practice serving independent properties.</li></ul>
            </div>
          </section>

          <section className="bl-chapter bl-shell" id="sheet-01" aria-labelledby="h-01">
            <header className="bl-chapter__head"><p className="bl-chapter__number">01 / System</p><div><SectionMark name="workflow" /><h2 id="h-01">What must one operator run?</h2><p>A business is more than a collection of tools. These capabilities describe the recurring work, the inputs it needs, and the judgment that cannot be automated away.</p></div></header>
            <GuideNote step={2} title="What has to run every week?"><p>Read the failure mode before the implementation. Notice where human approval still matters.</p></GuideNote>
            <div aria-label="Capabilities">
              {capabilities.map(([name, judgment, implementation, failure, result]) => (
                <div className="bl-ledger-row" key={name}>
                  <span className="bl-ledger-row__name">{name}</span>
                  <dl className="oe-facts"><div><dt>Human judgment</dt><dd>{judgment}</dd></div><div><dt>Implementation</dt><dd>{implementation}</dd></div><div><dt>Failure mode</dt><dd>{failure}</dd></div></dl>
                  <span className="bl-ledger-row__value">{result}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="bl-chapter oe-band-inset bl-shell" id="sheet-02" aria-labelledby="h-02">
            <header className="bl-chapter__head"><p className="bl-chapter__number">02 / Evidence</p><div><SectionMark name="evidence" /><h2 id="h-02">What do we know, and what remains uncertain?</h2><p>Evidence earns the right to keep investigating. It does not turn an illustrative model into a property-specific result.</p></div></header>
            <GuideNote step={3} title="Separate what is known from what is assumed."><p>Check the evidence class attached to each figure, the arithmetic behind the model, and the open questions the first engagement must answer.</p></GuideNote>
            <div style={{ display: 'grid', gap: 'var(--bl-space-4)' }} aria-label="Evidence receipts">
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Observed · <a href="https://www.cloudbeds.com/online-travel-agencies/commissions/" target="_blank" rel="noreferrer">Cloudbeds 2026</a></span><p><strong>63.4%</strong> of independent-hotel reservations were attributed to Booking.com and Expedia in the cited report. Vendor-published.</p><span className="bl-evidence-receipt__count">reported figure</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Observed · <a href="https://www.cloudbeds.com/online-travel-agencies/commissions/" target="_blank" rel="noreferrer">Cloudbeds 2026</a></span><p>Reported cancellation rates were <strong>21.8%</strong> for OTA bookings and <strong>10.6%</strong> for direct bookings in the cited report. Vendor-published.</p><span className="bl-evidence-receipt__count">reported figure</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Modeled · arithmetic</span><p><strong>$135K</strong> annual commission-exposure arithmetic: 20 rooms, $180 ADR, 70% occupancy, 63.4% OTA share, and 22% commission. Not a reported hotel result.</p><span className="bl-evidence-receipt__count">assumptions shown</span></aside>
            </div>
            <div style={{ marginTop: 'var(--bl-space-7)' }} aria-label="Unknown register">
              <p className="bl-chapter__number" style={{ marginBottom: 'var(--bl-space-3)' }}>Unknown register · open questions carried, not hidden</p>
              {unknowns.map(([id, statement]) => <div className="bl-ledger-row" key={id}><span className="bl-ledger-row__name">{id}</span><p>{statement}</p><span className="oe-class">Unknown</span></div>)}
            </div>
          </section>

          <section className="bl-chapter bl-shell" id="sheet-03" aria-labelledby="h-03">
            <header className="bl-chapter__head"><p className="bl-chapter__number">03 / Economics</p><div><SectionMark name="economics" /><h2 id="h-03">Could the economics work?</h2><p>The market pressure, hotel model, and operator workload answer different questions. Read them side by side; never collapse them into one revenue claim.</p></div></header>
            <GuideNote step={4} title="Where could value move, and what is still unpriced?"><p>Compare observed commission pressure, the illustrative hotel model, and the missing pricing, capacity, and renewal data.</p></GuideNote>
            <div className="oe-three" aria-label="Three views, never blended">
              <article><span className="oe-class">Observed · Cloudbeds 2026</span><h3>18–30%</h3><p>All-in Booking.com commission range reported when loyalty and visibility programs are included.</p><dl><div><dt>Base commission</dt><dd>Included</dd></div><div><dt>Visibility programs</dt><dd>Included</dd></div><div><dt>Property result</dt><dd>Unknown</dd></div></dl></article>
              <article><span className="oe-class">Modeled · arithmetic</span><h3>$135K/yr</h3><p>Arithmetic estimate of annual commission exposure. Not a reported hotel result or a universal loss figure.</p><dl><div><dt>Rooms × ADR</dt><dd>20 × $180</dd></div><div><dt>Occupancy × OTA share</dt><dd>70% × 63.4%</dd></div><div><dt>Commission</dt><dd>22%</dd></div></dl></article>
              <article><span className="oe-class">Unknown · open</span><h3>Unknown</h3><p>Public provider pricing does not establish what a hotel will pay for this service.</p><dl><div><dt>Providers scanned</dt><dd>Five</dd></div><div><dt>Delivery capacity</dt><dd>Test</dd></div><div><dt>Renewal threshold</dt><dd>Measure</dd></div></dl></article>
            </div>
            <aside className="bl-decision-note" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Most sensitive assumption</strong><p>The 22% commission point and the sector-average OTA share applied to one property. The first test replaces both with the property&apos;s own baseline.</p></aside>
            <aside className="bl-disclosure"><strong>Economics boundary</strong><span>Illustrative arithmetic, not observed performance and not an earnings forecast. No operator revenue is modeled: what a hotel pays for this service remains unknown.</span></aside>
          </section>

          <section className="bl-chapter oe-band-raised oe-active-chapter bl-shell" id="sheet-04" aria-labelledby="h-04">
            <header className="bl-chapter__head"><p className="bl-chapter__number">04 / Guardrails</p><div><SectionMark name="test" /><h2 id="h-04">What should you test first?</h2><p>The first engagement should reduce uncertainty, not hide it. Establish the baseline, repair the destination, respect permission, and define the result that would justify continuing.</p></div></header>
            <GuideNote step={5} title="What can you test before making a bigger claim?"><p>Start with the property&apos;s baseline, fix the booking and phone path, and name the stop conditions before activity begins.</p></GuideNote>
            <div className="bl-split">
              <div className="bl-anatomy"><h3>Start with permission and a baseline</h3><ol><li><span>Measure booking mix, commission, cancellations, missed calls, and repeat stays.</span></li><li><span>Repair the mobile booking and phone path before running outreach.</span></li><li><span>Begin with past guests who have permission to hear from the property.</span></li><li><span>Track direct share before and after; use other metrics to diagnose the path.</span></li></ol></div>
              <div className="bl-boundary-list oe-stop"><h3>Stop or redesign when</h3><ul><li>The property cannot establish a credible baseline.</li><li>Guest permission or data access is unclear.</li><li>The destination cannot complete the promise.</li><li>Activity rises while direct share does not move.</li></ul></div>
            </div>
          </section>
        </div>

        <section className="bl-chapter oe-band-inset bl-shell" id="episode" aria-labelledby="episode-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">Supporting material</p><div><h2 id="episode-title">Watch the investigation.</h2></div></header>
          <div className="oe-media">
            <a className="oe-video" href={operation.youtubeUrl} target="_blank" rel="noreferrer"><span>Watch №006 on YouTube<span className="oe-sr"> (opens in new tab)</span></span></a>
            <div><div className="bl-ledger-row"><span className="bl-ledger-row__name">Episode</span><p>{operation.episodeTitle} · live · Aug 2026</p></div><div className="bl-ledger-row"><span className="bl-ledger-row__name">Format</span><p>Published under the earlier V1 Blueprint regime.</p></div><div className="bl-ledger-row"><span className="bl-ledger-row__name">Transcript</span><p>Captions are available on YouTube.</p></div></div>
          </div>
        </section>

        <section className="bl-chapter oe-band-raised bl-shell" id="download" aria-labelledby="download-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">05 / Download</p><div><h2 id="download-title">Take the legacy Blueprint with you.</h2><p>The existing V1 PDF remains available as the historical companion to the episode. It is not a gated or V2 Canvas edition.</p></div></header>
          <aside className="bl-disclosure"><strong>Required disclosure</strong><span>This working paper is derived from a V1 episode. Figures shown are reported by their named sources or labeled arithmetic. Nothing here is observed operator performance or an earnings forecast.</span></aside>
          <a className="oe-direct-download" href={operation.pdfUrl}>Download the legacy Blueprint PDF</a>
          <p className="oe-page-note">Downloading does not subscribe you to the newsletter.</p>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
