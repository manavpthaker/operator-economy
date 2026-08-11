# Comp-set visual findings (2026-08-11)

`findings.md` closes by saying the images are unread — "the sandbox's egress policy blocks
`i.ytimg.com`" — and names that as the missing half. It is no longer missing. Egress to
`i.ytimg.com` works from the local clone, so all 78 banded thumbnails were fetched and read at
reading size and again at 120px browse width.

**Set.** The 78 top/bottom-quartile thumbnails from `compset.json`, excluding Company Man (bad
pull) and Growth in Reverse (no performance claim) as `findings.md` does. Six channels, banded
within channel: Modern MBA, How Money Works, MagnatesMedia (register lane, 20 top / 20 bottom);
UpFlip, Starter Story, Greg Isenberg (direct-comp and creator lanes, 19 / 19).

**The same limitation applies.** These are views, not CTR. A thumbnail in the top quartile got more
views than its channel-mates; it did not necessarily earn the click. What the images *can* settle
is the negative result — whether a design feature discriminates at all — and that is most of what
is below.

## Finding V1 — form does not discriminate, confirmed at the pixel level

`findings.md` Finding 2 showed surface *title* features separating top from bottom by +0 to −8pt,
all inside noise. The images show the same thing far more starkly, because within a channel the
top and bottom quartiles are frequently **the same template**.

UpFlip is the clearest case. Top and bottom are indistinguishable by construction: expressive face
on the right, hero money figure in a saturated colour box on the left, a two-word interpreting
label underneath (`PER MONTH`, `A MONTH`, `START UP`), episode number in a corner tab. Every rule
our rubric scores — one hero figure, interpreting label not a naming label, single anchor, face
close-cropped, text out of the lower right — is satisfied by both bands equally.

Starter Story likewise: number in white bold sans, handwritten lowercase unit (`/month`,
`in 24 hours`), hand-drawn arrow to a phone, person centre-right. Both bands.

**A rubric made of form rules cannot rank these sets.** It scores UpFlip's x0.12 the same as its
x6.67. That is the strongest available argument that the current weights measure a floor and call
it a strategy.

## Finding V2 — the hero number is null in one lane and negative in ours

Counting a dominant money/quantity figure as the thumbnail's headline element:

| lane | top quartile | bottom quartile |
|---|---|---|
| register (Modern MBA, How Money Works, MagnatesMedia) | **0 of 20** | 4 of 20 |
| direct-comp / creator (UpFlip, Starter Story, Greg Isenberg) | 8 of 19 | 10 of 19 |

**Not one top-quartile thumbnail in the register lane carries a hero number.** Not one. How Money
Works' entire top quartile is a flat editorial verdict in condensed white caps over a press photo —
`WELL…WE TRIED…`, `CANCELLED`, `BIG PROMISES ARE COMING DUE…`, `WE NEVER LEARN`, `THE MATH IS NOT
MATHING`, `HOUSE PRICES ARE CRASHING`. Modern MBA's is a franchise label over a dense physical
scene — `THE ECONOMICS OF COOKIES / WEED / BARBERSHOPS / TEXAS BBQ / BURGERS`. MagnatesMedia's is
two or three words over a corrupted brand mascot.

In the direct-comp lane the figure is present in both bands at the same rate. It is null there and
absent from the winners here.

`thumbnail_spec.py` gives `hero` — "is there exactly ONE dominant figure" — **22 points, the
largest weight in the rubric**. It is scoring the single feature that no winning thumbnail in our
own register lane exhibits.

## Finding V3 — believability, visible

`findings.md` measured this in titles ($20K/mo beat $340K/mo by 4.9×). The thumbnails show the same
ordering and show the mechanism.

- Starter Story's worst video puts **`$340K`** on the thumbnail. Its top quartile runs `$14K`,
  `$30K`, `$100K in 24 hours`.
- UpFlip's bottom quartile carries **`$5M PER MONTH`** and `$300K PER MONTH`; its top carries
  `$91,000 PER MONTH`, `$120K PER MONTH`, `$150,000 A MONTH`, and `$50 START UP`.
- MagnatesMedia's one numeric thumbnail in either band, `$3.5K` on a Beanie Baby, is bottom.

