import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

import type {Screen} from '../../BlueprintComposition';
import {COLORS, FONTS} from '../theme';

const grid: React.CSSProperties = {
  backgroundImage:
    `repeating-linear-gradient(0deg, ${COLORS.schemGrid} 0 1px, transparent 1px 48px), ` +
    `repeating-linear-gradient(90deg, ${COLORS.schemGrid} 0 1px, transparent 1px 48px)`,
};

const enter = (frame: number, from = 0, to = 18) =>
  interpolate(frame, [from, to], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

const Source: React.FC<{children: React.ReactNode; dark?: boolean}> = ({children, dark}) => (
  <div style={{
    position: 'absolute', left: 76, bottom: 50, fontFamily: FONTS.mono,
    fontSize: 16, letterSpacing: '0.04em', textTransform: 'uppercase',
    color: dark ? COLORS.onInkMuted : COLORS.ink500,
  }}>{children}</div>
);

const ColdOpen: React.FC = () => {
  const frame = useCurrentFrame();
  const t = enter(frame, 0, 16);
  return (
    <AbsoluteFill style={{background: COLORS.ink, overflow: 'hidden'}}>
      <Img src={staticFile('thumbs/direct-booking-recovery-ota-gravity.png')} style={{
        width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1.035 + frame * 0.00006})`,
      }}/>
      <AbsoluteFill style={{background: 'linear-gradient(90deg,rgba(18,19,18,.98) 0 35%,rgba(18,19,18,.68) 49%,rgba(18,19,18,.05) 72%)'}}/>
      <div style={{position: 'absolute', left: 96, top: 162, width: 900, opacity: t, transform: `translateY(${(1-t)*24}px)`}}>
        <div style={{fontFamily: FONTS.display, fontWeight: 800, fontSize: 114, lineHeight: .9, letterSpacing: '-.055em', color: COLORS.onInk}}>
          Hotels keep<br/>paying to meet<br/><span style={{color: COLORS.goldBright}}>the same guest.</span>
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: 18, marginTop: 34, color: COLORS.onInk, fontFamily: FONTS.sans, fontSize: 26}}>
          <span style={{width: 72, height: 3, background: COLORS.goldBright}}/>
          First booking: reach. Second booking: relationship.
        </div>
      </div>
      <Source dark>Visual thesis · OTA discovery is useful · repeat dependence is the problem</Source>
    </AbsoluteFill>
  );
};

const EvidenceReport: React.FC = () => {
  const frame = useCurrentFrame();
  const docT = enter(frame, 0, 16);
  const numberT = enter(frame, 14, 32);
  return (
    <AbsoluteFill style={{background: COLORS.paper, color: COLORS.ink900}}>
      <div style={{position: 'absolute', left: 76, top: 66, bottom: 88, width: 1030, overflow: 'hidden', border: `1px solid ${COLORS.rule}`, opacity: docT, transform: `translateX(${(1-docT)*-32}px)`}}>
        <Img src={staticFile('evidence/direct-booking-recovery/cloudbeds-report.png')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'center'}}/>
      </div>
      <div style={{position: 'absolute', left: 1170, right: 80, top: 250}}>
        <div style={{fontFamily: FONTS.mono, fontSize: 170, lineHeight: .9, letterSpacing: '-.08em', color: COLORS.draftingBlue, opacity: numberT, transform: `translateY(${(1-numberT)*26}px)`}}>60%+</div>
        <div style={{fontFamily: FONTS.sans, fontSize: 38, lineHeight: 1.24, marginTop: 32}}>of independent-hotel reservations came through online travel agencies.</div>
        <div style={{fontFamily: FONTS.mono, fontSize: 17, letterSpacing: '.08em', textTransform: 'uppercase', borderTop: `1px solid ${COLORS.ruleStrong}`, marginTop: 48, paddingTop: 22}}>Cloudbeds · vendor-published research · 2026</div>
      </div>
      <Source>Source: Cloudbeds · State of Independent Hotels · roughly 90M bookings</Source>
    </AbsoluteFill>
  );
};

const BookingInterface: React.FC = () => {
  const frame = useCurrentFrame();
  const t = enter(frame, 0, 18);
  return (
    <AbsoluteFill style={{background: COLORS.paper}}>
      <div style={{position: 'absolute', left: 52, top: 54, bottom: 70, width: 1250, overflow: 'hidden', border: `1px solid ${COLORS.ruleStrong}`, opacity: t, transform: `translateX(${(1-t)*-28}px)`}}>
        <Img src={staticFile('evidence/direct-booking-recovery/booking-results.png')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top'}}/>
        <div style={{position: 'absolute', left: 22, top: 22, padding: '13px 19px', background: '#003b95', color: '#fff', fontFamily: FONTS.sans, fontSize: 34, fontWeight: 700, letterSpacing: '-.04em'}}>Booking<span style={{color: '#28a9e0'}}>.com</span></div>
      </div>
      <div style={{position: 'absolute', left: 1370, right: 70, top: 235}}>
        <div style={{fontFamily: FONTS.display, fontSize: 78, fontWeight: 800, lineHeight: .94, letterSpacing: '-.055em', color: COLORS.ink900}}>Reach, trust and a checkout that already works.</div>
        <div style={{fontFamily: FONTS.sans, fontSize: 30, lineHeight: 1.35, color: COLORS.ink500, marginTop: 34}}>The platform earns its commission by making discovery and booking easier.</div>
      </div>
      <Source>Current interface capture · logged out · prices incidental, not narrated</Source>
    </AbsoluteFill>
  );
};

const CancellationChart: React.FC = () => {
  const frame = useCurrentFrame();
  const ota = enter(frame, 8, 34);
  const direct = enter(frame, 22, 48);
  return (
    <AbsoluteFill style={{background: COLORS.paper}}>
      <div style={{position: 'absolute', left: 105, top: 180, width: 610}}>
        <div style={{fontFamily: FONTS.display, fontSize: 92, fontWeight: 800, lineHeight: .93, letterSpacing: '-.055em'}}>Commission isn't the only cost.</div>
        <div style={{fontFamily: FONTS.sans, fontSize: 34, lineHeight: 1.35, color: COLORS.ink500, marginTop: 38}}>The hotel may pay more for a reservation that is also more likely to disappear.</div>
      </div>
      <div style={{position: 'absolute', left: 830, right: 100, top: 130, bottom: 120, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: 150, borderLeft: `1px solid ${COLORS.rule}`, paddingLeft: 90}}>
        {[{v:'21.8%',h:620,t:ota,label:'OTA',fill:COLORS.draftingBlue},{v:'10.6%',h:302,t:direct,label:'Direct',fill:'transparent'}].map((b) => <div key={b.label} style={{width: 300, textAlign: 'center'}}>
          <div style={{fontFamily: FONTS.sans, fontVariantNumeric: 'tabular-nums', fontWeight: 650, fontSize: 62, marginBottom: 18}}>{b.v}</div>
          <div style={{height: b.h * b.t, border: `2px solid ${COLORS.draftingBlue}`, background: b.fill, transformOrigin: 'bottom'}}/>
          <div style={{fontFamily: FONTS.sans, fontSize: 28, fontWeight: 700, marginTop: 18}}>{b.label}</div>
        </div>)}
      </div>
      <Source>Source: Cloudbeds · OTA commission guide · vendor-published data</Source>
    </AbsoluteFill>
  );
};

const Journey: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const stages = ['Discovered','Booked','Welcomed','Remembered','Returned'];
  const notes = ['OTA reach','First stay','Hotel delivers','Useful follow-up','Direct relationship'];
  const pathT = interpolate(frame, [8, fps * 2.8], [0, 1], {extrapolateLeft:'clamp', extrapolateRight:'clamp', easing:Easing.inOut(Easing.cubic)});
  return (
    <AbsoluteFill style={{background: COLORS.navy, ...grid, color: COLORS.onInk}}>
      <div style={{position:'absolute',left:115,top:105,fontFamily:FONTS.display,fontWeight:800,fontSize:96,lineHeight:.94,letterSpacing:'-.055em'}}>Use the platform for reach.<br/>Earn the return.</div>
      <div style={{position:'absolute',left:135,right:135,top:420,display:'grid',gridTemplateColumns:'repeat(5,1fr)',gap:62}}>
        {stages.map((stage,i)=>{const t=enter(frame,12+i*10,26+i*10);return <div key={stage} style={{textAlign:'center',opacity:t,transform:`translateY(${(1-t)*14}px)`}}><div style={{width:20,height:20,borderRadius:'50%',margin:'0 auto',background:i<2?'#78a4cf':COLORS.goldBright,boxShadow:`0 0 0 5px ${COLORS.navy},0 0 0 7px ${i<2?'#78a4cf':COLORS.goldBright}`}}/><div style={{fontFamily:FONTS.sans,fontWeight:700,fontSize:28,marginTop:42}}>{stage}</div><div style={{fontFamily:FONTS.mono,fontSize:15,textTransform:'uppercase',letterSpacing:'.06em',opacity:.58,marginTop:13}}>{notes[i]}</div></div>})}
      </div>
      <div style={{position:'absolute',left:150,right:150,top:665,height:4,background:'rgba(245,240,230,.22)'}}><div style={{height:'100%',width:`${pathT*100}%`,background:pathT<.44?'#35608c':COLORS.goldBright}}/></div>
      <div style={{position:'absolute',left:950,bottom:90,borderLeft:`4px solid ${COLORS.goldBright}`,padding:'12px 20px',fontFamily:FONTS.sans,fontSize:28}}>The handoff: platform demand → property relationship</div>
    </AbsoluteFill>
  );
};

const OperatingPath: React.FC = () => {
  const frame = useCurrentFrame();
  const nodes = ['Easy to find','Direct feels credible','Guest remembered','Returns direct'];
  return (
    <AbsoluteFill style={{background: COLORS.navy, ...grid, color: COLORS.onInk}}>
      <div style={{position:'absolute',left:110,top:105,fontFamily:FONTS.display,fontWeight:800,fontSize:96,lineHeight:.92,letterSpacing:'-.055em'}}>More repeat business<br/>the hotel doesn't buy again.</div>
      <div style={{position:'absolute',left:145,right:145,top:500,display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:70}}>
        {nodes.map((n,i)=>{const t=enter(frame,10+i*12,24+i*12);return <div key={n} style={{position:'relative',padding:'28px 18px',border:`2px solid ${i===3?COLORS.goldBright:COLORS.schemNodeBorder}`,background:COLORS.schemNodeBg,textAlign:'center',fontFamily:FONTS.sans,fontSize:29,fontWeight:500,opacity:t,transform:`translateY(${(1-t)*18}px)`,color:i===3?COLORS.goldBright:COLORS.onInk}}>{n}{i<3?<span style={{position:'absolute',right:-48,color:COLORS.goldBright}}>→</span>:null}</div>})}
      </div>
      <div style={{position:'absolute',left:145,right:145,top:700,display:'flex',justifyContent:'space-between',padding:'22px 24px',borderTop:`1px solid ${COLORS.schemNodeBorder}`,borderBottom:`1px solid ${COLORS.schemNodeBorder}`,fontFamily:FONTS.sans,fontSize:27}}><b>One operator owns the handoffs.</b><span style={{fontFamily:FONTS.mono,fontSize:17,textTransform:'uppercase',color:COLORS.sage}}>Human review · approve / do not send</span></div>
      <Source dark>The workflow is the product · tools enter only where they serve the path</Source>
    </AbsoluteFill>
  );
};

export const ApprovedEpisodeScene: React.FC<{screen: Screen}> = ({screen}) => {
  switch (screen.id) {
    case 'hook-01': return <ColdOpen/>;
    case 'hook-02':
    case 'evidence-01': return <EvidenceReport/>;
    case 'evidence-02': return <BookingInterface/>;
    case 'evidence-03': return <CancellationChart/>;
    case 'thesis-01': return <Journey/>;
    case 'stack-05': return <OperatingPath/>;
    default: return null;
  }
};

export const isApprovedEpisodeScreen = (screen: Screen) =>
  ['hook-01','hook-02','thesis-01','evidence-01','evidence-02','evidence-03','stack-05'].includes(screen.id);
