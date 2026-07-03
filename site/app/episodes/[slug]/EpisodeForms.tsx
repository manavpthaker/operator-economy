'use client';

import { useState, type FormEvent } from 'react';
import { submitCapture } from '../../lib/capture';
import s from './page.module.css';

type NotifyProps = { slug: string; number: string; title: string };

type FormStatus =
  | { state: 'idle' }
  | { state: 'submitting' }
  | { state: 'success'; message: string }
  | { state: 'error'; message: string };

export function NotifyForm({ slug, number, title }: NotifyProps) {
  const [status, setStatus] = useState<FormStatus>({ state: 'idle' });

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    const email = String(data.get('email') ?? '').trim();
    const hp = String(data.get('_bee') ?? '');
    if (!email) return;
    setStatus({ state: 'submitting' });
    const res = await submitCapture({ email, tag: `notify:${slug}`, slug, hp });
    setStatus(
      res.ok
        ? { state: 'success', message: res.message }
        : { state: 'error', message: res.message }
    );
    if (res.ok) form.reset();
  }

  return (
    <div className={s.notify}>
      <div className={s.notifyHead}>Operator Blueprint №{number}</div>
      <div className={s.notifyTitle}>{title}</div>
      <form onSubmit={onSubmit} noValidate>
        <label className={s.inputLabel} htmlFor={`notify-${slug}`}>
          Work email
        </label>
        <input
          id={`notify-${slug}`}
          type="email"
          name="email"
          placeholder="you@company.com"
          className={s.input}
          required
          autoComplete="email"
        />
        <input
          type="text"
          name="_bee"
          className={s.honeypot}
          tabIndex={-1}
          aria-hidden
          autoComplete="off"
        />
        <button
          type="submit"
          className={s.submit}
          disabled={status.state === 'submitting'}
        >
          {status.state === 'submitting'
            ? '…'
            : `Notify me when №${number} is live`}
        </button>
        {status.state === 'success' && (
          <div className={s.captureStatus} role="status">
            {status.message}
          </div>
        )}
        {status.state === 'error' && (
          <div className={s.captureError} role="alert">
            {status.message}
          </div>
        )}
      </form>
      <div className={s.fineprint}>
        One email when it ships. You&apos;re also on the Monday note unless you opt
        out.
      </div>
    </div>
  );
}

export function BlueprintCaptureForm({ slug, number, title }: NotifyProps) {
  const [status, setStatus] = useState<FormStatus>({ state: 'idle' });

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    const email = String(data.get('email') ?? '').trim();
    const hp = String(data.get('_bee') ?? '');
    if (!email) return;
    setStatus({ state: 'submitting' });
    const res = await submitCapture({ email, tag: `blueprint:${slug}`, slug, hp });
    setStatus(
      res.ok
        ? { state: 'success', message: res.message }
        : { state: 'error', message: res.message }
    );
    if (res.ok) form.reset();
  }

  return (
    <div className={s.notify}>
      <div className={s.notifyHead}>Operator Blueprint №{number}</div>
      <div className={s.notifyTitle}>{title}</div>
      <form onSubmit={onSubmit} noValidate>
        <label className={s.inputLabel} htmlFor={`bp-${slug}`}>
          Work email
        </label>
        <input
          id={`bp-${slug}`}
          type="email"
          name="email"
          placeholder="you@company.com"
          className={s.input}
          required
          autoComplete="email"
        />
        <input
          type="text"
          name="_bee"
          className={s.honeypot}
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
          <div className={s.captureStatus} role="status">
            {status.message}
          </div>
        )}
        {status.state === 'error' && (
          <div className={s.captureError} role="alert">
            {status.message}
          </div>
        )}
      </form>
      <div className={s.fineprint}>
        PDF + every citation in your inbox. Also the Monday note; unsub anytime.
      </div>
    </div>
  );
}
