import React from 'react';

/**
 * CitationChip — THE signature element. An on-screen source chip
 * shown every time a number appears: `SOURCE: Sacra · Apr 2026`.
 * Compliance asset, trust asset, and brand asset in one. Mono.
 * `estimate` flags a marked estimate rather than a hard source.
 * `onInk` renders the video lower-third treatment on dark surfaces.
 */
export function CitationChip({
  source,
  date,
  estimate = false,
  onInk = false,
  style,
  ...props
}) {
  const label = estimate ? 'ESTIMATE' : 'SOURCE';
  const accent = onInk ? 'var(--gold-bright)' : estimate ? 'var(--gold-700)' : 'var(--drafting-blue)';

  const base = onInk
    ? {
        background: 'rgba(26,26,26,0.82)',
        color: 'var(--text-on-ink)',
        border: '1px solid rgba(245,240,230,0.16)',
        backdropFilter: 'blur(2px)',
      }
    : {
        background: 'var(--paper-0)',
        color: 'var(--ink-700)',
        border: '1px solid var(--border)',
      };

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        padding: '4px 10px',
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-2xs)',
        fontWeight: 'var(--w-mono)',
        letterSpacing: 'var(--tracking-mono)',
        borderRadius: 'var(--radius-xs)',
        borderLeft: `2px solid ${accent}`,
        lineHeight: 1.3,
        whiteSpace: 'nowrap',
        ...base,
        ...style,
      }}
      {...props}
    >
      <span
        style={{
          fontSize: 'var(--text-3xs)',
          fontWeight: 'var(--w-mono)',
          letterSpacing: 'var(--tracking-caps)',
          color: accent,
        }}
      >
        {label}
      </span>
      <span style={{ opacity: onInk ? 0.9 : 1 }}>
        {source}{date ? ` · ${date}` : ''}
      </span>
    </span>
  );
}
