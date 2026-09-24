import {worldViewportForRig, type CameraRig} from '../camera';
import type {WorldEdge, WorldObject} from '../types';

type Props = {
  objects: WorldObject[];
  edges: WorldEdge[];
  rig: CameraRig;
  focused: Set<string>;
  contextual: Set<string>;
  colors: Record<string, string>;
};

export const OverviewMap: React.FC<Props> = ({objects, edges, rig, focused, contextual, colors}) => {
  const objectById = new Map(objects.map((object) => [object.id, object]));
  const viewport = worldViewportForRig(rig);
  return (
    <div
      style={{
        width: 414,
        border: '1px solid rgba(245,240,230,0.34)',
        background: 'rgba(26,26,26,0.96)',
        padding: '12px 13px 13px',
        boxSizing: 'border-box',
        fontFamily: 'Arial, Helvetica, sans-serif',
      }}
      data-camera-view={rig.view}
    >
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
        <div style={{fontSize: 13, fontWeight: 900, letterSpacing: 2}}>WORLD OVERVIEW</div>
        <div style={{fontSize: 12, letterSpacing: 1.4, color: colors.ledger_gold}}>
          {rig.view.toUpperCase()} · {rig.scale.toFixed(2)}×
        </div>
      </div>
      <svg
        viewBox="0 0 1920 960"
        style={{display: 'block', width: '100%', height: 198, marginTop: 8, background: colors.schematic_navy}}
        aria-label="Persistent world overview and current camera window"
      >
        <rect x={0} y={0} width={600} height={960} fill="rgba(245,240,230,0.035)" />
        <rect x={600} y={0} width={850} height={960} fill="rgba(31,58,95,0.4)" />
        <rect x={1450} y={0} width={470} height={960} fill="rgba(196,164,95,0.1)" />
        {edges.map((edge) => {
          const from = objectById.get(edge.from);
          const to = objectById.get(edge.to);
          if (!from || !to) return null;
          const active = focused.has(edge.from) || focused.has(edge.to);
          return (
            <line
              key={edge.id}
              x1={from.position.x}
              y1={from.position.y}
              x2={to.position.x}
              y2={to.position.y}
              stroke={active ? colors.ledger_gold : 'rgba(245,240,230,0.24)'}
              strokeWidth={active ? 10 : 5}
            />
          );
        })}
        {objects.map((object) => {
          if (object.kind === 'zone') return null;
          const isFocused = focused.has(object.id);
          const isContextual = contextual.has(object.id);
          return (
            <rect
              key={object.id}
              x={object.position.x - 34}
              y={object.position.y - 18}
              width={68}
              height={36}
              rx={3}
              fill={isFocused ? colors.ledger_gold : isContextual ? colors.sage : colors.drafting_blue}
              stroke={isFocused ? colors.paper : 'rgba(245,240,230,0.45)'}
              strokeWidth={isFocused ? 7 : 3}
            />
          );
        })}
        <rect
          x={viewport.x}
          y={viewport.y}
          width={viewport.width}
          height={viewport.height}
          fill="none"
          stroke={colors.paper}
          strokeWidth={9 / rig.scale}
          strokeDasharray={`${28 / rig.scale} ${18 / rig.scale}`}
        />
      </svg>
      <div style={{fontSize: 12, marginTop: 8, opacity: 0.62}}>
        The dashed frame is what the main camera is showing.
      </div>
    </div>
  );
};
