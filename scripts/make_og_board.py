#!/usr/bin/env python3
"""Generate assets/og-board.png — the OG/link-preview card (home + /b/ smart link).

Design (user-decided 2026-07-08): full-bleed BOARD crop instead of the old
widget-crop-plus-left-panel composition — at bubble-thumbnail scale the board's
big amber monospaced times + red "Cancelled" read instantly as "a station
departure board" (signature/recognition beats tagline text, which lives in
og:description anyway). Wordmark + domain ride a bottom gradient.

Source: the clean full-board simulator screenshot (no sheets), London Euston
section — 14:10 Birmingham New Cancelled(red) + yellow calling chips.
Regenerate: python3 scripts/make_og_board.py   (needs pillow: pip3 install --user pillow)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = (
    Path.home()
    / "Repos/CommuterApp/screenshots"
    / "Simulator Screenshot - iPhone 17 Pro Max - 2026-06-20 at 14.02.07.png"
)
OUT = Path(__file__).resolve().parent.parent / "assets" / "og-board.png"

W, H = 1200, 630
# London Euston band in the 1284x2778 original: section header bar through the
# first calling-at rows (incl. the red Cancelled + a yellow chip). Aspect
# matches 1200x630 (1284x674), so the resize is uniform (no distortion).
CROP = (0, 1515, 1284, 2189)

GRAD_H = 190          # gradient transition band height
SOLID_H = 92          # solid footer band (wordmark sits here, full legibility)
BG = (13, 13, 13)     # site --bg
TEXT = (240, 238, 232)  # site --text
AMBER = (240, 185, 60)  # site --amber

im = Image.open(SRC).convert("RGB")
card = im.crop(CROP).resize((W, H), Image.LANCZOS)

# Poster-style footer: a gradient fade into a fully SOLID bottom band — the
# wordmark/domain never fight the board texture (a bright calling-point chip
# sat right on the wordmark line in the pure-gradient version).
grad = Image.new("L", (1, GRAD_H))
for y in range(GRAD_H):
    grad.putpixel((0, y), int(255 * (y / (GRAD_H - 1)) ** 1.1))
alpha = grad.resize((W, GRAD_H))
band = card.crop((0, H - SOLID_H - GRAD_H, W, H - SOLID_H))
black = Image.new("RGB", (W, GRAD_H), BG)
card.paste(Image.composite(black, band, alpha), (0, H - SOLID_H - GRAD_H))
card.paste(Image.new("RGB", (W, SOLID_H), BG), (0, H - SOLID_H))

d = ImageDraw.Draw(card)
word_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 62)
mono_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 34)

# Wordmark ONLY — no domain in the image. An OG image always renders WITH the
# platform's link strip, which already shows title + domain; a domain baked in
# the image made the bubble read the brand three times (user report 2026-07-08).
# (The in-app SHARE CARD is the opposite case: that image travels without its
# link, so THAT footer carries CommuteWatch.app.)
d.text((48, H - 82), "CommuteWatch", font=word_font, fill=TEXT)

card.save(OUT, optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
