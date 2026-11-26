"""Draw the 26 November 2026 world-news front page.

Deterministic, offline, stdlib + Pillow only. No timestamps, no random
numbers, no network. Run:  python3 generate.py  (writes entry.png here)
Layout (1024x1024): masthead, a top band of the 3 biggest stories, a 2x4
grid of numbered, badged panels, and a ticker strip at the bottom.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 232)
INK = (22, 32, 46)
NAVY = (27, 58, 88)
RED = (176, 42, 30)
TEAL = (16, 104, 99)
GOLD = (168, 116, 26)
GREY = (96, 100, 108)
LIGHT = (233, 227, 212)
WHITE = (255, 255, 255)
SKY = (178, 205, 224)
SAND = (226, 205, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def pill(draw, x, y, label, fill):
    """Small rounded badge; returns width used."""
    fnt = font(SANS_B, 10)
    w = int(draw.textlength(label, font=fnt)) + 14
    draw.rounded_rectangle([x, y, x + w, y + 17], radius=8, fill=fill)
    draw.text((x + 7, y + 3), label, font=fnt, fill=WHITE)
    return w


# ---------------------------------------------------------------- scenes
def scene(draw, key, x0, y0, w, h):
    """Flat illustration for one panel, drawn from simple shapes."""
    if key == "missile":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 46, 66))
        for sx, sy in ((18, 20), (70, 12), (105, 34)):
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=WHITE)
        draw.polygon([(x0 + 20, y0 + 108), (x0 + 34, y0 + 118),
                      (x0 + 48, y0 + 108), (x0 + 48, y0 + 128),
                      (x0 + 20, y0 + 128)], fill=INK)
        draw.polygon([(x0 + 60, y0 + 66), (x0 + 66, y0 + 52),
                      (x0 + 72, y0 + 66)], fill=(220, 120, 40))
        draw.rectangle([x0 + 62, y0 + 66, x0 + 70, y0 + 96], fill=(200, 200, 205))
        draw.line([x0 + 58, y0 + 100, x0 + 50, y0 + 118], fill=(240, 200, 90), width=3)
        draw.line([x0 + 74, y0 + 100, x0 + 84, y0 + 116], fill=(240, 200, 90), width=3)
        draw.ellipse([x0 + 88, y0 + 40, x0 + 112, y0 + 64], fill=(255, 190, 60))
    elif key == "tanker":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
        draw.rectangle([x0, y0 + 84, x0 + w, y0 + h], fill=(36, 90, 120))
        draw.rectangle([x0 + 14, y0 + 58, x0 + 104, y0 + 88], fill=(150, 40, 32))
        draw.rectangle([x0 + 78, y0 + 38, x0 + 100, y0 + 58], fill=(230, 225, 210))
        draw.ellipse([x0 + 52, y0 + 30, x0 + 78, y0 + 56], fill=(255, 190, 60))
        draw.ellipse([x0 + 58, y0 + 36, x0 + 72, y0 + 50], fill=(240, 120, 40))
        for wy in (98, 116):
            draw.arc([x0 + 10, y0 + wy, x0 + 40, y0 + wy + 16], 0, 180,
                     fill=WHITE, width=3)
    elif key == "building":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 196, 160))
        draw.rectangle([x0 + 34, y0 + 26, x0 + 84, y0 + 128], fill=(120, 110, 96))
        for ry in (38, 58, 78, 98):
            for cx in (44, 62):
                draw.rectangle([x0 + cx, y0 + ry, x0 + cx + 10, y0 + ry + 12],
                               fill=(255, 220, 120))
        draw.polygon([(x0 + 88, y0 + 18), (x0 + 104, y0 + 34),
                      (x0 + 120, y0 + 18)], fill=RED)
        draw.ellipse([x0 + 14, y0 + 20, x0 + 30, y0 + 36], fill=(255, 170, 50))
    elif key == "refinery":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(38, 44, 54))
        draw.rectangle([x0 + 18, y0 + 84, x0 + 46, y0 + 128], fill=(150, 150, 155))
        draw.rectangle([x0 + 56, y0 + 96, x0 + 92, y0 + 128], fill=(110, 112, 118))
        draw.polygon([(x0 + 96, y0 + 128), (x0 + 104, y0 + 52),
                      (x0 + 112, y0 + 128)], fill=(90, 92, 98))
        draw.ellipse([x0 + 94, y0 + 34, x0 + 114, y0 + 54], fill=(255, 170, 50))
        draw.ellipse([x0 + 99, y0 + 40, x0 + 109, y0 + 50], fill=(255, 220, 90))
        draw.rectangle([x0 + 22, y0 + 96, x0 + 42, y0 + 104], fill=(255, 200, 80))
    elif key == "office":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 220, 204))
        draw.rectangle([x0 + 30, y0 + 22, x0 + 88, y0 + 128], fill=(110, 84, 52))
        draw.rectangle([x0 + 40, y0 + 34, x0 + 78, y0 + 128], fill=(70, 96, 110))
        draw.ellipse([x0 + 70, y0 + 78, x0 + 76, y0 + 84], fill=(255, 220, 90))
        draw.rectangle([x0 + 96, y0 + 16, x0 + 100, y0 + 60], fill=(120, 120, 120))
        draw.polygon([(x0 + 96, y0 + 16), (x0 + 116, y0 + 24),
                      (x0 + 96, y0 + 32)], fill=RED)
        draw.rectangle([x0 + 14, y0 + 104, x0 + 30, y0 + 128], fill=(150, 140, 120))
    elif key == "court":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(210, 208, 196))
        draw.polygon([(x0 + 16, y0 + 44), (x0 + 64, y0 + 14),
                      (x0 + 112, y0 + 44)], fill=(90, 84, 74))
        for cx in (26, 50, 74, 98):
            draw.rectangle([x0 + cx, y0 + 48, x0 + cx + 8, y0 + 108],
                           fill=(240, 236, 222))
        draw.rectangle([x0 + 12, y0 + 108, x0 + 116, y0 + 118], fill=(90, 84, 74))
        draw.rectangle([x0 + 52, y0 + 84, x0 + 76, y0 + 108], fill=(70, 70, 78))
    elif key == "mercury":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 20, 34))
        for sx, sy in ((14, 18), (96, 26), (40, 40), (112, 78), (20, 92)):
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=WHITE)
        draw.ellipse([x0 + 26, y0 + 52, x0 + 26, y0 + 52], fill=WHITE)
        draw.ellipse([x0 + 34, y0 + 48, x0 + 102, y0 + 116], fill=(188, 164, 140))
        for cx, cy, r in ((52, 66, 5), (78, 88, 7), (88, 62, 4), (60, 96, 4)):
            draw.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                         fill=(140, 116, 96))
        draw.arc([x0 + 8, y0 + 30, x0 + 120, y0 + 130], 200, 340,
                 fill=(120, 180, 220), width=3)
        draw.polygon([(x0 + 96, y0 + 112), (x0 + 108, y0 + 104),
                      (x0 + 112, y0 + 118)], fill=(120, 180, 220))
    elif key == "chess":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 228, 200))
        cell = 16
        for r in range(8):
            for c in range(8):
                if (r + c) % 2:
                    draw.rectangle([x0 + c * cell, y0 + r * cell,
                                    x0 + (c + 1) * cell, y0 + (r + 1) * cell],
                                   fill=(70, 70, 74))
        draw.ellipse([x0 + 40, y0 + 18, x0 + 56, y0 + 34], fill=INK)
        draw.rectangle([x0 + 38, y0 + 34, x0 + 58, y0 + 42], fill=INK)
        draw.ellipse([x0 + 72, y0 + 82, x0 + 88, y0 + 98], fill=WHITE,
                     outline=INK, width=2)
        draw.rectangle([x0 + 70, y0 + 98, x0 + 90, y0 + 106], fill=WHITE,
                       outline=INK, width=2)
    elif key == "cricket":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(88, 140, 74))
        draw.rectangle([x0, y0 + 96, x0 + w, y0 + 128], fill=(196, 178, 130))
        draw.polygon([(x0 + 52, y0 + 30), (x0 + 62, y0 + 26),
                      (x0 + 78, y0 + 78), (x0 + 68, y0 + 82)], fill=(196, 164, 110))
        draw.ellipse([x0 + 88, y0 + 30, x0 + 104, y0 + 46], fill=RED)
        draw.line([x0 + 20, y0 + 96, x0 + 108, y0 + 96], fill=WHITE, width=3)
        for sx in (30, 60, 90):
            draw.rectangle([x0 + sx, y0 + 78, x0 + sx + 3, y0 + 96],
                           fill=(255, 220, 120))
    elif key == "truck":
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 214, 188))
        draw.rectangle([x0 + 12, y0 + 52, x0 + 78, y0 + 96], fill=(196, 120, 40))
        draw.rectangle([x0 + 82, y0 + 64, x0 + 108, y0 + 96], fill=(150, 40, 32))
        draw.rectangle([x0 + 88, y0 + 70, x0 + 102, y0 + 82], fill=SKY)
        for cx in (30, 62, 94):
            draw.ellipse([x0 + cx, y0 + 94, x0 + cx + 18, y0 + 112],
                         fill=INK)
        draw.ellipse([x0 + 92, y0 + 20, x0 + 112, y0 + 40], fill=(255, 190, 60))
        draw.polygon([(x0 + 22, y0 + 30), (x0 + 30, y0 + 44),
                      (x0 + 14, y0 + 44)], fill=(240, 120, 40))


# ---------------------------------------------------------------- content
TOP_BAND = [
    ("RED SEA WAR", RED, "3 CITIES",
     "Houthi-Saudi escalation: missiles over Riyadh",
     "Air defences intercept a missile over Riyadh; a projectile hits "
     "Jazan port, a drone over Jeddah.",
     "Reuters \u00b7 Saudi authorities"),
    ("STRAIT OF HORMUZ", NAVY, "2 TANKERS",
     "Two tankers struck by sea mines",
     "Two tankers are hit by mines in the Strait of Hormuz, the busiest "
     "oil chokepoint.",
     "Reuters"),
    ("UKRAINE WAR", TEAL, "~500,000",
     "Russia's war toll nears half a million",
     "Reported Russian casualties in the Ukraine war reach about 500,000, "
     "new figures show.",
     "Reported figures"),
]

PANELS = [
    ("1", "MIDDLE EAST", RED, "REPORTED", "missile",
     "Israel strikes Hamas official in Gaza",
     "A strike targets a senior Hamas figure in Gaza as the war grinds on.",
     "Reuters", None),
    ("2", "UKRAINE WAR", NAVY, "REPORTED", "refinery",
     "Ukraine hits Russian oil refinery",
     "Kyiv strikes a refinery deep inside Russia in its long-range campaign.",
     "Reuters", None),
    ("3", "KOREA", TEAL, "CONFIRMED", "office",
     "Pyongyang orders Swiss office to shut",
     "North Korea tells Switzerland's office in the capital to close.",
     "AP", None),
    ("4", "UNITED STATES", NAVY, "CONFIRMED", "court",
     "Second judge blocks birthright order",
     "Another US judge halts Trump's bid to end birthright citizenship.",
     "AP", None),
    ("5", "SPACE", TEAL, "CONFIRMED", "mercury",
     "BepiColombo reaches Mercury",
     "The European-Japanese probe enters Mercury orbit after an 8-year trip.",
     "ESA", "8 YEARS"),
    ("6", "CHESS", GOLD, "CONFIRMED", "chess",
     "Gukesh-Sindarov: game 2 drawn",
     "The world title game 2 ends in a draw after just 20 moves.",
     "FIDE", "20 MOVES"),
    ("7", "CRICKET", RED, "CONFIRMED", "cricket",
     "Sooryavanshi, 15, hits 204 off 53 balls",
     "The 15-year-old smashes a 53-ball double century.",
     "ESPNcricinfo", "204 OFF 53"),
    ("8", "EGYPT", RED, "REPORTED", "truck",
     "Cairo fuel tanker crash kills 30+",
     "A fuel tanker crash in Cairo leaves more than 30 people dead.",
     "AP", "30+ KILLED"),
]

TICKER = ("Garment wages up 36% in Bangladesh  \u2022  20 hostages freed in "
          "Colombia  \u2022  Andy Taylor dies  \u2022  18 years since the "
          "26/11 Mumbai attacks")


def draw_top_band(draw, y0):
    col_w, gap = 312, 16
    for i, (kicker, color, callout, headline, summary, source) in enumerate(TOP_BAND):
        x = 24 + i * (col_w + gap)
        draw.rectangle([x, y0, x + col_w, y0 + 4], fill=color)
        draw.text((x, y0 + 12), kicker, font=font(SANS_B, 12), fill=color)
        draw.text((x, y0 + 32), callout, font=font(SERIF, 30), fill=INK)
        y = text_block(draw, x, y0 + 70,
                       wrap(draw, headline, font(SERIF, 17), col_w)[:2],
                       font(SERIF, 17), INK, 21)
        y = text_block(draw, x, y + 4,
                       wrap(draw, summary, font(SANS, 12), col_w)[:2],
                       font(SANS, 12), (60, 64, 72), 15)
        draw.text((x, y + 4), source, font=font(SANS, 10), fill=GREY)


def draw_panel(draw, x, y, w, h, panel):
    (num, kicker, color, badge, key, headline, summary, source, callout) = panel
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(200, 194, 178),
                   width=1)
    draw.rectangle([x, y, x + w, y + 4], fill=color)
    scene(draw, key, x + 10, y + 14, 128, 128)
    tx = x + 148
    tw = w - 158
    draw.text((tx, y + 12), kicker, font=font(SANS_B, 11), fill=color)
    bw = int(draw.textlength(badge, font=font(SANS_B, 10))) + 14
    pill(draw, x + w - 10 - bw, y + 10, badge, color)
    ycur = text_block(draw, tx, y + 32,
                      wrap(draw, headline, font(SERIF, 16), tw),
                      font(SERIF, 16), INK, 20)
    ycur = text_block(draw, tx, ycur + 4,
                      wrap(draw, summary, font(SANS, 12), tw),
                      font(SANS, 12), (60, 64, 72), 15)
    if callout:
        draw.text((tx, y + h - 34), callout, font=font(SANS_B, 13), fill=color)
    draw.text((tx, y + h - 18), source, font=font(SANS, 10), fill=GREY)
    draw.ellipse([x + 10, y + h - 30, x + 34, y + h - 6], fill=NAVY)
    draw.text((x + 17, y + h - 25), num, font=font(SANS_B, 14), fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF, 54)
    draw.text(((W - draw.textlength(title, font=tf)) / 2, 14),
              title, font=tf, fill=INK)
    df = font(SANS, 15)
    dateline = "THURSDAY 26 NOVEMBER 2026  \u2022  THE WORLD'S NEWS IN ONE IMAGE"
    draw.text(((W - draw.textlength(dateline, font=df)) / 2, 78),
              dateline, font=df, fill=GREY)
    draw.line([24, 104, W - 24, 104], fill=INK, width=2)
    draw.line([24, 108, W - 24, 108], fill=INK, width=1)

    draw_top_band(draw, 118)
    draw.line([24, 288, W - 24, 288], fill=(200, 194, 178), width=1)

    pw, ph, gap = 482, 158, 10
    for i, panel in enumerate(PANELS):
        px = 24 + (i % 2) * (pw + gap)
        py = 296 + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, panel)

    # Ticker
    draw.rectangle([0, 966, W, H], fill=NAVY)
    tf2 = font(SANS_B, 12)
    draw.text((24, 978), TICKER, font=tf2, fill=WHITE)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
