// The public business registry. The 2026-10 relaunch starts fresh: internal EP007 is public №001; earlier operations
// (№001-006) were unregistered on 2026-09-23 and their URLs redirect home (next.config.mjs).
// Their source remains in git history.
//
// No episode URL lives here. Watch links come only from launch/links.json via ./episode-links.ts.

export type OperationArtifact = 'canvas';

export type Operation = {
  slug: string;
  name: string;
  audience: string;
  offer: string;
  /** One line: what the business is, including its scope boundary. */
  summary: string;
  episodeTitle: string;
  /** Scheduled release, display form. */
  published: string;
  pdfUrl: string;
  thumbnail: { src: string; width: number; height: number; alt: string };
  artifact: OperationArtifact;
};

export const OPERATIONS: Operation[] = [
  {
    slug: 'exit-readiness-prep',
    name: 'Sale-Readiness Practice',
    audience: 'Owner-run businesses',
    offer: 'Fixed-fee readiness engagement',
    summary:
      'Get owner-run businesses ready to be inspected by a buyer, for a fixed fee that never depends on a sale.',
    episodeTitle: 'The One-Person Business That Gets Companies Ready for a Sale',
    published: 'Oct 2026',
    pdfUrl: '/blueprints/exit-readiness-prep.pdf',
    thumbnail: {
      src: '/episodes/exit-readiness-prep/thumbnail.jpg',
      width: 1920,
      height: 1080,
      alt: 'Episode thumbnail. A business owner sits across a workshop table from a buyer holding a pen over a blank sheet, while the presenter points back at her. Headline: Help her sell.',
    },
    artifact: 'canvas',
  },
];

export const LATEST = OPERATIONS[0];

export function getOperation(slug: string): Operation | undefined {
  return OPERATIONS.find((operation) => operation.slug === slug);
}
