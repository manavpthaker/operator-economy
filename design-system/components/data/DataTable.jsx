import React from 'react';

/**
 * DataTable — a ledger. Mono numerals, right-aligned, hairline rules,
 * optional zebra rows and a source footer. Numeric columns are mono
 * automatically; the first column reads as a label in sans.
 * columns: [{ key, label, align?, numeric? }]
 */
export function DataTable({
  columns = [],
  rows = [],
  source,
  zebra = true,
  style,
  ...props
}) {
  return (
    <div
      style={{
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-xs)',
        overflow: 'hidden',
        background: 'var(--paper-0)',
        ...style,
      }}
      {...props}
    >
      <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--font-sans)' }}>
        <thead>
          <tr>
            {columns.map((c) => (
              <th
                key={c.key}
                style={{
                  textAlign: c.align || (c.numeric ? 'right' : 'left'),
                  padding: '10px 16px',
                  fontFamily: 'var(--font-sans)',
                  fontSize: 'var(--text-3xs)',
                  fontWeight: 'var(--w-semibold)',
                  textTransform: 'uppercase',
                  letterSpacing: 'var(--tracking-label)',
                  color: 'var(--text-muted)',
                  borderBottom: '1.5px solid var(--border-strong)',
                  background: 'var(--paper-200)',
                  whiteSpace: 'nowrap',
                }}
              >
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, ri) => (
            <tr
              key={ri}
              style={{ background: zebra && ri % 2 === 1 ? 'var(--paper-100)' : 'transparent' }}
            >
              {columns.map((c, ci) => (
                <td
                  key={c.key}
                  style={{
                    textAlign: c.align || (c.numeric ? 'right' : 'left'),
                    padding: '11px 16px',
                    fontFamily: c.numeric ? 'var(--font-mono)' : 'var(--font-sans)',
                    fontSize: 'var(--text-sm)',
                    fontWeight: ci === 0 ? 'var(--w-medium)' : 'var(--w-regular)',
                    color: ci === 0 ? 'var(--ink-900)' : 'var(--ink-700)',
                    fontFeatureSettings: c.numeric ? "'tnum' 1, 'zero' 1" : undefined,
                    borderBottom: ri < rows.length - 1 ? '1px solid var(--border)' : 'none',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {r[c.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {source && (
        <div
          style={{
            padding: '8px 16px',
            borderTop: '1px solid var(--border)',
            background: 'var(--paper-200)',
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
