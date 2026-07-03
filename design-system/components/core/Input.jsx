import React from 'react';

/**
 * Input — text field for the one capture the site allows (email).
 * Sunken paper well, hairline border, blue focus. Mono variant for
 * numeric/code entry. Pair with a small-caps <label className="oe-label">.
 */
export function Input({
  mono = false,
  invalid = false,
  size = 'md',
  style,
  ...props
}) {
  const sizes = {
    sm: { padding: '8px 10px', fontSize: 'var(--text-sm)' },
    md: { padding: '11px 14px', fontSize: 'var(--text-base)' },
    lg: { padding: '14px 16px', fontSize: 'var(--text-lg)' },
  };

  return (
    <input
      className="oe-input"
      style={{
        width: '100%',
        fontFamily: mono ? 'var(--font-mono)' : 'var(--font-sans)',
        fontWeight: 'var(--w-regular)',
        color: 'var(--ink-900)',
        background: 'var(--paper-0)',
        border: `1px solid ${invalid ? 'var(--negative)' : 'var(--border-strong)'}`,
        borderRadius: 'var(--radius-xs)',
        boxShadow: 'var(--shadow-inset)',
        lineHeight: 1.4,
        transition: 'border-color var(--dur-fast) var(--ease-standard), box-shadow var(--dur-fast) var(--ease-standard)',
        ...sizes[size],
        ...style,
      }}
      {...props}
    />
  );
}
