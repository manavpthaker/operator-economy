import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getOperation, OPERATIONS } from '../../lib/operations';
import { SaleReadinessPage } from './SaleReadinessPage';

export const dynamicParams = false;

export function generateStaticParams() {
  return OPERATIONS.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const operation = getOperation((await params).slug);
  if (!operation) return {};
  return {
    title: `${operation.name} · The Operator Economy`,
    description: operation.summary,
    openGraph: {
      title: operation.episodeTitle,
      description: operation.summary,
      images: [{ url: operation.thumbnail.src, width: operation.thumbnail.width, height: operation.thumbnail.height }],
    },
  };
}

export default async function BusinessPage({ params }: { params: Promise<{ slug: string }> }) {
  const operation = getOperation((await params).slug);
  if (!operation) notFound();
  return <SaleReadinessPage operation={operation} />;
}
