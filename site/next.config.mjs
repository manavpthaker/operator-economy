/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  turbopack: {
    root: process.cwd(),
  },
  // Five V1 businesses were removed from the site on 2026-10-12. Their videos had been set private
  // in the 2026-09-23 relaunch and they held the numbers the relaunch reassigned. Both the
  // /businesses and the legacy /episodes form of each slug redirect to home so no live URL breaks.
  // Keep in step with RETIRED_SLUGS in app/lib/operations.ts.
  async redirects() {
    const retired = [
      'ai-implementation-consulting',
      'voice-agent-agency',
      'boring-automation-agency',
      'solo-design-agency',
      'direct-booking-recovery',
    ];
    return retired.flatMap((slug) => [
      { source: `/businesses/${slug}`, destination: '/', permanent: true },
      { source: `/episodes/${slug}`, destination: '/', permanent: true },
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
