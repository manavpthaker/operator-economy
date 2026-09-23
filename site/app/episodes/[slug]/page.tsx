import { notFound, permanentRedirect } from 'next/navigation';
import { getOperation } from '../../lib/operations';

// /episodes/<slug> is the blueprint_url shape written into launch/links.json.
// Current episodes redirect to their Canvas page. Retired slugs are redirected home in next.config.mjs.
export default async function EpisodeRedirect({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (getOperation(slug)) permanentRedirect(`/businesses/${slug}`);
  notFound();
}
