'use client';

import { useId, useState, type FormEvent } from 'react';
import Link from 'next/link';
import { submitCapture } from '../lib/capture';

type Status =
  | { state: 'idle'; message: '' }
  | { state: 'submitting'; message: '' }
  | { state: 'success' | 'error'; message: string };

export function NewsletterForm() {
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
      tag: 'newsletter',
      hp: String(data.get('_bee') ?? ''),
    });
    setStatus({
      state: result.ok ? 'success' : 'error',
      message: result.message,
    });
    if (result.ok) form.reset();
  }

  return (
    <form className="oe-form" aria-label="Newsletter signup" onSubmit={onSubmit} noValidate>
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
      <input
        className="oe-honeypot"
        name="_bee"
        type="text"
        tabIndex={-1}
        aria-hidden="true"
        autoComplete="off"
      />
      <button type="submit" disabled={status.state === 'submitting'}>
        {status.state === 'submitting' ? 'Subscribing…' : 'Subscribe'}
      </button>
      <small>
        Newsletter only. Read the <Link href="/privacy">privacy notice</Link>.
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

export function NewsletterBand() {
  return (
    <section className="bl-shell" id="newsletter" aria-labelledby="newsletter-title" style={{ paddingBottom: 'var(--bl-section-space)' }}>
      <aside className="bl-subscription-band">
        <div>
          <h3 id="newsletter-title">Get the next business when it ships.</h3>
          <p>One email with the episode and its working document. No drip campaign.</p>
        </div>
        <NewsletterForm />
      </aside>
    </section>
  );
}
