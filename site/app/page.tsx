import s from './page.module.css';
import { BlueprintForm, LedgerForm } from './CaptureForms';

// Revalidate daily so the "next Monday" ship date on LatestBlueprint stays
// current between deploys — the homepage otherwise gets baked at build.
export const revalidate = 86400;

import {
  LatestBlueprint,
  getLatestLive,
  getEpisodes,
  getChannelUrl,
  getUpdatedISO,
  getQueueDepth,
  pad,
} from './components/LatestBlueprint';
import { LibraryClient } from './components/LibraryClient';

// Sources for the format band's "SOURCE: Accenture FY2025" chip.
// These are the numbers currently on the format band; when the format band
// starts pulling per-episode figures, this table moves to episodes.json.
const FORMAT_BAND_SOURCE = {
  label: 'Accenture FY2025 · CIO Dive',
  url: 'https://www.ciodive.com/news/accenture-generative-ai-bookings-fy2025/730821/',
};

// Human-readable "N days ago" from an ISO date; build-time computation.
function relativeAge(iso: string): string {
  const then = Date.parse(iso);
  if (Number.isNaN(then)) return '';
  const now = Date.parse(BUILD_DATE);
  const days = Math.max(0, Math.floor((now - then) / 86_400_000));
  if (days === 0) return 'today';
  if (days === 1) return '1d ago';
  if (days < 30) return `${days}d ago`;
  const months = Math.floor(days / 30);
  return months === 1 ? '1mo ago' : `${months}mo ago`;
}

// Frozen build-day for deterministic prerender. The pipeline updates
// `episodes.json.updated` on every derive; that + this build-day drive
// the "recomputed Nd ago" label. On each Vercel deploy this string is
// re-evaluated at build time.
const BUILD_DATE = new Date().toISOString().slice(0, 10);

