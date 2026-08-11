# Comp-set packaging research (2026-08-11)

First-party data, not a synthesis of other people's checklists. 221 videos, 8 channels, pulled
from the channel pages on 2026-08-11 and banded **within channel** against that channel's own
median views.

Everything the thumbnail system currently believes was inferred. `thumbnail_spec.py` says so in
its own comment — the weights encode "a belief about what makes someone click, inferred from what
YouTube surfaces on a cold feed." `docs/thumbnail-rubric.md` came from a general-audience creator
checklist and had to be half-overturned by amendments A1–A6 inside a month, including A3 reversing
its own rule 3. Eight generation rounds were spent guessing. This is the first look at what the
comp set actually does, measured.

Rebuild with:

```bash
python3 studio/scripts/research/yt_compset.py --from-pulls <nimble-dumps> --out research/thumbnails
```

## Method, and what it cannot tell you

- **Within-channel only.** Subscriber bases differ by orders of magnitude, so cross-channel view
  comparison is meaningless. Every band is relative to that channel's own median.
- **Raw views, not views/day.** Early view velocity far exceeds the long-run average, and cadence
  varies wildly across the set (Greg Isenberg's recent-30 spans 90 days; MagnatesMedia's spans
  1095). Ranking by views/day would rank by recency. Videos under 21 days old are dropped.
- **Recent-30 per channel.** This describes what each channel is doing *now*, not its catalogue.
- **Excluded:** Company Man (the pull returned 16-year-old personal uploads, not the
  documentaries). Growth in Reverse is kept in the sheet but carries no performance claim — 219 to
  4,900 views is a newsletter brand's incidental YouTube presence. Codie Sanchez timed out on four
  attempts; her channel page is the one real gap in the set.

**The load-bearing limitation: views are not CTR.** A view count reflects topic demand and
algorithmic distribution at least as much as packaging. Where this document says a video won, it
means it got more views than its channel-mates — not that its thumbnail earned the click. Nothing
below should be read as "this thumbnail treatment causes clicks." The one claim the data supports
cleanly is the *negative* one in Finding 2, which needs no causal story.

**This is title analysis.** The thumbnails themselves are not analysed here: the sandbox's egress
policy blocks `i.ytimg.com`, so the images could not be fetched or looked at. That is what
`contact-sheet.html` is for, and reading it is the missing half of this work.

## Finding 1 — the comp set is split in two on whether the title carries the money

| Channel | Lane | Titles with a $ figure |
|---|---|---|
| MagnatesMedia | documentary craft | **3%** |
| How Money Works | register benchmark | **3%** |
| Modern MBA | register benchmark | **7%** |
| Greg Isenberg | AI-idea lane | 17% |
| UpFlip | direct comp | **93%** |
| Starter Story | direct comp | **97%** |

Not a spectrum — a fork. The register lane almost never puts a number in the title; the direct-comp
lane almost always does. Both lanes work at scale.

This matters because the rubric's `complement` dimension (15 pts) fails a candidate outright if it
shares "any word or number" with the title. That rule assumes the title carries the number. In the
register lane there is no number in the title to complement, so the rule fires on nothing; in the
direct-comp lane the number is in the title 95% of the time and those channels put it on the
thumbnail *too*. Neither lane behaves the way the dimension assumes. OE has been straddling: the
rubric demands a hero number on the thumbnail *and* forbids overlap with a title that often carries
one.

## Finding 2 — surface title features do not separate winners from losers

Pooled top vs bottom quartile, within channel, n=161:

| feature | top | bottom | delta |
|---|---|---|---|
| contains $ figure | 41% | 41% | **+0pt** |
| contains any number | 15% | 18% | −3pt |
| superlative / hype word | 5% | 10% | −5pt |
| second person ("you") | 0% | 5% | −5pt |
| opens with how/why/what | 23% | 31% | −8pt |
| ends with "?" | 13% | 5% | +8pt |
| median word count | 7 | 8 | — |

Every one of these is inside noise at this n. **The features a packaging rubric normally encodes
have essentially no discriminative power within these channels.** This is the most reliable result
in the set, because it is a null result — it needs no causal story about why something won.

The current rubric is built almost entirely from features of this kind: one hero figure, an
interpreting label of 2–3 words, no shared words with the title, a specific unanswered question.
Those are form rules. The data says form is not where the variance lives.

## Finding 3 — what does separate them is how recognisable the subject is

Two near-controlled pairs, same channel, same title construction, subject swapped:

