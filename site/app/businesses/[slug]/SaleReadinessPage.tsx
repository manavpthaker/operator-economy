import Link from 'next/link';
import { BlueprintRequestForm } from '../../components/BlueprintRequestForm';
import { GuideToggle } from '../../components/GuideToggle';
import { NewsletterBand } from '../../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../../components/SiteChrome';
import { EpisodeThumbnail, WatchAction, episodeStatus } from '../../components/WatchAction';
import { AI_DISCLOSURE } from '../../lib/brand';
import { type Operation } from '../../lib/operations';

// EP007 Operator Canvas, web edition.
// Sources (approved only): operator-blueprint-v2/episodes/EP007-exit-readiness-prep/01-editorial/
// (operator-canvas.md, claims-map.md, script.md, editorial-lock.md), studio/originate/
// exit-readiness-prep/content/PACKAGE-NOTES.md, and content-os/facts.md "EP007 research". Checked line by line
// against operator-canvas.md on 2026-09-23; the derived worksheet (content/blueprint.md) is no longer a source.
// Every figure below is in facts.md with the hedge carried beside it. See site/REBUILD-NOTES.md.

const SOURCES = {
  epi: 'https://exit-planning-institute.org/state-of-owner-readiness',
  epiGenerational: 'https://exit-planning-institute.org/hubfs/25SOOR-Generational.pdf',
  marketPulse:
    'https://www.prnewswire.com/news-releases/the-market-pulse-survey-q2-2026-reports-the-latest-trends-in-business-sales-up-to-50m-302858664.html',
  licensing: 'https://businessbrokeragepress.com/industry-resources/state-licensing/',
} as const;

const capabilities = [
  ['01 · Qualify', 'Decline owners who want a valuation or a buyer', 'Readiness checklist · written scope', 'The engagement drifts toward licensed work', 'Agree what it will not do'],
  ['02 · Interview', 'Surface what only the owner knows', 'Recorded owner and staff interviews', 'The owner will not give the time', 'The part no tool shortens'],
  ['03 · Document', 'Edit and verify every draft', 'AI-drafted write-ups from the interviews', 'A record nobody checked', 'Where AI carries the load'],
  ['04 · Analyse', 'Decide what a buyer would discount', 'Records, customer and key-person review', 'Fixing what a buyer would not care about', 'The judgment is the product'],
  ['05 · Hand off', 'Walk the owner through what was and was not fixed', 'Assembled package · signed acceptance record', 'Acceptance tied to a sale, which makes it a success fee', 'A signed checklist, not a closing'],
] as const;

const unknowns = [
  ['U001', 'Will an owner pay before a deadline exists? The first diagnostic tests it: does the owner see findings they had not seen, and ask what fixing them would cost?', 'Safe first test'],
  ['U002', 'Do brokers already do this work free to win the listing? Ask brokers what they do today with listings they decline.', 'Safe first test'],
  ['U003', 'What are real delivery hours at a defensible standard? Nobody has measured them. Record the hours on the first diagnostic.', 'Safe first test'],
  ['U004', 'Does any published readiness fee correspond to a real transaction? It cannot be resolved from public sources.', 'Later-stage blocker'],
  ['U005', 'Where exactly is the licensing line where you work? It varies by jurisdiction. The operator resolves it locally, with counsel.', 'Later-stage blocker'],
] as const;

const included = [
  'A baseline reading against the readiness checklist',
  'Owner and staff interviews',
  'Writing down how the work actually happens',
  'Cleaning up records so a stranger can verify them',
  'Customer-concentration and key-person analysis',
  'Moving or documenting work only the owner does',
  'Assembling the diligence package and walking the owner through it',
  'A prioritised remediation plan: what was fixed and what remains open',
];

const excluded = [
  'Valuing the business',
  'Finding or introducing a buyer',
  'Representing the owner in a transaction',
  'Negotiating or structuring a deal',
  'Advising on the transaction',
  'Tax, estate or legal advice',
  'Any fee tied to a sale',
];

