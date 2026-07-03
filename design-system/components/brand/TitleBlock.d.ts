import React from 'react';

export interface TitleBlockField {
  label: string;
  value: React.ReactNode;
}

export interface TitleBlockProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Document number, e.g. "Operator Blueprint №004". */
  docNumber?: string;
  /** Document title (serif). */
  title?: React.ReactNode;
  /** Mono metadata fields — date, revision, sources, reading time, etc. */
  fields?: TitleBlockField[];
  /** Dark end-card treatment. */
  onInk?: boolean;
}

/**
 * Drafting-style title block: doc number, title, sourced metadata grid.
 * @startingPoint section="Brand" subtitle="Versioned document title block for blueprints & end-cards" viewport="700x260"
 */
export function TitleBlock(props: TitleBlockProps): JSX.Element;
