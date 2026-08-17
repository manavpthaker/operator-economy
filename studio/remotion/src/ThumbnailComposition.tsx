import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COLORS, FONTS} from './oe/theme';
import {useEnsureFontsLoaded} from './oe/fonts';

/**
 * Thumbnail — YouTube episode thumbnail (2026-07-06). Designed for the
 * 320px-wide search/suggested tile, where the title-card frame dies:
 * ONE giant gold number, one counter-number, three words. Everything
 * else is noise at that size.
 *
 * Render: npx remotion still src/index.ts Thumbnail out/thumb.png
 *         --props=../originate/<slug>/render_data/thumbnail.json
 */

export type ThumbnailData = {
  bgImage?: string;     // photo variant: image under public/, e.g. "thumbs/ep001-people.png"
  bigLabel?: string;    // actor under the big number, e.g. "ACCENTURE"
  smallLabel?: string;  // actor under the small number, e.g. "YOU"
  rightGold?: boolean;  // split variant: gold right panel instead of paper
  variant?: 'hero' | 'numbers' | 'title' | 'versus' | 'split' | 'photo' | 'flatlay'; // hero = ONE number + interpreting text (preferred); numbers = stacked hierarchy; title = short title card; versus = equal-weight numbers + big divider
  accentColor?: string; // override goldBright (test punchier accents without leaving the family)
  big: string;          // the hero number, e.g. "$5.9B"
  small: string;        // the counter number, e.g. "$100"
  connector?: string;   // between them, e.g. "vs" | "→"
  label: string;        // ≤4 words (numbers) or the short title lines separated by \n (title)
  accentWord?: string;  // word in label to set gold
  kicker?: string;      // tiny corner mark. OFF unless set — rubric rule 1
  showMark?: boolean;   // the "OE." mark. OFF by default — rubric rules 1 and 4
  textStyle?: 'block' | 'bleed' | 'scrim'; // photo variant: solid panel (default), full-bleed caps with a hard shadow, or legacy gradient
  overline?: string;    // flatlay variant: the small tier above `big`
  groundTone?: 'light' | 'dark'; // flatlay variant: which way to key the type against the photograph
  logos?: {file: string; hex?: string; name?: string}[]; // photo variant: the episode's stack, as a SUPPORTING row. Never the subject — see LogoStrip.
  // flatlay variant: where the marks land, as fractions of the frame, with
  // scale and rotation. Tune per ground — the default fits an overhead surface
  // and will drop marks onto the subject at eye level. See SCATTER.
  // `ar` is the mark's width/height. Square glyph marks (Simple Icons) default
  // to 1; a WORDMARK is wide — Accenture's is 163x43 — and rendering one inside
  // a square chip shrinks it to a sliver of padding, which defeats the reason
  // for using a wordmark at all: the glyph alone is an unrecognisable chevron,
  // the word is the recognisable thing.
  // `plate: false` drops the paper chip and sets the mark straight onto the
  // photograph. The chip is right for a glyph that needs a ground to sit on;
  // on a wordmark it reads as a sticker applied afterwards, which is the
  // losing form — brand as vector chip rather than brand as object in the
  // scene. Without it the mark needs its own separation, so it gets a shadow.
  scatter?: ScatterMark[];
};

// Rule 1 bans a kicker, a channel mark and an episode number on a thumbnail:
// the channel name already renders next to the title, so branding spends
// curiosity space on information the viewer has. Rule 4 additionally reserves
// the lower-right for YouTube's duration stamp. Until 2026-08-10 every variant
// except `photo` hardcoded an "OE." mark into that exact corner and defaulted
// the kicker to "OPERATOR BLUEPRINT · № 001" — a wrong episode number for every
// episode after the first. Both are now opt-in and off by default.

/**
 * Hero — ONE number, plus text that interprets it. Added 2026-08-10.
 *
 * Every previous variant puts two numbers on the canvas and asks the viewer
 * to compare them ($5.9B vs $2K, $11B vs $500, 850 vs 1). A comparison costs
 * time nobody spends at feed size, and the whole back catalogue does it.
 * One figure owning the frame is the rule both current thumbnail rubrics
 * converge on.
 *
 * The label INTERPRETS rather than names: "GO TO VOICEMAIL", not "ELEVENLABS".
 * A bare label makes the viewer supply the meaning; interpretation hands it
 * to them.
 *
 * Type is FONTS.sans at 800 because rule 2 says so and, until now, no text
 * variant honoured it: split and title used the Didone the rubric explicitly
 * warns "fails the thin-stroke test at 168px-wide tiles".
 */
