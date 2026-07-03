import React from 'react';

/**
 * SheetHeader — chapter card styled as a drawing sheet:
 * "SHEET 2 OF 5 — UNIT ECONOMICS". Used for video chapter cards,
 * LinkedIn carousel sheets, and blueprint section dividers.
 * `onInk` for the dark video treatment.
 */
export function SheetHeader({
  sheet = 2,
  total = 5,
  title,
  subtitle,
  onInk = false,
  style,
  ...props
}) {
  const strong = onInk ? 'var(--text-on-ink)' : 'var(--ink-900)';
  const muted = onInk ? 'var(--text-on-ink-muted)' : 'var(--ink-500)';
  const rule = onInk ? 'rgba(245,240,230,0.28)' : 'var(--rule-strong)';
  const accent = onInk ? 'var(--gold-bright)' : 'var(--drafting-blue)';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)', ...style }} {...props}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-3)',
          fontFamily: 'var(--font-mono)',
          fontSize: 'var(--text-2xs)',
          textTransform: 'uppercase',
          letterSpacing: 'var(--tracking-caps)',
          color: accent,
          fontWeight: 'var(--w-mono)',
        }}
      >
        <span>Sheet {String(sheet).padStart(2, '0')} of {String(total).padStart(2, '0')}</span>
        <span style={{ flex: 1, height: '1px', background: rule }} />
      </div>
      <h2
        style={{
          fontFamily: 'var(--font-heading)',
          fontWeight: 'var(--w-bold)',
          fontSize: 'var(--text-2xl)',
          lineHeight: 'var(--leading-snug)',
          letterSpacing: 'var(--tracking-heading)',
          color: strong,
          margin: 0,
        }}
      >
        {title}
      </h2>
      {subtitle && (
        <p
          style={{
            fontFamily: 'var(--font-sans)',
            fontSize: 'var(--text-base)',
            color: muted,
            margin: 0,
            maxWidth: '56ch',
          }}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
}
