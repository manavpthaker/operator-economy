import React from 'react';
import {AbsoluteFill, Audio, interpolate, interpolateColors, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONTS} from './oe/theme';
import {useEnsureFontsLoaded} from './oe/fonts';
import {ScenePlayer, type Scene} from './shorts/scenes';

/**
 * Short — native 9:16 vertical.
 *
 * Two modes, chosen by whether `scenes` is present in props:
 *
 *   [v2, scenes present] Motion-graphics-native. A ScenePlayer fills the body
 *   with timed visual beats (big numbers, bar splits, stack diagrams, rings,
 *   waveforms) mapped to VO seconds. A compact top chip carries the kicker
 *   and title. Captions run as a small bottom safety net so muted viewers
 *   still catch the point.
 *
 *   [v1, no scenes] Original caption-first layout — big center word-highlight
 *   captions with a title that compacts to a top chip. Kept as fallback so
 *   older render_data JSONs still render.
 *
 * Audio arrives pre-mixed (VO + bed + tag) from prepare_shorts.py.
 */

type Word = {word: string; start: number; end: number; highlight: boolean};
type CaptionGroup = {text: string; words: Word[]; start: number; end: number};

export type ShortRenderData = {
  slug: string;
  title: string;
  kicker: string;
  audio: string; // path under public/
  duration_seconds: number;
  fps: number;
  groups: CaptionGroup[];
  end_card_seconds: number; // tail reserved for the end card
  scenes?: Scene[]; // v2: motion-graphics-native visual timeline
  cold_open_seconds?: number; // when scenes are present, how long before title compacts
};

const clampOpts = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const TITLE_HOLD_S = 2.4; // full-size title before it compacts

