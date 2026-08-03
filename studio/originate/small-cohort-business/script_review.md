# Script review: The Six-Person Business Model Nobody Markets

**GATE 1 — your POV pass.** Edit `script.json` directly:
- Replace every `[POV: ...]` token with your own experience/take (required — this is the monetization moat).
**POV insertions required: 1**
- Rewrite anything that doesn't sound like you.
- Check every number against the source. Delete claims you can't stand behind.

**Title options:** The Six-Person Business Model Nobody Markets | One Enrollee, One Peer, One Real Cohort Business | Why Reforge Sold Itself Instead of Scaling Cohorts

## hook
- (1) One operator is running a cohort business with exactly one paying student. Another, teaching almost the same thing at the same price, filled six seats and is profitable. A venture-backed version of this same idea raised twenty million dollars and got acquired by Miro this year. Same business. Wildly different outcomes. That gap is the entire episode.

## thesis
- (1) A small cohort is a group of six to fifteen people who pay eight hundred to two thousand dollars each to go through something you built and taught, live, two or three times a year. It's not a course sitting on a shelf. It's a room with a start date and an end date.
  - source: Research brief §1 — cohort pricing bands
- (2) The thing you'd teach is usually the job you already had. A recruiter teaching interview positioning. A clinician teaching other clinicians how to rebuild after a layoff. The expertise already exists. What used to be missing was a cheap way to build the intake, the scheduling, the payment, and the delivery without hiring anyone.
- (3) At the low effort level, this looks like one person running a single cohort a year off a free-tier stack, doing the coaching themselves. At the high effort level, someone runs three cohorts a year, has a waitlist, and has automated the intake scoring with AI so they spend their time teaching, not sorting spreadsheets. Both are real versions of the same build.

## evidence
- (1) Start with the honest low end, because most of what gets published here is a vendor blog pretending to be a case study. Joanie Johnson runs Reframe and Ready, a cohort for clinicians navigating job loss. Her current cohort has one enrollee — a PhD-level clinician who's basically driving his own curriculum. A peer running a similar program at a similar price point filled six seats. Her sixty-dollar interview-coaching webinar underfilled.
  - source: First-party call notes, July 14 2026 — Joanie Johnson
- (2)  ⚠️ POV NEEDED In her market, eight hundred dollars is a lot of money, because her buyers are unemployed clinicians between paychecks. She's had multiple sales consults recently and none converted, so she's testing a pay-on-placement structure instead of charging upfront. [POV: Manav could add what it was like building her intake flow and watching the consults not convert despite a clean funnel]
  - source: First-party call notes, July 14 2026
- (3) Joanie is not proof that fifteen people will pay two thousand dollars for a cohort. She's proof of something narrower and more useful: the cost to build this dropped to almost nothing. That's the actual claim of this episode, and it's worth being honest about the difference.
- (4) Now the ceiling anecdote, and the discount that has to come with it. Ali Abdaal's Part-Time YouTuber Academy sold seats at close to five thousand dollars each. The first cohort reportedly did close to three hundred thousand dollars, and later single cohorts were reported at close to two million. Treat that as close to worthless for planning your first cohort — he had a multi-million-subscriber audience before he sold a single seat.
  - source: ebizfacts, third-party review site relaying self-reported figures [reported, marketing-adjacent]
- (5) Now the venture-scale proof the market exists at all. Maven raised twenty million dollars in a Series A led by a16z, ran over three hundred cohorts, and did about nine million dollars in course sales in its first eighteen months. Reforge raised eighty-one million dollars total and built a hundred thousand alumni at companies like Netflix and SAP.
  - source: TechCrunch, a16z, PitchBook/PR Newswire — Maven Series A, Reforge Series B
- (6) And then, this March, Reforge was acquired by Miro. Not by another education company — by a workplace software company that wanted its learning platform and its AI tooling. The best-funded version of selling expertise to professionals didn't become an education empire. It became a feature inside someone else's product.
  - source: Miro newsroom, March 24 2026
- (7) Read that the way it deserves to be read. The venture lane for this business just closed at the top. Which raises the real question: if the biggest version of this idea got absorbed into someone else's roadmap, what's actually left for the person running it alone?

