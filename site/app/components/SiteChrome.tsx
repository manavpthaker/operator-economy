import Link from 'next/link';
import { AI_DISCLOSURE, CHANNEL_URL, TAGLINE } from '../lib/brand';

type Section = 'home' | 'businesses' | 'method' | 'about' | 'privacy' | 'newsletter';

export function Wordmark() {
  return (
    <Link className="bl-wordmark oe-wordmark" href="/" aria-label="The Operator Economy, home">
      <span className="oe-wordmark__the" aria-hidden="true">The</span>
      <span className="oe-wordmark__name" aria-hidden="true">Operator Economy</span>
    </Link>
  );
}

export function SiteHeader({ current }: { current?: Section }) {
  return (
    <header className="bl-masthead">
      <div className="bl-shell bl-masthead__inner oe-masthead__inner">
        <Wordmark />
        <nav className="oe-nav" aria-label="Site">
          <Link href="/businesses" aria-current={current === 'businesses' ? 'page' : undefined}>
            Businesses
          </Link>
          <Link href="/method" aria-current={current === 'method' ? 'page' : undefined}>
            Method
          </Link>
          <Link href="/about" aria-current={current === 'about' ? 'page' : undefined}>
            About
          </Link>
        </nav>
        <Link className="bl-action" href="/newsletter">
          Subscribe
        </Link>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="bl-system-footer">
      <div className="bl-shell bl-system-footer__inner">
        <div>
          <strong>The Operator Economy</strong>
          <p className="oe-footer-line">{TAGLINE}</p>
          <p className="oe-footer-disclosure">{AI_DISCLOSURE}</p>
          <nav className="oe-footer-nav" aria-label="Footer">
            <a href={CHANNEL_URL} target="_blank" rel="noreferrer">
              YouTube<span className="oe-sr"> (opens in new tab)</span>
            </a>
            <Link href="/newsletter">Newsletter</Link>
            <Link href="/businesses">Businesses</Link>
            <Link href="/method">Method</Link>
            <Link href="/about">About</Link>
            <Link href="/privacy">Privacy</Link>
          </nav>
        </div>
        <span className="oe-mark">Build. Own. Operate.</span>
      </div>
    </footer>
  );
}
