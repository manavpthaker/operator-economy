import React from 'react';
import {AbsoluteFill} from 'remotion';
import {GapArrow} from '../primitives/GapArrow';
import {CitationChip} from '../primitives/CitationChip';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * HookGap — Ink-world hook treatment. Kicker line up top, GapArrow front-
 * and-center, citation chip under. Used when the hook section's first
 * beat is a bar chart with exactly two series that describe a scale gap
 * (Accenture $5.9B → Solo $2K).
 */
export type HookGapProps = {
  overline?: string;
  from: string;
  to: string;
  label?: string;
  source?: string;
  estimate?: boolean;
  startFrame: number;
};

export const HookGap: React.FC<HookGapProps> = ({
  overline,
  from,
  to,
  label,
  source,
  estimate,
  startFrame,
}) => (
  <AbsoluteFill
    style={{
      background: COLORS.ink,
      justifyContent: 'center',
      alignItems: 'center',
      padding: '0 160px',
    }}
  >
    {overline && (
      <div
        style={{
          fontFamily: FONTS.mono,
          fontSize: TYPE.microLabel,
          letterSpacing: `${TRACK.caps}em`,
          textTransform: 'uppercase',
          color: COLORS.goldBright,
          marginBottom: 44,
        }}
      >
        {overline}
      </div>
    )}
    <GapArrow from={from} to={to} label={label} onInk startFrame={startFrame} size="xl" />
    {source && (
      <div style={{marginTop: 60}}>
        <CitationChip source={source} estimate={estimate} onInk />
      </div>
    )}
  </AbsoluteFill>
);
