import episodeUrls from '../../data/episode-urls.json';

export type OperationArtifact = 'canvas' | 'legacy_blueprint';

export type Operation = {
  number: number;
  slug: string;
  name: string;
  audience: string;
  offer: string;
  summary: string;
  /** The decision question the home page asks on this operation's behalf. */
  question: string;
  episodeTitle: string;
  youtubeUrl: string;
  sources: number;
  published: string;
  pdfUrl: string;
  artifact: OperationArtifact;
};

/**
 * Episode URLs come from the registry, never from this file.
 *
 * `site/data/episode-urls.json` is written by `studio/scripts/originate/publish.py`, which
 * copies each URL out of `studio/originate/<slug>/launch/links.json` — the only place an
 * episode URL may originate. Launch day is that script writing one value here.
 *
 * An operation whose episode has not published resolves to '', which is the pre-publish
 * switch every surface reads: `CanvasPage` and the home page's `latestIsLive`.
 */
const EPISODE_URLS = episodeUrls.episodes as Record<string, { url?: string } | undefined>;

function episodeUrl(slug: string): string {
  return EPISODE_URLS[slug]?.url ?? '';
}

const OPERATION_RECORDS: Omit<Operation, 'youtubeUrl'>[] = [
  // The relaunch of 2026-09-23 restarted public numbering and set every pre-EP007 video private.
  // The five V1 businesses that used to sit here were removed on 2026-10-12 (owner decision): they
  // all linked to videos nobody can watch, and they held the numbers the relaunch reassigned.
  // Their slugs redirect to home in next.config.mjs so no live URL breaks.
  {
    number: 2,
    slug: 'direct-booking-practice',
    name: 'A Direct-Booking Practice',
    audience: 'Independent hotels, 20 to 40 rooms',
    offer: 'Fixed-fee audit, then a monthly retainer',
    summary:
      "Help a small hotel get its returning guests to book direct, instead of paying a booking site to meet them again.",
    question: "Could one operator get a small hotel's returning guests to book direct?",
    episodeTitle: 'The One-Person Business That Gets Small Hotels Booking Direct',
    sources: 37,
    published: 'Oct 2026',
    pdfUrl: '/canvas/operator-canvas-002.pdf',
    artifact: 'canvas',
  },
  {
    number: 1,
    slug: 'exit-readiness-prep',
    name: 'A Sale-Readiness Practice',
    audience: 'Owner-run businesses preparing to sell',
    offer: 'Fixed-fee readiness engagement',
    summary:
      'Help an owner get a business ready to sell years before a buyer shows up, by finding what the business cannot do without them.',
    question: 'Could one operator get a business ready to sell years before a buyer shows up?',
    episodeTitle: 'The One-Person Business That Gets Companies Ready for a Sale',
    sources: 16,
    published: 'Oct 2026',
    pdfUrl: '/canvas/operator-canvas-001.pdf',
    artifact: 'canvas',
  },
];

export const OPERATIONS: Operation[] = OPERATION_RECORDS.map((record) => ({
  ...record,
  youtubeUrl: episodeUrl(record.slug),
}));

// Slugs removed in the 2026-10-12 cleanup. next.config.mjs redirects each to home; kept here so a
// reader of this file can see what the redirects are for without digging through the config.
export const RETIRED_SLUGS = [
  'ai-implementation-consulting',
  'voice-agent-agency',
  'boring-automation-agency',
  'solo-design-agency',
  'direct-booking-recovery',
] as const;

export function getOperation(slug: string): Operation | undefined {
  return OPERATIONS.find((operation) => operation.slug === slug);
}

export function padOperationNumber(number: number): string {
  return String(number).padStart(3, '0');
}
