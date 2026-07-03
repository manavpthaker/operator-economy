import type { Metadata } from 'next';
import './styles/globals.css';

export const metadata: Metadata = {
  title: 'The Operator Economy — Businesses one experienced person can build.',
  description:
    "Every Monday: one real business one experienced person can build and run — the companies proving it works, the exact stack and what it costs, the honest math. Plus the free Operator Blueprint to build from.",
  metadataBase: new URL('https://theoperatoreconomy.com'),
  openGraph: {
    title: 'The Operator Economy',
    description:
      "You can build it now. We show you what's worth building.",
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
