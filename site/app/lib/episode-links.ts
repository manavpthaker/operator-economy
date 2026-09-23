import { readFileSync } from 'node:fs';
import path from 'node:path';

// THE ONLY PLACE THE SITE GETS AN EPISODE URL.
//
// Content OS hard rule 3: only studio/originate/<slug>/launch/links.json may originate an episode
// URL. It is written by the YouTube upload. This module reads it at build time (pages are static),
// so after the upload writes a real URL the site must be rebuilt and redeployed to pick it up.
//
// Until links.json carries a real YouTube URL (and is not a dry run), every page shows the
// premiere state instead of a watch link. Nothing here, and nothing anywhere else in site/, may
// hand-type a video URL.

export type EpisodeLinks = {
  /** A verified https YouTube URL, or null while the upload is pending. */
  episodeUrl: string | null;
  /** Display form of the scheduled premiere, e.g. "Mon Oct 5, 11:00 ET". */
  premiereLabel: string | null;
  /** ISO date of the premiere (YYYY-MM-DD), when known. */
  premiereDate: string | null;
};

type LinksJson = {
  slug?: string;
  episode_url?: string;
  episode_publish_et?: string;
  dry_run?: boolean;
};

const YOUTUBE_URL = /^https:\/\/(youtu\.be\/[A-Za-z0-9_-]{6,}|(www\.)?youtube\.com\/(watch\?v=|live\/|shorts\/)[A-Za-z0-9_-]{6,})/;
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function linksPath(slug: string): string {
  // site/ is a sibling of studio/ in the operator-economy repo; Vercel clones the whole repo.
  return path.join(process.cwd(), '..', 'studio', 'originate', slug, 'launch', 'links.json');
}

function formatPremiere(raw: string | undefined): { label: string | null; date: string | null } {
  const match = raw?.match(/^(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}:\d{2})\s*ET$/);
  if (!match) return { label: null, date: null };
  const [, y, m, d, time] = match;
  const when = new Date(Date.UTC(Number(y), Number(m) - 1, Number(d)));
  return {
    label: `${DAYS[when.getUTCDay()]} ${MONTHS[when.getUTCMonth()]} ${Number(d)}, ${time} ET`,
    date: `${y}-${m}-${d}`,
  };
}

export function getEpisodeLinks(slug: string): EpisodeLinks {
  let data: LinksJson = {};
  try {
    data = JSON.parse(readFileSync(linksPath(slug), 'utf8')) as LinksJson;
  } catch {
    return { episodeUrl: null, premiereLabel: null, premiereDate: null };
  }
  const { label, date } = formatPremiere(data.episode_publish_et);
  const url = (data.episode_url ?? '').trim();
  const live = data.slug === slug && data.dry_run !== true && YOUTUBE_URL.test(url);
  return { episodeUrl: live ? url : null, premiereLabel: label, premiereDate: date };
}
