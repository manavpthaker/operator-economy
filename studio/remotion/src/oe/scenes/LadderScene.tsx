import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';
import {MonoCounter} from '../primitives/MonoCounter';
import {CitationChip} from '../primitives/CitationChip';

/**
 * LadderScene — 3-scale contrast that reads as a payoff, not a chart
 * (fixes the bare-sheet problem the research doc flagged for the
 * "Same business, three scales" moment).
 *
 * Three columns: label above / big mono figure below, hairline steps
 * ascending, gold on the peak. Reveals stagger 6 frames apart, source
 * chip lands after (secondary action).
 */
export type LadderStep = {
  label: string;      // "Freelancer/mo"
  value: number;      // 6000
  prefix?: string;    // "$"
  suffix?: string;    // "/mo"
  compactCurrency?: boolean;
};

export type LadderSceneProps = {
  overline?: string;
  heading?: string;
  steps: [LadderStep, LadderStep, LadderStep];
  source?: string;
  estimate?: boolean;
  onInk?: boolean;
};

export const LadderScene: React.FC<LadderSceneProps> = ({
  overline,
  heading,
  steps,
  source,
  estimate,
  onInk = false,
}) => {
  const frame = useCurrentFrame();
  const strong = onInk ? COLORS.onInk : COLORS.ink900;
  const muted = onInk ? COLORS.onInkMuted : COLORS.ink500;
  const accent = onInk ? COLORS.goldBright : COLORS.draftingBlue;
  const rule = onInk ? 'rgba(245,240,230,0.35)' : COLORS.ruleStrong;
  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;

  const overlineT = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const headingT = interpolate(frame, [4, 16], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  const chipT = interpolate(frame, [46, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: onInk ? COLORS.ink : COLORS.paper,
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '110px 160px 220px',
      }}
    >
      <div style={{maxWidth: 1600, width: '100%', display: 'flex', flexDirection: 'column', gap: 44}}>
        {overline && (
          <div
            style={{
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: accent,
              opacity: overlineT,
            }}
          >
            {overline}
          </div>
        )}
        {heading && (
          <h2
            style={{
              fontFamily: TYPE.h2 >= 40 ? FONTS.display : FONTS.heading,
              fontWeight: 700,
              fontSize: TYPE.h2,
              lineHeight: 1.06,
              letterSpacing: `${TRACK.heading}em`,
              color: strong,
              margin: 0,
              opacity: headingT,
              transform: `translateY(${(1 - headingT) * 14}px)`,
            }}
          >
            {heading}
          </h2>
        )}

        {/* Ascending ladder — each step is a row, hairline underline of
            increasing width, gold on the peak. */}
        <div style={{display: 'flex', flexDirection: 'column', gap: 20, marginTop: 12}}>
          {steps.map((step, i) => {
            const stepStart = 20 + i * 8;
            const t = interpolate(frame, [stepStart, stepStart + 14], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
              easing: Easing.bezier(...EASE.standard),
            });
            const isPeak = i === steps.length - 1;
            const width = 30 + i * 30; // 30% / 60% / 90%
            return (
              <div
                key={i}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '260px 1fr',
                  gap: 40,
                  alignItems: 'center',
                  opacity: t,
                  transform: `translateX(${(1 - t) * 14}px)`,
                }}
              >
                <div
                  style={{
                    fontFamily: FONTS.mono,
                    fontSize: TYPE.microLabel,
                    letterSpacing: `${TRACK.caps}em`,
                    textTransform: 'uppercase',
                    color: muted,
                  }}
                >
                  {step.label}
                </div>
                <div style={{display: 'flex', alignItems: 'center', gap: 32}}>
                  <MonoCounter
                    value={step.value}
                    prefix={step.prefix}
                    suffix={step.suffix}
                    startFrame={stepStart}
                    fontSize={TYPE.h2}
                    color={isPeak ? gold : strong}
                    compactCurrency={step.compactCurrency}
                  />
                  <span
                    aria-hidden
                    style={{
                      flex: 1,
                      height: 1,
                      background: rule,
                      transformOrigin: 'left',
                      transform: `scaleX(${t * width / 100})`,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {source && (
          <div style={{marginTop: 24, opacity: chipT}}>
            <CitationChip source={source} estimate={estimate} onInk={onInk} />
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
