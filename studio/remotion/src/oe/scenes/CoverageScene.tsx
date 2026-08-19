import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

import type {Screen} from '../../BlueprintComposition';
import {COLORS, FONTS} from '../theme';

const grid: React.CSSProperties = {
  backgroundImage:
    `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 48px), ` +
    `repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 48px)`,
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const motion = (frame: number, from = 0, to = 15) => interpolate(
  frame, [from, to], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)},
);

const short = (value = '', max = 116) => value.length > max ? `${value.slice(0, max).trim()}…` : value;

const Kicker: React.FC<{screen: Screen; dark?: boolean}> = ({screen, dark}) => (
  <div style={{
    position: 'absolute', left: 70, right: 70, bottom: 36, display: 'flex',
    justifyContent: 'space-between', fontFamily: FONTS.mono, fontSize: 15,
    letterSpacing: '.06em', textTransform: 'uppercase',
    color: dark ? COLORS.onInkMuted : COLORS.ink500,
  }}>
    <span>{screen.coverage_asset_ids?.join(' · ') || 'Original motion'}</span>
    <span>{String(screen.coverage_index ?? 0).padStart(3, '0')} / {screen.coverage_total ?? 0}</span>
  </div>
);

const MediaScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const t = motion(frame, 0, 18);
  const media = screen.coverage_media!;
  const isVideo = /\.(mp4|mov|m4v|webm)$/i.test(media);
  const asset = screen.coverage_asset ?? {};
  const startFrom = Math.round(Number(asset.source_in ?? 0) * 30);
  const common: React.CSSProperties = {
    width: '100%', height: '100%', objectFit: 'cover',
    objectPosition: asset.focal_point || 'center',
    transform: `scale(${1.025 + frame * 0.00008})`,
  };
  return (
    <AbsoluteFill style={{background: COLORS.ink, overflow: 'hidden'}}>
      {isVideo ? (
        <OffthreadVideo src={staticFile(media)} muted startFrom={startFrom} style={common}/>
      ) : (
        <Img src={staticFile(media)} style={{...common, objectFit: 'contain', transform: `scale(${.96 + t * .04})`}}/>
      )}
      <div style={{position: 'absolute', inset: 0, background: 'rgba(18,19,18,.18)'}}/>
      <div style={{
        position: 'absolute', left: 72, bottom: 82, maxWidth: 1240,
        padding: '22px 28px 24px', background: 'rgba(18,19,18,.88)',
        borderLeft: `5px solid ${COLORS.goldBright}`, opacity: t,
        transform: `translateY(${(1 - t) * 18}px)`,
      }}>
        <div style={{fontFamily: FONTS.sans, fontSize: 42, lineHeight: 1.12, fontWeight: 700, color: COLORS.onInk}}>
          {short(screen.coverage_narration, 104)}
        </div>
        <div style={{fontFamily: FONTS.mono, fontSize: 14, marginTop: 14, color: COLORS.onInkMuted, textTransform: 'uppercase'}}>
          {asset.provider || 'Editorial source'} · {asset.creator || asset.asset_type || 'selected asset'}
        </div>
      </div>
      <Kicker screen={screen} dark/>
    </AbsoluteFill>
  );
};

