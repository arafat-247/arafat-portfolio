#!/usr/bin/env python3
"""
Build a full static portfolio archive from the public Daily Star author pages.

Changes from v1:
* follows ?page=1, ?page=2, ...;
* deduplicates archive entries;
* extracts article bodies;
* generates local pages under site/stories/.../;
* keeps original-source attribution and canonical links.

The existing GitHub Actions command remains valid:
    python scripts/update_articles.py --limit 40

Here, --limit means maximum number of author archive pages to inspect.
Use full-text mirroring only when you have the necessary republication rights.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import trafilatura

AUTHOR_URL = "https://www.thedailystar.net/author/arafat-rahaman"
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
OUTPUT = SITE / "data" / "articles.json"
STORIES_DIR = SITE / "stories"

UA = (
    "Mozilla/5.0 (compatible; ArafatPortfolioIndexer/2.0; "
    "public-author-page-portfolio)"
)

ARTICLE_ID_RE = re.compile(r"-(\d{5,})/?$")
ARTICLE_HINTS = (
    "/news/", "/opinion/", "/business/", "/sports/", "/entertainment/",
    "/lifestyle/", "/youth/", "/supplements/", "/slow-reads/",
    "/analysis/", "/views/", "/culture/", "/star-multimedia/"
)

ALLOWED_BODY_TAGS = {
    "p", "h2", "h3", "h4", "blockquote",
    "ul", "ol", "li", "strong", "b", "em", "i",
    "a", "br", "table", "thead", "tbody", "tr", "th", "td"
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def get_meta(soup: BeautifulSoup, key: str, value: str) -> str:
    node = soup.find("meta", attrs={key: value})
    return clean(node.get("content", "")) if node else ""


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk_json(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_json(v)


def json_ld_values(soup: BeautifulSoup, field: str):
    values = []
    for node in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = node.string or node.get_text()
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except Exception:
            continue
        for obj in walk_json(payload):
            if isinstance(obj, dict) and field in obj:
                values.append(obj[field])
    return values


def normalise_source_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(fragment="", query="").geturl()


def author_page_url(page: int) -> str:
    return AUTHOR_URL if page == 0 else f"{AUTHOR_URL}?page={page}"


def section_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    mapping = [
        ("/education/", "Education"),
        ("/politics/", "Politics"),
        ("/governance/", "Governance"),
        ("/crime", "Crime and Justice"),
        ("/health", "Health"),
        ("/environment/", "Environment"),
        ("/agriculture/", "Agriculture"),
        ("/business/", "Business"),
        ("/sports/", "Sports"),
        ("/opinion/", "Opinion"),
        ("/views/", "Opinion"),
        ("/analysis/", "Analysis"),
        ("/culture/", "Culture"),
        ("/entertainment/", "Culture"),
        ("/youth/", "Youth"),
        ("/supplements/", "Supplement"),
    ]
    for token, label in mapping:
        if token in path:
            return label
    return "News"


def parse_date(raw: str) -> str:
    raw = clean(raw)
    if not raw:
        return ""

    match = re.match(r"^(\d{4}-\d{2}-\d{2})", raw)
    if match:
        return match.group(1)

    # Common Daily Star forms, with optional time after a comma.
    candidates = [raw]
    time_match = re.match(r"^(.+?\d{4}),\s*\d{1,2}:\d{2}", raw)
    if time_match:
        candidates.insert(0, time_match.group(1))

    for candidate in candidates:
        for fmt in (
            "%d %B %Y", "%d %b %Y",
            "%B %d, %Y", "%b %d, %Y",
            "%B %d %Y", "%b %d %Y"
        ):
            try:
                return datetime.strptime(candidate.strip(), fmt).date().isoformat()
            except ValueError:
                pass
    return ""


def extract_authors(soup: BeautifulSoup) -> list[str]:
    names = []

    for value in json_ld_values(soup, "author"):
        items = value if isinstance(value, list) else [value]
        for item in items:
            if isinstance(item, dict):
                name = clean(str(item.get("name", "")))
            else:
                name = clean(str(item))
            if name and name not in names:
                names.append(name)

    if names:
        return names[:10]

    for selector in ('[rel="author"]', '.author-name', '.byline a', '[class*="author"] a'):
        for node in soup.select(selector):
            name = clean(node.get_text(" ", strip=True))
            if name and len(name) <= 100 and name not in names:
                names.append(name)
        if names:
            break

    return names[:10]


def discover_story_links(session: requests.Session, page: int) -> list[str]:
    response = session.get(author_page_url(page), timeout=35)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    host = urlparse(AUTHOR_URL).netloc
    links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = normalise_source_url(urljoin(AUTHOR_URL, a["href"]))
        parsed = urlparse(href)

        if parsed.netloc != host:
            continue
        if not any(hint in parsed.path.lower() for hint in ARTICLE_HINTS):
            continue
        if not ARTICLE_ID_RE.search(parsed.path):
            continue
        if href in seen:
            continue

        seen.add(href)
        links.append(href)

    return links


def fallback_body(soup: BeautifulSoup) -> str:
    candidates = [
        "article .article-content",
        "article [class*='article-body']",
        "article [class*='story-body']",
        ".article-content",
        ".article-body",
        ".story-content",
        ".field--name-body",
        "article",
        "main",
    ]

    node = None
    for selector in candidates:
        node = soup.select_one(selector)
        if node:
            break

    if not node:
        return ""

    clone = BeautifulSoup(str(node), "html.parser")
    for bad in clone.select(
        "script, style, nav, aside, form, button, noscript, iframe, "
        ".related, .share, [class*='advert'], [id*='advert'], "
        "[class*='newsletter'], [class*='social']"
    ):
        bad.decompose()

    parts = []
    for el in clone.find_all(
        ["p", "h2", "h3", "h4", "blockquote", "ul", "ol", "table"]
    ):
        text = clean(el.get_text(" ", strip=True))
        if len(text) < 2:
            continue
        parts.append(str(el))
    return "\n".join(parts)


def sanitise_body(raw_html: str, source_url: str) -> str:
    soup = BeautifulSoup(raw_html or "", "html.parser")

    for bad in soup.find_all(
        ["script", "style", "iframe", "form", "button", "input", "svg"]
    ):
        bad.decompose()

    for tag in list(soup.find_all(True)):
        if tag.name not in ALLOWED_BODY_TAGS:
            tag.unwrap()
            continue

        keep = {}
        if tag.name == "a":
            href = tag.get("href")
            if href:
                keep["href"] = urljoin(source_url, href)
                keep["rel"] = "noopener"
        tag.attrs = keep

    return str(soup).strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:70] or "story"


def story_key(story: dict) -> str:
    match = ARTICLE_ID_RE.search(urlparse(story["url"]).path)
    if match:
        prefix = match.group(1)
    else:
        prefix = hashlib.sha1(story["url"].encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{slugify(story.get('title', 'story'))}"


def local_url_for(story: dict) -> str:
    return f"stories/{story_key(story)}/"


def extract_story(session: requests.Session, url: str) -> dict:
    response = session.get(url, timeout=40)
    response.raise_for_status()
    page_html = response.text
    soup = BeautifulSoup(page_html, "html.parser")

    title = (
        get_meta(soup, "property", "og:title")
        or get_meta(soup, "name", "twitter:title")
        or clean(soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else "")
    )
    title = re.sub(r"\s*\|\s*The Daily Star\s*$", "", title, flags=re.I)

    excerpt = (
        get_meta(soup, "property", "og:description")
        or get_meta(soup, "name", "description")
        or get_meta(soup, "name", "twitter:description")
    )

    raw_date = (
        get_meta(soup, "property", "article:published_time")
        or get_meta(soup, "name", "date")
        or get_meta(soup, "name", "pubdate")
    )
    if not raw_date:
        for value in json_ld_values(soup, "datePublished"):
            if isinstance(value, str) and value.strip():
                raw_date = value
                break
    if not raw_date:
        t = soup.find("time")
        if t:
            raw_date = t.get("datetime") or t.get_text(" ", strip=True)

    raw_section = (
        get_meta(soup, "property", "article:section")
        or get_meta(soup, "name", "section")
    )
    section = clean(raw_section).title() if raw_section else section_from_url(url)

    lead_image = (
        get_meta(soup, "property", "og:image")
        or get_meta(soup, "name", "twitter:image")
    )

    extracted = trafilatura.extract(
        page_html,
        url=url,
        include_comments=False,
        include_tables=True,
        include_images=False,
        favor_precision=True,
        output_format="html",
    ) or ""

    body_html = sanitise_body(extracted, url)
    body_text = clean(
        BeautifulSoup(body_html, "html.parser").get_text(" ", strip=True)
    )
    if len(body_text) < 180:
        body_html = sanitise_body(fallback_body(soup), url)

    if not title:
        raise RuntimeError("Headline could not be extracted")

    story = {
        "title": title,
        "date": parse_date(raw_date),
        "section": section,
        "excerpt": excerpt,
        "url": normalise_source_url(url),
        "authors": extract_authors(soup),
        "image": lead_image,
        "body_html": body_html,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "featured": False,
    }
    story["local_url"] = local_url_for(story)
    return story


def display_date(iso_date: str) -> str:
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        return f"{dt.day} {dt.strftime('%B %Y')}"
    except Exception:
        return iso_date or ""


def generate_story_page(story: dict) -> str:
    title = html_lib.escape(story.get("title", "Story"))
    excerpt = html_lib.escape(story.get("excerpt", ""))
    section = html_lib.escape(story.get("section", "Reporting"))
    date = html_lib.escape(display_date(story.get("date", "")))
    source = html_lib.escape(story.get("url", ""), quote=True)
    authors = story.get("authors") or ["Arafat Rahaman"]
    author_text = html_lib.escape(", ".join(authors))
    body = story.get("body_html", "").strip()

    if not body:
        body = (
            '<div class="article-error">'
            "<p>The full article text could not be extracted automatically from the source page.</p>"
            f'<p><a href="{source}" target="_blank" rel="noopener">Read the original at The Daily Star ↗</a></p>'
            "</div>"
        )

    dek = f'<p class="article-dek">{excerpt}</p>' if excerpt else ""
    date_sep = f" · {date}" if date else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,follow">
  <meta name="description" content="{excerpt}">
  <link rel="canonical" href="{source}">
  <title>{title} — Arafat Rahaman</title>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap nav-wrap">
      <a class="brand" href="../../">
        <span class="brand-mark">AR</span>
        <span class="brand-text">Arafat Rahaman</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="../../#work">Work</a>
        <a href="../../#about">About</a>
        <a class="nav-source" href="{source}" target="_blank" rel="noopener">Daily Star ↗</a>
      </nav>
    </div>
  </header>

  <main class="article-shell wrap">
    <div class="article-topline">
      <a href="../../#work">← Reporting archive</a>
      <span>{section}</span>
    </div>

    <article>
      <header class="article-header">
        <p class="article-kicker">{section}{date_sep}</p>
        <h1 class="article-title">{title}</h1>
        {dek}
        <div class="article-byline">
          <span>By <strong>{author_text}</strong></span>
          <span>Originally published by <em>The Daily Star</em></span>
        </div>
      </header>

      <div class="article-source-note">
        Portfolio copy from a publicly available article page.
        <a href="{source}" target="_blank" rel="noopener">View the original publication ↗</a>
      </div>

      <div class="article-body">
        {body}
      </div>

      <div class="article-end">
        <a href="../../#work">← Back to reporting archive</a>
        <a href="{source}" target="_blank" rel="noopener">Original at The Daily Star ↗</a>
      </div>
    </article>
  </main>

  <footer>
    <div class="wrap footer-inner">
      <div class="brand footer-brand">
        <span class="brand-mark">AR</span>
        <span class="brand-text">Arafat Rahaman</span>
      </div>
      <p>Portfolio archive. Original publication remains the source of record.</p>
      <a href="../../">Home ↑</a>
    </div>
  </footer>
</body>
</html>
"""