export default function Home() {
  const latest = getLatestLive();
  const num = latest ? pad(latest.number) : '001';
  const liveChipText = latest
    ? `Episode №${num} live · ${latest.title}`
    : 'Episode №001 publishes Monday';
  const channelUrl = getChannelUrl();
  const watchHref = latest?.youtube_url ?? channelUrl;
  const updatedISO = getUpdatedISO();
  const updatedAge = relativeAge(updatedISO);
  const sourcesLine = latest?.sources_verified
    ? `${latest.sources_verified} sources verified for №${num}`
    : 'sources publish with the episode';

  return (
    <main className={s.page}>
      {/* ============ HERO ============ */}
      <section className={s.hero}>
        <div className={s.heroLeft}>
          <header className={s.header}>
            <div className={s.brand}>
              <span className={s.brandKicker}>The</span>
              <span className={s.brandName}>Operator Economy</span>
            </div>
            <nav className={s.nav}>
              <a href="#library" className={s.navActive}>Episodes</a>
              <a href="#library">Blueprints</a>
              <a href="#capture">Newsletter</a>
              <a href="#disclosures">About</a>
            </nav>
            <a href="#capture" className={s.btnSecondary}>Subscribe</a>
          </header>

          <div className={s.heroBody}>
            <aside className={s.margin}>
              <span className={s.marginBadge}>V1 · {updatedISO}</span>
              <span className={s.marginNote}>
                <i className={`${s.dot} oe-pulse`} />
                {sourcesLine}
              </span>
              <span className={s.marginNote}>
                fig. 01 recomputed <b>↻ {updatedAge}</b>
              </span>
              <span className={s.marginNote}>
                estimates marked, never blended into sourced figures
              </span>
            </aside>

            <div className={s.heroCopy}>
              <div className={s.kicker}>Stop climbing. Start building.</div>
              <h1 className={s.h1}>
                It&apos;s easy to build now. It&apos;s hard to know <em>what</em> to build.
              </h1>
              <p className={s.lead}>
                Every Monday: one real business one experienced person can build and run —
                the companies proving it works, the exact stack and what it costs, the
                honest math. You bring the expertise you already have. The free
                Operator Blueprint is the rest.
              </p>
              <div className={s.chips}>
                <span className={s.chip}>Real companies</span>
                <span className={s.chip}>Sourced numbers</span>
                <span className={s.chip}>Exact stacks</span>
                <span className={s.chip}>Honest failure modes</span>
              </div>
              <div className={s.ctaRow}>
                <a href="#capture" className={s.btnPrimary}>Get the Blueprints →</a>
                <a
                  href={watchHref}
                  target="_blank"
                  rel="noreferrer"
                  className={s.btnGhost}
                >
                  Watch the latest breakdown ↗
                </a>
              </div>
              <span className={s.liveChip}>
                <i className={`${s.dot} oe-pulse`} />
                {liveChipText}
              </span>
            </div>
          </div>
        </div>

        <LatestBlueprint />
      </section>

      {/* ============ HOW EVERY EPISODE WORKS ============ */}
      <section className={s.section} id="format">
        <div className={s.formatHead}>
          <div>
            <div className={s.kicker} style={{ marginBottom: 12 }}>
              The tools got cheap. The judgment didn&apos;t.
            </div>
            <h2 className={s.h2}>How every episode works.</h2>
          </div>
          <p className={s.sub}>
            If we can&apos;t source it, we say it&apos;s an estimate. If it&apos;s a bad idea, we say
            that too.
          </p>
        </div>

        <div className={`${s.formatBand} schematic-grid`}>
          <div className={s.formatHeader}>
            <span className={s.panelSheet}>
              Sheet 00 · The format — running on №{num}
            </span>
            <span className={s.panelRunning}>
              <i className={`${s.dot} oe-pulse`} />
              Running
            </span>
          </div>

          <div className={s.formatNodes}>
            <div className={s.formatNode}>
              <div className={s.nodeMeta}>01 · The thesis</div>
              <div className={s.nodeName}>One buildable business, stated plainly</div>
              <div className={s.nodePrice}>
                ×1<span className={s.nodePriceUnit}> /week</span>
              </div>
            </div>
            <i className={s.formatWire} />
            <div className={s.formatNode}>
              <div className={s.nodeMeta}>02 · The evidence</div>
              <div className={s.nodeName}>Solo operators to venture scale, sourced</div>
              <div className={`${s.nodePrice} ${s.goldText}`}>$5.9B → $2K</div>
            </div>
            <i className={s.formatWire} />
            <div className={s.formatNode}>
              <div className={s.nodeMeta}>03 · The stack</div>
              <div className={s.nodeName}>Exact tools, what they cost and replace</div>
              <div className={s.nodePrice}>
                &lt; $100<span className={s.nodePriceUnit}>/mo</span>
              </div>
            </div>
            <i className={s.formatWire} />
            <div className={s.formatNode}>
              <div className={s.nodeMeta}>04 · The honest math</div>
              <div className={s.nodeName}>Realistic ranges + named failure modes</div>
              <div className={s.nodePrice}>
                $2–8K<span className={s.nodePriceUnit}>/mo yr 1</span>
              </div>
            </div>
          </div>

          <div className={s.formatFoot}>
            <a
              href={FORMAT_BAND_SOURCE.url}
              target="_blank"
              rel="noreferrer"
              className={s.reportedChip}
              style={{ textDecoration: 'none' }}
            >
              <b>SOURCE</b> {FORMAT_BAND_SOURCE.label} ↗
            </a>
            <span className={s.formatFootRight}>
              estimates marked · never blended ↻
            </span>
          </div>
        </div>
      </section>

      {/* ============ LIBRARY ============ */}
      <section className={s.library} id="library">
        <div className={s.libraryHead}>
          <div>
            <div className={s.kicker} style={{ marginBottom: 12 }}>The library</div>
            <h2 className={s.h2}>One-person businesses you could actually run.</h2>
          </div>
          <span className={s.tag}>Every episode ships with its blueprint</span>
        </div>

        <LibraryClient
          episodes={getEpisodes().filter((e) => e.status !== 'queued')}
          channelUrl={channelUrl}
          queueDepth={getQueueDepth()}
        />
      </section>

      {/* ============ DISCLOSURES ============ */}
      <section className={s.disclosures} id="disclosures">
        <div className={s.disclosureBlock}>
          <div className={s.disclosureHead}>
            <span className={s.disclosureTitle}>Disclosures</span>
            <span className={s.tag}>№000 · Applies to every episode</span>
          </div>
          <div className={s.disclosureRow}>
            <div className={s.disclosureLabel}>Income promises</div>
            <div className={s.disclosureAns}>None.</div>
          </div>
          <div className={s.disclosureRow}>
            <div className={s.disclosureLabel}>Course at the end of the funnel</div>
            <div className={s.disclosureAns}>
              <span className="oe-mono">$0</span> — there isn&apos;t one.
            </div>
          </div>
          <div className={s.disclosureRow}>
            <div className={s.disclosureLabel}>Secrets</div>
            <div className={s.disclosureAns}>None. Sources instead.</div>
          </div>
          <div className={s.disclosureRow}>
            <div className={s.disclosureLabel}>Scarcity timers</div>
            <div className={s.disclosureAns}>None. The library stays up, free.</div>
          </div>
          <div className={s.disclosureRow}>
            <div className={s.disclosureLabel}>Unicorn ambitions</div>
            <div className={s.disclosureAns}>
              None. These are livings: <span className="oe-mono">$2–8K/mo</span>, honestly ranged.
            </div>
          </div>
          <div className={s.disclosureRow}>
            <div className={`${s.disclosureLabel} ${s.disclosureLabelAccent}`}>Business model</div>
            <div className={s.disclosureAns}>
              You trust the numbers enough to come back.
            </div>
          </div>
        </div>
        <div className={s.filed}>Filed {updatedISO} · theoperatoreconomy.com</div>
      </section>

      {/* ============ CAPTURE ============ */}
      <section className={s.capture} id="capture">
        <div className={s.captureGrid}>
          <div>
            <div className={s.kicker} style={{ marginBottom: 16 }}>
              The Blueprint library
            </div>
            <h3 className={s.h3}>
              Don&apos;t take notes.
              <br />
              Take the document.
            </h3>
            <p className={s.lead} style={{ maxWidth: '44ch', fontSize: '15.5px' }}>
              Every episode ships with an Operator Blueprint: the sourced working doc behind the
              video — evidence table, tool stack with costs, week-by-week playbook, every
              citation. Written so you can execute without a technical background.
            </p>
            <div className={s.tag}>
              Free · One email a week · No drip campaigns · Unsubscribe anytime
            </div>
          </div>

          <BlueprintForm
            slug={latest?.slug ?? 'newsletter'}
            number={num}
            title={latest?.title}
            rev={latest?.rev}
            date={latest?.date}
            sourcesVerified={latest?.sources_verified}
            readMinutes={latest?.read_minutes}
          />
        </div>
      </section>

      {/* ============ LEDGER BAND ============ */}
      <section className={`${s.ledger} schematic-grid-h`} aria-label="Newsletter capture">
        <div>
          <div className={s.ledgerLeftLabel}>The Monday note</div>
          <div className={s.ledgerLeftHead}>
            One business, fully sourced, every Monday.
          </div>
        </div>
        <LedgerForm />
        <div className={s.ledgerMeta}>
          <span className={s.ledgerMetaText}>
            1/wk · no drip · unsub anytime
          </span>
          <span className={s.panelRunning}>
            <i className={`${s.dot} oe-pulse`} />
            Running
          </span>
        </div>
      </section>

      {/* ============ FOOTER ============ */}
      <footer className={s.footer}>
        <div className={s.footerTop}>
          <div className={s.brand}>
            <span className={`${s.brandKicker} ${s.footerBrandKicker}`}>The</span>
            <span className={`${s.brandName} ${s.footerBrandName}`}>
              Operator Economy
            </span>
          </div>
          <nav className={s.footerNav}>
            <a href={channelUrl} target="_blank" rel="noreferrer">YouTube ↗</a>
            <a href="#capture">Newsletter</a>
            <a
              href="https://www.linkedin.com/company/the-operator-economy"
              target="_blank"
              rel="noreferrer"
            >
              LinkedIn ↗
            </a>
            <a href="#library">Blueprints</a>
          </nav>
        </div>
        <div className={s.footerBottom}>
          <span className={s.footerTag}>Build. Own. Operate.</span>
          <div className={s.colophon}>
            <span>V1 · {updatedISO}</span>
            <span>
              <i className={s.dot} />
              {sourcesLine}
            </span>
            <span>theoperatoreconomy.com</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
