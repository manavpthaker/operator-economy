import Link from 'next/link';
import { SiteFooter, SiteHeader } from './components/SiteChrome';

export default function NotFound() {
  return (
    <div>
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="not-found-title">
          <div className="bl-episode-feature__intro">
            <p className="bl-chapter__number">404</p>
            <h1 id="not-found-title">This page is not in the ledger.</h1>
            <p>The address may be old, or the business may have moved.</p>
            <div className="oe-actions"><Link className="bl-action" href="/businesses">Browse businesses</Link><Link className="bl-action" href="/">Return home</Link></div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
