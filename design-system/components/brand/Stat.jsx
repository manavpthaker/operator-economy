import React from 'react';

/**
 * Stat — a single published figure in mono numerals with its unit and
 * an optional label + delta. The evidence object, not decoration.
 * `emphasis="gold"` marks the one key figure per view. `size` scales
 * from inline data to a thumbnail-grade display number.
 */
export function Stat({
  value,
  unit,
  prefix,
  label,
  delta,
  deltaDirection,
  emphasis = 'default',
  size = 'md',
  onInk = false,
  style,
  ...props
}) {
  const sizes = {
    sm: 'var(--text-xl)',
    md: 'var(--text-3xl)',
    lg: 'var(--text-4xl)',
    xl: 'var(--text-5xl)',
  };

  const valueColor = onInk
    ? (emphasis === 'gold' ? 'var(--gold-bright)' : 'var(--text-on-ink)')
    : (emphasis === 'gold' ? 'var(--gold-700)'
      : emphasis === 'accent' ? 'var(--drafting-blue)'
      : 'var(--ink-900)');

  const labelColor = onInk ? 'var(--text-on-ink-muted)' : 'var(--text-muted)';

  const deltaColor =
    deltaDirection === 'down' ? 'var(--negative)'
    : deltaDirection === 'up' ? 'var(--sage-700)'
    : 'var(--text-muted)';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', ...style }} {...props}>
      {label && (
        <div
          className="oe-label"
          style={{ color: labelColor }}
        >
          {label}
        </div>
      )}
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px' }}>
        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontWeight: 'var(--w-mono)',
            fontSize: sizes[size],
            lineHeight: 1,
            letterSpacing: '-0.01em',
            color: valueColor,
            fontFeatureSettings: "'tnum' 1, 'zero' 1",
          }}
        >
          {prefix}{value}{unit && <span style={{ fontSize: '0.55em', fontWeight: 'var(--w-mono)', marginLeft: '2px', opacity: 0.75 }}>{unit}</span>}
        </span>
        {delta && (
          <span
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-sm)',
              fontWeight: 'var(--w-mono)',
              color: deltaColor,
            }}
          >
            {deltaDirection === 'up' ? '▲' : deltaDirection === 'down' ? '▼' : ''} {delta}
          </span>
        )}
      </div>
    </div>
  );
}
