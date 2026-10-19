import type { Metadata } from 'next';
import { BusinessList } from '../components/BusinessList';
import { NewsletterBand } from '../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../components/SiteChrome';
import { OPERATIONS } from '../lib/operations';

export const metadata: Metadata = {
  title: 'Businesses · The Operator Economy',
  description: 'Business operations investigated by The Operator Economy, with their episodes, working documents, evidence, and open questions.',
};

export default function BusinessesPage() {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="businesses" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="page-title">
          <div className="bl-episode-feature__intro">
            <h1 id="page-title">Choose the work, not the headline.</h1>
            <p>Each business is named for the operation you would own. The episode title tells the story; the working document helps you judge the opportunity.</p>
          </div>
          <figure className="oe-page-hero__accent" aria-hidden="true">
            <img src="/illustration/system/owned-route.svg" alt="" width="480" height="320" />
          </figure>
        </section>

        <section className="oe-section oe-band-inset bl-shell" aria-labelledby="businesses-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">Published work</p>
            <div><h2 id="businesses-title">Start with a business.</h2><p>Open an entry for the business case, its episode, the Canvas, and what remains unproven.</p></div>
          </header>
          <BusinessList operations={OPERATIONS} />
        </section>

        <section className="oe-trust oe-trust--mineral bl-shell" aria-labelledby="formats-title">
          <p className="bl-chapter__number">Two formats</p>
          <h2 id="formats-title">A Canvas is the decision tool. Blueprints were the earlier format.</h2>
          <p>Each Canvas carries the four-number model, the evidence behind it, and what stays unproven. A business appears here only after its model, evidence, and publication state are locked. The earlier V1 Blueprints are no longer published.</p>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
