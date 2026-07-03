// Shared capture client: every form on the site posts through this.
// Contract mirrors /api/subscribe: {email, tag, slug?, hp}.

export type CaptureTag =
  | 'newsletter'
  | `blueprint:${string}`
  | `notify:${string}`;

export type CaptureRequest = {
  email: string;
  tag: CaptureTag;
  slug?: string;
  hp?: string; // honeypot
};

export type CaptureResult =
  | { ok: true; message: string }
  | { ok: false; message: string };

export async function submitCapture(req: CaptureRequest): Promise<CaptureResult> {
  try {
    const res = await fetch('/api/subscribe', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(req),
    });
    const body = (await res.json().catch(() => ({}))) as {
      ok?: boolean;
      message?: string;
    };
    if (!res.ok || body.ok === false) {
      return {
        ok: false,
        message: body.message || 'Something broke on our end. Try again in a minute.',
      };
    }
    return {
      ok: true,
      message: body.message || 'Filed. Check your inbox.',
    };
  } catch {
    return {
      ok: false,
      message: 'Network error. Check your connection and try again.',
    };
  }
}
