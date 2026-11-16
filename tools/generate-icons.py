"""Build every icon, the logo files and the link-preview image in public/.

Run from the repo root:  python tools/generate-icons.py
Needs Pillow (pip install pillow). Uses Segoe UI / Consolas on Windows for the
preview image text; on other systems set OG_FONT_BOLD / OG_FONT_REGULAR / OG_FONT_MONO.
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
TOOLS = ROOT / "tools"

BG = (38, 43, 47)            # #262b2f, the site's dark background
GREEN = (0, 154, 77)         # #009a4d, brand green
GREEN_BRIGHT = (46, 224, 138)  # #2ee08a, brand green on dark
WHITE = (255, 255, 255)

# The mark: three dots, in a 44 x 44 box (same geometry as the mat-tech.com favicon.svg).
# Their bounding box is centred on (22, 22).
DOTS = [(7.6, 27.9, 6.2), (21.6, 27.9, 6.2), (35.6, 16.9, 7.0)]
SS = 8  # supersampling factor for smooth edges


def mark(size, *, background=True, scale=0.86, corner=0.22, color=GREEN):
    """The three-dot mark on a dark rounded square (or transparent)."""
    big = size * SS
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if background:
        if corner:
            d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * corner), fill=BG + (255,))
        else:
            d.rectangle([0, 0, big, big], fill=BG + (255,))
    k = big * scale / 44
    off = big / 2 - 22 * k
    for cx, cy, r in DOTS:
        x, y, rr = off + cx * k, off + cy * k, r * k
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color + (255,))
    return img.resize((size, size), Image.LANCZOS)


def save_png(img, name):
    img.save(OUT / name, optimize=True)
    print("wrote", name, img.size)


def font(env, fallback, size):
    path = os.environ.get(env) or fallback
    return ImageFont.truetype(path, size)


def og_image():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)

    # soft green glow, bottom left and behind the mark
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse([-260, 380, 360, 900], fill=GREEN + (90,))
    g.ellipse([700, 60, 1180, 540], fill=GREEN + (55,))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(glow, (0, 0), glow)

    # large mark on the right
    m = mark(520, background=False, scale=1.0, color=GREEN_BRIGHT)
    img.paste(m, (650, 40), m)

    # wordmark, top left
    logo = Image.open(TOOLS / "logo-dark-source.png").convert("RGBA")
    logo = logo.crop(logo.getbbox())
    lw = 250
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    img.paste(logo, (72, 70), logo)

    d = ImageDraw.Draw(img)
    bold = font("OG_FONT_BOLD", "C:/Windows/Fonts/segoeuib.ttf", 112)
    reg = font("OG_FONT_REGULAR", "C:/Windows/Fonts/segoeui.ttf", 32)
    mono = font("OG_FONT_MONO", "C:/Windows/Fonts/consolab.ttf", 26)

    d.text((66, 190), "Mat-Tech", font=bold, fill=WHITE)
    d.text((66, 310), "Cloud", font=bold, fill=GREEN_BRIGHT)
    d.text((72, 462), "Online services of Mat-Tech, specialists in", font=reg, fill=(214, 218, 221))
    d.text((72, 504), "vacuum brazing, brazing and soldering.", font=reg, fill=(214, 218, 221))
    d.text((72, 562), "M A T - T E C H . C L O U D", font=mono, fill=GREEN_BRIGHT)

    img.save(OUT / "og-image.png", optimize=True)
    print("wrote og-image.png", img.size)


def main():
    OUT.mkdir(exist_ok=True)

    # Browser and search favicons. Google wants a square icon whose size is a multiple of 48 px.
    ico_sizes = [16, 32, 48]
    ico_master = mark(256)
    ico_master.save(OUT / "favicon.ico", sizes=[(s, s) for s in ico_sizes])
    print("wrote favicon.ico", ico_sizes)
    for s in (16, 32, 48, 96):
        save_png(mark(s), f"favicon-{s}x{s}.png")

    # Apple touch icon: opaque, square corners (iOS rounds them itself).
    save_png(mark(180, corner=0, scale=0.74).convert("RGB"), "apple-touch-icon.png")

    # Web app manifest icons
    save_png(mark(192), "icon-192.png")
    save_png(mark(512), "icon-512.png")
    # Maskable: full-bleed background, mark kept inside the 80% safe zone
    save_png(mark(512, corner=0, scale=0.62), "icon-maskable-512.png")

    # Logos for structured data (Google wants at least 112 x 112) and the page header
    logo = Image.open(TOOLS / "logo-source.png").convert("RGBA")
    logo = logo.crop(logo.getbbox())
    pad = 40
    canvas = Image.new("RGB", (logo.width + 2 * pad, logo.height + 2 * pad), WHITE)
    canvas.paste(logo, (pad, pad), logo)
    save_png(canvas, "logo.png")
    dark = Image.open(TOOLS / "logo-dark-source.png").convert("RGBA")
    dark = dark.crop(dark.getbbox())
    dark = dark.resize((600, round(dark.height * 600 / dark.width)), Image.LANCZOS)
    save_png(dark, "logo-dark.png")

    og_image()


if __name__ == "__main__":
    main()
