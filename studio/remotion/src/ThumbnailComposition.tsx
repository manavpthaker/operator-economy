import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COLORS, FONTS} from './oe/theme';
import {useEnsureFontsLoaded} from './oe/fonts';

/**
 * Thumbnail — YouTube episode thumbnail (2026-07-06). Designed for the
 * 320px-wide search/suggested tile, where the title-card frame dies:
 * ONE giant gold number, one counter-number, three words. Everything
 * else is noise at that size.
 *
 * Render: npx remotion still src/index.ts Thumbnail out/thumb.png
 *         --props=../originate/<slug>/render_data/thumbnail.json
 */

export type ThumbnailData = {
  variant?: 'numbers' | 'title' | 'versus'; // numbers = stacked hierarchy; title = short title card; versus = equal-weight numbers + big divider
  accentColor?: string; // override goldBright (test punchier accents without leaving the family)
  big: string;          // the hero number, e.g. "$5.9B"
  small: string;        // the counter number, e.g. "$100"
  connector?: string;   // between them, e.g. "vs" | "→"
  label: string;        // ≤4 words (numbers) or the short title lines separated by \n (title)
  accentWord?: string;  // word in label to set gold
  kicker?: string;      // tiny corner mark, default "OPERATOR BLUEPRINT · № 001"
};

const VersusVariant: React.FC<ThumbnailData> = (p) => {
  const gold = p.accentColor ?? COLORS.goldBright;
  return (
    <>
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 56,
          right: 56,
          bottom: 170,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 24,
        }}
      >
        <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 210, letterSpacing: '-0.04em', color: gold, textShadow: '0 6px 60px rgba(0,0,0,0.45)'}}>
          {p.big}
        </span>
        <span style={{fontFamily: FONTS.display, fontWeight: 700, fontStyle: 'italic', fontSize: 110, color: 'rgba(245,240,230,0.85)'}}>
          {p.connector ?? 'vs'}
        </span>
        <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 210, letterSpacing: '-0.04em', color: COLORS.paper, textShadow: '0 6px 60px rgba(0,0,0,0.45)'}}>
          {p.small}
        </span>
      </div>
      {p.label ? (
        <div
          style={{
            position: 'absolute',
            left: 56,
            right: 56,
            bottom: 48,
            borderTop: '2px solid rgba(245,240,230,0.25)',
            paddingTop: 24,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
          }}
        >
          <span style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 74, color: COLORS.paper}}>
            {p.accentWord && p.label.includes(p.accentWord) ? (
              <>
                {p.label.split(p.accentWord)[0]}
                <span style={{color: gold}}>{p.accentWord}</span>
                {p.label.split(p.accentWord)[1]}
              </>
            ) : p.label}
          </span>
          <span style={{fontFamily: FONTS.display, fontWeight: 700, fontSize: 52, color: gold}}>OE.</span>
        </div>
      ) : (
        <div style={{position: 'absolute', right: 56, bottom: 48, fontFamily: FONTS.display, fontWeight: 700, fontSize: 52, color: gold}}>OE.</div>
      )}
    </>
  );
};

const TitleVariant: React.FC<ThumbnailData> = (p) => {
  const lines = p.label.split('\\n');
  return (
    <>
      <div
        style={{
          position: 'absolute',
          top: 110,
          left: 64,
          right: 64,
          fontFamily: FONTS.display,
          fontWeight: 700,
          fontSize: 150,
          lineHeight: 1.02,
          color: COLORS.paper,
          letterSpacing: '-0.01em',
          textShadow: '0 6px 60px rgba(0,0,0,0.4)',
        }}
      >
        {lines.map((ln, i) => (
          <div key={i}>
            {p.accentWord && ln.includes(p.accentWord) ? (
              <>
                {ln.split(p.accentWord)[0]}
                <span style={{color: COLORS.goldBright}}>{p.accentWord}</span>
                {ln.split(p.accentWord)[1]}
              </>
            ) : (
              ln
            )}
          </div>
        ))}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 64,
          right: 64,
          bottom: 52,
          borderTop: '2px solid rgba(245,240,230,0.25)',
          paddingTop: 24,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
        }}
      >
        <div style={{display: 'flex', alignItems: 'baseline', gap: 28}}>
          <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 92, color: COLORS.goldBright}}>
            {p.big}
          </span>
          <span style={{fontFamily: FONTS.display, fontStyle: 'italic', fontSize: 48, color: 'rgba(245,240,230,0.6)'}}>
            {p.connector ?? 'vs'}
          </span>
          <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 92, color: COLORS.paper}}>
            {p.small}
          </span>
        </div>
        <div style={{fontFamily: FONTS.display, fontWeight: 700, fontSize: 52, color: COLORS.goldBright}}>OE.</div>
      </div>
    </>
  );
};

