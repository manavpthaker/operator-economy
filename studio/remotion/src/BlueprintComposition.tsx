import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

import {useEnsureFontsLoaded} from './oe/fonts';
import {COLORS, EASE, KEN_BURNS} from './oe/theme';
import {Captions} from './oe/Captions';
import {SoundBed} from './oe/SoundBed';
import {AmbientGround} from './oe/AmbientGround';
import {WorkingSchematic, SchematicNode} from './oe/primitives/WorkingSchematic';
import {HookGap} from './oe/scenes/HookGap';
import {ChartScene} from './oe/scenes/ChartScene';
import {AnnotationScene} from './oe/scenes/AnnotationScene';
import {BRollScene} from './oe/scenes/BRollScene';
import {LogoScene} from './oe/scenes/LogoScene';
import {BrandSting, TitleCard, OutroCard} from './oe/scenes/Bookends';
import {ScreenRecScene} from './oe/scenes/ScreenRecScene';
import {SheetScene, SheetLine} from './oe/scenes/SheetScene';
import {QuoteCard} from './oe/scenes/QuoteCard';
import {ProofCard} from './oe/scenes/ProofCard';
import {LadderScene, LadderStep} from './oe/scenes/LadderScene';
import {OfferCard} from './oe/scenes/OfferCard';
import {RiskCard} from './oe/scenes/RiskCard';
import {ArtifactScene, ArtifactNode} from './oe/scenes/ArtifactScene';
import {ChapterReset} from './oe/scenes/ChapterReset';
import {SourceCard} from './oe/scenes/SourceCard';
import {CaseFile} from './oe/scenes/CaseFile';

/**
 * BlueprintComposition v2 — "The Working Schematic Edition"
 *
 * Design authority: /design-system/ (Rev C). Every visual decision maps
 * back to /design-system/README.md §4 (Visual foundations) and §6
 * (Components). No hex codes inline; consume ./oe/theme.
 *
 * Same props contract as v1 (flat BlueprintRenderData, no pipeline
 * change). Scene grammar replaces v1's slide/chart switch:
 *
 *   hook section, chart w/ scale gap  → HookGap (GapArrow on ink)
 *   any chart beat                    → ChartScene (Rev C bar chart)
 *   slide (title + bullets)           → AnnotationScene (annotation rail)
 *   broll                             → BRollScene
 *   logo                              → LogoScene
 *   screen_rec                        → ScreenRecScene
 *
 *   stack section (any beats)         → full-section WorkingSchematic
 *                                       (nodes drop as each beat begins)
 *
 * Auto section transitions: SheetCard overlay covers the first ~1.4s of
 * every section.
 *
 * TODOs picked up from the v2 spec:
 *   - Progressive assembly of a single episode-wide schematic (needs
 *     `schematic` block in assets.json — plan_assets.py Phase 2).
 *   - Music bed + SFX (needs music_bed path in brand config + assets).
 *   - Real b-roll footage (fetch_broll.py wired to originate/).
 *   - AnnotationRail across multiple sub-lines against a persistent
 *     schematic (needs the full episode schematic).
 */

type Word = {word: string; start: number; end: number; highlight: boolean};
type CaptionGroup = {text: string; words: Word[]; start: number; end: number};

type AssetSpec = {
  type: 'slide' | 'chart' | 'broll' | 'screen_rec' | 'logo';
  title?: string;
  bullets?: string[];
  chart_type?: 'bar' | 'line' | 'waterfall';
  series?: {label: string; value: number; highlight?: boolean}[];
  unit?: string;
  source?: string;
  search_query?: string;
  company?: string;
  caption?: string;
  tool?: string;
  action?: string;
};

type Beat = {beat: number; start: number; end: number; asset: AssetSpec};
type Section = {id: string; start: number; duration: number; audio: string; beats: Beat[]};

// ---------------------------------------------------------------------
// Storyboard screens — the durable v2 grammar
// (planned by scripts/originate/storyboard.py, evaluated by
// scripts/originate/eval_storyboard.py, emitted into render data by
// prepare_longform.py. See docs/storyboard-stage.md.)
// ---------------------------------------------------------------------

export type ScreenReveal = {
  beat: number;
  at: number; // absolute seconds
  end: number;
  title: string;
  body: string;
  asset: AssetSpec;
  tags?: string[];
  word_anchor?: {start: number; end: number};
};

export type SfxCue = {cue: 'tick' | 'whoosh' | 'hit'; at: number};
export type MusicCue = {intensity: 'calm' | 'build' | 'silence'; duck_db?: number};

/**
 * PaceEvent — a timed in-screen visual event authored by
 * `scripts/originate/pace_storyboard.py`. `at` is absolute seconds
 * (like reveal.at) — scenes convert it to sequence-local frames
 * before use. Each kind stages content the screen ALREADY carries:
 *
 * - fragment: reveal `beat`'s body (split on " · ") — fragment
 *   `index` appears now. Fragment 0 shows with the reveal itself.
 * - item: internal item `index` inside a custom-card block
 *   (risk/artifact/caseFile/offer/ladder) appears now.
 * - pulse: brief accent flash on the active line's key `word` —
 *   subtle. Never moves layout.
 * - focus: chart/ladder attention cycle — re-highlight data `index`.
 */
