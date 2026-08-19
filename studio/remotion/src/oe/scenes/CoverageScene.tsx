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
  if (isVideo) return (
    <AbsoluteFill style={{background: COLORS.ink, overflow: 'hidden'}}>
      <OffthreadVideo src={staticFile(media)} muted startFrom={startFrom} style={common}/>
      <Kicker screen={screen} dark/>
    </AbsoluteFill>
  );
  return (
    <AbsoluteFill style={{background: COLORS.paper, color: COLORS.ink900}}>
      <div style={{position: 'absolute', left: 82, right: 82, top: 62, bottom: 82, border: `2px solid ${COLORS.ruleStrong}`, background: '#fff', opacity: t, transform: `translateY(${(1-t)*14}px)`}}>
        <div style={{height: 38, borderBottom: `1px solid ${COLORS.ruleStrong}`, display: 'flex', alignItems: 'center', gap: 10, padding: '0 15px'}}>
          {[0,1,2].map((dot) => <span key={dot} style={{width: 9,height:9,borderRadius:'50%',background:dot===0?COLORS.goldOnPaper:COLORS.ruleStrong}}/>)}
          <span style={{fontFamily:FONTS.mono,fontSize:12,marginLeft:14,color:COLORS.ink500}}>{asset.provider || 'Editorial capture'} · reviewed source window</span>
        </div>
        <div style={{position:'absolute',left:22,right:22,top:60,bottom:22,overflow:'hidden',background:COLORS.paper}}>
          <Img src={staticFile(media)} style={{width:'100%',height:'100%',objectFit:'contain',objectPosition:'center'}}/>
        </div>
      </div>
      <Kicker screen={screen}/>
    </AbsoluteFill>
  );
};

const ColdOpenScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame = useCurrentFrame();
  const t = motion(frame, 3, 18);
  const media = screen.coverage_media;
  return <AbsoluteFill style={{background:COLORS.ink,overflow:'hidden'}}>
    {media ? <>
      <div style={{position:'absolute',left:0,top:0,bottom:0,width:'50%',overflow:'hidden'}}><OffthreadVideo src={staticFile(media)} muted style={{width:'200%',height:'100%',objectFit:'cover',objectPosition:'left center'}}/></div>
      <div style={{position:'absolute',right:0,top:0,bottom:0,width:'50%',overflow:'hidden',borderLeft:`5px solid ${COLORS.goldBright}`}}><OffthreadVideo src={staticFile(media)} muted style={{width:'200%',height:'100%',objectFit:'cover',objectPosition:'left center',transform:'translateX(0) scaleX(-1)'}}/></div>
    </> : null}
    <div style={{position:'absolute',inset:0,background:'rgba(18,19,18,.42)'}}/>
    <div style={{position:'absolute',left:0,right:0,top:250,textAlign:'center',opacity:t,transform:`scale(${.88+t*.12})`}}>
      <div style={{fontFamily:FONTS.sans,fontWeight:800,fontSize:198,lineHeight:.8,letterSpacing:'-.075em',color:COLORS.onInk}}>SAME GUEST</div>
      <div style={{display:'inline-block',fontFamily:FONTS.sans,fontWeight:700,fontSize:38,letterSpacing:'-.02em',color:COLORS.ink,background:COLORS.goldBright,padding:'12px 24px',marginTop:36}}>THE HOTEL PAYS TO MEET THEM AGAIN</div>
    </div>
    <div style={{position:'absolute',left:'50%',top:0,bottom:0,width:interpolate(frame,[20,42],[0,5],clamp),background:COLORS.goldBright}}/>
    <Kicker screen={screen} dark/>
  </AbsoluteFill>;
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
      <div style={{fontFamily: FONTS.display, fontSize: 92, fontWeight: 800, letterSpacing: '-.055em',textAlign:'center'}}>The Operator Economy</div>
      <div style={{height: 3, width: line, margin: '28px 0 24px', background: COLORS.goldBright}}/>
      <div style={{fontFamily: FONTS.sans, fontSize: 34, maxWidth: 1240, textAlign: 'center', lineHeight: 1.3}}>Build and run a one-person business with useful AI and practical workflows.</div>
      <Kicker screen={screen} dark/>
    </AbsoluteFill>
  );
};

const EpisodeTitleScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame=useCurrentFrame(); const t=motion(frame,0,18);
  return <AbsoluteFill style={{background:COLORS.paper,color:COLORS.ink900}}>
    <div style={{position:'absolute',left:105,top:220,right:105,opacity:t,transform:`translateY(${(1-t)*22}px)`}}>
      <div style={{fontFamily:FONTS.display,fontWeight:800,fontSize:112,lineHeight:.9,letterSpacing:'-.06em'}}>Direct-booking<br/>recovery</div>
      <div style={{height:5,width:interpolate(frame,[12,38],[0,920],clamp),background:COLORS.draftingBlue,marginTop:42}}/>
      <div style={{fontFamily:FONTS.sans,fontSize:31,color:COLORS.ink500,marginTop:28}}>Use the platforms for reach. Help the property earn the return.</div>
    </div>
    <Kicker screen={screen}/>
  </AbsoluteFill>;
};

const PlatformPathScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame=useCurrentFrame(); const direct=screen.id==='V009';
  const nodes=['Platform reach','A good stay','Property relationship'];
  return <AbsoluteFill style={{background:COLORS.navy,...grid,color:COLORS.onInk}}>
    <div style={{position:'absolute',left:90,top:95,right:90,fontFamily:FONTS.display,fontSize:72,fontWeight:800,lineHeight:.98,letterSpacing:'-.05em'}}>{direct?'The stay belongs to the hotel. So should the relationship.':'Keep the reach. Change who owns the return.'}</div>
    <div style={{position:'absolute',left:130,right:130,top:470,display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:90}}>
      {nodes.map((n,i)=>{const t=motion(frame,8+i*10,24+i*10);return <div key={n} style={{position:'relative',padding:'34px 20px',border:`2px solid ${i===2?COLORS.goldBright:COLORS.schemNodeBorder}`,fontFamily:FONTS.sans,fontSize:30,fontWeight:700,textAlign:'center',opacity:t,color:i===2?COLORS.goldBright:COLORS.onInk}}>{n}{i<2?<span style={{position:'absolute',right:-62,color:COLORS.goldBright}}>→</span>:null}</div>})}
    </div><Kicker screen={screen} dark/>
  </AbsoluteFill>;
};

const JourneyScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame=useCurrentFrame();
  const stages=['Discovered','Booked','Welcomed','Remembered','Returned'];
  const active=Math.min(4,Math.max(0,screen.id==='V010'?0:screen.id==='V011'?1:screen.id==='V012'?2:screen.id==='V013'||screen.id==='V014'?3:4));
  return <AbsoluteFill style={{background:COLORS.navy,...grid,color:COLORS.onInk}}>
    <div style={{position:'absolute',left:86,top:78,right:86,fontFamily:FONTS.display,fontSize:68,fontWeight:800,lineHeight:.98,letterSpacing:'-.045em'}}>{short(screen.coverage_narration,100)}</div>
    <div style={{position:'absolute',left:95,right:95,top:465,display:'grid',gridTemplateColumns:'repeat(5,1fr)',gap:36}}>
      {stages.map((stage,i)=>{const t=motion(frame,6+i*6,18+i*6);const on=i<=active;return <div key={stage} style={{position:'relative',minHeight:168,padding:'30px 16px',border:`2px solid ${on?(i===active?COLORS.goldBright:'#78a4cf'):COLORS.schemNodeBorder}`,background:on?COLORS.schemNodeBg:'transparent',opacity:t,fontFamily:FONTS.sans,fontSize:34,fontWeight:700,textAlign:'center',color:i===active?COLORS.goldBright:COLORS.onInk}}><div style={{fontFamily:FONTS.mono,fontSize:16,marginBottom:22,opacity:.7}}>{String(i+1).padStart(2,'0')}</div>{stage}{i<4?<span style={{position:'absolute',right:-28,top:68,color:on?COLORS.goldBright:COLORS.schemNodeBorder}}>→</span>:null}</div>})}
    </div><Kicker screen={screen} dark/>
  </AbsoluteFill>;
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

const KineticTypeScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame=useCurrentFrame();
  const text=screen.coverage_narration || '';
  const emphasis=(text.match(/\b[A-Z][A-Z\s-]{3,}\b/)?.[0] || text.split(/[,.:]/)[0] || 'THE HANDOFF').trim();
  const t=motion(frame,0,16);
  const echo=interpolate(frame,[8,40],[120,0],clamp);
  return <AbsoluteFill style={{background:COLORS.ink,color:COLORS.onInk,overflow:'hidden'}}>
    {[0,1,2].map((i)=><div key={i} style={{position:'absolute',left:60+i*12,top:150+i*echo,fontFamily:FONTS.sans,fontWeight:800,fontSize:Math.min(176,1550/Math.max(8,emphasis.length)*10),lineHeight:.82,letterSpacing:'-.075em',color:i===0?COLORS.onInk:`rgba(245,240,230,${.12-i*.03})`,opacity:t}}>{emphasis}</div>)}
    <div style={{position:'absolute',left:80,right:80,bottom:150,borderTop:`5px solid ${COLORS.goldBright}`,paddingTop:26,fontFamily:FONTS.sans,fontSize:31,lineHeight:1.25}}>{short(text,150)}</div>
    <Kicker screen={screen} dark/>
  </AbsoluteFill>;
};

const ChecklistScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame=useCurrentFrame();
  const seeds=(screen.visual_intent || '').split(/[;,.]|\band\b/i).map(v=>v.trim()).filter(v=>v.length>5).slice(0,5);
  const items=seeds.length>=3?seeds:['Find the friction','Name the owner','Test the handoff','Record the baseline'];
  return <AbsoluteFill style={{background:COLORS.paper,color:COLORS.ink900}}>
    <div style={{position:'absolute',left:82,top:72,width:720,fontFamily:FONTS.display,fontSize:72,fontWeight:800,lineHeight:.98,letterSpacing:'-.05em'}}>{short(screen.coverage_narration,105)}</div>
    <div style={{position:'absolute',left:900,right:80,top:100,bottom:100,border:`2px solid ${COLORS.ruleStrong}`,background:'#fff'}}>
      <div style={{height:62,borderBottom:`1px solid ${COLORS.ruleStrong}`,padding:'20px 26px',fontFamily:FONTS.mono,fontSize:16,textTransform:'uppercase',color:COLORS.draftingBlue}}>Operator control surface · live pass</div>
      {items.map((item,i)=>{const t=motion(frame,7+i*9,20+i*9);return <div key={item} style={{display:'grid',gridTemplateColumns:'68px 1fr',alignItems:'center',padding:'21px 26px',borderBottom:`1px solid ${COLORS.rule}`,opacity:t,transform:`translateX(${(1-t)*22}px)`}}><div style={{width:30,height:30,border:`2px solid ${COLORS.draftingBlue}`,background:t>.96?COLORS.draftingBlue:'transparent',color:'#fff',fontFamily:FONTS.sans,textAlign:'center',lineHeight:'27px'}}>✓</div><div style={{fontFamily:FONTS.sans,fontSize:27,fontWeight:700}}>{short(item,76)}</div></div>})}
    </div><Kicker screen={screen}/>
  </AbsoluteFill>;
};

const CtaScene: React.FC<{screen: Screen}> = ({screen}) => {
  const frame=useCurrentFrame();const t=motion(frame,0,18);
  return <AbsoluteFill style={{background:COLORS.navy,...grid,color:COLORS.onInk,alignItems:'center',justifyContent:'center'}}>
    <div style={{fontFamily:FONTS.sans,fontSize:30,color:COLORS.goldBright,marginBottom:28}}>THE NEXT OPERATING ADVANTAGE</div>
    <div style={{fontFamily:FONTS.display,fontSize:108,fontWeight:800,lineHeight:.9,letterSpacing:'-.06em',textAlign:'center',opacity:t}}>Build it.<br/>Own it. Operate it.</div>
    <div style={{height:5,width:interpolate(frame,[14,44],[0,980],clamp),background:COLORS.goldBright,marginTop:40}}/>
    <Kicker screen={screen} dark/>
  </AbsoluteFill>;
};

const mediaTypes = new Set(['hospitality_footage','platform_visual','interface_capture','source_document','headline_document']);
const dataTypes = new Set(['custom_chart','comparison_chart','evidence_card']);
const processTypes = new Set(['process_diagram','stack_diagram']);
const documentTypes = new Set(['document_template']);

export const CoverageScene: React.FC<{screen: Screen}> = ({screen}) => {
  const type = screen.coverage_asset_type || 'visual_metaphor';
  if (screen.id === 'V001') return <ColdOpenScene screen={screen}/>;
  if (screen.id === 'V005') return <BrandScene screen={screen}/>;
  if (screen.id === 'V006') return <EpisodeTitleScene screen={screen}/>;
  if (screen.id === 'V007' || screen.id === 'V009') return <PlatformPathScene screen={screen}/>;
  if (/^V0(?:10|11|12|13|14|15|16|17|18|19)$/.test(screen.id)) return <JourneyScene screen={screen}/>;
  if (screen.coverage_media) return <MediaScene screen={screen}/>;
  if (mediaTypes.has(type)) return <MissingMedia screen={screen}/>;
  if (type === 'brand_ident') return <BrandScene screen={screen}/>;
  if (dataTypes.has(type)) return <DataScene screen={screen}/>;
  if (processTypes.has(type)) return <ProcessScene screen={screen}/>;
  if (type === 'checklist_motion') return <ChecklistScene screen={screen}/>;
  if (documentTypes.has(type)) return <DocumentScene screen={screen}/>;
  if (type === 'cta_card') return <CtaScene screen={screen}/>;
  if (type === 'outcome_card' || type === 'visual_metaphor') return <KineticTypeScene screen={screen}/>;
  return <DocumentScene screen={screen}/>;
};
