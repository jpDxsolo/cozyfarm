"""Build half-size thumbnails for the blog.

    python tools/make_thumbs.py

The blog's markdown renderer strips raw HTML, so there is no way to set a
display width. Click-to-open has to be plain `[![alt](thumb)](full)`, which
means the thumbnail must be a genuinely smaller file.

Three different halving strategies, because one size does not fit all here:

  * Game renders were upscaled x2 with NEAREST, so every 2x2 block is uniform
    and a NEAREST halve is an exact inverse. These come back to the native
    1152x648 render with zero loss.
  * The diagrams are rebuilt at half scale rather than resampled, so their
    pixel-art panels stay crisp and their text stays cleanly rendered.
  * Editor captures are photographic UI, so LANCZOS is right for those.

Writes docs/screenshots/half/<name>_half.png. Upload those alongside the
full-size images; blog_export.py points thumbnails at them.
"""
import os

from PIL import Image, ImageDraw

import postprocess as pp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "screenshots")
DST = os.path.join(SRC, "half")

# Pure game renders: x2 of a native capture, so NEAREST halving is lossless.
GAME = ["01_hero.png", "07a_camera_zoom_before.png", "07b_camera_zoom_after.png",
        "09_tiny_farm.png", "10_final_game.png"]

# Editor UI captures: real screenshots, resample properly.
EDITOR = ["02_player_scene.png", "03_spriteframes.png", "05_collision.png",
          "06_input_map.png", "08_animated_tree.png"]

# Half-scale figure metrics (exactly half of postprocess.py's).
H_PAD, H_GAP, H_LABEL = 24, 20, 32


def half_figure(panels, seps, out_name):
    tile = panels[0][0].width
    n = len(panels)
    canvas = Image.new("RGB",
                       (H_PAD * 2 + tile * n + H_GAP * (n - 1),
                        H_PAD * 2 + tile + H_LABEL), pp.BG)
    d = ImageDraw.Draw(canvas)
    f_label, f_sep = pp.font(15, bold=True), pp.font(29, bold=True)

    for i, (img, label) in enumerate(panels):
        x = H_PAD + i * (tile + H_GAP)
        d.rounded_rectangle([x, H_PAD, x + tile, H_PAD + tile], 6, fill=pp.PANEL)
        canvas.paste(img, (x, H_PAD))
        pp.centered(d, label, x + tile / 2, H_PAD + tile + 8, f_label, pp.TEXT)
        if i < n - 1 and i < len(seps):
            pp.centered(d, seps[i], x + tile + H_GAP / 2, H_PAD + tile / 2 - 20,
                        f_sep, pp.ACCENT)

    out = os.path.join(DST, out_name)
    canvas.save(out)
    print("  %-34s %dx%d" % (os.path.basename(out), canvas.width, canvas.height))


def halve(name, resample):
    img = Image.open(os.path.join(SRC, name)).convert("RGB")
    out = img.resize((img.width // 2, img.height // 2), resample)
    stem = os.path.splitext(name)[0]
    path = os.path.join(DST, stem + "_half.png")
    out.save(path)
    print("  %-34s %dx%d" % (os.path.basename(path), out.width, out.height))


def main():
    os.makedirs(DST, exist_ok=True)

    print("game renders (NEAREST, lossless):")
    for n in GAME:
        halve(n, Image.NEAREST)

    print("editor captures (LANCZOS):")
    for n in EDITOR:
        halve(n, Image.LANCZOS)

    print("diagrams (rebuilt at half scale):")
    half = {}
    for n in ["04a_body_only.png", "04b_hair_only.png", "04c_combined.png",
              "11a_walk_right.png", "11b_walk_left_fliph.png"]:
        img = Image.open(os.path.join(SRC, n)).convert("RGB")
        half[n] = img.resize((img.width // 2, img.height // 2), Image.NEAREST)

    box = pp.square(pp.content_bbox(half["04c_combined.png"], pad=7))
    half_figure([(half["04a_body_only.png"].crop(box), "BaseSprite"),
                 (half["04b_hair_only.png"].crop(box), "HairSprite"),
                 (half["04c_combined.png"].crop(box), "Finished character")],
                ["+", "="], "04_character_layers_half.png")
    half_figure([(half["11a_walk_right.png"].crop(box), "flip_h = false"),
                 (half["11b_walk_left_fliph.png"].crop(box), "flip_h = true")],
                ["→"], "11_flip_h_half.png")


if __name__ == "__main__":
    main()
