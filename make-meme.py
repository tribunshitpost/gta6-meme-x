#!/usr/bin/env python3
"""Build meme.png (1080x1080) for gta6-meme-x-01.

Pipeline, all local, no network:
  1. Take the AI-generated Vice City sunset background (bg-scene.jpg,
     generated in this session, no text in it, already square-cropped
     to 1080x1080) and use it as the base.
  2. Paste the real make.fun ghost from the press kit (assets/ghost.png)
     into the scene as a third passenger riding on the pink convertible,
     next to the two people waiting for GTA 6.
  3. Add the two caption lines in huge bold type with a thick black
     outline, on dark gradient bands top and bottom, so the words stay
     readable when X shrinks the picture to 480x480.
  4. Save as meme.png, optimised, under 1 MiB.

Run:  python3 make-meme.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "bg-scene.jpg")
GHOST = os.path.join(HERE, "assets", "ghost.png")
OUT = os.path.join(HERE, "meme.png")
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

SIZE = 1080
MAGENTA = (255, 46, 154)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def fit_font(draw, lines, max_width, start_size):
    """Largest bold size that fits every line inside max_width."""
    size = start_size
    while size > 30:
        font = ImageFont.truetype(FONT, size)
        if all(draw.textlength(line, font=font) <= max_width for line in lines):
            return font
        size -= 4
    return ImageFont.truetype(FONT, 30)


def outlined_text(draw, cx, y, text, font, fill):
    """Centred text with a thick black outline and a soft shadow."""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = cx - w // 2
    # soft shadow
    draw.text((x + 5, y + 6), text, font=font, fill=(0, 0, 0, 190))
    # thick outline: stroke draws around the glyphs
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=max(4, font.size // 14), stroke_fill=BLACK)


def band(img, top, height, fade):
    """Dark vertical gradient band, solid at the edge, fading inward."""
    overlay = Image.new("RGBA", (SIZE, height), (0, 0, 0, 0))
    px = overlay.load()
    for yy in range(height):
        t = yy / max(1, height - 1)
        alpha = int(205 * (1 - t)) if fade == "down" else int(205 * t)
        for xx in range(SIZE):
            px[xx, yy] = (0, 0, 0, alpha)
    img.alpha_composite(overlay, (0, top))


def main():
    bg = Image.open(BG).convert("RGB")
    # Centre-crop the wide background to a square, then resize to 1080.
    w, h = bg.size
    side = min(w, h)
    left = (w - side) // 2
    img = bg.crop((left, 0, left + side, h)).resize((SIZE, SIZE), Image.LANCZOS)
    img = img.convert("RGBA")

    # Dark bands top and bottom so the captions stay readable.
    band(img, 0, 250, "down")
    band(img, SIZE - 280, 280, "up")

    draw = ImageDraw.Draw(img)

    top_lines = ["13 YEARS WAITING", "FOR GTA 6"]
    top_font = fit_font(draw, top_lines, SIZE - 70, 108)
    y = 28
    for line in top_lines:
        outlined_text(draw, SIZE // 2, y, line, top_font, WHITE)
        y += int(top_font.size * 1.08)

    # The make.fun ghost rides along: on the rear deck of the pink
    # convertible, on the left, so the two people waiting on the car
    # stay visible on the right. Big and unmistakable, not a corner
    # sticker: it is a passenger in the scene.
    ghost = Image.open(GHOST).convert("RGBA")
    ghost = ghost.resize((250, 250), Image.LANCZOS)
    # soft drop shadow under the ghost so it sits in the scene
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([150, 775, 360, 810], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(shadow)
    img.alpha_composite(ghost, (130, 530))

    bottom_lines = ["MY AGENT ALREADY", "GOT PAID ON MAKE.FUN"]
    bottom_font = fit_font(draw, bottom_lines, SIZE - 70, 92)
    y = SIZE - 258
    for line in bottom_lines:
        outlined_text(draw, SIZE // 2, y, line, bottom_font, WHITE)
        y += int(bottom_font.size * 1.08)

    img.convert("RGB").save(OUT, "PNG", optimize=True, compress_level=9)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
