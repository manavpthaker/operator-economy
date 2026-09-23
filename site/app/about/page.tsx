import type { Metadata } from 'next';
import Link from 'next/link';
import { NewsletterBand } from '../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../components/SiteChrome';
import { AI_DISCLOSURE, CHANNEL_URL, POSITIONING, TAGLINE } from '../lib/brand';

export const metadata: Metadata = {
  title: 'About · The Operator Economy',
  description: POSITIONING,
};

export default function AboutPage() {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="about" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="page-title">
          <div className="bl-episode-feature__intro">
            <p className="bl-chapter__number">About</p>
            <h1 id="page-title">A business of one, taken apart before you build it.</h1>
            <p>{POSITIONING}</p>
            <p className="oe-page-note">{TAGLINE}</p>
          </div>
          <figure className="oe-page-hero__accent" aria-hidden="true">
            <img src="/illustration/system/operator-loop.svg" alt="" width="480" height="320" />
          </figure>
        </section>

        <section className="oe-section oe-band-inset bl-shell" aria-labelledby="what-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">What you get each Monday</p>
            <div><h2 id="what-title">One business, one episode, one Canvas.</h2><p>Each episode investigates a business one experienced operator could own and run with AI doing the work that used to need a team. The Operator Canvas on this site lays out the same case as a decision you can inspect.</p></div>
          </header>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Episode</span><p>The argument, the evidence, and the arithmetic, including the parts that do not survive it.</p><a className="bl-text-link" href={CHANNEL_URL} target="_blank" rel="noreferrer">YouTube<span className="oe-sr"> (opens in new tab)</span></a></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Canvas</span><p>Three decisions: is the problem worth solving, can one operator deliver it, and what should you test first.</p><Link className="bl-text-link" href="/businesses">Businesses</Link></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Canvas PDF</span><p>The print edition of the Operator Canvas, by email: the full model with every assumption shown, the risk register and every source note.</p><Link className="bl-text-link" href="/method">Method</Link></div>
        </section>

        <section className="oe-trust oe-trust--mineral bl-shell" aria-labelledby="disclosure-title">
          <p className="bl-chapter__number">How episodes are made</p>
          <h2 id="disclosure-title">The presenter is an AI avatar. The judgment is not.</h2>
          <p>{AI_DISCLOSURE}</p>
        </section>

        <section className="oe-section bl-shell" aria-labelledby="standard-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">What we will not do</p>
            <div><h2 id="standard-title">No income promises. No course at the end of the funnel.</h2><p>Modeled economics are labeled as modeled and are never an earnings forecast. A case that fails its own arithmetic is published as failing. Where the host has no direct experience of the work, the episode says so.</p><p><Link className="bl-text-link" href="/method">Read the method</Link></p></div>
          </header>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