const MissingMedia: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const t = motion(frame);
  const asset = screen.coverage_asset ?? {};
  return (
    <AbsoluteFill style={{background: COLORS.navy, ...grid, color: COLORS.onInk}}>
      <div style={{position: 'absolute', left: 90, top: 80, fontFamily: FONTS.mono, fontSize: 17, color: COLORS.brick, textTransform: 'uppercase', letterSpacing: '.1em'}}>
        Media required · render blocker
      </div>
      <div style={{position: 'absolute', left: 90, top: 190, width: 1120, opacity: t, transform: `translateY(${(1-t)*18}px)`}}>
        <div style={{fontFamily: FONTS.display, fontWeight: 800, fontSize: 78, lineHeight: .98, letterSpacing: '-.05em'}}>
          {short(screen.visual_intent || screen.coverage_narration, 150)}
        </div>
      </div>
      <div style={{position: 'absolute', left: 90, right: 90, bottom: 150, display: 'grid', gridTemplateColumns: '260px 1fr', borderTop: `1px solid ${COLORS.schemNodeBorder}`, borderBottom: `1px solid ${COLORS.schemNodeBorder}`}}>
        <div style={{padding: '26px 20px', borderRight: `1px solid ${COLORS.schemNodeBorder}`, fontFamily: FONTS.mono, color: COLORS.goldBright}}>
          {(screen.coverage_asset_ids || ['UNASSIGNED']).join(' · ')}<br/>{screen.coverage_asset_type}
        </div>
        <div style={{padding: '26px 28px', fontFamily: FONTS.sans, fontSize: 25, color: COLORS.onInkMuted}}>
          {asset.query_variants?.[0] || 'Source or generate the exact shot described above, then complete provenance and rights review.'}
        </div>
      </div>
      <Kicker screen={screen} dark/>
    </AbsoluteFill>
  );
};

const BrandScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const line = interpolate(frame, [8, 42], [0, 1180], clamp);
  return (
    <AbsoluteFill style={{background: COLORS.navy, ...grid, color: COLORS.onInk, alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: FONTS.display, fontSize: 92, fontWeight: 800, letterSpacing: '-.05em'}}>The Operator Economy</div>
      <div style={{height: 3, width: line, margin: '28px 0 24px', background: COLORS.goldBright}}/>
      <div style={{fontFamily: FONTS.sans, fontSize: 34, maxWidth: 1240, textAlign: 'center', lineHeight: 1.3}}>
        AI and practical workflows for building and running a one-person business.
      </div>
      <Kicker screen={screen} dark/>
    </AbsoluteFill>
  );
};

const ProcessScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const phrases = (screen.visual_intent || screen.coverage_narration || '')
    .split(/[;,.]|\band\b/i).map((v) => v.trim()).filter((v) => v.length > 5).slice(0, 4);
  while (phrases.length < 3) phrases.push(['Find the guest', 'Own the handoff', 'Measure the return'][phrases.length]);
  return (
    <AbsoluteFill style={{background: COLORS.navy, ...grid, color: COLORS.onInk}}>
      <div style={{position: 'absolute', left: 85, top: 76, right: 85, fontFamily: FONTS.display, fontSize: 70, fontWeight: 800, lineHeight: .98, letterSpacing: '-.045em'}}>
        {short(screen.coverage_narration, 118)}
      </div>
      <div style={{position: 'absolute', left: 100, right: 100, top: 445, display: 'grid', gridTemplateColumns: `repeat(${phrases.length},1fr)`, gap: 62}}>
        {phrases.map((phrase, i) => {const t = motion(frame, 8 + i * 8, 22 + i * 8); return (
          <div key={`${phrase}-${i}`} style={{position: 'relative', minHeight: 150, padding: '28px 22px', border: `2px solid ${i === phrases.length - 1 ? COLORS.goldBright : COLORS.schemNodeBorder}`, background: COLORS.schemNodeBg, opacity: t, transform: `translateY(${(1-t)*18}px)`, fontFamily: FONTS.sans, fontSize: 25, lineHeight: 1.2}}>
            <div style={{fontFamily: FONTS.mono, fontSize: 16, color: COLORS.goldBright, marginBottom: 18}}>{String(i+1).padStart(2,'0')}</div>
            {short(phrase, 54)}
            {i < phrases.length - 1 ? <span style={{position: 'absolute', right: -45, top: 62, color: COLORS.goldBright, fontSize: 34}}>→</span> : null}
          </div>
        );})}
      </div>
      <Kicker screen={screen} dark/>
    </AbsoluteFill>
  );
};

const DataScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const values = Array.from((screen.coverage_narration || '').matchAll(/(?:\$)?\d[\d,.]*(?:\s?(?:percent|%|million|billion|rooms?|days?|weeks?))?/gi)).map((m) => m[0]).slice(0, 3);
  const shown = values.length ? values : ['Evidence', 'Mechanism'];
  return (
    <AbsoluteFill style={{background: COLORS.paper, color: COLORS.ink900}}>
      <div style={{position: 'absolute', left: 82, top: 90, width: 710, fontFamily: FONTS.display, fontSize: 72, fontWeight: 800, lineHeight: .98, letterSpacing: '-.05em'}}>{short(screen.coverage_narration, 105)}</div>
      <div style={{position: 'absolute', left: 875, right: 90, top: 155, bottom: 125, display: 'flex', alignItems: 'flex-end', justifyContent: 'space-around', gap: 44, borderLeft: `1px solid ${COLORS.rule}`, paddingLeft: 58}}>
        {shown.map((value, i) => {const t = motion(frame, 8 + i * 10, 30 + i * 10); const h = 260 + (i % 3) * 150; return (
          <div key={`${value}-${i}`} style={{width: `${80 / shown.length}%`, textAlign: 'center'}}>
            <div style={{fontFamily: FONTS.sans, fontVariantNumeric: 'tabular-nums', fontSize: 49, fontWeight: 700, marginBottom: 18}}>{value}</div>
            <div style={{height: h * t, background: i === 0 ? COLORS.draftingBlue : 'transparent', border: `2px solid ${COLORS.draftingBlue}`}}/>
          </div>
        );})}
      </div>
      <Kicker screen={screen}/>
    </AbsoluteFill>
  );
};

const DocumentScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const t = motion(frame);
  return (
    <AbsoluteFill style={{background: COLORS.paper, color: COLORS.ink900}}>
      <div style={{position: 'absolute', left: 110, top: 80, right: 110, bottom: 90, border: `2px solid ${COLORS.ruleStrong}`, padding: '58px 68px', opacity: t, transform: `translateX(${(1-t)*-22}px)`}}>
        <div style={{fontFamily: FONTS.mono, fontSize: 17, textTransform: 'uppercase', color: COLORS.draftingBlue}}>{screen.coverage_asset_type?.replaceAll('_',' ')} · working document</div>
        <div style={{fontFamily: FONTS.display, fontSize: 76, fontWeight: 800, lineHeight: 1, letterSpacing: '-.05em', maxWidth: 1350, marginTop: 34}}>{short(screen.coverage_narration, 130)}</div>
        <div style={{position: 'absolute', left: 68, right: 68, top: 460, display: 'grid', gridTemplateRows: 'repeat(3,1fr)', gap: 24}}>
          {[screen.visual_intent, 'Owner / input / decision / next action', 'Source, timestamp, and approval remain attached'].map((line, i) => <div key={i} style={{padding: '20px 22px', borderBottom: `1px solid ${COLORS.rule}`, borderLeft: `4px solid ${i===0?COLORS.draftingBlue:COLORS.ruleStrong}`, fontFamily: FONTS.sans, fontSize: 26}}>{short(line || '', 126)}</div>)}
        </div>
      </div>
      <Kicker screen={screen}/>
    </AbsoluteFill>
  );
};

const mediaTypes = new Set(['hospitality_footage','platform_visual','interface_capture','source_document','headline_document']);
const dataTypes = new Set(['custom_chart','comparison_chart','evidence_card']);
const processTypes = new Set(['process_diagram','stack_diagram','checklist_motion']);
const documentTypes = new Set(['document_template']);

export const CoverageScene: React.FC<{screen: Screen}> = ({screen}) => {
  const type = screen.coverage_asset_type || 'visual_metaphor';
  if (screen.coverage_media) return <MediaScene screen={screen}/>;
  if (mediaTypes.has(type)) return <MissingMedia screen={screen}/>;
  if (type === 'brand_ident') return <BrandScene screen={screen}/>;
  if (dataTypes.has(type)) return <DataScene screen={screen}/>;
  if (processTypes.has(type)) return <ProcessScene screen={screen}/>;
  if (documentTypes.has(type)) return <DocumentScene screen={screen}/>;
  if (type === 'cta_card' || type === 'outcome_card' || type === 'visual_metaphor') return <ProcessScene screen={screen}/>;
  return <DocumentScene screen={screen}/>;
};
