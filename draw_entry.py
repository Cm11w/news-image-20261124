#!/usr/bin/env python3
"""Rebuild of the news-image-20261124 entry (post-opening session,
Tuesday 24 Nov 2026 ~07:10 WIB).

Draws one 1024x1024 PNG: a newspaper front page summing up Tuesday
24 November 2026 world news. Masthead names the date; one full-width
lead (Nvidia reinstates Jensen Huang, shares close +31%); a 3x13 grid
of 39 short stories across 10 regions, three of them drawn panels
(Bitcoin chart, Russian corvette, US ballot box); a one-line source
footer. All text is plain ASCII; any text that would overflow its box
aborts the run instead of drawing outside it.

Numbers are the Tuesday-morning snapshot (see research-24nov.md,
REFRESH section): Nvidia's Monday close, not the intraday peak;
Bitcoin's $64,505 local high, not its Monday close. Deterministic:
fixed fonts and layout, no clock, no randomness, so two runs write
byte-identical PNG output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

# Canvas size, fixed by the competition (at most 1024 by 1024).
W, H = 1024, 1024

# ---- palette: warm paper, navy masthead, one accent per region -------
PAPER = (248, 244, 237)
INK = (24, 28, 36)
NAVY = (18, 32, 58)
GOLD = (233, 186, 78)
CARD = (255, 255, 255)
EDGE = (216, 208, 194)
MUTED = (98, 102, 112)
WHITE = (255, 255, 255)
LIGHT = (206, 213, 225)
RED = (176, 32, 32)
BLUE = (26, 80, 142)
BROWN = (124, 76, 20)
TEAL = (14, 112, 111)
PURPLE = (90, 46, 122)
GREEN = (36, 112, 54)
ROSE = (178, 50, 98)
OCHRE = (192, 142, 12)
ORANGE = (202, 92, 32)
SLATE = (52, 68, 92)
NV_GREEN = (96, 150, 0)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        raise SystemExit("missing font: %s" % path)
    return ImageFont.truetype(path, size)


# Font handles, filled in main() so the module stays import-safe.
F_TITLE = None
F_DATE = None
F_KICKER = None
F_SUB = None
F_TAG = None
F_HEAD = None
F_BODY = None
F_MINI = None
F_DRAW = None
F_FOOT = None


def check_ascii(text, where):
    for ch in text:
        if ord(ch) > 127:
            raise SystemExit("non-ASCII char %r in %s" % (ch, where))


def wrap(draw, text, font, max_w):
    """Greedy word wrap; aborts if one word alone is wider than max_w."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if not cur:
                raise SystemExit("word too wide for its box: %r" % word)
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_w, max_lines, line_h, fill):
    """Draw wrapped text; abort if it needs more than max_lines lines."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) > max_lines:
        raise SystemExit(
            "text overflow: %d lines > %d allowed: %r"
            % (len(lines), max_lines, text[:60])
        )
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=font, fill=fill)
    return y + len(lines) * line_h


def tag_chip(draw, x, y, label, colour):
    """Small filled region tag; returns the width it used."""
    pad_x, pad_y = 8, 2
    w = int(draw.textlength(label, font=F_TAG)) + 2 * pad_x
    h = F_TAG.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=colour)
    draw.text((x + pad_x, y + pad_y - 1), label, font=F_TAG, fill=WHITE)
    return w, h


def draw_lead(draw, box):
    """Full-width lead card: tag, kicker, headline, four-line body."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                           outline=EDGE, width=2)
    draw.rounded_rectangle([x0, y0, x0 + 10, y1], radius=5, fill=NV_GREEN)
    inner_x = x0 + 28
    inner_w = x1 - inner_x - 24
    y = y0 + 12
    tag_w, tag_h = tag_chip(draw, inner_x, y, "TECH - NVIDIA", NV_GREEN)
    draw.text((inner_x + tag_w + 12, y + 1),
              "Board reverses itself - Trump claims credit",
              font=F_SUB, fill=MUTED)
    y += tag_h + 6
    head = "Nvidia brings back Huang as shares jump 31%"
    y = draw_wrapped(draw, head, F_HEAD, inner_x, y, inner_w, 1, 34, INK)
    y += 6
    body = (
        "Nvidia's board unanimously reinstated Jensen Huang as chief "
        "executive on Monday, 11 days after he resigned over affairs "
        "including one with a woman US officials suspect is a Chinese "
        "spy. Trump pressed the board and claimed credit; an inquiry "
        "continues. Nvidia shares closed up 31% - their best day since "
        "2003 - adding $952 billion, and Bitcoin rebounded 17% off its "
        "low to $64,505."
    )
    y = draw_wrapped(draw, body, F_BODY, inner_x, y, inner_w, 4, 21, INK)
    if y > y1 - 8:
        raise SystemExit("lead card overflow: text bottom %d > %d"
                         % (y, y1 - 8))


