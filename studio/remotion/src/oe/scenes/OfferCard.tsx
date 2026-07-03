import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';
import {CitationChip} from '../primitives/CitationChip';

/**
 * OfferCard — problem / deliverable / price / deadline as one card.
 *
 * Used for the "Missed calls get answered and booked" moment in №001
 * playbook: shows the shape of what the operator actually SELLS, in
 * concrete language. Fields flip from placeholder to filled with a
 * mono numeral pop for the price.
 */
export type OfferItemEvent = {atFrame: number; index: number};

export type OfferCardProps = {
  problem: string;      // "Missed calls at hotels"
  deliverable: string;  // "Callback + booked in Airtable"
  price: string;        // "$2,000 fixed"
  deadline: string;     // "14 days"
  source?: string;
  onInk?: boolean;
  /** Gate row[i] on {block:'offer',index:i}. Row 0 lands with the
   *  card header; rows 1+ wait on their events. */
  itemEvents?: OfferItemEvent[];
};

export const OfferCard: React.FC<OfferCardProps> = ({
  problem,
  deliverable,
  price,
  deadline,
  source,
  onInk = false,
  itemEvents = [],
}) => {
  const frame = useCurrentFrame();
  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;
  const rule = onInk ? 'rgba(245,240,230,0.35)' : COLORS.rule;
  const cardBg = onInk ? 'rgba(245,240,230,0.06)' : COLORS.paperLifted;

  const rows = [
    {label: 'Problem', value: problem, mono: false, gold: false},
    {label: 'Deliverable', value: deliverable, mono: false, gold: false},
    {label: 'Price', value: price, mono: true, gold: true},
    {label: 'Deadline', value: deadline, mono: true, gold: false},
  ];

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
      }}
    >
      <div
        style={{
          width: 1200,
          border: `1.5px solid ${rule}`,
          background: cardBg,
          padding: '60px 80px',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: muted,
            marginBottom: 8,
            opacity: interpolate(frame, [0, 10], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        >
          Offer template · One page
        </div>
        <div
          style={{
            width: 96,
            height: 2,
            background: gold,
            marginBottom: 40,
            transformOrigin: 'left',
            transform: `scaleX(${interpolate(frame, [4, 18], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })})`,
          }}
        />
        {rows.map((row, i) => {
          // Row 0 lands with the card header. Rows 1+ wait on their
          // pace event; if absent, don't render (paces come in as
          // Problem→Deliverable→Price→Deadline).
          let startFrame: number | null = i === 0 ? 14 : null;
          const ev = itemEvents.find((e) => e.index === i);
          if (ev) startFrame = ev.atFrame;
          if (startFrame === null) return null;
          const t = interpolate(frame, [startFrame, startFrame + 14], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(...EASE.standard),
          });
          return (
            <div
              key={row.label}
              style={{
                display: 'grid',
                gridTemplateColumns: '260px 1fr',
                gap: 32,
                padding: '20px 0',
                borderTop: i === 0 ? 'none' : `1px solid ${rule}`,
                opacity: t,
                transform: `translateY(${(1 - t) * 8}px)`,
              }}
            >
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: TYPE.microLabel,
                  letterSpacing: `${TRACK.caps}em`,
                  textTransform: 'uppercase',
                  color: muted,
                  paddingTop: 6,
                }}
              >
                {row.label}
              </div>
              <div
                style={{
                  fontFamily: row.mono ? FONTS.mono : FONTS.sans,
                  fontWeight: row.mono ? 400 : 500,
                  fontSize: row.mono ? TYPE.h3 : TYPE.bodyLg,
                  letterSpacing: row.mono ? `${TRACK.mono}em` : 'normal',
                  color: row.gold ? gold : strong,
                  lineHeight: 1.24,
                }}
              >
                {row.value}
              </div>
            </div>
          );
        })}
        {source && (
          <div
            style={{
              marginTop: 40,
              opacity: interpolate(frame, [50, 62], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              }),
            }}
          >
            <CitationChip source={source} onInk={onInk} />
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
