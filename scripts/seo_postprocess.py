"""Post-process generated output for cleaner search-engine migration signals."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE_HOST = "arafatrahaman.com"
REDIRECT_NOINDEX = '<meta name="robots" content="noindex,follow">'
INSTANT_REFRESH = re.compile(r'<meta http-equiv="refresh" content="0;url=[^"]+">', re.I)
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)">', re.I)
OG_IMAGE = re.compile(r'<meta property="og:image" content="([^"]+)">', re.I)
JSON_LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.I | re.S)
ARTICLE_MODIFIED = re.compile(r'<meta property="article:modified_time" content="([^"]+)">', re.I)
ARTICLE_PUBLISHED = re.compile(r'<meta property="article:published_time" content="([^"]+)">', re.I)
SITEMAP_URL = re.compile(r'<url><loc>([^<]+)</loc>(?:<lastmod>[^<]+</lastmod>)?</url>')


def is_site_url(url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == "https" and parts.hostname == SITE_HOST


def optimise_permanent_redirects() -> int:
    """Make legacy GitHub Pages redirects immediate and visually silent.

    GitHub Pages cannot emit configurable HTTP 301 responses for these static
    legacy files. The generated pages therefore use canonical + zero-second
    meta refresh + location.replace(). This post-process removes the noindex
    signal and moves the JavaScript redirect into the head so visitors do not
    see the old "Moved" interstitial before landing on the clean URL.
    """
    changed = 0
    for page in DIST.rglob("*.html"):
        source = page.read_text(encoding="utf-8")
        canonical = CANONICAL.search(source)
        if not canonical or not is_site_url(canonical.group(1)) or not INSTANT_REFRESH.search(source):
            continue
        destination = canonical.group(1)
        destination_json = json.dumps(destination)
        clean = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="canonical" href="{destination}"><script>const destination=new URL({destination_json});if(location.search)destination.search=location.search;if(location.hash)destination.hash=location.hash;location.replace(destination.href);</script><meta http-equiv="refresh" content="0;url={destination}"><title>Redirecting…</title><style>html,body{{margin:0;background:#fff}}body{{visibility:hidden}}</style></head><body><noscript><style>body{{visibility:visible;font-family:system-ui,sans-serif;padding:2rem}}</style><p>This address has changed. <a href="{destination}">Continue to the page</a>.</p></noscript></body></html>'''
        if source != clean:
            page.write_text(clean, encoding="utf-8")
            changed += 1
    return changed


def add_article_images_to_schema() -> int:
    """Use the page's generated social image as the Article image when absent."""
    changed = 0
    for page in DIST.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        image_match = OG_IMAGE.search(html)
        if not image_match or not is_site_url(image_match.group(1)):
            continue

        def replace_schema(match: re.Match[str]) -> str:
            nonlocal changed
            try:
                data = json.loads(match.group(2))
            except json.JSONDecodeError:
                return match.group(0)
            if data.get("@type") != "Article" or data.get("image"):
                return match.group(0)
            data["image"] = image_match.group(1)
            payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
            changed += 1
            return match.group(1) + payload + match.group(3)

        updated = JSON_LD.sub(replace_schema, html, count=1)
        if updated != html:
            page.write_text(updated, encoding="utf-8")
    return changed


def local_page_for(url: str) -> Path | None:
    if not is_site_url(url):
        return None
    path = urlsplit(url).path
    if path == "/":
        return DIST / "index.html"
    if path.endswith("/"):
        return DIST / path.lstrip("/") / "index.html"
    return DIST / path.lstrip("/")


def article_date(page: Path) -> str | None:
    if not page.is_file():
        return None
    html = page.read_text(encoding="utf-8")
    match = ARTICLE_MODIFIED.search(html) or ARTICLE_PUBLISHED.search(html)
    if not match:
        return None
    value = match.group(1)
    return value[:10] if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:.*)?", value) else None


def add_sitemap_lastmods() -> int:
    """Add accurate lastmod only to article URLs, where the build already knows the date."""
    sitemap = DIST / "sitemap.xml"
    if not sitemap.is_file():
        raise FileNotFoundError("dist/sitemap.xml was not generated")
    xml = sitemap.read_text(encoding="utf-8")
    changed = 0

    def replace_url(match: re.Match[str]) -> str:
        nonlocal changed
        url = match.group(1)
        page = local_page_for(url)
        date = article_date(page) if page else None
        if not date:
            return match.group(0)
        replacement = f"<url><loc>{url}</loc><lastmod>{date}</lastmod></url>"
        if replacement != match.group(0):
            changed += 1
        return replacement

    updated = SITEMAP_URL.sub(replace_url, xml)
    sitemap.write_text(updated, encoding="utf-8")
    return changed


def main() -> None:
    if not DIST.is_dir():
        raise FileNotFoundError("dist/ does not exist; run scripts/build.py first")
    redirects = optimise_permanent_redirects()
    schemas = add_article_images_to_schema()
    sitemap = add_sitemap_lastmods()
    print(f"SEO post-process: redirects={redirects}, article_images={schemas}, sitemap_lastmod={sitemap}")


if __name__ == "__main__":
    main()
