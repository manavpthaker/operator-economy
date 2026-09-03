// OE-branded email templates for the three subscribe tags.
// One shared shell (wordmark + footer), three variants (newsletter / blueprint / notify).
// System font stacks only. No web-font @import; the Boska/Zodiak feel is approximated
// with Georgia + system mono so Gmail/Outlook/Apple Mail render consistently.

const LINKEDIN_URL = 'https://www.linkedin.com/company/operator-economy/';
const LINKEDIN_DISPLAY = 'linkedin.com/company/operator-economy';

type NewsletterVars = { tag: 'newsletter' };

type Episode = { number: number; title: string; slug: string };

type BlueprintVars = {
  tag: `blueprint:${string}`;
  episode: Episode;
  pdfAvailable: boolean;
  siteUrl: string;
};

type NotifyVars = {
  tag: `notify:${string}`;
  episode: Episode;
};

type WelcomeVars = NewsletterVars | BlueprintVars | NotifyVars;

export type RenderedEmail = {
  subject: string;
  html: string;
  text: string;
};

const SERIF = "Georgia, 'Times New Roman', serif";
const MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";

const COLORS = {
  paper: '#F5F0E6',
  paperOuter: '#E8E4D8',
  ink: '#1A1A1A',
  ink700: '#3C3A36',
  ink500: '#6B675E',
  ink400: '#8A857A',
  rule: '#D8CFB9',
  gold: '#7A5E24',
  goldBright: '#C4A45F',
};

function pad(n: number): string {
  return String(n).padStart(3, '0');
}

