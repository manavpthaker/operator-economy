import type { Metadata } from 'next';
import './styles/globals.css';

export const metadata: Metadata = {
  title: 'The Operator Economy',
  description:
    'Evidence-led business investigations and working documents for people deciding what to test, revise, or reject.',
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
      <head>
        <link rel="preload" href="/fonts/boska-700.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
        <link rel="preload" href="/fonts/boska-700-italic.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
        <link rel="preload" href="/fonts/zodiak-700.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
        <link rel="preload" href="/fonts/supreme-400.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
      </head>
      <body data-oe-theme="boundary-ledger">{children}</body>
    </html>
  );
}
