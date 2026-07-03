import React from 'react';

/**
 * SchematicNode — one labeled node in the working schematic.
 * RULE: every node carries a REAL figure and its source is cited at
 * panel level. Placeholder nodes ("your tool here", "$???") are
 * banned — a node with no figure renders a dev warning.
 * Use inside <Schematic>; also works standalone on navy surfaces.
 */
export function SchematicNode({
  step,
  name,
  figure,
  unit,
  status,
  highlight = false,
  style,
  ...props
}) {
  if (figure === undefined || figure === null || figure === '') {
    // eslint-disable-next-line no-console
    console.warn('SchematicNode: every node must carry a real figure + source. Placeholder nodes are banned.');
  }

  return (
    <div
      style={{
        position: 'relative',
        border: '1px solid var(--schem-node-border)',
        background: 'var(--schem-node-bg)',
        padding: '12px 14px',
        borderRadius: 'var(--radius-none)',
        ...style,
      }}
      {...props}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          gap: '10px',
          fontFamily: 'var(--font-mono)',
          fontSize: '9px',
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color: 'rgba(245,240,230,0.55)',
          marginBottom: '7px',
        }}
      >
        <span>{step}</span>
        {status && (
          <span style={{ color: 'var(--status-live)' }}>● {status}</span>
        )}
      </div>
      <div
        style={{
          fontFamily: 'var(--font-sans)',
          fontSize: '14.5px',
          fontWeight: 'var(--w-medium)',
          color: 'var(--paper-100)',
          marginBottom: '6px',
        }}
      >
        {name}
      </div>
      <div
        style={{
          fontFamily: 'var(--font-mono)',
          fontWeight: 'var(--w-mono)',
          fontSize: '17px',
          color: highlight ? 'var(--gold-bright)' : 'rgba(245,240,230,0.92)',
          fontFeatureSettings: "'tnum' 1",
        }}
      >
        {figure ?? '—'}
        {unit && <span style={{ fontSize: '11px', color: 'rgba(245,240,230,0.55)' }}>{unit}</span>}
      </div>
    </div>
  );
}
