#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Layout: navy masthead with the date, six story cards (icon + headline +
two-line summary) across regions and fields, and a bottom strip with two
more items. All text is rendered with DejaVu/Liberation fonts so it stays
crisp and legible; no AI-generated raster text.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (15, 42, 74)
GREY = (90, 88, 80)
RULE = (200, 194, 178)

F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, box, color, accent):
    """Simple pictogram inside box (x0, y0, x1, y1).
    `color` is the icon's main fill (white on the card's colour panel);
    `accent` is the card's colour, used for inner details so they read."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "missile":
        # drone / missile silhouette with a starburst
        d.polygon([(cx - 8, cy + 26), (cx + 8, cy + 26), (cx + 4, cy - 6),
                   (cx, cy - 30), (cx - 4, cy - 6)], fill=color)
        d.polygon([(cx - 8, cy + 14), (cx - 30, cy + 30), (cx - 8, cy + 24)], fill=color)
        d.polygon([(cx + 8, cy + 14), (cx + 30, cy + 30), (cx + 8, cy + 24)], fill=color)
        for dx, dy in [(-38, -28), (-14, -40), (14, -40), (38, -28), (-44, -2), (44, -2)]:
            d.line([(cx + dx, cy + dy), (cx + dx * 6 // 5, cy + dy * 6 // 5)],
                   fill=color, width=4)
    elif kind == "summit":
        # three leaders' flags as overlapping circles
        cols = [(178, 34, 34), (29, 78, 216), (15, 42, 74)]
        labels = ["US", "CN", "RU"]
        for i, (c, lab) in enumerate(zip(cols, labels)):
            ox = cx - 34 + i * 34
            d.ellipse([ox - 22, cy - 22, ox + 22, cy + 22], fill=c,
                      outline=(255, 255, 255), width=3)
            f = font(F_BOLD, 20)
            tw = d.textlength(lab, font=f)
            d.text((ox - tw / 2, cy - 11), lab, font=f, fill=(255, 255, 255))
        d.line([(cx - 52, cy + 34), (cx + 52, cy + 34)], fill=color, width=4)
    elif kind == "gaza":
        # skyline with a flag
        base = cy + 30
        for bx, bh, bw in [(cx - 46, 52, 22), (cx - 18, 74, 22), (cx + 10, 60, 22),
                           (cx + 36, 40, 14)]:
            d.rectangle([bx, base - bh, bx + bw, base], fill=color)
        d.line([(cx - 52, base), (cx + 54, base)], fill=color, width=4)
        d.line([(cx + 24, base - 74), (cx + 24, base - 104)], fill=color, width=4)
        d.polygon([(cx + 24, base - 104), (cx + 52, base - 96), (cx + 24, base - 88)],
                  fill=(178, 34, 34))
    elif kind == "ballot":
        # ballot box with a check mark
        d.rectangle([cx - 40, cy - 6, cx + 40, cy + 34], fill=color)
        d.rectangle([cx - 18, cy - 14, cx + 18, cy - 6], fill=color)
        d.line([(cx - 28, cy + 14), (cx - 10, cy + 28), (cx + 30, cy - 18)],
               fill=accent, width=6)
    elif kind == "cyclone":
        # spiral of arcs
        for i, r in enumerate(range(8, 46, 6)):
            d.arc([cx - r, cy - r, cx + r, cy + r],
                  start=200 + i * 55, end=200 + i * 55 + 250,
                  fill=color, width=5)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)
    elif kind == "gamepad":
        # game controller
        d.rounded_rectangle([cx - 48, cy - 18, cx + 48, cy + 26], radius=16,
                            fill=color)
        d.rectangle([cx - 34, cy - 6, cx - 18, cy + 10], fill=accent)
        d.rectangle([cx - 30, cy - 2, cx - 22, cy + 6], fill=color)
        for bx, by in [(28, -6), (36, 2), (28, 10), (20, 2)]:
            d.ellipse([cx + bx - 5, cy + by - 5, cx + bx + 5, cy + by + 5],
                      fill=accent)


STORIES = [
    ("MIDDLE EAST", (185, 28, 28), "missile",
     "Iran war escalates",
     "Iran says its drones hit US forces at a Kuwait base; a tanker was struck in Hormuz."),
    ("ASIA-PACIFIC", (29, 78, 216), "summit",
     "Trump in China for three-way talks",
     "Xi and Putin met in Shenzhen before the first three-way summit with the US."),
    ("MIDDLE EAST", (194, 65, 12), "gaza",
     "Israel opens new Gaza operation",
     "Troops enter three areas of central Gaza; mediators say both sides miss ceasefire terms."),
    ("AMERICAS", (109, 40, 217), "ballot",
     "Democrats take the US Senate",
     "Peltola beats Sullivan in Alaska for a projected 56\u201344 Democratic majority."),
    ("SOUTH ASIA", (15, 118, 110), "cyclone",
     "Cyclone Akvan nears India",
     "Thousands shelter in Odisha as the severe storm strengthens in the Bay of Bengal."),
    ("CULTURE", (21, 128, 61), "gamepad",
     "GTA VI launches at midnight",
     "Rockstar's blockbuster arrives 13 years after the last main game in the series."),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
f_title = font(F_SERIF_B, 62)
title = "THE WORLD IN ONE DAY"
tw = d.textlength(title, font=f_title)
d.text(((W - tw) / 2, 22), title, font=f_title, fill=(255, 255, 255))
f_date = font(F_BOLD, 40)
date = "WEDNESDAY  \u00b7  18 NOVEMBER 2026"
tw = d.textlength(date, font=f_date)
d.text(((W - tw) / 2, 96), date, font=f_date, fill=(250, 204, 21))

# ---- subtitle strip ----
f_sub = font(F_SERIF, 24)
sub = "Six stories that defined the day \u2014 from the Gulf to the Pacific"
tw = d.textlength(sub, font=f_sub)
d.text(((W - tw) / 2, 160), sub, font=f_sub, fill=GREY)
d.line([(16, 192), (W - 16, 192)], fill=RULE, width=2)

# ---- story cards: 2 cols x 3 rows ----
CARD_W, CARD_H, GAP, M = 496, 236, 16, 16
TOP = 204
f_tag = font(F_BOLD, 17)
f_head = font(F_BOLD, 29)
f_body = font(F_REG, 21)

for i, (tag, color, icon, head, body) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = M + col * (CARD_W + GAP)
    y0 = TOP + row * (CARD_H + GAP)
    x1, y1 = x0 + CARD_W, y0 + CARD_H
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(255, 255, 255),
                        outline=RULE, width=2)
    # icon panel
    d.rounded_rectangle([x0, y0, x0 + 148, y1], radius=10, fill=color)
    d.rectangle([x0 + 138, y0 + 10, x0 + 148, y1 - 10], fill=color)
    draw_icon(d, icon, (x0 + 18, y0 + 66, x0 + 130, y0 + 178),
              (255, 255, 255), color)
    # text block
    tx = x0 + 164
    tw_text = x1 - tx - 14
    d.text((tx, y0 + 16), tag, font=f_tag, fill=color)
    lines = wrap(d, head, f_head, tw_text)[:2]
    ly = y0 + 44
    for ln in lines:
        d.text((tx, ly), ln, font=f_head, fill=INK)
        ly += 34
    lines = wrap(d, body, f_body, tw_text)
    ly += 6
    for ln in lines[:3]:
        d.text((tx, ly), ln, font=f_body, fill=(64, 62, 56))
        ly += 27

# ---- bottom strip: two more items ----
d.line([(16, 948), (W - 16, 948)], fill=RULE, width=2)
f_bot = font(F_REG, 21)
f_bot_b = font(F_BOLD, 21)
y = 962
d.text((16, y), "ALSO: ", font=f_bot_b, fill=INK)
x = 16 + d.textlength("ALSO: ", font=f_bot_b)
d.text((x, y), "Magnitude 6.0 earthquake strikes Papua New Guinea.",
       font=f_bot, fill=INK)
y = 992
d.text((16, y), "India\u2013US trade deal nearly final; signing delayed.",
       font=f_bot, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png")
