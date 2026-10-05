import type { MetadataRoute } from 'next';
import { LIVE_OPERATIONS } from './lib/operations';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = 'https://theoperatoreconomy.com';
  return [
    { url: base, changeFrequency: 'weekly', priority: 1 },
    { url: `${base}/businesses`, changeFrequency: 'weekly', priority: 0.9 },
    { url: `${base}/method`, changeFrequency: 'monthly', priority: 0.8 },
    { url: `${base}/privacy`, changeFrequency: 'yearly', priority: 0.3 },
    ...LIVE_OPERATIONS.map((operation) => ({
      url: `${base}/businesses/${operation.slug}`,
      changeFrequency: 'monthly' as const,
      priority: 0.8,
    })),
  ];
}
