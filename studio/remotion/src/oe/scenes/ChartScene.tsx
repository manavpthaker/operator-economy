import React from 'react';
import {AbsoluteFill} from 'remotion';
import {OEBarChart, BarDatum, BarFocusEvent} from '../primitives/OEBarChart';
import {COLORS} from '../theme';

/**
 * ChartScene — screen-register evidence chart. The chart owns the frame;
 * source metadata stays subordinate at the bottom edge.
 */
export type ChartSceneProps = {
  title?: string;
  series: BarDatum[];
  unit?: string;
  source?: string;
  estimate?: boolean;
  onInk?: boolean;
  startFrame: number;
  /** Chart re-read cues from pace_storyboard. */
  focusEvents?: BarFocusEvent[];
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
  focusEvents,
}) => (
  <AbsoluteFill
    style={{
      background: onInk ? COLORS.ink : COLORS.paper,
      justifyContent: 'center',
      alignItems: 'flex-start',
      padding: '72px 120px 96px',
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
      chartHeight={640}
      focusEvents={focusEvents}
    />
  </AbsoluteFill>
);
