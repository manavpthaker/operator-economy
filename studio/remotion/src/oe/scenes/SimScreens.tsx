import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS, TRACK, TYPE} from '../theme';

/**
 * SimScreens (2026-07-04) — the "tool shots": simulated screen
 * recordings BUILT AS CODE, not generated video. AI video models garble
 * UI text; these are pixel-crisp, factually controllable, and honest —
 * every sim carries a "RECONSTRUCTION" chip (evidence-first ethos: we
 * never pass a simulation off as a capture).
 *
 * Three kinds, routed via screen.custom.sim.kind:
 *   workflow  — n8n-style canvas; nodes execute left→right, wires pulse
 *   dashboard — Airtable-style table; booking rows populate live
 *   assistant — Claude-style panel; a draft streams in
 *
 * All time-normalized: pacing derives from the screen's duration.
 * Research doc shot hierarchy tier 2: "generated/constructed artifact
 * that represents the exact workflow."
 */

// ---------------------------------------------------------------------
// Shared chrome
// ---------------------------------------------------------------------

const ease = (frame: number, a: number, b: number) =>
  interpolate(frame, [a, b], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

const grid: React.CSSProperties = {
  backgroundImage:
    `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px), ` +
    `repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 36px)`,
};

const AppFrame: React.FC<{
  title: string;
  label: string; // lower-third: "n8n · WORKFLOW RECONSTRUCTION"
  dark?: boolean;
  children: React.ReactNode;
}> = ({title, label, dark = true, children}) => {
  const frame = useCurrentFrame();
  const inT = ease(frame, 0, 12);
  return (
    <AbsoluteFill style={{background: COLORS.navy, ...grid, justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          width: 1460,
          borderRadius: 12,
          overflow: 'hidden',
          border: '1px solid rgba(245,240,230,0.14)',
          boxShadow: '0 30px 80px rgba(0,0,0,0.45)',
          opacity: inT,
          transform: `translateY(${(1 - inT) * 18}px)`,
          background: dark ? '#1E1F24' : '#FFFFFF',
        }}
      >
        <div
          style={{
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '14px 20px',
            background: dark ? '#26272D' : '#F3F2EF',
            borderBottom: dark ? '1px solid #33343B' : '1px solid #E4E2DC',
          }}
        >
          {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => (
            <span key={c} style={{width: 12, height: 12, borderRadius: 6, background: c}} />
          ))}
          <span
            style={{
              marginLeft: 16, fontFamily: FONTS.sans, fontSize: 20,
              color: dark ? 'rgba(245,240,230,0.7)' : '#5B584F',
            }}
          >
            {title}
          </span>
        </div>
        {children}
      </div>
      <div
        style={{
          position: 'absolute', left: 120, bottom: 148,
          display: 'flex', alignItems: 'center', gap: 14,
          opacity: ease(frame, 10, 22),
        }}
      >
        <span style={{width: 34, height: 1, background: COLORS.goldBright}} />
        <span
          style={{
            fontFamily: FONTS.mono, fontSize: TYPE.microLabel,
            letterSpacing: `${TRACK.caps}em`, textTransform: 'uppercase',
            color: COLORS.onInkMuted,
          }}
        >
          {label} · reconstruction
        </span>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// 1) workflow — n8n-style execution canvas
// ---------------------------------------------------------------------

export type SimNode = {label: string; sub?: string};

export const WorkflowSim: React.FC<{
  title?: string;
  label?: string;
  nodes: SimNode[];
  durationFrames: number;
}> = ({title = 'workflow — missed-call rescue', label = 'n8n', nodes, durationFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  // Execution cascade: nodes fire sequentially across the middle 70%.
  const t0 = Math.round(durationFrames * 0.12);
  const span = Math.round(durationFrames * 0.7);
  const per = span / Math.max(nodes.length, 1);

  return (
    <AppFrame title={title} label={label} dark>
      <div style={{display: 'flex', alignItems: 'center', gap: 0, padding: '90px 60px 60px'}}>
        {nodes.map((n, i) => {
          const fire = t0 + i * per;
          const lit = ease(frame, fire, fire + 10);
          const done = ease(frame, fire + per * 0.75, fire + per * 0.75 + 8);
          return (
            <React.Fragment key={i}>
              {i > 0 && (
                <div style={{position: 'relative', width: 92, height: 2, background: '#3A3B42'}}>
                  <div
                    style={{
                      position: 'absolute', inset: 0,
                      background: COLORS.goldBright,
                      transformOrigin: 'left center',
                      transform: `scaleX(${ease(frame, fire - per * 0.35, fire)})`,
                    }}
                  />
                </div>
              )}
              <div
                style={{
                  flex: 1, minWidth: 0,
                  border: `1.5px solid ${lit > 0.5 ? COLORS.goldBright : '#3A3B42'}`,
                  borderRadius: 10,
                  padding: '26px 24px',
                  background: lit > 0.5 ? 'rgba(196,164,95,0.08)' : '#26272D',
                  transform: `scale(${1 + lit * 0.02})`,
                }}
              >
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <span
                    style={{
                      fontFamily: FONTS.heading, fontWeight: 700, fontSize: 26,
                      color: 'rgba(245,240,230,0.94)', whiteSpace: 'nowrap',
                      overflow: 'hidden', textOverflow: 'ellipsis',
                    }}
                  >
                    {n.label}
                  </span>
                  <span
                    style={{
                      fontFamily: FONTS.mono, fontSize: 20,
                      color: done > 0.5 ? '#28C840' : 'rgba(245,240,230,0.35)',
                      opacity: Math.max(done, 0.5),
                    }}
                  >
                    {done > 0.5 ? '✓' : '·'}
                  </span>
                </div>
                {n.sub && (
                  <div
                    style={{
                      marginTop: 8, fontFamily: FONTS.mono, fontSize: 18,
                      color: 'rgba(245,240,230,0.45)', whiteSpace: 'nowrap',
                      overflow: 'hidden', textOverflow: 'ellipsis',
                    }}
                  >
                    {n.sub}
                  </div>
                )}
              </div>
            </React.Fragment>
          );
        })}
      </div>
      <div
        style={{
          margin: '0 60px 40px', padding: '16px 22px',
          background: '#17181C', borderRadius: 8,
          fontFamily: FONTS.mono, fontSize: 19, color: 'rgba(245,240,230,0.55)',
        }}
      >
        {(() => {
          const done = nodes.filter((_, i) => frame > t0 + i * per + per * 0.75).length;
          const running = Math.min(nodes.length, Math.max(done + (frame > t0 ? 1 : 0), 0));
          const secs = ((frame / fps)).toFixed(1);
          return `▸ run #482 · ${done}/${nodes.length} nodes complete · ${secs}s`;
        })()}
      </div>
    </AppFrame>
  );
};

// ---------------------------------------------------------------------
// 2) dashboard — Airtable-style table, rows populate
// ---------------------------------------------------------------------

export type SimRow = string[]; // cells

export const DashboardSim: React.FC<{
  title?: string;
  label?: string;
  columns: string[];
  rows: SimRow[];
  durationFrames: number;
}> = ({title = 'Bookings — client dashboard', label = 'Airtable', columns, rows, durationFrames}) => {
  const frame = useCurrentFrame();
  const t0 = Math.round(durationFrames * 0.15);
  const span = Math.round(durationFrames * 0.6);
  const per = span / Math.max(rows.length, 1);
  const pill = (v: string) =>
    v === 'Booked' ? {bg: '#DFF5E3', fg: '#1F7A34'} :
    v === 'Callback sent' ? {bg: '#E8ECFD', fg: '#3350C8'} :
    v === 'New' ? {bg: '#FDF2DA', fg: '#9A6B15'} : null;

  return (
    <AppFrame title={title} label={label} dark={false}>
      <div style={{padding: '30px 40px 46px'}}>
        <div style={{display: 'flex', borderBottom: '2px solid #E4E2DC', padding: '12px 8px'}}>
          {columns.map((c, i) => (
            <div
              key={i}
              style={{
                flex: i === 0 ? 1.4 : 1,
                fontFamily: FONTS.mono, fontSize: 18,
                letterSpacing: `${TRACK.caps}em`, textTransform: 'uppercase',
                color: '#8A867C',
              }}
            >
              {c}
            </div>
          ))}
        </div>
        {rows.map((r, ri) => {
          const at = t0 + ri * per;
          const inT = ease(frame, at, at + 9);
          return (
            <div
              key={ri}
              style={{
                display: 'flex', alignItems: 'center',
                padding: '16px 8px',
                borderBottom: '1px solid #EFEDE8',
                opacity: inT,
                transform: `translateY(${(1 - inT) * 8}px)`,
                background: inT > 0 && inT < 1 ? 'rgba(196,164,95,0.10)' : 'transparent',
              }}
            >
              {r.map((cell, ci) => {
                const p = pill(cell);
                return (
                  <div key={ci} style={{flex: ci === 0 ? 1.4 : 1}}>
                    {p ? (
                      <span
                        style={{
                          fontFamily: FONTS.sans, fontSize: 20, fontWeight: 600,
                          background: p.bg, color: p.fg,
                          padding: '5px 14px', borderRadius: 999,
                        }}
                      >
                        {cell}
                      </span>
                    ) : (
                      <span style={{fontFamily: ci === r.length - 1 ? FONTS.mono : FONTS.sans, fontSize: 22, color: '#3B3830'}}>
                        {cell}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
    </AppFrame>
  );
};

// ---------------------------------------------------------------------
// 3) assistant — Claude-style panel, response streams
// ---------------------------------------------------------------------

export const AssistantSim: React.FC<{
  title?: string;
  label?: string;
  prompt: string;
  response: string;
  durationFrames: number;
}> = ({title = 'Claude', label = 'Claude', prompt, response, durationFrames}) => {
  const frame = useCurrentFrame();
  const promptT = ease(frame, Math.round(durationFrames * 0.06), Math.round(durationFrames * 0.12));
  const streamStart = Math.round(durationFrames * 0.2);
  const streamEnd = Math.round(durationFrames * 0.82);
  const chars = Math.round(
    interpolate(frame, [streamStart, streamEnd], [0, response.length], {
      extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    }),
  );
  return (
    <AppFrame title={title} label={label} dark>
      <div style={{padding: '44px 70px 54px', minHeight: 520}}>
        <div
          style={{
            marginLeft: 'auto', maxWidth: 760,
            background: '#33343B', borderRadius: 14,
            padding: '20px 26px',
            fontFamily: FONTS.sans, fontSize: 23, lineHeight: 1.45,
            color: 'rgba(245,240,230,0.92)',
            opacity: promptT,
            transform: `translateY(${(1 - promptT) * 10}px)`,
          }}
        >
          {prompt}
        </div>
        <div
          style={{
            marginTop: 34, maxWidth: 1080,
            fontFamily: FONTS.sans, fontSize: 23, lineHeight: 1.55,
            color: 'rgba(245,240,230,0.85)',
            whiteSpace: 'pre-wrap',
          }}
        >
          {response.slice(0, chars)}
          {chars > 0 && chars < response.length && (
            <span style={{opacity: frame % 16 < 8 ? 1 : 0, color: COLORS.goldBright}}>▍</span>
          )}
        </div>
      </div>
    </AppFrame>
  );
};
