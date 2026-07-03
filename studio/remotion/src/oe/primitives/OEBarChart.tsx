import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';
import {CitationChip} from './CitationChip';

/**
 * OEBarChart — the Rev C bar chart: hairline baseline, mono value labels
 * (tabular), one optional gold highlight bar (max value or first
 * highlight={true} entry). Bars grow with a spring keyed off startFrame.
 * Renders a citation chip inline when `source` is provided.
 *
 * Adapts to onInk vs. onPaper surfaces via `onInk`.
 */
export type BarDatum = {label: string; value: number; highlight?: boolean};
export type OEBarChartProps = {
  title?: string;
  data: BarDatum[];
  unit?: string; // "$" | "%" | "" — placed on the number
  compactCurrency?: boolean;
  source?: string;
  estimate?: boolean;
  onInk?: boolean;
  startFrame: number;
  chartHeight?: number;
};

const compactValue = (v: number, unit = '') => {
  const abs = Math.abs(v);
  if (abs >= 1_000_000_000) return `${(v / 1_000_000_000).toFixed(1).replace(/\.0$/, '')}B${unit}`;
  if (abs >= 1_000_000) return `${(v / 1_000_000).toFixed(1).replace(/\.0$/, '')}M${unit}`;
  if (abs >= 10_000) return `${Math.round(v / 1000)}K${unit}`;
  if (abs >= 1000) return `${(v / 1000).toFixed(1).replace(/\.0$/, '')}K${unit}`;
  return `${Math.round(v).toLocaleString()}${unit}`;
};

export const OEBarChart: React.FC<OEBarChartProps> = ({
  title,
  data,
  unit = '',
  compactCurrency = false,
  source,
  estimate = false,
  onInk = false,
  startFrame,
  chartHeight = 540,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rel = frame - startFrame;
  const growth = spring({frame: rel - 8, fps, config: {damping: 200, stiffness: 60}, durationInFrames: 34});

  const max = Math.max(...data.map((d) => d.value), 1);
  // If nobody flagged a highlight, gold the largest bar (the "one gold" per DS).
  const anyHl = data.some((d) => d.highlight);
  const goldIdx = anyHl ? data.findIndex((d) => d.highlight) : data.findIndex((d) => d.value === max);

  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const baseline = onInk ? 'rgba(245,240,230,0.7)' : COLORS.ink900;
  const barColor = onInk ? '#6E8FB8' : COLORS.draftingBlue; // slightly lighter blue on ink
  const goldColor = onInk ? COLORS.goldBright : COLORS.goldFill;
  const goldText = onInk ? COLORS.goldBright : COLORS.goldOnPaper;

  const titleIn = interpolate(rel, [0, 12], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const fmt = (v: number) => {
    if (compactCurrency) return compactValue(v, '');
    return `${unit}${Math.round(v).toLocaleString()}`;
  };

  return (
    <div
      style={{
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        gap: 40,
      }}
    >
      {title && (
        <h2
          style={{
            fontFamily: TYPE.h2 >= 40 ? FONTS.display : FONTS.heading,
            fontWeight: 700,
            fontSize: 52,
            lineHeight: 1.08,
            letterSpacing: `${TRACK.heading}em`,
            color: strong,
            margin: 0,
            opacity: titleIn,
            transform: `translateY(${(1 - titleIn) * 10}px)`,
            maxWidth: '90%',
          }}
        >
          {title}
        </h2>
      )}
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: 56,
          height: chartHeight,
          borderBottom: `2px solid ${baseline}`,
          paddingBottom: 0,
        }}
      >
        {data.map((d, i) => {
          const isGold = i === goldIdx;
          const finalH = (d.value / max) * 100;
          const h = Math.max(finalH * growth, 0.5);
          const shownValue = d.value * growth;
          return (
            <div
              key={i}
              style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-end',
                alignItems: 'center',
                height: '100%',
              }}
            >
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 34,
                  fontWeight: 400,
                  color: isGold ? goldText : strong,
                  marginBottom: 16,
                  fontFeatureSettings: "'tnum' 1, 'zero' 1",
                  whiteSpace: 'nowrap',
                  opacity: Math.min(1, growth * 1.3),
                }}
              >
                {fmt(shownValue)}
              </div>
              <div
                style={{
                  width: '100%',
                  maxWidth: 220,
                  height: `${h}%`,
                  background: isGold ? goldColor : barColor,
                  minHeight: 3,
                }}
              />
            </div>
          );
        })}
      </div>
      <div style={{display: 'flex', gap: 56, marginTop: -14}}>
        {data.map((d, i) => (
          <div
            key={i}
            style={{
              flex: 1,
              textAlign: 'center',
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: muted,
              opacity: titleIn,
            }}
          >
            {d.label}
          </div>
        ))}
      </div>
      {source && (
        <div style={{marginTop: 12, opacity: titleIn}}>
          <CitationChip source={source} estimate={estimate} onInk={onInk} />
        </div>
      )}
    </div>
  );
};
