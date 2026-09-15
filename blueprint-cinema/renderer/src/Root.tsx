import {Composition, getInputProps} from 'remotion';
import {BlueprintCinema} from './BlueprintCinema';
import {DeckPrototype, DECK_PROTOTYPE_SECONDS} from './DeckPrototype';
import type {RenderData} from './types';

const fallbackProps: RenderData = {
  schema_version: '1.0.0',
  workflow_version: 'blueprint-cinema-1.0',
  episode: {episode_number: 0, episode_code: 'EP000', slug: 'no-props', folder_name: 'EP000-no-props'},
  duration_seconds: 1,
  fps: 30,
  width: 1920,
  height: 1080,
  audio_file: 'generated/missing/full-episode.mp3',
  source_hashes: {},
  palette: {ink: '#1A1A1A', paper: '#F5F0E6', schematic_navy: '#14263E', drafting_blue: '#1F3A5F', ledger_gold: '#C4A45F', sage: '#7B9E87', negative: '#9B3E2E'},
  objects: [],
  edges: [],
  evidence: [],
  cameras: [],
  tickets: [],
  units: [],
};

export const RemotionRoot: React.FC = () => {
  const input = getInputProps() as Partial<RenderData>;
  const props = input.units?.length ? (input as RenderData) : fallbackProps;
  return (
    <>
      <Composition
        id="BlueprintCinema"
        component={BlueprintCinema}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={Math.ceil(props.duration_seconds * 30)}
        defaultProps={props}
        calculateMetadata={({props: metadataProps}) => ({
          durationInFrames: Math.ceil(metadataProps.duration_seconds * metadataProps.fps),
          fps: metadataProps.fps,
          width: metadataProps.width,
          height: metadataProps.height,
        })}
      />
      <Composition
        id="BlueprintCinemaDeckPrototype"
        component={DeckPrototype}
        width={1920}
        height={1080}
        fps={30}
        durationInFrames={DECK_PROTOTYPE_SECONDS * 30}
        defaultProps={props}
        calculateMetadata={({props: metadataProps}) => ({
          durationInFrames: DECK_PROTOTYPE_SECONDS * metadataProps.fps,
          fps: metadataProps.fps,
          width: metadataProps.width,
          height: metadataProps.height,
        })}
      />
    </>
  );
};
