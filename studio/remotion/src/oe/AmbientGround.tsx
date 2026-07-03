import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COLORS} from './theme';

/**
 * AmbientGround — the subtle global life on every non-impact screen.
 * A slow scale drift 1.000 → 1.018 over the screen's duration on the
 * content wrapper, plus (on navy grounds) a 2–4px grid parallax so the
 * drafting grid isn't visually locked to the content behind it.
 *
 * Impact frames (quote/chapter_reset) opt OUT via `enabled={false}` —
 * their stillness IS the effect.
 *
 * The wrapper is transparent — content passes through untouched. Only
 * the transform is applied.
 */
export type AmbientGroundProps = {
  enabled?: boolean;
  durationInFrames: number;
  /** When true, layer a subtle grid parallax under the content. This
   *  only reads on navy grounds — on paper/ink there is no grid to
   *  parallax against. */
  gridParallax?: boolean;
  children: React.ReactNode;
};

const DRIFT_START = 1.0;
const DRIFT_END = 1.018;

export const AmbientGround: React.FC<AmbientGroundProps> = ({
  enabled = true,
  durationInFrames,
  gridParallax = false,
  children,
}) => {
  const frame = useCurrentFrame();
  if (!enabled) return <AbsoluteFill>{children}</AbsoluteFill>;

  // Linear drift so the accumulated change is a slow, steady breath —
  // no acceleration, no bounce.
  const scale = interpolate(frame, [0, durationInFrames], [DRIFT_START, DRIFT_END], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Grid parallax: 2–4px translation over the screen duration, opposite
  // direction from the content drift so the layers separate.
  const gridOffset = gridParallax
    ? interpolate(frame, [0, durationInFrames], [0, -3], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 0;

  return (
    <AbsoluteFill>
      {gridParallax && (
        <AbsoluteFill
          aria-hidden
          style={{
            backgroundImage:
              `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px), ` +
              `repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px)`,
            transform: `translate(${gridOffset}px, ${gridOffset}px)`,
            pointerEvents: 'none',
          }}
        />
      )}
      <AbsoluteFill
        style={{
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
