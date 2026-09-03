export type OperationArtifact = 'canvas' | 'legacy_blueprint';

export type Operation = {
  number: number;
  slug: string;
  name: string;
  audience: string;
  offer: string;
  summary: string;
  episodeTitle: string;
  youtubeUrl: string;
  sources: number;
  published: string;
  pdfUrl: string;
  artifact: OperationArtifact;
};

export const OPERATIONS: Operation[] = [
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
  },
];

export function getOperation(slug: string): Operation | undefined {
  return OPERATIONS.find((operation) => operation.slug === slug);
}

export function padOperationNumber(number: number): string {
  return String(number).padStart(3, '0');
}
