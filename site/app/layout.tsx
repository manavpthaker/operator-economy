import type { Metadata } from 'next';
import { preload } from 'react-dom';
import './styles/globals.css';

export const metadata: Metadata = {
  title: 'The Operator Economy',
  description:
    'The Operator Economy shows experienced professionals how to build, own and operate a business of one using AI.',
  metadataBase: new URL('https://theoperatoreconomy.com'),
  openGraph: {
    title: 'The Operator Economy',
    description: 'Build, own and operate a business of one using AI. New episodes Mondays.',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  preload('/fonts/boska-700.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' });
  preload('/fonts/boska-700-italic.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' });
  preload('/fonts/zodiak-700.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' });
  preload('/fonts/supreme-400.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' });

  return (
    <html lang="en">
      <body data-oe-theme="boundary-ledger">{children}</body>
    </html>
  );
}
