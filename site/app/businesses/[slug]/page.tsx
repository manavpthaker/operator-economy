import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { NewsletterBand } from '../../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../../components/SiteChrome';
import { getOperation, OPERATIONS, padOperationNumber } from '../../lib/operations';
import { DirectBookingPage } from './DirectBookingPage';

export function generateStaticParams() {
  return OPERATIONS.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const operation = getOperation((await params).slug);
  if (!operation) return {};
  return {
    title: `${operation.name} · The Operator Economy`,
    description: operation.summary,
  };
}

export default async function BusinessPage({ params }: { params: Promise<{ slug: string }> }) {
  const operation = getOperation((await params).slug);
  if (!operation) notFound();
  if (operation.slug === 'direct-booking-recovery') return <DirectBookingPage operation={operation} />;

  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="businesses" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="business-title">
          <div className="bl-episode-feature__intro">
            <h1 id="business-title">{operation.name}</h1>
            <p>{operation.summary}</p>
            <p className="oe-page-note">This business was published under the earlier V1 Blueprint format. It is not represented as a V2 Canvas.</p>
          </div>
          <figure className="oe-page-hero__accent" aria-hidden="true"><img src="/illustration/system/operator-loop.svg" alt="" width="480" height="320" /></figure>
        </section>

        <section className="oe-section oe-band-inset bl-shell" aria-labelledby="record-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">Operation №{padOperationNumber(operation.number)}</p><div><h2 id="record-title">The operation and the episode are different titles.</h2><p>The operation names the work you would own. The episode title packages the investigation for video.</p></div></header>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Operation</span><p>{operation.name}</p><span className="oe-class">Stable name</span></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Buyer</span><p>{operation.audience}</p><span className="oe-class">V1 record</span></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Offer</span><p>{operation.offer}</p><span className="oe-class">V1 record</span></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Episode</span><p>{operation.episodeTitle}</p><span className="oe-class">Editorial title</span></div>
        </section>

        <section className="bl-chapter bl-shell" aria-labelledby="watch-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">Investigation</p><div><h2 id="watch-title">Watch the episode.</h2><p>The episode carries the original V1 argument and evidence package.</p></div></header>
          <div className="oe-media"><a className="oe-video" href={operation.youtubeUrl} target="_blank" rel="noreferrer"><span>Watch №{padOperationNumber(operation.number)} on YouTube</span></a><div><div className="bl-ledger-row"><span className="bl-ledger-row__name">Sources</span><p>{operation.sources} in the published package</p></div><div className="bl-ledger-row"><span className="bl-ledger-row__name">Published</span><p>{operation.published}</p></div></div></div>
        </section>

        <section className="bl-chapter oe-band-raised bl-shell" aria-labelledby="download-title">
          <header className="bl-chapter__head"><p className="bl-chapter__number">Legacy Blueprint</p><div><h2 id="download-title">Download the original working document.</h2><p>The PDF is the historical companion to this V1 episode. It is not a V2 Canvas.</p></div></header>
          <a className="oe-direct-download" href={operation.pdfUrl}>Download the legacy Blueprint PDF</a>
          <p className="oe-page-note">Downloading does not subscribe you to the newsletter.</p>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
