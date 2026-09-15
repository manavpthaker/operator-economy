import {AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {DeckObject} from './components/DeckObject';
import type {AssetTicket, Evidence, RenderData, VisualUnit} from './types';

export const DECK_PROTOTYPE_SECONDS = 90;

const UNIT_TITLES: Record<string, {index: string; title: string; emphasis: string}> = {
  'unit-001': {index: '01', title: 'A guest completes a stay.', emphasis: 'THE STAY'},
  'unit-002': {index: '02', title: 'The OTA made the introduction.', emphasis: 'THE FIRST BOOKING'},
  'unit-003': {index: '03', title: 'Then the same guest goes back through the paid gate.', emphasis: 'THE LEAK'},
  'unit-004': {index: '04', title: 'The fix starts by testing the hotel’s direct path.', emphasis: 'AUDIT FIRST'},
  'unit-005': {index: '05', title: 'The OTA is useful acquisition—not the villain.', emphasis: 'KEEP THE REACH'},
  'unit-006': {index: '06', title: 'The first booking can stay OTA.', emphasis: 'FIRST BOOKING'},
  'unit-007': {index: '07', title: 'The hotel still delivers the actual stay.', emphasis: 'HUMAN SERVICE'},
  'unit-008': {index: '08', title: 'A completed stay is not permission to market.', emphasis: 'STAY ≠ CONSENT'},
  'unit-009': {index: '09', title: 'Without a return path, the relationship leaks.', emphasis: 'BROKEN RETURN'},
  'unit-010': {index: '10', title: 'The opportunity is the next appropriate booking.', emphasis: 'SECOND BOOKING'},
  'unit-011': {index: '11', title: 'Today, nobody owns the whole return journey.', emphasis: 'NO OWNER'},
  'unit-012': {index: '12', title: 'Every handoff sits in a different place.', emphasis: 'DISCONNECTED'},
  'unit-013': {index: '13', title: 'Follow-up happens only if somebody remembers.', emphasis: 'RETRY'},
};

const activeUnit = (units: VisualUnit[], seconds: number): VisualUnit =>
  units.find((unit) => seconds >= unit.in && seconds < unit.out) ?? units[0];

const unitNumber = (unit: VisualUnit): number => Number(unit.id.split('-')[1]);

const PrototypeProgress: React.FC<{seconds: number; colors: Record<string, string>}> = ({seconds, colors}) => (
  <div style={{position: 'absolute', left: 0, bottom: 0, width: `${Math.min(100, (seconds / DECK_PROTOTYPE_SECONDS) * 100)}%`, height: 12, background: colors.ledger_gold}} />
);

const BrandIdentitySlide: React.FC<{
  progress: number;
  seconds: number;
  colors: Record<string, string>;
}> = ({progress, seconds, colors}) => {
  const reveal = interpolate(progress, [0, 0.18, 0.72, 1], [0, 1, 1, 0.94], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const rule = interpolate(progress, [0.08, 0.52], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: colors.schematic_navy, color: colors.paper, overflow: 'hidden'}} data-bookend="show-identity">
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(245,240,230,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(245,240,230,0.055) 1px, transparent 1px)', backgroundSize: '54px 54px'}} />
      <div style={{position: 'absolute', left: 120, top: 96, fontFamily: 'Courier New, monospace', fontSize: 16, letterSpacing: 2.4, color: colors.ledger_gold, fontWeight: 900}}>
        SHOW IDENTITY · TYPOGRAPHIC WORDMARK
      </div>
      <div style={{position: 'absolute', left: 120, top: 230, opacity: reveal, transform: `translateY(${(1 - reveal) * 26}px)`}}>
        <div style={{fontFamily: 'Arial, Helvetica, sans-serif', fontSize: 39, fontWeight: 500, letterSpacing: 1.5, color: 'rgba(245,240,230,0.7)'}}>The</div>
        <div style={{fontFamily: 'Georgia, Times New Roman, serif', fontSize: 128, lineHeight: 0.92, fontWeight: 700, letterSpacing: -5}}>Operator</div>
        <div style={{fontFamily: 'Georgia, Times New Roman, serif', fontSize: 128, lineHeight: 0.92, fontWeight: 700, letterSpacing: -5, color: colors.ledger_gold}}>Economy</div>
      </div>
      <div style={{position: 'absolute', left: 120, top: 620, width: 1020 * rule, height: 7, background: colors.ledger_gold}} />
      <div style={{position: 'absolute', left: 120, bottom: 170, display: 'flex', gap: 24, alignItems: 'baseline', fontFamily: 'Georgia, Times New Roman, serif', fontSize: 45, fontWeight: 700, opacity: reveal}}>
        <span>Build.</span><span>Own.</span><span>Operate.</span>
      </div>
      <div style={{position: 'absolute', right: 120, bottom: 112, fontFamily: 'Courier New, monospace', fontSize: 15, letterSpacing: 1.8, color: 'rgba(245,240,230,0.58)'}}>
        CANONICAL WORDMARK · NO SEPARATE ICON MARK
      </div>
      <PrototypeProgress seconds={seconds} colors={colors} />
    </AbsoluteFill>
  );
};

