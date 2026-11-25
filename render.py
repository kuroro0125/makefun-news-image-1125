#!/usr/bin/env python3
"""Render the front page for 25 November 2026 as a deterministic 1024x1024 PNG.

Everything is drawn with Pillow from the content table below; no network, no
randomness, no timestamps. Run: python3 render.py  (writes entry.png next to
this file). Render twice and the bytes must be identical.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (164, 31, 31)
BLUE = (31, 58, 95)
GREY = (110, 108, 100)
RULE = (26, 26, 26)
SKY_TOP = (38, 52, 84)
SKY_BOT = (214, 122, 62)
TOWER = (52, 58, 74)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(draw, text, fnt_path, start, width, max_lines):
    """Shrink the headline font until it fits in max_lines at the given width."""
    size = start
    while size > 18:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 2
    fnt = font(fnt_path, size)
    return fnt, wrap(draw, text, fnt, width)[:max_lines]


def draw_tower_panel(draw, x, y, w, h):
    """Dusk skyline of Riyadh's financial district: tallest tower, smoke, streak."""
    # gradient sky
    for i in range(h):
        t = i / max(1, h - 1)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # sun disc low on the horizon
    draw.ellipse([x + w - 118, y + h - 150, x + w - 58, y + h - 90],
                 fill=(240, 196, 110))
    # distant skyline
    base = y + h
    for bx, bw, bh in [(0, 46, 120), (52, 34, 170), (92, 40, 96),
                       (252, 40, 130), (296, 34, 88)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(44, 48, 66))
    # the tallest tower, centre, with a lit crown
    tx = x + w // 2 - 34
    draw.rectangle([tx, y + 26, tx + 68, base], fill=TOWER)
    draw.polygon([(tx, y + 26), (tx + 34, y + 2), (tx + 68, y + 26)],
                 fill=(70, 76, 96))
    for wy in range(y + 52, base - 14, 26):
        for wx in (tx + 8, tx + 28, tx + 48):
            draw.rectangle([wx, wy, wx + 10, wy + 12], fill=(240, 196, 110))
    # smoke curling from the tower crown
    for cx, cy, cr in [(tx + 58, y + 22, 10), (tx + 76, y + 12, 12),
                       (tx + 94, y + 26, 13), (tx + 112, y + 40, 10)]:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(120, 116, 110))
    # missile streak across the sky
    draw.line([(x + 8, y + 44), (x + 150, y + 96)], fill=(255, 220, 130),
              width=4)
    draw.line([(x + 8, y + 44), (x + 60, y + 62)], fill=(255, 240, 190),
              width=7)
    # ground line
    draw.rectangle([x, base - 6, x + w, base], fill=(30, 30, 34))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # side margin
    right = W - mx

    # ---- masthead ----
    d.rectangle([0, 0, W, 10], fill=INK)
    f_title = font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 26), title, font=f_title, fill=INK)
    f_date = font(SERIF, 26)
    date = "Wednesday, 25 November 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 116), date, font=f_date, fill=RED)
    d.line([(mx, 158), (right, 158)], fill=RULE, width=3)
    d.line([(mx, 164), (right, 164)], fill=RULE, width=1)

    # ---- lead story ----
    y = 186
    f_kick = font(SANS_B, 19)
    d.text((mx, y), "MIDDLE EAST  ·  LEAD", font=f_kick, fill=RED)
    y += 30
    f_head, head_lines = fit_headline(
        d, "Missile hits Riyadh's tallest tower; 11 hurt",
        SERIF_B, 52, 560, 2)
    y = draw_lines(d, head_lines, mx, y, f_head, INK, 58)
    y += 6
    f_dek = font(SERIF, 24)
    dek = ("Second Houthi hit on the capital's financial district "
           "in under a week.")
    y = draw_lines(d, wrap(d, dek, f_dek, 560), mx, y, f_dek, BLUE, 30)
    y += 10
    f_body = font(SERIF, 20)
    body = ("Saudi civil defence said 11 people were wounded when a "
            "missile struck the tallest tower in Riyadh's financial "
            "district. The Houthis claimed the strike, the second on "
            "the area in days, as the war reaches deeper into the Gulf.")
    y = draw_lines(d, wrap(d, body, f_body, 560), mx, y, f_body, INK, 27)

    # illustration panel, right of the lead text
    px, py, pw, ph = 640, 186, 340, 300
    draw_tower_panel(d, px, py, pw, ph)
    f_cap = font(SANS, 15)
    cap = "Riyadh's financial district at dusk. Illustration."
    d.text((px, py + ph + 6), cap, font=f_cap, fill=GREY)

    div_y = max(y + 14, py + ph + 34)
    d.line([(mx, div_y), (right, div_y)], fill=RULE, width=2)

    # ---- secondary stories ----
    y = div_y + 22
    col_w = (right - mx - 28) // 2
    secondaries = [
        ("UKRAINE  ·  WAR AT SEA",
         "Zelenskiy confirms strike on Russian ship",
         "Zelenskiy confirmed a drone strike on a Russian cargo ship "
         "in the Gulf of Finland. Kyiv called its Libya attack "
         "self-defence; Norway urged caution."),
        ("TECH  ·  COURTS",
         "Huawei convicted; Shanghai chief probed",
         "A US jury convicted Huawei over its Iran business. Beijing "
         "placed Politburo member Chen Jining, the Shanghai party "
         "chief, under investigation."),
    ]
    sec_bottom = y
    for i, (kick, head, txt) in enumerate(secondaries):
        x = mx + i * (col_w + 28)
        yy = y
        d.text((x, yy), kick, font=f_kick, fill=RED)
        yy += 28
        f_h, h_lines = fit_headline(d, head, SERIF_B, 30, col_w, 2)
        yy = draw_lines(d, h_lines, x, yy, f_h, INK, 36)
        yy += 4
        yy = draw_lines(d, wrap(d, txt, f_body, col_w), x, yy, f_body,
                        INK, 26)
        sec_bottom = max(sec_bottom, yy)
    div2 = sec_bottom + 16
    d.line([(mx, div2), (right, div2)], fill=RULE, width=2)

    # ---- briefs ----
    y = div2 + 20
    f_brief_h = font(SANS_B, 19)
    d.text((mx, y), "IN BRIEF", font=f_brief_h, fill=RED)
    y += 30
    briefs = [
        ("SPACE", "Shenzhou-24 launches with first Pakistani aboard."),
        ("WASHINGTON", "Trump gives Giuliani the Medal of Freedom."),
        ("COLOMBIA", "Gunmen hold 25 hostage in a supermarket siege."),
        ("TRADE", "Shein pays $100m to settle US deception claims."),
    ]
    f_b = font(SERIF, 20)
    f_bk = font(SANS_B, 18)
    bx_w = (right - mx - 28) // 2
    for i, (k, t) in enumerate(briefs):
        x = mx + (i % 2) * (bx_w + 28)
        yy = y + (i // 2) * 56
        d.text((x, yy), k + " — ", font=f_bk, fill=INK)
        kw = d.textlength(k + " — ", font=f_bk)
        lines = wrap(d, t, f_b, bx_w - kw)
        draw_lines(d, lines, x + kw, yy + 1, f_b, INK, 25)

    # ---- footer ----
    d.line([(mx, 976), (right, 976)], fill=RULE, width=1)
    f_foot = font(SANS, 14)
    foot = ("Sources: Reuters, Associated Press, SCMP, The Japan Times  ·  "
            "25 November 2026  ·  One day's world news, in one image.")
    d.text((mx, 988), foot, font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
