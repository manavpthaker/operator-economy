'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import { pad, type Episode } from './LatestBlueprint';
import s from '../page.module.css';

type Props = {
  episodes: Episode[];
  channelUrl: string;
  queueDepth: number;
};

const FILTERS = ['All', 'Services', 'Software', 'Media'] as const;
type Filter = (typeof FILTERS)[number];

export function LibraryClient({ episodes, channelUrl, queueDepth }: Props) {
  const [filter, setFilter] = useState<Filter>('All');

  const counts = useMemo(() => {
    const map: Record<string, number> = { All: episodes.length };
    for (const cat of ['Services', 'Software', 'Media']) {
      map[cat] = episodes.filter((e) => e.category === cat).length;
    }
    return map;
  }, [episodes]);

  const shown = useMemo(
    () =>
      filter === 'All'
        ? episodes
        : episodes.filter((e) => e.category === filter),
    [episodes, filter]
  );

  const liveCount = episodes.filter((e) => e.status === 'live').length;

  return (
    <>
      <div className={s.filterRow}>
        <div className={s.filters}>
          {FILTERS.map((f) => {
            const n = counts[f] ?? 0;
            const isActive = filter === f;
            const isEmpty = n === 0;
            return (
              <button
                key={f}
                type="button"
                onClick={() => !isEmpty && setFilter(f)}
                className={isActive ? s.filterActive : s.filterInactive}
                disabled={isEmpty}
                style={
                  isEmpty
                    ? { opacity: 0.4, cursor: 'not-allowed' }
                    : { cursor: 'pointer' }
                }
                aria-pressed={isActive}
              >
                {f} · {n}
              </button>
            );
          })}
        </div>
        <span className={s.tag}>
          {liveCount === 1 ? '№001 live' : `${liveCount} live`} · {queueDepth}{' '}
          more in the research queue
        </span>
      </div>

      <div className={s.cards}>
        {shown.map((ep) => {
          const num = pad(ep.number);
          const isLive = ep.status === 'live';

          return (
            <article
              key={ep.slug}
              className={`${s.card} ${isLive ? s.cardLive : s.cardQueued}`}
            >
              <div className={s.cardHead}>
                <span
                  className={
                    isLive
                      ? s.cardEpisode
                      : `${s.cardEpisode} ${s.cardEpisodeMuted}`
                  }
                >
                  №{num} · {ep.category}
                </span>
                {isLive ? (
                  <span className={s.cardStatus}>
                    <i
                      className={`${s.dot} oe-pulse`}
                      style={{ width: 5, height: 5 }}
                    />
                    Live
                  </span>
                ) : (
                  <span className={s.cardStatusMuted}>
                    {ep.stage === 'production'
                      ? 'In production'
                      : ep.stage === 'scripting'
                        ? 'In scripting'
                        : 'In research'}
                  </span>
                )}
              </div>

              <h3
                className={
                  isLive ? s.cardTitle : `${s.cardTitle} ${s.cardTitleQueued}`
                }
              >
                {ep.title}
              </h3>

              <div className={s.cardTail}>
                {isLive ? (
                  <>
                    {ep.honest_math && (
                      <div className={s.cardFigure}>{ep.honest_math}</div>
                    )}
                    {ep.stack_cost && (
                      <div className={s.cardFigureMeta}>
                        Realistic year one · {ep.stack_cost} stack
                      </div>
                    )}
                    {ep.honest_math_estimate && (
                      <span className={s.estimateChip}>
                        <b>ESTIMATE</b> №{num} honest math
                      </span>
                    )}
                    <div className={s.cardLinks}>
                      <a
                        href={ep.youtube_url ?? channelUrl}
                        target="_blank"
                        rel="noreferrer"
                        className={s.cardLinkPrimary}
                      >
                        Watch the episode ↗
                      </a>
                      <Link
                        href={`/episodes/${ep.slug}`}
                        className={s.cardLinkSecondary}
                      >
                        Blueprint №{num}
                      </Link>
                    </div>
                  </>
                ) : (
                  <>
                    {ep.thesis && (
                      <p className={s.queuedNote}>
                        {ep.thesis.length > 160
                          ? ep.thesis.slice(0, 160).trim() + '…'
                          : ep.thesis}
                      </p>
                    )}
                    <div className={s.cardLinks}>
                      <Link
                        href={`/episodes/${ep.slug}`}
                        className={s.cardLinkPrimary}
                      >
                        Read the thesis + notify me →
                      </Link>
                    </div>
                  </>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </>
  );
}
