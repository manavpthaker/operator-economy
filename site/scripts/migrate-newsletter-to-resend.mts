// One-time: copy newsletter subscribers from Supabase into a Resend segment so
// issues can go out as Resend Broadcasts. Safe to re-run (contacts upsert).
//
//   SUPABASE_URL=… SUPABASE_SERVICE_ROLE_KEY=… RESEND_API_KEY=… \
//     npx tsx scripts/migrate-newsletter-to-resend.mts [--dry-run]
//
// Prints the segment id; set it as RESEND_OE_SEGMENT_ID in Vercel so new
// signups and unsubscribes keep the segment in sync.
import { createClient } from '@supabase/supabase-js';
import { Resend } from 'resend';
import { syncNewsletterContact } from '../app/lib/resend-contacts';

const SEGMENT_NAME = 'The Operator Economy';
const dryRun = process.argv.includes('--dry-run');

const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, RESEND_API_KEY } = process.env;
if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY || !RESEND_API_KEY) {
  console.error('Needs SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY and RESEND_API_KEY.');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
const { data: rows, error } = await supabase
  .from('subscribers')
  .select('email, unsubscribed_at')
  .eq('tag', 'newsletter');
if (error) throw new Error(error.message);
const active = rows.filter((r) => !r.unsubscribed_at);
console.log(`newsletter rows: ${rows.length} (${active.length} active, ${rows.length - active.length} unsubscribed)`);
if (dryRun) process.exit(0);

const resend = new Resend(RESEND_API_KEY);
let segmentId = process.env.RESEND_OE_SEGMENT_ID;
if (!segmentId) {
  const list = await resend.segments.list();
  if (list.error) throw new Error(list.error.message);
  segmentId = list.data?.data.find((s) => s.name === SEGMENT_NAME)?.id;
  if (!segmentId) {
    const made = await resend.segments.create({ name: SEGMENT_NAME });
    if (made.error || !made.data) throw new Error(made.error?.message ?? 'segment create failed');
    segmentId = made.data.id;
  }
  process.env.RESEND_OE_SEGMENT_ID = segmentId;
}

// Resend's default API rate limit is a few requests a second; stay under it.
const pause = () => new Promise((r) => setTimeout(r, 600));
let n = 0;
for (const r of rows) {
  await syncNewsletterContact(resend, r.email, Boolean(r.unsubscribed_at));
  n += 1;
  if (n % 25 === 0) console.log(`  ${n}/${rows.length}`);
  await pause();
}
console.log(`done: ${n} contacts synced (unsubscribed ones kept as unsubscribed).`);
console.log(`RESEND_OE_SEGMENT_ID=${segmentId}`);
