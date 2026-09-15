export type WorldState = {
  object_id: string;
  state: string;
};

export type WorldObject = {
  id: string;
  kind:
    | 'zone'
    | 'actor'
    | 'token'
    | 'gate'
    | 'node'
    | 'destination'
    | 'ledger'
    | 'outcome'
    | 'money_flow'
    | 'state_marker';
  label: string;
  description: string;
  zone_id: string;
  position: {x: number; y: number};
  states: Array<{id: string; label: string}>;
  initial_state: string;
};

export type WorldEdge = {
  id: string;
  from: string;
  to: string;
  kind: string;
  label: string;
  states: Array<{id: string; label: string}>;
  initial_state: string;
};

export type Evidence = {
  id: string;
  label: string;
  target_ids: string[];
  claim_ids: string[];
  parameter_ids: string[];
  source_path: string;
  status: string;
};

export type Camera = {
  id: string;
  label: string;
  zone_id: string;
  position: {x: number; y: number};
  target_contract: 'representative_zone_anchors';
  target_ids: string[];
};

export type AssetTicket = {
  id: string;
  story_role: string;
  narration_anchor: string;
  required_semantic_content: string;
  preferred_source_route: string;
  placeholder_behavior: string;
  status: string;
};

export type VisualUnit = {
  id: string;
  in: number;
  out: number;
  sequence_id: string;
  narration_anchor: {word_start: number; word_end: number; quote: string};
  narrative_state: string;
  mode: 'reality' | 'system' | 'proof' | 'reset';
  action: string;
  motion_verb: string;
  carry: string[];
  focus: string[];
  world_state_before: WorldState[];
  world_state_after: WorldState[];
  camera_anchor: string;
  evidence_ids: string[];
  asset_ticket_ids: string[];
  audio_state: {narration: true; music: false; sound_design: false};
  status: 'greybox';
};

export type RenderData = {
  schema_version: '1.0.0';
  workflow_version: 'blueprint-cinema-1.0';
  episode: {
    episode_number: number;
    episode_code: string;
    slug: string;
    folder_name: string;
  };
  duration_seconds: number;
  fps: 30;
  width: 1920;
  height: 1080;
  audio_file: string;
  source_hashes: Record<string, string>;
  palette: Record<string, string>;
  objects: WorldObject[];
  edges: WorldEdge[];
  evidence: Evidence[];
  cameras: Camera[];
  tickets: AssetTicket[];
  units: VisualUnit[];
};
