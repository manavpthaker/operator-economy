import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';
import {CitationChip} from '../primitives/CitationChip';

/**
 * LogoScene — a company name treated as an evidence card, not a logo
 * slide. Wordmark in Zodiak/Boska, a mono "COMPANY · SECTOR" line above,
 * caption below, optional citation.
 */
export type LogoSceneProps = {
  company: string;
  caption?: string;
  source?: string;
  onInk?: boolean;
  startFrame: number;
};

export const LogoScene: React.FC<LogoSceneProps> = ({company, caption, source, onInk = true, startFrame}) => {
  const frame = useCurrentFrame();
  const rel = frame - startFrame;
  const t = interpolate(rel, [0, 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 32,
          opacity: t,
          transform: `translateY(${(1 - t) * 14}px)`,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: onInk ? COLORS.goldBright : COLORS.draftingBlue,
          }}
        >
          Company
        </div>
        <h1
          style={{
            fontFamily: FONTS.display,
            fontWeight: 700,
            fontSize: 132,
            lineHeight: 1,
            letterSpacing: `${TRACK.display}em`,
            color: onInk ? COLORS.onInk : COLORS.ink900,
            margin: 0,
          }}
        >
          {company}
        </h1>
        {caption && (
          <div
            style={{
              fontFamily: FONTS.sans,
              fontSize: TYPE.bodyLg,
              color: onInk ? COLORS.onInkMuted : COLORS.ink500,
              maxWidth: 900,
              textAlign: 'center',
              marginTop: 12,
            }}
          >
            {caption}
          </div>
        )}
        {source && (
          <div style={{marginTop: 24}}>
            <CitationChip source={source} onInk={onInk} />
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
