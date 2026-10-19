import { NewsletterBand } from '../../components/NewsletterForm';
import { SiteFooter, SiteHeader } from '../../components/SiteChrome';
import { padOperationNumber, type Operation } from '../../lib/operations';

/**
 * The page for a V2 Canvas episode.
 *
 * The generic business page describes a V1 legacy blueprint in its own copy, so a Canvas episode
 * rendered through it would tell the reader it is something it is not. This component carries the
 * Canvas language instead: the Canvas is the working document, the episode is the investigation.
 *
 * It also handles an episode whose video is not live yet. Only `launch/links.json` may originate an
 * episode URL, so `youtubeUrl` is empty between the site going up and the upload running. In that
 * window the page states the publication date rather than linking nowhere.
 */
export function CanvasPage({ operation }: { operation: Operation }) {
  const num = padOperationNumber(operation.number);
  const live = operation.youtubeUrl.length > 0;

  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="businesses" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="business-title">
          <div className="bl-episode-feature__intro">
            <h1 id="business-title">{operation.name}</h1>
            <p>{operation.summary}</p>
          </div>
          <figure className="oe-page-hero__accent" aria-hidden="true">
            <img src="/illustration/system/operator-loop.svg" alt="" width="480" height="320" />
          </figure>
        </section>

        <section className="oe-section oe-band-inset bl-shell" aria-labelledby="record-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">Operation №{num}</p>
            <div>
              <h2 id="record-title">The operation and the episode are different titles.</h2>
              <p>The operation names the work you would own. The episode title packages the investigation for video.</p>
            </div>
          </header>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Operation</span><p>{operation.name}</p><span className="oe-class">Stable name</span></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Buyer</span><p>{operation.audience}</p><span className="oe-class">Canvas §2</span></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Offer</span><p>{operation.offer}</p><span className="oe-class">Canvas §4</span></div>
          <div className="bl-ledger-row"><span className="bl-ledger-row__name">Episode</span><p>{operation.episodeTitle}</p><span className="oe-class">Editorial title</span></div>
        </section>

        <section className="bl-chapter bl-shell" aria-labelledby="watch-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">Investigation</p>
            <div>
              <h2 id="watch-title">{live ? 'Watch the episode.' : 'The episode is on its way.'}</h2>
              <p>
                {live
                  ? 'The episode works the business down to the number that decides it.'
                  : 'It works the business down to the number that decides it. The Canvas below is already complete.'}
              </p>
            </div>
          </header>
          <div className="oe-media">
            {live ? (
              <a className="oe-video" href={operation.youtubeUrl} target="_blank" rel="noreferrer">
                <span>Watch №{num} on YouTube</span>
              </a>
            ) : (
              <p className="oe-page-note">Publishing {operation.published}.</p>
            )}
            <div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Sources</span><p>{operation.sources} in the published package</p></div>
              <div className="bl-ledger-row"><span className="bl-ledger-row__name">Published</span><p>{operation.published}</p></div>
            </div>
          </div>
        </section>

        <section className="bl-chapter oe-band-raised bl-shell" aria-labelledby="download-title">
          <header className="bl-chapter__head">
            <p className="bl-chapter__number">Operator Canvas</p>
            <div>
              <h2 id="download-title">Download the Operator Canvas.</h2>
              <p>
                The working document behind the episode: the buyer, the offer, the delivery loop, the
                stack, the economics model and what is still unknown. Every modelled figure carries
                its hedge on the page with the number.
              </p>
            </div>
          </header>
          <a className="oe-direct-download" href={operation.pdfUrl}>Download the Operator Canvas (PDF)</a>
          <p className="oe-page-note">Downloading does not subscribe you to the newsletter.</p>
        </section>

        <NewsletterBand />
      </main>
      <SiteFooter />
    </div>
  );
}
