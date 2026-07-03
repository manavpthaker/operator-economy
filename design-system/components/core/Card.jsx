import React from 'react';

/**
 * Card — a blueprint surface. Near-square corners, hairline rule,
 * whisper-quiet shadow. Depth comes from paper tone, not float.
 * Use `sheet` to add the top drafting rule + optional kicker label.
 */
export function Card({
  as = 'div',
  kicker,
  sheet = false,
  padding = 'md',
  children,
  style,
  ...props
}) {
  const pads = {
    none: 0,
    sm: 'var(--space-4)',
    md: 'var(--space-5)',
    lg: 'var(--space-6)',
  };
  const Tag = as;

  return (
    <Tag
      style={{
        background: 'var(--surface-card)',
        border: '1px solid var(--border)',
        borderTop: sheet ? '2px solid var(--drafting-blue)' : '1px solid var(--border)',
        borderRadius: 'var(--radius-md)',
        boxShadow: 'var(--shadow-sm)',
        padding: pads[padding],
        ...style,
      }}
      {...props}
    >
      {kicker && (
        <div
          className="oe-label"
          style={{ marginBottom: 'var(--space-3)' }}
        >
          {kicker}
        </div>
      )}
      {children}
    </Tag>
  );
}
