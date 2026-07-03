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

export type LadderItemEvent = {atFrame: number; index: number};
export type LadderFocusEvent = {atFrame: number; index: number};

export type LadderSceneProps = {
  overline?: string;
  heading?: string;
  steps: [LadderStep, LadderStep, LadderStep];
  source?: string;
  estimate?: boolean;
  onInk?: boolean;
  /** Steps 1+ wait on their pace event. Step 0 lands with the heading. */
  itemEvents?: LadderItemEvent[];
  /** Re-highlight step `index` — lift + brighten, others recede. */
  focusEvents?: LadderFocusEvent[];
};

export const LadderScene: React.FC<LadderSceneProps> = ({
  overline,
  heading,
  steps,
  source,
  estimate,
  onInk = false,
  itemEvents = [],
  focusEvents = [],
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
            // Step 0 lands with the heading; steps 1+ wait on pace events.
            // If an event is missing, the step stays ABSENT (spec: never
            // dimmed-then-appears — viewer reads "faded" as "coming").
            let stepStart: number | null = i === 0 ? 20 : null;
            const ev = itemEvents.find((e) => e.index === i);
            if (ev) stepStart = ev.atFrame;
            if (stepStart === null) return null;
            const t = interpolate(frame, [stepStart, stepStart + 14], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
              easing: Easing.bezier(...EASE.standard),
            });
            const isPeak = i === steps.length - 1;
            const width = 30 + i * 30; // 30% / 60% / 90%

            // Focus events: this step re-highlights (lift + brighten) OR
            // recedes with the others.
            let focusScale = 1;
            let focusYOffset = 0;
            let dimAmt = 0;
            for (const ev2 of focusEvents) {
              const fRel = frame - ev2.atFrame;
              if (fRel < 0 || fRel > 30) continue;
              const amp = interpolate(fRel, [0, 6, 24, 30], [0, 1, 1, 0], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              if (ev2.index === i) {
                focusScale = 1 + 0.02 * amp;
                focusYOffset = -4 * amp;
              } else {
                dimAmt = Math.max(dimAmt, amp);
              }
            }

            return (
              <div
                key={i}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '260px 1fr',
                  gap: 40,
                  alignItems: 'center',
                  opacity: t * (1 - 0.3 * dimAmt),
                  transform: `translateX(${(1 - t) * 14}px) translateY(${focusYOffset}px) scale(${focusScale})`,
                  transformOrigin: 'left center',
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