And a move worth naming, visible only in the images: **UpFlip converts the annual figure in the
title to a monthly figure on the thumbnail.** Title "This Is How He Makes $1M a Year Selling Fish"
→ thumbnail `$91,000 PER MONTH`. Title "Her Half-Pound Eggrolls Bring In $1.8M/Year!" → thumbnail
`$150,000 A MONTH`. The thumbnail number is *smaller* than the title's and describes the same fact.
The pair is built so the title supplies the magnitude and the thumbnail supplies the plausibility.

## Finding V4 — one focal mass survives 120px; a multi-node composition does not

Every thumbnail was re-read at 120px wide, the browse width `check_thumbnail.py` measures.

What survives: a single large logo (Ford, McDonald's, IKEA, Nintendo, PayPal), a single large face,
a single large word or short sentence in condensed caps, and — unexpectedly — a **dense food scene**,
which stops being legible but stays instantly categorisable by colour and texture alone. Modern
MBA's `TEXAS BBQ` and `BURGERS` are unreadable at 120px and still unmistakably food.

What dies: everything with multiple nodes. The 1990s-vs-2020s split, the `DEJA VU` twin war maps
carrying five money figures, `$10,000 / $500` two-figure comparison, the `THE ORIGIN OF
SHRINKFLATION` scatter of eight percentages, the Insta360 product vitrine, the `STALEMATE` cinema
map with six chain logos. All six are bottom quartile, all six reduce to mush.

## Finding V5 — a logo collage is a bottom-quartile pattern; one big logo is a top-quartile one

This is the sharpest single result in the visual set, and it is a clean negative.

**Multiple small logos arranged as the subject — 5 instances, 5 bottom quartile, 0 top:**

| thumbnail | channel | band |
|---|---|---|
| `I WILL MAKE IT LEGAL!` over scattered Uber / Klarna / Airbnb / afterpay / Kalshi marks | How Money Works | x0.50 |
| `$17,000/MO IOS APP PLAYBOOK` over a row of five app icons | Greg Isenberg | x0.57 |
| `HE RAN A SAAS FROM UBERS` over Claude Code / Codex / OpenClaw chips | Greg Isenberg | x0.54 |
| `THE RISE OF Insta360`, a vitrine of GoPro / Nikon / Canon / Casio product | Modern MBA | x0.43 |
| `STALEMATE`, a US map tiled with AMC / Regal / Cinemark marks | Modern MBA | x0.57 |

**One logo at scale — MagnatesMedia's entire top quartile**, plus Ford (How Money Works, x2.38) and
the single Hermes Agent mark that anchors Greg Isenberg's two best (x1.85, x2.06).

**The one qualification, and it matters.** Greg Isenberg's `BUILD THE PERFECT HERMES-AGENT` (x1.68)
does show a six-card grid, and his two whiteboard-diagram thumbnails are top quartile (x1.61,
x1.45). In all three the grid or diagram is *illegible texture positioned behind a dominant face
and headline* — it is not the subject, it is evidence that a system exists. The diagram is never
read; it is counted. That is the only form in which a multi-node composition appears in a top
quartile anywhere in the set, and it depends on a creator face carrying the focal mass, which is a
lane OE does not run.

## Finding V6 — series format repeats; the rubric penalises exactly that

`unrepeatable` (10 pts) scores a concept 0 if it "could be reused on a different episode." Every
channel in the set reuses its concept on every episode by design. Modern MBA runs `THE ECONOMICS OF
___` across five of its seven top-quartile thumbnails. UpFlip runs one template with the number
swapped. MagnatesMedia runs one palette and one corrupted-mascot idea. Consistency is the
recognisability asset, and the dimension as written scores it as a defect.

The thing that must not repeat is the **subject**. The **format** should.

## What this leaves standing

Of the seven scored dimensions, the images support `curiosity` (How Money Works' verdict sentences
are the register lane's whole strategy), `subject` (one anchor, confirmed everywhere), and
`legibility` (confirmed, and it is doing more work than 8 points admits). They contradict `hero` and
`unrepeatable`, and they show `complement` failing on winners: Modern MBA's `THE ECONOMICS OF TEXAS
BBQ` shares "Texas BBQ" verbatim with its title "Why Texas BBQ Joints Rarely Survive" and would
score 0 on a 15-point dimension while sitting at x2.49.

Re-weighted in `thumbnail_spec.py` and recorded as amendment A8 in `docs/thumbnail-rubric.md`.

## Reproduce

```bash
# manifest → download → per-channel banded grids → 120px browse simulation
python3 studio/scripts/research/build_contact_grids.py --out <scratch-dir>
```
