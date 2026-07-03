import React from 'react';

export interface GapFigureProps extends React.HTMLAttributes<HTMLDivElement> {
  /** The before figure, e.g. "$5.9B". Stays neutral. */
  from: React.ReactNode;
  /** The after figure, e.g. "$2K". Gold, like the arrow. */
  to: React.ReactNode;
  /** Optional bracket label underneath, e.g. "The gap". */
  label?: React.ReactNode;
  /** Dark-surface treatment (thumbnails, video). */
  onInk?: boolean;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

/**
 * The signature before/after economics gap with the gold arrow.
 * @startingPoint section="Brand" subtitle="$5.9B → $2K — the gold-arrow gap figure" viewport="700x200"
 */
export function GapFigure(props: GapFigureProps): JSX.Element;
