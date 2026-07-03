import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';
import {CitationChip} from '../primitives/CitationChip';

/**
 * SourceCard — a single claim with its source, held long enough for
 * the viewer to read both. Smaller than a QuoteCard; larger than a
 * chart's inline citation chip. Used when the whole beat is "here is
 * the source we're relying on for this claim."
 */
export type SourceCardProps = {
  claim: string;
  source: string;
  estimate?: boolean;
  onInk?: boolean;
};

export const SourceCard: React.FC<SourceCardProps> = ({claim, source, estimate, onInk = false}) => {
  const frame = useCurrentFrame();
  const claimT = interpolate(frame, [0, 14], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const chipT = interpolate(frame, [16, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.standard),
  });

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 200px',
      }}
    >
      <div style={{maxWidth: 1400, textAlign: 'left'}}>
        <div
          style={{
            fontFamily: FONTS.heading,
            fontWeight: 700,
            fontSize: TYPE.h2,
            lineHeight: 1.14,
            letterSpacing: `${TRACK.heading}em`,
            color: onInk ? COLORS.onInk : COLORS.ink900,
            opacity: claimT,
            transform: `translateY(${(1 - claimT) * 12}px)`,
          }}
        >
          {claim}
        </div>
        <div style={{marginTop: 32, opacity: chipT}}>
          <CitationChip source={source} estimate={estimate} onInk={onInk} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
