import React from 'react';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Semantic tone. */
  tone?: 'neutral' | 'accent' | 'gold' | 'positive' | 'negative';
  /** Show a leading status dot. */
  dot?: boolean;
  children?: React.ReactNode;
}

/** Small-caps drafting-stamp label / status tag. */
export function Badge(props: BadgeProps): JSX.Element;
