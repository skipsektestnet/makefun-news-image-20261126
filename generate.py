#!/usr/bin/env python3
"""news-image-20261126 v2 — "THE WORLD TODAY", 1024x1024.

Ditulis dari nol di sesi ini. Python + Pillow, tanpa network / random /
timestamp — deterministik. Perubahan vs v1: nomor panel pindah ke baris
header tiap panel sebagai badge lingkaran 34px (angka putih tebal) di kiri
tag; headline panel 20px; headline top band 21px; angka besar top band
44px; data callout panel diperbesar & ditebalkan. Layout & 11 cerita sama
dengan v1 (tidak ada fakta baru).
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry-v2.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---- palette ------------------------------------------------------------
BG = (247, 241, 227)      # cream page
INK = (26, 42, 58)        # near-black navy text
NAVY = (22, 50, 79)       # ticker / dark accents
RED = (179, 39, 30)
TEAL = (14, 124, 107)
GOLD = (166, 124, 0)
GRAY = (110, 110, 100)
PANEL_BG = (255, 255, 255)
PANEL_LINE = (205, 200, 185)
CREAM_ILL = (237, 230, 214)

# ---- fonts --------------------------------------------------------------
F_TITLE = font(SERIF_B, 54)
F_SUB = font(SANS, 14)
F_TAG = font(SANS_B, 13)
F_BIGNUM = font(SANS_B, 44)
F_TOP_HEAD = font(SERIF_B, 21)
F_TOP_BODY = font(SANS, 12)
F_TOP_SRC = font(SANS, 11)
F_HEAD = font(SERIF_B, 20)
F_BODY = font(SANS, 12)
F_CALLOUT = font(SANS_B, 16)
F_SRC = font(SANS, 11)
F_BADGE = font(SANS_B, 20)
F_PILL = font(SANS_B, 10)
F_TICKER = font(SANS_B, 12)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels (greedy, word based)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap2(draw, text, fnt, max_w):
    """Greedy wrap, but if it yields exactly 2 lines, re-split at the word
    boundary that best balances the two lines (no orphan last word)."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) == 2:
        words = text.split()
        best = None
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            m = max(draw.textlength(a, font=fnt),
                    draw.textlength(b, font=fnt))
            if best is None or m < best[0]:
                best = (m, [a, b])
        if best and best[0] <= max_w:
            return best[1]
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---- illustrations (flat vector scenes, 128x128) ------------------------
def ill_missile(d, x, y):
    d.rectangle([x, y, x + 128, y + 128], fill=(27, 42, 68))
    for sx, sy in [(14, 18), (30, 40), (52, 12), (78, 26), (104, 14),
                   (20, 70), (112, 58), (44, 88), (96, 92)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + 92, y + 22, x + 120, y + 50], fill=(240, 196, 80))
    d.polygon([(x + 58, y + 44), (x + 66, y + 44), (x + 62, y + 30)],
              fill=(240, 120, 40))
    d.rectangle([x + 58, y + 44, x + 66, y + 96], fill=(220, 220, 220))
    d.polygon([(x + 58, y + 96), (x + 50, y + 112), (x + 58, y + 100)],
              fill=(240, 120, 40))
    d.polygon([(x + 66, y + 96), (x + 74, y + 112), (x + 66, y + 100)],
              fill=(240, 120, 40))
    d.polygon([(x + 60, y + 96), (x + 64, y + 96), (x + 62, y + 114)],
              fill=(250, 200, 60))
    d.rectangle([x, y + 118, x + 128, y + 128], fill=(20, 30, 50))


def ill_refinery(d, x, y):
    d.rectangle([x, y, x + 128, y + 128], fill=(35, 40, 46))
    d.ellipse([x + 88, y + 14, x + 116, y + 42], fill=(240, 160, 50))
    d.rectangle([x + 12, y + 62, x + 40, y + 128], fill=(120, 124, 128))
    d.rectangle([x + 46, y + 78, x + 74, y + 128], fill=(96, 100, 104))
    d.rectangle([x + 80, y + 52, x + 86, y + 128], fill=(140, 142, 144))
    d.rectangle([x + 94, y + 88, x + 118, y + 128], fill=(80, 84, 88))
    d.rectangle([x + 20, y + 74, x + 32, y + 84], fill=(240, 196, 80))
    d.rectangle([x + 54, y + 90, x + 66, y + 98], fill=(240, 196, 80))
    d.rectangle([x, y + 118, x + 128, y + 128], fill=(24, 28, 32))