const VerticalCaptions: React.FC<{groups: CaptionGroup[]}> = ({groups}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const HOLD = 0.45;

  const idx = groups.findIndex((g, i) => {
    const next = groups[i + 1];
    const holdUntil = next ? Math.min(g.end + HOLD, next.start) : g.end + HOLD;
    return t >= g.start && t < Math.max(g.end, holdUntil);
  });
  const active = idx >= 0 ? groups[idx] : undefined;
  if (!active) return null;

  const nextStart = idx + 1 < groups.length ? groups[idx + 1].start : Infinity;
  const fadeOutStart = Math.min(active.end + 0.12, nextStart);
  const fadeOutEnd = Math.min(active.end + HOLD, nextStart);
  const fadeIn = interpolate(t, [active.start, active.start + 4 / fps], [0, 1], clampOpts);
  const fadeOut = fadeOutEnd > fadeOutStart ? interpolate(t, [fadeOutStart, fadeOutEnd], [1, 0], clampOpts) : 1;
  const opacity = Math.min(fadeIn, t < active.end ? 1 : fadeOut);

  const dim = 'rgba(245,240,230,0.38)';
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          opacity,
          maxWidth: 880,
          padding: '0 70px',
          textAlign: 'center',
          fontFamily: FONTS.sans,
          fontWeight: 600,
          fontSize: 66,
          lineHeight: 1.3,
          letterSpacing: '-0.005em',
        }}
      >
        {active.words.map((w, i) => {
          const onset = interpolate(t, [w.start - 0.12, w.start + 0.06], [0, 1], clampOpts);
          const release = w.highlight ? 1 : interpolate(t, [w.end, w.end + 0.2], [1, 0], clampOpts);
          const goldAmt = Math.min(onset, release);
          const rest = interpolateColors(onset, [0, 1], [dim, COLORS.onInk]);
          const color = interpolateColors(goldAmt, [0, 1], [rest, COLORS.goldBright]);
          return (
            <span key={i} style={{color, marginRight: 16}}>
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

const BottomCaptions: React.FC<{groups: CaptionGroup[]}> = ({groups}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const HOLD = 0.35;

  const idx = groups.findIndex((g, i) => {
    const next = groups[i + 1];
    const holdUntil = next ? Math.min(g.end + HOLD, next.start) : g.end + HOLD;
    return t >= g.start && t < Math.max(g.end, holdUntil);
  });
  const active = idx >= 0 ? groups[idx] : undefined;
  if (!active) return null;

  const nextStart = idx + 1 < groups.length ? groups[idx + 1].start : Infinity;
  const fadeOutStart = Math.min(active.end + 0.1, nextStart);
  const fadeOutEnd = Math.min(active.end + HOLD, nextStart);
  const fadeIn = interpolate(t, [active.start, active.start + 4 / fps], [0, 1], clampOpts);
  const fadeOut = fadeOutEnd > fadeOutStart ? interpolate(t, [fadeOutStart, fadeOutEnd], [1, 0], clampOpts) : 1;
  const opacity = Math.min(fadeIn, t < active.end ? 1 : fadeOut);
  const highlightAny = active.words.some((w) => w.highlight);
  return (
    <div
      style={{
        position: 'absolute',
        bottom: 260,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          opacity,
          maxWidth: 940,
          padding: '18px 42px',
          textAlign: 'center',
          fontFamily: FONTS.sans,
          fontWeight: 600,
          fontSize: 44,
          lineHeight: 1.25,
          background: 'rgba(20, 38, 62, 0.72)',
          border: `1px solid ${COLORS.borderOnInk}`,
          borderRadius: 4,
          color: COLORS.paper,
        }}
      >
        {active.words.map((w, i) => {
          const isHi = highlightAny ? w.highlight : false;
          const color = isHi ? COLORS.goldBright : COLORS.paper;
          return (
            <span key={i} style={{color, marginRight: 12}}>
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const ShortComposition: React.FC<ShortRenderData> = (props) => {
  useEnsureFontsLoaded();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const endStart = props.duration_seconds - props.end_card_seconds;
  const useScenes = !!(props.scenes && props.scenes.length > 0);
  // v1: title holds full-size at center then compacts to top chip (captions gate on compact).
  // v2: title compacts immediately — the ScenePlayer owns the frame from t=0 so the
  //     cold-open scene is on-screen before it, and captions run against real content.
  const compact = useScenes
    ? 1
    : interpolate(t, [TITLE_HOLD_S, TITLE_HOLD_S + 0.5], [0, 1], clampOpts);
  const endIn = interpolate(t, [endStart, endStart + 0.4], [0, 1], clampOpts);
  const contentOut = 1 - endIn;
  // v2 title fades in over the first 0.4s so t=0 isn't jarring.
  const v2TitleIn = interpolate(t, [0, 0.4], [0, 1], clampOpts);

  return (
    <AbsoluteFill style={{background: COLORS.navy}}>
      <Audio src={staticFile(props.audio)} />

      {/* faint blueprint grid, same DNA as the longform navy cards */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(245,240,230,0.045) 1px, transparent 1px),' +
            'linear-gradient(90deg, rgba(245,240,230,0.045) 1px, transparent 1px)',
          backgroundSize: '54px 54px',
        }}
      />

      {/* kicker + title (center → top chip) */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: interpolate(compact, [0, 1], [560, 96]),
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: interpolate(compact, [0, 1], [34, 14]),
          padding: '0 64px',
          opacity: contentOut * (useScenes ? v2TitleIn : 1),
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: interpolate(compact, [0, 1], [26, 21]),
            letterSpacing: '0.14em',
            color: COLORS.goldBright,
          }}
        >
          {props.kicker}
        </div>
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 600,
            fontSize: interpolate(compact, [0, 1], [86, 40]),
            lineHeight: 1.12,
            textAlign: 'center',
            color: COLORS.paper,
            maxWidth: 920,
          }}
        >
          {props.title}
        </div>
      </div>

      {/* Body: v2 → ScenePlayer + bottom captions; v1 → center captions */}
      {useScenes ? (
        <>
          <div style={{opacity: contentOut}}>
            <ScenePlayer scenes={props.scenes!} />
          </div>
          <div style={{opacity: contentOut}}>
            <BottomCaptions groups={props.groups} />
          </div>
        </>
      ) : (
        <div style={{opacity: Math.min(compact, contentOut)}}>
          <VerticalCaptions groups={props.groups} />
        </div>
      )}

      {/* bottom chip — v1 only; v2 uses captions in this band */}
      <div
        style={{
          position: 'absolute',
          bottom: 340,
          left: 0,
          right: 0,
          display: useScenes ? 'none' : 'flex',
          justifyContent: 'center',
          opacity: Math.min(compact, contentOut),
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 24,
            letterSpacing: '0.1em',
            color: 'rgba(245,240,230,0.55)',
            border: '1px solid rgba(245,240,230,0.22)',
            borderRadius: 6,
            padding: '14px 26px',
          }}
        >
          FULL EPISODE → LINK BELOW
        </div>
      </div>

      {/* end card — the "operator" tag lands over this */}
      <AbsoluteFill
        style={{
          background: COLORS.navy,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 30,
          opacity: endIn,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 600,
            fontSize: 74,
            color: COLORS.paper,
            textAlign: 'center',
          }}
        >
          The Operator Economy
        </div>
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 27,
            letterSpacing: '0.2em',
            color: COLORS.goldBright,
          }}
        >
          BUILD · OWN · OPERATE
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
