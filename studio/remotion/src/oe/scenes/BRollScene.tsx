import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * BRollScene — until Phase 2 wires actual footage in, this is a legible
 * placeholder styled Rev C: ink ground, monochrome mono "PENDING B-ROLL"
 * label with the search query framed like a shot list ticket. Slight
 * scale drift so it doesn't sit dead. Once fetch_broll.py is wired to
 * originate/*, this scene will accept a source_video URL and render an
 * OffthreadVideo desaturated + tinted ink.
 */
export type BRollSceneProps = {
  searchQuery: string;
  caption?: string;
  startFrame: number;
};

export const BRollScene: React.FC<BRollSceneProps> = ({searchQuery, caption, startFrame}) => {
  const frame = useCurrentFrame();
  const rel = frame - startFrame;
  const fadeIn = interpolate(rel, [0, 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const drift = interpolate(rel, [0, 120], [1.0, 1.04], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill
      style={{
        background: COLORS.ink,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          border: `1px solid ${COLORS.borderOnInk}`,
          padding: '48px 64px',
          maxWidth: 1300,
          opacity: fadeIn,
          transform: `scale(${drift})`,
          transformOrigin: 'center',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: COLORS.goldBright,
            marginBottom: 28,
          }}
        >
          Pending b-roll
        </div>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 46,
            color: COLORS.onInk,
            lineHeight: 1.2,
            fontFeatureSettings: "'tnum' 1",
          }}
        >
          &ldquo;{searchQuery}&rdquo;
        </div>
        {caption && (
          <div
            style={{
              fontFamily: FONTS.sans,
              fontSize: TYPE.body,
              color: COLORS.onInkMuted,
              marginTop: 28,
            }}
          >
            {caption}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
