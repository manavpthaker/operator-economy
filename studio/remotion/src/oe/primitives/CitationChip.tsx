import React from 'react';
import {COLORS, FONTS, RADIUS, TRACK, TYPE} from '../theme';

/**
 * CitationChip — THE signature element. Every published figure gets one.
 * Left-rule accent color communicates the chip's role:
 *   - onInk / default:      gold-bright (video lower-third on ink/navy)
 *   - onInk / estimate:     gold-bright + "ESTIMATE" label
 *   - onPaper / default:    drafting-blue
 *   - onPaper / estimate:   gold-on-paper
 */
export type CitationChipProps = {
  source: string;
  date?: string;
  estimate?: boolean;
  onInk?: boolean;
  style?: React.CSSProperties;
};

export const CitationChip: React.FC<CitationChipProps> = ({
  source,
  date,
  estimate = false,
  onInk = false,
  style,
}) => {
  const label = estimate ? 'ESTIMATE' : 'SOURCE';
  const accent = onInk
    ? COLORS.goldBright
    : estimate
      ? COLORS.goldOnPaper
      : COLORS.draftingBlue;

  const bg = onInk ? 'rgba(26,26,26,0.82)' : COLORS.paperLifted;
  const color = onInk ? COLORS.onInk : COLORS.ink700;
  const border = onInk ? `1px solid ${COLORS.borderOnInk}` : `1px solid ${COLORS.rule}`;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 10,
        padding: '8px 14px',
        fontFamily: FONTS.mono,
        fontSize: TYPE.citation,
        fontWeight: 400,
        letterSpacing: `${TRACK.mono}em`,
        borderRadius: RADIUS.xs,
        borderLeft: `2px solid ${accent}`,
        background: bg,
        color,
        border,
        lineHeight: 1.3,
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      <span
        style={{
          fontSize: TYPE.microLabel,
          letterSpacing: `${TRACK.caps}em`,
          color: accent,
        }}
      >
        {label}
      </span>
      <span style={{opacity: onInk ? 0.92 : 1}}>
        {source}
        {date ? ` · ${date}` : ''}
      </span>
    </span>
  );
};
