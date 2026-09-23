import type { Metadata } from 'next';
import Link from 'next/link';
import { NewsletterBand } from './components/NewsletterForm';
import { SiteFooter, SiteHeader } from './components/SiteChrome';
import { EpisodeThumbnail, WatchAction, episodeStatus } from './components/WatchAction';
import { AI_DISCLOSURE, POSITIONING } from './lib/brand';
import { LATEST } from './lib/operations';

export const metadata: Metadata = {
  title: 'The Operator Economy',
  description: POSITIONING,
};

export default function Home() {
  const latest = LATEST;
  const canvasHref = `/businesses/${latest.slug}`;

  return (
    <div className="oe-home" data-oe-theme="boundary-ledger" id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="home" />

      <main id="main">
        <section className="bl-opening bl-shell" aria-labelledby="hero-title">
          <div className="oe-hero">
            <div className="bl-episode-feature__intro">
              <p className="bl-chapter__number">The Operator Economy</p>
              <h1 id="hero-title">Build, own and operate a business of one using AI.</h1>
              <p>
                For experienced professionals. Each episode takes one business you could run
                yourself: what it sells, who pays for it, what it can honestly charge, and where it
                breaks. Then it walks through how to start it.
              </p>
              <a className="oe-hero-cta" href="#latest">
                <span className="oe-hero-cta__label">Newest episode · {episodeStatus(latest.slug)}</span>
                <span className="oe-hero-cta__title">{latest.episodeTitle}</span>
                <span className="oe-hero-cta__go">See the episode <span aria-hidden="true">→</span></span>
              </a>
              <div className="oe-actions">
                <a className="bl-text-link" href="#newsletter">Get new episodes by email</a>
              </div>
              <p className="oe-disclosure-line">{AI_DISCLOSURE}</p>
            </div>
          </div>
        </section>

        <section className="bl-shell oe-latest" id="latest" aria-labelledby="latest-episode-title">
          <div className="bl-episode-feature__intro">
            <p className="bl-chapter__number">Newest episode</p>
            <h2 id="latest-episode-title">{latest.episodeTitle}</h2>
            <p>
              A one-person practice that gets owner-run businesses ready to be inspected by a
              buyer, for a fixed fee. It prepares the business. It does not sell it.
            </p>
            <div className="oe-actions">
              <WatchAction slug={latest.slug} label="Watch the newest episode" />
              <Link className="bl-action" href={canvasHref}>Open the Operator Canvas</Link>
            </div>
          </div>

          <article className="oe-operation-sheet oe-operation-sheet--episode" aria-labelledby="latest-title">
            <aside className="bl-docket">
              <div className="bl-docket__head">
                <span>Latest operation</span>
                <span>{episodeStatus(latest.slug)}</span>
              </div>
              <div className="bl-docket__body">
                <span className="bl-docket__identity">{latest.audience}</span>
                <h3 id="latest-title">{latest.name}</h3>
                <p>{latest.summary}</p>
              </div>
              <dl className="bl-docket__rows">
                <div className="bl-docket__row"><dt>Buyer</dt><dd>{latest.audience}</dd></div>
                <div className="bl-docket__row"><dt>Offer</dt><dd>{latest.offer}</dd></div>
                <div className="bl-docket__row"><dt>Not included</dt><dd>The sale, brokerage, any fee tied to a sale</dd></div>
              </dl>
            </aside>

            <figure className="oe-episode-art">
              <EpisodeThumbnail
                slug={latest.slug}
                thumbnail={latest.thumbnail}
                sizes="(max-width: 900px) calc(100vw - 3rem), (max-width: 1600px) 62vw, 58rem"
              />
              <figcaption>
                <span>Episode thumbnail. Everyone pictured is AI-generated.</span>
                <span>{latest.published}</span>
              </figcaption>
            </figure>
          </article>
        </section>

        <NewsletterBand />

        <section className="oe-value oe-band-raised bl-shell" id="canvas" aria-labelledby="canvas-title">
          <div className="oe-value__intro">
            <p className="bl-chapter__number">The Operator Canvas</p>
            <h2 id="canvas-title">The episode tells the story. The Canvas helps you decide.</h2>
            <p>Every business is reduced to three decisions. The evidence, assumptions and open questions stay attached to each answer.</p>
            <Link className="bl-action" href={canvasHref}>Open this episode&apos;s Canvas</Link>
          </div>
          <ol className="oe-decision-list" aria-label="Three decisions">
            <li><span>01</span><div><strong>Is the problem worth solving?</strong><p>The buyer, the costly problem, the offer and the result being purchased.</p></div></li>
            <li><span>02</span><div><strong>Can one operator deliver it?</strong><p>The workflow, the tools, the human judgment, the capacity and the economics.</p></div></li>
            <li><span>03</span><div><strong>What should I test first?</strong><p>The weakest assumption, the first 30-day test, and the conditions for stopping.</p></div></li>
          </ol>
        </section>

        <section className="oe-section bl-shell" id="standard" aria-labelledby="trust-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">The standard</p>
            <div>
              <h2 id="trust-title">Evidence you can inspect. Assumptions you can challenge. Unknowns kept visible.</h2>
              <p>No income promises and no course at the end of the funnel. A sourced number names its source. A modeled number shows its arithmetic. When nobody knows, the page says so.</p>
              <p><Link className="bl-text-link" href="/method">Read the method</Link></p>
            </div>
          </header>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}
