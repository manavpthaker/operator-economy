import React from 'react';

/**
 * Button — Welsh-grade restraint. One clear action per view.
 * Variants: primary (Drafting Blue), secondary (outline), ghost (text).
 * Never neon, never gradient. Square-ish corners; the label is sans.
 */
export function Button({
  variant = 'primary',
  size = 'md',
  as = 'button',
  fullWidth = false,
  disabled = false,
  children,
  style,
  ...props
}) {
  const sizes = {
    sm: { padding: '7px 14px', fontSize: 'var(--text-xs)' },
    md: { padding: '10px 20px', fontSize: 'var(--text-sm)' },
    lg: { padding: '14px 28px', fontSize: 'var(--text-base)' },
  };

  const variants = {
    primary: {
      background: 'var(--accent)',
      color: 'var(--paper-100)',
      border: '1px solid var(--accent)',
    },
    secondary: {
      background: 'transparent',
      color: 'var(--ink-900)',
      border: '1px solid var(--border-strong)',
    },
    ghost: {
      background: 'transparent',
      color: 'var(--accent)',
      border: '1px solid transparent',
    },
  };

  const Tag = as;

  return (
    <Tag
      disabled={Tag === 'button' ? disabled : undefined}
      data-variant={variant}
      className="oe-btn"
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 'var(--space-2)',
        width: fullWidth ? '100%' : 'auto',
        fontFamily: 'var(--font-sans)',
        fontWeight: 'var(--w-semibold)',
        lineHeight: 1,
        letterSpacing: '0.005em',
        borderRadius: 'var(--radius-sm)',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.45 : 1,
        transition: 'background var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard), color var(--dur-fast) var(--ease-standard)',
        textDecoration: 'none',
        whiteSpace: 'nowrap',
        ...sizes[size],
        ...variants[variant],
        ...style,
      }}
      {...props}
    >
      {children}
    </Tag>
  );
}
