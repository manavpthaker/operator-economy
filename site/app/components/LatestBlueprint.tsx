import episodesData from '../../data/episodes.json';
import s from './LatestBlueprint.module.css';

type EpisodeStatus = 'live' | 'in_research' | 'queued';

export type Episode = {
  number: number;
  slug: string;
  title: string;
  category: string;
  status: EpisodeStatus;
  rev?: string;
  date?: string;
  sources_verified?: number;
  stack_cost?: string;
  honest_math?: string;
  honest_math_estimate?: boolean;
  playbook_span?: string;
  read_minutes?: number;
  pdf_href?: string;
  episode_href?: string;
};

export type EpisodesData = {
  updated: string;
  queue_depth: number;
  episodes: Episode[];
};

const data = episodesData as EpisodesData;

export function getLatestLive(): Episode | undefined {
  const live = data.episodes.filter((e) => e.status === 'live');
  if (live.length === 0) return undefined;
  return live.reduce((a, b) => (a.number > b.number ? a : b));
}

export function getNextInResearch(): Episode | undefined {
  return data.episodes
    .filter((e) => e.status === 'in_research')
    .sort((a, b) => a.number - b.number)[0];
}

export function getLiveCount(): number {
  return data.episodes.filter((e) => e.status === 'live').length;
}

export function getQueueDepth(): number {
  return data.queue_depth;
}

function pad(n: number): string {
  return n.toString().padStart(3, '0');
}

const MAX_GHOSTS = 4;
const MIN_GHOSTS = 1; // Show one ghost even at N=1 so the "stack" metaphor reads.

export function LatestBlueprint() {
  const latest = getLatestLive();
  const next = getNextInResearch();
  const liveCount = getLiveCount();
  const queueDepth = getQueueDepth();

  if (!latest) {
    return (
      <aside
        className={`${s.panel} schematic-grid`}
        aria-label="No blueprint published yet"
      >
        <div className={s.header}>
          <span className={s.headerLabel}>The latest blueprint</span>
          <span className={s.headerCadence}>ships every Monday</span>
        </div>
        <div className={s.stackWrap}>
          <div className={s.doc}>
            <div className={s.docTitle}>№001 publishes Monday.</div>
          </div>
        </div>
      </aside>
    );
  }

  const ghostCount = Math.min(MAX_GHOSTS, Math.max(MIN_GHOSTS, liveCount - 1));
  const num = pad(latest.number);
  const estimateFlag = latest.honest_math_estimate ? ' · est.' : '';

  return (
    <aside className={`${s.panel} schematic-grid`}>
      <div className={s.header}>
        <span className={s.headerLabel}>The latest blueprint</span>
        <span className={s.headerCadence}>
          <i className={`${s.pulseDot} oe-pulse`} />
          ships every Monday
        </span>
      </div>

      <figure
        className={s.stackWrap}
        aria-label={`Operator Blueprint No. ${num}: ${latest.title}. ${
          latest.sources_verified
            ? `${latest.sources_verified} sources verified. `
            : ''
        }${latest.honest_math ? `Honest math: ${latest.honest_math}.` : ''}`}
      >
        {Array.from({ length: ghostCount }, (_, i) => {
          const step = ghostCount - i; // farthest ghost first
          const offset = step * 5; // 5px per layer
          return (
            <div
              key={i}
              className={s.ghost}
              style={{
                transform: `translate(${offset}px, ${offset}px)`,
                zIndex: 0,
              }}
              aria-hidden
            />
          );
        })}

        <article className={s.doc} style={{ position: 'relative', zIndex: 1 }}>
          <div className={s.docHead}>
            <span className={s.docNumber}>Operator Blueprint №{num}</span>
            <span className={s.docRev}>
              {latest.rev ? `Rev ${latest.rev}` : ''}
              <b>· LIVE</b>
            </span>
          </div>

          <h3 className={s.docTitle}>{latest.title}</h3>

          <div className={s.specTable}>
            {latest.sources_verified !== undefined && (
              <div className={s.specRow}>
                <span className={s.specLabel}>Sources</span>
                <span className={s.specValue}>
                  →&nbsp;&nbsp;{latest.sources_verified} verified
                </span>
              </div>
            )}
            {latest.stack_cost && (
              <div className={s.specRow}>
                <span className={s.specLabel}>Stack</span>
                <span className={s.specValue}>
                  →&nbsp;&nbsp;{latest.stack_cost}
                </span>
              </div>
            )}
            {latest.honest_math && (
              <div className={s.specRow}>
                <span className={s.specLabel}>Honest math</span>
                <span className={s.specValue}>
                  →&nbsp;&nbsp;{latest.honest_math}
                  {estimateFlag && <em>{estimateFlag}</em>}
                </span>
              </div>
            )}
            {latest.playbook_span && (
              <div className={s.specRow}>
                <span className={s.specLabel}>Playbook</span>
                <span className={s.specValue}>
                  →&nbsp;&nbsp;{latest.playbook_span}
                </span>
              </div>
            )}
          </div>

          <div className={s.docFoot}>
            <span className={s.docFootLabel}>PDF · every citation</span>
            <a
              href={latest.pdf_href ?? '#capture'}
              className={s.getBtn}
              aria-label={`Get Operator Blueprint No. ${num}: ${latest.title}`}
            >
              Get №{num} →
            </a>
          </div>
        </article>
      </figure>

      <div className={s.ticker}>
        <span className={s.tickerNext}>
          {next ? (
            <>
              №{pad(next.number)} <b>{next.title}</b> · in research
            </>
          ) : (
            <>Queue empty — new theses added weekly</>
          )}
        </span>
        <span className={s.tickerCount}>{queueDepth} queued</span>
      </div>
    </aside>
  );
}
