import {Audio, AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {cameraRigAt} from './camera';
import {OverviewMap} from './components/OverviewMap';
import {TicketSlate} from './components/TicketSlate';
import {WorldNode} from './components/WorldNode';
import type {RenderData, VisualUnit} from './types';

const stateAt = (props: RenderData, seconds: number): Record<string, string> => {
  const states = Object.fromEntries(props.objects.map((object) => [object.id, object.initial_state]));
  for (const unit of props.units) {
    if (unit.in > seconds) {
      break;
    }
    for (const update of unit.world_state_after) {
      states[update.object_id] = update.state;
    }
  }
  return states;
};

const activeUnitIndex = (units: VisualUnit[], seconds: number): number => {
  const index = units.findIndex((unit) => seconds >= unit.in && seconds < unit.out);
  return index >= 0 ? index : Math.max(0, units.length - 1);
};

export const BlueprintCinema: React.FC<RenderData> = (props) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const seconds = frame / fps;
  const unitIndex = activeUnitIndex(props.units, seconds);
  const unit = props.units[unitIndex];
  const states = stateAt(props, seconds);
  const objectById = new Map(props.objects.map((object) => [object.id, object]));
  const evidenceById = new Map(props.evidence.map((item) => [item.id, item]));
  const ticketById = new Map(props.tickets.map((item) => [item.id, item]));
  const camera = props.cameras.find((item) => item.id === unit.camera_anchor);
  const focused = new Set(unit.focus);
  const carried = new Set(unit.carry);
  const contextual = new Set<string>();
  for (const edge of props.edges) {
    if (focused.has(edge.from)) contextual.add(edge.to);
    if (focused.has(edge.to)) contextual.add(edge.from);
  }
  for (const id of unit.carry) {
    const carriedObject = objectById.get(id);
    const focusObject = unit.focus.map((focusId) => objectById.get(focusId)).find(Boolean);
    if (
      carriedObject &&
      focusObject &&
      Math.hypot(
        carriedObject.position.x - focusObject.position.x,
        carriedObject.position.y - focusObject.position.y,
      ) <= 390
    ) {
      contextual.add(id);
    }
  }
  const rig = cameraRigAt(props, unitIndex, seconds);
  const focusLabel = unit.focus
    .map((id) => objectById.get(id)?.label ?? id)
    .join(' + ');
  const visibleTickets = unit.asset_ticket_ids.map((id) => ticketById.get(id)).filter(Boolean);

  return (
    <AbsoluteFill style={{background: props.palette.ink, color: props.palette.paper, overflow: 'hidden'}}>
      <Audio src={staticFile(props.audio_file)} />
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(245,240,230,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(245,240,230,0.035) 1px, transparent 1px)', backgroundSize: '36px 36px'}} />

      <div
        style={{
          position: 'absolute',
          width: 1920,
          height: 1080,
          transformOrigin: '0 0',
          transform: `translate(${rig.translateX}px, ${rig.translateY}px) scale(${rig.scale})`,
          willChange: 'transform',
        }}
        data-camera-target={`${rig.targetX.toFixed(1)},${rig.targetY.toFixed(1)}`}
      >
        <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(245,240,230,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(245,240,230,0.055) 1px, transparent 1px)', backgroundSize: '36px 36px'}} />
        <div style={{position: 'absolute', left: 0, top: 0, width: 600, height: 960, borderRight: '1px solid rgba(245,240,230,0.18)', background: 'rgba(245,240,230,0.035)'}} />
        <div style={{position: 'absolute', left: 600, top: 0, width: 850, height: 960, borderRight: '1px solid rgba(245,240,230,0.18)', background: 'rgba(31,58,95,0.16)'}} />
        <div style={{position: 'absolute', left: 1450, top: 0, width: 470, height: 960, background: 'rgba(176,141,62,0.055)'}} />
        {[
          ['REALITY', 44],
          ['SYSTEM', 626],
          ['PROOF', 1476],
        ].map(([label, left]) => (
          <div key={label} style={{position: 'absolute', left, top: 34, fontSize: 18, fontFamily: 'Arial, Helvetica, sans-serif', fontWeight: 800, letterSpacing: 3, opacity: 0.34}}>
            {label}
          </div>
        ))}

        <svg width={1920} height={960} style={{position: 'absolute', inset: 0}}>
        <defs>
          <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 Z" fill="rgba(245,240,230,0.38)" />
          </marker>
        </defs>
        {props.edges.map((edge) => {
          const from = objectById.get(edge.from);
          const to = objectById.get(edge.to);
          if (!from || !to) return null;
          const isCurrent = focused.has(edge.from) || focused.has(edge.to);
          const isContext = contextual.has(edge.from) && contextual.has(edge.to);
          return (
            <line
              key={edge.id}
              x1={from.position.x}
              y1={from.position.y}
              x2={to.position.x}
              y2={to.position.y}
              stroke={isCurrent ? props.palette.ledger_gold : isContext ? 'rgba(123,158,135,0.48)' : 'rgba(245,240,230,0.08)'}
              strokeWidth={isCurrent ? 5 : isContext ? 3 : 1.5}
              strokeDasharray={edge.kind === 'failure' || edge.kind === 'suppression' ? '10 8' : undefined}
              markerEnd="url(#arrow)"
            />
          );
        })}
        {unit.evidence_ids.flatMap((id) => {
          const evidence = evidenceById.get(id);
          if (!evidence) return [];
          return evidence.target_ids.map((targetId) => {
            const target = objectById.get(targetId);
            if (!target) return null;
            return (
              <circle
                key={`${id}-${targetId}`}
                cx={target.position.x + 96}
                cy={target.position.y - 42}
                r={11}
                fill={props.palette.ledger_gold}
                stroke={props.palette.paper}
                strokeWidth={3}
              />
            );
          });
        })}
        </svg>

        {props.objects.map((object) => (
          <WorldNode
            key={object.id}
            object={object}
            state={states[object.id]}
            focused={focused.has(object.id)}
            contextual={contextual.has(object.id)}
            carried={carried.has(object.id)}
            colors={props.palette}
          />
        ))}
      </div>

      <div style={{position: 'absolute', left: 28, top: 26, width: 720, borderLeft: `5px solid ${props.palette.ledger_gold}`, background: 'rgba(26,26,26,0.91)', padding: '13px 17px 14px', fontFamily: 'Arial, Helvetica, sans-serif'}}>
        <div style={{fontSize: 13, letterSpacing: 2, opacity: 0.62}}>{props.episode.episode_code} · {unit.sequence_id} · {unit.mode.toUpperCase()}</div>
        <div style={{fontSize: 29, fontWeight: 900, lineHeight: 1.1, marginTop: 5}}>{focusLabel}</div>
      </div>

      <div style={{position: 'absolute', right: 28, top: 24, width: 414, display: 'flex', flexDirection: 'column', gap: 10}}>
        <OverviewMap objects={props.objects} edges={props.edges} rig={rig} focused={focused} contextual={contextual} colors={props.palette} />
        <div style={{border: '1px solid rgba(245,240,230,0.3)', background: 'rgba(26,26,26,0.94)', padding: '13px 16px', fontFamily: 'Arial, Helvetica, sans-serif'}}>
          <div style={{fontSize: 12, letterSpacing: 2, opacity: 0.6}}>CAMERA · {camera?.id ?? unit.camera_anchor}</div>
          <div style={{fontSize: 18, fontWeight: 800, marginTop: 4}}>{camera?.label ?? 'Unknown camera'}</div>
        </div>
        {visibleTickets.map((ticket) => ticket && <TicketSlate key={ticket.id} ticket={ticket} colors={props.palette} />)}
        {unit.evidence_ids.map((id) => {
          const evidence = evidenceById.get(id);
          if (!evidence) return null;
          return (
            <div key={id} style={{borderLeft: `5px solid ${props.palette.ledger_gold}`, background: props.palette.paper, color: props.palette.ink, padding: '12px 14px', fontFamily: 'Arial, Helvetica, sans-serif'}}>
              <div style={{fontSize: 13, fontWeight: 800, letterSpacing: 1.5}}>EVIDENCE PIN · {id}</div>
              <div style={{fontSize: 17, lineHeight: 1.25, marginTop: 5}}>{evidence.label}</div>
              <div style={{fontSize: 12, marginTop: 7, opacity: 0.7}}>Source context retained · no synthetic proof</div>
            </div>
          );
        })}
      </div>

      <div style={{position: 'absolute', left: 28, right: 28, bottom: 24, borderTop: `3px solid ${props.palette.ledger_gold}`, background: 'rgba(20,38,62,0.97)', padding: '13px 18px 12px', fontFamily: 'Arial, Helvetica, sans-serif', display: 'grid', gridTemplateColumns: '210px 1fr 300px', gap: 20, alignItems: 'center'}}>
        <div>
          <div style={{fontSize: 14, letterSpacing: 1.8, opacity: 0.65}}>{unit.id} · {unit.mode}</div>
          <div style={{fontSize: 22, fontWeight: 900, marginTop: 3}}>{unit.motion_verb}</div>
        </div>
        <div style={{fontSize: 23, lineHeight: 1.18, fontWeight: 700}}>{unit.action}</div>
        <div style={{textAlign: 'right'}}>
          <div style={{fontSize: 14, letterSpacing: 1.5, opacity: 0.65}}>{unit.narrative_state}</div>
          <div style={{fontSize: 18, marginTop: 5}}>{unit.in.toFixed(3)}–{unit.out.toFixed(3)}s</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