const HeroVariant: React.FC<ThumbnailData> = (p) => {
  // Scale to the digit count so a short figure still owns the frame. "$2K"
  // at a fixed size left half the canvas dead; the rubrics want the number
  // at roughly 35-50% of the frame regardless of how many characters it has.
  const n = (p.big ?? '').length;
  const heroSize = n <= 3 ? 460 : n === 4 ? 400 : n === 5 ? 350 : 300;
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: 88, paddingRight: 88, paddingBottom: 36}}>
      <div
        style={{
          fontFamily: FONTS.sans,
          fontWeight: 800,
          fontSize: heroSize,
          lineHeight: 0.88,
          letterSpacing: '-0.035em',
          color: p.accentColor ?? COLORS.goldBright,
          textShadow: '0 8px 70px rgba(0,0,0,0.5)',
        }}
      >
        {p.big}
      </div>
      {p.label ? (
        <div
          style={{
            fontFamily: FONTS.sans,
            fontWeight: 800,
            fontSize: 92,
            letterSpacing: '0.01em',
            lineHeight: 1.04,
            color: COLORS.paper,
            marginTop: 20,
            whiteSpace: 'nowrap', // a wrapped label reads as two ideas; keep it to 2-3 words
          }}
        >
          {p.label}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

/**
 * Photo — text over a photograph.
 *
 * `textStyle` decides how the type separates from the picture:
 *
 *   'block'  (default) solid panel behind the text. Separation is guaranteed
 *            regardless of what the photograph does underneath.
 *   'scrim'  the original soft gradient. Legacy.
 *
 * The gradient was fine over an empty navy card and fails over a real
 * photograph: a soft ramp cannot guarantee contrast against a face, a window
 * or a pale wall, so the type sits ON the picture instead of IN it. Every
 * text-bearing tile in a live YouTube feed uses a hard edge — a solid colour
 * block or a heavy outline — and not one relies on a gradient.
 */
/**
 * `big` was sized at a flat 168px because it only ever held a short figure
 * ($4,995, $11B). Amendment A8 retired the hero number on measured evidence,
 * so `big` now usually holds a verdict — THEY DON'T CALL BACK, THE ROOM ISN'T
 * EMPTY — and four words at 168px wrap to three lines and run off the frame.
 *
 * The ramp keeps a lone figure as large as it ever was and steps a sentence
 * down to something that still fills the block. Sizes chosen so the smallest
 * step, 76px, is ~10.5% of frame height and clears the 120px shrink test with
 * room to spare.
 */
const bigFontSize = (text: string): number => {
  const n = (text ?? '').length;
  if (n <= 6) return 200;   // a figure
  if (n <= 12) return 168;
  if (n <= 18) return 140;
  if (n <= 26) return 118;
  return 96;
};

/**
 * The stack, as a supporting row inside the text block.
 *
 * The measured distinction is narrow and this component encodes it. A logo
 * COLLAGE AS THE SUBJECT loses: five such thumbnails in the comp set, five in
 * the bottom quartile, none in any top. Marks as a SUPPORTING layer under a
 * dominant subject win: MagnatesMedia's whole top quartile, and Greg Isenberg's
 * LOCAL AI IS TAKING OVER at 1.80x its channel median.
 *
 * So the row is capped at four, sits below the headline rather than beside it,
 * and is sized to roughly a fifth of the headline's cap height. If it ever
 * competes with the subject for the eye, it is wrong.
 *
 * Marks whose brand colour is too dark to read against the navy block are
 * flipped to paper. Simple Icons hands back #000000 for ElevenLabs, Next.js
 * and Resend, which would otherwise composite to an invisible square.
 */
const LogoStrip: React.FC<{logos: NonNullable<ThumbnailData['logos']>; size: number; onPhoto?: boolean}> = ({logos, size, onPhoto}) => {
  const tooDark = (hex?: string) => {
    if (!hex) return true;
    const h = hex.replace('#', '');
    if (h.length !== 6) return true;
    const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) < 70;   // vs COLORS.navy
  };
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: size * 0.42, marginTop: size * 0.5}}>
      {logos.slice(0, 4).map((l) => (
        <div
          key={l.file}
          style={{
            width: size, height: size,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            // A dark mark gets a paper disc rather than a recolour, so the
            // brand's own colour survives wherever it legibly can.
            background: onPhoto || tooDark(l.hex) ? COLORS.paper : 'transparent',
            borderRadius: onPhoto || tooDark(l.hex) ? size * 0.22 : 0,
            padding: onPhoto || tooDark(l.hex) ? size * 0.16 : 0,
            boxShadow: onPhoto ? '0 4px 18px rgba(0,0,0,0.55)' : 'none',
            boxSizing: 'border-box',
          }}
        >
          <Img src={staticFile(l.file)} style={{width: '100%', height: '100%', objectFit: 'contain'}} />
        </div>
      ))}
    </div>
  );
};

