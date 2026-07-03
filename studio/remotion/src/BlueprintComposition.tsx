import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';

import {useEnsureFontsLoaded} from './oe/fonts';
import {COLORS} from './oe/theme';
import {Captions} from './oe/Captions';
import {SheetCard} from './oe/primitives/SheetCard';
import {WorkingSchematic, SchematicNode} from './oe/primitives/WorkingSchematic';
import {HookGap} from './oe/scenes/HookGap';
import {ChartScene} from './oe/scenes/ChartScene';
import {AnnotationScene} from './oe/scenes/AnnotationScene';
import {BRollScene} from './oe/scenes/BRollScene';
import {LogoScene} from './oe/scenes/LogoScene';
import {ScreenRecScene} from './oe/scenes/ScreenRecScene';

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

export type BlueprintRenderData = {
  slug: string;
  title: string;
  duration_seconds: number;
  fps: number;
  total_frames: number;
  resolution: [number, number];
  sections: Section[];
  captions: {groups: CaptionGroup[]; style: string; words_per_group: number};
  brand: any;
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
  // Titles look like "The brain — $20–40/mo". Split on em-dash / hyphen.
  const dashSplit = title.split(/[—–-]\s*/);
  const name = (dashSplit[0] ?? title).trim();
  const figure = (dashSplit.slice(1).join(' — ') || (beat.asset.bullets?.[0] ?? '')).trim();
  const isLast = false;
  return {
    id: `stack-${i}`,
    step: `Step ${String(i + 1).padStart(2, '0')}`,
    name,
    figure: figure || '—',
    appearAtFrame: appearFrame,
    status: i < 2 ? 'live' : 'running',
    goldFigure: isLast,
  };
}

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
        startFrame={startFrame}
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
          startFrame={startFrame}
        />
      );
    case 'slide':
      return (
        <AnnotationScene
          title={beat.asset.title}
          overline={meta?.title?.toUpperCase()}
          bullets={beat.asset.bullets ?? []}
          onInk={onInk}
          startFrame={startFrame}
        />
      );
    case 'broll':
      return <BRollScene searchQuery={beat.asset.search_query ?? '—'} caption={beat.asset.caption} startFrame={startFrame} />;
    case 'logo':
      return (
        <LogoScene
          company={beat.asset.company ?? '—'}
          caption={beat.asset.caption}
          source={beat.asset.source}
          onInk={onInk}
          startFrame={startFrame}
        />
      );
    case 'screen_rec':
      return (
        <ScreenRecScene
          tool={beat.asset.tool ?? '—'}
          action={beat.asset.action ?? ''}
          caption={beat.asset.caption}
          startFrame={startFrame}
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
          durationInFrames={Math.max(1, Math.round(section.duration * fps))}
        >
          <AbsoluteFill style={{background: COLORS.navy, padding: '120px 160px 300px'}}>
            <WorkingSchematic
              nodes={nodes}
              sheetLabel={`Sheet ${String(sectionIndex + 1).padStart(2, '0')} of ${String(totalSections).padStart(2, '0')} — The stack`}
              margin="≤ $100/mo"
              running
            />
          </AbsoluteFill>
        </Sequence>
      </>
    );
  }

  // Default: per-beat scenes
  return (
    <>
      {section.beats.map((beat, i) => {
        const from = Math.round(beat.start * fps);
        const dur = Math.max(1, Math.round((beat.end - beat.start) * fps));
        return (
          <Sequence key={beat.beat} from={from} durationInFrames={dur}>
            <BeatScene beat={beat} section={section} isSectionFirst={i === 0} startFrame={0} />
          </Sequence>
        );
      })}
    </>
  );
};

// ---------------------------------------------------------------------
// Root composition
// ---------------------------------------------------------------------

export const BlueprintComposition: React.FC<BlueprintRenderData> = (renderData) => {
  useEnsureFontsLoaded();
  const {fps} = useVideoConfig();
  const {sections, captions} = renderData;

  // The whole episode floats over Ink so cross-section fades never flash
  // a caller color between Sequences.
  return (
    <AbsoluteFill style={{background: COLORS.ink}}>
      {/* Per-section audio */}
      {sections.map((section) => (
        <Sequence
          key={`audio-${section.id}`}
          from={Math.round(section.start * fps)}
          durationInFrames={Math.max(1, Math.round(section.duration * fps))}
        >
          {section.audio ? <Audio src={staticFile(section.audio)} /> : null}
        </Sequence>
      ))}

      {/* Per-section visuals (stack becomes the schematic; others route
          per beat). */}
      {sections.map((section, i) => (
        <SectionLayer
          key={`sec-${section.id}`}
          section={section}
          sectionIndex={i}
          totalSections={sections.length}
          fps={fps}
        />
      ))}

      {/* Section-transition sheet cards on top (first ~1.4s of each). */}
      {sections.map((section, i) => {
        const meta = SECTION_TITLES[section.id];
        if (!meta) return null;
        const sectionStart = Math.round(section.start * fps);
        const dur = Math.min(42, Math.max(1, Math.round(section.duration * fps)));
        return (
          <Sequence key={`sheet-${section.id}`} from={sectionStart} durationInFrames={dur}>
            <SheetCard
              sheet={i + 1}
              total={sections.length}
              title={meta.title}
              subtitle={meta.subtitle}
              onInk={meta.onInk || section.id === 'stack'}
              startFrame={0}
              totalFrames={dur}
            />
          </Sequence>
        );
      })}

      {/* Captions layer — always on top. */}
      <Captions groups={captions?.groups ?? []} onInk />
    </AbsoluteFill>
  );
};
