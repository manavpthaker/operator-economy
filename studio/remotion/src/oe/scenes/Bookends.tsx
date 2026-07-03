import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * Bookends — the episode's opening and closing cards (2026-07-03).
 *
 * BrandSting  → TitleCard  → [episode]  → OutroCard
 *
 * BrandSting: wordmark on Schematic Navy + drafting grid, gold hairline
 * draws, tagline lands. Short (≈1.8s) — it's a sting, not an intro;
 * retention research punishes long pre-hook branding.
 *
 * TitleCard: Paper editorial print — episode № overline, Boska 900
 * title, thesis line below. The paper flash between two navy worlds
 * reads as a page-turn.
 *
 * OutroCard: navy + grid, brand line + domain + CTA rows. Composition
 * keeps the lower-right clear-ish for YouTube end-screen overlays.
 */

const grid: React.CSSProperties = {
  backgroundImage:
    `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px), ` +
    `repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px)`,
};

const easeIn = (frame: number, a: number, b: number) =>
  interpolate(frame, [a, b], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

// ---------------------------------------------------------------------

export const BrandSting: React.FC<{name: string; tagline: string}> = ({name, tagline}) => {
  const frame = useCurrentFrame();
  const wordT = easeIn(frame, 0, 12);
  const ruleT = easeIn(frame, 8, 22);
  const tagT = easeIn(frame, 16, 28);
  return (
    <AbsoluteFill
      style={{background: COLORS.navy, ...grid, justifyContent: 'center', alignItems: 'center'}}
    >
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30}}>
        <h1
          style={{
            fontFamily: FONTS.display,
            fontWeight: 900,
            fontSize: 118,
            lineHeight: 1.02,
            letterSpacing: `${TRACK.display}em`,
            color: COLORS.onInk,
            margin: 0,
            textAlign: 'center',
            opacity: wordT,
            transform: `translateY(${(1 - wordT) * 16}px)`,
          }}
        >
          {name}
        </h1>
        <div style={{width: `${ruleT * 260}px`, height: 2, background: COLORS.goldBright}} />
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel + 4,
            letterSpacing: `${TRACK.caps + 0.08}em`,
            textTransform: 'uppercase',
            color: COLORS.onInkMuted,
            opacity: tagT,
          }}
        >
          {tagline}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------

export const TitleCard: React.FC<{
  overline?: string; // "OPERATOR BLUEPRINT · № 001"
  title: string;
  thesis?: string;
}> = ({overline, title, thesis}) => {
  const frame = useCurrentFrame();
  const overT = easeIn(frame, 0, 10);
  const titleT = easeIn(frame, 6, 20);
  const thesisT = easeIn(frame, 18, 32);
  return (
    <AbsoluteFill
      style={{
        background: COLORS.paper,
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '0 220px',
      }}
    >
      <div style={{display: 'flex', flexDirection: 'column', gap: 40, maxWidth: 1480}}>
        {overline && (
          <div style={{display: 'flex', alignItems: 'center', gap: 24, opacity: overT}}>
            <span
              style={{
                fontFamily: FONTS.mono,
                fontSize: TYPE.microLabel,
                letterSpacing: `${TRACK.caps}em`,
                textTransform: 'uppercase',
                color: COLORS.goldOnPaper,
                whiteSpace: 'nowrap',
              }}
            >
              {overline}
            </span>
            <span
              aria-hidden
              style={{
                width: 120,
                height: 1,
                background: COLORS.ruleStrong,
                transformOrigin: 'left center',
                transform: `scaleX(${overT})`,
              }}
            />
          </div>
        )}
        <h1
          style={{
            fontFamily: FONTS.display,
            fontWeight: 900,
            fontSize: title.length > 48 ? 104 : 124,
            lineHeight: 1.04,
            letterSpacing: `${TRACK.display}em`,
            color: COLORS.ink900,
            margin: 0,
            opacity: titleT,
            transform: `translateY(${(1 - titleT) * 18}px)`,
          }}
        >
          {title}
        </h1>
        {thesis && (
          <p
            style={{
              fontFamily: FONTS.sans,
              fontSize: TYPE.bodyLg,
              lineHeight: 1.4,
              color: COLORS.ink500,
              margin: 0,
              maxWidth: 1200,
              opacity: thesisT,
            }}
          >
            {thesis}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------

export const OutroCard: React.FC<{
  brand: string;
  tagline: string;
  url: string;
  ctas: string[];
}> = ({brand, tagline, url, ctas}) => {
  const frame = useCurrentFrame();
  const brandT = easeIn(frame, 0, 12);
  const urlT = easeIn(frame, 10, 22);
  return (
    <AbsoluteFill
      style={{
        background: COLORS.navy,
        ...grid,
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '0 200px',
      }}
    >
      <div style={{display: 'flex', flexDirection: 'column', gap: 44, maxWidth: 1200}}>
        <h2
          style={{
            fontFamily: FONTS.display,
            fontWeight: 900,
            fontSize: 96,
            lineHeight: 1.04,
            letterSpacing: `${TRACK.display}em`,
            color: COLORS.onInk,
            margin: 0,
            opacity: brandT,
            transform: `translateY(${(1 - brandT) * 14}px)`,
          }}
        >
          {tagline}
        </h2>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 40,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: COLORS.goldBright,
            opacity: urlT,
          }}
        >
          {url}
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: 20}}>
          {ctas.map((cta, i) => {
            const t = easeIn(frame, 20 + i * 8, 32 + i * 8);
            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 20,
                  opacity: t,
                  transform: `translateX(${(1 - t) * 12}px)`,
                }}
              >
                <span style={{width: 40, height: 1, background: 'rgba(245,240,230,0.35)'}} />
                <span
                  style={{
                    fontFamily: FONTS.sans,
                    fontSize: TYPE.body,
                    color: COLORS.onInkMuted,
                  }}
                >
                  {cta}
                </span>
              </div>
            );
          })}
        </div>
        <div
          style={{
            marginTop: 8,
            fontFamily: FONTS.mono,
            fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`,
            textTransform: 'uppercase',
            color: COLORS.onInkMuted,
            opacity: easeIn(frame, 40, 52),
          }}
        >
          {brand}
        </div>
      </div>
    </AbsoluteFill>
  );
};