export const Thumbnail: React.FC<ThumbnailData> = (p) => {
  useEnsureFontsLoaded();
  const labelParts = p.accentWord && p.label.includes(p.accentWord)
    ? p.label.split(p.accentWord)
    : null;

  return (
    <AbsoluteFill style={{background: COLORS.navy, overflow: 'hidden'}}>
      {/* faint grid + a huge soft gold glow behind the hero number for
          small-size contrast pop */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(245,240,230,0.05) 1px, transparent 1px),' +
            'linear-gradient(90deg, rgba(245,240,230,0.05) 1px, transparent 1px)',
          backgroundSize: '64px 64px',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -140,
          top: -180,
          width: 900,
          height: 900,
          background: 'radial-gradient(circle, rgba(176,141,62,0.28) 0%, rgba(176,141,62,0) 62%)',
        }}
      />

      {/* kicker */}
      <div
        style={{
          position: 'absolute',
          top: 44,
          left: 56,
          fontFamily: FONTS.mono,
          fontSize: 26,
          letterSpacing: '0.16em',
          color: 'rgba(245,240,230,0.55)',
        }}
      >
        {p.kicker ?? 'OPERATOR BLUEPRINT · № 001'}
      </div>

      {p.variant === 'title' ? <TitleVariant {...p} /> : null}
      {p.variant === 'versus' ? <VersusVariant {...p} /> : null}

      {/* the number stack */}
      {(!p.variant || p.variant === 'numbers') && (
      <div
        style={{
          position: 'absolute',
          top: 96,
          left: 56,
          right: 56,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontWeight: 700,
            fontSize: 300,
            lineHeight: 0.95,
            color: p.accentColor ?? COLORS.goldBright,
            letterSpacing: '-0.03em',
            textShadow: '0 6px 60px rgba(0,0,0,0.45)',
          }}
        >
          {p.big}
        </div>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 34, marginTop: 8}}>
          <span
            style={{
              fontFamily: FONTS.display,
              fontStyle: 'italic',
              fontSize: 70,
              color: 'rgba(245,240,230,0.6)',
            }}
          >
            {p.connector ?? 'vs'}
          </span>
          <span
            style={{
              fontFamily: FONTS.mono,
              fontWeight: 700,
              fontSize: 190,
              lineHeight: 1,
              color: COLORS.paper,
              letterSpacing: '-0.02em',
            }}
          >
            {p.small}
          </span>
        </div>
      </div>

      )}

      {/* label band — bottom, full width, paper on navy via a hairline */}
      {(!p.variant || p.variant === 'numbers') && (
      <div
        style={{
          position: 'absolute',
          left: 56,
          right: 56,
          bottom: 48,
          borderTop: '2px solid rgba(245,240,230,0.25)',
          paddingTop: 26,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 600,
            fontSize: 84,
            lineHeight: 1,
            color: COLORS.paper,
          }}
        >
          {labelParts ? (
            <>
              {labelParts[0]}
              <span style={{color: COLORS.goldBright}}>{p.accentWord}</span>
              {labelParts[1]}
            </>
          ) : (
            p.label
          )}
        </div>
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 700,
            fontSize: 56,
            color: COLORS.goldBright,
          }}
        >
          OE.
        </div>
      </div>
      )}
    </AbsoluteFill>
  );
};
