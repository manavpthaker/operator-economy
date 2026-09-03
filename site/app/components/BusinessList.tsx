'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import { type Operation, padOperationNumber } from '../lib/operations';

type Filter = 'all' | 'canvas' | 'legacy_blueprint';

export function BusinessList({ operations }: { operations: Operation[] }) {
  const [filter, setFilter] = useState<Filter>('all');
  const visible = useMemo(
    () => filter === 'all' ? operations : operations.filter((operation) => operation.artifact === filter),
    [filter, operations]
  );

  return (
    <>
      <div className="oe-filters" role="group" aria-label="Filter businesses">
        <button type="button" aria-pressed={filter === 'all'} onClick={() => setFilter('all')}>All</button>
        <button type="button" aria-pressed={filter === 'canvas'} onClick={() => setFilter('canvas')}>Canvases</button>
        <button type="button" aria-pressed={filter === 'legacy_blueprint'} onClick={() => setFilter('legacy_blueprint')}>Legacy</button>
      </div>

      <p className="bl-chapter__number oe-library-count" aria-live="polite">
        {visible.length} {visible.length === 1 ? 'business' : 'businesses'}
      </p>

      {visible.length ? (
        <div className="oe-library" aria-label="Published businesses, newest first">
          {visible.map((operation) => (
            <Link className="bl-library-row" href={`/businesses/${operation.slug}`} key={operation.slug}>
              <span className="bl-library-row__number">№{padOperationNumber(operation.number)}</span>
              <span>
                <strong>{operation.name}</strong>
                <small>
                  {operation.summary}
                  <span className="oe-record">
                    Episode + Legacy Blueprint · {operation.sources} sources · {operation.published}
                  </span>
                </small>
              </span>
              <span aria-hidden="true">Open</span>
            </Link>
          ))}
        </div>
      ) : (
        <aside className="bl-disclosure oe-empty-state">
          <strong>No Canvas is live yet.</strong>
          <span>The library will add its first Canvas only after a V2 model passes its editorial lock and publication gate.</span>
        </aside>
      )}
    </>
  );
}