const EpisodeTitleSlide: React.FC<{
  progress: number;
  seconds: number;
  colors: Record<string, string>;
}> = ({progress, seconds, colors}) => {
  const reveal = interpolate(progress, [0, 0.16], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const route = interpolate(progress, [0.18, 0.68], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: colors.paper, color: colors.ink, overflow: 'hidden'}} data-bookend="episode-title">
      <div style={{position: 'absolute', left: 0, top: 0, width: 415, height: 1080, background: colors.schematic_navy}} />
      <div style={{position: 'absolute', left: 62, top: 62, color: colors.ledger_gold, fontFamily: 'Courier New, monospace', fontSize: 24, fontWeight: 900, letterSpacing: 2}}>EP006</div>
      <div style={{position: 'absolute', left: 62, top: 250, width: 290, color: colors.paper, fontFamily: 'Courier New, monospace', fontSize: 17, lineHeight: 1.5, letterSpacing: 1.5}}>
        OPENING TITLE<br />DIRECT-BOOKING<br />RECOVERY
      </div>
      <div style={{position: 'absolute', left: 510, top: 155, opacity: reveal, transform: `translateY(${(1 - reveal) * 22}px)`}}>
        <div style={{fontFamily: 'Courier New, monospace', fontSize: 18, fontWeight: 900, letterSpacing: 2.4, color: colors.negative}}>THE OPERATOR ECONOMY · EPISODE 006</div>
        <div style={{fontFamily: 'Georgia, Times New Roman, serif', fontSize: 112, lineHeight: 0.95, fontWeight: 700, letterSpacing: -4, marginTop: 30}}>Direct Booking</div>
        <div style={{fontFamily: 'Georgia, Times New Roman, serif', fontSize: 112, lineHeight: 0.95, fontWeight: 700, letterSpacing: -4, color: colors.drafting_blue}}>Recovery</div>
      </div>

      <div style={{position: 'absolute', left: 510, top: 610, width: 1260, borderTop: `5px solid ${colors.schematic_navy}`, paddingTop: 28, fontFamily: 'Arial, Helvetica, sans-serif'}}>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 120px 1fr', alignItems: 'center', gap: 24}}>
          <div>
            <div style={{fontFamily: 'Courier New, monospace', fontSize: 15, fontWeight: 900, letterSpacing: 1.6, color: colors.ledger_gold}}>FIRST BOOKING</div>
            <div style={{fontSize: 31, fontWeight: 900, marginTop: 7}}>OTA can be useful acquisition</div>
          </div>
          <div style={{height: 8, width: `${120 * route}px`, background: colors.ledger_gold, position: 'relative'}}>
            <div style={{position: 'absolute', right: -2, top: -12, width: 0, height: 0, borderTop: '16px solid transparent', borderBottom: '16px solid transparent', borderLeft: `24px solid ${colors.ledger_gold}`}} />
          </div>
          <div>
            <div style={{fontFamily: 'Courier New, monospace', fontSize: 15, fontWeight: 900, letterSpacing: 1.6, color: colors.sage}}>RETURN OPPORTUNITY</div>
            <div style={{fontSize: 31, fontWeight: 900, marginTop: 7}}>Next appropriate booking: direct</div>
          </div>
        </div>
      </div>
      <div style={{position: 'absolute', right: 75, bottom: 74, fontFamily: 'Courier New, monospace', fontSize: 15, color: colors.drafting_blue, letterSpacing: 1.2}}>GREYBOX TITLE PLATE · NO POLISHED ASSETS</div>
      <PrototypeProgress seconds={seconds} colors={colors} />
    </AbsoluteFill>
  );
};

