import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * GapArrow — the signature move ("$5.9B → $2K"). The origin figure lands
 * first (spring in), then the arrow strokes to the right, then the
 * destination figure lands in gold. Optional bracket label underneath.
 *
 * One per composition. Ink-world (hook) or paper-world (economics)
 * treatment via onInk.
 */
export type GapArrowProps = {
  from: string;
  to: string;
  label?: string;
  onInk?: boolean;
  startFrame: number;
  size?: 'lg' | 'xl';
};

const SIZE_PX = {lg: 96, xl: 138} as const;

export const GapArrow: React.FC<GapArrowProps> = ({
  from,
  to,
  label,
  onInk = false,
  startFrame,
  size = 'xl',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rel = frame - startFrame;

  const fromT = spring({frame: rel, fps, config: {damping: 200, stiffness: 90}, durationInFrames: 18});
  // Arrow starts drawing 12 frames after origin appears
  const arrowT = interpolate(rel, [12, 26], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Destination spring lands after arrow finishes
  const toT = spring({frame: rel - 22, fps, config: {damping: 180, stiffness: 90}, durationInFrames: 20});
  const labelT = interpolate(rel, [40, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;
  const base = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const rule = onInk ? 'rgba(245,240,230,0.4)' : COLORS.ruleStrong;
  const px = SIZE_PX[size];

  return (
    <div style={{display: 'inline-flex', flexDirection: 'column', alignItems: 'center'}}>
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'baseline',
          gap: 28,
          fontFamily: FONTS.mono,
          fontWeight: 400,
          fontSize: px,
          lineHeight: 1,
          letterSpacing: `-0.02em`,
          fontFeatureSettings: "'tnum' 1",
          whiteSpace: 'nowrap',
        }}
      >
        <span
          style={{
            color: base,
            opacity: fromT,
            transform: `translateY(${(1 - fromT) * 12}px)`,
            display: 'inline-block',
          }}
        >
          {from}
        </span>
        <span
          aria-hidden
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            width: 96,
            height: px * 0.55,
            position: 'relative',
          }}
        >
          <span
            style={{
              position: 'absolute',
              left: 0,
              top: '50%',
              width: `${arrowT * 100}%`,
              height: 2,
              background: gold,
              transform: 'translateY(-50%)',
            }}
          />
          {/* Arrowhead */}
          <span
            style={{
              position: 'absolute',
              right: `${100 - arrowT * 100}%`,
              top: '50%',
              width: 0,
              height: 0,
              borderTop: '10px solid transparent',
              borderBottom: '10px solid transparent',
              borderLeft: `14px solid ${gold}`,
              transform: 'translate(2px, -50%)',
              opacity: arrowT > 0.85 ? 1 : 0,
            }}
          />
        </span>
        <span
          style={{
            color: gold,
            opacity: toT,
            transform: `translateY(${(1 - toT) * 12}px)`,
            display: 'inline-block',
          }}
        >
          {to}
        </span>
      </div>
      {label && (
        <div style={{marginTop: 22, opacity: labelT, width: '58%'}}>
          <div
            aria-hidden
            style={{
              height: 10,
              border: `1px solid ${rule}`,
              borderTop: 'none',
            }}
          />
          <div
            style={{
              textAlign: 'center',
              marginTop: 12,
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.label}em`,
              textTransform: 'uppercase',
              color: muted,
            }}
          >
            {label}
          </div>
        </div>
      )}
    </div>
  );
};
