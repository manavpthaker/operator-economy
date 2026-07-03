import React from 'react';

export interface SheetHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Current sheet number. */
  sheet?: number;
  /** Total sheets. */
  total?: number;
  /** Section title (serif). */
  title: React.ReactNode;
  /** Optional supporting line. */
  subtitle?: React.ReactNode;
  /** Dark video-chapter treatment. */
  onInk?: boolean;
}

/**
 * Chapter / section divider styled as a drawing sheet ("SHEET 02 OF 05").
 * @startingPoint section="Brand" subtitle="Drawing-sheet chapter divider" viewport="700x200"
 */
export function SheetHeader(props: SheetHeaderProps): JSX.Element;
