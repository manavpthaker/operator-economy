import Link from 'next/link';

type Section = 'home' | 'businesses' | 'method' | 'privacy';

export function SiteHeader({ current }: { current?: Section }) {
  return (
    <header className="bl-masthead">
      <div className="bl-shell bl-masthead__inner oe-masthead__inner">
        <Link className="bl-wordmark" href="/" aria-label="The Operator Economy, home">
          The Operator Economy
        </Link>
        <nav className="oe-nav" aria-label="Site">
          <Link href="/businesses" aria-current={current === 'businesses' ? 'page' : undefined}>
            Businesses
          </Link>
          <Link href="/method" aria-current={current === 'method' ? 'page' : undefined}>
            Method
          </Link>
        </nav>
        <Link className="bl-action" href="/#newsletter">
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
          <nav className="oe-footer-nav" aria-label="Footer">
            <a href="https://www.youtube.com/@operatoreconomy" target="_blank" rel="noreferrer">
              YouTube<span className="oe-sr"> (opens in new tab)</span>
            </a>
            <Link href="/#newsletter">Newsletter</Link>
            <Link href="/businesses">Businesses</Link>
            <Link href="/method">Method</Link>
            <Link href="/privacy">Privacy</Link>
          </nav>
        </div>
        <span className="oe-mark">Build. Own. Operate.</span>
      </div>
    </footer>
  );
}