def draw_cell(draw, box, tag, colour, head):
    """One dense grid cell: region tag on top, headline below (2 lines)."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=EDGE, width=1)
    inner_x = x0 + 12
    inner_w = x1 - inner_x - 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    y = draw_wrapped(draw, head, F_MINI, inner_x, y0 + 19, inner_w,
                     2, 14, INK)
    if y > y1 - 1:
        raise SystemExit("cell %s overflow: text bottom %d > %d"
                         % (tag, y, y1 - 1))


def draw_chart(draw, box, tag, colour, head):
    """Drawn panel: tag, Bitcoin sparkline, one-line headline."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=EDGE, width=1)
    inner_x = x0 + 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    # Sparkline of the day's arc: Sat low 55,130 - Mon morning 61,424
    # - Mon high 64,505 (Bitstamp). Points are joined straight.
    vals = [55130, 61424, 64505]
    lo, hi = min(vals), max(vals)
    cx0, cx1 = inner_x, x1 - 62
    cy0, cy1 = y0 + 20, y0 + 31
    pts = []
    for i, v in enumerate(vals):
        px = cx0 + i * (cx1 - cx0) // 2
        py = cy1 - (v - lo) * (cy1 - cy0) // (hi - lo)
        pts.append((px, py))
    draw.line(pts, fill=BLUE, width=2)
    draw.ellipse([pts[-1][0] - 3, pts[-1][1] - 3,
                  pts[-1][0] + 3, pts[-1][1] + 3], fill=BLUE)
    draw.text((x1 - 58, y0 + 19), "$64.5k", font=F_DRAW, fill=BLUE)
    y = draw_wrapped(draw, head, F_DRAW, inner_x, y0 + 33,
                     x1 - inner_x - 12, 1, 14, INK)
    if y > y1 - 1:
        raise SystemExit("chart panel overflow: %d > %d" % (y, y1 - 1))


def draw_warship(draw, box, tag, colour, head):
    """Drawn panel: tag, corvette pictogram with blast, headline."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=EDGE, width=1)
    inner_x = x0 + 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    # Mast, superstructure, hull.
    draw.line([(inner_x + 48, y0 + 20), (inner_x + 48, y0 + 12)],
              fill=SLATE, width=2)
    draw.rectangle([inner_x + 36, y0 + 20, inner_x + 60, y0 + 25],
                   fill=SLATE)
    draw.polygon([(inner_x + 12, y0 + 25), (inner_x + 84, y0 + 25),
                  (inner_x + 76, y0 + 31), (inner_x + 20, y0 + 31)],
                 fill=NAVY)
    # Blast starburst above the bow.
    bx, by = inner_x + 78, y0 + 16
    for dx, dy in [(0, -6), (5, -4), (6, 0), (5, 4), (0, 6),
                   (-5, 4), (-6, 0), (-5, -4)]:
        draw.line([(bx, by), (bx + dx, by + dy)], fill=RED, width=2)
    draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=RED)
    # Waterline.
    draw.line([(inner_x, y0 + 32), (x1 - 12, y0 + 32)], fill=TEAL, width=1)
    y = draw_wrapped(draw, head, F_DRAW, inner_x, y0 + 33,
                     x1 - inner_x - 12, 1, 14, INK)
    if y > y1 - 1:
        raise SystemExit("warship panel overflow: %d > %d" % (y, y1 - 1))


def draw_ballot(draw, box, tag, colour, head):
    """Drawn panel: tag, ballot-box pictogram, headline."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=EDGE, width=1)
    inner_x = x0 + 12
    tag_chip(draw, inner_x, y0 + 2, tag, colour)
    # Ballot box with a ticked slip.
    bx0, by0, bx1, by1 = inner_x + 6, y0 + 20, inner_x + 26, y0 + 32
    draw.rectangle([bx0, by0, bx1, by1], outline=NAVY, width=2)
    draw.line([(bx0 + 4, by0 + 3), (bx1 - 4, by0 + 3)], fill=NAVY, width=2)
    draw.line([(bx0 + 3, by0 + 8), (bx0 + 8, by0 + 11),
               (bx0 + 15, by0 + 3)], fill=GREEN, width=2)
    draw.text((bx1 + 8, y0 + 20), "258+ seats - most since 1992",
              font=F_DRAW, fill=INK)
    y = draw_wrapped(draw, head, F_DRAW, inner_x, y0 + 33,
                     x1 - inner_x - 12, 1, 14, INK)
    if y > y1 - 1:
        raise SystemExit("ballot panel overflow: %d > %d" % (y, y1 - 1))