def ill_door(d, x, y):
    d.rectangle([x, y, x + 128, y + 128], fill=CREAM_ILL)
    d.rectangle([x + 22, y + 18, x + 78, y + 128], fill=(122, 90, 60))
    d.rectangle([x + 30, y + 26, x + 70, y + 128], fill=(46, 90, 116))
    d.ellipse([x + 62, y + 76, x + 68, y + 82], fill=(240, 196, 80))
    d.rectangle([x + 88, y + 20, x + 91, y + 78], fill=(90, 90, 90))
    d.polygon([(x + 91, y + 20), (x + 116, y + 28), (x + 91, y + 38)],
              fill=(200, 40, 30))
    d.rectangle([x + 8, y + 108, x + 20, y + 128], fill=(160, 150, 130))
    d.rectangle([x + 96, y + 112, x + 120, y + 128], fill=(160, 150, 130))


def ill_court(d, x, y):
    d.rectangle([x, y, x + 128, y + 128], fill=CREAM_ILL)
    d.polygon([(x + 14, y + 52), (x + 64, y + 18), (x + 114, y + 52)],
              fill=(74, 64, 56))
    d.rectangle([x + 14, y + 52, x + 114, y + 60], fill=(74, 64, 56))
    for cx in (24, 48, 72, 96):
        d.rectangle([x + cx, y + 60, x + cx + 8, y + 104], fill=(250, 250, 246))
    d.rectangle([x + 56, y + 76, x + 72, y + 104], fill=(60, 60, 66))
    d.rectangle([x + 10, y + 104, x + 118, y + 112], fill=(180, 172, 158))
    d.rectangle([x + 6, y + 112, x + 122, y + 120], fill=(160, 152, 138))


def ill_mercury(d, x, y):
    d.rectangle([x, y, x + 128, y + 128], fill=(20, 28, 46))
    for sx, sy in [(12, 14), (40, 26), (108, 18), (20, 96), (116, 88)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + 28, y + 44, x + 100, y + 116], outline=(90, 160, 220),
              width=2)
    d.ellipse([x + 34, y + 52, x + 94, y + 112], fill=(201, 177, 140))
    for cx, cy, cr in [(52, 70, 7), (74, 92, 9), (78, 64, 5), (58, 96, 4)]:
        d.ellipse([x + cx - cr, y + cy - cr, x + cx + cr, y + cy + cr],
                  fill=(170, 145, 108))
    d.polygon([(x + 102, y + 30), (x + 112, y + 44), (x + 96, y + 46)],
              fill=(90, 200, 220))


def ill_chess(d, x, y):
    light, dark = (240, 217, 181), (181, 136, 99)
    for r in range(8):
        for c in range(8):
            col = light if (r + c) % 2 == 0 else dark
            d.rectangle([x + c * 16, y + r * 16, x + c * 16 + 16,
                         y + r * 16 + 16], fill=col)
    # black king on d5-ish
    kx, ky = x + 40, y + 40
    d.ellipse([kx - 9, ky - 9, kx + 9, ky + 9], fill=(30, 30, 30))
    d.rectangle([kx - 2, ky - 16, kx + 2, ky - 6], fill=(30, 30, 30))
    d.rectangle([kx - 7, ky - 12, kx + 7, ky - 8], fill=(30, 30, 30))
    d.rectangle([kx - 11, ky + 8, kx + 11, ky + 14], fill=(30, 30, 30))
    # white pawn
    px, py = x + 84, y + 88
    d.ellipse([px - 8, py - 10, px + 8, py + 6], fill=(250, 250, 246),
              outline=(120, 120, 120))
    d.rectangle([px - 10, py + 6, px + 10, py + 12], fill=(250, 250, 246),
                outline=(120, 120, 120))


