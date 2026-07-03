import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';

/**
 * QuoteCard — the impact-frame primitive.
 *
 * Full-screen single statement in Boska on ink or navy. HARD cut in
 * (no fade — the parent Sequence has 0 pre-fade for quote screens),
 * spring scale-settle 0.96 → 1, holds 1.2–2.5s for short lines and
 * 3–4s for longer ones. Captions are HIDDEN during the screen (the
 * card IS the caption — duplication is a rubric kill list item).
 *
 * L-cut convention: the VO continues under the card as normal. The
 * parent composition arranges music.intensity=silence and a hit SFX
 * cue at the screen start.
 *
 * Rev C constraints: Boska 700 ≥40px (we go 96–140px), one accent
 * (gold-on-ink) only on the optional accent phrase, corners flat.
 */
export type QuoteCardProps = {
  quote: string;
  accentPhrase?: string; // an inline fragment rendered in gold-bright
  attribution?: string;  // optional small caption below
  onInk?: boolean;
};

export const QuoteCard: React.FC<QuoteCardProps> = ({
  quote,
  accentPhrase,
  attribution,
  onInk = true,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Spring scale-settle: 0.96 → 1 over ~14 frames, spring config sets
  // damping high so the card doesn't overshoot (Rev C — no bounce).
  const s = spring({
    frame,
    fps,
    config: {damping: 200, stiffness: 100, mass: 1.2},
    durationInFrames: 14,
  });
  const scale = interpolate(s, [0, 1], [0.96, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Text opacity: fade in over 8 frames with entrance easing.
  const opacity = interpolate(frame, [0, 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.entrance),
  });
  // Underline draws in on longer holds (secondary action).
  const under = interpolate(frame, [14, 26], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.standard),
  });

  const bg = onInk ? COLORS.ink : COLORS.paper;
  const text = onInk ? COLORS.onInk : COLORS.ink900;
  const rule = onInk ? 'rgba(245,240,230,0.35)' : COLORS.ruleStrong;
  const gold = onInk ? COLORS.goldBright : COLORS.goldOnPaper;
  const attrColor = onInk ? COLORS.onInkMuted : COLORS.ink500;

  // If the quote has an accent phrase, render it inline with gold.
  const rendered = React.useMemo(() => {
    if (!accentPhrase || !quote.includes(accentPhrase)) {
      return <>{quote}</>;
    }
    const [before, ...rest] = quote.split(accentPhrase);
    return (
      <>
        {before}
        <span style={{color: gold}}>{accentPhrase}</span>
        {rest.join(accentPhrase)}
      </>
    );
  }, [quote, accentPhrase, gold]);

  return (
    <AbsoluteFill
      style={{
        background: bg,
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 160px',
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          maxWidth: 1600,
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 900,
            fontSize: quote.length > 60 ? TYPE.h1 * 0.72 : TYPE.h1,
            lineHeight: 1.06,
            letterSpacing: `${TRACK.display}em`,
            color: text,
          }}
        >
          {rendered}
        </div>
        <div
          style={{
            width: `${under * 160}px`,
            height: 2,
            background: rule,
            margin: '32px auto 0',
          }}
        />
        {attribution && (
          <div
            style={{
              marginTop: 24,
              fontFamily: FONTS.mono,
              fontSize: TYPE.microLabel,
              letterSpacing: `${TRACK.caps}em`,
              textTransform: 'uppercase',
              color: attrColor,
            }}
          >
            {attribution}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
