"""Generate the blog-ready copy of an article.

    python tools/blog_export.py

Takes the repo article (which uses relative image paths so GitHub renders it)
and writes docs/part1-blog.md with:

  * image paths rewritten to the S3 bucket
  * every image wrapped as a clickable half-size thumbnail

Width is half each image's real pixel width rather than width="50%", because a
percentage is relative to the container: it would stretch the small 440px
scene-tree capture UP to fill half a wide column and make it blurry. A pixel
width never upscales, and a blog theme's `img { max-width: 100% }` still lets
it shrink responsively on narrow screens.
"""
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLE = os.path.join(ROOT, "build_a_cozy_farming_game_part1_polished.md")
SHOTS = os.path.join(ROOT, "docs", "screenshots")
OUT = os.path.join(ROOT, "docs", "part1-blog.md")

BASE = "https://inkwell-uploads-prod.s3.us-east-1.amazonaws.com/uploads/godot/cozyfarm/"

TEMPLATE = (
    '<a href="{url}" target="_blank" rel="noopener">\n'
    '  <img src="{url}" alt="{alt}" width="{w}" loading="lazy">\n'
    '</a>'
)


def main():
    text = open(ARTICLE, encoding="utf-8").read()
    seen = []

    def repl(m):
        alt, path = m.group(1), m.group(2)
        name = os.path.basename(path)
        local = os.path.join(SHOTS, name)
        if not os.path.exists(local):
            raise SystemExit("missing image: %s" % local)
        full = Image.open(local).width
        half = full // 2
        seen.append((name, full, half))
        return TEMPLATE.format(url=BASE + name, alt=alt.replace('"', "&quot;"), w=half)

    out = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, text)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)

    print("%-32s %10s %10s" % ("image", "natural", "displayed"))
    for name, full, half in seen:
        print("%-32s %9dpx %9dpx" % (name, full, half))
    print("\n%d images rewritten -> %s" % (len(seen), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
