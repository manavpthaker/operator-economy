# Step 8 runbook v0.1: LinkedIn OE page and newsletter

Status: **approved v0.1 (owner, 2026-09-24).** Derived from EP007 / public №001 and updated 2026-09-24 to point presenter work at `blueprint-cinema/references/PRESENTER-RECIPE.md`. Authoritative for its stage; a record still wins where it disagrees on EP007 facts. Page refresh done; post and
newsletter scheduling to be completed after the YouTube upload and recorded here.
`content-os/flow.md` step 16 owns the scheduling order and composer gotchas; this adds the how-to.

## Access

- Use the owner's Chrome (Claude in Chrome extension); the operator's LinkedIn account is an admin
  of **The Operator Economy** page (`linkedin.com/company/136054601`, public `/company/operator-economy`).
- Never sign in or enter credentials. Stop before each final "Schedule/Post" click for owner confirmation.

## Page branding (done 2026-09-23)

Admin → Edit page:
- **Page info:** logo = `channel/brand-2026-09/linkedin-logo-400.png` (file input "Upload logo");
  cover = `linkedin-cover.png` via "Edit background" → "Edit cover image" → "Change image" file
  input → Apply (applies immediately); decline the "share your page edits" post prompt.
- **Tagline** (120 max): "Build, own and operate a business of one using AI. New episodes Mondays."
- **Details → Overview:** the approved About text (same as YouTube).
- LinkedIn's React form ignores programmatic value changes: click the field, select all, and
  **type** the text; then click Save in the sticky header. Verify via
  `/company/136054601/about/?viewAsMember=true` page text.

## Scheduling (after YouTube links exist)

Order (flow.md): OE page episode post → Mon 11:00 ET (Canvas image/carousel attached **last**,
then Schedule); four Shorts posts → Tue–Fri 08:30 ET; newsletter edition → Mon (verify the native
schedule Mon 08:25). Copy: `studio/originate/<slug>/content/linkedin_posts.md`, `newsletter.md`,
with `{{EPISODE_URL}}` / Canvas URL filled from `launch/links.json`.

Composer gotchas: media is discarded by any schedule-dialog round trip (set text, set schedule,
attach media last, Schedule immediately); the time field only commits via dropdown select or blur;
nothing can be scheduled < 10 minutes out; one composer at a time while video processes.

After scheduling, record each scheduled item (type, time, URL if shown) in the episode
`RELEASE-RECORD.md` and run `content-os/bin/weekly.py record-scheduled` when the gate applies.
