import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COLORS, FONTS} from './oe/theme';
import {useEnsureFontsLoaded} from './oe/fonts';

/**
 * CarouselSlide — LinkedIn document/carousel stills (2026-07-06).
 * 1080×1350 (4:5), one slide per props JSON, rendered via
 * `npx remotion still`. Same brand system as the episode.
 *
 * Layouts: cover | statement | stat | list | cta
 */

export type CarouselSlideData = {
  layout: 'cover' | 'statement' | 'stat' | 'list' | 'cta';
  kicker?: string;
  title?: string;
  subtitle?: string;
  statement?: string;
  accent?: string; // gold phrase inside statement (exact substring)
  stat?: {value: string; label: string};
  items?: {lead: string; detail?: string}[];
  source?: string;
  footer?: string;
  page?: string; // "3 / 10"
  ground?: 'paper' | 'navy';
};

const Grid: React.FC<{onNavy: boolean}> = ({onNavy}) => (
  <AbsoluteFill
    style={{
      backgroundImage: onNavy
        ? 'linear-gradient(rgba(245,240,230,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(245,240,230,0.045) 1px, transparent 1px)'
        : 'linear-gradient(rgba(26,26,26,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(26,26,26,0.035) 1px, transparent 1px)',
      backgroundSize: '54px 54px',
    }}
  />
);

const withAccent = (text: string, accent: string | undefined, gold: string) => {
  if (!accent || !text.includes(accent)) return <>{text}</>;
  const [pre, post] = text.split(accent);
  return (
    <>
      {pre}
      <span style={{color: gold}}>{accent}</span>
      {post}
    </>
  );
};

export const CarouselSlide: React.FC<CarouselSlideData> = (p) => {
  useEnsureFontsLoaded();
  const navy = p.ground === 'navy';
  const ink = navy ? COLORS.paper : '#1A1A1A';
  const dim = navy ? 'rgba(245,240,230,0.62)' : 'rgba(26,26,26,0.6)';
  const gold = navy ? COLORS.goldBright : COLORS.goldOnPaper;
  const rule = navy ? 'rgba(245,240,230,0.18)' : 'rgba(26,26,26,0.15)';

  return (
    <AbsoluteFill style={{background: navy ? COLORS.navy : COLORS.paper, padding: 84}}>
      <Grid onNavy={navy} />

      {/* header */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{fontFamily: FONTS.mono, fontSize: 24, letterSpacing: '0.14em', color: gold}}>
          {p.kicker ?? 'THE OPERATOR ECONOMY'}
        </div>
        {p.page && (
          <div style={{fontFamily: FONTS.mono, fontSize: 22, color: dim}}>{p.page}</div>
        )}
      </div>

      {/* body */}
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 44}}>
        {p.layout === 'cover' && (
          <>
            <div style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 100, lineHeight: 1.06, color: ink}}>
              {p.title}
            </div>
            {p.subtitle && (
              <div style={{fontFamily: FONTS.sans, fontSize: 40, lineHeight: 1.35, color: dim, maxWidth: 800}}>
                {p.subtitle}
              </div>
            )}
          </>
        )}

        {p.layout === 'statement' && (
          <div style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 84, lineHeight: 1.12, color: ink}}>
            {withAccent(p.statement ?? '', p.accent, gold)}
          </div>
        )}

        {p.layout === 'stat' && (
          <>
            <div style={{fontFamily: FONTS.mono, fontSize: 190, lineHeight: 1, color: gold}}>
              {p.stat?.value}
            </div>
            <div style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 62, lineHeight: 1.15, color: ink, maxWidth: 860}}>
              {p.stat?.label}
            </div>
            {p.statement && (
              <div style={{fontFamily: FONTS.sans, fontSize: 36, lineHeight: 1.4, color: dim, maxWidth: 840}}>
                {withAccent(p.statement, p.accent, gold)}
              </div>
            )}
          </>
        )}

        {p.layout === 'list' && (
          <>
            {p.title && (
              <div style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 66, lineHeight: 1.1, color: ink, marginBottom: 10}}>
                {p.title}
              </div>
            )}
            <div style={{display: 'flex', flexDirection: 'column'}}>
              {(p.items ?? []).map((it, i) => (
                <div key={i} style={{display: 'flex', gap: 30, padding: '30px 0', borderTop: `1px solid ${rule}`, alignItems: 'baseline'}}>
                  <div style={{fontFamily: FONTS.mono, fontSize: 26, color: gold, minWidth: 54}}>
                    {String(i + 1).padStart(2, '0')}
                  </div>
                  <div>
                    <div style={{fontFamily: FONTS.heading, fontSize: 40, color: ink, lineHeight: 1.25}}>{it.lead}</div>
                    {it.detail && (
                      <div style={{fontFamily: FONTS.sans, fontSize: 30, color: dim, lineHeight: 1.4, marginTop: 8}}>{it.detail}</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {p.layout === 'cta' && (
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: 40}}>
            <div style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 86, lineHeight: 1.1, color: ink}}>
              {p.title}
            </div>
            {p.subtitle && (
              <div style={{fontFamily: FONTS.sans, fontSize: 38, lineHeight: 1.4, color: dim, maxWidth: 820}}>
                {p.subtitle}
              </div>
            )}
            <div style={{fontFamily: FONTS.mono, fontSize: 30, letterSpacing: '0.2em', color: gold, marginTop: 20}}>
              BUILD · OWN · OPERATE
            </div>
          </div>
        )}
      </div>

      {/* footer */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{fontFamily: FONTS.mono, fontSize: 22, color: dim}}>{p.footer ?? 'theoperatoreconomy.com'}</div>
        {p.source && (
          <div style={{fontFamily: FONTS.mono, fontSize: 20, color: dim, border: `1px solid ${rule}`, borderRadius: 5, padding: '8px 14px'}}>
            SOURCE {p.source}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
