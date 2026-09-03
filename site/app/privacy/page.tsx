import type { Metadata } from 'next';
import { SiteFooter, SiteHeader } from '../components/SiteChrome';

export const metadata: Metadata = {
  title: 'Privacy · The Operator Economy',
  description: 'How The Operator Economy handles newsletter and site data.',
};

export default function PrivacyPage() {
  return (
    <div id="top">
      <a className="bl-skip-link" href="#main">Skip to content</a>
      <SiteHeader current="privacy" />
      <main id="main">
        <section className="bl-opening bl-shell oe-page-hero" aria-labelledby="privacy-title">
          <div className="bl-episode-feature__intro">
            <h1 id="privacy-title">Privacy, stated plainly.</h1>
            <p>The Operator Economy is an independent publication. This notice explains what the site collects, why it is used, and how to ask for deletion.</p>
            <p className="oe-page-note">Effective September 3, 2026 · Privacy contact: <a href="mailto:hello@theoperatoreconomy.com">hello@theoperatoreconomy.com</a></p>
          </div>
        </section>

        <section className="oe-section oe-band-inset bl-shell" aria-labelledby="notice-title">
          <div className="oe-privacy-copy">
            <h2 id="notice-title">What the site collects</h2>
            <p>If you subscribe, the site collects the email address you submit and records that you requested the newsletter. The hosting and delivery providers may also process basic request, device, and delivery information needed to operate and secure the service.</p>

            <h2>How it is used</h2>
            <p>Your email is used to send The Operator Economy newsletter, confirm or service that request, prevent abuse, and maintain unsubscribe or suppression records. It is not sold.</p>

            <h2>Downloads and consent</h2>
            <p>Public Blueprint downloads do not require an email address and do not subscribe you. Newsletter signup is a separate action. Every marketing email includes an unsubscribe path.</p>

            <h2>Service providers</h2>
            <p>The site uses Vercel for hosting, Supabase for subscription records, and Resend for email delivery. Those providers process data under their own terms and may process it in the United States or other locations where they operate.</p>

            <h2>Retention and deletion</h2>
            <p>Subscription data is retained while the subscription is active and for the limited period needed to honor suppression, security, and legal obligations. To request access, correction, or deletion, email <a href="mailto:hello@theoperatoreconomy.com">hello@theoperatoreconomy.com</a>. Some suppression information may be retained so an unsubscribe request is not accidentally reversed.</p>

            <h2>Cookies and analytics</h2>
            <p>The current site does not use advertising cookies. Hosting providers may keep routine security and request logs. This notice will be updated before adding materially different tracking or advertising technology.</p>

            <h2>Changes</h2>
            <p>A material change to this notice will receive a new effective date on this page.</p>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
