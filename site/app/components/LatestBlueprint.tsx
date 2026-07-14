import Link from 'next/link';
import episodesData from '../../data/episodes.json';
import s from './LatestBlueprint.module.css';

export type EpisodeStatus = 'live' | 'upcoming' | 'queued';
export type PipelineStage = 'research' | 'scripting' | 'production';

export type EpisodeSource = { label: string; url: string | null };

export type Episode = {
  number: number;
  slug: string;
  title: string;
  category: string;
  model?: string; // revenue shape: Retainers | Projects | Products | Audience
  status: EpisodeStatus;
  stage?: PipelineStage;
  expected?: string;
  thesis?: string;
  rev?: string;
  date?: string;
  sources_verified?: number;
  stack_cost?: string;
  honest_math?: string;
  honest_math_estimate?: boolean;
  playbook_span?: string;
  read_minutes?: number;
  youtube_url?: string;
  pdf_href?: string;
  episode_href?: string;
  sources?: EpisodeSource[];
};

export type EpisodesData = {
  updated: string;
  queue_depth: number;
  channel_url: string;
  episodes: Episode[];
};

const data = episodesData as EpisodesData;

export function getEpisodes(): Episode[] {
  return data.episodes;
}

export function getEpisodeBySlug(slug: string): Episode | undefined {
  return data.episodes.find((e) => e.slug === slug);
}

export function getLatestLive(): Episode | undefined {
  const live = data.episodes.filter((e) => e.status === 'live');
  if (live.length === 0) return undefined;
  return live.reduce((a, b) => (a.number > b.number ? a : b));
}

export function getUpcoming(): Episode[] {
  return data.episodes
    .filter((e) => e.status === 'upcoming')
    .sort((a, b) => a.number - b.number);
}

export function getLiveCount(): number {
  return data.episodes.filter((e) => e.status === 'live').length;
}

export function getQueueDepth(): number {
  return data.queue_depth;
}

export function getChannelUrl(): string {
  return data.channel_url;
}

export function getUpdatedISO(): string {
  return data.updated;
}

export function pad(n: number): string {
  return n.toString().padStart(3, '0');
}

// Next Monday from `from`. If `from` is already a Monday, returns +7d — we ship
// on Mondays, so a same-day rebuild still forecasts the *next* one.
export function nextMonday(from: Date = new Date()): Date {
  const d = new Date(from);
  d.setHours(0, 0, 0, 0);
  const day = d.getDay(); // 0 Sun, 1 Mon, …
  const delta = day === 1 ? 7 : (8 - day) % 7 || 7;
  d.setDate(d.getDate() + delta);
  return d;
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export function formatNextMondayShort(d: Date = nextMonday()): string {
  return `${MONTHS[d.getMonth()]} ${d.getDate()}`;
}

const MAX_GHOSTS = 4;
const MIN_GHOSTS = 1;
const UPCOMING_ROWS = 3;

const STAGE_LABELS: Record<PipelineStage, string> = {
  research: '● research',
  scripting: '● scripting',
  production: '● production',
};

const STAGE_CLASSES: Record<PipelineStage, string> = {
  research: s.stageResearch,
  scripting: s.stageScripting,
  production: s.stageProduction,
};

export function LatestBlueprint() {
  const latest = getLatestLive();
  const upcoming = getUpcoming().slice(0, UPCOMING_ROWS);
  const liveCount = getLiveCount();
  const queueDepth = getQueueDepth();
  const nextShip = formatNextMondayShort();

  if (!latest) {
    return (
      <aside className={`${s.panel} schematic-grid`} aria-label="No blueprint published yet">
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
          ships every Monday · next {nextShip}
        </span>
      </div>

      <figure
        className={s.stackWrap}
        aria-label={`Operator Blueprint No. ${num}: ${latest.title}. ${
          latest.sources_verified ? `${latest.sources_verified} sources verified. ` : ''
        }${latest.honest_math ? `Honest math: ${latest.honest_math}.` : ''}`}
      >
        {Array.from({ length: ghostCount }, (_, i) => {
          const step = ghostCount - i;
          const offset = step * 5;
          return (
            <div
              key={i}
              className={s.ghost}
              style={{ transform: `translate(${offset}px, ${offset}px)`, zIndex: 0 }}
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
                <span className={s.specValue}>→&nbsp;&nbsp;{latest.stack_cost}</span>
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
                <span className={s.specValue}>→&nbsp;&nbsp;{latest.playbook_span}</span>
              </div>
            )}
          </div>

          <div className={s.docFoot}>
            <span className={s.docFootLabel}>PDF · every citation</span>
            <Link
              href={`/episodes/${latest.slug}`}
              className={s.getBtn}
              aria-label={`Get Operator Blueprint No. ${num}: ${latest.title}`}
            >
              Get №{num} →
            </Link>
          </div>
        </article>
      </figure>

      {upcoming.length > 0 && (
        <nav className={s.upcoming} aria-label="Upcoming episodes">
          <div className={s.upcomingHead}>Upcoming</div>
          <ul className={s.upcomingList}>
            {upcoming.map((ep) => {
              const stage = ep.stage ?? 'research';
              return (
                <li key={ep.slug}>
                  <Link href={`/episodes/${ep.slug}`} className={s.upcomingRow}>
                    <span className={s.upcomingLabel}>
                      <span className={s.upcomingNum}>№{pad(ep.number)}</span>{' '}
                      {ep.title}
                    </span>
                    <span className={`${s.stageChip} ${STAGE_CLASSES[stage]}`}>
                      {STAGE_LABELS[stage]}
                    </span>
                  </Link>
                </li>
              );
            })}
          </ul>
          <div className={s.queueDepth}>
            {queueDepth} more in the research queue
          </div>
        </nav>
      )}
    </aside>
  );
}
