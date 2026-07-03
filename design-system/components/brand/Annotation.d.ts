import React from 'react';

export interface AnnotationProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Small-caps callout label. */
  label: React.ReactNode;
  /** Which side the measurement bracket sits on. */
  side?: 'left' | 'right' | 'top' | 'bottom';
  /** Bracket + label color (defaults to Drafting Blue). */
  color?: string;
  children?: React.ReactNode;
}

/** Measurement-bracket callout — the "diagram being explained" motif. */
export function Annotation(props: AnnotationProps): JSX.Element;
