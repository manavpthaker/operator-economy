import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';
import {CitationChip} from '../primitives/CitationChip';

/**
 * CaseFile — problem → workflow → result. Used when the beat describes
 * a specific engagement: the shape lets viewers see the pattern.
 *
 * Three rows on a lifted paper card with an engineering-title-block
 * feel: doc-style header, hairline separators, mono labels.
 */
export type CaseFileProps = {
  reference?: string; // "Case 001"
  problem: string;
  workflow: string;
  result: string;
  source?: string;
  onInk?: boolean;
};

export const CaseFile: React.FC<CaseFileProps> = ({
  reference = 'Case 001',
  problem,
  workflow,
  result,
  source,
  onInk = false,
}) => {
  const frame = useCurrentFrame();
  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const rule = onInk ? 'rgba(245,240,230,0.28)' : COLORS.ruleStrong;
  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;
  const cardBg = onInk ? 'rgba(245,240,230,0.04)' : COLORS.paperLifted;

  const chipT = interpolate(frame, [46, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const rows = [
    {label: 'Problem', value: problem, gold: false},
    {label: 'Workflow', value: workflow, gold: false},
    {label: 'Result', value: result, gold: true},
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
          width: 1400,
          border: `1.5px solid ${rule}`,
          background: cardBg,
          padding: '48px 64px',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderBottom: `1px solid ${rule}`,
            paddingBottom: 20,
            marginBottom: 32,
          }}
        >
          <span
            style={{
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: muted,
            }}
          >
            {reference}
          </span>
          <span
            style={{
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: gold,
            }}
          >
            Case file
          </span>
        </div>
        {rows.map((row, i) => {
          const startFrame = 10 + i * 10;
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
                gridTemplateColumns: '200px 1fr',
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
                  paddingTop: 4,
                }}
              >
                {row.label}
              </div>
              <div
                style={{
                  fontFamily: FONTS.sans,
                  fontWeight: 500,
                  fontSize: TYPE.body,
                  lineHeight: 1.35,
                  color: row.gold ? gold : strong,
                }}
              >
                {row.value}
              </div>
            </div>
          );
        })}
        {source && (
          <div style={{marginTop: 32, opacity: chipT}}>
            <CitationChip source={source} onInk={onInk} />
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
