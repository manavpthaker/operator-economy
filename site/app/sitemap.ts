import type { MetadataRoute } from 'next';
import { OPERATIONS } from './lib/operations';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = 'https://theoperatoreconomy.com';
  return [
    { url: base, changeFrequency: 'weekly', priority: 1 },
    ...OPERATIONS.map((operation) => ({
      url: `${base}/businesses/${operation.slug}`,
      changeFrequency: 'weekly' as const,
      priority: 0.9,
    })),
    { url: `${base}/businesses`, changeFrequency: 'weekly', priority: 0.7 },
    { url: `${base}/method`, changeFrequency: 'monthly', priority: 0.6 },
    { url: `${base}/about`, changeFrequency: 'monthly', priority: 0.6 },
    { url: `${base}/newsletter`, changeFrequency: 'monthly', priority: 0.5 },
    { url: `${base}/privacy`, changeFrequency: 'yearly', priority: 0.3 },
  ];
}