# Refresh decisions, Tuesday morning (~07:10 WIB): the lead uses
# Nvidia's Monday CLOSE (+31%, +$952bn), not the +35% intraday peak
# the first research pass quoted; the Bitcoin panel keeps the $64,505
# intraday high because that is the day's arc the chart draws. Two
# grid cards were swapped for fresher stories: Zelenskyy's four-way
# peace talks offer replaces the EU digital-tax pitch, and the
# Anthropic IPO contrast replaces the vague US weather warning.
# (kind, tag, colour, headline) — kind: "cell", "chart", "warship",
# "ballot". Lead story is drawn separately; these 39 make 40 total.
STORIES = [
    ("cell", "EUROPE", BLUE, "Poland confirms 3 Russian missiles; NATO Council meets"),
    ("cell", "EUROPE", BLUE, "Germany: 450 schools get emailed bomb threats"),
    ("cell", "EUROPE", BLUE, "EU warns of personal data leak after cyberattack"),
    ("cell", "EUROPE", BLUE, "Von der Leyen: EU to bar visas for ex-Russian fighters"),
    ("cell", "EUROPE", BLUE, "Spain polls put right ahead of Nov 29 snap vote"),
    ("cell", "EUROPE", BLUE, "128 nations agree to draft rules on killer robots"),
    ("cell", "EUROPE", BLUE, "Zelenskyy: Ukraine ready for four-way peace talks"),
    ("cell", "EUROPE", BLUE, "Drone hits Russian cargo ship in Baltic; Finland on alert"),
    ("cell", "EUROPE", BLUE, "Dymer drone toll reaches 11; boy pulled from rubble"),
    ("cell", "MIDEAST", BROWN, "Three tankers ablaze after mine blasts in Hormuz"),
    ("cell", "MIDEAST", BROWN, "Houthis claim strike on Saudi Rabigh refinery"),
    ("cell", "MIDEAST", BROWN, "Iran truck drivers strike over crumbling economy"),
    ("cell", "MIDEAST", BROWN, "Bahrain: two hurt as Iran strike hits civilian site"),
    ("cell", "MIDEAST", BROWN, "Trump dares Iran to test Hormuz blockade"),
    ("cell", "MIDEAST", BROWN, "Istanbul: thousands protest TV raid crackdown"),
    ("cell", "E. ASIA", TEAL, "South Korea picks first woman spy chief"),
    ("cell", "E. ASIA", TEAL, "China sentences official to death for spying"),
    ("cell", "E. ASIA", TEAL, "Kim: North Korea seeks security, not supremacy"),
    ("cell", "S. ASIA", PURPLE, "Nepal PM meets Modi on first India visit"),
    ("cell", "S. ASIA", PURPLE, "India pledges $1.62bn to rebuild Nepal"),
    ("cell", "S. ASIA", PURPLE, "Bangladesh: Hasina to be jailed if she returns"),
    ("cell", "SE ASIA", GREEN, "Indonesia factory fire: search goes on"),
    ("ballot", "N. AMERICA", ROSE, "Democrats win House majority"),
    ("cell", "N. AMERICA", ROSE, "Trump delays Iowa toxic blast to Nov 25"),
    ("cell", "N. AMERICA", ROSE, "22 states sue over housing aid rule"),
    ("cell", "N. AMERICA", ROSE, "Labor Dept finalizes contractor test"),
    ("cell", "N. AMERICA", ROSE, "US loses measles-elimination status"),
    ("cell", "N. AMERICA", ROSE, "Columbus: two bus drivers killed in crash"),
    ("cell", "N. AMERICA", ROSE, "Broncos star Tom Jackson dies at 75"),
    ("cell", "N. AMERICA", ROSE, "Carney stages Trump impersonator in Ottawa"),
    ("cell", "MARKETS", RED, "Anthropic shares slip while AI stocks rally"),
    ("cell", "N. AMERICA", ROSE, "Storms threaten Thanksgiving travel"),
    ("cell", "S. AMERICA", OCHRE, "Bolsonaro rushed to ICU with bowel blockage"),
    ("cell", "S. AMERICA", OCHRE, "Colombia: drone hits police base, civilians hurt"),
    ("cell", "S. AMERICA", OCHRE, "Colombia charges Starlink over prison comms"),
    ("cell", "AFRICA", ORANGE, "Senegal rescues about 1,000 migrants at sea"),
    ("cell", "AFRICA", ORANGE, "Oil falls 3% as Libya pipeline restarts"),
    ("warship", "WAR", SLATE, "Ukraine drones sink Russian corvette"),
    ("chart", "MARKETS", RED, "Bitcoin rebounds 17% to $64,505"),
]

