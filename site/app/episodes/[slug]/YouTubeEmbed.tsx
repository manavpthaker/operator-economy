import s from './page.module.css';

function extractVideoId(url: string): string | null {
  try {
    const u = new URL(url);
    if (u.hostname === 'youtu.be') return u.pathname.slice(1) || null;
    if (u.hostname.endsWith('youtube.com')) {
      const v = u.searchParams.get('v');
      if (v) return v;
      const parts = u.pathname.split('/').filter(Boolean);
      if (parts[0] === 'embed' || parts[0] === 'shorts') return parts[1] ?? null;
    }
    return null;
  } catch {
    return null;
  }
}

export function YouTubeEmbed({ url, title }: { url: string; title: string }) {
  const id = extractVideoId(url);
  if (!id) return null;
  const src = `https://www.youtube-nocookie.com/embed/${id}?rel=0&modestbranding=1`;
  return (
    <div className={s.videoFrame}>
      <iframe
        src={src}
        title={title}
        loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowFullScreen
        referrerPolicy="strict-origin-when-cross-origin"
      />
    </div>
  );
}
