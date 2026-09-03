import type { Metadata } from 'next';
import Link from 'next/link';
import { NewsletterBand } from '../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../components/SiteChrome';

export const metadata: Metadata = {
  title: 'Method · The Operator Economy',
  description: 'How an Operator Canvas separates evidence, assumptions, unknowns, economics, and the first test.',
};

const evidenceClasses = [
  ['Observed', 'A sourced fact. The receipt names who measured or reported it.'],
  ['Parallel', 'Evidence from a neighboring model. The Canvas states what transfers and what remains unproven.'],
  ['Modeled', 'An assumption with its arithmetic shown. It is not presented as observed performance.'],
  ['Unknown', 'An open question. The Canvas keeps it visible and says how the first test could resolve it.'],
] as const;

export default function MethodPage() {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="method" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="page-title">
          <div className="bl-episode-feature__intro">
            <h1 id="page-title">A way to decide before you commit.</h1>
            <p>An Operator Canvas turns a business opportunity into a decision you can inspect. It shows what is known, what is assumed, what one person would have to run, and what to test first.</p>
          </div>
          <figure className="oe-page-hero__accent" aria-hidden="true">
            <img src="/illustration/system/evidence-pin.svg" alt="" width="480" height="320" />
          </figure>
        </section>

        <nav className="bl-anchor-nav bl-shell" aria-label="On this page">
          <a href="#why">Why this exists</a>
          <a href="#decisions">What the Canvas answers</a>
          <a href="#evidence-classes">How claims are marked</a>
          <a href="#process">How it is made</a>
          <a href="#standard">What we will not claim</a>
        </nav>

        <section className="oe-trust oe-trust--mineral bl-shell" id="why" aria-labelledby="why-title">
          <p className="bl-chapter__number">Why this exists</p>
          <h2 id="why-title">AI made more businesses possible. It did not make them worth building.</h2>
          <p>One person can now deliver work that once required a team. That changes the minimum viable size of a business, but it does not prove demand, defensibility, capacity, or economics. The Operator Canvas exists to test those questions before the story makes the opportunity feel inevitable.</p>
        </section>

        <section className="oe-value bl-shell" id="decisions" aria-labelledby="decisions-title">
          <div className="oe-value__intro">
            <p className="bl-chapter__number">What the Canvas answers</p>
            <h2 id="decisions-title">Three decisions, in a useful order.</h2>
            <p>The Canvas is not a score or a promise. It gives you enough structure to test, revise, or reject the opportunity.</p>
          </div>
          <ol className="oe-decision-list">
            <li><span>01</span><div><strong>Is the problem worth solving?</strong><p>Who has the problem, why it matters now, what the operator sells, and what result the buyer is purchasing.</p></div></li>
            <li><span>02</span><div><strong>Can one operator deliver it?</strong><p>The recurring workflow, tools, human judgment, price, costs, capacity, and customer count.</p></div></li>
            <li><span>03</span><div><strong>What should I test first?</strong><p>The weakest assumption, a bounded 30-day test, a success signal, and a stop condition.</p></div></li>
          </ol>
        </section>

        <section className="oe-section oe-band-inset bl-shell" id="evidence-classes" aria-labelledby="evidence-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">How claims are marked</p>
            <div>
              <h2 id="evidence-title">Facts, transfers, assumptions, and unknowns stay distinct.</h2>
              <p>The label beside a claim tells you what kind of support it has. The source or arithmetic sits with the claim, not in a distant appendix.</p>
            </div>
          </header>
          <div aria-label="Evidence classes">
            {evidenceClasses.map(([name, description]) => (
              <div className="bl-ledger-row" key={name}>
                <span className="bl-ledger-row__name">{name}</span>
                <p>{description}</p>
                <span className="oe-class">{name}</span>
              </div>
            ))}
          </div>
          <aside className="bl-evidence-receipt" style={{ marginTop: 'var(--bl-space-6)' }}>
            <span className="bl-evidence-receipt__source">Observed · named source</span>
            <p><strong>A source receipt answers three questions:</strong> who published the evidence, what it supports, and what it does not establish.</p>
            <span className="bl-evidence-receipt__count">Inspectable</span>
          </aside>
        </section>

        <section className="oe-section bl-shell" id="process" aria-labelledby="process-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">How it is made</p>
            <div><h2 id="process-title">Research first. Canvas second. Story third.</h2><p>A compelling story cannot rescue an incomplete business model. The model is reviewed before the episode is produced.</p></div>
          </header>
          <div className="bl-anatomy"><ol>
            <li><span><strong>Research the opportunity.</strong> Identify the buyer, problem, delivery path, economics, risks, and a testable first offer.</span></li>
            <li><span><strong>Build and challenge the Canvas.</strong> Attach evidence classes, expose unknowns, test capacity, and reject the opportunity if a required part does not hold.</span></li>
            <li><span><strong>Lock the model.</strong> Material claims, assumptions, and disclosures are fixed before narration and production begin.</span></li>
            <li><span><strong>Publish the investigation.</strong> The episode tells the story. The Canvas lets the reader inspect and use the model.</span></li>
          </ol></div>
        </section>

        <section className="oe-trust oe-trust--mineral bl-shell" id="standard" aria-labelledby="standard-title">
          <p className="bl-chapter__number">The standard</p>
          <h2 id="standard-title">No income promises. No hidden assumptions. No polished answer where the evidence is incomplete.</h2>
          <p>Modeled economics are not observed performance or an earnings forecast. A failing case stays failed. A material edit creates a new revision. The public page contains everything you need to judge the opportunity; a PDF adds detail and print utility.</p>
        </section>

        <section className="oe-section oe-band-inset bl-shell" id="versioning" aria-labelledby="versioning-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">How revisions work</p>
            <div><h2 id="versioning-title">The current model never erases the prior one.</h2><p>A material Canvas change creates a new dated revision. Its source, public data, and PDF each receive their own full hash. Earlier revisions remain available and clearly labeled.</p></div>
          </header>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Current library</span><p>The published businesses currently use the earlier Blueprint format. No V2 Canvas is represented as live.</p><span className="oe-class">Legacy</span></div>
          <p style={{ marginTop: 'var(--bl-space-5)' }}><Link className="bl-text-link" href="/businesses">Browse businesses</Link></p>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
