import React from 'react';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';
import {MonoCounter} from './MonoCounter';

/**
 * StatBlock — a single published figure with an optional label above.
 * Wraps MonoCounter so the numeral animates in with a spring; the label
 * fades in slightly ahead of the numeral (small-caps, mono).
 */
export type StatBlockProps = {
  value: number;
  prefix?: string;
  suffix?: string;
  label?: string;
  compactCurrency?: boolean;
  onInk?: boolean;
  emphasis?: 'default' | 'gold';
  size?: 'md' | 'lg' | 'xl';
  startFrame: number;
  align?: 'left' | 'center';
};

const SIZE_PX = {md: 68, lg: 92, xl: 128} as const;

export const StatBlock: React.FC<StatBlockProps> = ({
  value,
  prefix,
  suffix,
  label,
  compactCurrency = false,
  onInk = false,
  emphasis = 'default',
  size = 'lg',
  startFrame,
  align = 'left',
}) => {
  const numeralColor =
    emphasis === 'gold'
      ? onInk
        ? COLORS.goldBright
        : COLORS.goldOnPaper
      : onInk
        ? COLORS.onInk
        : COLORS.ink900;
  const labelColor = onInk ? COLORS.onInkMuted : COLORS.ink500;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: align === 'center' ? 'center' : 'flex-start',
        gap: 12,
      }}
    >
      {label && (
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            fontWeight: 400,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: labelColor,
          }}
        >
          {label}
        </div>
      )}
      <MonoCounter
        value={value}
        prefix={prefix}
        suffix={suffix}
        startFrame={startFrame}
        fontSize={SIZE_PX[size]}
        color={numeralColor}
        compactCurrency={compactCurrency}
        align={align === 'center' ? 'center' : 'left'}
      />
    </div>
  );
};
