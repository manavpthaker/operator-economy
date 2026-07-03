import { NextResponse } from 'next/server';
import { neon } from '@neondatabase/serverless';

export const runtime = 'nodejs';

export async function GET(req: Request) {
  const url = new URL(req.url);
  const token = url.searchParams.get('token');
  if (!token) {
    return new NextResponse('Missing token.', { status: 400 });
  }

  const dbUrl = process.env.DATABASE_URL || process.env.POSTGRES_URL;
  if (!dbUrl) {
    return new NextResponse('Unsubscribe is offline. Email hello@theoperatoreconomy.com.', {
      status: 503,
    });
  }

  const sql = neon(dbUrl);
  try {
    const rows = await sql`
      update subscribers
        set unsubscribed_at = now()
        where unsubscribe_token = ${token}
        returning email, tag
    `;
    if (rows.length === 0) {
      return new NextResponse(
        'That link has already been used or is invalid. If you keep receiving mail, reply STOP to any message.',
        { status: 404, headers: { 'content-type': 'text/plain; charset=utf-8' } }
      );
    }
    return new NextResponse(
      `Unsubscribed. You won't hear from us again. If this was a mistake, resubscribe at theoperatoreconomy.com.`,
      { status: 200, headers: { 'content-type': 'text/plain; charset=utf-8' } }
    );
  } catch (err) {
    console.error('unsubscribe failed', err);
    return new NextResponse('Storage error. Try again in a minute.', {
      status: 500,
    });
  }
}