export type PaceEvent =
  | {at: number; kind: 'fragment'; beat: number; index: number}
  | {at: number; kind: 'item'; block: 'risk' | 'artifact' | 'caseFile' | 'offer' | 'ladder'; index: number}
  | {at: number; kind: 'pulse'; word: string}
  | {at: number; kind: 'focus'; index: number};

// Custom-props payload for hand-tuned screens. When the storyboard's
// auto-derived reveal fields aren't rich enough (a quote line that
// isn't stored on the beat, a ladder step set, an artifact node graph),
// the operator drops a `custom` block into the storyboard and the
// composition prefers it.
export type ScreenCustom = {
  // Quote / chapter reset
  quote?: string;
  accentPhrase?: string;
  attribution?: string;
  onInk?: boolean; // legacy; prefer `ground`
  ground?: 'ink' | 'navy' | 'paper'; // impact-line ground rotation
  // Proof card
  proof?: {
    value: number;
    prefix?: string;
    suffix?: string;
    compactCurrency?: boolean;
    label?: string;
    contrast?: string;
    source?: string;
    estimate?: boolean;
  };
  // Ladder
  ladder?: {
    overline?: string;
    heading?: string;
    steps: LadderStep[]; // exactly 3
    source?: string;
    estimate?: boolean;
  };
  // Offer card
  offer?: {
    problem: string;
    deliverable: string;
    price: string;
    deadline: string;
    source?: string;
  };
  // Risk card
  risk?: {
    title: string;
    body?: string;
    bullets?: string[];
  };
  // Artifact / network map
  artifact?: {
    overline?: string;
    title?: string;
    nodes?: ArtifactNode[];
    callout?: string;
    source?: string;
  };
  // Chapter reset
  chapter?: {
    kicker?: string;
    heading: string;
  };
  // Source card
  sourceCard?: {
    claim: string;
    source: string;
    estimate?: boolean;
  };
  // Case file
  caseFile?: {
    reference?: string;
    problem: string;
    workflow: string;
    result: string;
    source?: string;
  };
};

export type Screen = {
  id: string;
  section: string;
  layout:
    | 'sheet'
    | 'schematic'
    | 'chart'
    | 'gap'
    | 'broll'
    | 'screen_rec'
    | 'logo'
    | 'cta'
    | 'quote'
    | 'proof_card'
    | 'ladder'
    | 'offer_card'
    | 'risk_card'
    | 'artifact'
    | 'chapter_reset'
    | 'source_card'
    | 'case_file';
  heading?: string;
  start: number;
  end: number;
  reveals: ScreenReveal[];
  figure?: {text: string; source?: string} | null;
  source?: string | null;
  audio?: string | null;
  sfx?: SfxCue[];
  music?: MusicCue;
  custom?: ScreenCustom;
  /** Per-screen visual events from pace_storyboard.py. */
  events?: PaceEvent[];
};

export type Bookends = {
  brand_seconds: number;
  title_seconds: number;
  outro_seconds: number;
  j_cut_seconds?: number; // VO starts this long BEFORE the intro ends (under the title card)
  l_cut_seconds?: number; // outro card enters this long before the VO ends
  title: string;
  thesis?: string;
  episode_no?: number | null;
  brand: {name: string; tagline: string; domain: string};
  ctas: string[];
};

export type BlueprintRenderData = {
  slug: string;
  title: string;
  duration_seconds: number;
  fps: number;
  total_frames: number;
  resolution: [number, number];
  sections: Section[];
  screens?: Screen[]; // optional — prefer when present
  captions: {groups: CaptionGroup[]; style: string; words_per_group: number};
  brand: any;
  bookends?: Bookends; // brand sting + title card + outro (2026-07-03)
};

// ---------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------

const SECTION_TITLES: Record<string, {title: string; subtitle?: string; onInk: boolean}> = {
  hook: {title: 'The gap', subtitle: 'What Accenture books vs. the solo version.', onInk: true},
  thesis: {title: 'The thesis', subtitle: 'Not building. Installing.', onInk: false},
  evidence: {title: 'The evidence', subtitle: 'Real companies. Sourced numbers. Range, not averages.', onInk: false},
  stack: {title: 'The stack', subtitle: 'Every tool. Every real monthly price.', onInk: true},
  playbook: {title: 'The playbook', subtitle: 'Week one. Weeks two–four. The first project.', onInk: false},
  economics: {title: 'The economics', subtitle: "What margins actually look like. And what breaks.", onInk: false},
  cta: {title: 'The blueprint', subtitle: 'Templates + full stack. Free — link below.', onInk: true},
};

const compactCurrency = (v: number, unit = '') => {
  const abs = Math.abs(v);
  if (abs >= 1_000_000_000) return `$${(v / 1_000_000_000).toFixed(1).replace(/\.0$/, '')}B${unit}`;
  if (abs >= 1_000_000) return `$${(v / 1_000_000).toFixed(1).replace(/\.0$/, '')}M${unit}`;
  if (abs >= 1000) return `$${(v / 1000).toFixed(1).replace(/\.0$/, '')}K${unit}`;
  return `$${Math.round(v).toLocaleString()}${unit}`;
};

