import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * AnnotationRail — replaces the "slide with bullets" grammar. Titles set
 * in Zodiak, then each bullet becomes an annotation line: a small-caps
 * mono label (e.g. "01 · Point", "02 · Point"), a hairline tick, the
 * body text in Supreme. Lines stagger in 120ms apart (spec: 120/200/320
 * durations), following the DS's "diagram-being-explained" motif.
 *
 * Optional overline for the section context ("STACK", "EVIDENCE").
 */
export type AnnotationRailProps = {
  title?: string;
  overline?: string;
  bullets: string[];
  onInk?: boolean;
  startFrame: number;
};

export const AnnotationRail: React.FC<AnnotationRailProps> = ({
  title,
  overline,
  bullets,
  onInk = false,
  startFrame,
}) => {
  const frame = useCurrentFrame();
  const rel = frame - startFrame;

  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const accent = onInk ? COLORS.goldBright : COLORS.draftingBlue;
  const tick = onInk ? 'rgba(245,240,230,0.35)' : COLORS.ruleStrong;

  const overlineT = interpolate(rel, [0, 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const titleT = interpolate(rel, [4, 16], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Stagger bullets: line n starts at 18 + n*4 frames (~0.13s apart)
  const perBullet = 4;
  const bulletsStart = 18;

  return (
    <div
      style={{
        width: '100%',
        maxWidth: 1520,
        display: 'flex',
        flexDirection: 'column',
        gap: 44,
      }}
    >
      {overline && (
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: accent,
            opacity: overlineT,
          }}
        >
          {overline}
        </div>
      )}
      {title && (
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
      )}
      <div style={{display: 'flex', flexDirection: 'column', gap: 24, marginTop: 12}}>
        {bullets.map((b, i) => {
          const t = interpolate(rel, [bulletsStart + i * perBullet, bulletsStart + i * perBullet + 12], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 32,
                opacity: t,
                transform: `translateX(${(1 - t) * 14}px)`,
              }}
            >
              <div
                style={{
                  flex: '0 0 auto',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  gap: 4,
                  minWidth: 96,
                }}
              >
                <span
                  style={{
                    fontFamily: FONTS.mono,
                    fontSize: TYPE.microLabel,
                    letterSpacing: `${TRACK.caps}em`,
                    textTransform: 'uppercase',
                    color: muted,
                  }}
                >
                  {String(i + 1).padStart(2, '0')}
                </span>
                <span
                  aria-hidden
                  style={{
                    display: 'block',
                    width: 80,
                    height: 1,
                    background: tick,
                    marginTop: 12,
                  }}
                />
              </div>
              <div
                style={{
                  fontFamily: FONTS.sans,
                  fontWeight: 500,
                  fontSize: TYPE.bodyLg,
                  lineHeight: 1.4,
                  color: strong,
                  flex: 1,
                  paddingTop: 2,
                }}
              >
                {b}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