/**
 * `bleed` — type straight onto the photograph with a hard shadow, no panel.
 *
 * The block was introduced because a soft gradient scrim cannot guarantee
 * contrast against a face or a window, which was correct. But a block large
 * enough to hold a four-word verdict at the size the comp set sets type covers
 * most of the frame, and then the photograph it sits on is decorative. How
 * Money Works — the closest channel to this register, and the one whose entire
 * top quartile is verdict-over-photo — uses neither: white condensed caps
 * straight over the picture, hard shadow, spanning nearly the full width.
 *
 * So this is the third option rather than a replacement. `block` still wins on
 * a busy or pale ground where nothing can be guaranteed; `bleed` wins wherever
 * the ground has a quiet zone, which the generator is now explicitly asked to
 * leave.
 */
const PhotoVariant: React.FC<ThumbnailData> = (p) => {
  const style = p.textStyle ?? 'block';
  const block = style === 'block';
  const bleed = style === 'bleed';
  const bigSize = bigFontSize(p.big ?? '');
  // A hard offset shadow plus a tight dark halo. Two shadows, not a blur: a
  // blur alone goes muddy at 120px, which is the width that decides it.
  const hardShadow =
    '0 6px 0 rgba(0,0,0,0.65), 0 0 26px rgba(0,0,0,0.85), 0 2px 4px rgba(0,0,0,0.9)';
  return (
    <AbsoluteFill>
      {p.bgImage ? (
        <Img src={staticFile(p.bgImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      ) : null}
      {!block ? (
        <AbsoluteFill style={{background: 'linear-gradient(to top, rgba(10,18,32,0.85) 0%, rgba(10,18,32,0.3) 34%, rgba(10,18,32,0) 55%)'}} />
      ) : null}
      {/* ONE text block, bottom-left (lower-right = duration stamp).
          Supreme 800: thick sans survives the 168px shrink test. NO kicker,
          NO mark — branding on a thumbnail is wasted curiosity space (rule 1). */}
      <div
        style={{
          position: 'absolute',
          bottom: block ? 0 : bleed ? 34 : 40,
          left: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          padding: block ? '30px 44px 34px 52px' : '0 0 0 48px',
          background: block ? COLORS.navy : 'transparent',
          borderTop: block ? `6px solid ${COLORS.goldBright}` : 'none',
          maxWidth: block ? (bigSize <= 140 ? '86%' : '68%') : '92%',
        }}
      >
        <span style={{fontFamily: FONTS.sans, fontWeight: 800, fontSize: bigSize, lineHeight: 0.95, letterSpacing: '-0.02em', color: bleed ? COLORS.paper : COLORS.goldBright, textShadow: block ? 'none' : hardShadow}}>{p.big}</span>
        {p.bigLabel ? (
          <span style={{fontFamily: FONTS.sans, fontWeight: 800, fontSize: 58, letterSpacing: '0.04em', color: bleed ? COLORS.goldBright : COLORS.paper, marginTop: 6, textShadow: block ? 'none' : hardShadow}}>{p.bigLabel}</span>
        ) : null}
        {p.logos && p.logos.length > 0 ? (
          <LogoStrip logos={p.logos} size={Math.round(bigSize * 0.60)} onPhoto={!block} />
        ) : null}
      </div>
      {p.small ? (
        <div style={{position: 'absolute', top: 40, right: 52, display: 'flex', flexDirection: 'column', alignItems: 'flex-end'}}>
          <span style={{fontFamily: FONTS.sans, fontWeight: 800, fontSize: 84, lineHeight: 1, color: COLORS.paper, textShadow: '0 2px 0 rgba(0,0,0,0.55), 0 4px 30px rgba(0,0,0,0.9)'}}>{p.small}</span>
          {p.smallLabel ? (
            <span style={{fontFamily: FONTS.sans, fontWeight: 800, fontSize: 40, letterSpacing: '0.08em', color: COLORS.goldBright, marginTop: 6, textShadow: '0 2px 0 rgba(0,0,0,0.55)'}}>{p.smallLabel}</span>
          ) : null}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};


/**
 * Flatlay — copied structurally from Modern MBA's THE ECONOMICS OF COOKIES,
 * 8.21x its channel median and the highest multiple anywhere in the register
 * lane. Copied on purpose rather than reasoned from principles, because four
 * rounds of reasoning produced single objects centred in empty rooms and
 * nothing in the 78-image comp set looks remotely like that.
 *
 * What the original does, and what this reproduces:
 *
 *   - type CENTRED and OVERLAPPING the objects, not sitting in reserved space
 *   - two tiers, the second several times the first
 *   - heavy outline plus offset shadow, so it survives any ground underneath
 *   - the whole block rotated a couple of degrees; nothing is squared up
 *   - branded packets SCATTERED among the real objects at different sizes and
 *     angles, never a row
 *
 * That last point is the one worth stating plainly, because the previous
 * attempt got it exactly backwards: a tidy row of equal marks reads as a logo
 * collage, which is 5 for 5 bottom quartile in the comp set. Scattered at
 * varied scale and rotation they read as objects on the desk, which is what
 * Mrs Fields and Famous Amos are doing in the original.
 *
 * Positions are fractions of the frame and are tuned to the generated ground's
 * bare patches. A different ground needs different numbers — they are data, not
 * layout logic, which is why they sit here rather than being computed.
 */
// One composited mark. `ar` is the aspect ratio for wordmarks wider than they
// are tall; `plate: false` drops the paper plate so the mark sits straight on
// the surface. Both were already read below via `?? 1` and `=== false` but had
// no home in the type, so no caller could pass them.
type ScatterMark = {
  x: number; y: number; s: number; r: number;
  ar?: number; plate?: boolean;
};

const SCATTER: ScatterMark[] = [
  {x: 0.150, y: 0.580, s: 1.00, r: -14},
  {x: 0.830, y: 0.470, s: 0.78, r: 13},
  {x: 0.660, y: 0.520, s: 0.92, r: -7},
  {x: 0.885, y: 0.720, s: 0.62, r: 19},
  {x: 0.300, y: 0.865, s: 0.70, r: -21},
];
// These are the OVERHEAD ground's bare patches. Once the camera became a free
// axis they stopped being a default that fits every frame: at eye level the
// dead zones move — the subject is usually centre or one third, the surface
// runs as a band rather than filling the frame — so a fixed set drops marks
// onto faces. `scatter` in the props overrides per ground, which is what the
// paragraph above means by "they are data, not layout logic".
// Spread to the corners rather than clustered, scale range widened to 0.62-1.00,
// rotation to +/-21. The first pass put three marks in one quadrant at similar
// sizes, which reads as a row however much each one is rotated — and a row is
// the 5-for-5 bottom-quartile pattern. In the original the packets overlap the
// cookies and the marble and each other; they are objects on the surface, not a
// legend, so they are allowed to sit on top of things.
//
// The two dead zones are the type at top-centre and the hands at bottom-centre.
// Everything else is fair ground.

const FlatlayVariant: React.FC<ThumbnailData> = (p) => {
  // Theme rule is ink + paper (or navy) + ONE accent per frame. Which of ink
  // and paper carries the fill depends on the ground: cream type vanishes on a
  // cream drafting table, navy type vanishes on dark wood. The stroke always
  // takes the opposite, which is also what separates a navy headline from the
  // navy diagram lines underneath it.
  const light = (p.groundTone ?? 'dark') === 'light';
  const fill = light ? COLORS.navy : COLORS.paper;
  const stroke = light ? COLORS.paper : COLORS.ink;
  // Cream fill, ink outline, gold offset — theme rule is ink + paper + ONE
  // accent per frame, and the accent is the offset rather than the fill because
  // gold on warm wood has nothing to separate it from the ground.
  const outline = (w: number) => ({
    WebkitTextStrokeWidth: `${w}px`,
    WebkitTextStrokeColor: stroke,
    paintOrder: 'stroke fill' as const,
  });
  return (
    <AbsoluteFill>
      {p.bgImage ? (
        <Img src={staticFile(p.bgImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      ) : null}

      {p.logos?.slice(0, (p.scatter ?? SCATTER).length).map((l, i) => {
        const c = (p.scatter ?? SCATTER)[i];
        // 172 made the chips outrank the headline at 120px: bright white squares
        // on a mid-tone photograph read before navy type does. V5 is explicit
        // that marks survive as subordinate texture and die as the subject, so
        // the base drops to 132 and the type keeps the focal mass.
        const size = Math.round(132 * c.s);
        const chipW = Math.round(size * (c.ar ?? 1));
        return (
          <div
            key={l.file}
            style={{
              position: 'absolute',
              left: `${c.x * 100}%`, top: `${c.y * 100}%`,
              width: chipW, height: size,
              transform: `translate(-50%, -50%) rotate(${c.r}deg)`,
              ...(c.plate === false
                ? {filter: 'drop-shadow(0 4px 10px rgba(0,0,0,0.55)) drop-shadow(0 1px 2px rgba(0,0,0,0.6))'}
                : {
                    background: COLORS.paper,
                    borderRadius: size * 0.16,
                    padding: size * 0.17,
                    boxSizing: 'border-box' as const,
                    boxShadow: '0 10px 26px rgba(0,0,0,0.45), 0 2px 0 rgba(0,0,0,0.3)',
                  }),
            }}
          >
            <Img src={staticFile(l.file)} style={{width: '100%', height: '100%', objectFit: 'contain'}} />
          </div>
        );
      })}

      <div
        style={{
          position: 'absolute', top: 28, left: 0, right: 0,
          display: 'flex', flexDirection: 'column', alignItems: 'center',
          transform: 'rotate(-2deg)', maxWidth: '94%', textAlign: 'center',
        }}
      >
        {p.overline ? (
          <span style={{
            fontFamily: FONTS.sans, fontWeight: 800, fontSize: 76,
            // Was goldOnPaper on light grounds. That is a paper colour and it
            // disappeared on a bright PHOTOGRAPH — 'STILL RUNNING', 'QUIETLY'
            // and 'THE BUSINESS OF' were all gone by 120px. Navy is the same
            // ink as `big`, so the two tiers read as one mass; the gold stays
            // as the offset, which is where it has contrast to spend.
            letterSpacing: '0.02em', color: light ? COLORS.navy : COLORS.paper,
            textShadow: `0 5px 0 ${light ? COLORS.navy : COLORS.goldFill}, 0 8px 0 rgba(0,0,0,0.45), 0 14px 30px rgba(0,0,0,0.4)`,
            ...outline(10),
          }}>{p.overline}</span>
        ) : null}
        <span style={{
          fontFamily: FONTS.sans, fontWeight: 800,
          // Same length ramp the photo variant uses, scaled up because a
          // flat-lay headline is the whole composition. Fixed at 196 it was
          // fine for BORING and ran clean off the frame on SHIPPED WITHOUT AN
          // ENGINEER.
          fontSize: Math.round(bigFontSize(p.big ?? '') * 1.10), lineHeight: 0.9,
          letterSpacing: '-0.03em', color: fill, marginTop: -6,
          textShadow: `0 10px 0 ${COLORS.goldFill}, 0 15px 0 rgba(0,0,0,0.55), 0 24px 46px rgba(0,0,0,0.45)`,
          ...outline(14),
        }}>{p.big}</span>
      </div>
    </AbsoluteFill>
  );
};

const SplitVariant: React.FC<ThumbnailData> = (p) => {
  const rightBg = p.rightGold ? COLORS.goldFill : COLORS.paper;
  return (
    <AbsoluteFill style={{flexDirection: 'row'}}>
      {/* LEFT: navy — the corporate number */}
      <div style={{flex: 11, background: COLORS.navy, display: 'flex', flexDirection: 'column', justifyContent: 'center', paddingLeft: 64, position: 'relative'}}>
        <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(rgba(245,240,230,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(245,240,230,0.05) 1px, transparent 1px)', backgroundSize: '64px 64px'}} />
        {p.kicker ? (
          <div style={{position: 'absolute', top: 40, left: 64, fontFamily: FONTS.mono, fontSize: 24, letterSpacing: '0.16em', color: 'rgba(245,240,230,0.55)'}}>
            {p.kicker}
          </div>
        ) : null}
        <div style={{fontFamily: FONTS.display, fontWeight: 700, fontSize: 250, lineHeight: 1, color: COLORS.goldBright, textShadow: '0 8px 70px rgba(0,0,0,0.5)'}}>
          {p.big}
        </div>
        <div style={{fontFamily: FONTS.mono, fontSize: 40, letterSpacing: '0.18em', color: COLORS.paper, marginTop: 22}}>
          {p.bigLabel ?? 'ACCENTURE'}
        </div>
      </div>
      {/* RIGHT: paper (or gold) — your number */}
      <div style={{flex: 7, background: rightBg, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative'}}>
        <div style={{fontFamily: FONTS.display, fontWeight: 700, fontSize: 190, lineHeight: 1, color: COLORS.navy}}>
          {p.small}
        </div>
        <div style={{fontFamily: FONTS.mono, fontSize: 40, letterSpacing: '0.24em', color: COLORS.navy, marginTop: 22}}>
          {p.smallLabel ?? 'YOU'}
        </div>
        {p.showMark ? (
          <div style={{position: 'absolute', bottom: 36, right: 44, fontFamily: FONTS.display, fontWeight: 700, fontSize: 48, color: COLORS.navy}}>OE.</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

const VersusVariant: React.FC<ThumbnailData> = (p) => {
  const gold = p.accentColor ?? COLORS.goldBright;
  return (
    <>
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 56,
          right: 56,
          bottom: 170,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 24,
        }}
      >
        <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 210, letterSpacing: '-0.04em', color: gold, textShadow: '0 6px 60px rgba(0,0,0,0.45)'}}>
          {p.big}
        </span>
        <span style={{fontFamily: FONTS.display, fontWeight: 700, fontStyle: 'italic', fontSize: 110, color: 'rgba(245,240,230,0.85)'}}>
          {p.connector ?? 'vs'}
        </span>
        <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 210, letterSpacing: '-0.04em', color: COLORS.paper, textShadow: '0 6px 60px rgba(0,0,0,0.45)'}}>
          {p.small}
        </span>
      </div>
      {p.label ? (
        <div
          style={{
            position: 'absolute',
            left: 56,
            right: 56,
            bottom: 48,
            borderTop: '2px solid rgba(245,240,230,0.25)',
            paddingTop: 24,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'baseline',
          }}
        >
          <span style={{fontFamily: FONTS.display, fontWeight: 600, fontSize: 74, color: COLORS.paper}}>
            {p.accentWord && p.label.includes(p.accentWord) ? (
              <>
                {p.label.split(p.accentWord)[0]}
                <span style={{color: gold}}>{p.accentWord}</span>
                {p.label.split(p.accentWord)[1]}
              </>
            ) : p.label}
          </span>
          {p.showMark ? (
            <span style={{fontFamily: FONTS.display, fontWeight: 700, fontSize: 52, color: gold}}>OE.</span>
          ) : null}
        </div>
      ) : p.showMark ? (
        <div style={{position: 'absolute', right: 56, bottom: 48, fontFamily: FONTS.display, fontWeight: 700, fontSize: 52, color: gold}}>OE.</div>
      ) : null}
    </>
  );
};

const TitleVariant: React.FC<ThumbnailData> = (p) => {
  const lines = p.label.split('\\n');
  return (
    <>
      <div
        style={{
          position: 'absolute',
          top: 110,
          left: 64,
          right: 64,
          fontFamily: FONTS.display,
          fontWeight: 700,
          fontSize: 150,
          lineHeight: 1.02,
          color: COLORS.paper,
          letterSpacing: '-0.01em',
          textShadow: '0 6px 60px rgba(0,0,0,0.4)',
        }}
      >
        {lines.map((ln, i) => (
          <div key={i}>
            {p.accentWord && ln.includes(p.accentWord) ? (
              <>
                {ln.split(p.accentWord)[0]}
                <span style={{color: COLORS.goldBright}}>{p.accentWord}</span>
                {ln.split(p.accentWord)[1]}
              </>
            ) : (
              ln
            )}
          </div>
        ))}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 64,
          right: 64,
          bottom: 52,
          borderTop: '2px solid rgba(245,240,230,0.25)',
          paddingTop: 24,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
        }}
      >
        <div style={{display: 'flex', alignItems: 'baseline', gap: 28}}>
          <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 92, color: COLORS.goldBright}}>
            {p.big}
          </span>
          <span style={{fontFamily: FONTS.display, fontStyle: 'italic', fontSize: 48, color: 'rgba(245,240,230,0.6)'}}>
            {p.connector ?? 'vs'}
          </span>
          <span style={{fontFamily: FONTS.mono, fontWeight: 700, fontSize: 92, color: COLORS.paper}}>
            {p.small}
          </span>
        </div>
        {p.showMark ? (
          <div style={{fontFamily: FONTS.display, fontWeight: 700, fontSize: 52, color: COLORS.goldBright}}>OE.</div>
        ) : null}
      </div>
    </>
  );
};

export const Thumbnail: React.FC<ThumbnailData> = (p) => {
  useEnsureFontsLoaded();
  const labelParts = p.accentWord && p.label.includes(p.accentWord)
    ? p.label.split(p.accentWord)
    : null;

  return (
    <AbsoluteFill style={{background: COLORS.navy, overflow: 'hidden'}}>
      {/* faint grid + a huge soft gold glow behind the hero number for
          small-size contrast pop */}
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(245,240,230,0.05) 1px, transparent 1px),' +
            'linear-gradient(90deg, rgba(245,240,230,0.05) 1px, transparent 1px)',
          backgroundSize: '64px 64px',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -140,
          top: -180,
          width: 900,
          height: 900,
          background: 'radial-gradient(circle, rgba(176,141,62,0.28) 0%, rgba(176,141,62,0) 62%)',
        }}
      />

      {/* kicker — opt-in only (rule 1) */}
      {p.kicker && p.variant !== 'split' && p.variant !== 'photo' && (
      <div
        style={{
          position: 'absolute',
          top: 44,
          left: 56,
          fontFamily: FONTS.mono,
          fontSize: 26,
          letterSpacing: '0.16em',
          color: 'rgba(245,240,230,0.55)',
        }}
      >
        {p.kicker}
      </div>
      )}

      {p.variant === 'hero' ? <HeroVariant {...p} /> : null}
      {p.variant === 'title' ? <TitleVariant {...p} /> : null}
      {p.variant === 'versus' ? <VersusVariant {...p} /> : null}
      {p.variant === 'split' ? <SplitVariant {...p} /> : null}
      {p.variant === 'photo' ? <PhotoVariant {...p} /> : null}
      {p.variant === 'flatlay' ? <FlatlayVariant {...p} /> : null}

      {/* the number stack */}
      {(!p.variant || p.variant === 'numbers') && (
      <div
        style={{
          position: 'absolute',
          top: 96,
          left: 56,
          right: 56,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontWeight: 700,
            fontSize: 300,
            lineHeight: 0.95,
            color: p.accentColor ?? COLORS.goldBright,
            letterSpacing: '-0.03em',
            textShadow: '0 6px 60px rgba(0,0,0,0.45)',
          }}
        >
          {p.big}
        </div>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 34, marginTop: 8}}>
          <span
            style={{
              fontFamily: FONTS.display,
              fontStyle: 'italic',
              fontSize: 70,
              color: 'rgba(245,240,230,0.6)',
            }}
          >
            {p.connector ?? 'vs'}
          </span>
          <span
            style={{
              fontFamily: FONTS.mono,
              fontWeight: 700,
              fontSize: 190,
              lineHeight: 1,
              color: COLORS.paper,
              letterSpacing: '-0.02em',
            }}
          >
            {p.small}
          </span>
        </div>
      </div>

      )}

      {/* label band — bottom, full width, paper on navy via a hairline */}
      {(!p.variant || p.variant === 'numbers') && (
      <div
        style={{
          position: 'absolute',
          left: 56,
          right: 56,
          bottom: 48,
          borderTop: '2px solid rgba(245,240,230,0.25)',
          paddingTop: 26,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
        }}
      >
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 600,
            fontSize: 84,
            lineHeight: 1,
            color: COLORS.paper,
          }}
        >
          {labelParts ? (
            <>
              {labelParts[0]}
              <span style={{color: COLORS.goldBright}}>{p.accentWord}</span>
              {labelParts[1]}
            </>
          ) : (
            p.label
          )}
        </div>
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 700,
            fontSize: 56,
            color: COLORS.goldBright,
          }}
        >
          OE.
        </div>
      </div>
      )}
    </AbsoluteFill>
  );
};
