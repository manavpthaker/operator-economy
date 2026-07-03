import React from 'react';
import {AbsoluteFill} from 'remotion';
import {OEBarChart, BarDatum} from '../primitives/OEBarChart';
import {COLORS} from '../theme';

/**
 * ChartScene — paper-world bar chart. Uses OEBarChart primitive with the
 * DS's one-gold-bar rule. Title + optional citation baked in. Reserved
 * space at the bottom for captions.
 */
export type ChartSceneProps = {
  title?: string;
  series: BarDatum[];
  unit?: string;
  source?: string;
  estimate?: boolean;
  onInk?: boolean;
  startFrame: number;
};

// Any chart series whose max value spans multiple orders of magnitude
// benefits from compact currency formatting ($5.9B vs 2,000).
const shouldCompact = (data: BarDatum[]) => {
  const max = Math.max(...data.map((d) => d.value));
  return max >= 1_000_000;
};

export const ChartScene: React.FC<ChartSceneProps> = ({
  title,
  series,
  unit,
  source,
  estimate,
  onInk = false,
  startFrame,
}) => (
  <AbsoluteFill
    style={{
      background: onInk ? COLORS.ink : COLORS.paper,
      justifyContent: 'center',
      alignItems: 'flex-start',
      padding: '120px 160px 260px',
    }}
  >
    <OEBarChart
      title={title}
      data={series}
      unit={unit}
      compactCurrency={unit === '$' && shouldCompact(series)}
      source={source}
      estimate={estimate}
      onInk={onInk}
      startFrame={startFrame}
      chartHeight={540}
    />
  </AbsoluteFill>
);