function wrap(subject: string, bodyRows: string): string {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="color-scheme" content="light" />
<meta name="supported-color-schemes" content="light" />
<title>${escapeHtml(subject)}</title>
</head>
<body style="margin:0;padding:0;background:${COLORS.paperOuter};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${COLORS.paperOuter};">
<tr><td align="center" style="padding:32px 12px;">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" border="0" style="background:${COLORS.paper};font-family:${SERIF};color:${COLORS.ink};max-width:560px;">
${wordmarkRow()}
${bodyRows}
${signoffRow()}
${footerRow()}
</table>
</td></tr>
</table>
</body>
</html>`;
}

function wordmarkRow(): string {
  return `<tr><td style="padding:28px 40px 20px 40px;border-bottom:1px solid ${COLORS.rule};">
<div style="font-family:${MONO};font-size:10.5px;letter-spacing:0.18em;text-transform:uppercase;color:${COLORS.ink700};">The Operator Economy</div>
</td></tr>`;
}

function signoffRow(): string {
  return `<tr><td style="padding:36px 40px 24px 40px;border-top:1px solid ${COLORS.rule};">
<div style="font-family:${SERIF};font-size:14px;line-height:1.5;color:${COLORS.ink700};">Build it. Own it. Operate it.</div>
<div style="font-family:${SERIF};font-size:14px;line-height:1.5;color:${COLORS.ink700};">Manav</div>
</td></tr>`;
}

function footerRow(unsubscribeUrl?: string): string {
  const unsub = unsubscribeUrl
    ? `<div style="font-family:${MONO};font-size:10.5px;letter-spacing:0.02em;color:${COLORS.ink400};margin-top:14px;">
<a href="${escapeAttr(unsubscribeUrl)}" style="color:${COLORS.ink400};text-decoration:underline;">Unsubscribe</a>
</div>`
    : '';
  return `<tr><td style="padding:0 40px 28px 40px;">
<div style="font-family:${MONO};font-size:10.5px;line-height:1.6;letter-spacing:0.02em;color:${COLORS.ink500};">
Replies aren&rsquo;t monitored. This is a send-only mailbox.<br />
Follow along on LinkedIn: <a href="${LINKEDIN_URL}" style="color:${COLORS.gold};text-decoration:none;border-bottom:1px solid ${COLORS.gold};">${LINKEDIN_DISPLAY}</a>
</div>
${unsub}
</td></tr>`;
}

function headline(text: string): string {
  return `<tr><td style="padding:36px 40px 8px 40px;">
<div style="font-family:${SERIF};font-weight:700;font-size:26px;line-height:1.2;letter-spacing:-0.01em;color:${COLORS.ink};">${text}</div>
</td></tr>`;
}

function body(text: string): string {
  return `<tr><td style="padding:16px 40px 8px 40px;">
<div style="font-family:${SERIF};font-size:16px;line-height:1.55;color:${COLORS.ink};">${text}</div>
</td></tr>`;
}

function bodyMuted(text: string): string {
  return `<tr><td style="padding:24px 40px 0 40px;">
<div style="font-family:${SERIF};font-size:15px;line-height:1.5;color:${COLORS.ink700};">${text}</div>
</td></tr>`;
}

function metaRule(label: string): string {
  return `<tr><td style="padding:28px 40px 0 40px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="border-left:2px solid ${COLORS.gold};padding:2px 0 2px 10px;">
<div style="font-family:${MONO};font-size:11px;letter-spacing:0.06em;color:${COLORS.ink700};">${label}</div>
</td></tr></table>
</td></tr>`;
}

function goldLabelRow(label: string): string {
  return `<tr><td style="padding:28px 40px 4px 40px;">
<div style="font-family:${MONO};font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:${COLORS.gold};">${label}</div>
</td></tr>`;
}

function ctaBlock(href: string, label: string): string {
  return `<tr><td style="padding:28px 40px 0 40px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="background:${COLORS.ink};padding:14px 22px;">
<a href="${escapeAttr(href)}" style="font-family:${MONO};font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:${COLORS.goldBright};text-decoration:none;">${label}</a>
</td></tr></table>
</td></tr>`;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttr(s: string): string {
  return escapeHtml(s);
}

export function renderWelcomeEmail(
  vars: WelcomeVars,
  unsubscribeUrl: string
): RenderedEmail {
  if (vars.tag === 'newsletter') {
    const subject = 'You are subscribed to The Operator Economy.';
    const rows = [
      headline('You&rsquo;re subscribed.'),
      body(
        'When a new business ships, you&rsquo;ll get the episode and its working document, with the sources, assumptions, and failure modes kept visible.'
      ),
      body('No drip. No sequence.'),
      metaRule('The Operator Economy &middot; new work only'),
    ].join('\n');
    // Rebuild wrap to inject unsubscribe into the footer.
    const html = wrapWithUnsub(subject, rows, unsubscribeUrl);
    const text = `You're subscribed to The Operator Economy.

When a new business ships, you'll get the episode and its working document, with the sources, assumptions, and failure modes kept visible.

No drip. No sequence.

The Operator Economy · new work only

Build it. Own it. Operate it.
Manav

Replies aren't monitored. This is a send-only mailbox. Follow along on LinkedIn: ${LINKEDIN_URL}

Unsubscribe: ${unsubscribeUrl}`;
    return { subject, html, text };
  }

  if (vars.tag.startsWith('blueprint:')) {
    const v = vars as BlueprintVars;
    const num = pad(v.episode.number);
    const subject = `Operator Blueprint №${num}: ${v.episode.title}`;
    const pdfHref = `${v.siteUrl}/blueprints/${v.episode.slug}.pdf`;
    const cta = v.pdfAvailable
      ? ctaBlock(pdfHref, 'Download the PDF &rarr;')
      : bodyMuted(
          'The PDF ships with the episode. I&rsquo;ll email you the moment it&rsquo;s ready.'
        );
    const rows = [
      goldLabelRow(`Operator Blueprint &#8470;${num}`),
      `<tr><td style="padding:6px 40px 8px 40px;"><div style="font-family:${SERIF};font-weight:700;font-size:26px;line-height:1.2;letter-spacing:-0.01em;color:${COLORS.ink};">${escapeHtml(v.episode.title)}.</div></td></tr>`,
      body(
        'Here it is. Each published claim carries its source or estimate label so you can inspect it.'
      ),
      cta,
      bodyMuted('This delivery does not subscribe you to the newsletter.'),
    ].join('\n');
    const html = wrapWithUnsub(subject, rows, unsubscribeUrl);
    const pdfLine = v.pdfAvailable
      ? `Download the PDF: ${pdfHref}`
      : `The PDF ships with the episode. I'll email you the moment it's ready.`;
    const text = `Operator Blueprint №${num}: ${v.episode.title}

Here it is. Each published claim carries its source or estimate label so you can inspect it.

${pdfLine}

This delivery does not subscribe you to the newsletter.

Build it. Own it. Operate it.
Manav

Replies aren't monitored. This is a send-only mailbox. Follow along on LinkedIn: ${LINKEDIN_URL}

Unsubscribe: ${unsubscribeUrl}`;
    return { subject, html, text };
  }

  // notify:*
  const v = vars as NotifyVars;
  const num = pad(v.episode.number);
  const subject = `You'll get one email when №${num} is live.`;
  const rows = [
    headline(`Filed. You&rsquo;ll get one email when &#8470;${num} is live.`),
    body(
      `When it is live, I&rsquo;ll email you the episode and its published working document for &ldquo;${escapeHtml(v.episode.title)}.&rdquo; That&rsquo;s it. Nothing else in between.`
    ),
    bodyMuted('This notification does not subscribe you to the newsletter.'),
  ].join('\n');
  const html = wrapWithUnsub(subject, rows, unsubscribeUrl);
  const text = `Filed. You'll get one email when №${num} is live.

When it is live, I'll email you the episode and its published working document for "${v.episode.title}." That's it. Nothing else in between.

This notification does not subscribe you to the newsletter.

Build it. Own it. Operate it.
Manav

Replies aren't monitored. This is a send-only mailbox. Follow along on LinkedIn: ${LINKEDIN_URL}

Unsubscribe: ${unsubscribeUrl}`;
  return { subject, html, text };
}

function wrapWithUnsub(subject: string, bodyRows: string, unsubscribeUrl: string): string {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="color-scheme" content="light" />
<meta name="supported-color-schemes" content="light" />
<title>${escapeHtml(subject)}</title>
</head>
<body style="margin:0;padding:0;background:${COLORS.paperOuter};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${COLORS.paperOuter};">
<tr><td align="center" style="padding:32px 12px;">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" border="0" style="background:${COLORS.paper};font-family:${SERIF};color:${COLORS.ink};max-width:560px;">
${wordmarkRow()}
${bodyRows}
${signoffRow()}
${footerRow(unsubscribeUrl)}
</table>
</td></tr>
</table>
</body>
</html>`;
}
