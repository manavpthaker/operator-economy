import React from 'react';

export interface BarDatum {
  label: React.ReactNode;
  value: number;
  /** Render this bar in Ledger Gold — the one highlight per chart. */
  highlight?: boolean;
}

export interface BarChartProps extends React.HTMLAttributes<HTMLDivElement> {
  data: BarDatum[];
  /** Unit suffix appended to value labels, e.g. "B" or "%". */
  unit?: string;
  /** Prefix, e.g. "$". */
  prefix?: string;
  /** Chart plot height in px. */
  height?: number;
  /** Source line for the footer. */
  source?: string;
  /** Custom value formatter (v:number)=>string. */
  format?: (v: number) => string;
}

/**
 * Institutional bar chart — Drafting-Blue bars, mono labels, one gold highlight.
 * @startingPoint section="Data" subtitle="Institutional bar chart with sourced footer" viewport="700x340"
 */
export function BarChart(props: BarChartProps): JSX.Element;
