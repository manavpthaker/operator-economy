import s from './page.module.css';
import { BlueprintForm, LedgerForm } from './CaptureForms';

export default function Home() {
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
            <span className={s.btnSecondary}>Subscribe</span>
          </header>

          <div className={s.heroBody}>
            <aside className={s.margin}>
              <span className={s.marginBadge}>V1 · 2026-07-03</span>
              <span className={s.marginNote}>
                <i className={`${s.dot} oe-pulse`} />
                8 sources verified for №001
              </span>
              <span className={s.marginNote}>
                fig. 01 recomputed <b>↻ 2d ago</b>
              </span>
              <span className={s.marginNote}>
                estimates marked, never blended into sourced figures
              </span>
            </aside>

            <div className={s.heroCopy}>
              <div className={s.kicker}>Stop climbing. Start building.</div>
              <h1 className={s.h1}>
                You can build it now. We show you what&apos;s <em>worth</em> building.
              </h1>
              <p className={s.lead}>
                Every Monday: one real business one experienced person can build and run —
                the companies proving it works, the exact stack and what it costs, the
                honest math. Plus the free Operator Blueprint to build from.
              </p>
              <div className={s.chips}>
                <span className={s.chip}>Real companies</span>
                <span className={s.chip}>Sourced numbers</span>
                <span className={s.chip}>Exact stacks</span>
                <span className={s.chip}>Honest failure modes</span>
              </div>
              <div className={s.ctaRow}>
                <a href="#capture" className={s.btnPrimary}>Get the Blueprints →</a>
                <a href="#library" className={s.btnGhost}>Watch the latest breakdown ↗</a>
              </div>
              <span className={s.liveChip}>
                <i className={`${s.dot} oe-pulse`} />
                Episode №001 live · AI implementation as a service
              </span>
            </div>
          </div>
        </div>

        <aside className={`${s.heroPanel} schematic-grid`}>
          <div className={s.panelHeader}>
            <span className={s.panelSheet}>Sheet 01 · №001 — The stack</span>
            <span className={s.panelRunning}>
              <i className={`${s.dot} oe-pulse`} />
              Running
            </span>
          </div>

          <div className={s.stack}>
            <div className={s.node}>
              <div className={s.nodeMeta}>
                <span>Step 01 · Intake</span>
                <span style={{ color: 'var(--status-live)' }}>● Live</span>
              </div>
              <div className={s.nodeName}>Airtable client portal</div>
              <div className={s.nodePrice}>
                $0<span className={s.nodePriceUnit}>/mo</span>
              </div>
            </div>
            <i className={s.wire} />
            <div className={s.node}>
              <div className={s.nodeMeta}>
                <span>Step 02 · The brain</span>
                <span style={{ color: 'var(--status-live)' }}>● Running</span>
              </div>
              <div className={s.nodeName}>Claude API</div>
              <div className={s.nodePrice}>
                $20<span className={s.nodePriceUnit}>/mo</span>
              </div>
            </div>
            <i className={s.wire} />
            <div className={s.node}>
              <div className={s.nodeMeta}>
                <span>Step 03 · Runtime</span>
              </div>
              <div className={s.nodeName}>n8n, self-hosted</div>
              <div className={s.nodePrice}>
                ~$0<span className={s.nodePriceUnit}>/mo</span>
              </div>
            </div>
            <i className={s.wire} />
            <div className={s.node}>
              <div className={s.nodeMeta}>
                <span>Step 04 · Delivery</span>
                <span className={s.goldText}>Reported</span>
              </div>
              <div className={s.nodeName}>First client project</div>
              <div className={`${s.nodePrice} ${s.goldText}`}>$2,000</div>
            </div>
            <div className={s.bracket}>
              <span className={s.bracketLabel}>≤ $100/mo tooling</span>
            </div>
          </div>

          <div className={s.panelFoot}>
            <span className={s.reportedChip}>
              <b>REPORTED</b> Medium · Mar 2026 · unaudited
            </span>
            <span className={s.margin90}>
              Margin ~90% <i className={s.tri}>▲</i>
            </span>
          </div>
        </aside>
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
              Sheet 00 · The format — running on №001
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
            <span className={s.reportedChip}>
              <b>SOURCE</b> Accenture FY2025 · CIO Dive
            </span>
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
            <h2 className={s.h2}>Businesses you could build.</h2>
          </div>
          <span className={s.tag}>Every episode ships with its blueprint</span>
        </div>

        <div className={s.filterRow}>
          <div className={s.filters}>
            <span className={s.filterActive}>All</span>
            <span className={s.filterInactive}>Services</span>
            <span className={s.filterInactive}>Software</span>
            <span className={s.filterInactive}>Media</span>
          </div>
          <span className={s.tag}>№001 live · 18 more in the research queue</span>
        </div>

        <div className={s.cards}>
          <article className={`${s.card} ${s.cardLive}`}>
            <div className={s.cardHead}>
              <span className={s.cardEpisode}>№001 · Services</span>
              <span className={s.cardStatus}>
                <i className={`${s.dot} oe-pulse`} style={{ width: 5, height: 5 }} />
                Live
              </span>
            </div>
            <h3 className={s.cardTitle}>AI implementation as a service</h3>
            <div className={s.cardTail}>
              <div className={s.cardFigure}>
                $2–8K<span className={s.cardFigureUnit}>/mo</span>
              </div>
              <div className={s.cardFigureMeta}>
                Realistic year one · &lt;$100/mo stack
              </div>
              <span className={s.estimateChip}>
                <b>ESTIMATE</b> №001 honest math
              </span>
              <div className={s.cardLinks}>
                <a href="#capture" className={s.cardLinkPrimary}>Watch the episode ↗</a>
                <a href="#capture" className={s.cardLinkSecondary}>Blueprint №001 (PDF)</a>
              </div>
            </div>
          </article>

          <article className={`${s.card} ${s.cardQueued}`}>
            <div className={s.cardHead}>
              <span className={`${s.cardEpisode} ${s.cardEpisodeMuted}`}>№002 · Services</span>
              <span className={s.cardStatusMuted}>In research</span>
            </div>
            <h3 className={`${s.cardTitle} ${s.cardTitleQueued}`}>The voice-agent agency</h3>
            <div className={s.cardTail}>
              <div className={s.queuedNote}>
                Figures publish with the episode — sourced first, shown second.
              </div>
            </div>
          </article>

          <article className={`${s.card} ${s.cardQueued}`}>
            <div className={s.cardHead}>
              <span className={`${s.cardEpisode} ${s.cardEpisodeMuted}`}>№003 · Services</span>
              <span className={s.cardStatusMuted}>In research</span>
            </div>
            <h3 className={`${s.cardTitle} ${s.cardTitleQueued}`}>The boring-automation agency</h3>
            <div className={s.cardTail}>
              <div className={s.queuedNote}>
                Figures publish with the episode — sourced first, shown second.
              </div>
            </div>
          </article>
        </div>
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
            <div className={`${s.disclosureLabel} ${s.disclosureLabelAccent}`}>Business model</div>
            <div className={s.disclosureAns}>
              You trust the numbers enough to come back.
            </div>
          </div>
        </div>
        <div className={s.filed}>Filed 2026-07-03 · theoperatoreconomy.com</div>
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
              citation.
            </p>
            <div className={s.tag}>
              Free · One email a week · No drip campaigns · Unsubscribe anytime
            </div>
          </div>

          <BlueprintForm />
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
            <a href="https://www.youtube.com/@TheOperatorEconomy" target="_blank" rel="noreferrer">YouTube ↗</a>
            <a href="#capture">Newsletter</a>
            <a href="https://www.linkedin.com/company/the-operator-economy" target="_blank" rel="noreferrer">LinkedIn ↗</a>
            <a href="#library">Blueprints</a>
          </nav>
        </div>
        <div className={s.footerBottom}>
          <span className={s.footerTag}>Build. Own. Operate.</span>
          <div className={s.colophon}>
            <span>V1 · 2026-07-03</span>
            <span>
              <i className={s.dot} />
              8 sources verified for №001
            </span>
            <span>theoperatoreconomy.com</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
