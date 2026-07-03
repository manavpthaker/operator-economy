import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, EASE, FONTS, TRACK, TYPE} from '../theme';

/**
 * QuoteCard — the impact-frame primitive.
 *
 * Full-screen single statement in Boska on one of three grounds. HARD
 * cut in (no fade — the parent Sequence has 0 pre-fade for quote
 * screens), spring scale-settle 0.96 → 1, holds 1.2–2.5s for short
 * lines and 3–4s for longer ones. Captions are HIDDEN during the
 * screen (the card IS the caption — duplication is a rubric kill list
 * item).
 *
 * L-cut convention: the VO continues under the card as normal. The
 * parent composition arranges music.intensity=silence and a hit SFX
 * cue at the screen start.
 *
 * Rev C constraint (one accent per frame — rotate GROUNDS, not
 * accents): the ground rotates by narrative role, gold stays as the
 * single accent color across all three:
 *   - ink   (#1A1A1A):  thesis / cold-open impact lines
 *   - navy  (#14263E):  evidence turning-points — carries the drafting
 *                       grid so the "we are inside the schematic" world
 *                       is continuous with the WorkingSchematic panel
 *   - paper (#F5F0E6):  economics honest-math lines, ink text
 *
 * Boska stays weight 900. ChapterReset stays on ink (`ground=ink`).
 */
export type QuoteGround = 'ink' | 'navy' | 'paper';

export type QuoteCardProps = {
  quote: string;
  accentPhrase?: string; // an inline fragment rendered in gold
  attribution?: string;  // optional small caption below
  ground?: QuoteGround;
  /** @deprecated — pass `ground` instead. Kept for storyboard back-compat. */
  onInk?: boolean;
};

export const QuoteCard: React.FC<QuoteCardProps> = ({
  quote,
  accentPhrase,
  attribution,
  ground,
  onInk = true,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Resolve ground: explicit `ground` wins; otherwise fall back to the
  // legacy `onInk` boolean (`true` → ink, `false` → paper).
  const effectiveGround: QuoteGround = ground ?? (onInk ? 'ink' : 'paper');

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

  // Ground → colors. Gold stays the single accent across all three.
  const isDarkGround = effectiveGround !== 'paper';
  const bg =
    effectiveGround === 'navy' ? COLORS.navy
    : effectiveGround === 'paper' ? COLORS.paper
    : COLORS.ink;
  const text = isDarkGround ? COLORS.onInk : COLORS.ink900;
  const rule = isDarkGround ? 'rgba(245,240,230,0.35)' : COLORS.ruleStrong;
  const gold = isDarkGround ? COLORS.goldBright : COLORS.goldOnPaper;
  const attrColor = isDarkGround ? COLORS.onInkMuted : COLORS.ink500;

  // Navy ground carries the drafting grid — makes the evidence quote
  // read as an annotation inside the WorkingSchematic world rather
  // than as a separate title slide (research doc §"impact frames as
  // continuous with the world, not intercuts").
  const gridStyle: React.CSSProperties | undefined = effectiveGround === 'navy'
    ? {
        backgroundImage:
          `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px), ` +
          `repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px)`,
      }
    : undefined;

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
        ...gridStyle,
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
