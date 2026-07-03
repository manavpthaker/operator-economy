import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK} from '../theme';

/**
 * Frame-driven mono numeral — the moment a figure "lands" on screen.
 * Counts up from 0 (or `from`) to the target value with a soft spring,
 * then holds. Formatted with tabular figures / slashed zero so the
 * width doesn't wobble as digits change.
 */
export type MonoCounterProps = {
  value: number;
  from?: number;
  prefix?: string;
  suffix?: string;
  startFrame: number;
  durationInFrames?: number;
  fontSize?: number;
  color?: string;
  format?: (v: number) => string;
  align?: 'left' | 'center' | 'right';
  // If true, formatted as compact currency ($5.9B / $2K / $2,000)
  compactCurrency?: boolean;
};

const compact = (v: number, unit = '') => {
  const abs = Math.abs(v);
  if (abs >= 1_000_000_000) return `${(v / 1_000_000_000).toFixed(1).replace(/\.0$/, '')}B${unit}`;
  if (abs >= 1_000_000) return `${(v / 1_000_000).toFixed(1).replace(/\.0$/, '')}M${unit}`;
  if (abs >= 10_000) return `${Math.round(v / 1000)}K${unit}`;
  if (abs >= 1000) return `${(v / 1000).toFixed(1).replace(/\.0$/, '')}K${unit}`;
  return `${Math.round(v)}${unit}`;
};

export const MonoCounter: React.FC<MonoCounterProps> = ({
  value,
  from = 0,
  prefix = '',
  suffix = '',
  startFrame,
  durationInFrames,
  fontSize = 80,
  color = COLORS.ink900,
  format,
  align = 'left',
  compactCurrency = false,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dur = durationInFrames ?? Math.round(fps * 0.9);
  const rel = frame - startFrame;
  const progress = spring({
    frame: rel,
    fps,
    config: {damping: 200, stiffness: 90, mass: 1.2},
    durationInFrames: dur,
  });
  const shown = from + (value - from) * progress;

  const text = format
    ? format(shown)
    : compactCurrency
      ? `${prefix}${compact(shown)}${suffix}`
      : `${prefix}${Math.round(shown).toLocaleString()}${suffix}`;

  return (
    <span
      style={{
        fontFamily: FONTS.mono,
        fontWeight: 400,
        fontSize,
        lineHeight: 1,
        letterSpacing: `${TRACK.mono}em`,
        color,
        fontFeatureSettings: "'tnum' 1, 'zero' 1",
        display: 'inline-block',
        textAlign: align,
        whiteSpace: 'nowrap',
      }}
    >
      {text}
    </span>
  );
};
