import React from 'react';

/**
 * Badge — small-caps annotation label / status tag.
 * Reads like a drafting stamp, not a pill. Tones map to brand
 * semantics: neutral, accent (blue), gold (key), positive (sage),
 * negative (brick). Set `dot` for a status marker.
 */
export function Badge({
  tone = 'neutral',
  dot = false,
  children,
  style,
  ...props
}) {
  const tones = {
    neutral:  { color: 'var(--ink-700)',   border: 'var(--border-strong)', bg: 'var(--paper-0)' },
    accent:   { color: 'var(--drafting-blue)', border: 'var(--drafting-blue)', bg: 'var(--blue-tint)' },
    gold:     { color: 'var(--gold-700)',  border: 'var(--gold-500)', bg: 'var(--gold-tint)' },
    positive: { color: 'var(--sage-700)',  border: 'var(--sage-500)', bg: 'transparent' },
    negative: { color: 'var(--negative)',  border: 'var(--negative)', bg: 'transparent' },
  };
  const t = tones[tone] || tones.neutral;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        padding: '3px 8px',
        fontFamily: 'var(--font-sans)',
        fontWeight: 'var(--w-semibold)',
        fontSize: 'var(--text-3xs)',
        textTransform: 'uppercase',
        letterSpacing: 'var(--tracking-label)',
        color: t.color,
        background: t.bg,
        border: `1px solid ${t.border}`,
        borderRadius: 'var(--radius-xs)',
        lineHeight: 1,
        whiteSpace: 'nowrap',
        ...style,
      }}
      {...props}
    >
      {dot && (
        <span
          style={{
            width: '6px',
            height: '6px',
            borderRadius: 'var(--radius-pill)',
            background: t.color,
            flex: '0 0 auto',
          }}
        />
      )}
      {children}
    </span>
  );
}
