export type OperationArtifact = 'canvas' | 'legacy_blueprint';

// The 2026-10 relaunch starts the public count again: internal EP007 is public №001. The earlier
// series is archived: its videos are private, so it is unlisted and its pages carry no watch link.
// A live operation's watch link comes only from launch/links.json (lib/episode-links.ts), never from here.
export type Operation = {
  number: number;
  slug: string;
  name: string;
  audience: string;
  offer: string;
  summary: string;
  episodeTitle: string;
  /** Earlier series only; the video is now private and the URL is kept for the record. */
  youtubeUrl?: string;
  sources?: number;
  published: string;
  pdfUrl: string;
  artifact: OperationArtifact;
  archived?: boolean;
  /** Homepage docket question. */
  question?: string;
  thumbnail?: { src: string; width: number; height: number; alt: string };
};

export const OPERATIONS: Operation[] = [
  {
    // Internal EP009. Not EP006's direct-booking-recovery (archived below, with its own links.json).
    number: 2,
    slug: 'direct-booking-practice',
    name: 'Direct-Booking Practice',
    audience: 'Small independent hotels',
    offer: 'Fixed-fee audit, then a retainer',
    summary:
      'Help small independent hotels get returning guests to book direct, instead of paying a booking site to meet them again.',
    episodeTitle: 'The One-Person Business That Gets Small Hotels Booking Direct',
    published: 'Oct 2026',
    pdfUrl: '/blueprints/direct-booking-practice.pdf',
    artifact: 'canvas',
    question:
      'Could one operator help a small hotel keep its returning guests, for a fee priced under what the property could recover?',
    thumbnail: {
      src: '/episodes/direct-booking-practice/thumbnail.jpg',
      width: 1920,
      height: 1080,
      alt: 'Episode thumbnail. An innkeeper behind a wooden front desk hands a room key to a departing guest, while the presenter stands beside her looking at the camera. Headline: Help her keep them.',
    },
  },
  {
    number: 1,
    slug: 'exit-readiness-prep',
    name: 'Sale-Readiness Practice',
    audience: 'Owner-run businesses',
    offer: 'Fixed-fee readiness engagement',
    summary:
      'Get owner-run businesses ready to be inspected by a buyer, for a fixed fee that never depends on a sale.',
    episodeTitle: 'The One-Person Business That Gets Companies Ready for a Sale',
    published: 'Oct 2026',
    pdfUrl: '/blueprints/exit-readiness-prep.pdf',
    artifact: 'canvas',
    question: 'Could one operator get a business ready for a buyer, and be paid a fixed fee for it?',
    thumbnail: {
      src: '/episodes/exit-readiness-prep/thumbnail.jpg',
      width: 1920,
      height: 1080,
      alt: 'Episode thumbnail. A business owner sits across a workshop table from a buyer holding a pen over a blank sheet, while the presenter points back at her. Headline: Help her sell.',
    },
  },
  {
    number: 6,
    slug: 'direct-booking-recovery',
    name: 'Direct Booking Recovery',
    audience: 'Independent hotels',
    offer: 'Recovery setup',
    summary: 'Help independent hotels turn OTA guests into direct repeat customers.',
    episodeTitle: 'Hotels pay 30% to book their own rooms',
    youtubeUrl: 'https://youtu.be/pOoQLaSyUGQ',
    sources: 9,
    published: 'Aug 2026',
    pdfUrl: '/blueprints/direct-booking-recovery.pdf',
    artifact: 'legacy_blueprint',
    archived: true,
  },
  {
    number: 4,
    slug: 'solo-design-agency',
    name: 'Solo Design Studio',
    audience: 'Specialist service buyers',
    offer: 'Subscription design',
    summary: 'Sell and deliver focused design work with a deliberately small operating model.',
    episodeTitle: 'The solo design agency',
    youtubeUrl: 'https://youtu.be/H8AmNEaKrfs',
    sources: 12,
    published: 'Aug 2026',
    pdfUrl: '/blueprints/solo-design-agency.pdf',
    artifact: 'legacy_blueprint',
    archived: true,
  },
  {
    number: 3,
    slug: 'boring-automation-agency',
    name: 'Workflow Automation Retainer',
    audience: 'Small businesses',
    offer: 'Managed workflow reliability',
    summary: 'Build and maintain the workflows that move data between the systems a business already uses.',
    episodeTitle: 'The boring-automation agency',
    youtubeUrl: 'https://youtu.be/tvlVy6sIoYo',
    sources: 6,
    published: 'Jul 2026',
    pdfUrl: '/blueprints/boring-automation-agency.pdf',
    artifact: 'legacy_blueprint',
    archived: true,
  },
  {
    number: 2,
    slug: 'voice-agent-agency',
    name: 'Voice Booking Operator',
    audience: 'Local service businesses',
    offer: 'Missed-call recovery',
    summary: 'Help local businesses capture missed calls and turn qualified conversations into appointments.',
    episodeTitle: 'The voice-agent agency',
    youtubeUrl: 'https://youtu.be/CFuVAwc2yzs',
    sources: 11,
    published: 'Jul 2026',
    pdfUrl: '/blueprints/voice-agent-agency.pdf',
    artifact: 'legacy_blueprint',
    archived: true,
  },
  {
    number: 1,
    slug: 'ai-implementation-consulting',
    name: 'AI Implementation Partner',
    audience: 'One familiar vertical',
    offer: 'Implementation service',
    summary: 'Install a small set of useful AI tools inside a vertical you already understand.',
    episodeTitle: 'AI implementation as a service',
    youtubeUrl: 'https://youtu.be/cXC4lYRu_Gg',
    sources: 8,
    published: 'Jul 2026',
    pdfUrl: '/blueprints/ai-implementation-consulting.pdf',
    artifact: 'legacy_blueprint',
    archived: true,
  },
];

export const ARCHIVED_NOTE =
  'This episode belongs to the earlier series and is no longer public on YouTube. The working document below remains available.';

/** The current series: listed, featured and in the sitemap. */
export const LIVE_OPERATIONS = OPERATIONS.filter((operation) => !operation.archived);

export function getOperation(slug: string): Operation | undefined {
  return OPERATIONS.find((operation) => operation.slug === slug);
}

export function padOperationNumber(number: number): string {
  return String(number).padStart(3, '0');
}
