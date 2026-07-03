import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS} from './theme';

type Word = {word: string; start: number; end: number; highlight: boolean};
type CaptionGroup = {text: string; words: Word[]; start: number; end: number};

/**
 * Captions — Rev C caption bar. Supreme 500 (Boska is banned <40px),
 * Paper color on ink surfaces / ink-900 on paper surfaces, gold-bright
 * active-word (replaces v1 sage green), tighter measure, sunk closer to
 * the frame edge. Highlighted words stay lit; unspoken words dim.
 *
 * Placement is bottom of the frame with a dark scrim gradient underneath
 * so captions survive against paper-ground scenes without shipping a
 * full opaque bar.
 */
export const Captions: React.FC<{groups: CaptionGroup[]; onInk?: boolean}> = ({groups, onInk = false}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const t = frame / fps;
  const active = groups.find((g) => t >= g.start && t <= g.end);
  if (!active) return null;

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
          const spoken = t >= w.start;
          const isActive = t >= w.start && t <= w.end;
          const color = spoken
            ? w.highlight || isActive
              ? goldColor
              : baseColor
            : dimColor;
          return (
            <span
              key={i}
              style={{
                color,
                marginRight: 12,
                transition: 'color 90ms linear',
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
