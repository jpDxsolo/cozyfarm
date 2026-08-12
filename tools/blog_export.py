"""Generate the blog-ready copy of an article.

    python tools/blog_export.py

Takes the repo article (which uses relative image paths so GitHub renders it)
and writes docs/part1-blog.md with:

  * image paths rewritten to the S3 bucket
  * every image shown as a half-size thumbnail that links to the full size

The blog strips raw HTML, so `<a><img width=...>` is not available and the
output is plain `[![alt](thumb)](full)`. Markdown has no width syntax, so the
thumbnail has to be a physically smaller file: run tools/make_thumbs.py first
and upload the *_half.png files alongside the originals.
"""
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLE = os.path.join(ROOT, "build_a_cozy_farming_game_part1_polished.md")
SHOTS = os.path.join(ROOT, "docs", "screenshots")
OUT = os.path.join(ROOT, "docs", "part1-blog.md")

BASE = "https://inkwell-uploads-prod.s3.us-east-1.amazonaws.com/uploads/godot/cozyfarm/"

THUMBS = os.path.join(SHOTS, "half")

# Thumbnail links to the full-size image. Pure markdown, no HTML.
TEMPLATE = "[![{alt}]({thumb})]({full})"


def main():
    text = open(ARTICLE, encoding="utf-8").read()
    seen = []

    def repl(m):
        alt, path = m.group(1), m.group(2)
        name = os.path.basename(path)
        stem = os.path.splitext(name)[0]
        thumb_name = stem + "_half.png"

        local = os.path.join(SHOTS, name)
        thumb = os.path.join(THUMBS, thumb_name)
        for p in (local, thumb):
            if not os.path.exists(p):
                raise SystemExit("missing: %s\n(run tools/make_thumbs.py first)" % p)

        seen.append((name, Image.open(local).width, Image.open(thumb).width))
        return TEMPLATE.format(alt=alt, thumb=BASE + thumb_name, full=BASE + name)

    out = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, text)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)

    print("%-32s %10s %10s" % ("image", "full", "thumb"))
    for name, full, half in seen:
        print("%-32s %9dpx %9dpx" % (name, full, half))
    print("\n%d images rewritten -> %s" % (len(seen), os.path.relpath(OUT, ROOT)))
    print("upload: %d full-size + %d *_half.png thumbnails"
          % (len(seen), len(seen)))


if __name__ == "__main__":
    main()
