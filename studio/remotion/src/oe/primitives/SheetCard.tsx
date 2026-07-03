import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * SheetCard — chapter/section transition card. Frame the section like a
 * drawing sheet: "SHEET 02 OF 07 — THE EVIDENCE". The frame hairline
 * draws itself in from left/right in the first ~0.32s; label + title
 * fade in behind it; then the whole thing dissolves after the hold.
 *
 * Placed inside a Sequence covering the first ~1.4s of each section.
 */
export type SheetCardProps = {
  sheet: number;
  total: number;
  title: string;
  subtitle?: string;
  onInk?: boolean;
  startFrame: number;
  totalFrames?: number;
};

export const SheetCard: React.FC<SheetCardProps> = ({
  sheet,
  total,
  title,
  subtitle,
  onInk = true,
  startFrame,
  totalFrames = 60, // ~2s @ 30fps
}) => {
  const frame = useCurrentFrame();
  const rel = frame - startFrame;

  // Frame hairline draws in (0-10), holds, dissolves out (last 10)
  const frameDraw = interpolate(rel, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Text fades in behind the frame (6-18) and out (totalFrames-10 → total)
  const textIn = interpolate(rel, [6, 18], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const textOut = interpolate(rel, [totalFrames - 10, totalFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Card fades IN over the outgoing scene (no hard cut) and dissolves
  // out at the end of the hold.
  const overlayIn = interpolate(rel, [0, 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const overlayOut = interpolate(rel, [totalFrames - 12, totalFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const overlay = overlayIn * overlayOut;

  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const accent = onInk ? COLORS.goldBright : COLORS.draftingBlue;
  const rule = onInk ? 'rgba(245,240,230,0.28)' : COLORS.ruleStrong;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        // Fully opaque ground — a translucent scrim ghosts the underlying
        // scene through the card (Rev C: flat surfaces, no see-through).
        background: onInk ? COLORS.navy : COLORS.paper,
        opacity: overlay,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
      }}
    >
      {/* Sheet label + hairline */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 24,
          width: '100%',
          maxWidth: 1400,
          opacity: textIn * textOut,
          marginBottom: 40,
        }}
      >
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
          Sheet {String(sheet).padStart(2, '0')} of {String(total).padStart(2, '0')}
        </span>
        <span
          aria-hidden
          style={{
            flex: 1,
            height: 1,
            background: rule,
            transformOrigin: 'left center',
            transform: `scaleX(${frameDraw})`,
          }}
        />
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
          textAlign: 'left',
          width: '100%',
          maxWidth: 1400,
          opacity: textIn * textOut,
          transform: `translateY(${(1 - textIn) * 12}px)`,
        }}
      >
        {title}
      </h2>
      {subtitle && (
        <p
          style={{
            fontFamily: FONTS.sans,
            fontSize: TYPE.bodyLg,
            lineHeight: 1.5,
            color: muted,
            margin: '20px 0 0',
            maxWidth: 1200,
            width: '100%',
            opacity: textIn * textOut,
            textAlign: 'left',
          }}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
};
