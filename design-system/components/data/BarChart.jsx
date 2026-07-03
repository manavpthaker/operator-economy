import React from 'react';

/**
 * BarChart — a custom chart that reads as institutional research, never
 * default Excel. Drafting-Blue bars on a baseline axis, mono value
 * labels, one optional Ledger-Gold highlight bar, sourced footer.
 * data: [{ label, value, highlight? }]
 */
export function BarChart({
  data = [],
  unit = '',
  prefix = '',
  height = 220,
  source,
  format,
  style,
  ...props
}) {
  const max = Math.max(...data.map((d) => d.value), 1);
  const fmt = format || ((v) => `${prefix}${v.toLocaleString()}${unit}`);

  return (
    <div style={{ fontFamily: 'var(--font-sans)', ...style }} {...props}>
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: 'var(--space-5)',
          height,
          borderBottom: '1.5px solid var(--ink-900)',
          paddingBottom: 0,
        }}
      >
        {data.map((d, i) => {
          const h = Math.max((d.value / max) * 100, 1.5);
          const color = d.highlight ? 'var(--ledger-gold)' : 'var(--drafting-blue)';
          return (
            <div
              key={i}
              style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-end',
                alignItems: 'center',
                height: '100%',
              }}
            >
              <div
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: 'var(--text-sm)',
                  fontWeight: 'var(--w-mono)',
                  color: d.highlight ? 'var(--gold-700)' : 'var(--ink-900)',
                  marginBottom: '8px',
                  fontFeatureSettings: "'tnum' 1",
                  whiteSpace: 'nowrap',
                }}
              >
                {fmt(d.value)}
              </div>
              <div
                style={{
                  width: '100%',
                  maxWidth: '96px',
                  height: `${h}%`,
                  background: color,
                  transition: 'height var(--dur-slow) var(--ease-out)',
                }}
              />
            </div>
          );
        })}
      </div>
      <div style={{ display: 'flex', gap: 'var(--space-5)', marginTop: '10px' }}>
        {data.map((d, i) => (
          <div
            key={i}
            className="oe-label"
            style={{ flex: 1, textAlign: 'center', color: 'var(--text-muted)' }}
          >
            {d.label}
          </div>
        ))}
      </div>
      {source && (
        <div
          style={{
            marginTop: 'var(--space-4)',
            fontFamily: 'var(--font-mono)',
            fontSize: 'var(--text-3xs)',
            letterSpacing: 'var(--tracking-caps)',
            textTransform: 'uppercase',
            color: 'var(--text-muted)',
          }}
        >
          Source: {source}
        </div>
      )}
    </div>
  );
}
