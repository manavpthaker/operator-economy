import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS} from '../oe/theme';

/**
 * Shorts v2 — motion-graphics-native scenes.
 *
 * Each scene is time-mapped to VO seconds. The dispatcher (<ScenePlayer/>) picks
 * the active scene by clock and renders it with entrance + exit windows. All
 * scenes share the OE grammar: navy ground, gold accent (max one per frame),
 * Boska display / Fragment Mono numerals, faint blueprint grid underneath.
 *
 * Primitives (sufficient to script EP002's four shorts and repeat for future ones):
 *   - bignumber   giant figure + label (kicker / sub optional)
 *   - barsplit    two-value horizontal bar comparison
 *   - counter     digit rolls from A → B while VO says the number
 *   - stack       3-box stack diagram (platform / agency / operator) with emphasis + bypass
 *   - waveform    procedural sine bars, headline overlay
 *   - stamp       text stamps in with a slight rotation (source chip, "= AI", etc.)
 *   - rings       up to 3 progress rings drawing simultaneously with labels
 *   - wordkill    strikethrough one phrase and reveal the replacement
 */

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ENTER_S = 0.35;
const EXIT_S = 0.25;

// Currency / integer formatting for counters.
const fmtMoney = (n: number) => '$' + Math.round(n).toLocaleString('en-US');
const fmtInt = (n: number) => Math.round(n).toLocaleString('en-US');

// ────────────────────────────────────────────────────────────────────────
// Scene type definitions (discriminated union). Exported so ShortComposition
// can type-check the `scenes` prop it receives from render_data.
// ────────────────────────────────────────────────────────────────────────

type SceneBase = {start: number; duration: number; kicker?: string};

export type BigNumberScene = SceneBase & {
  kind: 'bignumber';
  value: string;
  label?: string;
  sub?: string[];
  accent?: boolean;
  size?: 'hero' | 'primary' | 'medium';
};

export type BarSplitScene = SceneBase & {
  kind: 'barsplit';
  left: {value: number; label: string; sub?: string; display?: string};
  right: {value: number; label: string; sub?: string; display?: string};
  highlight?: 'left' | 'right';
  unit?: string;
};

export type CounterScene = SceneBase & {
  kind: 'counter';
  from: number;
  to: number;
  format?: 'money' | 'int';
  suffix?: string;
  label?: string;
  sub?: string;
};

export type StackScene = SceneBase & {
  kind: 'stack';
  nodes: string[];
  emphasis?: number;
  bypass?: [number, number];
  headline?: string;
};

export type WaveformScene = SceneBase & {
  kind: 'waveform';
  headline?: string;
  sub?: string;
  bars?: number;
};

export type StampScene = SceneBase & {
  kind: 'stamp';
  text: string;
  sub?: string;
  size?: 'hero' | 'primary';
};

export type RingsScene = SceneBase & {
  kind: 'rings';
  rings: {value: number; label: string; sub?: string}[];
};

export type WordkillScene = SceneBase & {
  kind: 'wordkill';
  crossed: string;
  replacement?: string;
};

export type Scene =
  | BigNumberScene
  | BarSplitScene
  | CounterScene
  | StackScene
  | WaveformScene
  | StampScene
  | RingsScene
  | WordkillScene;

// ────────────────────────────────────────────────────────────────────────
// Shared UI bits
// ────────────────────────────────────────────────────────────────────────

const KickerLabel: React.FC<{text: string}> = ({text}) => (
  <div
    style={{
      fontFamily: FONTS.mono,
      fontSize: 26,
      letterSpacing: '0.14em',
      color: COLORS.goldBright,
      textTransform: 'uppercase',
      marginBottom: 34,
    }}
  >
    {text}
  </div>
);

const SubLabel: React.FC<{text: string; muted?: boolean}> = ({text, muted}) => (
  <div
    style={{
      fontFamily: FONTS.mono,
      fontSize: 30,
      letterSpacing: '0.08em',
      color: muted ? COLORS.onInkMuted : COLORS.onInk,
      textTransform: 'uppercase',
      marginTop: 24,
    }}
  >
    {text}
  </div>
);

const CenterStack: React.FC<{
  children: React.ReactNode;
  opacity?: number;
}> = ({children, opacity = 1}) => (
  <div
    style={{
      position: 'absolute',
      inset: 0,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '0 60px',
      textAlign: 'center',
      opacity,
    }}
  >
    {children}
  </div>
);

