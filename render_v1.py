#!/usr/bin/env python3
"""Render the news-image-20261123 entry.

Draws a 1024x1024 ink-on-paper newspaper front page from news23.json.
Standard library + Pillow only, no network, no randomness: the same
input always produces the same image.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24                      # side margin
PAPER = (247, 243, 234)
CARD_BG = (252, 249, 241)
INK = (26, 35, 64)
RED = (178, 44, 30)
BAR = (20, 27, 49)
LIGHT = (247, 243, 234)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SANS = lambda s: F("DejaVuSans.ttf", s)
SANSB = lambda s: F("DejaVuSans-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif-Bold.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap by measured width. Deterministic."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(d, x, y, text, f, color, gap=3):
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textlength(ch, font=f) + gap
    return x


# ---------------------------------------------------------------- icons

def ic_globe(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=2)
    d.ellipse([x + s * 0.25, y, x + s * 0.75, y + s], outline=c, width=2)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=c, width=2)
    d.line([x + s * 0.08, y + s * 0.28, x + s * 0.92, y + s * 0.28], fill=c, width=2)
    d.line([x + s * 0.08, y + s * 0.72, x + s * 0.92, y + s * 0.72], fill=c, width=2)


def ic_ship(d, x, y, s, c):
    d.polygon([(x + s * 0.1, y + s * 0.62), (x + s * 0.9, y + s * 0.62),
               (x + s * 0.78, y + s * 0.82), (x + s * 0.22, y + s * 0.82)], outline=c, width=2)
    d.rectangle([x + s * 0.38, y + s * 0.3, x + s * 0.62, y + s * 0.62], outline=c, width=2)
    d.line([x + s * 0.5, y + s * 0.1, x + s * 0.5, y + s * 0.3], fill=c, width=2)
    d.polygon([(x + s * 0.5, y + s * 0.1), (x + s * 0.72, y + s * 0.22),
               (x + s * 0.5, y + s * 0.3)], fill=c)
    d.line([x + s * 0.05, y + s * 0.92, x + s * 0.3, y + s * 0.92], fill=c, width=2)
    d.line([x + s * 0.42, y + s * 0.92, x + s * 0.7, y + s * 0.92], fill=c, width=2)
    d.line([x + s * 0.8, y + s * 0.92, x + s * 0.95, y + s * 0.92], fill=c, width=2)


def ic_ballot(d, x, y, s, c):
    d.rectangle([x + s * 0.15, y + s * 0.35, x + s * 0.85, y + s * 0.9], outline=c, width=2)
    d.line([x + s * 0.35, y + s * 0.5, x + s * 0.65, y + s * 0.5], fill=c, width=2)
    d.polygon([(x + s * 0.4, y + s * 0.05), (x + s * 0.72, y + s * 0.05),
               (x + s * 0.6, y + s * 0.32), (x + s * 0.35, y + s * 0.32)], outline=c, width=2)
    d.line([x + s * 0.42, y + s * 0.68, x + s * 0.5, y + s * 0.78], fill=c, width=2)
    d.line([x + s * 0.5, y + s * 0.78, x + s * 0.62, y + s * 0.62], fill=c, width=2)


def ic_chip(d, x, y, s, c):
    r = s * 0.2
    d.rectangle([x + r, y + r, x + s - r, y + s - r], outline=c, width=2)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], outline=c, width=2)
    for t in (0.35, 0.5, 0.65):
        d.line([x + s * t, y, x + s * t, y + r], fill=c, width=2)
        d.line([x + s * t, y + s - r, x + s * t, y + s], fill=c, width=2)
        d.line([x, y + s * t, x + r, y + s * t], fill=c, width=2)
        d.line([x + s - r, y + s * t, x + s, y + s * t], fill=c, width=2)


def ic_radar(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=2)
    d.ellipse([x + s * 0.25, y + s * 0.25, x + s * 0.75, y + s * 0.75], outline=c, width=2)
    d.line([x + s * 0.5, y + s * 0.5, x + s * 0.85, y + s * 0.15], fill=c, width=2)
    d.ellipse([x + s * 0.72, y + s * 0.12, x + s * 0.84, y + s * 0.24], fill=c)


def ic_oil(d, x, y, s, c):
    d.rectangle([x + s * 0.25, y + s * 0.15, x + s * 0.75, y + s * 0.9], outline=c, width=2)
    d.line([x + s * 0.25, y + s * 0.35, x + s * 0.75, y + s * 0.35], fill=c, width=2)
    d.line([x + s * 0.25, y + s * 0.65, x + s * 0.75, y + s * 0.65], fill=c, width=2)
    d.line([x + s * 0.38, y, x + s * 0.38, y + s * 0.15], fill=c, width=2)
    d.line([x + s * 0.62, y, x + s * 0.62, y + s * 0.15], fill=c, width=2)


def ic_drone(d, x, y, s, c):
    d.rectangle([x + s * 0.35, y + s * 0.35, x + s * 0.65, y + s * 0.65], outline=c, width=2)
    for cx, cy in ((0.18, 0.18), (0.82, 0.18), (0.18, 0.82), (0.82, 0.82)):
        d.line([x + s * 0.5, y + s * 0.5, x + s * cx, y + s * cy], fill=c, width=2)
        d.ellipse([x + s * cx - s * 0.12, y + s * cy - s * 0.12,
                   x + s * cx + s * 0.12, y + s * cy + s * 0.12], outline=c, width=2)


def ic_crowd(d, x, y, s, c):
    for i, (cx, r) in enumerate(((0.3, 0.14), (0.7, 0.14), (0.5, 0.16))):
        top = y + (s * 0.2 if i < 2 else s * 0.38)
        d.ellipse([x + s * cx - s * r, top, x + s * cx + s * r, top + s * 2 * r], outline=c, width=2)
        d.arc([x + s * cx - s * 0.28, top + s * 0.3 * (1 if i < 2 else 1.4),
               x + s * cx + s * 0.28, top + s * 1.1 * (1 if i < 2 else 1.4)],
              0, 180, fill=c, width=2)


def ic_bank(d, x, y, s, c):
    d.polygon([(x + s * 0.05, y + s * 0.3), (x + s * 0.5, y + s * 0.05),
               (x + s * 0.95, y + s * 0.3)], outline=c, width=2)
    for t in (0.2, 0.4, 0.6, 0.8):
        d.line([x + s * t, y + s * 0.4, x + s * t, y + s * 0.78], fill=c, width=2)
    d.line([x + s * 0.1, y + s * 0.85, x + s * 0.9, y + s * 0.85], fill=c, width=2)
    d.line([x + s * 0.05, y + s * 0.93, x + s * 0.95, y + s * 0.93], fill=c, width=2)


def ic_flag(d, x, y, s, c):
    d.line([x + s * 0.25, y, x + s * 0.25, y + s], fill=c, width=2)
    d.rectangle([x + s * 0.25, y + s * 0.1, x + s * 0.8, y + s * 0.45], outline=c, width=2)
    d.line([x + s * 0.25, y + s * 0.27, x + s * 0.8, y + s * 0.27], fill=c, width=2)


def ic_temple(d, x, y, s, c):
    d.polygon([(x + s * 0.1, y + s * 0.25), (x + s * 0.5, y + s * 0.02),
               (x + s * 0.9, y + s * 0.25)], outline=c, width=2)
    for t in (0.25, 0.45, 0.65, 0.85):
        d.line([x + s * t, y + s * 0.35, x + s * t, y + s * 0.85], fill=c, width=2)
    d.line([x + s * 0.1, y + s * 0.9, x + s * 0.9, y + s * 0.9], fill=c, width=2)


def ic_cross(d, x, y, s, c):
    d.rectangle([x, y, x + s, y + s], outline=c, width=2)
    cx, cy = x + s / 2, y + s / 2
    w = s * 0.14
    d.line([cx - w, cy, cx + w, cy], fill=c, width=2)
    d.line([cx, cy - w, cx, cy + w], fill=c, width=2)


def ic_flame(d, x, y, s, c):
    d.polygon([(x + s * 0.5, y), (x + s * 0.72, y + s * 0.4), (x + s * 0.66, y + s * 0.55),
               (x + s * 0.8, y + s * 0.7), (x + s * 0.7, y + s * 0.92), (x + s * 0.5, y + s),
               (x + s * 0.3, y + s * 0.92), (x + s * 0.2, y + s * 0.7), (x + s * 0.34, y + s * 0.55),
               (x + s * 0.28, y + s * 0.4)], outline=c, width=2)


def ic_plane(d, x, y, s, c):
    d.polygon([(x + s * 0.95, y + s * 0.5), (x + s * 0.45, y + s * 0.38),
               (x + s * 0.62, y + s * 0.5), (x + s * 0.45, y + s * 0.62)], outline=c, width=2)
    d.polygon([(x + s * 0.3, y + s * 0.05), (x + s * 0.42, y + s * 0.38),
               (x + s * 0.18, y + s * 0.3)], outline=c, width=2)
    d.polygon([(x + s * 0.3, y + s * 0.95), (x + s * 0.42, y + s * 0.62),
               (x + s * 0.18, y + s * 0.7)], outline=c, width=2)
    d.polygon([(x, y + s * 0.4), (x + s * 0.15, y + s * 0.47), (x, y + s * 0.55)], outline=c, width=2)


ICONS = {
    "globe": ic_globe, "ship": ic_ship, "ballot": ic_ballot, "chip": ic_chip,
    "radar": ic_radar, "oil": ic_oil, "drone": ic_drone, "crowd": ic_crowd,
    "bank": ic_bank, "flag": ic_flag, "temple": ic_temple, "cross": ic_cross,
    "flame": ic_flame, "plane": ic_plane,
}


# ---------------------------------------------------------------- layout

def lead_block(d, data, y, h, icon_s, hf, df):
    x0 = M
    wtxt = W - 2 * M - icon_s - 18
    d.text((x0, y + 4), data["tag"], font=SANSB(13), fill=RED)
    ty = y + 26
    for ln in wrap(d, data["headline"], hf, wtxt):
        d.text((x0, ty), ln, font=hf, fill=INK)
        ty += hf.size + 6
    dy = y + h - (df.size + 4) * min(len(wrap(d, data["deck"], df, wtxt)), 2) - 2
    for ln in wrap(d, data["deck"], df, wtxt)[:2]:
        d.text((x0, dy), ln, font=df, fill=(70, 78, 104))
        dy += df.size + 4
    ICONS[data["icon"]](d, W - M - icon_s, y + (h - icon_s) / 2, icon_s, INK)


def card(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(190, 184, 168), width=1)
    d.rectangle([x, y, x + 3, y + h], fill=RED)
    tracked(d, x + 12, y + 8, c["region"], SANSB(10), RED, gap=2)
    ICONS[c["icon"]](d, x + w - 12 - 24, y + 7, 24, INK)
    hy = y + 27
    for ln in wrap(d, c["headline"], SANSB(17), w - 24 - 36)[:2]:
        d.text((x + 12, hy), ln, font=SANSB(17), fill=INK)
        hy += 20
    d.line([x + 12, hy + 2, x + w - 12, hy + 2], fill=(190, 184, 168), width=1)
    by = hy + 8
    for ln in wrap(d, c["body"], SANS(12), w - 24)[:2]:
        d.text((x + 12, by), ln, font=SANS(12), fill=(70, 78, 104))
        by += 15


def render(path):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "news23.json")) as f:
        data = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([M, 14, W - M, 14], fill=INK, width=2)
    d.line([M, 19, W - M, 19], fill=INK, width=1)
    d.text((M, 26), data["kicker_top"], font=SANSB(13), fill=INK)
    d.text((W - M - d.textlength(data["kicker_no"], font=SANSB(13)), 26),
           data["kicker_no"], font=SANSB(13), fill=INK)
    dl = data["date_line"]
    df = SERIF(40)
    d.text(((W - d.textlength(dl, font=df)) / 2, 42), dl, font=df, fill=INK)
    d.line([M, 104, W - M, 104], fill=INK, width=3)

    # leads
    lead_block(d, data["lead1"], 116, 182, 92, SERIF(33), SANS(15))
    d.line([M, 308, W - M, 308], fill=INK, width=1)
    lead_block(d, data["lead2"], 318, 140, 74, SERIF(29), SANS(14))
    d.line([M, 468, W - M, 468], fill=INK, width=3)

    # grid 3x4
    gy, gh, gap = 480, 494, 10
    cw = (W - 2 * M - 2 * gap) / 3
    ch = (gh - 3 * gap) / 4
    for i, c in enumerate(data["cards"][:12]):
        col, row = i % 3, i // 3
        card(d, M + col * (cw + gap), gy + row * (ch + gap), cw, ch, c)

    # ticker bar
    ty0 = 986
    d.rectangle([0, ty0, W, H], fill=BAR)
    line1 = "ALSO TODAY   " + "    ·    ".join(data["ticker"][:3])
    line2 = "    ·    ".join(data["ticker"][3:])
    tf = SANS(12)
    d.text((M, ty0 + 5), line1, font=tf, fill=LIGHT)
    d.text((M, ty0 + 21), line2, font=tf, fill=LIGHT)

    img.save(path, "PNG")
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    render(os.path.join(out, "entry.png"))
