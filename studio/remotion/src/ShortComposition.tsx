import React from 'react';
import {AbsoluteFill, Audio, interpolate, interpolateColors, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS} from './oe/theme';
import {useEnsureFontsLoaded} from './oe/fonts';

/**
 * Short — native 9:16 vertical (2026-07-06, replaces the letterboxed
 * 16:9 crops that "did not look good"). Designed FOR the phone frame:
 *
 *   kicker + serif title open (VO j-cuts underneath)
 *   title compacts to a top chip · big center word-highlight captions
 *   "full episode" chip at the bottom
 *   end card: wordmark + tagline while the "operator" tag stamps out
 *
 * Audio arrives pre-mixed (VO + bed + tag) from prepare_shorts.py.
 * One composition, one props JSON per short.
 */

type Word = {word: string; start: number; end: number; highlight: boolean};
type CaptionGroup = {text: string; words: Word[]; start: number; end: number};

export type ShortRenderData = {
  slug: string;
  title: string;
  kicker: string;
  audio: string; // path under public/
  duration_seconds: number;
  fps: number;
  groups: CaptionGroup[];
  end_card_seconds: number; // tail reserved for the end card
};

const clampOpts = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const TITLE_HOLD_S = 2.4; // full-size title before it compacts

const VerticalCaptions: React.FC<{groups: CaptionGroup[]}> = ({groups}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const HOLD = 0.45;

  const idx = groups.findIndex((g, i) => {
    const next = groups[i + 1];
    const holdUntil = next ? Math.min(g.end + HOLD, next.start) : g.end + HOLD;
    return t >= g.start && t < Math.max(g.end, holdUntil);
  });
  const active = idx >= 0 ? groups[idx] : undefined;
  if (!active) return null;

  const nextStart = idx + 1 < groups.length ? groups[idx + 1].start : Infinity;
  const fadeOutStart = Math.min(active.end + 0.12, nextStart);
  const fadeOutEnd = Math.min(active.end + HOLD, nextStart);
  const fadeIn = interpolate(t, [active.start, active.start + 4 / fps], [0, 1], clampOpts);
  const fadeOut = fadeOutEnd > fadeOutStart ? interpolate(t, [fadeOutStart, fadeOutEnd], [1, 0], clampOpts) : 1;
  const opacity = Math.min(fadeIn, t < active.end ? 1 : fadeOut);

  const dim = 'rgba(245,240,230,0.38)';
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          opacity,
          maxWidth: 880,
          padding: '0 70px',
          textAlign: 'center',
          fontFamily: FONTS.sans,
          fontWeight: 600,
          fontSize: 66,
          lineHeight: 1.3,
          letterSpacing: '-0.005em',
        }}
      >
        {active.words.map((w, i) => {
          const onset = interpolate(t, [w.start - 0.12, w.start + 0.06], [0, 1], clampOpts);
          const release = w.highlight ? 1 : interpolate(t, [w.end, w.end + 0.2], [1, 0], clampOpts);
          const goldAmt = Math.min(onset, release);
          const rest = interpolateColors(onset, [0, 1], [dim, COLORS.onInk]);
          const color = interpolateColors(goldAmt, [0, 1], [rest, COLORS.goldBright]);
          return (
            <span key={i} style={{color, marginRight: 16}}>
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const ShortComposition: React.FC<ShortRenderData> = (props) => {
  useEnsureFontsLoaded();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const endStart = props.duration_seconds - props.end_card_seconds;

  // Title: full-size center → compact top chip.
  const compact = interpolate(t, [TITLE_HOLD_S, TITLE_HOLD_S + 0.5], [0, 1], clampOpts);
  const endIn = interpolate(t, [endStart, endStart + 0.4], [0, 1], clampOpts);
  const contentOut = 1 - endIn;

  return (
    <AbsoluteFill style={{background: COLORS.navy}}>
      <Audio src={staticFile(props.audio)} />

      {/* faint blueprint grid, same DNA as the longform navy cards */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(245,240,230,0.045) 1px, transparent 1px),' +
            'linear-gradient(90deg, rgba(245,240,230,0.045) 1px, transparent 1px)',
          backgroundSize: '54px 54px',
        }}
      />

      {/* kicker + title (center → top chip) */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: interpolate(compact, [0, 1], [560, 96]),
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: interpolate(compact, [0, 1], [34, 14]),
          padding: '0 64px',
          opacity: contentOut,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: interpolate(compact, [0, 1], [26, 21]),
            letterSpacing: '0.14em',
            color: COLORS.goldBright,
          }}
        >
          {props.kicker}
        </div>
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 600,
            fontSize: interpolate(compact, [0, 1], [86, 40]),
            lineHeight: 1.12,
            textAlign: 'center',
            color: COLORS.paper,
            maxWidth: 920,
          }}
        >
          {props.title}
        </div>
      </div>

      {/* captions own the center once the title compacts */}
      <div style={{opacity: Math.min(compact, contentOut)}}>
        <VerticalCaptions groups={props.groups} />
      </div>

      {/* bottom chip */}
      <div
        style={{
          position: 'absolute',
          bottom: 340,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          opacity: Math.min(compact, contentOut),
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 24,
            letterSpacing: '0.1em',
            color: 'rgba(245,240,230,0.55)',
            border: '1px solid rgba(245,240,230,0.22)',
            borderRadius: 6,
            padding: '14px 26px',
          }}
        >
          FULL EPISODE → LINK BELOW
        </div>
      </div>

      {/* end card — the "operator" tag lands over this */}
      <AbsoluteFill
        style={{
          background: COLORS.navy,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 30,
          opacity: endIn,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 600,
            fontSize: 74,
            color: COLORS.paper,
            textAlign: 'center',
          }}
        >
          The Operator Economy
        </div>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 27,
            letterSpacing: '0.2em',
            color: COLORS.goldBright,
          }}
        >
          BUILD · OWN · OPERATE
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