const ReviewPlaceholder: React.FC<{
  ticket?: AssetTicket;
  evidence?: Evidence;
  colors: Record<string, string>;
}> = ({ticket, evidence, colors}) => {
  if (!ticket && !evidence) return null;
  return (
    <div
      style={{
        position: 'absolute',
        right: 70,
        bottom: 50,
        width: 390,
        border: `4px dashed ${colors.negative}`,
        background: colors.paper,
        color: colors.ink,
        padding: '15px 18px',
        fontFamily: 'Arial, Helvetica, sans-serif',
        boxSizing: 'border-box',
      }}
    >
      <div style={{fontFamily: 'Courier New, monospace', fontSize: 14, fontWeight: 900, color: colors.negative, letterSpacing: 1.6}}>
        GREYBOX PLACEHOLDER
      </div>
      <div style={{fontSize: 19, lineHeight: 1.15, fontWeight: 800, marginTop: 6}}>
        {evidence?.label ?? ticket?.story_role}
      </div>
      <div style={{fontSize: 13, marginTop: 7, opacity: 0.68}}>{ticket?.id ?? evidence?.id}</div>
    </div>
  );
};

const CoinStack: React.FC<{visible: boolean; active: boolean; colors: Record<string, string>}> = ({visible, active, colors}) => (
  <div
    style={{
      position: 'absolute',
      left: 720,
      top: 458,
      width: 410,
      opacity: visible ? 1 : 0,
      transform: `translateY(${visible ? 0 : 28}px)`,
      borderTop: `5px solid ${active ? colors.ledger_gold : colors.drafting_blue}`,
      paddingTop: 13,
      fontFamily: 'Arial, Helvetica, sans-serif',
      color: colors.ink,
      transition: 'none',
    }}
    data-object-id="first-booking-money-flow"
  >
    <div style={{display: 'flex', alignItems: 'center', gap: 8}}>
      {[0, 1, 2].map((item) => (
        <div key={item} style={{width: 34, height: 34, borderRadius: '50%', border: `6px solid ${colors.ledger_gold}`, background: colors.paper}} />
      ))}
      <div style={{fontSize: 24, fontWeight: 900}}>COMMISSION</div>
    </div>
    <div style={{fontSize: 14, marginTop: 6, fontFamily: 'Courier New, monospace'}}>OPERATOR-SIDE ECONOMIC CONSEQUENCE</div>
  </div>
);

const GateChip: React.FC<{left: number; label: string; active: boolean; colors: Record<string, string>}> = ({left, label, active, colors}) => (
  <div
    style={{
      position: 'absolute',
      left,
      top: 650,
      width: 200,
      height: 54,
      display: 'grid',
      placeItems: 'center',
      background: colors.paper,
      border: `4px solid ${active ? colors.ledger_gold : colors.drafting_blue}`,
      color: colors.ink,
      fontFamily: 'Courier New, monospace',
      fontSize: 12,
      fontWeight: 900,
      letterSpacing: 1.2,
      textAlign: 'center',
      lineHeight: 1.08,
      padding: '0 7px',
      boxSizing: 'border-box',
    }}
  >
    {label}
  </div>
);

