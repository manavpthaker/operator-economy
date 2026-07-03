import React from 'react';

export interface CitationChipProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** The source, e.g. "Sacra" or "Accenture Annual Report". */
  source: string;
  /** Optional date, e.g. "Apr 2026". */
  date?: string;
  /** Mark as an estimate (gold) rather than a hard source (blue). */
  estimate?: boolean;
  /** Video lower-third treatment for dark surfaces. */
  onInk?: boolean;
}

/**
 * The channel's signature: a source chip beside every published number.
 * @startingPoint section="Brand" subtitle="Signature source chip — SOURCE: … on every number" viewport="700x120"
 */
export function CitationChip(props: CitationChipProps): JSX.Element;
