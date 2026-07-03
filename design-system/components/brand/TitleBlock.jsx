import React from 'react';

/**
 * TitleBlock — the drafting-style title block on every blueprint PDF,
 * video end-card, and chart. Signals "versioned, sourced document",
 * not lead-gen PDF. A framed grid of mono metadata fields.
 * `onInk` for dark end-cards.
 */
export function TitleBlock({
  docNumber = 'Operator Blueprint №004',
  title,
  fields = [],
  onInk = false,
  style,
  ...props
}) {
  const ink = onInk;
  const frame = ink ? 'rgba(245,240,230,0.28)' : 'var(--rule-strong)';
  const strong = ink ? 'var(--text-on-ink)' : 'var(--ink-900)';
  const muted = ink ? 'var(--text-on-ink-muted)' : 'var(--ink-500)';

  return (
    <div
      style={{
        border: `1.5px solid ${frame}`,
        borderRadius: 'var(--radius-xs)',
        background: ink ? 'transparent' : 'var(--paper-0)',
        fontFamily: 'var(--font-mono)',
        ...style,
      }}
      {...props}
    >
      {/* Header row: doc number */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
          gap: 'var(--space-4)',
          padding: '10px 16px',
          borderBottom: `1px solid ${frame}`,
          fontSize: 'var(--text-3xs)',
          textTransform: 'uppercase',
          letterSpacing: 'var(--tracking-caps)',
          color: ink ? 'var(--gold-bright)' : 'var(--drafting-blue)',
          fontWeight: 'var(--w-mono)',
        }}
      >
        <span>{docNumber}</span>
        <span style={{ color: muted }}>The Operator Economy</span>
      </div>

      {/* Title */}
      {title && (
        <div
          style={{
            padding: '16px',
            borderBottom: fields.length ? `1px solid ${frame}` : 'none',
          }}
        >
          <div
            style={{
              fontFamily: 'var(--font-heading)',
              fontWeight: 'var(--w-bold)',
              fontSize: 'var(--text-xl)',
              lineHeight: 'var(--leading-snug)',
              color: strong,
              letterSpacing: 'var(--tracking-tight)',
            }}
          >
            {title}
          </div>
        </div>
      )}

      {/* Metadata grid */}
      {fields.length > 0 && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${Math.min(fields.length, 4)}, 1fr)`,
          }}
        >
          {fields.map((f, i) => (
            <div
              key={i}
              style={{
                padding: '10px 16px',
                borderRight: (i + 1) % Math.min(fields.length, 4) !== 0 ? `1px solid ${frame}` : 'none',
                borderTop: i >= Math.min(fields.length, 4) ? `1px solid ${frame}` : 'none',
              }}
            >
              <div
                style={{
                  fontSize: 'var(--text-3xs)',
                  textTransform: 'uppercase',
                  letterSpacing: 'var(--tracking-caps)',
                  color: muted,
                  marginBottom: '4px',
                }}
              >
                {f.label}
              </div>
              <div
                style={{
                  fontSize: 'var(--text-sm)',
                  fontWeight: 'var(--w-mono)',
                  color: strong,
                }}
              >
                {f.value}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
