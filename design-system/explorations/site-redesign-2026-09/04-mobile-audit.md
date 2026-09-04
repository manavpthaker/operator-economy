# Mobile audit — 2026-09-03

## Scope

Audited the live production site and the optimized local production build at 320, 375, 390, and 430 CSS-pixel widths. The representative journey covered:

- Homepage
- Business library and all filter states
- Direct Booking Recovery working paper
- Method
- A representative legacy business
- Privacy, newsletter, shared header, and shared footer
- Keyboard focus, guided-mode state, hash links, accessible names, raw server HTML, runtime logs, and Lighthouse mobile

The large display-heading direction was treated as intentional. The pass optimized the responsive shell and repeated content patterns around it rather than flattening the hierarchy.

## Production baseline

| Route | Performance | Accessibility | Best practices | SEO | FCP | LCP | CLS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | 81 | 97 | 96 | 100 | 2.1 s | 4.1 s | 0.112 |
| `/businesses/direct-booking-recovery` | 85 | 97 | 96 | 100 | 2.0 s | 4.0 s | 0 |

## Findings and resolutions

### Critical

1. **Newsletter contrast failed WCAG AA.** The heading measured 1.62:1, the label 1.72:1, and the supporting copy 4.13:1 against mineral green. The Boundary Ledger component now explicitly assigns the light paper color to the heading and the muted paper color to labels, placeholder text, and supporting copy.
2. **Full-bleed bands created horizontal overdraw.** Viewport units included the desktop scrollbar during emulation, extending decorative backgrounds beyond the page. The themed page now clips that decorative overdraw without clipping content.

### High

3. **The mobile header occupied three rows and 149 px.** Navigation and Subscribe now share the second row. The header is 97 px at 320–390 px, with every control retaining a 44 px target.
4. **The working-model image was always delivered as a 486 KB, 1536×1024 JPEG.** It now uses responsive Next Image delivery and lazy loading. The 640 px local production response is 26.7 KB, about 94.5% smaller than the source asset.
5. **Font loading shifted the homepage hero.** Critical local faces are preloaded, and Fragment Mono no longer requires a render-blocking Google Fonts stylesheet. Measured CLS is now effectively zero.
6. **Guided deep links drifted after hydration.** Revealing guide notes changed the height above the requested sheet. Guided-mode state now restores the current hash target after the layout change.

### Medium

7. **Repeated mobile sections used desktop rhythm.** Opening, section, working-paper, and chapter spacing is reduced only below 680 px. No content was removed.
8. **Method and working-paper indexes took 206 px and read as loose wraps.** They now use an explicit two-column mobile index with 44 px rows.
9. **Ledger hierarchy collapsed into long vertical stacks.** At 390 px, record name and status share a clear first row. At 320 px, they stack in reading order so long labels do not crush the record title.
10. **Filter and footer targets were undersized in one dimension.** Interactive targets now have a 44 px minimum inline size where the control is not an inline-text exception.
11. **The YouTube control's accessible name disagreed with its visible label.** The visible label now supplies the accessible name, with the new-window notice appended for assistive technology.
12. **A missing favicon produced a console error.** A Boundary Ledger favicon is now part of the app route.

## Optimized local result

| Route | Performance | Accessibility | Best practices | SEO | FCP | LCP | CLS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | 96 | 100 | 100 | 100 | 1.1 s | 2.7 s | 0.0001 |
| `/businesses/direct-booking-recovery` | 97 | 100 | 100 | 100 | 0.8 s | 2.6 s | 0.00004 |

Local and deployed network conditions differ, so the production performance numbers must be rerun after deployment. Accessibility, contrast, target sizing, layout, and state fixes are deterministic and were verified against the production build.

## Acceptance status

- 320–430 px layout: pass
- Large heading hierarchy retained: pass
- Keyboard focus visibility: pass
- Business filters and empty state: pass
- Guided toggle and URL state: pass
- Hash target restoration after guide layout changes and browser Back: pass in the local production build
- Core evidence in server-rendered HTML without JavaScript: pass
- Lighthouse contrast and accessible-name checks: pass
- Real-device Safari and VoiceOver: still required as a post-deploy spot check