// ────────────────────────────────────────────────────────────────────────
// Scene renderers
// ────────────────────────────────────────────────────────────────────────

const BigNumber: React.FC<{scene: BigNumberScene; t: number; fps: number; opacity: number}> = ({
  scene,
  t,
  fps,
  opacity,
}) => {
  const enterT = (t - scene.start) / ENTER_S;
  const s = spring({fps, frame: Math.max(0, (t - scene.start) * fps), config: {damping: 14, stiffness: 90}});
  const size = scene.size ?? 'primary';
  const fontSize = size === 'hero' ? 320 : size === 'primary' ? 220 : 140;
  const color = scene.accent ? COLORS.goldBright : COLORS.paper;
  const rise = interpolate(s, [0, 1], [40, 0], clamp);
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      <div
        style={{
          fontFamily: FONTS.mono,
          fontWeight: 500,
          fontSize,
          lineHeight: 1,
          color,
          letterSpacing: '-0.02em',
          transform: `translateY(${rise}px)`,
          opacity: Math.min(1, Math.max(0, enterT)),
          fontVariantNumeric: 'tabular-nums slashed-zero',
        }}
      >
        {scene.value}
      </div>
      {scene.label ? <SubLabel text={scene.label} /> : null}
      {scene.sub
        ? scene.sub.map((line, i) => (
            <div
              key={i}
              style={{
                fontFamily: FONTS.display,
                fontSize: 60,
                lineHeight: 1.15,
                marginTop: i === 0 ? 40 : 8,
                color: COLORS.onInk,
                opacity: interpolate(t, [scene.start + 0.35 + i * 0.35, scene.start + 0.7 + i * 0.35], [0, 1], clamp),
              }}
            >
              {line}
            </div>
          ))
        : null}
    </CenterStack>
  );
};

const BarSplit: React.FC<{scene: BarSplitScene; t: number; opacity: number}> = ({scene, t, opacity}) => {
  const total = scene.left.value + scene.right.value;
  const leftPct = scene.left.value / total;
  const rightPct = scene.right.value / total;
  const draw = interpolate(t, [scene.start, scene.start + 0.9], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.2, 0.9, 0.2, 1),
  });
  const goldLeft = scene.highlight === 'left';
  const goldRight = scene.highlight === 'right';
  const barH = 96;
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      <div style={{width: '90%', maxWidth: 900}}>
        {/* labels row */}
        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 24}}>
          <div style={{textAlign: 'left'}}>
            <div style={{fontFamily: FONTS.mono, fontSize: 24, letterSpacing: '0.12em', color: COLORS.onInkMuted}}>
              {scene.left.label}
            </div>
            <div
              style={{
                fontFamily: FONTS.mono,
                fontSize: 96,
                fontWeight: 500,
                color: goldLeft ? COLORS.goldBright : COLORS.paper,
                marginTop: 8,
                fontVariantNumeric: 'tabular-nums slashed-zero',
              }}
            >
              {scene.left.display ?? `${scene.left.value}${scene.unit ?? ''}`}
            </div>
            {scene.left.sub ? (
              <div style={{fontFamily: FONTS.mono, fontSize: 22, color: COLORS.onInkFaint, marginTop: 4}}>
                {scene.left.sub}
              </div>
            ) : null}
          </div>
          <div style={{textAlign: 'right'}}>
            <div style={{fontFamily: FONTS.mono, fontSize: 24, letterSpacing: '0.12em', color: COLORS.onInkMuted}}>
              {scene.right.label}
            </div>
            <div
              style={{
                fontFamily: FONTS.mono,
                fontSize: 96,
                fontWeight: 500,
                color: goldRight ? COLORS.goldBright : COLORS.paper,
                marginTop: 8,
                fontVariantNumeric: 'tabular-nums slashed-zero',
              }}
            >
              {scene.right.display ?? `${scene.right.value}${scene.unit ?? ''}`}
            </div>
            {scene.right.sub ? (
              <div style={{fontFamily: FONTS.mono, fontSize: 22, color: COLORS.onInkFaint, marginTop: 4}}>
                {scene.right.sub}
              </div>
            ) : null}
          </div>
        </div>
        {/* the split bar */}
        <div
          style={{
            display: 'flex',
            height: barH,
            border: `1px solid ${COLORS.schemNodeBorder}`,
            borderRadius: 3,
            overflow: 'hidden',
            background: COLORS.schemNodeBg,
          }}
        >
          <div
            style={{
              width: `${leftPct * 100 * draw}%`,
              background: goldLeft ? COLORS.goldFill : COLORS.paper,
              transition: 'none',
            }}
          />
          <div
            style={{
              width: `${rightPct * 100 * draw}%`,
              background: goldRight ? COLORS.goldFill : 'rgba(245,240,230,0.28)',
              borderLeft: `1px solid ${COLORS.schemNodeBorder}`,
            }}
          />
        </div>
      </div>
    </CenterStack>
  );
};

