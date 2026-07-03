import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';

/**
 * RiskCard — blunt warning card. Brick-red left rule (not the accent
 * gold; risks aren't celebrated), muted-brick label, short body. Used
 * for "Revenue stops when you stop" and similar failure-mode lines.
 *
 * One brick accent + optional short list. Nothing decorative.
 */
export type RiskCardProps = {
  title: string;
  body?: string;
  bullets?: string[];
  onInk?: boolean;
};

export const RiskCard: React.FC<RiskCardProps> = ({title, body, bullets, onInk = false}) => {
  const frame = useCurrentFrame();
  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const brick = COLORS.negative;

  const labelT = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const titleT = interpolate(frame, [4, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const bodyT = interpolate(frame, [18, 34], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.standard),
  });

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '110px 200px 220px',
      }}
    >
      <div style={{maxWidth: 1400, borderLeft: `3px solid ${brick}`, paddingLeft: 48}}>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: brick,
            opacity: labelT,
            marginBottom: 22,
          }}
        >
          Risk · failure mode
        </div>
        <h2
          style={{
            fontFamily: TYPE.h2 >= 40 ? FONTS.display : FONTS.heading,
            fontWeight: 700,
            fontSize: TYPE.h2,
            lineHeight: 1.08,
            letterSpacing: `${TRACK.heading}em`,
            color: strong,
            margin: 0,
            opacity: titleT,
            transform: `translateY(${(1 - titleT) * 14}px)`,
          }}
        >
          {title}
        </h2>
        {body && (
          <p
            style={{
              marginTop: 28,
              fontFamily: FONTS.sans,
              fontSize: TYPE.bodyLg,
              lineHeight: 1.5,
              color: muted,
              maxWidth: '54ch',
              opacity: bodyT,
            }}
          >
            {body}
          </p>
        )}
        {bullets && bullets.length > 0 && (
          <div style={{marginTop: 32, display: 'flex', flexDirection: 'column', gap: 14}}>
            {bullets.map((b, i) => {
              const t = interpolate(frame, [32 + i * 6, 32 + i * 6 + 14], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
                easing: Easing.bezier(...EASE.standard),
              });
              return (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    alignItems: 'baseline',
                    gap: 20,
                    fontFamily: FONTS.sans,
                    fontSize: TYPE.body,
                    color: strong,
                    opacity: t,
                  }}
                >
                  <span
                    style={{
                      fontFamily: FONTS.mono,
                      fontSize: TYPE.microLabel,
                      color: brick,
                      letterSpacing: `${TRACK.caps}em`,
                      textTransform: 'uppercase',
                    }}
                  >
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  {b}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
