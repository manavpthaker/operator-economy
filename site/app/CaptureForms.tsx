'use client';

import { useState, type FormEvent } from 'react';
import { submitCapture, type CaptureTag } from './lib/capture';
import s from './page.module.css';

type FormStatus =
  | { state: 'idle' }
  | { state: 'submitting' }
  | { state: 'success'; message: string }
  | { state: 'error'; message: string };

function useCapture(tag: CaptureTag, slug?: string) {
  const [status, setStatus] = useState<FormStatus>({ state: 'idle' });

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    const email = String(data.get('email') ?? '').trim();
    const hp = String(data.get('_bee') ?? '');
    if (!email) return;
    setStatus({ state: 'submitting' });
    const res = await submitCapture({ email, tag, slug, hp });
    setStatus(
      res.ok
        ? { state: 'success', message: res.message }
        : { state: 'error', message: res.message }
    );
    if (res.ok) form.reset();
  }

  return { status, onSubmit };
}

type BlueprintProps = {
  slug: string;
  number: string;
  title?: string;
  rev?: string;
  date?: string;
  sourcesVerified?: number;
  readMinutes?: number;
};

export function BlueprintForm({
  slug,
  number,
  title = 'AI implementation as a service',
  rev = 'A',
  date = '2026-07',
  sourcesVerified = 8,
  readMinutes = 9,
}: BlueprintProps) {
  const tag: CaptureTag = `blueprint:${slug}`;
  const { status, onSubmit } = useCapture(tag, slug);

  return (
    <form className={s.captureCard} onSubmit={onSubmit} noValidate>
      <div className={s.captureHead}>
        <span className={s.cardEpisode}>Operator Blueprint №{number}</span>
        <span className={s.tag}>Rev {rev}</span>
      </div>
      <div className={s.captureName}>{title}</div>
      <div className={s.captureMeta}>
        <div className={s.metaCell}>
          <div className={s.metaLabel}>Date</div>
          <div className={s.metaValue}>{date}</div>
        </div>
        <div className={s.metaCell}>
          <div className={s.metaLabel}>Sources</div>
          <div className={s.metaValue}>{sourcesVerified}</div>
        </div>
        <div className={s.metaCell}>
          <div className={s.metaLabel}>Read</div>
          <div className={s.metaValue}>{readMinutes} min</div>
        </div>
      </div>
      <label htmlFor="bp-email" className={s.inputLabel}>Work email</label>
      <input
        id="bp-email"
        type="email"
        name="email"
        placeholder="you@company.com"
        className={`${s.input} oe-input`}
        required
        autoComplete="email"
      />
      <input
        type="text"
        name="_bee"
        style={{
          position: 'absolute',
          left: -9999,
          width: 1,
          height: 1,
          opacity: 0,
        }}
        tabIndex={-1}
        aria-hidden
        autoComplete="off"
      />
      <button
        type="submit"
        className={s.submit}
        disabled={status.state === 'submitting'}
      >
        {status.state === 'submitting' ? '…' : `Get Blueprint №${number}`}
      </button>
      {status.state === 'success' && (
        <div
          role="status"
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 11.5,
            color: 'var(--sage-700)',
            marginTop: 10,
            textAlign: 'center',
          }}
        >
          {status.message}
        </div>
      )}
      {status.state === 'error' && (
        <div
          role="alert"
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 11.5,
            color: 'var(--negative)',
            marginTop: 10,
            textAlign: 'center',
          }}
        >
          {status.message}
        </div>
      )}
      <div className={s.captureFineprint}>
        PDF + every citation · straight to your inbox
      </div>
    </form>
  );
}

export function LedgerForm() {
  const { status, onSubmit } = useCapture('newsletter');

  return (
    <form className={s.ledgerForm} onSubmit={onSubmit} noValidate>
      <input
        type="email"
        name="email"
        placeholder="you@company.com"
        className={s.ledgerInput}
        required
        autoComplete="email"
        aria-label="Email address for the Monday note"
      />
      <input
        type="text"
        name="_bee"
        style={{
          position: 'absolute',
          left: -9999,
          width: 1,
          height: 1,
          opacity: 0,
        }}
        tabIndex={-1}
        aria-hidden
        autoComplete="off"
      />
      <button
        type="submit"
        className={s.ledgerSubmit}
        disabled={status.state === 'submitting'}
      >
        {status.state === 'submitting' ? '…' : 'Get the Blueprints'}
      </button>
      {status.state === 'success' && (
        <div
          role="status"
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 11,
            color: 'var(--paper-100)',
            marginLeft: 12,
            whiteSpace: 'nowrap',
            alignSelf: 'center',
          }}
        >
          {status.message}
        </div>
      )}
      {status.state === 'error' && (
        <div
          role="alert"
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 11,
            color: 'var(--negative)',
            marginLeft: 12,
            whiteSpace: 'nowrap',
            alignSelf: 'center',
          }}
        >
          {status.message}
        </div>
      )}
    </form>
  );
}