const JourneySlide: React.FC<{
  unit: VisualUnit;
  progress: number;
  colors: Record<string, string>;
  ticket?: AssetTicket;
  evidence?: Evidence;
}> = ({unit, progress, colors, ticket, evidence}) => {
  const step = unitNumber(unit);
  const firstRoute = step >= 2;
  const showCommission = step >= 6;
  const leak = step === 3 || step === 9;
  const audit = step === 4;
  const directPreview = step === 10;
  const routeTokenX = interpolate(progress, [0, 0.5, 1], [380, 850, 1390], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const activeRouteToken = [2, 5, 6, 7].includes(step);

  return (
    <div style={{position: 'absolute', left: 0, top: 225, width: 1920, height: 780}}>
      <svg width={1920} height={760} style={{position: 'absolute', inset: 0}} aria-label="Guest booking and return relationship">
        <defs>
          <marker id="deck-arrow-gold" markerWidth="11" markerHeight="11" refX="9" refY="5.5" orient="auto">
            <path d="M0,0 L11,5.5 L0,11 Z" fill={colors.ledger_gold} />
          </marker>
          <marker id="deck-arrow-red" markerWidth="11" markerHeight="11" refX="9" refY="5.5" orient="auto">
            <path d="M0,0 L11,5.5 L0,11 Z" fill={colors.negative} />
          </marker>
          <marker id="deck-arrow-sage" markerWidth="11" markerHeight="11" refX="9" refY="5.5" orient="auto">
            <path d="M0,0 L11,5.5 L0,11 Z" fill={colors.sage} />
          </marker>
        </defs>
        <path d="M390 305 H710" fill="none" stroke={colors.ledger_gold} strokeWidth={12} opacity={firstRoute ? 1 : 0.18} markerEnd="url(#deck-arrow-gold)" />
        <path d="M1120 305 H1390" fill="none" stroke={colors.ledger_gold} strokeWidth={12} opacity={firstRoute ? 1 : 0.18} markerEnd="url(#deck-arrow-gold)" />
        <text x={495} y={276} fill={colors.ink} fontFamily="Courier New, monospace" fontSize={18} fontWeight={900} opacity={firstRoute ? 1 : 0.35}>DISCOVERY</text>
        <text x={1186} y={276} fill={colors.ink} fontFamily="Courier New, monospace" fontSize={18} fontWeight={900} opacity={firstRoute ? 1 : 0.35}>RESERVATION</text>

        <path d="M1455 250 C1320 66 1050 56 914 168" fill="none" stroke={colors.negative} strokeWidth={12} strokeDasharray="22 16" opacity={leak ? 1 : 0} markerEnd="url(#deck-arrow-red)" />
        <text x={1090} y={80} fill={colors.negative} fontFamily="Arial, Helvetica, sans-serif" fontSize={28} fontWeight={900} opacity={leak ? 1 : 0}>NEXT TRIP GOES BACK TO THE PAID GATE</text>

        <path d="M1385 520 C1230 665 1095 704 1045 704" fill="none" stroke={colors.negative} strokeWidth={12} opacity={leak ? 1 : 0} />
        <path d="M760 704 C650 690 530 625 390 520" fill="none" stroke={colors.negative} strokeWidth={12} opacity={leak ? 1 : 0} markerEnd="url(#deck-arrow-red)" />
        <line x1={854} y1={674} x2={926} y2={734} stroke={colors.negative} strokeWidth={15} opacity={leak ? 1 : 0} />
        <line x1={926} y1={674} x2={854} y2={734} stroke={colors.negative} strokeWidth={15} opacity={leak ? 1 : 0} />
        <text x={772} y={642} fill={colors.negative} fontFamily="Courier New, monospace" fontSize={21} fontWeight={900} opacity={leak ? 1 : 0}>NO OWNED RETURN PATH</text>

        <path d="M390 535 C650 710 1150 710 1390 535" fill="none" stroke={colors.sage} strokeWidth={13} strokeDasharray="25 17" opacity={directPreview ? 1 : audit ? 0.18 : 0} markerEnd="url(#deck-arrow-sage)" />
        <text x={676} y={610} fill={colors.sage} fontFamily="Arial, Helvetica, sans-serif" fontSize={28} fontWeight={900} opacity={directPreview ? 1 : 0}>NEXT APPROPRIATE BOOKING · DIRECT</text>

        {activeRouteToken ? <circle cx={routeTokenX} cy={305} r={18} fill={colors.paper} stroke={colors.ledger_gold} strokeWidth={10} /> : null}
      </svg>

      <DeckObject id="stay-key-tag" role="guest" label="Guest / stay" eyebrow="SAME PERSON" left={120} top={170} active={step === 1 || step === 8} colors={colors} note={step >= 7 ? 'STAY COMPLETE' : undefined} />
      <DeckObject id="ota-booking-gate" role="ota" label="OTA gate" eyebrow="PAID INTRODUCTION" left={720} top={170} active={step === 2 || step === 5} colors={colors} note="USEFUL ACQUISITION" />
      <DeckObject id="hotel-stay-node" role="hotel" label="Independent hotel" eyebrow="DELIVERS THE STAY" left={1390} top={170} active={step === 7} colors={colors} />

      <CoinStack visible={showCommission} active={step === 6} colors={colors} />

      {audit || directPreview ? (
        <>
          <GateChip left={540} label={audit ? 'AUDIT · OPEN' : 'AUDIT · REQUIRED'} active={audit} colors={colors} />
          <GateChip left={760} label="PERMISSION · CLOSED" active={false} colors={colors} />
          <GateChip left={980} label="HUMAN REVIEW · CLOSED" active={false} colors={colors} />
        </>
      ) : null}

      <ReviewPlaceholder ticket={ticket} evidence={evidence} colors={colors} />
    </div>
  );
};

const WorkCard: React.FC<{left: number; top: number; label: string; active: boolean; colors: Record<string, string>}> = ({left, top, label, active, colors}) => (
  <div
    style={{
      position: 'absolute',
      left,
      top,
      width: 290,
      height: 118,
      boxSizing: 'border-box',
      background: colors.paper,
      border: `5px ${active ? 'solid' : 'dashed'} ${active ? colors.negative : colors.drafting_blue}`,
      padding: '18px 20px',
      color: colors.ink,
      fontFamily: 'Arial, Helvetica, sans-serif',
      fontSize: 26,
      fontWeight: 900,
      display: 'grid',
      placeItems: 'center start',
    }}
  >
    {label}
  </div>
);

const FragmentedWorkSlide: React.FC<{unit: VisualUnit; colors: Record<string, string>}> = ({unit, colors}) => {
  const step = unitNumber(unit);
  return (
    <div style={{position: 'absolute', left: 0, top: 220, width: 1920, height: 780}}>
      <svg width={1920} height={760} style={{position: 'absolute', inset: 0}}>
        {[
          [510, 170, 790, 295],
          [510, 365, 790, 335],
          [1120, 170, 1050, 295],
          [1120, 365, 1050, 335],
          [815, 565, 920, 480],
        ].map(([x1, y1, x2, y2], index) => (
          <line key={index} x1={x1} y1={y1} x2={x2} y2={y2} stroke={colors.drafting_blue} strokeWidth={7} strokeDasharray="17 14" opacity={step >= 12 ? 1 : 0.45} />
        ))}
      </svg>
      <DeckObject id="independent-hotel-operator" role="operator" label="Hotel operator" eyebrow="ACCOUNTABLE HUMAN" left={790} top={190} active={step === 11} colors={colors} note="BUT NOT THE OWNER OF EVERY HANDOFF" />
      <WorkCard left={155} top={90} label="Google listing" active={false} colors={colors} />
      <WorkCard left={155} top={330} label="Website" active={false} colors={colors} />
      <WorkCard left={1465} top={90} label="Phone / front desk" active={false} colors={colors} />
      <WorkCard left={1465} top={330} label="Booking system" active={false} colors={colors} />
      <WorkCard left={815} top={565} label={step >= 13 ? 'Follow-up: if remembered' : 'Follow-up'} active={step >= 13} colors={colors} />
      <div style={{position: 'absolute', left: 80, bottom: 55, display: 'flex', alignItems: 'center', gap: 16, fontFamily: 'Arial, Helvetica, sans-serif', color: colors.ink}}>
        <div style={{width: 74, height: 74, borderRadius: '50%', background: colors.schematic_navy, border: `5px solid ${colors.ledger_gold}`}} />
        <div>
          <div style={{fontFamily: 'Courier New, monospace', fontSize: 14, fontWeight: 900, letterSpacing: 1.4}}>THE SAME GUEST IS STILL WAITING</div>
          <div style={{fontSize: 25, fontWeight: 900, marginTop: 3}}>No connected return journey</div>
        </div>
      </div>
    </div>
  );
};

export const DeckPrototype: React.FC<RenderData> = (props) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const seconds = frame / fps;
  const unit = activeUnit(props.units, seconds);
  const progress = (seconds - unit.in) / Math.max(0.001, unit.out - unit.in);
  const copy = UNIT_TITLES[unit.id] ?? {index: '--', title: unit.action, emphasis: unit.motion_verb.toUpperCase()};
  const ticket = props.tickets.find((candidate) => unit.asset_ticket_ids.includes(candidate.id));
  const evidence = props.evidence.find((candidate) => unit.evidence_ids.includes(candidate.id));
  const titleIn = interpolate(seconds - unit.in, [0, 0.35], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fragmented = unitNumber(unit) >= 11;

  if (unit.id === 'unit-005') {
    return (
      <AbsoluteFill>
        <Audio src={staticFile(props.audio_file)} />
        <BrandIdentitySlide progress={progress} seconds={seconds} colors={props.palette} />
      </AbsoluteFill>
    );
  }
  if (unit.id === 'unit-006') {
    return (
      <AbsoluteFill>
        <Audio src={staticFile(props.audio_file)} />
        <EpisodeTitleSlide progress={progress} seconds={seconds} colors={props.palette} />
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill style={{background: props.palette.paper, color: props.palette.ink, overflow: 'hidden'}}>
      <Audio src={staticFile(props.audio_file)} />
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(20,38,62,0.055) 1px, transparent 1px)', backgroundSize: '100% 54px'}} />

      <div style={{position: 'absolute', left: 62, top: 40, fontFamily: 'Courier New, monospace', fontSize: 16, fontWeight: 900, letterSpacing: 2.2, color: props.palette.drafting_blue}}>
        EP006 · DECK GREYBOX · OPENING PROTOTYPE
      </div>
      <div style={{position: 'absolute', right: 62, top: 38, fontFamily: 'Courier New, monospace', fontSize: 18, fontWeight: 900, color: props.palette.ledger_gold}}>
        {copy.index} / 13 · {seconds.toFixed(1)}s
      </div>

      <div style={{position: 'absolute', left: 62, right: 62, top: 92, borderTop: `6px solid ${props.palette.schematic_navy}`, paddingTop: 22, opacity: titleIn, transform: `translateY(${(1 - titleIn) * 12}px)`}}>
        <div style={{fontFamily: 'Courier New, monospace', fontSize: 18, fontWeight: 900, letterSpacing: 2.2, color: unit.mode === 'reality' ? props.palette.sage : unit.mode === 'proof' ? props.palette.ledger_gold : props.palette.negative}}>
          {copy.emphasis}
        </div>
        <div style={{fontFamily: 'Arial, Helvetica, sans-serif', fontSize: 57, lineHeight: 1.02, fontWeight: 900, letterSpacing: -1.8, marginTop: 8, maxWidth: 1480}}>{copy.title}</div>
      </div>

      {fragmented ? (
        <FragmentedWorkSlide unit={unit} colors={props.palette} />
      ) : (
        <JourneySlide unit={unit} progress={progress} colors={props.palette} ticket={ticket} evidence={evidence} />
      )}

      <PrototypeProgress seconds={seconds} colors={props.palette} />
    </AbsoluteFill>
  );
};
