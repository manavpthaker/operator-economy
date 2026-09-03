import { notFound, permanentRedirect } from 'next/navigation';
import { getOperation } from '../../lib/operations';

export default async function LegacyEpisodeRedirect({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (slug === 'too-small-to-bother') permanentRedirect('/method#why');
  if (getOperation(slug)) permanentRedirect(`/businesses/${slug}`);
  notFound();
}
