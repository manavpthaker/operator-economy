import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export const runtime = 'nodejs';

export async function GET(req: Request) {
  const url = new URL(req.url);
  const token = url.searchParams.get('token');
  if (!token) {
    return new NextResponse('Missing token.', { status: 400 });
  }

  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!supabaseUrl || !supabaseKey) {
    return new NextResponse('Unsubscribe is offline. Email hello@theoperatoreconomy.com.', {
      status: 503,
    });
  }

  const supabase = createClient(supabaseUrl, supabaseKey, {
    auth: { persistSession: false },
  });

  const { data, error } = await supabase
    .from('subscribers')
    .update({ unsubscribed_at: new Date().toISOString() })
    .eq('unsubscribe_token', token)
    .select('email, tag');

  if (error) {
    console.error('unsubscribe failed', error);
    return new NextResponse('Storage error. Try again in a minute.', {
      status: 500,
    });
  }

  if (!data || data.length === 0) {
    return new NextResponse(
      'That link has already been used or is invalid. If you keep receiving mail, reply STOP to any message.',
      { status: 404, headers: { 'content-type': 'text/plain; charset=utf-8' } }
    );
  }

  return new NextResponse(
    `Unsubscribed. You won't hear from us again. If this was a mistake, resubscribe at theoperatoreconomy.com.`,
    { status: 200, headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
}
