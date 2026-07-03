import React from 'react';

export interface SchematicProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Sheet number for the tag, e.g. 1 → "SHEET 01 OF 05". */
  sheet?: number;
  total?: number;
  /** Sheet title, e.g. "The stack". */
  title?: React.ReactNode;
  /** Live-status label (sage). Pass null to hide. */
  running?: React.ReactNode | null;
  /** Vertical measurement-bracket label, e.g. "≤ $100/mo". */
  bracket?: React.ReactNode;
  /** REQUIRED by brand rule: the panel's source, e.g. "Sacra · Apr 2026". */
  source?: React.ReactNode;
  /** Right-side footer readout, e.g. "Margin 94% ▲". */
  footer?: React.ReactNode;
  width?: number | string;
  /** SchematicNodes — wires are inserted between children automatically. */
  children?: React.ReactNode;
}

/**
 * The navy working-schematic panel: grid, sheet tag, wired nodes, sourced footer.
 * @startingPoint section="Brand" subtitle="Navy schematic panel with wired, priced nodes" viewport="700x420"
 */
export function Schematic(props: SchematicProps): JSX.Element;
