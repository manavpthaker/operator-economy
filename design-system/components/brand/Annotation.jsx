import React from 'react';

/**
 * Annotation — the diagram-being-explained motif. Wraps content with a
 * measurement-style bracket and a small-caps label in the margin, as if
 * a schematic were being called out. `side` places the bracket.
 */
export function Annotation({
  label,
  side = 'right',
  color = 'var(--drafting-blue)',
  children,
  style,
  ...props
}) {
  const horizontal = side === 'top' || side === 'bottom';

  const bracket = (
    <div
      aria-hidden="true"
      style={
        horizontal
          ? {
              height: '7px',
              borderLeft: `1.5px solid ${color}`,
              borderRight: `1.5px solid ${color}`,
              borderTop: side === 'top' ? 'none' : `1.5px solid ${color}`,
              borderBottom: side === 'top' ? `1.5px solid ${color}` : 'none',
              width: '100%',
            }
          : {
              width: '7px',
              borderTop: `1.5px solid ${color}`,
              borderBottom: `1.5px solid ${color}`,
              borderLeft: side === 'left' ? 'none' : `1.5px solid ${color}`,
              borderRight: side === 'left' ? `1.5px solid ${color}` : 'none',
              alignSelf: 'stretch',
            }
      }
    />
  );

  const tag = (
    <span
      className="oe-label"
      style={{
        color,
        whiteSpace: horizontal ? 'nowrap' : 'normal',
        writingMode: horizontal ? 'horizontal-tb' : 'horizontal-tb',
        maxWidth: horizontal ? 'none' : '12ch',
      }}
    >
      {label}
    </span>
  );

  const gap = 'var(--space-3)';

  if (horizontal) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap, ...style }} {...props}>
        {side === 'top' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>{bracket}{tag}</div>
        )}
        <div>{children}</div>
        {side === 'bottom' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>{bracket}{tag}</div>
        )}
      </div>
    );
  }

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: side === 'left' ? 'row' : 'row',
        alignItems: 'stretch',
        gap,
        ...style,
      }}
      {...props}
    >
      {side === 'left' && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>{tag}{bracket}</div>
      )}
      <div style={{ flex: 1 }}>{children}</div>
      {side === 'right' && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>{bracket}{tag}</div>
      )}
    </div>
  );
}
