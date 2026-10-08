import type { Resend } from 'resend';

// The newsletter list lives in Resend so issues go out as Resend Broadcasts.
// Supabase stays the record for welcome and Blueprint emails; this mirrors only
// `newsletter` signups (the only form that consents to the newsletter, per /privacy).
// Best-effort: a Resend hiccup must never fail a signup or an unsubscribe.

function segmentId(): string | null {
  return process.env.RESEND_OE_SEGMENT_ID || null;
}

export async function syncNewsletterContact(
  resend: Resend,
  email: string,
  unsubscribed: boolean
): Promise<void> {
  const id = segmentId();
  if (!id) return;
  try {
    const created = await resend.contacts.create({ email, unsubscribed, segments: [{ id }] });
    if (!created.error) return;
    // Already a contact (e.g. from another list): update in place and make sure
    // they're in this segment.
    const updated = await resend.contacts.update({ email, unsubscribed });
    if (updated.error) throw new Error(updated.error.message);
    if (!unsubscribed) {
      const added = await resend.contacts.segments.add({ email, segmentId: id });
      if (added.error && !/already/i.test(added.error.message)) throw new Error(added.error.message);
    }
  } catch (err) {
    console.error('resend contact sync failed', err instanceof Error ? err.message : err);
  }
}
