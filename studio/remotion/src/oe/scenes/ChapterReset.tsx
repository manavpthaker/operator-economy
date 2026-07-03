import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';

/**
 * ChapterReset — a short section transition card. Captions are HIDDEN
 * (rubric §VII kill list) because the card IS the caption for the
 * transition moment. Renders a mono kicker + Boska heading centered on
 * ink; hairline expands underneath. Silence in the audio bed timed to
 * this screen makes the reset feel like an edit, not a title slide.
 */
export type ChapterResetProps = {
  kicker?: string; // "SHEET 04 OF 07"
  heading: string; // "The stack"
  onInk?: boolean;
};

export const ChapterReset: React.FC<ChapterResetProps> = ({kicker, heading, onInk = true}) => {
  const frame = useCurrentFrame();
  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const rule = onInk ? 'rgba(245,240,230,0.35)' : COLORS.ruleStrong;
  const accent = onInk ? COLORS.goldBright : COLORS.draftingBlue;

  const kickT = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const headT = interpolate(frame, [6, 22], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const ruleT = interpolate(frame, [20, 34], [0, 1], {
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
        padding: '0 160px',
      }}
    >
      {kicker && (
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: accent,
            opacity: kickT,
            marginBottom: 40,
          }}
        >
          {kicker}
        </div>
      )}
      <h2
        style={{
          fontFamily: FONTS.display,
          fontWeight: 900,
          fontSize: TYPE.h1,
          lineHeight: 1.04,
          letterSpacing: `${TRACK.display}em`,
          color: strong,
          margin: 0,
          textAlign: 'center',
          opacity: headT,
          transform: `translateY(${(1 - headT) * 14}px)`,
        }}
      >
        {heading}
      </h2>
      <div
        style={{
          width: `${ruleT * 320}px`,
          height: 1,
          background: rule,
          marginTop: 36,
        }}
      />
    </AbsoluteFill>
  );
};