def write_story_pages(articles: list[dict]) -> None:
    if STORIES_DIR.exists():
        shutil.rmtree(STORIES_DIR)
    STORIES_DIR.mkdir(parents=True, exist_ok=True)

    for story in articles:
        if not story.get("url"):
            continue
        story["local_url"] = local_url_for(story)
        folder = STORIES_DIR / story_key(story)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(
            generate_story_page(story),
            encoding="utf-8"
        )


def load_existing() -> dict:
    if OUTPUT.exists():
        try:
            return json.loads(OUTPUT.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"updated_at": "", "articles": []}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="Maximum number of author archive pages to inspect."
    )
    parser.add_argument("--delay", type=float, default=0.45)
    parser.add_argument(
        "--refresh-all",
        action="store_true",
        help="Re-fetch stories even when a cached full body exists."
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    existing = load_existing()
    old = {
        normalise_source_url(a.get("url", "")): a
        for a in existing.get("articles", [])
        if a.get("url")
    }

    session = requests.Session()
    session.headers.update({
        "User-Agent": UA,
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
    })

    discovered = []
    discovered_set = set()
    no_new_streak = 0

    try:
        for page in range(max(1, args.limit)):
            try:
                links = discover_story_links(session, page)
            except Exception as exc:
                print(f"Archive page {page}: {exc}", file=sys.stderr)
                no_new_streak += 1
                if page >= 3 and no_new_streak >= 3:
                    break
                continue

            new_links = [u for u in links if u not in discovered_set]
            print(
                f"Archive page {page}: {len(links)} links, "
                f"{len(new_links)} new",
                file=sys.stderr
            )

            if new_links:
                no_new_streak = 0
                for url in new_links:
                    discovered_set.add(url)
                    discovered.append(url)
            else:
                no_new_streak += 1

            if page >= 3 and no_new_streak >= 3:
                break

            time.sleep(max(0.0, args.delay))

        if not discovered and not old:
            raise RuntimeError("No story URLs were discovered")

        refreshed = []
        total = len(discovered)

        for i, url in enumerate(discovered, 1):
            prior = old.get(url)
            has_cached_body = bool(prior and prior.get("body_html"))

            if prior and has_cached_body and not args.refresh_all:
                story = dict(prior)
                story["local_url"] = local_url_for(story)
                refreshed.append(story)
                print(f"[{i}/{total}] cached: {story.get('title','')}", file=sys.stderr)
                continue

            try:
                story = extract_story(session, url)
                refreshed.append(story)
                print(f"[{i}/{total}] fetched: {story['title']}", file=sys.stderr)
            except Exception as exc:
                print(f"[{i}/{total}] failed {url}: {exc}", file=sys.stderr)
                if prior:
                    story = dict(prior)
                    story["local_url"] = local_url_for(story)
                    refreshed.append(story)

            if i < total:
                time.sleep(max(0.0, args.delay))

        seen = {
            normalise_source_url(a.get("url", ""))
            for a in refreshed if a.get("url")
        }
        for url, story in old.items():
            if url not in seen:
                kept = dict(story)
                kept["local_url"] = local_url_for(kept)
                refreshed.append(kept)

        unique = {}
        for story in refreshed:
            url = normalise_source_url(story.get("url", ""))
            if url:
                story["url"] = url
                story["local_url"] = local_url_for(story)
                unique[url] = story

        articles = sorted(
            unique.values(),
            key=lambda a: (a.get("date", ""), a.get("title", "")),
            reverse=True
        )

        for story in articles:
            story["featured"] = False
        if articles:
            articles[0]["featured"] = True

        write_story_pages(articles)

        payload = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source": AUTHOR_URL,
            "articles": articles,
        }
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        print(
            f"Completed: {len(articles)} stories; "
            f"local pages written to {STORIES_DIR}",
            file=sys.stderr
        )
        return 0

    except Exception as exc:
        print(f"Refresh failed: {exc}", file=sys.stderr)
        if existing.get("articles"):
            cached = existing["articles"]
            for story in cached:
                if story.get("url"):
                    story["local_url"] = local_url_for(story)
            write_story_pages(cached)
            existing["updated_at"] = datetime.now(timezone.utc).isoformat()
            OUTPUT.write_text(
                json.dumps(existing, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            print("Existing archive retained.", file=sys.stderr)
            return 1 if args.strict else 0
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
