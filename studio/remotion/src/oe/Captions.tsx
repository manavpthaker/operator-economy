import React from 'react';
import {interpolate, interpolateColors, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS} from './theme';

type Word = {word: string; start: number; end: number; highlight: boolean};
type CaptionGroup = {text: string; words: Word[]; start: number; end: number};

/**
 * Captions — Rev C caption bar. Supreme 500 (Boska is banned <40px),
 * Paper color on ink surfaces / ink-900 on paper surfaces, gold-bright
 * active-word (replaces v1 sage green), tighter measure, sunk closer to
 * the frame edge. Highlighted words stay lit; unspoken words dim.
 *
 * All color changes are derived from useCurrentFrame via interpolate /
 * interpolateColors — NEVER CSS transitions, which render
 * non-deterministically frame-to-frame and flicker.
 *
 * Groups are held on screen through inter-group gaps (up to HOLD_MAX_S)
 * so captions don't blink off between phrases.
 */

const HOLD_MAX_S = 0.45; // max seconds a group persists past its end to bridge gaps
const clampOpts = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const Captions: React.FC<{groups: CaptionGroup[]; onInk?: boolean}> = ({groups, onInk = false}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const t = frame / fps;

  // Active group: normally the group whose window contains t; between
  // groups, hold the previous group until the next one starts (capped).
  const idx = groups.findIndex((g, i) => {
    const next = groups[i + 1];
    const holdUntil = next ? Math.min(g.end + HOLD_MAX_S, next.start) : g.end + HOLD_MAX_S;
    return t >= g.start && t < Math.max(g.end, holdUntil);
  });
  const active = idx >= 0 ? groups[idx] : undefined;
  if (!active) return null;

  // Group-level opacity: 4-frame fade-in at start; fade out across the
  // hold window once the last word has been spoken (unless the next
  // group replaces it immediately — tiled speech keeps opacity at 1).
  const nextStart = idx + 1 < groups.length ? groups[idx + 1].start : Infinity;
  const fadeOutStart = Math.min(active.end + 0.12, nextStart);
  const fadeOutEnd = Math.min(active.end + HOLD_MAX_S, nextStart);
  const fadeIn = interpolate(t, [active.start, active.start + 4 / fps], [0, 1], clampOpts);
  const fadeOut = fadeOutEnd > fadeOutStart
    ? interpolate(t, [fadeOutStart, fadeOutEnd], [1, 0], clampOpts)
    : 1;
  const groupOpacity = Math.min(fadeIn, t < active.end ? 1 : fadeOut);

  const baseColor = onInk ? COLORS.onInk : COLORS.ink900;
  const dimColor = onInk ? 'rgba(245,240,230,0.42)' : 'rgba(26,26,26,0.35)';
  // Gold reads well on both ink and paper (goldOnPaper vs goldBright)
  const goldColor = onInk ? COLORS.goldBright : COLORS.goldOnPaper;

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 120,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          opacity: groupOpacity,
          maxWidth: Math.min(1500, width - 260),
          textAlign: 'center',
          fontFamily: FONTS.sans,
          fontWeight: 500,
          fontSize: 46,
          lineHeight: 1.28,
          letterSpacing: '-0.005em',
        }}
      >
        {active.words.map((w, i) => {
          // Frame-derived color ramps (deterministic per frame):
          // dim → base as the word onset arrives; base → gold while the
          // word is active; highlighted words keep gold once spoken.
          const onset = interpolate(t, [w.start - 0.12, w.start + 0.06], [0, 1], clampOpts);
          const release = w.highlight ? 1 : interpolate(t, [w.end, w.end + 0.2], [1, 0], clampOpts);
          const goldAmt = Math.min(onset, release);
          const restColor = interpolateColors(onset, [0, 1], [dimColor, baseColor]);
          const color = interpolateColors(goldAmt, [0, 1], [restColor, goldColor]);
          return (
            <span
              key={i}
              style={{
                color,
                marginRight: 12,
              }}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