def ill_cricket(d, x, y):
    d.rectangle([x, y, x + 128, y + 88], fill=(95, 168, 90))
    d.rectangle([x, y + 88, x + 128, y + 128], fill=(232, 217, 168))
    d.rectangle([x, y + 84, x + 128, y + 88], fill=(220, 205, 155))
    for sx in (30, 38, 46):
        d.rectangle([x + sx, y + 62, x + sx + 3, y + 88], fill=(240, 210, 80))
    d.rectangle([x + 30, y + 58, x + 49, y + 62], fill=(240, 210, 80))
    d.polygon([(x + 66, y + 30), (x + 76, y + 34), (x + 62, y + 84),
               (x + 52, y + 80)], fill=(214, 178, 130))
    d.ellipse([x + 92, y + 34, x + 110, y + 52], fill=(200, 40, 30))


def ill_tanker(d, x, y):
    d.rectangle([x, y, x + 128, y + 128], fill=CREAM_ILL)
    d.ellipse([x + 92, y + 12, x + 118, y + 38], fill=(240, 196, 80))
    d.polygon([(x + 8, y + 62), (x + 30, y + 30), (x + 52, y + 62)],
              fill=(230, 130, 40))
    d.rectangle([x + 12, y + 62, x + 88, y + 100], fill=(220, 110, 30))
    d.rectangle([x + 88, y + 70, x + 116, y + 100], fill=(190, 50, 40))
    d.rectangle([x + 94, y + 76, x + 110, y + 88], fill=(180, 220, 235))
    for wx in (26, 56, 98):
        d.ellipse([x + wx, y + 96, x + wx + 16, y + 112], fill=(30, 30, 30))
    d.rectangle([x, y + 112, x + 128, y + 128], fill=(200, 190, 165))


# ---- content (sama dengan v1, sudah terverifikasi) -----------------------
TOP = [
    dict(tag="RED SEA WAR", color=RED, big="3 CITIES",
         head="Houthi-Saudi escalation: missiles over Riyadh",
         body=("Air defences intercept a missile over Riyadh; a projectile "
               "hits Jazan port, a drone over Jeddah."),
         src="Reuters · Saudi authorities"),
    dict(tag="STRAIT OF HORMUZ", color=NAVY, big="2 TANKERS",
         head="Two tankers struck by sea mines",
         body=("Two tankers are hit by mines in the Strait of Hormuz, the "
               "busiest oil chokepoint."),
         src="Reuters"),
    dict(tag="UKRAINE WAR", color=TEAL, big="~500,000",
         head="Russia's war toll nears half a million",
         body=("Reported Russian casualties in the Ukraine war reach about "
               "500,000, new figures show."),
         src="Reported figures"),
]

PANELS = [
    dict(n=1, tag="MIDDLE EAST", color=RED, status="REPORTED",
         head="Israel strikes Hamas official in Gaza",
         body="A strike targets a senior Hamas figure in Gaza as the war grinds on.",
         src="Reuters", callout=None, ill=ill_missile),
    dict(n=2, tag="UKRAINE WAR", color=NAVY, status="REPORTED",
         head="Ukraine hits Russian oil refinery",
         body="Kyiv strikes a refinery deep inside Russia in its long-range campaign.",
         src="Reuters", callout=None, ill=ill_refinery),
    dict(n=3, tag="KOREA", color=TEAL, status="CONFIRMED",
         head="Pyongyang orders Swiss office to shut",
         body="North Korea tells Switzerland's office in the capital to close.",
         src="AP", callout=None, ill=ill_door),
    dict(n=4, tag="UNITED STATES", color=NAVY, status="CONFIRMED",
         head="Second judge blocks birthright order",
         body="Another US judge halts Trump's bid to end birthright citizenship.",
         src="AP", callout=None, ill=ill_court),
    dict(n=5, tag="SPACE", color=TEAL, status="CONFIRMED",
         head="BepiColombo reaches Mercury",
         body="The European-Japanese probe enters Mercury orbit after an 8-year trip.",
         src="ESA", callout="8 YEARS", ill=ill_mercury),
    dict(n=6, tag="CHESS", color=GOLD, status="CONFIRMED",
         head="Gukesh-Sindarov: game 2 drawn",
         body="The world title game 2 ends in a draw after just 20 moves.",
         src="FIDE", callout="20 MOVES", ill=ill_chess),
    dict(n=7, tag="CRICKET", color=RED, status="CONFIRMED",
         head="Sooryavanshi, 15, hits 204 off 53 balls",
         body="The 15-year-old smashes a 53-ball double century.",
         src="ESPNcricinfo", callout="204 OFF 53", ill=ill_cricket),
    dict(n=8, tag="EGYPT", color=RED, status="REPORTED",
         head="Cairo fuel tanker crash kills 30+",
         body="A fuel tanker crash in Cairo leaves more than 30 people dead.",
         src="AP", callout="30+ KILLED", ill=ill_tanker),
]