// The hook section's first-beat chart wants GapArrow when the values
// span multiple orders of magnitude (>1000×).
function isHookGapChart(beat: Beat): beat is Beat & {asset: AssetSpec & {series: NonNullable<AssetSpec['series']>}} {
  const s = beat.asset.series;
  if (!s || s.length !== 2) return false;
  const [a, b] = s.map((d) => d.value).sort((x, y) => x - y);
  return b / Math.max(a, 1) > 1000;
}

function toGap(series: {label: string; value: number}[], unit?: string): {from: string; to: string; label?: string} {
  const [big, small] = [...series].sort((a, b) => b.value - a.value);
  if (unit === '$') {
    return {from: compactCurrency(big.value), to: compactCurrency(small.value), label: 'The gap'};
  }
  return {from: `${big.value}${unit ?? ''}`, to: `${small.value}${unit ?? ''}`, label: 'The gap'};
}

// Derive a schematic node from a stack-section slide beat: label from the
// beat title's price fragment ("$20–40/mo"), name from what's before the
// em-dash.
function deriveStackNode(beat: Beat, i: number, appearFrame: number): SchematicNode {
  const title = beat.asset.title ?? `Step ${i + 1}`;
  // Titles look like "The brain — $20–40/mo". Only em-dashes and en-dashes
  // separate name from figure — regular hyphens are word-internal
  // ("client-facing").
  const emDashSplit = title.split(/\s+[—–]\s+/);
  const name = (emDashSplit[0] ?? title).trim();
  const figure = emDashSplit.length > 1
    ? emDashSplit.slice(1).join(' — ').trim()
    : (beat.asset.bullets?.[0] ?? '').trim();
  return {
    id: `stack-${i}`,
    step: `Step ${String(i + 1).padStart(2, '0')}`,
    name,
    figure: figure || '—',
    appearAtFrame: appearFrame,
    status: i < 2 ? 'live' : 'running',
    goldFigure: false,
  };
}

// ---------------------------------------------------------------------
// Cross-dissolve plumbing
// ---------------------------------------------------------------------

// Frames of overlap between consecutive beats/sections. Each Sequence is
// extended by this much so the outgoing scene is still mounted underneath
// while the incoming scene (rendered later in the tree, therefore on top)
// eases in — a true cross-transition, never a hard cut or an ink flash.
const XFADE_FRAMES = 14;

