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
  beat?: number;         // for gating body fragments on {kind:'fragment',beat,index}
  ordinal?: number;      // per-section running number ACROSS sheet screens
                         // (prepare_longform) — fixes every screen showing "01"
  title: string;
  body?: string;
  appearAtFrame: number; // relative to scene start
  startSec: number;
  endSec: number;
};

export type SheetFragmentEvent = {atFrame: number; beat: number; index: number};
export type SheetPulseEvent = {atFrame: number; word: string};

export type SheetSceneProps = {
  overline?: string;
  heading?: string;
  subtitle?: string;
  lines: SheetLine[];
  onInk?: boolean;
  /** From pace_storyboard: fragment `index` in reveal `beat`'s body
   *  appears at atFrame (sequence-local). Fragment 0 shows with the
   *  reveal itself; the rest are ABSENT until their event fires. */
  fragmentEvents?: SheetFragmentEvent[];
  /** Brief accent underline flash on the active line. */
  pulseEvents?: SheetPulseEvent[];
};

const FRAG_IN_FRAMES = 12;

/**
 * BodyFragments — the body of a sheet line, "·"-separated. Fragment 0
 * shows with the reveal itself; each subsequent fragment is ABSENT until
 * its fragment event fires, then fades in with an 8px rise.
 *
 * A pulse event flashes a gold underline across the last-active fragment
 * on the currently-active line — subtle accent, ~60% opacity peak,
 * settles over 20 frames. Never moves layout.
 */
const BodyFragments: React.FC<{
  body: string;
  beat: number | undefined;
  lineInT: number;
  lineEmphasis: number;
  color: string;
  accent: string;
  frame: number;
  lineAppearAtFrame: number;
  fragmentEvents: SheetFragmentEvent[];
  pulseEvents: SheetPulseEvent[];
  isActive: boolean;
}> = ({body, beat, lineInT, lineEmphasis, color, accent, frame, lineAppearAtFrame, fragmentEvents, pulseEvents, isActive}) => {
  const parts = body.split(' · ');
  const fragsForBeat = beat !== undefined
    ? fragmentEvents.filter((e) => e.beat === beat)
    : [];

  // Pulse: only fires on the ACTIVE line and within a small window of the
  // pulse event. Underline sweeps in and fades out over ~20 frames.
  let pulseOpacity = 0;
  if (isActive) {
    for (const p of pulseEvents) {
      const rel = frame - p.atFrame;
      if (rel >= 0 && rel <= 22) {
        const o = interpolate(rel, [0, 6, 22], [0, 0.6, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        if (o > pulseOpacity) pulseOpacity = o;
      }
    }
  }

  return (
    <div
      style={{
        fontFamily: FONTS.sans,
        fontWeight: 400,
        fontSize: TYPE.body,
        lineHeight: 1.42,
        color,
        maxWidth: 1150,
        // Body base opacity: full strength while active, receding after.
        opacity: lineInT * (0.3 + 0.7 * lineEmphasis),
        position: 'relative',
      }}
    >
      {parts.map((part, i) => {
        // Fragment 0 shows with the reveal; the rest gate on events.
        let fragT = 0;
        if (i === 0) {
          fragT = interpolate(frame, [lineAppearAtFrame, lineAppearAtFrame + FRAG_IN_FRAMES], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.out(Easing.cubic),
          });
        } else {
          const evForIndex = fragsForBeat.find((e) => e.index === i);
          if (evForIndex) {
            fragT = interpolate(frame, [evForIndex.atFrame, evForIndex.atFrame + FRAG_IN_FRAMES], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
              easing: Easing.out(Easing.cubic),
            });
          }
          // If no event yet, fragT stays 0 → absent (not dimmed).
        }
        if (fragT <= 0) return null;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <span style={{opacity: fragT}}> · </span>
            )}
            <span
              style={{
                display: 'inline-block',
                opacity: fragT,
                transform: `translateY(${(1 - fragT) * 8}px)`,
              }}
            >
              {part}
            </span>
          </React.Fragment>
        );
      })}
      {pulseOpacity > 0 && (
        <div
          aria-hidden
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            bottom: -6,
            height: 2,
            background: accent,
            opacity: pulseOpacity,
            transformOrigin: 'left',
          }}
        />
      )}
    </div>
  );
};

export const SheetScene: React.FC<SheetSceneProps> = ({
  overline,
  heading,
  subtitle,
  lines,
  onInk = false,
  fragmentEvents = [],
  pulseEvents = [],
}) => {
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
                    {String(line.ordinal ?? i + 1).padStart(2, '0')}
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
                    <BodyFragments
                      body={line.body}
                      beat={line.beat}
                      lineInT={inT}
                      lineEmphasis={emphasis}
                      color={muted}
                      accent={accent}
                      frame={frame}
                      lineAppearAtFrame={line.appearAtFrame}
                      fragmentEvents={fragmentEvents}
                      pulseEvents={pulseEvents}
                      isActive={emphasis > 0.5}
                    />
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