const Counter: React.FC<{scene: CounterScene; t: number; opacity: number}> = ({scene, t, opacity}) => {
  const p = interpolate(t, [scene.start + 0.2, scene.start + Math.max(1.4, scene.duration - 0.4)], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.25, 0.9, 0.25, 1),
  });
  const v = scene.from + (scene.to - scene.from) * p;
  const rendered = scene.format === 'money' ? fmtMoney(v) : fmtInt(v);
  // Auto-scale down for wide values so nothing wraps off-frame.
  const chars = (rendered + (scene.suffix ?? '')).length;
  const fontSize = chars > 9 ? 150 : chars > 6 ? 190 : 240;
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      <div
        style={{
          fontFamily: FONTS.mono,
          fontWeight: 500,
          fontSize,
          lineHeight: 1,
          color: COLORS.goldBright,
          letterSpacing: '-0.02em',
          fontVariantNumeric: 'tabular-nums slashed-zero',
          whiteSpace: 'nowrap',
          display: 'flex',
          alignItems: 'baseline',
          gap: 14,
        }}
      >
        <span>{rendered}</span>
        {scene.suffix ? (
          <span style={{fontSize: fontSize * 0.42, color: COLORS.onInk}}>{scene.suffix}</span>
        ) : null}
      </div>
      {scene.label ? <SubLabel text={scene.label} /> : null}
      {scene.sub ? (
        <div style={{fontFamily: FONTS.display, fontSize: 48, color: COLORS.onInk, marginTop: 20}}>{scene.sub}</div>
      ) : null}
    </CenterStack>
  );
};

const Stack: React.FC<{scene: StackScene; t: number; opacity: number; fps: number}> = ({scene, t, opacity, fps}) => {
  const draw = interpolate(t, [scene.start, scene.start + 0.6], [0, 1], clamp);
  // Emphasis flicker for a "watch this box" cue on middle.
  const eIdx = scene.emphasis ?? -1;
  const wobble = Math.sin((t - scene.start) * 6) * 0.5 + 0.5;
  const emphasisOpacity = eIdx >= 0 ? 0.55 + wobble * 0.45 : 1;
  const bypassP = interpolate(
    t,
    [scene.start + Math.max(0.4, scene.duration * 0.55), scene.start + scene.duration - 0.2],
    [0, 1],
    clamp,
  );
  return (
    <CenterStack opacity={opacity}>
      {scene.headline ? (
        <div
          style={{
            fontFamily: FONTS.display,
            fontSize: 60,
            color: COLORS.onInk,
            marginBottom: 40,
            maxWidth: 820,
            lineHeight: 1.2,
          }}
        >
          {scene.headline}
        </div>
      ) : null}
      <div
        style={{
          width: '82%',
          maxWidth: 780,
          display: 'flex',
          flexDirection: 'column',
          gap: 22,
          position: 'relative',
          opacity: draw,
        }}
      >
        {scene.nodes.map((n, i) => {
          const isE = i === eIdx;
          return (
            <div
              key={i}
              style={{
                border: `1px solid ${isE ? COLORS.goldBright : COLORS.schemNodeBorder}`,
                background: COLORS.schemNodeBg,
                padding: '34px 26px',
                textAlign: 'center',
                fontFamily: FONTS.mono,
                fontSize: 38,
                letterSpacing: '0.06em',
                textTransform: 'uppercase',
                color: isE ? COLORS.goldBright : COLORS.paper,
                opacity: isE ? emphasisOpacity : 1,
                borderRadius: 3,
              }}
            >
              {n}
              {/* wire between boxes */}
              {i < scene.nodes.length - 1 ? (
                <div
                  style={{
                    position: 'absolute',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    marginTop: 34,
                    height: 22,
                    width: 2,
                    background: COLORS.schemWire,
                  }}
                />
              ) : null}
            </div>
          );
        })}
        {/* bypass arrow: dashed line from the first node's right edge to the
            last node's right edge, skipping the middle. Positioned absolutely
            in the stack container so it aligns with the node rows. */}
        {scene.bypass ? (
          <div
            style={{
              position: 'absolute',
              right: -46,
              top: '10%',
              height: '80%',
              width: 40,
              opacity: bypassP,
            }}
          >
            <div
              style={{
                position: 'absolute',
                right: 12,
                top: 0,
                bottom: 0,
                width: 3,
                background: `repeating-linear-gradient(to bottom, ${COLORS.goldBright} 0 10px, transparent 10px 20px)`,
                transformOrigin: 'top',
                transform: `scaleY(${bypassP})`,
              }}
            />
            {/* top tick */}
            <div
              style={{
                position: 'absolute',
                right: 12,
                top: 0,
                width: 32,
                height: 3,
                background: COLORS.goldBright,
              }}
            />
            {/* arrowhead at the bottom */}
            <div
              style={{
                position: 'absolute',
                right: 3,
                bottom: -6,
                width: 0,
                height: 0,
                borderLeft: '10px solid transparent',
                borderRight: '10px solid transparent',
                borderTop: `18px solid ${COLORS.goldBright}`,
              }}
            />
          </div>
        ) : null}
      </div>
    </CenterStack>
  );
};

