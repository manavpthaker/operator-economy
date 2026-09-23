# R74 S26 — verified legacy end-screen reference

The actual EP001 and EP002 final exports use the same six-second navy-grid end card. It contains a large tagline, website, download invitation, subscription invitation and small typeset brand footer. It does **not** contain a separate logo graphic. The rendered reference, rather than the latest theme defaults, should guide the requested legacy match.

## Exact rendered copy

Top to bottom:

1. **Build. Own. Operate.**
2. **THEOPERATORECONOMY.COM**
3. **Get the Operator Blueprint — free, link in the description**
4. **One business blueprint every week — subscribe**
5. **THE OPERATOR ECONOMY**

The domain has no visible https:// prefix or download-path suffix. The card points to the homepage and separately says the free blueprint link is in the description. These references do not establish an EP007-specific download URL, a live downloadable EP007 artifact, or a current weekly schedule. Root is separately checking the current site and should not carry the historical weekly-cadence claim into EP007 without authority.

## Actual rendered reference

Owned reference image: `qa/ep001-final-card-566s.png`, decoded from EP001 at 566.0 s and personally inspected at native 1920×1080. Its SHA is `89a4a71649297de897999de8cc4c57830906e24b8e62b2420a0c003cc34c6ea2`. This QA path is ignored by Git.

The frame shows a large cream high-contrast serif heading, gold monospaced uppercase domain, gray CTA rows preceded by short thin horizontal rules, and a small uppercase monospaced text footer. Everything is left aligned, with the content beginning around x=200 px, about 10.4% of the width. The group is centered vertically; the right half is largely empty for platform end-screen overlays. A fine square grid covers the navy background. There is no QR code, button, subscription confirmation, bell, icon logo or download-path text.

The independent read-only child audit also inspected EP001 at 561.0/566.0 s and EP002 at 745.0/750.2 s, plus quarter-second samples of EP001's entry. The settled final cards match. Both exports are 1920×1080 at 30 fps. Their relationship to a published upload was not established.

## Timing: rendered evidence and source intent

| Rendered reference | End-card start | Video end | End-card duration |
|---|---:|---:|---:|
| EP001 `ep001-final.mp4` | 560.200 s | 566.200 s | 6.000 s |
| EP002 `ep002-final.mp4` | 744.433333 s | 750.433333 s | 6.000 s |

The rendered sequence reveals the heading, domain, first CTA, second CTA and footer in that order. All text is visibly present by approximately 1.5 s into the sampled outro, leaving approximately 4.5 s with the complete card visible. The final inspected frames retain the card without a fade to black.

Current `OutroCard` code specifies these entrance intervals at 30 fps: headline frames 0–12, URL 10–22, first CTA 20–32, second CTA 28–40, footer 40–52. The source therefore reaches full footer opacity at 1.733333 s, leaving 4.266667 s fully settled in a six-second outro. This is source intent, distinct from the sampled rendered visibility estimate above. The episode props specify six outro seconds and a 2.5-second L-cut over the narration tail. Reuse of that L-cut or cadence in EP007 is not required by this reference audit; root owns the current locked narration and edit.

## Source implementation and logo identity

The source is `studio/remotion/src/oe/scenes/Bookends.tsx`, `OutroCard` at line 237. `BlueprintComposition.tsx` calculates the outro placement around lines 1154–1171 and passes brand/tagline/domain/CTA props at lines 1298–1307. The EP001, EP002 and direct-booking-recovery blueprint JSON files all contain the exact same five strings through `/bookends/brand` and `/bookends/ctas`.

`OutroCard` references no logo image. Its identity is typeset from the tagline and brand props. `LogoScene.tsx` is an unrelated company-evidence card component, not a logo asset used by this outro. If EP007 includes an additional separate logo at the user's request, that is a current brand-asset choice rather than a claim that this reference contained one.

Current `theme.ts` supplies navy #14263E, paper #F5F0E6, gold #C4A45F, muted text rgba(245,240,230,0.62), and grid rgba(245,240,230,0.055). The grid period is 36 px. Source sizes at 1920×1080 are 96 px heading, 40 px URL, 32 px CTA and 20 px footer; the content uses 200 px horizontal padding, 44 px major gaps and 20 px CTA-row gaps.

There is a material source/render difference: current theme.ts resolves FONTS.display to Supreme sans, while the inspected legacy exports visibly use a serif headline. Do not claim that rendering the current source verbatim would reproduce the old card. The rendered image is the appearance reference; the exact historical font file/commit that generated those MP4s was not established.

## Handoff limits

All source, props, video and reference-image hashes are in deliverable.json. This investigation did not edit the legacy sources, inspect a live website, prove current offer availability or cadence, alter episode approval, or invoke any paid provider. Only findings and the reference image in the assigned deliverable directory were written. New production remains root's HyperFrames work; the legacy Remotion files are reference evidence.
