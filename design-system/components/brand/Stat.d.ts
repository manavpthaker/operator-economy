import React from 'react';

export interface StatProps extends React.HTMLAttributes<HTMLDivElement> {
  /** The number itself, e.g. "5.9" or "5,900". */
  value: React.ReactNode;
  /** Unit suffix, e.g. "B", "%", "/mo". */
  unit?: string;
  /** Prefix, e.g. "$". */
  prefix?: string;
  /** Small-caps label above the figure. */
  label?: React.ReactNode;
  /** Optional delta value, e.g. "2×" or "31%". */
  delta?: React.ReactNode;
  /** Delta direction — colors and adds a marker. */
  deltaDirection?: 'up' | 'down' | 'flat';
  /** default | gold (the one key figure) | accent. */
  emphasis?: 'default' | 'gold' | 'accent';
  /** sm (inline) → xl (thumbnail display). */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Dark-surface treatment. */
  onInk?: boolean;
}

/**
 * A single published figure in mono numerals — the evidence object.
 * @startingPoint section="Brand" subtitle="Mono figure with unit, label & delta" viewport="700x160"
 */
export function Stat(props: StatProps): JSX.Element;
