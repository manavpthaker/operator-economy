import Link from 'next/link';
import { Fragment } from 'react';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import {
  getEpisodes,
  getEpisodeBySlug,
  getChannelUrl,
  pad,
  type Episode,
  type PipelineStage,
} from '../../components/LatestBlueprint';
import { NotifyForm, BlueprintCaptureForm } from './EpisodeForms';
import { YouTubeEmbed } from './YouTubeEmbed';
import s from './page.module.css';

export function generateStaticParams() {
  // All non-queued entries get pre-rendered pages.
  return getEpisodes()
    .filter((e) => e.status !== 'queued')
    .map((e) => ({ slug: e.slug }));
}

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const ep = getEpisodeBySlug(slug);
  if (!ep) return { title: 'Not found · The Operator Economy' };
  const num = pad(ep.number);
  const title =
    ep.status === 'live'
      ? `№${num} — ${ep.title} · The Operator Economy`
      : `№${num} — ${ep.title} (upcoming) · The Operator Economy`;
  return {
    title,
    description: ep.thesis?.slice(0, 200) ?? undefined,
  };
}

const STAGES: PipelineStage[] = ['research', 'scripting', 'production'];
const STAGE_STEP: Record<PipelineStage, number> = { research: 0, scripting: 1, production: 2 };

function Masthead({ watchHref }: { watchHref: string }) {
  return (
    <header className={s.masthead}>
      <Link href="/" className={s.brandLink}>
        <span className={s.brandKicker}>The</span>
        <span className={s.brandName}>Operator Economy</span>
      </Link>
      <nav className={s.mastheadNav} aria-label="Episode navigation">
        <a
          href={watchHref}
          target="_blank"
          rel="noreferrer"
          className={s.watchLink}
        >
          Watch on YouTube ↗
        </a>
        <Link href="/#library" className={s.backLink}>
          ← Back to the library
        </Link>
      </nav>
    </header>
  );
}

function PipelinePosition({ current }: { current: PipelineStage }) {
  const currentStep = STAGE_STEP[current];
  const nodes = [
    { key: 'research', label: '01', name: 'Research' },
    { key: 'scripting', label: '02', name: 'Script + Gate 1' },
    { key: 'production', label: '03', name: 'Production' },
    { key: 'live', label: '04', name: 'Live' },
  ];

  return (
    <div className={s.pipeline}>
      <div className={s.pipelineHead}>
        <span className={s.pipelineLabel}>Pipeline position</span>
        <span className={s.pipelineLabel}>no dates · honest status</span>
      </div>
      <div className={s.pipelineNodes}>
        {nodes.map((n, i) => {
          const stateClass =
            i < currentStep
              ? s.done
              : i === currentStep
                ? `${s.active} oe-pulse`
                : '';
          return (
            <Fragment key={n.key}>
              <div className={`${s.pipeNode} ${stateClass}`}>
                <div className={s.pipeNodeLabel}>{n.label}</div>
                <div className={s.pipeNodeName}>{n.name}</div>
              </div>
              {i < nodes.length - 1 && <span className={s.pipeWire} />}
            </Fragment>
          );
        })}
      </div>
    </div>
  );
}

function UpcomingView({ ep }: { ep: Episode }) {
  const num = pad(ep.number);
  const stage = ep.stage ?? 'research';

  return (
    <>
      <div className={s.titleBlock}>
        <div className={s.titleRow}>
          <span className={s.epLabel}>№{num} · {ep.model ?? ep.category} · Upcoming</span>
          <span className={s.stageInline}>● {stage}</span>
        </div>
        <h1 className={s.title}>{ep.title}</h1>
        <div className={s.metaRow}>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Expected</div>
            <div className={s.metaValue}>{ep.expected ?? '—'}</div>
          </div>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Stage</div>
            <div className={s.metaValue}>{stage}</div>
          </div>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Model</div>
            <div className={s.metaValue}>{ep.model ?? ep.category}</div>
          </div>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Figures</div>
            <div className={s.metaValue}>publish w/ episode</div>
          </div>
        </div>
      </div>

      <section className={s.section}>
        <div className={s.sectionKicker}>The thesis</div>
        <p className={s.thesis}>{ep.thesis}</p>
      </section>

      <section className={s.section}>
        <div className={s.sectionKicker}>What ships with it</div>
        <ul className={s.shipsList}>
          <li>
            <span className={s.shipsLabel}>Episode</span>
            <span className={s.shipsDesc}>
              A 20-30 min breakdown on YouTube — thesis, evidence, exact stack, honest math.
            </span>
          </li>
          <li>
            <span className={s.shipsLabel}>Operator Blueprint</span>
            <span className={s.shipsDesc}>
              The working doc behind the video — sourced figures, tool costs, week-by-week
              playbook. PDF, free.
            </span>
          </li>
          <li>
            <span className={s.shipsLabel}>Monday note</span>
            <span className={s.shipsDesc}>
              One newsletter the day it publishes — the full receipts, in your inbox.
            </span>
          </li>
        </ul>
      </section>

      <section className={s.section}>
        <div className={s.sectionKicker}>Where it is now</div>
        <PipelinePosition current={stage} />
      </section>

      <section className={s.section}>
        <div className={s.sectionKicker}>Notify me</div>
        <NotifyForm slug={ep.slug} number={num} title={ep.title} />
      </section>
    </>
  );
}