function SectionMark({ name }: { name: 'buyer' | 'workflow' | 'evidence' | 'economics' | 'test' }) {
  return <svg className="oe-section-mark" aria-hidden="true"><use href={`/illustration/system/icons.svg#${name}`} /></svg>;
}

function GuideNote({ step, title, children }: { step: number; title: string; children: React.ReactNode }) {
  return (
    <aside className="bl-decision-note oe-guide" aria-label={`Walkthrough, step ${step} of 5`}>
      <strong>{title}</strong>
      {children}
    </aside>
  );
}

function Source({ href, children }: { href: string; children: React.ReactNode }) {
  return <a href={href} target="_blank" rel="noreferrer">{children}<span className="oe-sr"> (opens in new tab)</span></a>;
}

export function SaleReadinessPage({ operation }: { operation: Operation }) {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="businesses" />
      <main id="main">
        <section className="bl-opening bl-shell" aria-labelledby="business-title">
          <div className="oe-hero">
            <div className="bl-episode-feature__intro">
              <p className="bl-chapter__number">Operator Canvas</p>
              <h1 id="business-title">{operation.name}</h1>
              <p>It makes a small business able to survive a buyer&apos;s inspection. One operator, one engagement in its interview phase at a time, for a fixed fee that never depends on a sale.</p>
              <p className="oe-page-note">
                Built from the episode&apos;s locked Operator Canvas. Scope: preparation only. It is not the sale, not brokerage, and takes no success fee.{' '}
                <Link className="bl-text-link" href="/method">How the Canvas works</Link>
              </p>
            </div>
          </div>

          <article className="oe-operation-sheet oe-operation-sheet--episode" aria-labelledby="docket-title">
            <aside className="bl-docket">
              <div className="bl-docket__head"><span>Operator Canvas · locked</span><span>{episodeStatus(operation.slug)}</span></div>
              <div className="bl-docket__body">
                <span className="bl-docket__identity">{operation.audience}</span>
                <h2 id="docket-title">Could one operator get a business ready for a buyer, and be paid a fixed fee for it?</h2>
                <p>Judge the problem, the work, the arithmetic, and the test that should come before any bigger claim.</p>
              </div>
              <dl className="bl-docket__rows">
                <div className="bl-docket__row"><dt>Buyer</dt><dd>{operation.audience}</dd></div>
                <div className="bl-docket__row"><dt>Entry offer</dt><dd>One fixed-fee engagement</dd></div>
                <div className="bl-docket__row"><dt>First test</dt><dd>One free diagnostic, timed</dd></div>
              </dl>
            </aside>
            <figure className="oe-episode-art">
              <EpisodeThumbnail
                slug={operation.slug}
                thumbnail={operation.thumbnail}
                sizes="(max-width: 900px) calc(100vw - 3rem), (max-width: 1600px) 62vw, 58rem"
                priority
              />
              <figcaption><span>Episode thumbnail. Everyone pictured is AI-generated.</span><span>{operation.published}</span></figcaption>
            </figure>
          </article>
        </section>

        <section className="oe-value oe-band-raised bl-shell" id="summary" aria-labelledby="summary-title">
          <div className="oe-value__intro">
            <p className="bl-chapter__number">Start here</p>
            <h2 id="summary-title">The case in three decisions.</h2>
            <p>Read these first. The sheets below hold the evidence, the assumptions, the arithmetic and the stop conditions behind each answer.</p>
          </div>
          <ol className="oe-decision-list" aria-label="Decision summary">
            <li><span>01</span><div><strong>Is the problem worth solving?</strong><p>Owners reach a sale with a business that depends on them and records a buyer cannot verify. Research from the Exit Planning Institute puts the listed small businesses that actually sell at roughly three in ten. EPI trains exit planners, so read it as directional.</p><span className="oe-class"><Link href="/method#evidence-classes">Reported premise · directional</Link></span></div></li>
            <li><span>02</span><div><strong>Can one operator deliver it?</strong><p>AI now carries the drafting and assembly that once made this a team job. The interviews and the judgment stay with the operator. The modeled base case does not clear its own income target.</p><span className="oe-class"><Link href="/method#evidence-classes">Modeled offer · base case fails</Link></span></div></li>
            <li><span>03</span><div><strong>What should I test first?</strong><p>Build and publish the readiness checklist, then run one full diagnostic, unpaid, on a real business and record the hours. Ask brokers what they do with listings they decline. Stop if the owner sees findings they had not seen and still will not pay.</p><span className="oe-class"><Link href="/method#evidence-classes">Modeled test · unknown result</Link></span></div></li>
          </ol>
          <div className="oe-actions" style={{ alignItems: 'center' }}>
            <a className="bl-action" href="#sheet-00">Explore the Canvas</a>
            <GuideToggle />
          </div>
        </section>

        <nav className="bl-anchor-nav bl-shell" aria-label="Canvas sections">
          <a href="#sheet-00">00 · Opportunity</a><a href="#sheet-01">01 · System</a><a href="#sheet-02">02 · Evidence</a><a href="#sheet-03">03 · Economics</a><a href="#sheet-04">04 · Guardrails</a><a href="#download">05 · Download</a>
        </nav>

        <div id="working-paper-shell">
          <section className="bl-chapter bl-shell" id="sheet-00" aria-labelledby="h-00">
            <header className="bl-chapter__head"><p className="bl-chapter__number">00 / Opportunity</p><div><SectionMark name="buyer" /><h2 id="h-00">Is the problem worth solving?</h2><p>Everyone around a small-business sale is compensated by the transaction. Getting the business ready to be inspected, years before, is the job.</p></div></header>
            <GuideNote step={1} title="Start with who is paid, and when."><p>Notice that the people around the sale are compensated by the transaction. Then ask who is paid to prepare the business before there is a deal, and what stops them.</p></GuideNote>
            <div className="bl-split">
              <div className="bl-prose">
                <h3>Who buys</h3>
                <p>The owner of an owner-run business with real profit, who intends to exit in one to five years, whose records exist but are not ready for a buyer&apos;s diligence, and whose operations depend materially on them.</p>
                <h3>Who does not</h3>
                <p>A business already run by a manager rather than the owner, one with no realistic buyer, an owner who will not give the interview time, or an owner who wants a valuation or a buyer introduction instead of preparation.</p>
                <h3>What the owner receives</h3>
                <p>A business that survives inspection, and a signed record of every checklist item: resolved, deferred with a stated reason, or out of scope. The deliverable is that record, not a sale. The operator changes what the business can show a buyer. The operator does not change whether a buyer appears.</p>
              </div>
              <ul className="bl-rule-list" aria-label="Entry wedge and expansion">
                <li><strong>Entry wedge.</strong> One fixed-fee readiness engagement for one owner.</li>
                <li><strong>Proof before expansion.</strong> One engagement delivered, with its hours recorded.</li>
                <li><strong>Aspirational destination.</strong> A transition-readiness practice with a referral network and repeat work.</li>
                <li><strong>Scope that must hold at every stage.</strong> Never paid on a transaction. Never advises on one.</li>
              </ul>
            </div>
            <div className="oe-scope" aria-label="Scope">
              <div><h3>Included</h3><ul>{included.map((item) => <li key={item}>{item}</li>)}</ul></div>
              <div className="oe-scope__out"><h3>Never included</h3><ul>{excluded.map((item) => <li key={item}>{item}</li>)}</ul></div>
            </div>
            <aside className="bl-disclosure"><strong>Scope boundary</strong><span>The practice prepares a business for sale. It does not sell it, broker it, value it or advise on the deal. If an owner asks for anything on the never-included list, route it out in writing.</span></aside>
          </section>

          <section className="bl-chapter bl-shell" id="sheet-01" aria-labelledby="h-01">
            <header className="bl-chapter__head"><p className="bl-chapter__number">01 / System</p><div><SectionMark name="workflow" /><h2 id="h-01">What must one operator run?</h2><p>The engagement runs in sequence and waits on one person&apos;s calendar: the owner&apos;s. Adding people does not shorten the interviews, so one operator can hold one engagement in its interview phase at a time.</p></div></header>
            <GuideNote step={2} title="Where does AI help, and where does it not?"><p>AI drafts the write-ups, organises the records and assembles the package. That is now the cheapest part of the job instead of the most expensive. Deciding what a buyer will discount, and telling the owner the business depends on them, stays human.</p></GuideNote>
            <div aria-label="Capabilities">
              {capabilities.map(([name, judgment, implementation, failure, result]) => (
                <div className="bl-ledger-row" key={name}>
                  <span className="bl-ledger-row__name">{name}</span>
                  <dl className="oe-facts"><div><dt>Human judgment</dt><dd>{judgment}</dd></div><div><dt>Implementation</dt><dd>{implementation}</dd></div><div><dt>Failure mode</dt><dd>{failure}</dd></div></dl>
                  <span className="bl-ledger-row__value">{result}</span>
                </div>
              ))}
            </div>
            <aside className="bl-decision-note" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Routed out, every time</strong><p>Anything touching valuation, deal structure, tax or law goes to the owner&apos;s own adviser. Where a transaction follows, the handoff includes a named referral to a licensed broker or adviser.</p></aside>
          </section>

          <section className="bl-chapter oe-band-inset bl-shell" id="sheet-02" aria-labelledby="h-02">
            <header className="bl-chapter__head"><p className="bl-chapter__number">02 / Evidence</p><div><SectionMark name="evidence" /><h2 id="h-02">What do we know, and what remains uncertain?</h2><p>Most of the evidence comes from organisations with an interest in the answer. Each receipt says who published it and how far it can be trusted.</p></div></header>
            <GuideNote step={3} title="Read the hedge before the number."><p>Check who published each figure and what it does not establish. None of it shows that owners will pay to prepare, or that preparation changes whether a business sells.</p></GuideNote>
            <div style={{ display: 'grid', gap: 'var(--bl-space-4)' }} aria-label="Evidence receipts">
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.epi}>Exit Planning Institute</Source></span><p>Roughly <strong>three in ten</strong> listed small businesses actually sell. EPI trains and certifies exit planners, so it has an interest in owners feeling unprepared. Take it as directional rather than precise.</p><span className="bl-evidence-receipt__count">directional</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.epi}>Exit Planning Institute</Source></span><p>Roughly <strong>half</strong> of business exits are not planned at all: death, disability, divorce, disagreement, distress. The timing is often not the owner&apos;s. It does not mean any given owner faces one. Same interest caveat.</p><span className="bl-evidence-receipt__count">directional</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.epiGenerational}>EPI 2025 generational report</Source></span><p><strong>Over half</strong> of owners surveyed intend to exit within five years. <strong>About a quarter</strong> have had a valuation. <strong>Fewer than one in ten</strong> has an estate plan. Self-reported survey. It shows unpreparedness, not that owners will pay to prepare.</p><span className="bl-evidence-receipt__count">self-reported</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.marketPulse}>IBBA and M&amp;A Source, Market Pulse, Q2 2026</Source></span><p>In one recent quarter, <strong>almost nine in ten</strong> deals above $5M drew at least three offers, and <strong>a third</strong> drew ten or more. Advisers reporting their own closings, not an audited database. It says nothing about businesses that are not ready.</p><span className="bl-evidence-receipt__count">directional</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Parallel · adjacent markets</span><p>Similar readiness work is already paid for at three separate scales: preparing large companies before an acquisition, getting software companies ready for a security audit, and certified exit planners. Evidence the job exists, not proof that small owners buy it, or at what price.</p><span className="bl-evidence-receipt__count">parallel</span></aside>
              <aside className="bl-evidence-receipt"><span className="bl-evidence-receipt__source">Reported · <Source href={SOURCES.licensing}>Business Brokerage Press, state licensing</Source></span><p>In a meaningful number of states, taking a fee tied to the sale of a business is a regulated activity, and in some places it can cost you every fee you earned on the deal. No state is named here, because the line moves. Not legal advice.</p><span className="bl-evidence-receipt__count">directional</span></aside>
            </div>
            <aside className="bl-disclosure" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Excluded on purpose</strong><span>A widely circulated claim about what preparation does to a sale price is published by firms that sell preparation, with no corroborating transaction data. It is not used here in any form.</span></aside>
            <div style={{ marginTop: 'var(--bl-space-7)' }} aria-label="Unknown register">
              <p className="bl-chapter__number" style={{ marginBottom: 'var(--bl-space-3)' }}>Unknown register · open questions carried, not hidden</p>
              {unknowns.map(([id, statement, classification]) => <div className="bl-ledger-row" key={id}><span className="bl-ledger-row__name">{id}</span><p>{statement}</p><span className="oe-class">Unknown · {classification}</span></div>)}
            </div>
          </section>

          <section className="bl-chapter bl-shell" id="sheet-03" aria-labelledby="h-03">
            <header className="bl-chapter__head"><p className="bl-chapter__number">03 / Economics</p><div><SectionMark name="economics" /><h2 id="h-03">Could the economics work?</h2><p>Modeled scenario, not observed performance or an earnings forecast. Every input is an assumption, shown so you can replace it. The base case is shown failing because it does.</p></div></header>
            <GuideNote step={4} title="Find the number nobody has measured."><p>Follow the arithmetic to the input everything turns on: hours per engagement. Its largest part is time with the owner, which no tool makes shorter.</p></GuideNote>
            <div className="oe-three" aria-label="Three views, never blended">
              <article><span className="oe-class">Modeled · base case</span><h3>$86,000</h3><p>After costs, before owner pay or tax. Against a $120,000 target, it does not clear. It is not close.</p><dl><div><dt>Fee × engagements</dt><dd>$12,000 × 8</dd></div><div><dt>Gross</dt><dd>$96,000</dd></div><div><dt>Tools and overhead</dt><dd>$10,000</dd></div></dl></article>
              <article><span className="oe-class">Modeled · what it would take</span><h3>about 11</h3><p>Engagements at $12,000 to reach $130,000 gross. The model&apos;s 10.8 engagements at 85 hours each is 920 delivery hours against about 900 available: the entire delivery capacity, with nothing left for acquisition.</p><dl><div><dt>Required gross</dt><dd>$130,000</dd></div><div><dt>Or, at 8 engagements</dt><dd>about $16,250 each</dd></div><div><dt>Or</dt><dd>accept less while testing</dd></div></dl></article>
              <article><span className="oe-class">Unknown · unmeasured</span><h3>85 hours?</h3><p>Hours per engagement. That is an assumption, not a finding. Nobody has measured it, including the host.</p><dl><div><dt>Owner interviews</dt><dd>Not compressible</dd></div><div><dt>Documentation</dt><dd>AI-assisted</dd></div><div><dt>Measure it in</dt><dd>The first diagnostic</dd></div></dl></article>
            </div>
            <aside className="bl-decision-note" style={{ marginTop: 'var(--bl-space-5)' }}><strong>Most sensitive assumption</strong><p>Delivery hours per engagement. Everything turns on it, it is unmeasured, and its largest part, owner interview time, is the part AI does not compress. Plan for cash timing too: a two-to-three month engagement paid on completion creates a working-capital gap, so stage the payments.</p></aside>
            <div className="oe-econ-table" role="region" aria-label="Economics assumptions, low, base and high case" tabIndex={0}>
              <table>
                <caption>Assumptions behind the model (all modeled, from the locked Canvas)</caption>
                <thead><tr><th scope="col">Assumption</th><th scope="col">Low case</th><th scope="col">Base case</th><th scope="col">High case</th><th scope="col">Reasoning</th></tr></thead>
                <tbody>
                  <tr><th scope="row">Price per engagement</th><td>$6,000</td><td>$12,000</td><td>$20,000</td><td>Transferred from compliance-readiness project pricing</td></tr>
                  <tr><th scope="row">Engagements per year</th><td>6</td><td>8</td><td>10</td><td>Constrained by owner availability, not operator hours</td></tr>
                  <tr><th scope="row">Delivery hours per engagement</th><td>120</td><td>85</td><td>60</td><td>Interview time dominates and does not compress</td></tr>
                  <tr><th scope="row">Direct cost per engagement</th><td>$800</td><td>$500</td><td>$300</td><td>Tooling and incidentals</td></tr>
                  <tr><th scope="row">Acquisition cost or effort</th><td>high</td><td>moderate</td><td>low</td><td>Referral-led; cost is time, not spend</td></tr>
                </tbody>
              </table>
              <p>Low and high cases are ranges for testing, not forecasts. No sale-readiness fee has been observed.</p>
            </div>
            <aside className="bl-disclosure"><strong>Economics boundary</strong><span>Modeled scenario, not observed performance or an earnings forecast. No sale-readiness fee has been observed; $12,000 and $16,250 are assumptions, not typical or achievable prices.</span></aside>
          </section>

          <section className="bl-chapter oe-band-raised oe-active-chapter bl-shell" id="sheet-04" aria-labelledby="h-04">
            <header className="bl-chapter__head"><p className="bl-chapter__number">04 / Guardrails</p><div><SectionMark name="test" /><h2 id="h-04">What should you test first?</h2><p>The first move costs nothing. It produces the one number this business turns on, and it tells you whether an owner cares.</p></div></header>
            <GuideNote step={5} title="What can you learn before you sell anything?"><p>Run the diagnostic for free, time it, and talk to the people who meet these owners years before a sale. Settle the licensing question before the first paid conversation.</p></GuideNote>
            <div className="bl-split">
              <div className="bl-anatomy"><h3>The first 30 days</h3><ol>
                <li><span>Build the readiness checklist and publish it. It is the credibility artifact and the delivery spine.</span></li>
                <li><span>Run one full diagnostic, unpaid, on a real business. Record the actual hours, and note which findings the owner had not already seen.</span></li>
                <li><span>Ask three brokers what they do today with listings they decline, and whether they would refer.</span></li>
                <li><span>Verify the licensing perimeter in your own state, in writing.</span></li>
              </ol>
              <p className="oe-page-note">Success looks like an owner recognising findings they had not seen and asking what remediation costs, and at least one adviser willing to refer.</p></div>
              <div className="bl-boundary-list oe-stop"><h3>Stop or redesign when</h3><ul>
                <li>The owner sees findings they had not seen and still will not pay.</li>
                <li>Brokers say they already do this work themselves, or advisers will not refer.</li>
                <li>Your measured hours make the fee unsellable.</li>
                <li>Your jurisdiction defines the brokerage line so tightly that fixed-fee preparation itself needs a licence.</li>
              </ul></div>
            </div>
            <aside className="bl-disclosure"><strong>Not legal advice</strong><span>Licensing varies by jurisdiction and no state is named here on purpose. Keep payment independent of any transaction, in the contract and in practice. Seek a professional the moment a question touches value, deal terms, tax or law.</span></aside>
          </section>
        </div>

        <section className="bl-chapter oe-band-inset bl-shell" id="episode" aria-labelledby="episode-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">Supporting material</p><div><h2 id="episode-title">Watch the investigation.</h2><p>The episode carries the argument, the evidence and the modeled arithmetic, including the parts that do not survive it.</p></div></header>
          <div className="oe-media">
            <div className="oe-media__watch"><WatchAction slug={operation.slug} /></div>
            <div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Episode</span><p>{operation.episodeTitle}</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Status</span><p>{episodeStatus(operation.slug)}</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Host</span><p>The host has no transaction experience, and the episode does not pretend otherwise.</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">AI disclosure</span><p>{AI_DISCLOSURE}</p></div>
            </div>
          </div>
        </section>

        <section className="bl-chapter oe-band-raised bl-shell" id="download" aria-labelledby="download-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">05 / Download</p><div><h2 id="download-title">Take the Operator Canvas with you.</h2><p>The print edition of this Canvas, transcribed from the locked version: the scope boundary and acceptance measure, the delivery system, the full model with low, base and high cases, the risk register, the 30-day test plan, the unknowns and every source note.</p></div></header>
          <aside className="bl-disclosure"><strong>Required disclosure</strong><span>Modeled scenario, not observed performance or an earnings forecast. Other figures are reported by their named sources and carry their hedges. Nothing here is legal, tax or financial advice, and nothing predicts what any business will sell for.</span></aside>
          <BlueprintRequestForm slug={operation.slug} />
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
