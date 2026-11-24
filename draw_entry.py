#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page as a single 1024x1024 PNG.

Layout (top to bottom), all coordinates in pixels on a 1024x1024 canvas:
  masthead  -> lead story (Nvidia) -> three picture panels -> 33-card grid
  -> footer.  Every string comes from research-24nov.md, reworded here.
The output is fully deterministic: same code, same bytes, every run.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: newsprint cream, near-black ink, one red accent --------------
PAPER = (247, 242, 231)
INK = (26, 26, 26)
SOFT_INK = (74, 74, 66)
RULE = (163, 22, 33)          # masthead red
CARD_BG = (255, 255, 255)
CARD_LINE = (205, 198, 184)
PANEL_BG = (238, 232, 219)
GREEN = (28, 110, 44)         # market gains
BLUE = (31, 78, 121)

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "MIDEAST": (122, 59, 6),
    "ASIA": (46, 107, 52),
    "N. AMERICA": (91, 42, 134),
    "S. AMERICA": (138, 109, 0),
    "AFRICA": (138, 59, 18),
    "OCEANIA": (15, 94, 110),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSans.ttf", 15)
F_LEAD = font("DejaVuSerif-Bold.ttf", 31)
F_DEK = font("DejaVuSans.ttf", 15)
F_STRIP = font("DejaVuSans-Bold.ttf", 14)
F_PANEL_TITLE = font("DejaVuSans-Bold.ttf", 14)
F_PANEL_BODY = font("DejaVuSans.ttf", 12)
F_PANEL_BIG = font("DejaVuSans-Bold.ttf", 17)
F_TAG = font("DejaVuSans-Bold.ttf", 9)
F_CARD = font("DejaVuSans.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_masthead(d):
    d.text((W // 2, 34), "THE WORLD TODAY", font=F_TITLE, fill=INK, anchor="mt")
    d.text((W // 2, 82), "Tuesday, November 24, 2026  ·  One page, 37 stories, 7 regions",
           font=F_DATE, fill=SOFT_INK, anchor="mt")
    d.line([(24, 104), (1000, 104)], fill=RULE, width=4)
    d.line([(24, 110), (1000, 110)], fill=RULE, width=1)


def draw_lead(d):
    y = 122
    d.text((24, y), "MARKETS ROAR BACK", font=F_STRIP, fill=RULE)
    d.text((1000, y), "LEAD STORY", font=F_STRIP, fill=SOFT_INK, anchor="rt")
    y += 26
    headline = "Nvidia brings Huang back; shares jump 31%"
    for line in wrap(d, headline, F_LEAD, 976):
        d.text((24, y), line, font=F_LEAD, fill=INK)
        y += 36
    dek = ("The board reverses the chief executive's 11-day-old exit after "
           "pressure from President Trump. Nasdaq posts its best day since "
           "April 2025; Nvidia adds about $952 billion in a day.")
    for line in wrap(d, dek, F_DEK, 976):
        d.text((24, y), line, font=F_DEK, fill=SOFT_INK)
        y += 20
    y += 6
    strip = "NASDAQ +6.5%    S&P 500 +4.7%    DOW +3.0%    NVIDIA +31.5%    BITCOIN $61,300"
    d.rectangle([24, y, 1000, y + 26], fill=INK)
    d.text((512, y + 13), strip, font=F_STRIP, fill=PAPER, anchor="mm")
    return y + 40


# --- the 33 grid stories: (region, headline) -------------------------------
STORIES = [
    ("EUROPE", "Poland confirms three Russian missiles hit its soil; NATO sends spy plane"),
    ("EUROPE", "Germany signs on to Ukraine's Delta battle system"),
    ("EUROPE", "Bomb threats emailed to about 450 German schools"),
    ("EUROPE", "Von der Leyen: EU to bar visas for ex-Russian fighters"),
    ("EUROPE", "Zelenskyy: Ukraine ready for four-way peace talks"),
    ("EUROPE", "Drone hits Russian cargo ship in Baltic; Finland on alert"),
    ("MIDEAST", "Iran vows to use all tools against US naval blockade"),
    ("MIDEAST", "US sanctions dozens tied to Iran shadow banking"),
    ("MIDEAST", "Two tankers struck in Strait of Hormuz; no casualties"),
    ("MIDEAST", "Houthis claim strike on Saudi Rabigh refinery"),
    ("MIDEAST", "Israeli strikes kill three in Gaza, incl. UN worker"),
    ("MIDEAST", "Gaza soil and water poisoned for decades, report says"),
    ("ASIA", "South Korea picks first woman spy chief"),
    ("ASIA", "China sentences official to death for spying"),
    ("ASIA", "Kim: North Korea seeks security, not supremacy"),
    ("ASIA", "Nepal PM meets Modi on first India visit"),
    ("ASIA", "India pledges $1.62bn to rebuild Nepal"),
    ("ASIA", "Indonesia factory fire: search goes on"),
    ("ASIA", "ICJ: Myanmar guilty of Rohingya genocide, 9-6"),
    ("ASIA", "Lahore tops pollution ranking as AQI passes 500"),
    ("N. AMERICA", "Democrats win House majority, 258+ seats, most since 1992"),
    ("N. AMERICA", "Trump orders Army to pause Iowa toxic blast"),
    ("N. AMERICA", "22 states sue over housing aid rule"),
    ("N. AMERICA", "O'Hare ground stop amid Thanksgiving rush"),
    ("N. AMERICA", "US loses measles-elimination status"),
    ("N. AMERICA", "Anthropic shares slip while AI stocks rally"),
    ("N. AMERICA", "Waymo pulls robotaxis from US freeways"),
    ("N. AMERICA", "Trump targets Newsom over death-row commutations"),
    ("S. AMERICA", "Bolsonaro rushed to ICU with bowel blockage"),
    ("S. AMERICA", "Colombia: drone hits police base, civilians hurt"),
    ("AFRICA", "Senegal rescues about 1,000 migrants at sea"),
    ("AFRICA", "Oil falls 3% as Libya pipeline restarts"),
    ("OCEANIA", "COP flop: Australia faces backlash"),
]


def draw_grid(d, top):
    x0, cols, rows = 24, 3, 11
    cw, ch, gap = 318, 50, 11
    for i, (region, headline) in enumerate(STORIES):
        col, row = i % cols, i // cols
        x = x0 + col * (cw + gap)
        y = top + row * (ch + 2)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD_BG, outline=CARD_LINE, width=1)
        d.text((x + 8, y + 6), region, font=F_TAG, fill=REGION_COLORS[region])
        lines = wrap(d, headline, F_CARD, cw - 16)[:2]
        ly = y + 20
        for line in lines:
            d.text((x + 8, ly), line, font=F_CARD, fill=INK)
            ly += 15
    return top + rows * ch + (rows - 1) * 2


def draw_panels(d, top):
    """Three picture panels: a Bitcoin chart, a ship at sea, a globe."""
    pw, ph, gap = 318, 140, 11
    titles = ["MARKETS", "WAR AT SEA", "CLIMATE"]
    for i, title in enumerate(titles):
        x = 24 + i * (pw + gap)
        d.rectangle([x, top, x + pw, top + ph], fill=PANEL_BG, outline=CARD_LINE, width=1)
        d.text((x + 10, top + 7), title, font=F_PANEL_TITLE, fill=RULE)
    # Panel 1: Bitcoin rebound chart, $55,130 low -> $64,505 high -> $61,300.
    x = 24
    pts = [(x + 14, top + 128), (x + 70, top + 118), (x + 120, top + 132),
           (x + 175, top + 96), (x + 235, top + 62), (x + 290, top + 52),
           (x + 304, top + 74)]
    d.line(pts, fill=GREEN, width=3)
    d.ellipse([x + 296, top + 44, x + 312, top + 60], fill=GREEN)
    d.text((x + 12, top + 26), "BITCOIN +17%", font=F_PANEL_BIG, fill=INK)
    d.text((x + 12, top + 48), "Low $55,130  ·  High $64,505", font=F_PANEL_BODY, fill=SOFT_INK)
    d.text((x + 12, top + 66), "Settles near $61,300", font=F_PANEL_BODY, fill=SOFT_INK)
    # Panel 2: corvette silhouette on waves, struck by a drone.
    x = 24 + pw + gap
    d.polygon([(x + 40, top + 118), (x + 280, top + 118), (x + 258, top + 96),
               (x + 60, top + 96)], fill=BLUE)                       # hull
    d.rectangle([x + 130, top + 66, x + 138, top + 96], fill=BLUE)   # mast
    d.polygon([(x + 138, top + 66), (x + 178, top + 88), (x + 138, top + 88)],
              fill=BLUE)                                             # bridge
    for wx in range(0, 300, 42):                                     # waves
        d.arc([x + 10 + wx, top + 122, x + 46 + wx, top + 140], 0, 180, fill=BLUE, width=2)
    d.text((x + 12, top + 26), "Ukraine drones sink", font=F_PANEL_BIG, fill=INK)
    d.text((x + 12, top + 48), "Russian corvette off Libya", font=F_PANEL_BIG, fill=INK)
    # Panel 3: globe with a crack — COP31 collapses with no deal.
    x = 24 + 2 * (pw + gap)
    cx, cy, r = x + 84, top + 96, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    d.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=BLUE, width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=BLUE, width=2)
    d.line([(cx - 30, cy - 30), (cx + 6, cy + 2), (cx - 8, cy + 26),
            (cx + 28, cy + 34)], fill=RULE, width=3)                 # crack
    d.text((x + 140, top + 30), "COP31", font=F_PANEL_BIG, fill=INK)
    d.text((x + 140, top + 52), "talks collapse", font=F_PANEL_BODY, fill=SOFT_INK)
    d.text((x + 140, top + 68), "with no deal", font=F_PANEL_BODY, fill=SOFT_INK)
    d.text((x + 140, top + 88), "in Turkey", font=F_PANEL_BODY, fill=SOFT_INK)
    return top + ph


def draw_footer(d, y):
    d.line([(24, y), (1000, y)], fill=CARD_LINE, width=1)
    d.text((512, y + 8),
           "37 stories · 7 regions · Sources: Reuters, CNN, CoinDesk, Finnhub, BBC",
           font=F_FOOT, fill=SOFT_INK, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_lead(d)
    y = draw_panels(d, y + 8)
    y = draw_grid(d, y + 10)
    draw_footer(d, y + 4)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