TICKER = ("Garment wages up 36% in Bangladesh  •  20 hostages freed in "
          "Colombia  •  Andy Taylor dies  •  18 years since the 26/11 "
          "Mumbai attacks")


def pill(d, x, y, text, color):
    w = int(d.textlength(text, font=F_PILL)) + 20
    d.rounded_rectangle([x, y, x + w, y + 18], radius=9, fill=color)
    d.text((x + 10, y + 4), text, font=F_PILL, fill=(255, 255, 255))
    return w


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------------
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, 10), title,
           font=F_TITLE, fill=INK)
    sub = "THURSDAY 26 NOVEMBER 2026  •  THE WORLD'S NEWS IN ONE IMAGE"
    d.text(((W - d.textlength(sub, font=F_SUB)) / 2, 68), sub,
           font=F_SUB, fill=GRAY)
    d.line([24, 90, 1000, 90], fill=INK, width=2)
    d.line([24, 94, 1000, 94], fill=INK, width=1)

    # ---- top band: 3 big stories ---------------------------------------
    col_w, gap = 313, 18
    for i, s in enumerate(TOP):
        cx = 24 + i * (col_w + gap)
        d.rectangle([cx, 100, cx + col_w, 105], fill=s["color"])
        d.text((cx, 112), s["tag"], font=F_TAG, fill=s["color"])
        d.text((cx, 128), s["big"], font=F_BIGNUM, fill=INK)
        y = draw_lines(d, wrap2(d, s["head"], F_TOP_HEAD, col_w),
                       cx, 172, F_TOP_HEAD, INK, 24)
        y = draw_lines(d, wrap(d, s["body"], F_TOP_BODY, col_w),
                       cx, y + 4, F_TOP_BODY, (70, 70, 60), 15)
        d.text((cx, y + 4), s["src"], font=F_TOP_SRC, fill=GRAY)

    # ---- panel grid 2x4 --------------------------------------------------
    px0, py0, pw, ph, pg = 24, 292, 480, 162, 8
    for i, p in enumerate(PANELS):
        px = px0 + (i % 2) * (pw + 16)
        py = py0 + (i // 2) * (ph + pg)
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL_BG,
                    outline=PANEL_LINE, width=1)
        d.rectangle([px, py, px + pw, py + 4], fill=p["color"])
        # illustration, left
        p["ill"](d, px + 10, py + 10)
        # header row: badge 34px + tag + status pill
        tx = px + 148
        cx, cy = tx + 17, py + 10 + 17
        d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=p["color"])
        num = str(p["n"])
        d.text((cx - d.textlength(num, font=F_BADGE) / 2, cy - 11), num,
               font=F_BADGE, fill=(255, 255, 255))
        d.text((tx + 42, py + 20), p["tag"], font=F_TAG, fill=p["color"])
        pill_w = int(d.textlength(p["status"], font=F_PILL)) + 20
        pill(d, px + pw - 10 - pill_w, py + 18, p["status"], p["color"])
        # headline 20px, body, callout, source
        y = draw_lines(d, wrap2(d, p["head"], F_HEAD, pw - 158),
                       tx, py + 46, F_HEAD, INK, 22)
        y = draw_lines(d, wrap2(d, p["body"], F_BODY, pw - 158),
                       tx, y + 4, F_BODY, (70, 70, 60), 15)
        if p["callout"]:
            d.text((tx, y + 4), p["callout"], font=F_CALLOUT,
                   fill=p["color"])
        d.text((tx, py + ph - 14), p["src"], font=F_SRC, fill=GRAY)

    # ---- ticker ----------------------------------------------------------
    d.rectangle([0, 972, W, H], fill=NAVY)
    d.text(((W - d.textlength(TICKER, font=F_TICKER)) / 2, 991), TICKER,
           font=F_TICKER, fill=(255, 255, 255))

    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print("saved", OUT, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
