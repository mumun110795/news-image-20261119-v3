#!/usr/bin/env python3
"""
The World in One Day -- Thursday 19 November 2026.

A newspaper front page in a single image, drawn entirely in code:
cream paper, ink type, red accents, three illustrated hero stories,
numbered story cards, a markets box and a long "also on Thursday"
list -- 53 stories from one day.

Python standard library only, no network. Deterministic output.
Writes entry.png into the directory named by MAKEFUN_OUTPUT_DIR
(default /output).
"""

import os
import struct
import zlib

W, H = 1024, 1024

# --------------------------------------------------------------------------
# Bitmap font, drawn in code: 5x7 glyphs, upper + lower case, digits,
# punctuation. Each glyph is 7 rows of 5 pixels.
# --------------------------------------------------------------------------

FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    'X': ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    'a': (".....", ".....", ".####", "....#", ".####", "#...#", ".####"),
    'b': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    'c': (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    'd': ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    'e': (".....", ".....", ".###.", "#...#", "#####", "#....", ".####"),
    'f': ("..##.", ".#...", ".#...", "####.", ".#...", ".#...", ".#..."),
    'g': (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
    'h': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'i': ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    'j': ("...#.", ".....", "..##.", "...#.", "...#.", "#..#.", ".##.."),
    'k': ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    'l': (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'm': (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    'n': (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'o': (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    'p': (".....", ".....", "####.", "#...#", "#...#", "####.", "#...."),
    'q': (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
    'r': (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    's': (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    't': (".#...", ".#...", "####.", ".#...", ".#...", ".#..#", "..##."),
    'u': (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
    'v': (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'w': (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    'x': (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    'y': (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
    'z': (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    '0': (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    '3': (".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".....", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".....", ".##..", ".#..."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    '·': (".....", ".....", ".....", ".##..", ".##..", ".....", "....."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '(': ("..##.", ".#...", "#....", "#....", "#....", ".#...", "..##."),
    ')': (".##..", "...#.", "....#", "....#", "....#", "...#.", ".##.."),
    '%': ("##..#", "#...#", "...#.", "..#..", ".#...", "#...#", "#.##."),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '£': (".###.", "#....", "#....", "####.", "#....", "#....", "#####"),
    '+': (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    '#': (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    '&': (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...##", "..#..", ".....", "..#.."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '*': (".....", ".#.#.", ".###.", ".#.#.", ".....", ".....", "....."),
}

_GLYPH_FIX = {'\u2212': '-', '\u2013': '-', '\u2014': '-',
              '\u2019': "'", '\u201c': '"', '\u201d': '"',
              '\u2022': '·'}


def glyph(ch):
    ch = _GLYPH_FIX.get(ch, ch)
    return FONT.get(ch, FONT[' '])


# --------------------------------------------------------------------------
# Colours: cream paper, dark ink, red accents.
# --------------------------------------------------------------------------

PAPER = (247, 241, 227)
PAPER_CARD = (255, 253, 247)
INK = (26, 26, 24)
INK_SOFT = (74, 70, 60)
RED = (179, 35, 27)
RED_DARK = (140, 26, 20)
HAIR = (201, 191, 165)
GOLD = (166, 124, 46)
GREEN = (46, 125, 50)
GREEN_SOFT = (231, 243, 231)
SKY = (219, 233, 246)
SAND = (246, 236, 210)
NAVY = (34, 53, 74)


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set_px(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(col)

    def rect(self, x, y, w, h, col):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(col) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def frame(self, x, y, w, h, col, t=1):
        self.rect(x, y, w, t, col)
        self.rect(x, y + h - t, w, t, col)
        self.rect(x, y, t, h, col)
        self.rect(x + w - t, y, t, h, col)

    def line(self, x0, y0, x1, y1, col, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        r = t // 2
        while True:
            self.rect(x - r, y - r, t, t, col)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, rad, col):
        r2 = rad * rad
        for dy in range(-rad, rad + 1):
            dx = int((r2 - dy * dy) ** 0.5)
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, col)

    def ring(self, cx, cy, rad, col, t=2):
        r2o, r2i = rad * rad, (rad - t) * (rad - t)
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                d2 = dx * dx + dy * dy
                if r2i < d2 <= r2o:
                    self.set_px(cx + dx, cy + dy, col)

    def poly(self, pts, col):
        ys = [p[1] for p in pts]
        for yy in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= yy < y1) or (y1 <= yy < y0):
                    xs.append(x0 + (yy - y0) * (x1 - x0) // (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.rect(xs[i], yy, xs[i + 1] - xs[i] + 1, 1, col)

    # ---------------- text ----------------

    def text_w(self, s, scale, tracking=0):
        if not s:
            return 0
        return len(s) * 6 * scale - scale + tracking * (len(s) - 1)

    def text(self, x, y, s, scale, col, bold=False, tracking=0):
        extra = max(1, scale // 2) if bold else 0
        cx = x
        for ch in s:
            g = glyph(ch)
            for r in range(7):
                row = g[r]
                for c in range(5):
                    if row[c] == '#':
                        self.rect(cx + c * scale, y + r * scale,
                                  scale + extra, scale, col)
            cx += 6 * scale + tracking
        return cx - tracking

    def text_r(self, xr, y, s, scale, col, bold=False, tracking=0):
        return self.text(xr - self.text_w(s, scale, tracking), y, s,
                         scale, col, bold, tracking)

    def text_c(self, cx, y, s, scale, col, bold=False, tracking=0):
        return self.text(cx - self.text_w(s, scale, tracking) // 2, y, s,
                         scale, col, bold, tracking)


def wrap(s, maxw, scale):
    """Greedy word wrap; returns list of lines fitting maxw pixels."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if len(trial) * 6 * scale - scale <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def save_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# --------------------------------------------------------------------------
# Illustrations, all drawn in code (flat newspaper style).
# --------------------------------------------------------------------------

def draw_flag(cv, x, y, w, h, kind):
    if kind == 'us':
        cv.rect(x, y, w, h, (255, 255, 255))
        for i in range(0, 7, 2):
            cv.rect(x, y + i * h // 7, w, h // 7, (178, 34, 52))
        cw, chh = w * 2 // 5, h // 2 + 2
        cv.rect(x, y, cw, chh, (40, 50, 110))
        for r in range(3):
            for c in range(4):
                cv.rect(x + 3 + c * (cw - 4) // 3, y + 3 + r * (chh - 4) // 2,
                        2, 2, (255, 255, 255))
    elif kind == 'cn':
        cv.rect(x, y, w, h, (204, 32, 44))
        cv.circle(x + 10, y + 9, 4, (250, 210, 60))
        for dx, dy in ((18, 4), (20, 10), (18, 16)):
            cv.circle(x + dx, y + dy, 2, (250, 210, 60))
    else:  # ru
        cv.rect(x, y, w, h // 3, (255, 255, 255))
        cv.rect(x, y + h // 3, w, h // 3, (0, 60, 160))
        cv.rect(x, y + 2 * h // 3, w, h - 2 * h // 3, (204, 32, 44))
    cv.frame(x, y, w, h, INK, 1)


def ill_summit(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    cv.circle(x + w - 54, y + 30, 17, (240, 180, 60))
    base = y + h - 26
    blds = [(0.02, 0.10, 0.52), (0.13, 0.08, 0.68), (0.22, 0.12, 0.44),
            (0.35, 0.07, 0.74), (0.43, 0.10, 0.56), (0.54, 0.08, 0.66),
            (0.63, 0.12, 0.40), (0.76, 0.08, 0.60), (0.85, 0.13, 0.48)]
    for fx, fw, fh in blds:
        bx, bw = x + int(fx * w), int(fw * w)
        bh = int(fh * (h - 34))
        cv.rect(bx, base - bh, bw, bh, NAVY)
        for wy in range(base - bh + 6, base - 5, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if (wx * 7 + wy * 13) % 3 == 0:
                    cv.rect(wx, wy, 3, 4, (250, 240, 200))
    cv.rect(x, base, w, h - 26, (176, 198, 220))
    for f, kind in ((0.27, 'us'), (0.48, 'cn'), (0.69, 'ru')):
        px = x + int(f * w)
        cv.rect(px, y + h - 80, 3, 70, INK_SOFT)
        draw_flag(cv, px + 3, y + h - 80, 46, 30, kind)


def ill_scales(cv, x, y, w, h):
    cv.rect(x, y, w, h, SAND)
    cx, top = x + w // 2, y + 14
    cv.circle(cx, top, 5, RED)
    cv.rect(cx - 95, top + 6, 190, 5, INK)
    cv.rect(cx - 3, top + 11, 6, h - 50, INK)
    cv.poly([(cx - 36, y + h - 12), (cx + 36, y + h - 12),
             (cx + 16, y + h - 26), (cx - 16, y + h - 26)], INK)
    for px in (cx - 95, cx + 95):
        cv.line(px, top + 11, px - 22, top + 44, INK, 2)
        cv.line(px, top + 11, px + 22, top + 44, INK, 2)
        cv.rect(px - 27, top + 42, 54, 3, INK)
        cv.poly([(px - 27, top + 45), (px + 27, top + 45),
                 (px + 15, top + 57), (px - 15, top + 57)], GOLD)
        cv.circle(px, top + 36, 4, INK)


def ill_chart(cv, x, y, w, h):
    cv.rect(x, y, w, h, GREEN_SOFT)
    ax, base, top = x + 30, y + h - 22, y + 14
    cv.line(ax, top, ax, base, INK, 2)
    cv.line(ax, base, x + w - 14, base, INK, 2)
    span = base - top - 16
    pts = []
    for i, f in enumerate((0.30, 0.45, 0.55, 0.75, 0.95)):
        bx = ax + 22 + i * 48
        bh = int(f * span)
        cv.rect(bx, base - bh, 34, bh, GREEN)
        pts.append((bx + 17, base - bh))
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1] - 8, pts[i + 1][0], pts[i + 1][1] - 8,
                RED, 4)
    lx, ly = pts[-1][0], pts[-1][1] - 8
    cv.poly([(lx + 16, ly - 12), (lx - 2, ly - 10), (lx + 4, ly + 4)], RED)
    for px, py in pts:
        cv.circle(px, py, 3, INK)


# --------------------------------------------------------------------------
# The day's news: Thursday 19 November 2026 (verified story set).
# --------------------------------------------------------------------------

REGIONS = [("EUROPE", 7, (51, 102, 138)), ("MIDDLE EAST", 2, (188, 108, 37)),
           ("ASIA", 11, (157, 2, 8)), ("AFRICA", 2, (96, 108, 56)),
           ("AMERICAS", 20, (56, 102, 65)), ("OCEANIA", 3, (17, 138, 178)),
           ("WORLD", 8, (106, 76, 147))]

STATS = [("$81.3BN", "LARGEST IPO EVER RAISED", INK),
         ("589M", "CHILDREN IN CONFLICT ZONES", INK),
         ("-2.0%", "S&P 500 - FIFTH DAY OF FALLS", RED),
         ("879,000", "AI CHIPS CLEARED FOR CHINA", INK),
         ("-1,100", "DOW POINTS LOST AT THE CLOSE", RED),
         ("109-0", "DENMARK BACKS GREENLAND DEAL", INK)]

HEROES = [
    (1, "ASIA · SUMMIT", "Trump, Xi and Putin hold first three-way summit",
     "The three presidents meet as a trio for the first time in Shenzhen, "
     "signing a joint declaration on UN reform, nuclear restraint and "
     "open oil routes.", ill_summit),
    (2, "ASIA · JUSTICE", "UN court: Myanmar committed genocide",
     "The ICJ finds Myanmar's 2016-17 campaign against the Rohingya was "
     "genocide, a first verdict against a state, and orders safe return "
     "with compensation.", ill_scales),
    (3, "AMERICAS · MARKETS", "Anthropic's record IPO stuns Wall Street",
     "The debut raises $81.3bn, the biggest IPO ever. Shares jump 34% at "
     "the open to $83, valuing the AI firm above $2 trillion as records "
     "fall.", ill_chart),
]

CARDS = [
    (4, "MIDDLE EAST · IRAN WAR", "Houthi missile hits Riyadh tower",
     "Cross-border strikes reach the Saudi capital."),
    (5, "AMERICAS · MARKETS", "Dow plunges 1,100 points",
     "Fifth straight losing day as AI fears bite."),
    (6, "MIDDLE EAST · GAZA", "Aid groups score Gaza plan 4 of 26",
     "Relief plan meets just 4 of 26 aid benchmarks."),
    (7, "EUROPE · UKRAINE WAR", "Kyiv hits Crimean Bridge a third time",
     "Rail hit halts trains; Putin vows harsher reply."),
    (8, "WORLD · GAMING", "GTA VI goes on sale worldwide",
     "Rockstar's sequel launches globally at last."),
    (9, "WORLD · CHILDREN", "589m children live in war zones",
     "A record count as wars grind on worldwide."),
    (10, "WORLD · CLIMATE", "COP31 cuts fossil fuels from draft",
     "Antalya draft drops the phase-out pledge."),
    (11, "AMERICAS · AI", "OpenAI ships GPT-6.2 Astra and Sol",
     "Two flagship models land on a rival's big day."),
    (12, "AMERICAS · POLITICS", "Senate rejects war-powers bill 51-48",
     "Close vote leaves Iran campaign unchecked."),
    (13, "OCEANIA · CRICKET", "England win ODI series in Hobart",
     "A closing win wraps up the one-day series."),
]

ALSO = [
    "Trump: 'see what happens' on Iran strikes",
    "Takaichi and Putin agree to keep talking",
    "APEC adopts outlook on trade, data and AI",
    "UK and Norway fund £100m naval craft",
    "Bitcoin dips below $63,000, then recovers",
    "Voyager 1 reaches one light-day from Earth",
    "Denmark approves Greenland deal 109-0",
    "LPG tanker Gas Husky sinks off Bulgaria",
    "US gas prices in biggest 3-week dive since 2008",
    "Bangladesh shut down amid unrest, Yunus home ablaze",
    "North Korea expands Yongbyon uranium plant - IAEA",
    "Trump asks top court on Venezuelan protections",
    "Marathon champion Jepchirchir banned 3 years",
    "Canada-China trade gains worth $400m at APEC",
    "879,000 AI chips cleared for China",
    "Nvidia stops H200 chip sales in China",
    "Japan inflation accelerates",
    "Australia jobless rate at 4.9%",
    "South Africa holds rate at 7.25%",
    "Walmart beats forecasts, lifts guidance",
    "Google builds two new TPU chips",
    "Microsoft to package chips at Intel",
    "North Korea unveils AI chatbot",
    "Alcaraz into ATP Finals semi-finals",
    "Chelsea beat PSG 1-0 in Europe",
    "Man City win 2-0",
    "Miami Heat edge Bucks 137-130",
    "Taylor Swift wins first HMMA",
    "Rooftop solar cuts heat deaths - study",
    "Typhoons intensify after heatwaves - study",
    "Students sue over Doritos AI alert",
    "Visa, Mastercard, JPMorgan data leak",
    "USDS stablecoin shrinks 35%",
    "Bitcoin ETF holdings hit record",
    "$500bn Nvidia pledge, $0 delivered",
    "Rio Tinto pledges $250m mine fund",
    "Indonesia passes asset bill",
    "Rockstar names GTA VI voice cast",
    "Fiona the hippo dies at Cincinnati Zoo",
    "150 fall ill in cruise ship outbreak",
]


# --------------------------------------------------------------------------
# Layout: the front page.
# --------------------------------------------------------------------------

M = 16            # page margin
CW = W - 2 * M    # content width (992)


def build(cv):
    # ---- kicker row + rules ----
    cv.text(M, 14, "THE WORLD'S NEWS IN ONE PICTURE", 1, INK, bold=True)
    cv.text_r(M + CW, 14, "53 STORIES · 7 REGIONS · ALL FROM THURSDAY",
              1, RED, bold=True)
    cv.rect(M, 25, CW, 3, INK)
    cv.rect(M, 31, CW, 1, INK)

    # ---- masthead ----
    cv.text_c(W // 2, 38, "Thursday 19 November 2026", 6, INK,
              bold=True, tracking=2)
    cv.rect(M, 88, CW, 1, INK)
    cv.rect(M, 91, CW, 2, RED)

    # ---- region bar ----
    labels = ["%s %d" % (name, n) for name, n, _ in REGIONS]
    mins = [cv.text_w(s, 1) + 22 for s in labels]
    extra = CW - sum(mins)
    total = sum(n for _, n, _ in REGIONS)
    widths, used = [], 0
    for i, (name, n, col) in enumerate(REGIONS):
        if i < len(REGIONS) - 1:
            wdt = mins[i] + extra * n // total
        else:
            wdt = CW - used
        widths.append(wdt)
        used += wdt
    bx = M
    for (name, n, col), s, wdt in zip(REGIONS, labels, widths):
        cv.rect(bx, 98, wdt, 24, col)
        cv.text_c(bx + wdt // 2, 106, s, 1, (255, 255, 255), bold=True)
        bx += wdt

    # ---- stat strip ----
    bounds = [M + i * CW // 6 for i in range(7)]
    for i in range(1, 6):
        cv.line(bounds[i], 128, bounds[i], 174, HAIR, 1)
    for i, (num, cap, col) in enumerate(STATS):
        cx = (bounds[i] + bounds[i + 1]) // 2
        cv.text_c(cx, 130, num, 3, col, bold=True)
        for j, ln in enumerate(wrap(cap, bounds[i + 1] - bounds[i] - 10, 1)):
            cv.text_c(cx, 156 + j * 9, ln, 1, INK_SOFT)
    cv.rect(M, 180, CW, 1, INK)

    # ---- hero stories ----
    hy = 190
    for i, (num, kick, head, body, ill) in enumerate(HEROES):
        x = M + i * 333
        ill(cv, x, hy, 322, 112)
        cv.frame(x, hy, 322, 112, INK, 1)
        cv.rect(x, hy + 120, 22, 20, RED)
        cv.text(x + 5, hy + 123, str(num), 2, (255, 255, 255), bold=True)
        cv.text(x + 30, hy + 126, kick, 1, RED, bold=True)
        for j, ln in enumerate(wrap(head, 322, 2)):
            cv.text(x, hy + 148 + j * 16, ln, 2, INK, bold=True)
        for j, ln in enumerate(wrap(body, 322, 1)):
            cv.text(x, hy + 186 + j * 10, ln, 1, INK_SOFT)

    # ---- numbered story cards 4-13 ----
    cy = 415
    for idx, (num, kick, head, body) in enumerate(CARDS):
        x = M + (idx % 5) * 200
        y = cy + (idx // 5) * 108
        cv.rect(x, y, 192, 100, PAPER_CARD)
        cv.frame(x, y, 192, 100, HAIR, 1)
        cv.rect(x, y, 3, 100, RED)
        nw = cv.text_w(str(num), 2)
        cv.text(x + 10, y + 7, str(num), 2, RED, bold=True)
        cv.text(x + 18 + nw, y + 10, kick, 1, RED, bold=True)
        for j, ln in enumerate(wrap(head, 174, 2)):
            cv.text(x + 10, y + 28 + j * 15, ln, 2, INK, bold=True)
        for j, ln in enumerate(wrap(body, 174, 1)):
            cv.text(x + 10, y + 76 + j * 9, ln, 1, INK_SOFT)

    # ---- markets at the close ----
    my = 635
    cv.rect(M, my, CW, 68, INK)
    cv.text(M + 16, my + 11, "MARKETS AT THE CLOSE", 2, PAPER, bold=True)
    cv.text(M + 16, my + 33, "DOW -1,100 PTS · S&P 500 -2.0% · NASDAQ -2.25%",
            1, PAPER, bold=True)
    cv.text(348, my + 33,
            "WINNERS: ANTHROPIC +34% · LENOVO +48% · INSMED +20.6% · "
            "PALO ALTO +6.4%", 1, (150, 220, 150))
    cv.text(M + 16, my + 51, "LOSER: TAKE-TWO -3.7% ON GTA VI LAUNCH DAY",
            1, (255, 130, 110), bold=True)
    cv.text_r(M + CW - 16, my + 51, "ALL PRICES AT THE CLOSE",
              1, (170, 165, 150))

    # ---- also on Thursday ----
    cv.text(M, 717, "ALSO ON THURSDAY 19 NOVEMBER", 2, INK, bold=True)
    cv.text_r(M + CW, 720, "STORIES 14-53 · IN BRIEF", 1, RED, bold=True)
    cv.rect(M, 737, CW, 2, RED)
    numbered = list(enumerate(ALSO, start=14))
    columns = [numbered[0:14], numbered[14:27], numbered[27:40]]
    list_bottom = 0
    for ci, items in enumerate(columns):
        x = M + ci * 333
        yy = 747
        for num, s in items:
            cv.text(x, yy, "%d." % num, 1, RED, bold=True)
            for j, ln in enumerate(wrap(s, 322 - 24, 1)):
                cv.text(x + 24, yy + j * 10, ln, 1, INK)
            yy += len(wrap(s, 322 - 24, 1)) * 10 + 3
        list_bottom = max(list_bottom, yy)

    # ---- footer ----
    fy = list_bottom + 12
    cv.rect(M, fy, CW, 2, INK)
    cv.text_c(W // 2, fy + 10,
              "Every story here happened or was first reported on "
              "Thursday 19 November 2026.", 1, INK, bold=True)
    cv.text_c(W // 2, fy + 24,
              "Compiled from wire reports, official statements, court "
              "records and company filings.", 1, INK_SOFT)
    return fy + 31


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = Canvas(W, H, PAPER)
    end_y = build(cv)
    save_png(cv, os.path.join(out_dir, "entry.png"))
    print("front page drawn; content ends at y=%d of %d" % (end_y, H))


if __name__ == "__main__":
    main()
