import Image from 'next/image';
import { getEpisodeLinks } from '../lib/episode-links';

/** Watch link when links.json has a real URL; otherwise the premiere state. Never a guessed URL. */
export function WatchAction({ slug, label = 'Watch the episode' }: { slug: string; label?: string }) {
  const { episodeUrl, premiereLabel } = getEpisodeLinks(slug);
  if (episodeUrl) {
    return (
      <a className="bl-action" href={episodeUrl} target="_blank" rel="noreferrer">
        {label}<span className="oe-sr"> on YouTube (opens in new tab)</span>
      </a>
    );
  }
  return (
    <span className="oe-premiere" role="status">
      <span className="oe-premiere__dot" aria-hidden="true" />
      {premiereLabel ? `Premieres ${premiereLabel}` : 'Premiere date to be announced'}
    </span>
  );
}

/** Short status string for dockets and ledger rows. */
export function episodeStatus(slug: string): string {
  const { episodeUrl, premiereLabel } = getEpisodeLinks(slug);
  if (episodeUrl) return 'Live on YouTube';
  return premiereLabel ? `Premieres ${premiereLabel}` : 'Premiere to be announced';
}

/** The thumbnail, linked to the episode when it exists. */
export function EpisodeThumbnail({
  slug,
  thumbnail,
  sizes,
  priority,
}: {
  slug: string;
  thumbnail: { src: string; width: number; height: number; alt: string };
  sizes: string;
  priority?: boolean;
}) {
  const { episodeUrl } = getEpisodeLinks(slug);
  const img = (
    <Image
      src={thumbnail.src}
      alt={thumbnail.alt}
      width={thumbnail.width}
      height={thumbnail.height}
      sizes={sizes}
      priority={priority}
    />
  );
  return episodeUrl ? (
    <a href={episodeUrl} target="_blank" rel="noreferrer" className="oe-thumb-link">
      {img}
      <span className="oe-sr"> Watch on YouTube (opens in new tab)</span>
    </a>
  ) : (
    img
  );
}
