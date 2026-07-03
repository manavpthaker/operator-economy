import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';
import {MonoCounter} from '../primitives/MonoCounter';
import {CitationChip} from '../primitives/CitationChip';

/**
 * ProofCard — one number + a source chip. The number lands with a
 * MonoCounter spring, then the citation chip ticks in after (secondary
 * action). Optional supporting line above ("Accenture GenAI bookings")
 * and contrast/context line below ("flat overall").
 *
 * Used for the "The AI implementation work is the only thing growing"
 * ×2 contrast in №001 (proof + a small contrast pill in muted brick).
 */
export type ProofCardProps = {
  value: number;
  prefix?: string;
  suffix?: string;
  compactCurrency?: boolean;
  label?: string;    // small-caps overline
  contrast?: string; // e.g. "flat overall" — muted brick chip below
  source?: string;
  estimate?: boolean;
  onInk?: boolean;
};

export const ProofCard: React.FC<ProofCardProps> = ({
  value,
  prefix,
  suffix,
  compactCurrency,
  label,
  contrast,
  source,
  estimate,
  onInk = false,
}) => {
  const frame = useCurrentFrame();
  const labelT = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const chipT = interpolate(frame, [22, 34], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.standard),
  });
  const contrastT = interpolate(frame, [34, 46], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.standard),
  });

  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
      }}
    >
      {label && (
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: muted,
            marginBottom: 32,
            opacity: labelT,
          }}
        >
          {label}
        </div>
      )}
      <MonoCounter
        value={value}
        prefix={prefix}
        suffix={suffix}
        startFrame={2}
        fontSize={TYPE.displayLg}
        color={gold}
        compactCurrency={compactCurrency}
        align="center"
      />
      {contrast && (
        <div
          style={{
            marginTop: 28,
            display: 'inline-flex',
            padding: '8px 16px',
            fontFamily: FONTS.mono,
            fontSize: TYPE.small,
            letterSpacing: `${TRACK.mono}em`,
            color: COLORS.negative,
            background: onInk ? 'rgba(155,62,46,0.08)' : 'rgba(155,62,46,0.06)',
            borderLeft: `2px solid ${COLORS.negative}`,
            opacity: contrastT,
          }}
        >
          {contrast}
        </div>
      )}
      {source && (
        <div style={{marginTop: 40, opacity: chipT}}>
          <CitationChip source={source} estimate={estimate} onInk={onInk} />
        </div>
      )}
    </AbsoluteFill>
  );
};