const Waveform: React.FC<{scene: WaveformScene; t: number; opacity: number}> = ({scene, t, opacity}) => {
  const n = scene.bars ?? 32;
  const local = t - scene.start;
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      {scene.headline ? (
        <div
          style={{
            fontFamily: FONTS.display,
            fontSize: 130,
            color: COLORS.paper,
            marginBottom: 60,
            letterSpacing: '-0.02em',
          }}
        >
          {scene.headline}
        </div>
      ) : null}
      <div style={{display: 'flex', alignItems: 'center', gap: 12, height: 240}}>
        {Array.from({length: n}).map((_, i) => {
          const phase = i * 0.35 + local * 4.2;
          const amp = 0.35 + 0.65 * Math.abs(Math.sin(phase));
          const gold = i === Math.floor(n / 2) || i === Math.floor(n / 2) - 1 || i === Math.floor(n / 2) + 1;
          return (
            <div
              key={i}
              style={{
                width: 12,
                height: `${amp * 100}%`,
                background: gold ? COLORS.goldBright : COLORS.paper,
                borderRadius: 2,
                opacity: 0.85,
              }}
            />
          );
        })}
      </div>
      {scene.sub ? (
        <div style={{fontFamily: FONTS.mono, fontSize: 28, color: COLORS.onInkMuted, letterSpacing: '0.12em', marginTop: 40}}>
          {scene.sub}
        </div>
      ) : null}
    </CenterStack>
  );
};

const Stamp: React.FC<{scene: StampScene; t: number; opacity: number; fps: number}> = ({scene, t, opacity, fps}) => {
  const s = spring({fps, frame: Math.max(0, (t - scene.start) * fps), config: {damping: 8, stiffness: 140, mass: 0.7}});
  const scale = interpolate(s, [0, 1], [1.35, 1], clamp);
  const rot = interpolate(s, [0, 1], [-3, -1.5], clamp);
  const size = scene.size === 'hero' ? 180 : 130;
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      <div
        style={{
          fontFamily: FONTS.display,
          fontSize: size,
          fontWeight: 700,
          color: COLORS.goldBright,
          border: `4px solid ${COLORS.goldBright}`,
          padding: '18px 46px',
          transform: `scale(${scale}) rotate(${rot}deg)`,
          letterSpacing: '-0.01em',
          borderRadius: 4,
          textTransform: 'uppercase',
        }}
      >
        {scene.text}
      </div>
      {scene.sub ? (
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 30,
            color: COLORS.onInkMuted,
            marginTop: 42,
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
          }}
        >
          {scene.sub}
        </div>
      ) : null}
    </CenterStack>
  );
};

