import type { Metadata } from 'next';
import Link from 'next/link';
import { NewsletterBand } from './components/NewsletterForm';
import { SiteFooter, SiteHeader } from './components/SiteChrome';
import { OPERATIONS, padOperationNumber } from './lib/operations';

export const metadata: Metadata = {
  title: 'The Operator Economy',
  description: 'Choose an operation worth owning. Inspect the buyer, offer, economics, evidence, and first test before you commit.',
};

export default function Home() {
  const latest = OPERATIONS[0];
  const recent = OPERATIONS.slice(0, 2);

  return (
    <div className="oe-home" data-oe-theme="boundary-ledger" id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="home" />

      <main id="main">
        <section className="bl-opening bl-shell" aria-labelledby="hero-title">
          <div className="oe-hero">
            <div className="bl-episode-feature__intro">
              <h1 id="hero-title">You can build it now. We show you what&apos;s <em>worth</em> building.</h1>
              <p>
                Choose an operation worth owning. See who buys, what you would run, how the
                numbers work, and the first test to make before you commit.
              </p>
              <div className="oe-actions">
                <a className="bl-action" href={latest.youtubeUrl} target="_blank" rel="noreferrer">
                  Watch the latest episode<span className="oe-sr"> (opens in new tab)</span>
                </a>
                <Link className="bl-action" href="/businesses">Browse businesses</Link>
              </div>
            </div>
          </div>

          <article className="oe-operation-sheet" aria-labelledby="latest-title">
            <aside className="bl-docket">
              <div className="bl-docket__head">
                <span>Latest operation</span>
                <span className="bl-live">Live</span>
              </div>
              <div className="bl-docket__body">
                <span className="bl-docket__identity">№{padOperationNumber(latest.number)} · {latest.audience}</span>
                <h2 id="latest-title">{latest.name}</h2>
                <p>Could one operator help independent hotels turn OTA guests into direct repeat customers?</p>
              </div>
              <dl className="bl-docket__rows">
                <div className="bl-docket__row"><dt>Buyer</dt><dd>{latest.audience}</dd></div>
                <div className="bl-docket__row"><dt>Offer</dt><dd>{latest.offer}</dd></div>
                <div className="bl-docket__row"><dt>Episode</dt><dd>{latest.episodeTitle}</dd></div>
              </dl>
            </aside>

            <figure className="bl-working-model">
              <img
                src="/illustration/episode-006/hotel-working-model.jpg"
                alt="A rough hand-drawn working model showing a guest's first hotel stay routed through an OTA toll booth and the second stay returning directly to the hotel."
                width="1536"
                height="1024"
                loading="eager"
                decoding="async"
              />
              <figcaption>
                <span>Working model for the operation</span>
                <span>{latest.sources} sources · {latest.published}</span>
              </figcaption>
            </figure>
          </article>
        </section>

        <section className="oe-value oe-band-raised bl-shell" id="canvas" aria-labelledby="canvas-title">
          <div className="oe-value__intro">
            <p className="bl-chapter__number">The Operator Canvas</p>
            <h2 id="canvas-title">The story explains the opportunity. The Canvas helps you decide.</h2>
            <p>Every investigation is reduced to three decisions. The evidence, assumptions, and open questions stay attached to the answer.</p>
            <Link className="bl-action" href="/method">See how the Canvas works</Link>
          </div>
          <ol className="oe-decision-list" aria-label="Three decisions">
            <li><span>01</span><div><strong>Is the problem worth solving?</strong><p>See the buyer, the costly problem, the offer, and the result being purchased.</p></div></li>
            <li><span>02</span><div><strong>Can one operator deliver it?</strong><p>See the workflow, tools, human judgment, capacity, and economics.</p></div></li>
            <li><span>03</span><div><strong>What should I test first?</strong><p>See the weakest assumption, the first 30-day test, and the conditions for stopping.</p></div></li>
          </ol>
        </section>

        <section className="oe-section oe-band-inset bl-shell" id="library" aria-labelledby="library-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">Latest work</p>
            <div>
              <h2 id="library-title">Start with a business.</h2>
              <p>Each entry gives you the case for the opportunity, the operating model, the economics, and where the thesis could fail.</p>
            </div>
          </header>
          <div aria-label="Latest episodes">
            {recent.map((operation) => (
              <Link className="bl-library-row" href={`/businesses/${operation.slug}`} key={operation.slug}>
                <span className="bl-library-row__number">№{padOperationNumber(operation.number)}</span>
                <span><strong>{operation.name}</strong><small>{operation.summary}</small></span>
                <span aria-hidden="true">View</span>
              </Link>
            ))}
          </div>
          <p style={{ marginTop: 'var(--bl-space-5)' }}><Link className="bl-text-link" href="/businesses">View all businesses</Link></p>
        </section>

        <section className="oe-trust oe-trust--mineral bl-shell" id="about" aria-labelledby="trust-title">
          <p className="bl-chapter__number">The standard</p>
          <h2 id="trust-title">Evidence you can inspect. Assumptions you can challenge. Unknowns we keep visible.</h2>
          <p>No income promises and no course at the end of the funnel. If a number is sourced, you can open the source. If it&apos;s modeled, you can inspect the arithmetic. If we don&apos;t know, we say so.</p>
          <Link className="bl-text-link" href="/method">Read the method</Link>
        </section>

        <NewsletterBand />
      </main>

      <SiteFooter />
    </div>
  );
}