## stack
- (1) There are two paths here, and both are legitimate. Path one is a hosted platform — Kajabi, Teachable, Podia, Circle. You pay a monthly fee, sometimes a transaction cut on top, and you're running a cohort within a week. That's a real trade of margin for speed, and for a first cohort it's not a bad one.
  - source: Kourses, Teachery, Circle vendor pricing pages, July 2026 [reported, vendor]
- (2) Path two is owning the stack. Next.js for the site, Supabase for the database and login, Resend for email, and Square or Stripe to take payment. At this scale that's roughly zero to fifty dollars a month, plus the standard card processing fee. This is exactly what the Reframe and Ready platform runs on.
  - source: First-party — Reframe & Ready build, grapevines/apps/cohorts
- (3) The part that's actually new is the AI layer sitting on top of either path — scoring intake forms, analyzing assessments, drafting the session decks. That used to be a Google Form, a spreadsheet you built by hand, and a Canva deck someone stayed up until 1 a.m. finishing. Now it's mostly automated.
- (4) Before any of that, there's a step zero most people skip: using something like Claude or NotebookLM to find the gap between what you know and what people are actually searching for. Most people who fail here didn't build the wrong platform — they picked the wrong topic before they built anything.

## playbook
- (1) Week one is not building anything. It's using an AI research tool to map what you know against what people are actually asking for, and writing down the narrowest version of that gap you can defend in one sentence.
- (2) Weeks two and three, pick your path. If you're using a hosted platform, get a landing page and a payment link live — that can happen in days. If you're owning the stack, this is where a Next.js site, a Supabase table for enrollees, and a Square payment link get wired together. Either way, the goal is a page that can take money before the curriculum is finished.
- (3) Month one is entirely about talking to the six to ten people who might actually pay — not posting content and hoping. Direct outreach to your existing network, one specific offer, one specific price. This is the part AI does not shortcut.
- (4) Your first dollar comes from someone who already trusts you professionally, not a cold audience. Set a floor — Joanie's peer who filled six seats had a minimum-cohort clause: below that number, the date moves or the client pays a floor fee. Build that in from the start, not after your first half-empty cohort.
  - source: Research brief §1 — experience floor, minimum cohort clauses [reported]
- (5) By the end of month one you should know one thing for certain: whether six people who don't already know you will pay for this. If they won't yet, the fix is never a better platform. It's a sharper offer to more of the right people — which is a distribution problem, not a build problem.

## economics
- (1) If you want the exact build plan Joanie used, the stack, the intake flow, and the outreach script from month one, that's laid out step by step in the free blueprint — link's below.
- (2) Here's the math that actually decides whether this business works. Six seats at two thousand dollars is twelve thousand dollars gross. Run that through Maven and the platform fee alone is around fifteen hundred dollars — roughly one enrollee's worth of revenue, gone before you've taught a single session. Run it through an owned stack and that cost drops to near zero.
  - source: Research brief §4 — platform tax math
- (3) Realistic range for a first-time solo operator: one small cohort a year, six to eight people, four to fifteen thousand dollars gross, minus almost nothing in platform costs if you own the stack. That's not a living on its own. It's a second income stream that scales with your reputation, not your hours.
  - source: estimate, reasoning: derived from research brief §1 pricing bands and §4 platform-tax math
- (4) What it costs you is real time before any money arrives — building the curriculum, the intake, and doing outreach with no guarantee anyone signs up. The build risk is close to zero now. The enrollment risk never went away, and no tool fixes that for you.
- (5) The failure modes are specific: cohorts under six people stop feeling like a room, buyers in career transition are often cash-constrained, and progress on a curriculum doesn't feel as urgent to a buyer as sending out ten more job applications today. Those are the real objections, not the platform you pick.
  - source: Research brief §6 — failure modes

## cta
- (1) The full blueprint has the stack, the intake templates, and the outreach script — grab it with the link below. And if you want the next build broken down the same way, subscribe.

---
When done, continue with:
```
python originate.py <slug> --continue
```