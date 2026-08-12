"""Draw the series' standard red callouts onto a screenshot.

One consistent stroke weight, corner radius and colour across every article, so
the whole series shares a visual language.

    python tools/annotate.py docs/screenshots/02_player_scene.png \
        --box 40,120,360,190 \
        --label 40,120,"Scene tree" \
        --arrow 700,300,520,240

Boxes are x,y,w,h. Arrows are x1,y1,x2,y2 and point AT (x2,y2).
Writes <name>_annotated.png next to the source unless --out is given.
"""
import argparse
import math
import os

from PIL import Image, ImageDraw, ImageFont

ACCENT = (255, 82, 82)
STROKE = 6
RADIUS = 10
HEAD = 26  # arrowhead length in px


def font(size):
    for name in ("seguisb.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)
        except OSError:
            continue
    return ImageFont.load_default()


def triple(s, n, name):
    parts = s.split(",")
    if len(parts) < n:
        raise argparse.ArgumentTypeError("%s needs %d comma-separated numbers" % (name, n))
    return parts


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--box", action="append", default=[], help="x,y,w,h")
    p.add_argument("--arrow", action="append", default=[], help="x1,y1,x2,y2")
    p.add_argument("--label", action="append", default=[], help="x,y,text")
    p.add_argument("--size", type=int, default=34, help="label font size")
    p.add_argument("--out")
    a = p.parse_args()

    img = Image.open(a.image).convert("RGB")
    d = ImageDraw.Draw(img)

    for spec in a.box:
        x, y, w, h = (int(v) for v in triple(spec, 4, "--box")[:4])
        d.rounded_rectangle([x, y, x + w, y + h], RADIUS, outline=ACCENT, width=STROKE)

    for spec in a.arrow:
        x1, y1, x2, y2 = (int(v) for v in triple(spec, 4, "--arrow")[:4])
        d.line([x1, y1, x2, y2], fill=ACCENT, width=STROKE)
        ang = math.atan2(y2 - y1, x2 - x1)
        for side in (+1, -1):
            t = ang + side * math.radians(28)
            d.line([x2, y2, x2 - HEAD * math.cos(t), y2 - HEAD * math.sin(t)],
                   fill=ACCENT, width=STROKE)

    f = font(a.size)
    for spec in a.label:
        parts = triple(spec, 3, "--label")
        x, y = int(parts[0]), int(parts[1])
        text = ",".join(parts[2:])
        tw, th = d.textbbox((0, 0), text, font=f)[2:]
        # Solid plate so the label stays readable over busy editor UI.
        d.rounded_rectangle([x, y - th - 18, x + tw + 24, y - 2], 8, fill=ACCENT)
        d.text((x + 12, y - th - 12), text, font=f, fill=(255, 255, 255))

    out = a.out or os.path.splitext(a.image)[0] + "_annotated.png"
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