DRAWERS = {"cell": draw_cell, "chart": draw_chart,
           "warship": draw_warship, "ballot": draw_ballot}


def main():
    global F_TITLE, F_DATE, F_KICKER, F_SUB, F_TAG
    global F_HEAD, F_BODY, F_MINI, F_DRAW, F_FOOT

    F_TITLE = load_font("NotoSans-Bold.ttf", 52)
    F_DATE = load_font("NotoSans-Bold.ttf", 26)
    F_KICKER = load_font("NotoSans-Bold.ttf", 18)
    F_SUB = load_font("NotoSans-Regular.ttf", 19)
    F_TAG = load_font("NotoSans-Bold.ttf", 11)
    F_HEAD = load_font("NotoSans-Bold.ttf", 28)
    F_BODY = load_font("NotoSans-Regular.ttf", 17)
    F_MINI = load_font("NotoSans-Bold.ttf", 13)
    F_DRAW = load_font("NotoSans-Bold.ttf", 13)
    F_FOOT = load_font("NotoSans-Regular.ttf", 16)

    if len(STORIES) != 39:
        raise SystemExit("story count must be 39 cells + lead = 40, got %d"
                         % len(STORIES))

    texts = [
        "THE WORLD IN ONE IMAGE",
        "WORLD NEWS",
        "Tuesday, November 24, 2026",
        "40 stories - 10 regions - 3 drawn - as reported on Tuesday",
    ]
    for t in texts:
        check_ascii(t, "masthead")
    for kind, tag, colour, head in STORIES:
        check_ascii(head, "story head " + tag)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead: navy band, gold date, subline top right -----------
    mast_h = 116
    draw.rectangle([0, 0, W, mast_h], fill=NAVY)
    draw.rectangle([0, mast_h - 4, W, mast_h], fill=GOLD)
    draw.text((36, 8), "THE WORLD IN ONE IMAGE",
              font=F_KICKER, fill=GOLD)
    draw.text((36, 24), "WORLD NEWS", font=F_TITLE, fill=WHITE)
    draw.text((36, 80), "Tuesday, November 24, 2026",
              font=F_DATE, fill=GOLD)
    sub = "40 stories - 10 regions - 3 drawn - as reported on Tuesday"
    sub_w = draw.textlength(sub, font=F_SUB)
    draw.text((W - 36 - sub_w, 12), sub, font=F_SUB, fill=LIGHT)

    # ---- lead story, full width ---------------------------------------
    draw_lead(draw, (36, 124, W - 36, 292))

    # ---- 3-column grid, 13 rows ---------------------------------------
    gx0, gy0 = 36, 300
    gw, gh, gap = 309, 48, 4
    for i, (kind, tag, colour, head) in enumerate(STORIES):
        col = i % 3
        row = i // 3
        x0 = gx0 + col * (gw + 12)
        y0 = gy0 + row * (gh + gap)
        DRAWERS[kind](draw, (x0, y0, x0 + gw, y0 + gh), tag, colour, head)

    # ---- footer: sources, centred --------------------------------------
    foot = ("Sources: Reuters - AP - BBC - TechCrunch - Cointelegraph - "
            "Al Jazeera  |  Reported Tuesday, Nov 24, 2026")
    check_ascii(foot, "footer")
    fw = draw.textlength(foot, font=F_FOOT)
    if fw > W - 72:
        raise SystemExit("footer too wide: %d" % fw)
    draw.text(((W - fw) / 2, 984), foot, font=F_FOOT, fill=MUTED)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (OUT_PATH, W, H))


if __name__ == "__main__":
    main()
