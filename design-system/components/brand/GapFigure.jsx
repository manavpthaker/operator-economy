import React from 'react';

/**
 * GapFigure — the signature before/after economics gap:
 * "$5.9B → $2K" with the gold arrow. The arrow and destination
 * figure are gold; the origin stays neutral. Optional bracket
 * label underneath ("THE GAP"). Fragment Mono, single weight.
 */
export function GapFigure({
  from,
  to,
  label,
  onInk = false,
  size = 'md',
  style,
  ...props
}) {
  const sizes = { sm: '1.5rem', md: '2.75rem', lg: '4.5rem', xl: '7rem' };
  const gold = onInk ? 'var(--gold-bright)' : 'var(--gold-700)';
  const base = onInk ? 'var(--text-on-ink)' : 'var(--ink-900)';
  const rule = onInk ? 'rgba(245,240,230,0.4)' : 'var(--rule-strong)';
  const muted = onInk ? 'var(--text-on-ink-muted)' : 'var(--text-muted)';

  return (
    <div style={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center', ...style }} {...props}>
      <div
        style={{
          fontFamily: 'var(--font-mono)',
          fontWeight: 'var(--w-mono)',
          fontSize: sizes[size],
          lineHeight: 1,
          letterSpacing: '-0.02em',
          color: base,
          fontFeatureSettings: "'tnum' 1",
          whiteSpace: 'nowrap',
        }}
      >
        {from} <span style={{ color: gold }}>→</span> <span style={{ color: gold }}>{to}</span>
      </div>
      {label && (
        <div style={{ width: '58%', marginTop: '10px' }}>
          <div
            aria-hidden="true"
            style={{ height: '8px', border: `1px solid ${rule}`, borderTop: 'none' }}
          />
          <div
            style={{
              textAlign: 'center',
              marginTop: '8px',
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-3xs)',
              letterSpacing: 'var(--tracking-label)',
              textTransform: 'uppercase',
              color: muted,
            }}
          >
            {label}
          </div>
        </div>
      )}
    </div>
  );
}