// DS motion spec: fades/slides only, eased. The incoming scene fades AND
// settles upward ~24px with an ease-out — the "document sliding onto the
// desk" move — instead of a flat linear opacity ramp.
//
// `hard` skips the fade entirely (used for QuoteCard entries per craft §P1
// impact-frame: hard cut in, spring settle handled inside the scene).
const FadeIn: React.FC<{frames?: number; hard?: boolean; children: React.ReactNode}> = ({
  frames = XFADE_FRAMES,
  hard = false,
  children,
}) => {
  const frame = useCurrentFrame();
  if (hard) return <AbsoluteFill>{children}</AbsoluteFill>;
  const p = interpolate(frame, [0, frames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  return (
    <AbsoluteFill style={{opacity: p, transform: `translateY(${(1 - p) * 24}px)`}}>
      {children}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// Scene router
// ---------------------------------------------------------------------

const BeatScene: React.FC<{
  beat: Beat;
  section: Section;
  isSectionFirst: boolean;
  startFrame: number;
}> = ({beat, section, isSectionFirst, startFrame}) => {
  const meta = SECTION_TITLES[section.id];
  const onInk = meta?.onInk ?? false;

  // Hook-section first-beat gap treatment.
  if (section.id === 'hook' && isSectionFirst && beat.asset.type === 'chart' && isHookGapChart(beat)) {
    const {from, to, label} = toGap(beat.asset.series ?? [], beat.asset.unit);
    return (
      <HookGap
        overline="The Operator Economy · Blueprint № · Evidence-first"
        from={from}
        to={to}
        label={label}
        source={beat.asset.source}
        startFrame={0}
      />
    );
  }

  switch (beat.asset.type) {
    case 'chart':
      return (
        <ChartScene
          title={beat.asset.title}
          series={beat.asset.series ?? []}
          unit={beat.asset.unit}
          source={beat.asset.source}
          estimate={/estimate|reported/i.test(beat.asset.source ?? '') || /estimate|reported/i.test(beat.asset.title ?? '')}
          onInk={onInk}
          startFrame={0}
        />
      );
    case 'slide':
      return (
        <AnnotationScene
          title={beat.asset.title}
          overline={meta?.title?.toUpperCase()}
          bullets={beat.asset.bullets ?? []}
          onInk={onInk}
          startFrame={0}
        />
      );
    case 'broll':
      return <BRollScene searchQuery={beat.asset.search_query ?? '—'} caption={beat.asset.caption} startFrame={0} />;
    case 'logo':
      return (
        <LogoScene
          company={beat.asset.company ?? '—'}
          caption={beat.asset.caption}
          source={beat.asset.source}
          onInk={onInk}
          startFrame={0}
        />
      );
    case 'screen_rec':
      return (
        <ScreenRecScene
          tool={beat.asset.tool ?? '—'}
          action={beat.asset.action ?? ''}
          caption={beat.asset.caption}
          startFrame={0}
        />
      );
    default:
      return <AbsoluteFill style={{background: COLORS.ink}} />;
  }
};

// ---------------------------------------------------------------------
// Section renderer — the router for whole-section treatments
// (stack becomes a WorkingSchematic layer; everything else per-beat).
// ---------------------------------------------------------------------

const SectionLayer: React.FC<{
  section: Section;
  sectionIndex: number;
  totalSections: number;
  fps: number;
}> = ({section, sectionIndex, totalSections, fps}) => {
  const meta = SECTION_TITLES[section.id];

  // Stack section: full-section WorkingSchematic. Nodes appear as each
  // beat begins so the schematic assembles alongside the VO.
  if (section.id === 'stack') {
    const sectionStartFrame = Math.round(section.start * fps);
    const nodes = section.beats.map((b, i) =>
      deriveStackNode(b, i, Math.round(b.start * fps) - sectionStartFrame),
    );
    // Highlight the last node's figure gold (the "$2K" close of the stack).
    if (nodes.length > 0) nodes[nodes.length - 1].goldFigure = true;

    return (
      <>
        <Sequence
          from={sectionStartFrame}
          durationInFrames={Math.max(1, Math.round(section.duration * fps)) + XFADE_FRAMES}
        >
          <FadeIn>
          <AbsoluteFill style={{background: COLORS.navy, padding: '120px 160px 300px'}}>
            <WorkingSchematic
              nodes={nodes}
              sheetLabel={`Sheet ${String(sectionIndex + 1).padStart(2, '0')} of ${String(totalSections).padStart(2, '0')} — The stack`}
              margin="≤ $100/mo"
              running
            />
          </AbsoluteFill>
          </FadeIn>
        </Sequence>
      </>
    );
  }

  // Render-layer storyboard: group consecutive `slide` beats into ONE
  // persistent SheetScene (talking points reveal in place, like the
  // stack schematic's node drops). Charts / broll / logo / screen_rec
  // stay standalone scenes. This is what keeps the video from cutting
  // to a new full screen on every talking point.
  type Group =
    | {kind: 'sheet'; beats: {beat: Beat; index: number}[]}
    | {kind: 'single'; beat: Beat; index: number};

  const groups: Group[] = [];
  section.beats.forEach((beat, i) => {
    // The hook-gap chart keeps its special treatment; slides merge.
    if (beat.asset.type === 'slide') {
      const last = groups[groups.length - 1];
      if (last && last.kind === 'sheet') {
        last.beats.push({beat, index: i});
      } else {
        groups.push({kind: 'sheet', beats: [{beat, index: i}]});
      }
    } else {
      groups.push({kind: 'single', beat, index: i});
    }
  });

  return (
    <>
      {groups.map((group, gi) => {
        if (group.kind === 'sheet' && group.beats.length > 1) {
          const first = group.beats[0].beat;
          const last = group.beats[group.beats.length - 1].beat;
          const from = Math.round(first.start * fps);
          const dur = Math.max(1, Math.round((last.end - first.start) * fps)) + XFADE_FRAMES;
          const lines: SheetLine[] = group.beats.map(({beat}) => ({
            title: beat.asset.title ?? '',
            body: (beat.asset.bullets ?? []).join(' · '),
            appearAtFrame: Math.round((beat.start - first.start) * fps),
            startSec: beat.start - first.start,
            endSec: beat.end - first.start,
          }));
          return (
            <Sequence key={`sheet-run-${gi}`} from={from} durationInFrames={dur}>
              <FadeIn>
                <SheetScene
                  overline={`Sheet ${String(sectionIndex + 1).padStart(2, '0')} of ${String(totalSections).padStart(2, '0')}`}
                  heading={meta?.title}
                  subtitle={meta?.subtitle}
                  lines={lines}
                  onInk={meta?.onInk ?? false}
                />
              </FadeIn>
            </Sequence>
          );
        }

        // Single beat (lone slide, chart, broll, logo, screen_rec).
        const {beat, index} = group.kind === 'single' ? group : {beat: group.beats[0].beat, index: group.beats[0].index};
        const from = Math.round(beat.start * fps);
        // Extend past the end so it holds under the next scene's fade-in
        // (cross-dissolve; later Sequences stack on top).
        const dur = Math.max(1, Math.round((beat.end - beat.start) * fps)) + XFADE_FRAMES;
        return (
          <Sequence key={`beat-${beat.beat}`} from={from} durationInFrames={dur}>
            <FadeIn>
              <BeatScene beat={beat} section={section} isSectionFirst={index === 0} startFrame={0} />
            </FadeIn>
          </Sequence>
        );
      })}
    </>
  );
};

// ---------------------------------------------------------------------
// Drift — the slow virtual camera on every screen (craft §motion). 2–4%
// Ken Burns scale over the screen's hold, alternating direction per
// screen so the camera never resets to the same origin twice.
// ---------------------------------------------------------------------

const Drift: React.FC<{direction: 'in' | 'out'; durationInFrames: number; children: React.ReactNode}> = ({
  direction,
  durationInFrames,
  children,
}) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(...EASE.standard),
  });
  const from = direction === 'in' ? KEN_BURNS.scaleMin : KEN_BURNS.scaleMax;
  const to = direction === 'in' ? KEN_BURNS.scaleMax : KEN_BURNS.scaleMin;
  const scale = from + (to - from) * t;
  return (
    <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: 'center'}}>
      {children}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// Screen router (preferred path — reads storyboard-derived screens[])
// ---------------------------------------------------------------------

// Convert a PaceEvent's absolute-seconds `at` to a sequence-local frame
// (screen.start is the Sequence's `from`, so subtract it from event.at
// before multiplying by fps). Filtering by kind first keeps each scene's
// event array small.
export type LocalEvent<T extends PaceEvent> = T & {atFrame: number};

function localEvents<K extends PaceEvent['kind']>(
  events: PaceEvent[] | undefined,
  kind: K,
  screenStart: number,
  fps: number,
): LocalEvent<Extract<PaceEvent, {kind: K}>>[] {
  if (!events || events.length === 0) return [];
  const out: LocalEvent<Extract<PaceEvent, {kind: K}>>[] = [];
  for (const ev of events) {
    if (ev.kind === kind) {
      out.push({
        ...(ev as Extract<PaceEvent, {kind: K}>),
        atFrame: Math.round((ev.at - screenStart) * fps),
      });
    }
  }
  return out;
}

const ScreenLayer: React.FC<{
  screen: Screen;
  screenIndex: number;
  totalScreens: number;
  fps: number;
}> = ({screen, screenIndex, totalScreens, fps}) => {
  const from = Math.round(screen.start * fps);
  const dur = Math.max(1, Math.round((screen.end - screen.start) * fps)) + XFADE_FRAMES;
  const meta = SECTION_TITLES[screen.section];
  const onInk = meta?.onInk ?? false;
  const first = screen.reveals[0];

  const overline = `Sheet ${String(screenIndex + 1).padStart(2, '0')} of ${String(totalScreens).padStart(2, '0')}`;

  // Pre-filter pace events into local-frame lists per kind. Scenes take
  // only what they use.
  const fragmentEvents = localEvents(screen.events, 'fragment', screen.start, fps);
  const itemEvents = localEvents(screen.events, 'item', screen.start, fps);
  const pulseEvents = localEvents(screen.events, 'pulse', screen.start, fps);
  const focusEvents = localEvents(screen.events, 'focus', screen.start, fps);

  let content: React.ReactNode;

  switch (screen.layout) {
    case 'schematic': {
      // Nodes assemble as their reveal beats begin.
      const nodes: SchematicNode[] = screen.reveals.map((r, i) => {
        const title = r.title || `Step ${i + 1}`;
        const emDashSplit = title.split(/\s+[—–]\s+/);
        const name = (emDashSplit[0] ?? title).trim();
        const figure = emDashSplit.length > 1
          ? emDashSplit.slice(1).join(' — ').trim()
          : (r.body || '').split(' · ')[0];
        return {
          id: `${screen.id}-node-${i}`,
          step: `Step ${String(i + 1).padStart(2, '0')}`,
          name,
          figure: figure || '—',
          appearAtFrame: Math.round((r.at - screen.start) * fps),
          status: i < 2 ? 'live' : 'running',
          goldFigure: i === screen.reveals.length - 1,
        };
      });
      // Camera cues: reveal.at → local frame, WorkingSchematic uses
      // them to slowly frame the active node group. Drift back on the
      // final reveal so the whole board is visible at the section end.
      const cameraCues = screen.reveals.map((r, i) => ({
        atFrame: Math.round((r.at - screen.start) * fps),
        nodeIndex: i,
        isLast: i === screen.reveals.length - 1,
      }));
      content = (
        <AbsoluteFill style={{background: COLORS.navy, padding: '120px 160px 300px'}}>
          <WorkingSchematic
            nodes={nodes}
            sheetLabel={`${overline} — ${screen.heading ?? ''}`}
            margin="≤ $100/mo"
            running
            cameraCues={cameraCues}
          />
        </AbsoluteFill>
      );
      break;
    }
    case 'gap': {
      // Hook-first-chart special: derive from/to from the chart series.
      const series = first?.asset?.series ?? [];
      if (series.length >= 2) {
        const {from: gapFrom, to: gapTo, label} = toGap(series, first?.asset?.unit);
        content = (
          <HookGap
            overline="The Operator Economy · Blueprint № · Evidence-first"
            from={gapFrom}
            to={gapTo}
            label={label}
            source={first?.asset?.source ?? screen.source ?? undefined}
            startFrame={0}
          />
        );
      } else {
        content = <ChartScene series={series} title={first?.title} onInk={onInk} startFrame={0} />;
      }
      break;
    }
    case 'chart':
      content = (
        <ChartScene
          title={first?.asset?.title ?? first?.title}
          series={first?.asset?.series ?? []}
          unit={first?.asset?.unit}
          source={first?.asset?.source ?? screen.source ?? undefined}
          estimate={/estimate|reported/i.test(first?.asset?.source ?? '') || /estimate|reported/i.test(first?.title ?? '')}
          onInk={onInk}
          startFrame={0}
          focusEvents={focusEvents}
        />
      );
      break;
    case 'sheet':
    case 'cta': {
      // Pass each reveal's beat number through so SheetScene can gate
      // its body fragments on {kind:'fragment',beat,index} events.
      const lines: SheetLine[] = screen.reveals.map((r) => ({
        beat: r.beat,
        ordinal: (r as {ordinal?: number}).ordinal,
        title: r.title,
        body: r.body,
        appearAtFrame: Math.round((r.at - screen.start) * fps),
        startSec: r.at - screen.start,
        endSec: r.end - screen.start,
      }));
      content = (
        <SheetScene
          overline={overline}
          heading={screen.heading}
          subtitle={meta?.subtitle}
          lines={lines}
          onInk={screen.layout === 'cta' ? true : onInk}
          fragmentEvents={fragmentEvents}
          pulseEvents={pulseEvents}
        />
      );
      break;
    }
    case 'broll':
      content = (
        <BRollScene
          searchQuery={first?.asset?.search_query ?? first?.title ?? ''}
          caption={first?.asset?.caption}
          startFrame={0}
        />
      );
      break;
    case 'logo':
      content = (
        <LogoScene
          company={first?.asset?.company ?? first?.title ?? ''}
          caption={first?.asset?.caption}
          source={first?.asset?.source ?? screen.source ?? undefined}
          onInk={onInk}
          startFrame={0}
        />
      );
      break;
    case 'screen_rec':
      content = (
        <ScreenRecScene
          tool={first?.asset?.tool ?? first?.title ?? ''}
          action={first?.asset?.action ?? ''}
          caption={first?.asset?.caption}
          startFrame={0}
        />
      );
      break;
    case 'quote': {
      // Impact-line ground rotation per Rev C (one accent per frame —
      // rotate GROUNDS, not accents). Storyboard can pin the ground
      // via `custom.ground`; otherwise section id is the proxy:
      //   hook, thesis       → ink  (cold-open, thesis lines)
      //   evidence           → navy (drafting-grid, evidence
      //                              turning-points)
      //   economics          → paper (honest-math lines)
      //   playbook, stack,
      //   cta                → ink  (fallback — impact frames here are
      //                              typically final brand or reversal
      //                              cards; ink keeps continuity)
      // 2026-07-03: ink retired as a quote ground (read as dead void) —
      // navy+grid is the default; paper stays for honest-math prints.
      const groundFromSection: 'ink' | 'navy' | 'paper' =
        screen.section === 'economics' ? 'paper' : 'navy';
      const resolvedGround = screen.custom?.ground ?? groundFromSection;
      const c = screen.custom?.quote
        ? {
            quote: screen.custom.quote,
            accentPhrase: screen.custom.accentPhrase,
            attribution: screen.custom.attribution,
            ground: resolvedGround,
          }
        : {
            quote: first?.title ?? '',
            attribution: first?.body,
            ground: resolvedGround,
          };
      content = <QuoteCard {...c} />;
      break;
    }
    case 'proof_card': {
      const c = screen.custom?.proof;
      if (c) {
        content = (
          <ProofCard
            value={c.value}
            prefix={c.prefix}
            suffix={c.suffix}
            compactCurrency={c.compactCurrency}
            label={c.label}
            contrast={c.contrast}
            source={c.source ?? screen.source ?? undefined}
            estimate={c.estimate}
            onInk={onInk}
          />
        );
      } else {
        // Fallback: numeric value pulled from the reveal's asset.series (best of the pair).
        const series = first?.asset?.series ?? [];
        const value = series[0]?.value ?? 0;
        content = (
          <ProofCard
            value={value}
            prefix={first?.asset?.unit === '$' ? '$' : ''}
            compactCurrency={first?.asset?.unit === '$'}
            label={first?.title}
            source={first?.asset?.source ?? screen.source ?? undefined}
            onInk={onInk}
          />
        );
      }
      break;
    }
    case 'ladder': {
      const c = screen.custom?.ladder;
      if (c && c.steps.length === 3) {
        content = (
          <LadderScene
            overline={c.overline ?? screen.heading?.toUpperCase()}
            heading={c.heading ?? first?.title}
            steps={c.steps as [LadderStep, LadderStep, LadderStep]}
            source={c.source ?? screen.source ?? undefined}
            estimate={c.estimate}
            onInk={onInk}
            itemEvents={itemEvents.filter((e) => e.block === 'ladder')}
            focusEvents={focusEvents}
          />
        );
      } else {
        // Fallback: try to build 3 steps from the reveal's series.
        const series = first?.asset?.series ?? [];
        if (series.length >= 3) {
          const [a, b, cS] = series.slice(0, 3);
          const isDollar = first?.asset?.unit === '$';
          content = (
            <LadderScene
              overline={screen.heading?.toUpperCase()}
              heading={first?.asset?.title ?? first?.title}
              steps={[
                {label: a.label, value: a.value, prefix: isDollar ? '$' : '', compactCurrency: isDollar},
                {label: b.label, value: b.value, prefix: isDollar ? '$' : '', compactCurrency: isDollar},
                {label: cS.label, value: cS.value, prefix: isDollar ? '$' : '', compactCurrency: isDollar},
              ]}
              source={first?.asset?.source ?? screen.source ?? undefined}
              onInk={onInk}
              itemEvents={itemEvents.filter((e) => e.block === 'ladder')}
              focusEvents={focusEvents}
            />
          );
        } else {
          // Not enough data — degrade to a ChartScene.
          content = (
            <ChartScene
              title={first?.asset?.title ?? first?.title}
              series={series}
              unit={first?.asset?.unit}
              source={first?.asset?.source ?? screen.source ?? undefined}
              onInk={onInk}
              startFrame={0}
            />
          );
        }
      }
      break;
    }
    case 'offer_card': {
      const c = screen.custom?.offer;
      const offerItems = itemEvents.filter((e) => e.block === 'offer');
      if (c) {
        content = (
          <OfferCard
            problem={c.problem}
            deliverable={c.deliverable}
            price={c.price}
            deadline={c.deadline}
            source={c.source ?? screen.source ?? undefined}
            onInk={onInk}
            itemEvents={offerItems}
          />
        );
      } else {
        content = (
          <OfferCard
            problem={first?.title ?? ''}
            deliverable={first?.body ?? ''}
            price=""
            deadline=""
            source={screen.source ?? undefined}
            onInk={onInk}
            itemEvents={offerItems}
          />
        );
      }
      break;
    }
    case 'risk_card': {
      const c = screen.custom?.risk;
      content = (
        <RiskCard
          title={c?.title ?? first?.title ?? ''}
          body={c?.body ?? first?.body}
          bullets={c?.bullets ?? first?.asset?.bullets}
          onInk={onInk}
          itemEvents={itemEvents.filter((e) => e.block === 'risk')}
        />
      );
      break;
    }
    case 'artifact': {
      const c = screen.custom?.artifact;
      content = (
        <ArtifactScene
          overline={c?.overline ?? screen.heading?.toUpperCase()}
          title={c?.title ?? first?.asset?.title ?? first?.title}
          nodes={c?.nodes}
          callout={c?.callout ?? first?.body}
          source={c?.source ?? first?.asset?.source ?? screen.source ?? undefined}
          onInk={onInk}
          itemEvents={itemEvents.filter((e) => e.block === 'artifact')}
        />
      );
      break;
    }
    case 'chapter_reset': {
      const c = screen.custom?.chapter;
      content = (
        <ChapterReset
          kicker={c?.kicker ?? overline}
          heading={c?.heading ?? screen.heading ?? first?.title ?? ''}
          onInk={onInk}
        />
      );
      break;
    }
    case 'source_card': {
      const c = screen.custom?.sourceCard;
      content = (
        <SourceCard
          claim={c?.claim ?? first?.title ?? ''}
          source={c?.source ?? screen.source ?? first?.asset?.source ?? ''}
          estimate={c?.estimate}
          onInk={onInk}
        />
      );
      break;
    }
    case 'case_file': {
      const c = screen.custom?.caseFile;
      content = (
        <CaseFile
          reference={c?.reference}
          problem={c?.problem ?? first?.title ?? ''}
          workflow={c?.workflow ?? ''}
          result={c?.result ?? ''}
          source={c?.source ?? screen.source ?? undefined}
          onInk={onInk}
          itemEvents={itemEvents.filter((e) => e.block === 'caseFile')}
        />
      );
      break;
    }
    default:
      content = <AbsoluteFill style={{background: COLORS.ink}} />;
  }

  // Quote / chapter_reset use hard cuts (no cross-fade). Everything else
  // gets the standard 14-frame settle.
  const hardCut = screen.layout === 'quote' || screen.layout === 'chapter_reset';
  const driftDir: 'in' | 'out' = screenIndex % 2 === 0 ? 'in' : 'out';

  // AmbientGround adds the slow scale drift (1.000→1.018) so nothing
  // sits perfectly still. Impact frames opt OUT — their stillness IS
  // the effect. Navy grounds also get the grid parallax. Because
  // schematic screens carry their own painted drafting grid, we only
  // gridParallax the sheet/cta layers on evidence (whose ground is
  // navy per the impact-line ground rotation — but sheets don't use
  // navy; the schematic screens do). Keeping this simple: parallax on
  // schematic only.
  const impactStill = hardCut; // quote/chapter_reset — stay dead still
  const gridParallax = screen.layout === 'schematic';

  return (
    <Sequence key={`screen-${screen.id}`} from={from} durationInFrames={dur}>
      <FadeIn hard={hardCut}>
        <Drift direction={driftDir} durationInFrames={dur}>
          <AmbientGround
            enabled={!impactStill}
            durationInFrames={dur}
            gridParallax={gridParallax}
          >
            {content}
          </AmbientGround>
        </Drift>
      </FadeIn>
    </Sequence>
  );
};

// ---------------------------------------------------------------------
// Root composition
// ---------------------------------------------------------------------

// Return the caption groups filtered so nothing renders during quote or
// chapter_reset windows — the card IS the caption there, and duplicating
// it is a rubric kill-list item.
function captionsHiddenDuring(
  groups: CaptionGroup[],
  screens: Screen[] | undefined,
): CaptionGroup[] {
  if (!screens) return groups;
  const silenced = screens.filter(
    (s) => s.layout === 'quote' || s.layout === 'chapter_reset',
  );
  if (silenced.length === 0) return groups;
  return groups.filter((g) => {
    // Drop the group if its window overlaps any silenced screen.
    return !silenced.some((s) => g.start < s.end && g.end > s.start);
  });
}

export const BlueprintComposition: React.FC<BlueprintRenderData> = (renderData) => {
  useEnsureFontsLoaded();
  const {fps} = useVideoConfig();
  const {sections, captions, screens, bookends} = renderData;
  const useScreens = Array.isArray(screens) && screens.length > 0;
  const captionGroups = React.useMemo(
    () => captionsHiddenDuring(captions?.groups ?? [], screens),
    [captions?.groups, screens],
  );

  // Bookends: content shifts right by the intro MINUS the J-cut (VO
  // starts under the title card); the outro card enters L-cut seconds
  // before the VO ends and overlays the tail.
  const brandFrames = bookends ? Math.round(bookends.brand_seconds * fps) : 0;
  const titleFrames = bookends ? Math.round(bookends.title_seconds * fps) : 0;
  const introFrames = brandFrames + titleFrames;
  const jCutFrames = bookends
    ? Math.min(Math.round((bookends.j_cut_seconds ?? bookends.title_seconds) * fps), titleFrames)
    : 0;
  const lCutFrames = bookends ? Math.round((bookends.l_cut_seconds ?? 2.5) * fps) : 0;
  const contentFrames = Math.round(renderData.duration_seconds * fps) + 1;
  const contentFrom = introFrames - jCutFrames;
  const outroFrames = bookends ? Math.round(bookends.outro_seconds * fps) : 0;
  const outroFrom = contentFrom + contentFrames - lCutFrames;

  // The whole episode floats over Ink so cross-section fades never flash
  // a caller color between Sequences.
  const episode = (
    <AbsoluteFill style={{background: COLORS.ink}}>
      {/* Per-section audio — same in both grammars, since a screen's
          audio still comes from its section's VO. */}
      {sections.map((section) => (
        <Sequence
          key={`audio-${section.id}`}
          from={Math.round(section.start * fps)}
          durationInFrames={Math.max(1, Math.round(section.duration * fps))}
        >
          {section.audio ? <Audio src={staticFile(section.audio)} /> : null}
        </Sequence>
      ))}

      {/* Prefer storyboard-planned screens[] when present; otherwise fall
          back to the run-grouping shim in SectionLayer. Once every
          episode ships with a storyboard the shim can be removed
          (docs/storyboard-stage.md §Migration). */}
      {useScreens
        ? screens!.map((screen, i) => (
            <ScreenLayer
              key={`screen-${screen.id}`}
              screen={screen}
              screenIndex={i}
              totalScreens={screens!.length}
              fps={fps}
            />
          ))
        : sections.map((section, i) => (
            <SectionLayer
              key={`sec-${section.id}`}
              section={section}
              sectionIndex={i}
              totalSections={sections.length}
              fps={fps}
            />
          ))}

      {/* Sound layer — music bed (config-gated) + SFX cues. Enabled by
          dropping bed.mp3 into remotion/public/music/ and tick/whoosh/
          hit into remotion/public/sfx/. Absent files disable the layer
          silently (never a placeholder tone). */}
      {useScreens && (
        // Flipped ON 2026-07-03: bed.mp3 (ElevenLabs Music, normalized
        // −16 LUFS, loops) + tick/whoosh/hit (ElevenLabs SFX) are in
        // remotion/public/. Ducking + silence pre-laps live in SoundBed.
        <SoundBed screens={screens!} musicDir="music" sfxDir="sfx" />
      )}

      {/* Captions layer — always on top, hidden during quote/chapter_reset. */}
      <Captions groups={captionGroups} onInk />
    </AbsoluteFill>
  );

  if (!bookends) return episode;

  // JSX order = z-order: episode content sits UNDER the bookend cards,
  // so the J-cut (VO + hook running beneath the title card) and L-cut
  // (outro covering the final beats while the VO finishes) both read
  // as edits, not slides.
  return (
    <AbsoluteFill style={{background: COLORS.navy}}>
      <Sequence from={contentFrom} durationInFrames={contentFrames}>
        {episode}
      </Sequence>
      <Sequence from={0} durationInFrames={brandFrames}>
        <BrandSting name={bookends.brand.name} tagline={bookends.brand.tagline} />
      </Sequence>
      <Sequence from={brandFrames} durationInFrames={titleFrames}>
        <TitleCard
          overline={
            bookends.episode_no
              ? `Operator Blueprint · № ${String(bookends.episode_no).padStart(3, '0')}`
              : 'Operator Blueprint'
          }
          title={bookends.title}
          thesis={bookends.thesis}
        />
      </Sequence>
      <Sequence from={outroFrom} durationInFrames={outroFrames}>
        <OutroCard
          brand={bookends.brand.name}
          tagline={bookends.brand.tagline}
          url={bookends.brand.domain}
          ctas={bookends.ctas}
        />
      </Sequence>
    </AbsoluteFill>
  );
};
