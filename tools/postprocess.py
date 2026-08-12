"""Post-process the raw Godot captures for the tutorial series.

Run after tools/capture_screenshots.tscn:

    python tools/postprocess.py

  1. Upscales every raw 1152x648 capture x2 with nearest-neighbour, so the
     pixel art stays perfectly square. Never use a non-integer scale here.
  2. Builds the two explanatory diagrams:
       04_character_layers.png : BaseSprite + HairSprite = finished character
       11_flip_h.png           : one walk frame, flip_h false vs true
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "screenshots")

SCALE = 2
RAW_W = 1152

BG = (29, 34, 41)          # Godot-ish dark panel
PANEL = (39, 46, 56)
TEXT = (222, 228, 236)
ACCENT = (255, 82, 82)     # the series' callout red

PAD = 48
GAP = 40
LABEL_H = 64


def font(size, bold=False):
    name = "seguisb.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)
    except OSError:
        return ImageFont.load_default()


def upscale_all():
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".png"):
            continue
        path = os.path.join(SRC, f)
        img = Image.open(path)
        if img.width != RAW_W:
            continue
        out = img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)
        out.save(path)
        print("  upscaled %-30s %s -> %s" % (f, img.size, out.size))


def content_bbox(img, pad=14):
    """Bounding box of everything that isn't the flat background colour."""
    bg = img.getpixel((2, 2))
    mask = Image.new("L", img.size, 0)
    px, mp = img.load(), mask.load()
    for y in range(img.height):
        for x in range(img.width):
            p = px[x, y]
            if abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2]) > 24:
                mp[x, y] = 255
    box = mask.getbbox()
    if box is None:
        return (0, 0, img.width, img.height)
    l, t, r, b = box
    return (max(0, l - pad), max(0, t - pad),
            min(img.width, r + pad), min(img.height, b + pad))


def square(box):
    l, t, r, b = box
    side = max(r - l, b - t)
    cx, cy = (l + r) // 2, (t + b) // 2
    return (cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)


def load(name):
    return Image.open(os.path.join(SRC, name)).convert("RGB")


def centered(draw, text, cx, y, fnt, fill):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def figure(panels, seps, out_name):
    """panels = [(image, label), ...]; seps drawn between consecutive panels."""
    n = len(panels)
    # Any rescale here would be non-integer and would smear the pixel art, so
    # panels are pasted at their native crop size.
    tile = panels[0][0].width
    canvas = Image.new("RGB",
                       (PAD * 2 + tile * n + GAP * (n - 1),
                        PAD * 2 + tile + LABEL_H), BG)
    d = ImageDraw.Draw(canvas)
    f_label, f_sep = font(30, bold=True), font(58, bold=True)

    for i, (img, label) in enumerate(panels):
        x = PAD + i * (tile + GAP)
        d.rounded_rectangle([x, PAD, x + tile, PAD + tile], 12, fill=PANEL)
        canvas.paste(img, (x, PAD))
        centered(d, label, x + tile / 2, PAD + tile + 16, f_label, TEXT)
        if i < n - 1 and i < len(seps):
            centered(d, seps[i], x + tile + GAP / 2, PAD + tile / 2 - 40,
                     f_sep, ACCENT)

    canvas.save(os.path.join(SRC, out_name))
    print("  built    %-30s %s" % (out_name, canvas.size))


def main():
    print("upscaling raw captures...")
    upscale_all()

    print("building diagrams...")
    combined = load("04c_combined.png")
    box = square(content_bbox(combined))

    figure([(load("04a_body_only.png").crop(box), "BaseSprite"),
            (load("04b_hair_only.png").crop(box), "HairSprite"),
            (combined.crop(box), "Finished character")],
           ["+", "="],
           "04_character_layers.png")

    figure([(load("11a_walk_right.png").crop(box), "Walk right  -  flip_h = false"),
            (load("11b_walk_left_fliph.png").crop(box), "Walk left  -  flip_h = true")],
           ["\u2192"],
           "11_flip_h.png")


if __name__ == "__main__":
    main()
