import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual weight. primary = Drafting Blue fill; secondary = outline; ghost = text-only. */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** Control size. */
  size?: 'sm' | 'md' | 'lg';
  /** Render as a different element (e.g. 'a' for links). */
  as?: 'button' | 'a';
  /** Stretch to fill the container width. */
  fullWidth?: boolean;
  disabled?: boolean;
  children?: React.ReactNode;
}

/**
 * The single, restrained call-to-action. One primary per view.
 * @startingPoint section="Core" subtitle="Restrained CTA — primary / secondary / ghost" viewport="700x160"
 */
export function Button(props: ButtonProps): JSX.Element;