| | views | |
|---|---|---|
| Modern MBA — "Why **Crumbl Cookies** Can't Survive" | 2,200,000 | |
| Modern MBA — "Why **OpenAI** Can't Survive" | 143,000 | **15.4×** |
| MagnatesMedia — "The CRAZY Truth About **McDonald's**" | 2,800,000 | |
| MagnatesMedia — "The Scariest Business **In The World**" | 360,000 | **7.8×** |

Identical grammar. The variable is whether the subject is a specific thing the viewer has direct
experience of. The pattern holds across the whole set: top quartiles are named brands (Crumbl,
McDonald's, IKEA, Rockefeller, Hermes Agent), familiar physical trades (barbers, fried chicken,
fish, food trucks), or conditions in the viewer's own life (the car market, inflation). Bottom
quartiles are abstract categories, macro topics, and anonymous subjects — Ukraine's minerals, "a
hidden niche," "9 biggest startup ideas," "the scariest business in the world."

Caveat per the method note: this is very likely partly a topic-demand effect, not purely a
packaging effect. More people want a Crumbl video than an OpenAI-economics video. That does not
weaken the operational conclusion — *put a recognisable, concrete thing in the frame* — but it does
mean the mechanism is unproven.

## Finding 4 — believable numbers beat bigger numbers

In the two channels that do put money in titles, the smaller figure won both times, decisively:

| | views | |
|---|---|---|
| Starter Story — "I Built a **$20K/Month** App in 83 Days" | 271,000 | |
| Starter Story — "She Built This **$340K/Month** App in 60 Days" | 55,000 | **4.9×** |
| UpFlip — "How He Makes **$3M a Year** Selling Fried Chicken" | 2,700,000 | |
| UpFlip — "Hidden Business Idea that Brings in **$5M/Month**" | 144,000 | **18.8×** |

And over-precision sits at the very bottom: UpFlip's "This Cleaning Business Makes **$23,013.69** a
Week" is the worst-performing video in its channel's sample at 87,000. A figure to the cent reads as
a spreadsheet, not a claim.

This inverts the intuition behind the `hero` dimension, which rewards a figure "concrete enough to
read instantly at browse size" and says nothing about whether the viewer believes it. On this
evidence the constraint on a hero number is **credibility**, not size or legibility. Which is
convenient: it is the same constraint the brand's documentary register already imposes.

## Finding 5 — cleverness in the packaging layer is a cost

How Money Works' two typographically stylised titles — a strikethrough gag and a sArCaStIc-CaPs
title — are both in its bottom quartile (485,000 and 457,000 against a top-quartile median of
1,400,000). Small n, but it points the same direction as the superlative rate in Finding 2. The
joke is legible to people who already subscribe and is noise to everyone else.

## What this implies for the rubric

The current weights look close to inverted against this evidence:

| dimension | weight | what the data says |
|---|---|---|
| `hero` — one dominant figure | **22** | number-presence has **+0pt** effect (F2). Where numbers are used, credibility is the binding constraint, which the dimension does not encode (F4) |
| `stakes` — gain/loss to viewer | 18 | untested here; plausible and unchallenged |
| `complement` — no overlap with title | **15** | assumes a fact pattern neither lane exhibits (F1) |
| `curiosity` — unresolved question | 15 | untested directly; the "?" signal is +8pt but inside noise |
| `subject` — human or object anchor | 12 | closest to the real variable, but scores *presence* of an anchor, not its **recognisability** (F3) |
| `unrepeatable` — episode specificity | **10** | nearest thing to the dominant variable in the data, and third-lowest weighted |
| `legibility` — survives 120px | 8 | untested by this data; keep, it is a floor not a driver |

The shape of the fix: collapse the form dimensions, and promote a single dimension for *how
recognisable and concrete the depicted thing is* — which is roughly today's `unrepeatable` and
`subject` merged and given the weight `hero` currently holds.

**Not doing that yet, deliberately.** Re-weighting a thumbnail rubric from title data, without
having looked at a single comp thumbnail, would repeat the exact mistake that produced the current
one: inferring visual rules from non-visual evidence. `contact-sheet.html` is the instrument for
the other half. The re-weighting should follow reading it.

## Open

- **Read the contact sheet.** The visual question it is built to answer: what do a channel's
  top-quartile tiles share that its own bottom-quartile tiles do not?
- **Codie Sanchez is missing** — four timeouts. The one named direct competitor absent from the set.
- **CTR is unavailable for anyone but us.** Nothing here can be validated against click-through
  externally; our own Test & Compare data is the only route to that, whenever the channel unlocks it.