const Rings: React.FC<{scene: RingsScene; t: number; opacity: number}> = ({scene, t, opacity}) => {
  const p = interpolate(t, [scene.start + 0.3, scene.start + Math.max(1.6, scene.duration - 0.6)], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.25, 0.9, 0.25, 1),
  });
  const size = 240;
  const stroke = 18;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      <div style={{display: 'flex', gap: 40, alignItems: 'flex-start', justifyContent: 'center'}}>
        {scene.rings.slice(0, 3).map((ring, i) => {
          const shown = Math.round(ring.value * p);
          const dash = c * (1 - (ring.value / 100) * p);
          return (
            <div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: size + 40}}>
              <svg width={size} height={size} style={{transform: 'rotate(-90deg)'}}>
                <circle cx={size / 2} cy={size / 2} r={r} stroke="rgba(245,240,230,0.14)" strokeWidth={stroke} fill="none" />
                <circle
                  cx={size / 2}
                  cy={size / 2}
                  r={r}
                  stroke={COLORS.goldBright}
                  strokeWidth={stroke}
                  fill="none"
                  strokeLinecap="round"
                  strokeDasharray={c}
                  strokeDashoffset={dash}
                />
              </svg>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 80,
                  fontWeight: 500,
                  color: COLORS.paper,
                  marginTop: -170,
                  fontVariantNumeric: 'tabular-nums slashed-zero',
                }}
              >
                {shown}%
              </div>
              <div
                style={{
                  fontFamily: FONTS.mono,
                  fontSize: 22,
                  letterSpacing: '0.12em',
                  color: COLORS.onInk,
                  textAlign: 'center',
                  marginTop: 92,
                  textTransform: 'uppercase',
                  lineHeight: 1.25,
                }}
              >
                {ring.label}
              </div>
              {ring.sub ? (
                <div style={{fontFamily: FONTS.mono, fontSize: 18, color: COLORS.onInkFaint, marginTop: 4}}>
                  {ring.sub}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
    </CenterStack>
  );
};

const Wordkill: React.FC<{scene: WordkillScene; t: number; opacity: number}> = ({scene, t, opacity}) => {
  const strikeP = interpolate(t, [scene.start + 0.4, scene.start + 1.1], [0, 1], clamp);
  const revealP = scene.replacement
    ? interpolate(t, [scene.start + 1.4, scene.start + 2.1], [0, 1], clamp)
    : 0;
  return (
    <CenterStack opacity={opacity}>
      {scene.kicker ? <KickerLabel text={scene.kicker} /> : null}
      <div
        style={{
          fontFamily: FONTS.display,
          fontSize: 82,
          lineHeight: 1.14,
          color: COLORS.onInkMuted,
          maxWidth: 900,
          position: 'relative',
          display: 'inline-block',
        }}
      >
        {scene.crossed}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: `${(1 - strikeP) * 100}%`,
            top: '54%',
            height: 6,
            background: COLORS.negative,
          }}
        />
      </div>
      {scene.replacement ? (
        <div
          style={{
            fontFamily: FONTS.display,
            fontSize: 92,
            lineHeight: 1.14,
            color: COLORS.goldBright,
            marginTop: 60,
            maxWidth: 940,
            opacity: revealP,
            transform: `translateY(${(1 - revealP) * 20}px)`,
          }}
        >
          {scene.replacement}
        </div>
      ) : null}
    </CenterStack>
  );
};

// ────────────────────────────────────────────────────────────────────────
// The dispatcher
// ────────────────────────────────────────────────────────────────────────

export const ScenePlayer: React.FC<{scenes: Scene[]}> = ({scenes}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <AbsoluteFill>
      {scenes.map((sc, i) => {
        const end = sc.start + sc.duration;
        if (t < sc.start - ENTER_S || t > end + EXIT_S) return null;
        const enter = interpolate(t, [sc.start - ENTER_S, sc.start], [0, 1], clamp);
        const exit = interpolate(t, [end - EXIT_S, end], [1, 0], clamp);
        const opacity = t >= end - EXIT_S ? exit : enter;
        switch (sc.kind) {
          case 'bignumber':
            return <BigNumber key={i} scene={sc} t={t} fps={fps} opacity={opacity} />;
          case 'barsplit':
            return <BarSplit key={i} scene={sc} t={t} opacity={opacity} />;
          case 'counter':
            return <Counter key={i} scene={sc} t={t} opacity={opacity} />;
          case 'stack':
            return <Stack key={i} scene={sc} t={t} opacity={opacity} fps={fps} />;
          case 'waveform':
            return <Waveform key={i} scene={sc} t={t} opacity={opacity} />;
          case 'stamp':
            return <Stamp key={i} scene={sc} t={t} opacity={opacity} fps={fps} />;
          case 'rings':
            return <Rings key={i} scene={sc} t={t} opacity={opacity} />;
          case 'wordkill':
            return <Wordkill key={i} scene={sc} t={t} opacity={opacity} />;
          default:
            return null;
        }
      })}
    </AbsoluteFill>
  );
};
