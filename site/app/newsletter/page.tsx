import type { Metadata } from 'next';
import Link from 'next/link';
import { NewsletterForm } from '../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../components/SiteChrome';
import { AI_DISCLOSURE, TAGLINE } from '../lib/brand';

export const metadata: Metadata = {
  title: 'Newsletter · The Operator Economy',
  description: 'One email when a new episode ships, with its Operator Canvas.',
};

export default function NewsletterPage() {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="newsletter" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="page-title">
          <div className="bl-episode-feature__intro">
            <p className="bl-chapter__number">Newsletter</p>
            <h1 id="page-title">Get Monday&apos;s episode by email.</h1>
            <p>{TAGLINE} One email when each episode ships, with a link to its Operator Canvas. No drip campaign, and you can unsubscribe from any email.</p>
          </div>
        </section>

        <section className="bl-shell" id="newsletter" aria-labelledby="newsletter-title" style={{ paddingBottom: 'var(--bl-section-space)' }}>
          <aside className="bl-subscription-band">
            <div>
              <h2 id="newsletter-title">Subscribe</h2>
              <p>What you get: the episode and the Operator Canvas for each new business. What you do not get: income promises or a sales sequence.</p>
            </div>
            <NewsletterForm />
          </aside>
          <p className="oe-page-note" style={{ marginTop: 'var(--bl-space-5)' }}>{AI_DISCLOSURE} <Link className="bl-text-link" href="/about">About the show</Link></p>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
