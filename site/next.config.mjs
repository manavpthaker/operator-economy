// Relaunch 2026-10: episodes №001-006 are retired from the site. Their pages, Blueprint PDFs and
// carousel redirect home. Redirects run before pages and /public files, so the old PDFs in
// public/ are no longer served even though they remain on disk and in git history.
const RETIRED_SLUGS = [
  'ai-implementation-consulting',
  'voice-agent-agency',
  'boring-automation-agency',
  'solo-design-agency',
  'too-small-to-bother',
  'direct-booking-recovery',
  'small-cohort-business',
];

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  turbopack: {
    root: process.cwd(),
  },
  async redirects() {
    return RETIRED_SLUGS.flatMap((slug) => [
      { source: `/episodes/${slug}`, destination: '/', permanent: true },
      { source: `/businesses/${slug}`, destination: '/', permanent: true },
      { source: `/blueprints/${slug}.pdf`, destination: '/', permanent: true },
      { source: `/carousels/${slug}.pdf`, destination: '/', permanent: true },
    ]);
  },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        ],
      },
    ];
  },
};

export default nextConfig;
