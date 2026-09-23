import Link from 'next/link';
import { type Operation } from '../lib/operations';

export function BusinessList({ operations }: { operations: Operation[] }) {
  return (
    <>
      <p className="bl-chapter__number oe-library-count">
        {operations.length} {operations.length === 1 ? 'business' : 'businesses'}
      </p>
      <div className="oe-library" aria-label="Published businesses, newest first">
        {operations.map((operation) => (
          <Link className="bl-library-row" href={`/businesses/${operation.slug}`} key={operation.slug}>
            <span className="bl-library-row__number">{operation.published}</span>
            <span>
              <strong>{operation.name}</strong>
              <small>
                {operation.summary}
                <span className="oe-record">Episode + Operator Canvas + PDF</span>
              </small>
            </span>
            <span aria-hidden="true">Open</span>
          </Link>
        ))}
      </div>
    </>
  );
}
