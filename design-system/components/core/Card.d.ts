import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLElement> {
  as?: keyof JSX.IntrinsicElements;
  /** Small-caps label rendered at the top of the card. */
  kicker?: React.ReactNode;
  /** Add the top Drafting-Blue rule — reads as a drawing sheet. */
  sheet?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  children?: React.ReactNode;
}

/**
 * Document-grade surface: hairline border, quiet shadow, tight corners.
 * @startingPoint section="Core" subtitle="Blueprint surface with optional sheet rule" viewport="700x220"
 */
export function Card(props: CardProps): JSX.Element;
