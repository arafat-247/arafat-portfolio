"""Replace text-heavy generated social cards in related-story panels.

Use a real article cover when the target page has one; otherwise use the
existing neutral editorial placeholder. This runs after build_case_studies.py.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = "https://arafatrahaman.com"

CARD_RE = re.compile(
    r'(?P<open><article class="portfolio-related-card">.*?'
    r'<a class="portfolio-related-card__image" href="(?P<href>[^"]+)"[^>]*>)'
    r'(?P<visual>.*?)'
    r'(?P<close></a>.*?</article>)',
    re.I | re.S,
)
COVER_RE = re.compile(
    r'<figure class="cover">.*?<img[^>]+src="(?P<src>[^"]+)"[^>]*>',
    re.I | re.S,
)
SOCIAL_IMAGE_RE = re.compile(r'/assets/social/', re.I)


def local_page(href: str) -> Path | None:
    path = urlsplit(href).path
    if not path.startswith("/") or ".." in path.split("/") or not path.endswith("/"):
        return None
    target = DIST / path.lstrip("/") / "index.html"
    return target if target.is_file() else None


def cover_for(href: str) -> str | None:
    target = local_page(href)
    if not target:
        return None
    source = target.read_text(encoding="utf-8")
    match = COVER_RE.search(source)
    if not match:
        return None
    src = html.unescape(match.group("src")).strip()
    if not src or SOCIAL_IMAGE_RE.search(src):
        return None
    absolute = urljoin(SITE + urlsplit(href).path, src)
    parts = urlsplit(absolute)
    if parts.scheme in ("http", "https") and parts.netloc:
        if parts.netloc == "arafatrahaman.com":
            return parts.path + (("?" + parts.query) if parts.query else "")
        return absolute
    return None


def related_thumbnail(cover: str) -> str:
    parts = urlsplit(cover)
    if parts.netloc and parts.netloc != "arafatrahaman.com":
        return cover
    rel = parts.path.lstrip("/")
    if not rel.startswith("assets/"):
        return cover
    source = DIST / rel
    if not source.is_file():
        source = ROOT / "site" / rel
    if not source.is_file():
        return cover
    target_dir = DIST / "assets" / "related"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{source.stem}-related.webp"
    try:
        if not target.is_file() or target.stat().st_mtime < source.stat().st_mtime:
            with Image.open(source) as original:
                image = ImageOps.exif_transpose(original)
                image = ImageOps.fit(image, (720, 405), method=Image.Resampling.LANCZOS)
                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert("RGB")
                image.save(target, "WEBP", quality=70, method=6)
        return "/assets/related/" + target.name
    except (OSError, ValueError):
        return cover


def replace_card(match: re.Match[str]) -> str:
    href = html.unescape(match.group("href"))
    cover = cover_for(href)
    if cover:
        cover = related_thumbnail(cover)
        visual = (
            f'<img src="{html.escape(cover, quote=True)}" alt="" width="720" height="405" '
            'loading="lazy" decoding="async" fetchpriority="low">'
        )
    else:
        visual = '<span class="portfolio-related-card__placeholder" aria-hidden="true"></span>'
    return match.group("open") + visual + match.group("close")


def main() -> None:
    changed_pages = 0
    changed_cards = 0
    for page in list((DIST / "stories").glob("*/index.html")) + list((DIST / "thoughts").glob("*/index.html")):
        source = page.read_text(encoding="utf-8")
        if 'class="portfolio-related-card"' not in source:
            continue
        updated, count = CARD_RE.subn(replace_card, source)
        if count and updated != source:
            page.write_text(updated, encoding="utf-8")
            changed_pages += 1
            changed_cards += count
    print(f"Related preview cleanup: pages={changed_pages}, cards={changed_cards}")


if __name__ == "__main__":
    main()
