import React from 'react';

export interface SchematicNodeProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Step label, e.g. "Step 02 · The brain". */
  step: React.ReactNode;
  /** What it is, e.g. "Claude API". */
  name: React.ReactNode;
  /** REQUIRED by brand rule: a real figure, e.g. "$20". No placeholders. */
  figure: React.ReactNode;
  /** Unit suffix, e.g. "/mo". */
  unit?: string;
  /** Live/verified status text ("Live", "Running") — sage, status only. */
  status?: React.ReactNode;
  /** Gold treatment for the one output figure per panel. */
  highlight?: boolean;
}

/** One labeled, priced node of the working schematic. */
export function SchematicNode(props: SchematicNodeProps): JSX.Element;
