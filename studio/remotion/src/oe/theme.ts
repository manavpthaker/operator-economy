/**
 * The Operator Economy — Rev C theme constants for Remotion.
 *
 * Source of truth: /design-system/tokens/. This file mirrors the tokens that
 * every primitive/scene consumes. When the DS changes, update here — do NOT
 * inline hex codes in components.
 *
 * One rule: any single frame = Ink + Paper (or Navy) + ONE accent.
 */

export const COLORS = {
  // Core
  ink: '#1A1A1A',
  paper: '#F5F0E6',
  paperLifted: '#FBF8F1',
  paperSunken: '#EDE7D8',
  navy: '#14263E',
  draftingBlue: '#1F3A5F',

  // Ink ramp
  ink900: '#1A1A1A',
  ink700: '#3C3A36',
  ink500: '#6B675E',
  ink400: '#8A857A',
  ink300: '#B4AE9F',

  // Paper ramp
  rule: '#D8CFB9',
  ruleStrong: '#C4B99E',

  // Ledger Gold
  goldOnPaper: '#7A5E24', // gold TEXT on paper (AA 5.3:1)
  goldFill: '#B08D3E', // gold fills / chart highlight
  goldBright: '#C4A45F', // gold on navy/ink (6.4:1 on navy)
  goldTint: '#EFE6CF',

  // Sage — status only (live/verified dots, running pulses)
  sage: '#7B9E87',
  sagePaper: '#5E7F6A',

  // Negative delta
  negative: '#9B3E2E',

  // On-ink text
  onInk: '#F5F0E6',
  onInkMuted: 'rgba(245,240,230,0.62)',
  onInkFaint: 'rgba(245,240,230,0.40)',
  borderOnInk: 'rgba(245,240,230,0.16)',

  // Schematic anatomy
  schemGrid: 'rgba(245,240,230,0.055)',
  schemNodeBorder: 'rgba(245,240,230,0.30)',
  schemNodeBg: 'rgba(31,58,95,0.38)',
  schemWire: 'rgba(245,240,230,0.32)',
} as const;

export const FONTS = {
  // Boska — display ≥40px hard floor
  display: "'Boska', Georgia, 'Times New Roman', serif",
  // Zodiak — 18-44px workhorse, tracked -0.02em
  heading: "'Zodiak', Georgia, 'Times New Roman', serif",
  // Supreme — body/UI
  sans: "'Supreme', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif",
  // Fragment Mono — every number & citation, tabular, slashed zero
  mono: "'Fragment Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace",
} as const;

// Boska hard floor is 40px. Anything smaller uses Zodiak.
export const BOSKA_FLOOR = 40;

// Spacing — 4px base scale matching /design-system/tokens/spacing.css
export const SPACE = {
  s1: 4,
  s2: 8,
  s3: 12,
  s4: 16,
  s5: 24,
  s6: 32,
  s7: 48,
  s8: 64,
  s9: 96,
  s10: 128,
} as const;

// Motion — the three durations locked in the DS
// (120 / 200 / 320 ms) plus derived frame counts at 30fps.
export const DUR = {
  fast: 120,
  normal: 200,
  slow: 320,
} as const;

export const framesAt30 = (ms: number) => Math.round((ms / 1000) * 30);

// Radii — 2-3px max; corners are near-square documents, not SaaS bubbles.
export const RADIUS = {
  xs: 2,
  sm: 3,
  md: 3,
  pill: 999, // rare — status dots only
} as const;

// Type scale (px) at 1920×1080 broadcast — larger than editorial so the
// smallest labels read at Shorts crops (1080×1920) too.
export const TYPE = {
  microLabel: 20, // annotation rail labels ("SOURCE:", "SHEET 02 OF 07")
  citation: 22, // citation chip body
  small: 26,
  body: 30, // annotation-rail body lines
  bodyLg: 36, // lead / thesis paragraph
  h3: 44, // Zodiak
  h2: 60, // Zodiak or Boska (>= 40 → Boska ok)
  h1: 92, // Boska display
  displayLg: 128, // hook display figure
} as const;

// Tracking (em)
export const TRACK = {
  display: -0.01,
  heading: -0.02,
  label: 0.14, // small-caps annotation labels
  caps: 0.08, // doc numbers, sheet tags
  mono: 0.01,
} as const;
