import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { Resend } from 'resend';
import { randomBytes } from 'node:crypto';
import { getEpisodeBySlug } from '../../components/LatestBlueprint';
import { renderWelcomeEmail } from '../../lib/email-templates';

export const runtime = 'nodejs';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const TAG_RE = /^(newsletter|blueprint:[a-z0-9-]+|notify:[a-z0-9-]+)$/;

type Body = {
  email?: string;
  tag?: string;
  slug?: string;
  hp?: string;
};

// Best-effort rate limit — one write per IP per 15s, in-memory (per-region).
// Not a security boundary (that's the honeypot + email verification via Resend),
// just abuse dampening. Cleared on cold-start; that's fine.
const recentWrites = new Map<string, number>();
const RATE_WINDOW_MS = 15_000;

function tooSoon(ip: string): boolean {
  const now = Date.now();
  const last = recentWrites.get(ip) ?? 0;
  if (now - last < RATE_WINDOW_MS) return true;
  recentWrites.set(ip, now);
  // Prune occasionally.
  if (recentWrites.size > 500) {
    for (const [k, t] of recentWrites) {
      if (now - t > RATE_WINDOW_MS * 4) recentWrites.delete(k);
    }
  }
  return false;
}

function fail(message: string, status = 400) {
  return NextResponse.json({ ok: false, message }, { status });
}

function baseUrl(req: Request): string {
  return process.env.NEXT_PUBLIC_SITE_URL || new URL(req.url).origin;
}

function slugFromTag(tag: string): string | null {
  if (tag.startsWith('blueprint:') || tag.startsWith('notify:')) {
    return tag.split(':')[1] ?? null;
  }
  return null;
}

function fromAddress(): string {
  return (
    process.env.RESEND_FROM ||
    'The Operator Economy <hello@theoperatoreconomy.com>'
  );
}

async function sendWelcome({
  resend,
  email,
  tag,
  unsubscribeUrl,
}: {
  resend: Resend;
  email: string;
  tag: string;
  unsubscribeUrl: string;
}) {
  const slug = slugFromTag(tag);
  const ep = slug ? getEpisodeBySlug(slug) : undefined;

  if (tag === 'newsletter') {
    const { subject, html, text } = renderWelcomeEmail(
      { tag: 'newsletter' },
      unsubscribeUrl
    );
    await resend.emails.send({ from: fromAddress(), to: email, subject, html, text });
    return;
  }

  if (tag.startsWith('blueprint:') && ep) {
    const { subject, html, text } = renderWelcomeEmail(
      {
        tag: tag as `blueprint:${string}`,
        episode: { number: ep.number, title: ep.title, slug: ep.slug },
        pdfAvailable: ep.status === 'live',
        siteUrl: baseUrlFromResend(),
      },
      unsubscribeUrl
    );
    await resend.emails.send({ from: fromAddress(), to: email, subject, html, text });
    return;
  }

  if (tag.startsWith('notify:') && ep) {
    const { subject, html, text } = renderWelcomeEmail(
      {
        tag: tag as `notify:${string}`,
        episode: { number: ep.number, title: ep.title, slug: ep.slug },
      },
      unsubscribeUrl
    );
    await resend.emails.send({ from: fromAddress(), to: email, subject, html, text });
    return;
  }

  // Unknown tag / missing episode — plain confirmation, no template.
  await resend.emails.send({
    from: fromAddress(),
    to: email,
    subject: 'Confirmed.',
    text: `Confirmed. Unsubscribe any time: ${unsubscribeUrl}`,
  });
}

function baseUrlFromResend(): string {
  return (
    process.env.NEXT_PUBLIC_SITE_URL || 'https://operator-economy.vercel.app'
  );
}

export async function POST(req: Request) {
  let body: Body;
  try {
    body = (await req.json()) as Body;
  } catch {
    return fail('Malformed request.', 400);
  }

  // Honeypot — silently accept but do nothing.
  if (body.hp && body.hp.trim() !== '') {
    return NextResponse.json({ ok: true, message: 'Filed. Check your inbox.' });
  }

  const email = (body.email ?? '').trim().toLowerCase();
  const tag = (body.tag ?? '').trim();
  if (!EMAIL_RE.test(email)) return fail('That email looks off. Retry it.');
  if (!TAG_RE.test(tag)) return fail('Unknown form.');

  const ip =
    req.headers.get('x-forwarded-for')?.split(',')[0].trim() ||
    req.headers.get('x-real-ip') ||
    'unknown';
  if (tooSoon(ip)) return fail('Slow down — try again in a few seconds.', 429);

  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const resendKey = process.env.RESEND_API_KEY;

  if (!supabaseUrl || !supabaseKey || !resendKey) {
    return fail(
      'Signup is temporarily offline. This is on us — try again in a bit.',
      503
    );
  }

  const supabase = createClient(supabaseUrl, supabaseKey, {
    auth: { persistSession: false },
  });
  const unsubscribeToken = randomBytes(24).toString('hex');
  const slug = body.slug ?? slugFromTag(tag);

  const { error: upsertError } = await supabase
    .from('subscribers')
    .upsert(
      {
        email,
        tag,
        slug: slug ?? null,
        unsubscribe_token: unsubscribeToken,
        unsubscribed_at: null,
      },
      { onConflict: 'email,tag' }
    );

  if (upsertError) {
    console.error('subscribe upsert failed', upsertError);
    return fail('Storage error. Try again in a minute.', 500);
  }

  const unsubscribeUrl = `${baseUrl(req)}/api/unsubscribe?token=${unsubscribeToken}`;

  try {
    const resend = new Resend(resendKey);
    await sendWelcome({ resend, email, tag, unsubscribeUrl });
  } catch (err) {
    console.error('resend send failed', err);
    // The row is stored; the send failed. Tell the user honestly.
    return fail(
      "You're on the list, but the confirmation email didn't send. Check your spam and email hello@theoperatoreconomy.com if it never arrives.",
      502
    );
  }

  return NextResponse.json({ ok: true, message: 'Filed. Check your inbox.' });
}