function LiveView({ ep }: { ep: Episode }) {
  const num = pad(ep.number);

  return (
    <>
      <div className={s.titleBlock}>
        <div className={s.titleRow}>
          <span className={s.epLabel}>
            Operator Blueprint №{num} · {ep.model ?? ep.category}
          </span>
          <span className={s.stageInline} style={{ color: 'var(--gold-700)' }}>
            {ep.rev ? `Rev ${ep.rev}` : ''} · LIVE
          </span>
        </div>
        <h1 className={s.title}>{ep.title}</h1>
        <div className={s.metaRow}>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Date</div>
            <div className={s.metaValue}>{ep.date ?? '—'}</div>
          </div>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Sources</div>
            <div className={s.metaValue}>{ep.sources_verified ?? '—'}</div>
          </div>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Read</div>
            <div className={s.metaValue}>{ep.read_minutes ? `${ep.read_minutes} min` : '—'}</div>
          </div>
          <div className={s.metaCell}>
            <div className={s.metaLabel}>Model</div>
            <div className={s.metaValue}>{ep.model ?? ep.category}</div>
          </div>
        </div>
      </div>

      {ep.youtube_url && (
        <section className={s.section}>
          <div className={s.sectionKicker}>Watch</div>
          <YouTubeEmbed url={ep.youtube_url} title={ep.title} />
        </section>
      )}

      {ep.thesis && (
        <section className={s.section}>
          <div className={s.sectionKicker}>The thesis</div>
          <p className={s.thesis}>{ep.thesis}</p>
        </section>
      )}

      {(ep.honest_math || ep.stack_cost || ep.playbook_span) && (
        <section className={s.section}>
          <div className={s.sectionKicker}>The honest math</div>
          <div className={s.honestMathRow}>
            {ep.stack_cost && (
              <div className={s.honestMathCell}>
                <div className={s.honestMathLabel}>Stack</div>
                <div className={s.honestMathValue}>{ep.stack_cost}</div>
              </div>
            )}
            {ep.honest_math && (
              <div className={s.honestMathCell}>
                <div className={s.honestMathLabel}>
                  Realistic yr 1{ep.honest_math_estimate ? ' · estimate' : ''}
                </div>
                <div className={s.honestMathValue}>{ep.honest_math}</div>
              </div>
            )}
            {ep.playbook_span && (
              <div className={s.honestMathCell}>
                <div className={s.honestMathLabel}>Playbook</div>
                <div className={s.honestMathValue}>{ep.playbook_span}</div>
              </div>
            )}
          </div>
        </section>
      )}

      {ep.sources && ep.sources.length > 0 && (
        <section className={s.section}>
          <div className={s.sectionKicker}>Sources</div>
          <ul className={s.sourcesList}>
            {ep.sources.map((src, i) => (
              <li key={i}>
                {src.url ? (
                  <a href={src.url} target="_blank" rel="noreferrer">
                    {src.label} ↗
                  </a>
                ) : (
                  src.label
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className={s.section}>
        <div className={s.sectionKicker}>Get the Operator Blueprint</div>
        <BlueprintCaptureForm slug={ep.slug} number={num} title={ep.title} />
      </section>
    </>
  );
}

export default async function EpisodePage({ params }: Props) {
  const { slug } = await params;
  const ep = getEpisodeBySlug(slug);
  if (!ep || ep.status === 'queued') notFound();

  // Live episodes link to their own video where available; upcoming episodes
  // link to the channel so viewers can see the format (and the prior receipts).
  const watchHref = ep.youtube_url ?? getChannelUrl();

  return (
    <main className={s.page}>
      <div className={s.wrap}>
        <Masthead watchHref={watchHref} />
        {ep.status === 'live' ? <LiveView ep={ep} /> : <UpcomingView ep={ep} />}
      </div>
    </main>
  );
}
