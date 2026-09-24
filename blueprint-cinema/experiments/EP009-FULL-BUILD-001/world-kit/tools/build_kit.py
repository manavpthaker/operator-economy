#!/usr/bin/env python3
"""Build world-kit/kit.svg for EP009.

Authored geometry, fixed at build time. Repeated parts (windows, box sides) take small seeded
endpoint offsets and open corners so no two strokes are identical; nothing moves at render time.
Figure and table geometry are copied verbatim from EP007 accepted scenes (R54 S11b, R57 S13ab,
R60 S15 part 1). Run: python3 tools/build_kit.py  (writes ../kit.svg)
"""
import random
from pathlib import Path

INK = "#173530"
STEEL = "#586D74"
MUTED = "#33464C"
PAPER = "#F5F0E6"
SHEET = "#FBF8F1"
CARD = "#EDE5D6"
FONT = "Supreme, sans-serif"

OUT = Path(__file__).resolve().parent.parent / "kit.svg"


def n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def P(d, stroke=INK, w=3.0, fill="none", extra=""):
    return (f'<path d="{d}" stroke="{stroke}" stroke-width="{n(w)}" fill="{fill}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def F(d, fill=SHEET, op=None):
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<path d="{d}" fill="{fill}"{o} stroke="none"/>'


def T(x, y, text, size=22, weight=400, fill=MUTED, anchor="start", tid=None, extra=""):
    i = f' id="{tid}"' if tid else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text{i} x="{n(x)}" y="{n(y)}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{a}{extra}>{text}</text>')


class Hand:
    """Seeded construction helper: short partial strokes, open corners, unequal retraces."""

    def __init__(self, seed):
        self.r = random.Random(seed)

    def j(self, a=1.0):
        return self.r.uniform(-a, a)

    def line(self, x1, y1, x2, y2, brk=False, a=1.0, gap=(6, 11)):
        x1 += self.j(a); y1 += self.j(a); x2 += self.j(a); y2 += self.j(a)
        if not brk:
            return f"M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}"
        t = self.r.uniform(.38, .62)
        L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5 or 1
        g = self.r.uniform(*gap) / L / 2
        ax, ay = x1 + (x2 - x1) * (t - g), y1 + (y2 - y1) * (t - g)
        bx, by = x1 + (x2 - x1) * (t + g), y1 + (y2 - y1) * (t + g) + self.j(.8)
        return f"M{n(x1)} {n(y1)}L{n(ax)} {n(ay)}M{n(bx)} {n(by)}L{n(x2)} {n(y2)}"

    def rect(self, x, y, w, h, a=.9, brk_side=None, corner=(-2.5, 3.0)):
        """Four separate sides; corners overshoot or stop short."""
        c = lambda: self.r.uniform(*corner)
        sides = [
            (x - c(), y, x + w - c(), y),
            (x + w, y + c(), x + w, y + h - c()),
            (x + w + c() * .5, y + h, x + c(), y + h),
            (x, y + h - c(), x, y + c() + 1),
        ]
        out = []
        for i, s in enumerate(sides):
            out.append(self.line(*s, brk=(brk_side == i), a=a))
        return "".join(out)


def g(gid, body, desc):
    return f'<g id="{gid}" data-kit-desc="{desc}">\n{body}\n</g>'


# ---------------------------------------------------------------- figures (EP007 verbatim)
PERSON_INK = ("M-25-51C-39-78-27-103-4-105C22-108 37-87 27-64C23-52 14-43 0-43C-12-42-20-46-25-51"
              "M-58 33L-55-5C-47-29-27-31-20-33M18-33C45-34 59-14 61 17L61 32M-36 5L-36 33M36 3L36 31")
PERSON_LIGHT = "M-29-85C-19-108 11-112 28-94M-60 39L-13 39M22 39L64 39"


def person():
    return g("kit-person", P(PERSON_INK, INK, 3) + "\n" + P(PERSON_LIGHT, STEEL, 1.3),
             "Generic person. Verbatim EP007 R54/R57/R60 #person geometry.")


def guest():
    # Same figure; the only added mark is a small daypack behind his left shoulder (viewer right)
    # with one strap across the shoulder. Proportions untouched.
    pack = P("M60-25C67-33 80-31 82-19L83 15C83 22 78 25 70 24M63 24L62 20", INK, 2.4)
    strap = P("M24-34C30-24 32-12 31 1", INK, 2.2)
    retr = P("M66-27C74-29 79-24 79-15M72 1L80 1", STEEL, 1.1)
    return g("kit-guest", '<use href="#kit-person"/>\n' + pack + strap + retr,
             "The guest: kit-person plus the daypack mark. No other figure carries a daypack.")


def innkeeper():
    # Same figure; the only added mark is the open V of a cardigan inside the torso outline
    # (the filmed innkeeper wears an olive cardigan). The silhouette does not change.
    collar = P("M-18-31L-4-9M17-31L3-9", INK, 2)
    retr = P("M-12-30L-3-16", STEEL, 1.1)
    return g("kit-innkeeper", '<use href="#kit-person"/>\n' + collar + retr,
             "The innkeeper: kit-person plus the open V of her cardigan. Silhouette and proportions unchanged.")


def practice_figure():
    # The practice / You: same figure holding the EP007 practice card at its side.
    card = (F("M46-8L76-10L77 30L47 31Z", CARD)
            + P("M46-8L75-10M77-7L77 29M74 31L47 31M46 28L46-5", INK, 2.4)
            + P("M52 2L70 1M52 10L70 10M52 18L64 18", STEEL, 1.1))
    return g("kit-practice-figure", '<use href="#kit-person"/>\n' + card,
             "The practice figure (A direct-booking practice / You): kit-person holding the EP007 practice card. Not the presenter's likeness.")


def table():
    return g("kit-table", P("m0 0 118-1m10 1 112-1m-230 10 1 58m222-59-1 57", INK, 3),
             "Small table. Verbatim EP007 R54 S11b table. Origin at left end of the top.")


def desk():
    h = Hand(11)
    top = P("m0 0 118-1m10 1 112-1", INK, 3)
    sides = P(h.line(8, 9, 9, 92) + h.line(233, 8, 232, 91), INK, 2.8)
    base = P(h.line(6, 96, 116, 95) + h.line(128, 96, 236, 95), INK, 2.3)
    panel = P(h.line(24, 30, 108, 29) + h.line(136, 30, 218, 31) + h.line(24, 62, 70, 62)
              + h.line(150, 63, 216, 62), STEEL, 1.2)
    retr = P(h.line(14, 4, 104, 4) + h.line(226, 16, 226, 48), STEEL, 1.05)
    bell = P("M186-2C186-15 204-15 204-2M181-1L209-1M193-17L197-17", INK, 1.9)
    cards = P("M34-3L66-4M36-7L64-8", STEEL, 1.3)
    return g("kit-desk", top + sides + base + panel + retr + bell + cards,
             "The inn's front desk (counter). Top line is the EP007 table top; a closed front panel, a desk bell, a small card stack. Origin at left end of the top.")


# ---------------------------------------------------------------- the inn
WIN_W, WIN_H = 24, 28
ROW_Y = (88, 144)


def win_x(i):
    return 38 + i * 42


def inn_body(seed, s=1.0, detail=True, gid="kit-inn"):
    h = Hand(seed)
    S = lambda v: v * s
    ww = lambda w: w if s == 1 else max(w * .78, .9)
    out = []
    fill = (f"M{S(20)} {S(76)}H{S(460)}V{S(300)}H{S(20)}Z"
            f"M{S(10)} {S(76)}L{S(80)} {S(18)}H{S(400)}L{S(470)} {S(76)}Z")
    out.append(F(fill, PAPER, .58))
    # roof
    out.append(P(h.line(S(10), S(77), S(79), S(20)) + h.line(S(82), S(19), S(236), S(18))
                 + h.line(S(247), S(18), S(398), S(19)) + h.line(S(401), S(20), S(470), S(76))
                 + h.line(S(8), S(77), S(206), S(76)) + h.line(S(216), S(77), S(472), S(76)),
                 INK, ww(2.8)))
    out.append(P(h.line(S(18), S(80), S(70), S(35)) + h.line(S(96), S(24), S(182), S(23))
                 + h.line(S(302), S(23), S(382), S(24)) + h.line(S(414), S(31), S(462), S(71)),
                 STEEL, ww(1.1)))
    if detail:
        hatch = "".join(h.line(x, 30 + (x % 3) * 6, x + 9, 44 + (x % 3) * 6, a=.6)
                        for x in (112, 150, 196, 268, 322, 366))
        out.append(P(hatch, STEEL, .95))
    # chimney
    out.append(P(h.line(S(338), S(19), S(339), S(-4)) + h.line(S(336), S(-5), S(362), S(-4))
                 + h.line(S(362), S(-2), S(363), S(18)), INK, ww(2.3)))
    # walls and base
    out.append(P(h.line(S(22), S(80), S(21), S(196)) + h.line(S(22), S(208), S(21), S(300))
                 + h.line(S(458), S(79), S(459), S(170)) + h.line(S(458), S(182), S(459), S(300))
                 + h.line(S(16), S(301), S(146), S(300)) + h.line(S(158), S(301), S(320), S(300))
                 + h.line(S(331), S(301), S(466), S(300)), INK, ww(2.6)))
    if detail:
        # inner bay structure and pressure marks, as in the EP007 workshop construction
        out.append(P(h.line(30, 84, 31, 180) + h.line(30, 196, 31, 292) + h.line(450, 85, 451, 160)
                     + h.line(450, 176, 451, 292) + h.line(28, 81, 198, 81) + h.line(214, 81, 452, 81)
                     + h.line(30, 293, 150, 292) + h.line(164, 293, 280, 293) + h.line(338, 293, 450, 292),
                     INK, 2.1))
        out.append(P(h.line(30, 309, 92, 308) + h.line(304, 309, 396, 308) + h.line(12, 82, 13, 128)
                     + h.line(466, 200, 467, 250) + "M16 186L24 187M17 191L25 192M458 222L466 223M459 227L467 228",
                     STEEL, 1))
    out.append(P(h.line(S(26), S(134), S(210), S(133)) + h.line(S(222), S(134), S(454), S(134))
                 + h.line(S(26), S(190), S(170), S(189)) + h.line(S(182), S(190), S(454), S(190))
                 + h.line(S(27), S(96), S(28), S(128)) + h.line(S(453), S(212), S(454), S(262)),
                 STEEL, ww(1.1)))
    # twenty room windows, two rows of ten
    frames, munt = [], []
    for y in ROW_Y:
        for i in range(10):
            x = win_x(i)
            if detail:
                frames.append(h.rect(S(x), S(y), S(WIN_W), S(WIN_H), a=.7, corner=(-1.5, 2.5)))
                munt.append(h.line(S(x + 12), S(y + 3), S(x + 12), S(y + 25), a=.5)
                            + h.line(S(x + 3), S(y + 13), S(x + 21), S(y + 13), a=.5)
                            + h.line(S(x - 3), S(y + 32), S(x + 27), S(y + 32), a=.6))
            else:
                frames.append(h.rect(S(x), S(y), S(WIN_W), S(WIN_H), a=.35, corner=(-1, 1.5)))
    out.append(P("".join(frames), INK if detail else STEEL, 1.6 if detail else 1.25))
    if munt:
        out.append(P("".join(munt), STEEL, 1.05))
    # lobby cutaway with the front desk inside
    out.append(F(f"M{S(56)} {S(204)}H{S(252)}V{S(296)}H{S(56)}Z", PAPER))
    out.append(P(h.rect(S(56), S(204), S(196), S(92), brk_side=0), INK, ww(2.4)))
    if detail:
        out.append(P(h.line(61, 209, 150, 208) + h.line(247, 212, 247, 250), STEEL, 1))
        # lobby window onto the trail: a hill and one tree, never a rising line
        out.append(P(h.rect(70, 214, 46, 32, a=.5) + h.line(93, 217, 93, 243, a=.3)
                     + "M73 243C80 235 88 234 96 239C102 243 108 240 113 236M104 236L107 226L110 236",
                     STEEL, 1.2))
        out.append(P(h.line(168, 224, 216, 223) + "M176 224L176 230M188 224L188 231M200 224L200 230M210 224L210 231",
                     STEEL, 1.2))
    out.append(P(h.line(S(84), S(262), S(150), S(261)) + h.line(S(157), S(262), S(224), S(261))
                 + h.line(S(86), S(266), S(87), S(292)) + h.line(S(222), S(265), S(221), S(291)),
                 INK, ww(2)))
    if detail:
        out.append(P(h.line(96, 278, 210, 277) + "M94 259L108 256L122 259M108 256L108 260", STEEL, 1.2))
    # door and porch
    out.append(P(h.line(S(286), S(300), S(285), S(216)) + h.line(S(284), S(214), S(331), S(213), brk=True)
                 + h.line(S(331), S(216), S(332), S(300)) + h.line(S(272), S(206), S(344), S(205)),
                 INK, ww(2.2)))
    if detail:
        out.append(P(h.line(293, 224, 293, 290) + h.line(324, 224, 324, 290) + h.line(276, 206, 286, 214)
                     + h.line(342, 205, 332, 213), STEEL, 1.05))
        out.append(P("M318 256L319 263", INK, 2))
        out.append(P(h.line(360, 294, 444, 293) + h.line(368, 294, 368, 282) + h.line(436, 293, 436, 281)
                     + "M20 298L26 290M22 302L28 295M440 299L444 291M450 300L453 295", STEEL, 1))
    return g(gid, "\n".join(out), "")


def inn():
    body = inn_body(21)
    return body.replace('data-kit-desc=""',
                        'data-kit-desc="The inn. 20 room windows in two rows of ten, lobby cutaway with the front desk, door with porch. Native 480x304, origin top-left (chimney reaches y -5)."')


def inn_mini():
    body = inn_body(22, s=.5, detail=False, gid="kit-inn-mini")
    return body.replace('data-kit-desc=""',
                        'data-kit-desc="Same inn at half size with fine construction removed, for groups (six inns, a handful). Native 240x152."')


def inn_window_lit():
    h = Hand(31)
    body = (F("M0 0H24V28H0Z", SHEET) + P(h.rect(0, 0, 24, 28, a=.5), INK, 2.1)
            + P("M12 3L12 25M3 13L21 13", STEEL, 1.05)
            + P("M4 22L9 17M4 16L14 7M11 22L20 13", STEEL, 1)
            + P("M-5-4L-13-11M29-4L37-11M-6 32L-14 38M30 32L38 38M12-6L12-14", INK, 1.6))
    return g("kit-inn-window-lit", body,
             "Overlay for one room window lighting. Place at a window origin: x = 38 + i*42, y = 88 (upper row) or 144 (lower row), in inn coordinates.")


def own_page(dashed=False):
    h = Hand(41)
    if dashed:
        body = (P("M0 2L40 0L54 13L53 62L1 63Z", STEEL, 2, extra=' stroke-dasharray="6 5"'))
        return g("kit-inn-own-page-dashed", body,
                 "The inn's own page before a job makes it live: dashed outline only. Anchor in inn coordinates at (372, 214).")
    body = (F("M0 2L40 0L54 13L53 62L1 63Z", SHEET)
            + P(h.line(0, 2, 40, 0) + h.line(54, 14, 53, 62) + h.line(51, 63, 1, 63) + h.line(0, 60, 1, 4), INK, 2.2)
            + P("M40 0L40 13L54 13", STEEL, 1.3)
            + P("M9 22L34 21M9 32L42 32M9 42L28 42", STEEL, 1.15)
            + P("M22 63L22 52C22 46 32 46 32 52L32 63", INK, 1.6))
    return g("kit-inn-own-page", body,
             "The inn's own page, live: a small page with a door mark. Anchor in inn coordinates at (372, 214).")


def hotel_large():
    h = Hand(51)
    out = [F("M10 30H210V214H10Z", PAPER, .58)]
    out.append(P(h.line(4, 30, 216, 29, brk=True) + h.line(10, 22, 210, 21) + h.line(10, 33, 11, 214)
                 + h.line(210, 32, 211, 214) + h.line(2, 215, 218, 214, brk=True), INK, 2.3))
    out.append(P(h.line(14, 36, 100, 36) + h.line(206, 40, 206, 120), STEEL, 1.1))
    fr = []
    for r in range(4):
        for c in range(8):
            fr.append(h.rect(22 + c * 23.5, 44 + r * 34, 14, 20, a=.4, corner=(-1, 1.5)))
    out.append(P("".join(fr), STEEL, 1.4))
    out.append(P(h.line(94, 214, 94, 186) + h.line(94, 185, 126, 185) + h.line(126, 186, 127, 214), INK, 2))
    return g("kit-hotel-large", "\n".join(out),
             "A larger independent hotel (S09 tier 1). Four storeys, flat parapet roof; drawn so it never reads as the inn. Native 220x216.")


# ---------------------------------------------------------------- the booking site
def booking_site():
    h = Hand(61)
    out = [F("M6 84L220 10L436 84V256H6Z", PAPER, .58)]
    out.append(P(h.line(6, 84, 214, 12) + h.line(226, 11, 436, 83) + h.line(4, 86, 214, 85)
                 + h.line(226, 86, 440, 85), INK, 2.4))
    out.append(P(h.line(20, 80, 180, 25) + h.line(262, 25, 420, 78) + h.line(170, 70, 270, 70)
                 + h.line(24, 104, 150, 104) + h.line(300, 250, 410, 250) + "M14 262L20 256M16 266L22 260M424 264L430 257",
                 STEEL, 1.1))
    out.append(P(h.line(18, 98, 424, 97, brk=True) + h.line(10, 256, 432, 255, brk=True), INK, 2.2))
    bays, posts, arcs = [], [], []
    for i in range(6):
        x = 36 + i * 64
        out.append(F(f"M{x} 112H{x + 44}V246H{x}Z", SHEET))
        bays.append(h.rect(x, 112, 44, 134, a=.6, corner=(-1.5, 2.5)))
        arcs.append(f"M{x + 5} 120C{x + 12} 114 {x + 32} 114 {x + 39} 120")
        posts.append(h.line(x - 10, 104, x - 10, 252, a=.6))
    posts.append(h.line(414, 104, 414, 252, a=.6))
    out.append(P("".join(posts), INK, 2))
    out.append(P("".join(bays), STEEL, 1.8))
    out.append(P("".join(arcs) + h.line(0, 270, 440, 269, brk=True) + h.line(-6, 284, 446, 283, brk=True),
                 STEEL, 1.3))
    return g("kit-booking-site", "\n".join(out),
             "The booking site: a lit hall with six lit bays facing its audience. Neutral ink and steel, no logo, never a villain colour. Native 440x286. Listing slots: bay centres x = 58 + i*64, y = 180.")


def booking_site_simple():
    h = Hand(62)
    out = [F("M4 44L80 6L156 44V116H4Z", PAPER, .58)]
    out.append(P(h.line(4, 44, 78, 7) + h.line(84, 7, 156, 43) + h.line(2, 46, 158, 45, brk=True)
                 + h.line(4, 116, 156, 115, brk=True), INK, 2.2))
    bays = []
    for i in range(3):
        x = 22 + i * 44
        out.append(F(f"M{x} 58H{x + 26}V108H{x}Z", SHEET))
        bays.append(h.rect(x, 58, 26, 50, a=.5, corner=(-1, 2)))
    out.append(P("".join(bays), STEEL, 1.6))
    out.append(P(h.line(-2, 124, 162, 123), STEEL, 1.2))
    return g("kit-booking-site-simple", "\n".join(out),
             "The booking site in its simple S00 form: same pediment and lit bays, three bays. Native 160x126.")


def listing_card(inn_glyph=False):
    h = Hand(71 if inn_glyph else 72)
    body = F("M0 1L34 0L35 25L1 26Z", SHEET) + P(h.rect(0, 0, 34, 25, a=.4, corner=(-1, 1.5)), STEEL, 1.5)
    if inn_glyph:
        body += P("M5 13L11 6L17 13M6 13L6 19L16 19L16 13", INK, 1.5) + P("M21 10L30 10M21 16L28 16", STEEL, 1)
        return g("kit-listing-card-inn", body, "The inn's own listing card inside the booking site (small gable glyph). Native 35x26.")
    body += P("M6 8L28 8M6 14L24 14M6 19L18 19", STEEL, 1)
    return g("kit-listing-card", body, "Another property's listing card inside the booking site. Native 35x26.")


def crowd():
    pos = [(20, 40), (70, 34), (120, 42), (170, 36), (220, 41), (45, 86), (95, 80), (145, 88), (195, 82)]
    uses = "".join(f'<use href="#kit-person" transform="translate({x},{y}) scale(.34)"/>' for x, y in pos)
    return g("kit-crowd", uses,
             "Travellers facing the booking site: nine kit-person figures at scale .34. Native about 245x100, origin top-left of the group box (first head at y about 3).")


# ---------------------------------------------------------------- tags
def commission_tag(state="solid"):
    h = Hand(81)
    outline = "M16 3L62 2L63 38L16 39L2 21Z"
    if state == "empty":
        body = P(outline, STEEL, 2, extra=' stroke-dasharray="6 5"') + P("M12 21a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0", STEEL, 1.4)
        return g("kit-commission-tag-empty", body,
                 "The place a commission tag would be: dashed steel outline, no fill, no string. Same footprint as kit-commission-tag.")
    body = (F(outline, SHEET)
            + P(h.line(16, 3, 61, 2) + h.line(63, 5, 63, 38) + h.line(60, 39, 17, 39) + h.line(15, 38, 2, 22)
                + h.line(2, 19, 13, 5), INK, 2.4)
            + P("M12 21a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0", INK, 1.6)
            + P("M12 21C4 24-6 15-16 21M22 7L56 6", STEEL, 1.2))
    return g("kit-commission-tag", body,
             "Commission tag, no number. Every commission tag in the episode is this object at the same size. Native 64x40 plus string to x -16.")


def tag_service():
    body = (P("M25 11L55 10L56 31L25 32Z", STEEL, 1.6, extra=' stroke-dasharray="4 4"'))
    return g("kit-tag-service", body,
             "Overlay: the dashed service shape inside a commission tag (S00h). Place at the tag's origin; label 'a service' is typeset by the builder. Solid in S21: set stroke-dasharray none on an inline copy.")


def commission_tag_layers():
    h = Hand(82)
    outline = "M64 12L248 8L252 152L64 156L8 84Z"
    body = (F(outline, SHEET)
            + P(h.line(64, 12, 244, 8) + h.line(252, 12, 252, 152) + h.line(248, 156, 66, 156)
                + h.line(60, 154, 8, 86) + h.line(8, 80, 58, 16), INK, 3)
            + P("M48 84a13 13 0 1 0 26 0a13 13 0 1 0-26 0", INK, 2)
            + P(h.line(86, 46, 244, 45) + h.line(86, 84, 244, 83) + h.line(86, 120, 244, 119), STEEL, 1.4)
            + P(h.line(84, 18, 230, 16), STEEL, 1.1))
    return g("kit-commission-tag-layers", body,
             "The commission tag enlarged to show its four layers (S03c, S03d). Same shape as kit-commission-tag at 4x, drawn at native size so stroke weights stay standard. Layer rows y 12-46, 46-84, 84-120, 120-156; text x from 96. Native 252x156.")


def rate_tag():
    h = Hand(83)
    body = (F("M10 1L55 1L56 33L1 34L1 10Z", SHEET)
            + P(h.line(10, 1, 55, 1) + h.line(56, 3, 56, 33) + h.line(54, 34, 1, 34) + h.line(1, 32, 1, 11)
                + h.line(1, 9, 9, 2), INK, 2.2)
            + P("M9 9a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0-5 0", INK, 1.3)
            + P("M12 24L44 24", STEEL, 1.2))
    return g("kit-rate-tag", body, "A blank room-rate tag (Bookable). No figure. Native 56x34.")


def retainer_tag():
    h = Hand(84)
    body = (F("M0 3L80 1L96 15L95 44L1 45Z", SHEET)
            + P(h.line(0, 3, 80, 1) + h.line(96, 16, 95, 44) + h.line(93, 45, 1, 45) + h.line(0, 42, 0, 6), STEEL, 2)
            + P("M80 1L80 15L96 15", STEEL, 1.3)
            + P("M12 31L66 31", STEEL, 1.2))
    return g("kit-retainer-tag", body,
             "A retainer tag with no price: small dog-eared label with a blank line. Always sits under a ceiling line. Native 96x45.")


# ---------------------------------------------------------------- the ceiling slip
SLIP_BOX_Y = (92, 178, 264, 350)
SLIP_LABELS = ("Rooms", "Rate", "Occupancy", "Share through the sites")
SLIP_VALUES = ("20", "$180 a night", "70%", "63%")


def slip_sheet(h):
    return (F("M4 6L262 2L298 36L296 436L2 438Z", SHEET)
            + P(h.line(4, 6, 262, 2) + h.line(298, 38, 296, 436) + h.line(293, 438, 3, 438)
                + h.line(2, 434, 3, 10), STEEL, 2)
            + P("M262 3L262 36L297 36", STEEL, 1.3))


def ceiling_slip(state):
    h = Hand(91)
    gid = f"kit-ceiling-slip-{state}"
    out = [slip_sheet(h), P("M24 50L170 49", STEEL, 1.2).replace("<path", f'<path id="{gid}__title-line"')]
    for i, y in enumerate(SLIP_BOX_Y):
        out.append(P(h.rect(24, y, 252, 52, a=.8, corner=(-2, 3)), INK, 2.2).replace("<path", f'<path id="{gid}__box{i + 1}"'))
        if state in ("labelled", "filled"):
            out.append(T(26, y - 10, SLIP_LABELS[i], 20, 400, MUTED, tid=f"{gid}__label{i + 1}"))
        if state == "filled":
            out.append(T(40, y + 36, SLIP_VALUES[i], 28, 500, INK, tid=f"{gid}__value{i + 1}"))
    out.append(P(h.line(24, 414, 276, 413, brk=True), INK, 2).replace("<path", f'<path id="{gid}__line"'))
    desc = {
        "blank": "Ceiling slip, blank: four empty input boxes and one unlabelled line (S00h, S21 cleared). No labels.",
        "labelled": "Ceiling slip with the four input labels and empty boxes (S14a real inputs, S16a, S21 after clearing).",
        "filled": "Ceiling slip filled with the illustrative inn's spoken inputs: 20, $180 a night, 70%, 63% (S10 only).",
    }[state]
    return g(gid, "\n".join(out), desc + " Native 300x440. Title 'The ceiling' goes on the title line (builder).")


def ceiling_line(ghost=False):
    if ghost:
        body = P("M0 0L172-1M180 0L360-1M0-7L0 7M360-8L360 6", STEEL, 2, extra=' opacity=".5"')
        return g("kit-ceiling-line-ghost", body,
                 "Ghost ceiling for sensitivity (steel, 50%). Never replaces the solid line. Native 360 wide, origin at left end.")
    body = (P("M0 0L172-1M180 0L360-1", "currentColor", 3)
            + P("M0-8L0 8M360-9L361 7", "currentColor", 2)
            + P("M16 4L118 4M232 3L300 3", STEEL, 1))
    return g("kit-ceiling-line", body,
             "The ceiling line. Stroke is currentColor: set color on the use (ink by default, oxide only when it is the one active accent). Native 360 wide, origin at left end.")


# ---------------------------------------------------------------- job cards and practice card
def job_card(kind):
    h = Hand({"findable": 101, "bookable": 102, "remembered": 103}[kind])
    title = {"findable": "Findable", "bookable": "Bookable", "remembered": "Remembered"}[kind]
    gid = f"kit-job-{kind}"
    out = [f'<rect x="0" y="0" width="250" height="180" rx="4" stroke="{INK}" stroke-width="3.5" fill="{CARD}"/>',
           T(20, 42, title, 26, 500, INK, tid=f"{gid}__title")]
    if kind == "findable":
        out.append(P(h.rect(20, 62, 180, 28, a=.5), STEEL, 1.4))
        out.append(P("M210 74a7 7 0 1 0 14 0a7 7 0 1 0-14 0M222 80L230 88", INK, 1.8))
        out.append(P(h.line(22, 112, 132, 112) + h.line(22, 128, 104, 128) + h.line(22, 150, 118, 150), STEEL, 1.3))
        out.append(P("M136 120C160 120 176 128 186 140M178 134L187 141L176 145", INK, 2))
        out.append(F("M192 118L218 117L228 127L227 166L193 167Z", SHEET)
                   + P(h.line(192, 118, 218, 117) + h.line(228, 128, 227, 166) + h.line(225, 167, 193, 167)
                       + h.line(192, 164, 192, 121), INK, 2)
                   + P("M218 117L218 127L228 127M198 138L220 137M198 148L214 148", STEEL, 1.1))
    elif kind == "bookable":
        for x in (34, 150):
            out.append(f'<use href="#kit-rate-tag" transform="translate({x},100) scale(1.2)"/>')
        out.append(T(125, 132, "=", 40, 500, INK, "middle"))
    else:
        out.append(f'<use href="#kit-guest-book-open" transform="translate(20,84) scale(.55)"/>')
        out.append(f'<use href="#kit-thank-you-note" transform="translate(150,90) scale(.8)"/>')
        out.append(f'<use href="#kit-leaf" transform="translate(206,140) scale(.8)"/>')
    desc = {
        "findable": "Job card Findable: a search, a free link, the inn's own page reached.",
        "bookable": "Job card Bookable: two blank rate tags joined by '='.",
        "remembered": "Job card Remembered: the guest book, a thank-you note, a seasonal leaf.",
    }[kind]
    return g(gid, "\n".join(out), desc + " Card grammar is the EP007 practice card (fill #EDE5D6, ink 3.5). Native 250x180.")


def practice_card():
    body = (f'<rect x="0" y="0" width="150" height="170" rx="4" stroke="{INK}" stroke-width="3.5" fill="{CARD}"/>'
            + P("M26 38L124 38M26 68L124 68M26 98L100 98", STEEL, 1.3))
    return g("kit-practice-card", body, "The practice card. Verbatim EP007 R57 practice geometry. Native 150x170.")


# ---------------------------------------------------------------- guest book and paper
def guest_book_closed():
    h = Hand(111)
    body = (F("M2 4L126 2L128 86L4 88Z", CARD)
            + P(h.line(2, 4, 126, 2) + h.line(128, 5, 128, 86) + h.line(125, 88, 4, 88) + h.line(2, 85, 2, 8), INK, 2.6)
            + P(h.line(18, 6, 19, 86), INK, 2)
            + P(h.line(7, 14, 13, 14) + h.line(7, 26, 13, 26) + h.line(7, 70, 13, 70)
                + h.line(132, 10, 133, 88) + h.line(8, 92, 130, 91), STEEL, 1.1)
            + P("M94 88L95 104L100 98L104 105L104 88", INK, 1.5))
    return g("kit-guest-book-closed", body, "The guest book, closed: cloth-bound, spine band, ribbon. Intact. Native 134x106.")


BOOK_OUT = ("M100 16C74 6 34 4 4 14M2 18L3 110M4 112C34 104 72 104 98 116"
            "M104 16C130 6 170 4 196 14M198 18L197 110M196 112C166 104 128 104 102 116")


def guest_book_open(dashed=False):
    h = Hand(112)
    if dashed:
        body = P(BOOK_OUT + "M101 20L101 112", STEEL, 2, extra=' stroke-dasharray="8 6"')
        return g("kit-guest-book-open-dashed", body,
                 "The inn's own guest book before anyone signs it: dashed outline of kit-guest-book-open (S07c). Turns solid in S15a. Native 200x120.")
    body = (F("M101 16C74 5 34 3 3 14L3 111C34 103 72 103 101 116C130 103 168 103 198 111L198 14C170 3 130 5 101 16Z", SHEET)
            + P(BOOK_OUT, INK, 2.4)
            + P("M101 18L101 114", INK, 1.8)
            + P("M6 117C36 110 70 110 101 121C132 110 166 110 195 117", STEEL, 1.2)
            + P(h.line(16, 22, 60, 16) + h.line(146, 16, 186, 22), STEEL, 1))
    return g("kit-guest-book-open", body, "The guest book, open, pages blank. Intact: never torn, locked, greyed or crossed. Native 200x122.")


def squiggle(h, x, y, w, amp=5, step=9):
    d = f"M{n(x)} {n(y)}"
    cx = x
    up = True
    while cx < x + w:
        nx = cx + step + h.j(2)
        a = amp * (1 if up else -.6) + h.j(1.5)
        d += f"C{n(cx + 2)} {n(y - a)} {n(nx - 2)} {n(y - a)} {n(nx)} {n(y + h.j(1))}"
        cx = nx
        up = not up
    return d


def guest_book_entries():
    h = Hand(113)
    body = (P(squiggle(h, 14, 44, 70, 6, 10), INK, 1.5).replace("<path", '<path id="kit-guest-book-entries__name"')
            + P(squiggle(h, 14, 66, 46, 4, 9), INK, 1.4).replace("<path", '<path id="kit-guest-book-entries__town"')
            + P("M16 80L38 80L38 94L16 94ZM16 80L27 88L38 80", INK, 1.4).replace("<path", '<path id="kit-guest-book-entries__envelope"'))
    return g("kit-guest-book-entries", body,
             "Overlay in kit-guest-book-open coordinates: a handwritten name, a town, a small envelope mark on the left page (S07a). Pencil marks, not readable words.")


def signature():
    h = Hand(114)
    body = P(squiggle(h, 116, 58, 64, 8, 12) + "M118 70L176 68", INK, 1.6)
    return g("kit-signature", body, "Overlay in kit-guest-book-open coordinates: a signature on the right page.")


def sheet():
    body = (P("m0 3 263-3 68 31-3 110-330 3z", STEEL, 2, fill=SHEET)
            + P("m263 1-1 30 66-1m-321 110 84-1m-87-126-1 43", STEEL, 1.3))
    return g("kit-sheet", body, "Generic paper sheet. Verbatim EP007 R46 decision sheet. Native 331x144. Use for audit card, email tool card, credential card, newsletter card, report pages.")


def card_small():
    h = Hand(121)
    body = (F("M0 2L170 0L200 22L198 108L1 110Z", SHEET)
            + P(h.line(0, 2, 170, 0) + h.line(200, 24, 198, 108) + h.line(196, 110, 1, 110) + h.line(0, 106, 0, 6), STEEL, 2)
            + P("M170 1L170 22L199 22", STEEL, 1.3))
    return g("kit-card-small", body, "Small dog-eared card for short typeset labels (free link, direct rate, thank you, reservation report, email tool, retainer). Native 200x110. Text from x 16, first baseline y 46.")


def registration_card():
    h = Hand(131)
    gid = "kit-registration-card"
    body = (F("M2 3L356 1L358 196L3 198Z", SHEET)
            + P(h.rect(2, 2, 356, 195, a=.8, brk_side=2), STEEL, 2)
            + P(h.line(20, 44, 200, 43) + h.line(20, 80, 150, 79), STEEL, 1.2)
            + P("M20 44L20 40M20 80L20 76", STEEL, 1)
            + T(20, 124, "Email", 20, 400, MUTED, tid=f"{gid}__label")
            + P(h.rect(20, 134, 320, 44, a=.7, corner=(-2, 3)), INK, 2.1).replace("<path", f'<path id="{gid}__field"'))
    return g(gid, body,
             "Registration card: two blank write-in lines and an Email field box (field inner text origin x 34, baseline y 164). Put kit-text-own-email or kit-text-relay inside. Native 360x200.")


RELAY_LOCAL = "k7m2q9x4"
RELAY_DOMAIN = "@guest.booking.com"


def text_own_email():
    return g("kit-text-own-email", T(0, 0, "guest's own email", 22, 400, INK),
             "Typeset field value for the guest's own email. Origin at text baseline start.")


def text_relay():
    body = (f'<text x="0" y="0" font-family="{FONT}" font-size="20" font-weight="400" fill="{INK}">'
            f'<tspan id="kit-text-relay__local">{RELAY_LOCAL}</tspan><tspan id="kit-text-relay__domain">{RELAY_DOMAIN}</tspan></text>')
    return g("kit-text-relay", body,
             "Typeset relay string (illustrative) sized to fit a registration card field. Origin at text baseline start.")


def relay_field():
    h = Hand(141)
    gid = "kit-relay-field"
    body = (F("M0 0H420V56H0Z", SHEET)
            + P(h.rect(0, 0, 420, 56, a=.8, corner=(-2, 3)), INK, 2.2)
            + f'<text x="18" y="37" font-family="{FONT}" font-size="24" font-weight="400" fill="{INK}">'
              f'<tspan id="{gid}__local">{RELAY_LOCAL}</tspan><tspan id="{gid}__domain">{RELAY_DOMAIN}</tspan></text>'
            + T(420, 84, "illustrative", 20, 400, MUTED, "end", tid=f"{gid}__illustrative"))
    return g(gid, body,
             "The relay address field: an illustrative string of letters and numbers ending @guest.booking.com, typeset, with the label 'illustrative'. Child tspans __local and __domain type on separately (S00d). Native 420x90.")


def reservation_record():
    h = Hand(151)
    gid = "kit-reservation-record"
    rows = ["Guest", "Dates", "Room"]
    out = [F("M0 3L560 0L596 30L594 322L2 324Z", SHEET),
           P(h.line(0, 3, 560, 0) + h.line(596, 32, 594, 322) + h.line(592, 324, 2, 324) + h.line(0, 320, 0, 6), STEEL, 2),
           P("M560 1L560 30L595 30", STEEL, 1.3),
           T(28, 52, "RESERVATION", 18, 500, MUTED, extra=' letter-spacing="2"'),
           P(h.line(28, 66, 566, 65), STEEL, 1.2)]
    for i, r in enumerate(rows):
        y = 108 + i * 50
        out.append(T(28, y, r, 22, 400, MUTED))
        out.append(P(h.line(150, y - 6, 150 + 170 - i * 40, y - 6), STEEL, 3.5, extra=' opacity=".45"'))
    out.append(T(28, 264, "Email", 22, 400, MUTED))
    out.append(f'<use href="#kit-relay-field" transform="translate(150,232) scale(.98)"/>')
    return g(gid, "\n".join(out),
             "Drawn reservation record for the S00d screen insert: typeset field names, unreadable values, and kit-relay-field in the Email row. Native 596x324 (relay label reaches y 314).")


def boundary():
    body = (P("M0 0L1 188", "currentColor", 5) + P("M-12 196L14 195", STEEL, 1.3))
    return g("kit-boundary", body,
             "Boundary marker: one vertical stroke (EP007 R59 construction) in front of one action only. currentColor: ink by default, oxide when it is the accountable accent. Label ('the site's rules') typeset below by the builder, centred at x 0, y 236. Native 190 tall.")


def checkbox(checked=False):
    box = P("m0 0 24 1-1 25-23-1z", INK, 2)
    if checked:
        return g("kit-checkbox-checked", box + P("m3 12 8 9 17-25", "currentColor", 3.4),
                 "Checkbox, checked. Verbatim EP007 R46 box and mark; mark is currentColor. EP009 rule: never used for S19 outcomes.")
    return g("kit-checkbox-empty", box, "Checkbox, empty. Verbatim EP007 R46 box. Native 24x26.")


def report_slip(two=False):
    h = Hand(161 if two else 162)
    gid = "kit-report-slip-before-after" if two else "kit-report-slip"
    out = [F("M0 3L340 0L380 30L378 206L2 208Z", SHEET),
           P(h.line(0, 3, 340, 0) + h.line(380, 32, 378, 206) + h.line(376, 208, 2, 208) + h.line(0, 204, 0, 6), STEEL, 2),
           P("M340 1L340 30L379 30", STEEL, 1.3),
           T(22, 52, "Direct share of bookings", 24, 500, INK, tid=f"{gid}__title")]
    if two:
        out.append(P(h.rect(22, 84, 150, 62, a=.7), INK, 2.2).replace("<path", f'<path id="{gid}__box1"'))
        out.append(P(h.rect(202, 84, 150, 62, a=.7), INK, 2.2).replace("<path", f'<path id="{gid}__box2"'))
        out.append(T(22, 178, "before", 20, 400, MUTED) + T(202, 178, "after", 20, 400, MUTED))
        desc = "Monthly report slip with before and after value boxes, both blank (S11b). Native 380x208."
    else:
        out.append(P(h.rect(22, 84, 200, 72, a=.7), INK, 2.2).replace("<path", f'<path id="{gid}__box"'))
        out.append(T(40, 130, "", 30, 500, INK, tid=f"{gid}__value"))
        desc = "Report slip with one value box (S15b). The value text node __value is empty; a builder writes only what the narration allows (for example 'not moving'). Native 380x208."
    return g(gid, "\n".join(out), desc)


def thank_you_note():
    h = Hand(171)
    body = (F("M0 2L118 0L120 78L1 80Z", SHEET)
            + P(h.rect(0, 1, 119, 78, a=.6, corner=(-1.5, 2.5)), STEEL, 1.8)
            + P(squiggle(h, 14, 28, 80, 3, 8) + squiggle(h, 14, 46, 64, 3, 8) + squiggle(h, 14, 64, 30, 3, 8), INK, 1.3))
    return g("kit-thank-you-note", body, "Handwritten thank-you note: pencil lines, no readable words. Native 120x80.")


def leaf():
    body = (P("M15 34C3 24 2 10 15 0C28 10 27 24 15 34ZM15 34L15 6M15 22L9 16M15 16L21 11", INK, 1.7))
    return g("kit-leaf", body, "Seasonal leaf mark. Native 30x36.")


def seasonal_note():
    h = Hand(181)
    body = (F("M0 2L118 0L120 78L1 80Z", SHEET)
            + P(h.rect(0, 1, 119, 78, a=.6, corner=(-1.5, 2.5)), STEEL, 1.8)
            + '<use href="#kit-leaf" transform="translate(14,20) scale(.9)"/>'
            + P("M50 60C60 46 72 58 82 44C90 34 98 42 106 30", STEEL, 1.4, extra=' stroke-dasharray="3 4"'))
    return g("kit-seasonal-note", body, "Seasonal note: a leaf and a trail line (the fall trail). 'October' is typeset by the builder. Native 120x80.")


def envelope():
    h = Hand(191)
    body = P(h.rect(0, 0, 48, 32, a=.5, corner=(-1, 2)) + "M1 2L24 19L47 2", INK, 2)
    return g("kit-envelope", body, "Envelope mark. Native 48x32.")


def phone():
    h = Hand(201)
    body = (F("M8 0H68C74 0 76 2 76 8V128C76 134 74 136 68 136H8C2 136 0 134 0 128V8C0 2 2 0 8 0Z", SHEET)
            + P("M8 1L66 0M75 8L76 126M68 136L10 136M1 128L0 10M1 6C2 2 4 1 8 1M70 0C74 1 75 3 75 6M76 130C75 134 73 136 69 136M6 136C2 135 1 133 1 130", INK, 2.4)
            + P(h.rect(8, 16, 60, 100, a=.4), STEEL, 1.2)
            + P("M32 126L44 126", INK, 1.8))
    return g("kit-phone", body, "Drawn phone. Screen area x 8-68, y 16-116 for steps drawn by the builder; no UI text or logos. Native 76x136.")


def calendar_leaf():
    h = Hand(211)
    grid = "".join(h.line(16 + c * 22, 58 + r * 20, 28 + c * 22, 58 + r * 20, a=.4) for r in range(3) for c in range(4))
    body = (F("M0 10L118 8L120 130L2 132Z", SHEET)
            + P(h.rect(0, 9, 119, 122, a=.6), STEEL, 2)
            + P(h.line(2, 36, 118, 35), INK, 2.2)
            + P("M30 2L30 18M88 2L88 18", INK, 2.2)
            + P(grid, STEEL, 1.4))
    return g("kit-calendar-leaf", body, "Calendar leaf ('A year later', S18 renewal calendar). Native 120x132.")


def wifi_sign():
    h = Hand(221)
    body = (F("M0 2L120 0L121 100L1 102Z", SHEET)
            + P(h.rect(0, 1, 120, 100, a=.6), INK, 2)
            + P("M40 30C52 18 68 18 80 30M47 38C55 30 65 30 73 38M60 45L60 46", INK, 1.8)
            + P(h.rect(14, 64, 92, 22, a=.4), STEEL, 1.3)
            + P("M34 102L28 146M86 102L92 146", STEEL, 1.4))
    return g("kit-wifi-sign", body, "Wifi login sign on a stand, with an email field (x 14-106, y 64-86). Native 121x146.")


def empty_place():
    body = f'<rect x="0" y="0" width="150" height="170" rx="4" stroke="{INK}" stroke-width="3" fill="none" stroke-dasharray="12 9"/>'
    return g("kit-empty-place", body,
             "The empty place after checkout: dashed outline no pay line reaches. Verbatim EP007 R57 gap outline, same footprint as kit-practice-card and kit-practice-figure space. Native 150x170.")


def timeline_line():
    h = Hand(231)
    body = P(h.line(0, 0, 440, -1) + h.line(452, 0, 900, 0), INK, 3) + P(h.line(20, 4, 300, 4), STEEL, 1.1)
    return g("kit-timeline-line", body, "Pencil timeline, 900 long, origin at left end. Scale x only if shorter.")


def tick():
    return g("kit-tick", P("M0-12L1 12", INK, 3), "Event tick on a timeline (booking, stay, checkout, next booking). Native 24 tall centred on the line.")


def wall_hook():
    return g("kit-wall-hook", P("M10 0L10 16C10 26 0 26 0 18", INK, 2) + P("M4 0L16 0", STEEL, 1.3),
             "An empty wall hook ('marketing', S03f). Native 16x26.")


def route_samples():
    solid = g("kit-route-solid", P("M0 0C60-6 140-6 200 0", STEEL, 2.5) + P("M186-8L201 0L187 9", STEEL, 2.5),
              "Sample route/relationship line with arrowhead: steel 2.5. Draw your own geometry with class kit-route.")
    dashed = g("kit-route-dashed", P("M0 0C60-6 140-6 200 0", STEEL, 2.5, extra=' stroke-dasharray="10 8"'),
               "Sample hypothesis route (not yet real): steel 2.5 dashed 10 8. Class kit-route-dashed.")
    pay = g("kit-pay-line", P("M0 0C60-6 140-6 200 0", INK, 4),
            "Sample pay line firmed to its event: ink 4 (EP007 R54). Class kit-pay.")
    return "\n".join([solid, dashed, pay])


def main():
    parts = [
        person(), guest(), innkeeper(), practice_figure(), table(), desk(),
        inn(), inn_mini(), inn_window_lit(), own_page(False), own_page(True), hotel_large(),
        booking_site(), booking_site_simple(), listing_card(False), listing_card(True), crowd(),
        commission_tag(), commission_tag("empty"), tag_service(), commission_tag_layers(), rate_tag(), retainer_tag(),
        ceiling_slip("blank"), ceiling_slip("labelled"), ceiling_slip("filled"), ceiling_line(), ceiling_line(True),
        job_card("findable"), job_card("bookable"), job_card("remembered"), practice_card(),
        guest_book_closed(), guest_book_open(), guest_book_open(True), guest_book_entries(), signature(),
        sheet(), card_small(), registration_card(), text_own_email(), text_relay(), relay_field(), reservation_record(),
        boundary(), checkbox(False), checkbox(True), report_slip(False), report_slip(True),
        thank_you_note(), leaf(), seasonal_note(), envelope(), phone(), calendar_leaf(), wifi_sign(),
        empty_place(), timeline_line(), tick(), wall_hook(), route_samples(),
    ]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">\n'
           '<title>EP009 world kit</title>\n'
           '<desc>Shared drawn objects for EP009-FULL-BUILD-001. Definitions only; see KIT.md. '
           'Generated by tools/build_kit.py. Do not hand edit; change the generator and rebuild.</desc>\n'
           '<defs>\n' + "\n".join(parts) + '\n</defs>\n</svg>\n')
    OUT.write_text(svg)
    print(OUT, len(svg))


if __name__ == "__main__":
    main()
