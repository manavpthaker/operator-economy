import type {Camera, RenderData, VisualUnit, WorldObject} from './types';

export type CameraRig = {
  scale: number;
  translateX: number;
  translateY: number;
  targetX: number;
  targetY: number;
  view: 'overview' | 'zone' | 'focus';
};

export const MAIN_VIEWPORT = {
  left: 0,
  top: 0,
  width: 1450,
  height: 835,
  focusX: 720,
  focusY: 430,
};

const WORLD_WIDTH = 1920;
const WORLD_HEIGHT = 960;
const OVERVIEW_SCALE = 0.78;

const clamp = (value: number, minimum: number, maximum: number): number =>
  Math.min(maximum, Math.max(minimum, value));

const lerp = (start: number, end: number, progress: number): number =>
  start + (end - start) * progress;

const smoothstep = (progress: number): number => {
  const value = clamp(progress, 0, 1);
  return value * value * (3 - 2 * value);
};

const rigForTarget = (
  targetX: number,
  targetY: number,
  scale: number,
  view: CameraRig['view'],
): CameraRig => ({
  scale,
  translateX: MAIN_VIEWPORT.focusX - targetX * scale,
  translateY: MAIN_VIEWPORT.focusY - targetY * scale,
  targetX,
  targetY,
  view,
});

export const overviewRig = (): CameraRig => ({
  scale: OVERVIEW_SCALE,
  translateX: (WORLD_WIDTH - WORLD_WIDTH * OVERVIEW_SCALE) / 2,
  translateY: 38,
  targetX: WORLD_WIDTH / 2,
  targetY: WORLD_HEIGHT / 2,
  view: 'overview',
});

const objectsForCamera = (
  props: RenderData,
  camera: Camera | undefined,
  zone: WorldObject | undefined,
): WorldObject[] => {
  const byId = new Map(props.objects.map((object) => [object.id, object]));
  const explicitTargets = camera?.target_ids
    .map((id) => byId.get(id))
    .filter((object): object is WorldObject => Boolean(object) && object?.kind !== 'zone');
  if (explicitTargets?.length) {
    return explicitTargets;
  }
  return props.objects.filter(
    (object) => object.kind !== 'zone' && object.zone_id === zone?.id,
  );
};

const rigForZone = (
  props: RenderData,
  unit: VisualUnit,
  zone: WorldObject | undefined,
): CameraRig => {
  const camera = props.cameras.find((candidate) => candidate.id === unit.camera_anchor);
  const targets = objectsForCamera(props, camera, zone);
  if (!targets.length) {
    const position = camera?.position ?? zone?.position ?? {x: 960, y: 480};
    return rigForTarget(position.x, position.y, 1.02, 'zone');
  }

  const xs = targets.map((object) => object.position.x);
  const ys = targets.map((object) => object.position.y);
  const minX = Math.min(...xs) - 180;
  const maxX = Math.max(...xs) + 180;
  const minY = Math.min(...ys) - 135;
  const maxY = Math.max(...ys) + 135;
  const scale = clamp(
    Math.min(MAIN_VIEWPORT.width / (maxX - minX), MAIN_VIEWPORT.height / (maxY - minY)),
    0.88,
    1.28,
  );
  return rigForTarget((minX + maxX) / 2, (minY + maxY) / 2, scale, 'zone');
};

export const cameraRigForUnit = (props: RenderData, unit: VisualUnit): CameraRig => {
  if (unit.mode === 'reset') {
    return overviewRig();
  }
  const byId = new Map(props.objects.map((object) => [object.id, object]));
  const focusObjects = unit.focus
    .map((id) => byId.get(id))
    .filter((object): object is WorldObject => Boolean(object));
  const zone = focusObjects.find((object) => object.kind === 'zone');
  if (zone) {
    return rigForZone(props, unit, zone);
  }
  if (!focusObjects.length) {
    const camera = props.cameras.find((candidate) => candidate.id === unit.camera_anchor);
    const position = camera?.position ?? {x: 960, y: 480};
    return rigForTarget(position.x, position.y, 1.12, 'zone');
  }

  const targetX = focusObjects.reduce((sum, object) => sum + object.position.x, 0) / focusObjects.length;
  const targetY = focusObjects.reduce((sum, object) => sum + object.position.y, 0) / focusObjects.length;
  const scale = focusObjects.some((object) => object.kind === 'ledger' || object.kind === 'outcome')
    ? 1.88
    : 1.72;
  return rigForTarget(targetX, targetY, scale, 'focus');
};

export const cameraRigAt = (
  props: RenderData,
  unitIndex: number,
  seconds: number,
): CameraRig => {
  const unit = props.units[unitIndex];
  const destination = cameraRigForUnit(props, unit);
  const origin = unitIndex === 0 ? overviewRig() : cameraRigForUnit(props, props.units[unitIndex - 1]);
  const duration = Math.max(0.001, unit.out - unit.in);
  const hold = unitIndex === 0 ? Math.min(0.65, duration * 0.12) : 0;
  const travel = Math.min(1.15, Math.max(0.45, duration * 0.22));
  const progress = smoothstep((seconds - unit.in - hold) / travel);
  return {
    scale: lerp(origin.scale, destination.scale, progress),
    translateX: lerp(origin.translateX, destination.translateX, progress),
    translateY: lerp(origin.translateY, destination.translateY, progress),
    targetX: lerp(origin.targetX, destination.targetX, progress),
    targetY: lerp(origin.targetY, destination.targetY, progress),
    view: progress < 0.5 ? origin.view : destination.view,
  };
};

export const worldViewportForRig = (rig: CameraRig) => ({
  x: (MAIN_VIEWPORT.left - rig.translateX) / rig.scale,
  y: (MAIN_VIEWPORT.top - rig.translateY) / rig.scale,
  width: MAIN_VIEWPORT.width / rig.scale,
  height: MAIN_VIEWPORT.height / rig.scale,
});
