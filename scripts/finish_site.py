"""Final housekeeping pass for the generated public site.

Runs after every other build step (see .github/workflows/deploy.yml). It does
not change the design. It only:

* removes private or off-topic pages (companion apps, the private reporting
  desk, design previews) from the public output, its links and the sitemap;
* crops the publisher strip baked into imported archive cover images.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

PRIVATE_DIRS = ("assistant", "android", "voice", "newsroom", "desktop-preview", "inner-preview")

LINK_TO_PRIVATE = re.compile(
    r'<a\b[^>]*href="(?:\.\./|/)*(?:' + "|".join(PRIVATE_DIRS) + r')/"[^>]*>.*?</a>', re.I | re.S
)


def remove_private_pages() -> int:
    removed = 0
    for name in PRIVATE_DIRS:
        target = DIST / name
        if target.exists():
            shutil.rmtree(target)
            removed += 1
    sitemap = DIST / "sitemap.xml"
    if sitemap.is_file():
        xml = sitemap.read_text(encoding="utf-8")
        for name in PRIVATE_DIRS:
            xml = re.sub(rf"<url>\s*<loc>[^<]*/{name}/[^<]*</loc>.*?</url>", "", xml, flags=re.S)
        sitemap.write_text(xml, encoding="utf-8")
    return removed


def strip_private_links() -> int:
    changed = 0
    for page in DIST.rglob("*.html"):
        if "admin" in page.relative_to(DIST).parts:
            continue
        source = page.read_text(encoding="utf-8")
        updated = LINK_TO_PRIVATE.sub("", source)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


STRIP = (11, 32, 99)


def _is_strip(pixel) -> bool:
    return abs(pixel[0] - STRIP[0]) < 18 and abs(pixel[1] - STRIP[1]) < 18 and abs(pixel[2] - STRIP[2]) < 22


def crop_publisher_strip(path: Path) -> bool:
    try:
        with Image.open(path) as original:
            image = original.convert("RGB")
            fmt = original.format
    except (OSError, ValueError):
        return False
    w, h = image.size
    if h < 120:
        return False
    xs = (w // 12, w // 4, w // 2)  # left and centre only: the publisher logo sits on the right
    y = h - 1
    while y > h * 0.75 and all(_is_strip(image.getpixel((x, y))) for x in xs):
        y -= 1
    if h - 1 - y < h * 0.05:
        return False
    # Trim a few extra rows: JPEG blends the strip edge into the photograph.
    cropped = image.crop((0, 0, w, max(1, y - 2)))
    if fmt == "PNG":
        cropped.save(path, "PNG", optimize=True)
    elif fmt == "WEBP":
        cropped.save(path, "WEBP", quality=84)
    else:
        cropped.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return True


def crop_imported() -> int:
    folder = DIST / "assets" / "imported"
    if not folder.is_dir():
        return 0
    return sum(crop_publisher_strip(p) for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"))


def main() -> None:
    removed = remove_private_pages()
    links = strip_private_links()
    cropped = crop_imported()
    print(f"Finish: private_dirs_removed={removed}, pages_with_private_links_removed={links}, images_cropped={cropped}")


if __name__ == "__main__":
    main()
