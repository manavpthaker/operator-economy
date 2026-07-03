import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * SheetScene — the render-layer storyboard screen.
 *
 * Replaces a RUN of consecutive slide beats with ONE persistent screen:
 * the section heading stays up for the whole run and each talking point
 * reveals as a numbered annotation line when its VO beat begins — the
 * same "diagram being explained" grammar as the stack's WorkingSchematic
 * node drops. The active line is at full strength; past lines settle
 * back; unspoken lines are absent.
 *
 * This kills the cut-per-talking-point problem: transitions happen
 * INSIDE the screen, not between screens.
 */

export type SheetLine = {
  title: string;
  body?: string;
  appearAtFrame: number; // relative to scene start
  startSec: number; // relative to scene start
  endSec: number; // relative to scene start
};

export type SheetSceneProps = {
  overline?: string;
  heading?: string;
  subtitle?: string;
  lines: SheetLine[];
  onInk?: boolean;
};

export const SheetScene: React.FC<SheetSceneProps> = ({overline, heading, subtitle, lines, onInk = false}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;

  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const accent = onInk ? COLORS.goldBright : COLORS.draftingBlue;
  const tick = onInk ? 'rgba(245,240,230,0.35)' : COLORS.ruleStrong;

  const overlineT = interpolate(frame, [0, 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const headingT = interpolate(frame, [4, 16], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '120px 200px 260px',
      }}
    >
      <div style={{width: '100%', maxWidth: 1520, display: 'flex', flexDirection: 'column', gap: 40}}>
        {overline && (
          <div style={{display: 'flex', alignItems: 'center', gap: 24, opacity: overlineT}}>
            <span
              style={{
                fontFamily: FONTS.mono,
                fontSize: TYPE.microLabel,
                letterSpacing: `${TRACK.caps}em`,
                textTransform: 'uppercase',
                color: accent,
                whiteSpace: 'nowrap',
              }}
            >
              {overline}
            </span>
            <span
              aria-hidden
              style={{
                flex: 1,
                height: 1,
                background: tick,
                transformOrigin: 'left center',
                transform: `scaleX(${overlineT})`,
              }}
            />
          </div>
        )}
        {heading && (
          <h2
            style={{
              fontFamily: TYPE.h2 >= 40 ? FONTS.display : FONTS.heading,
              fontWeight: 700,
              fontSize: TYPE.h2,
              lineHeight: 1.08,
              letterSpacing: `${TRACK.heading}em`,
              color: strong,
              margin: 0,
              opacity: headingT,
              transform: `translateY(${(1 - headingT) * 14}px)`,
            }}
          >
            {heading}
          </h2>
        )}
        {subtitle && (
          <p
            style={{
              fontFamily: FONTS.sans,
              fontSize: TYPE.small,
              lineHeight: 1.5,
              color: muted,
              margin: '-16px 0 0',
              opacity: headingT,
            }}
          >
            {subtitle}
          </p>
        )}
        <div style={{display: 'flex', flexDirection: 'column', gap: 36, marginTop: 8}}>
          {lines.map((line, i) => {
            // Reveal when this line's VO beat begins (frame-derived, eased).
            const inT = interpolate(frame, [line.appearAtFrame, line.appearAtFrame + 14], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
              easing: Easing.out(Easing.cubic),
            });
            // Active while its beat is speaking; settles back afterwards.
            const settle = interpolate(t, [line.endSec, line.endSec + 0.4], [1, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const emphasis = Math.min(inT, Math.max(settle, 0));
            const titleColor = strong;
            const numColor = emphasis > 0.5 ? accent : muted;
            const lineOpacity = inT * (0.62 + 0.38 * emphasis);
            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: 32,
                  opacity: lineOpacity,
                  transform: `translateX(${(1 - inT) * 14}px)`,
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
                      color: numColor,
                    }}
                  >
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <span
                    aria-hidden
                    style={{display: 'block', width: 80, height: 1, background: tick, marginTop: 12}}
                  />
                </div>
                <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 10}}>
                  <div
                    style={{
                      fontFamily: FONTS.heading,
                      fontWeight: 700,
                      fontSize: TYPE.bodyLg,
                      lineHeight: 1.2,
                      letterSpacing: `${TRACK.heading}em`,
                      color: titleColor,
                    }}
                  >
                    {line.title}
                  </div>
                  {line.body && (
                    <div
                      style={{
                        fontFamily: FONTS.sans,
                        fontWeight: 400,
                        fontSize: TYPE.body,
                        lineHeight: 1.42,
                        color: muted,
                        maxWidth: 1150,
                        // Supporting text reads full-strength only while
                        // its point is being spoken; it recedes after so
                        // the screen never competes with the captions.
                        opacity: inT * (0.3 + 0.7 * emphasis),
                      }}
                    >
                      {line.body}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
