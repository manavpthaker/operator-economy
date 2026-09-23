'use client';

import { useId, useState, type FormEvent } from 'react';
import Link from 'next/link';
import { submitCapture } from '../lib/capture';

type Status =
  | { state: 'idle'; message: '' }
  | { state: 'submitting'; message: '' }
  | { state: 'success' | 'error'; message: string };

/** Email-gated Operator Canvas PDF. Posts tag `blueprint:<slug>`; /api/subscribe emails the PDF link. */
export function BlueprintRequestForm({ slug }: { slug: string }) {
  const inputId = useId();
  const statusId = useId();
  const [status, setStatus] = useState<Status>({ state: 'idle', message: '' });

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const email = String(data.get('email') ?? '').trim();
    if (!email) return;

    setStatus({ state: 'submitting', message: '' });
    const result = await submitCapture({
      email,
      tag: `blueprint:${slug}`,
      slug,
      hp: String(data.get('_bee') ?? ''),
    });
    setStatus({
      state: result.ok ? 'success' : 'error',
      message: result.ok ? 'Sent. The PDF link is on its way to your inbox.' : result.message,
    });
    if (result.ok) form.reset();
  }

  return (
    <form className="oe-form oe-blueprint-form" aria-label="Request the Operator Canvas PDF" onSubmit={onSubmit} noValidate>
      <label htmlFor={inputId}>Email</label>
      <input
        id={inputId}
        name="email"
        type="email"
        autoComplete="email"
        placeholder="you@example.com"
        aria-describedby={status.message ? statusId : undefined}
        required
      />
      <input className="oe-honeypot" name="_bee" type="text" tabIndex={-1} aria-hidden="true" autoComplete="off" />
      <button type="submit" disabled={status.state === 'submitting'}>
        {status.state === 'submitting' ? 'Sending…' : 'Email me the PDF'}
      </button>
      <small>
        One email with the download link. It does not subscribe you to the newsletter. Read the{' '}
        <Link href="/privacy">privacy notice</Link>.
      </small>
      {status.message && (
        <p
          className="oe-newsletter-status"
          id={statusId}
          role={status.state === 'error' ? 'alert' : 'status'}
          data-state={status.state}
        >
          {status.message}
        </p>
      )}
    </form>
  );
}
