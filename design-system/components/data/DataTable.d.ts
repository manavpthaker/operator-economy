import React from 'react';

export interface DataColumn {
  key: string;
  label: React.ReactNode;
  align?: 'left' | 'right' | 'center';
  /** Render values in IBM Plex Mono, right-aligned by default. */
  numeric?: boolean;
}

export interface DataTableProps extends React.HTMLAttributes<HTMLDivElement> {
  columns: DataColumn[];
  rows: Record<string, React.ReactNode>[];
  /** Source line shown in the footer. */
  source?: string;
  zebra?: boolean;
}

/**
 * A ledger: mono numerals, hairline rules, sourced footer.
 * @startingPoint section="Data" subtitle="Sourced mono data table" viewport="700x300"
 */
export function DataTable(props: DataTableProps): JSX.Element;
