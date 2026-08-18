import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
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
 * COLD OPEN (2026-08-12). When `image` is set the sting opens on the
 * episode's own thumbnail ground and dissolves it INTO the navy over the
 * same 1.8 seconds. It is not an extra beat, and that is the whole point:
 * the constraint above still holds, nothing is added before the hook.
 *
 * Why: rendering four frames of a real episode next to its thumbnail
 * showed the two surfaces share NOTHING — photograph vs vector, Supreme
 * 800 at 196px vs Boska serif at ~48px, dense-to-the-edges vs 70-85%
 * empty, hands in frame vs no human anywhere. A viewer clicks a tactile
 * overhead photograph and lands on a silent navy slide. This is the join
 * that was missing: the thing they clicked is on screen at frame 0, and
 * they watch it become the diagram the rest of the episode is drawn in.
 *
 * TitleCard: screen-register title — episode № overline, heavy Supreme,
 * thesis line below. The paper flash between two navy worlds reads as a
 * page-turn without falling back into the document/editorial register.
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

/** The sting's wordmark, rule and tagline. Shared so the cold-open branch and
 *  the plain navy branch cannot drift apart. */
const StingType: React.FC<{
  name: string;
  tagline: string;
  wordT: number;
  ruleT: number;
  tagT: number;
}> = ({name, tagline, wordT, ruleT, tagT}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30, zIndex: 1}}>
    <h1
      style={{
        fontFamily: FONTS.display,
        fontWeight: 800,
        fontSize: 126,
        lineHeight: 1.02,
        letterSpacing: `${TRACK.display}em`,
        color: COLORS.onInk,
        margin: 0,
        textAlign: 'center',
        opacity: wordT,
        transform: `translateY(${(1 - wordT) * 16}px)`,
        // Over a photograph the wordmark needs its own separation; over navy
        // this is invisible.
        textShadow: '0 4px 30px rgba(0,0,0,0.55)',
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
        textShadow: '0 2px 18px rgba(0,0,0,0.6)',
      }}
    >
      {tagline}
    </div>
  </div>
);

export const BrandSting: React.FC<{name: string; tagline: string; image?: string}> = ({
  name,
  tagline,
  image,
}) => {
  const frame = useCurrentFrame();
  // Over a photograph the type has to arrive WITH the navy, not before it: at
  // the original 0-12 the wordmark was fully lit by frame 12 while the scrim
  // was ~20% in, which put white serif on a cream drafting table. On the plain
  // navy branch these are unchanged.
  const wordT = easeIn(frame, image ? 12 : 0, image ? 26 : 12);
  const ruleT = easeIn(frame, image ? 22 : 8, image ? 36 : 22);
  const tagT = easeIn(frame, image ? 30 : 16, image ? 44 : 28);

  // The photograph holds clean for ~8 frames so the eye registers it as the
  // thumbnail, then the navy closes over it. Grid and wordmark arrive on top of
  // the ramp rather than after it, so the two images are never separate shots.
  const scrimT = interpolate(frame, [8, 38], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  // Grid is the schematic language arriving. It is invisible over the photo and
  // full strength once the navy has landed.
  const gridT = easeIn(frame, 18, 44);

  if (image) {
    return (
      <AbsoluteFill style={{background: COLORS.navy, justifyContent: 'center', alignItems: 'center'}}>
        <Img
          src={staticFile(image)}
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            // A slow push keeps the still from reading as a freeze-frame.
            transform: `scale(${1.04 - 0.04 * scrimT})`,
            filter: `saturate(${1 - 0.45 * scrimT})`,
          }}
        />
        <AbsoluteFill style={{background: COLORS.navy, opacity: 0.92 * scrimT}} />
        <AbsoluteFill style={{...grid, opacity: gridT}} />
        <StingType name={name} tagline={tagline} wordT={wordT} ruleT={ruleT} tagT={tagT} />
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill
      style={{background: COLORS.navy, ...grid, justifyContent: 'center', alignItems: 'center'}}
    >
      <StingType name={name} tagline={tagline} wordT={wordT} ruleT={ruleT} tagT={tagT} />
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
        padding: '0 150px',
      }}
    >
      <div style={{display: 'flex', flexDirection: 'column', gap: 34, maxWidth: 1580}}>
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
            fontWeight: 800,
            fontSize: title.length > 48 ? 128 : 148,
            lineHeight: 0.96,
            letterSpacing: '-0.045em',
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
            fontWeight: 800,
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
