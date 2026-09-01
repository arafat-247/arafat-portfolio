#!/usr/bin/env python3
"""
Arafat Rahaman portfolio indexer.

Important correctness rule:
A URL is accepted ONLY after the individual article page itself confirms
Arafat Rahaman as an author. This prevents Daily Star site-wide/trending links
that appear above the author archive from contaminating the portfolio.

The crawler:
- walks author archive pages (?page=N), matching the site's Show more flow;
- deduplicates candidate URLs;
- verifies the byline on every candidate;
- extracts article metadata/body;
- writes one local reading page per verified story;
- rebuilds articles.json from verified stories only.

It does not bypass access controls.
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

AUTHOR_NAME = "Arafat Rahaman"
AUTHOR_SLUG = "/author/arafat-rahaman"
AUTHOR_URL = "https://www.thedailystar.net/author/arafat-rahaman"

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA_FILE = SITE / "data" / "articles.json"
STORIES_DIR = SITE / "stories"

ARTICLE_ID = re.compile(r"-(\d{5,})/?$")
STORY_HINTS = (
    "/news/", "/opinion/", "/business/", "/sports/", "/entertainment/",
    "/lifestyle/", "/youth/", "/supplements/", "/slow-reads/", "/analysis/",
    "/views/", "/culture/", "/star-multimedia/", "/ds/"
)

UA = (
    "Mozilla/5.0 (compatible; ArafatRahamanPortfolio/5.0; "
    "public-author-portfolio-indexer)"
)

ALLOWED = {
    "p", "h2", "h3", "h4", "blockquote", "ul", "ol", "li",
    "strong", "b", "em", "i", "a", "br", "table", "thead",
    "tbody", "tr", "th", "td"
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def canonical_source(url: str) -> str:
    p = urlparse(url)
    return p._replace(query="", fragment="").geturl()


def meta(soup: BeautifulSoup, key: str, value: str) -> str:
    node = soup.find("meta", attrs={key: value})
    return clean(node.get("content", "")) if node else ""


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def ld_objects(soup: BeautifulSoup):
    for node in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = node.string or node.get_text()
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except Exception:
            continue
        yield from walk_json(payload)


def author_names_from_ld(soup: BeautifulSoup) -> set[str]:
    names = set()
    for obj in ld_objects(soup):
        if not isinstance(obj, dict) or "author" not in obj:
            continue
        authors = obj["author"]
        items = authors if isinstance(authors, list) else [authors]
        for item in items:
            if isinstance(item, dict):
                name = clean(str(item.get("name", "")))
            else:
                name = clean(str(item))
            if name:
                names.add(name)
    return names


def author_verified(soup: BeautifulSoup) -> bool:
    # Signal 1: structured article author metadata.
    if AUTHOR_NAME.casefold() in {n.casefold() for n in author_names_from_ld(soup)}:
        return True

    # Signal 2: exact author-profile link inside the main article region.
    containers = []
    article = soup.find("article")
    main = soup.find("main")
    if article:
        containers.append(article)
    if main and main is not article:
        containers.append(main)
    if not containers:
        containers.append(soup)

    for container in containers:
        for a in container.find_all("a", href=True):
            href = urlparse(urljoin(AUTHOR_URL, a["href"])).path.rstrip("/")
            text = clean(a.get_text(" ", strip=True))
            if href == AUTHOR_SLUG and text.casefold() == AUTHOR_NAME.casefold():
                return True

    # Signal 3: common byline blocks, still requiring the exact name.
    for selector in (
        ".author-name", ".byline", "[class*='author-name']",
        "[class*='byline']", "[rel='author']"
    ):
        for node in soup.select(selector):
            text = clean(node.get_text(" ", strip=True))
            if AUTHOR_NAME.casefold() in text.casefold():
                return True

    return False


def archive_url(page: int) -> str:
    return AUTHOR_URL if page == 0 else f"{AUTHOR_URL}?page={page}"


def discover_candidates(session: requests.Session, page: int) -> list[str]:
    r = session.get(archive_url(page), timeout=35)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    host = urlparse(AUTHOR_URL).netloc
    found = []
    seen = set()

    for a in soup.find_all("a", href=True):
        url = canonical_source(urljoin(AUTHOR_URL, a["href"]))
        p = urlparse(url)
        if p.netloc != host:
            continue
        if not ARTICLE_ID.search(p.path):
            continue
        if not any(token in p.path.lower() for token in STORY_HINTS):
            continue
        if url in seen:
            continue
        seen.add(url)
        found.append(url)

    return found


def parse_date(raw: str) -> str:
    raw = clean(raw)
    if not raw:
        return ""

    iso = re.match(r"^(\d{4}-\d{2}-\d{2})", raw)
    if iso:
        return iso.group(1)

    candidates = [raw]
    timed = re.match(r"^(.+?\d{4}),\s*\d{1,2}:\d{2}", raw)
    if timed:
        candidates.insert(0, timed.group(1))

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


def extract_authors(soup: BeautifulSoup) -> list[str]:
    names = []
    for name in author_names_from_ld(soup):
        if name not in names:
            names.append(name)

    if AUTHOR_NAME not in names:
        names.insert(0, AUTHOR_NAME)

    return names[:8]


def sanitise_body(raw_html: str, source_url: str) -> str:
    soup = BeautifulSoup(raw_html or "", "html.parser")

    for bad in soup.find_all(
        ["script", "style", "iframe", "form", "button", "input", "svg", "video"]
    ):
        bad.decompose()

    for tag in list(soup.find_all(True)):
        if tag.name not in ALLOWED:
            tag.unwrap()
            continue

        keep = {}
        if tag.name == "a":
            href = tag.get("href")
            if href:
                keep["href"] = urljoin(source_url, href)
                keep["rel"] = "noopener"
                keep["target"] = "_blank"
        tag.attrs = keep

    return str(soup).strip()


def fallback_body(soup: BeautifulSoup, source_url: str) -> str:
    candidates = [
        "article .article-content",
        "article [class*='article-body']",
        "article [class*='story-body']",
        ".article-content",
        ".article-body",
        ".story-content",
        ".field--name-body",
        "article"
    ]

    for selector in candidates:
        node = soup.select_one(selector)
        if not node:
            continue

        clone = BeautifulSoup(str(node), "html.parser")
        for bad in clone.select(
            "script,style,nav,aside,form,button,iframe,"
            ".related,.share,[class*='advert'],[id*='advert'],"
            "[class*='newsletter'],[class*='social']"
        ):
            bad.decompose()

        pieces = []
        for el in clone.find_all(
            ["p", "h2", "h3", "h4", "blockquote", "ul", "ol", "table"]
        ):
            text = clean(el.get_text(" ", strip=True))
            if len(text) >= 2:
                pieces.append(str(el))
        return sanitise_body("\n".join(pieces), source_url)

    return ""


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:64] or "story"


def story_id(source_url: str) -> str:
    match = ARTICLE_ID.search(urlparse(source_url).path)
    if match:
        return match.group(1)
    return hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]


def local_url(story: dict) -> str:
    return f"stories/{story_id(story['url'])}-{slugify(story['title'])}/"


def simplify_story_type(url: str, section: str) -> str:
    text = f"{url} {section}".lower()
    if any(x in text for x in ("/opinion/", "/views/", "/analysis/", "opinion", "analysis")):
        return "Opinion / Analysis"
    return "Reporting"


def topic_from_story(url: str, section: str, title: str) -> str:
    text = f"{url} {section} {title}".lower()
    rules = [
        (("education","school","university","ssc","hsc","ugc","nctb","teacher","student"), "Education"),
        (("politic","parliament","government","cabinet","bnp","jamaat","election"), "Politics & Governance"),
        (("rights","disappear","police","law and order","court","justice","mob"), "Rights & Justice"),
        (("health","dengue","hospital","medical"), "Health"),
        (("environment","climate","pollution","noise"), "Environment"),
        (("business","budget","economy","inflation","fertiliser","agriculture"), "Economy & Livelihoods"),
        (("sports","football","cricket","messi"), "Sport"),
    ]
    for needles, label in rules:
        if any(n in text for n in needles):
            return label
    if section and section.lower() not in {"news","bangladesh"}:
        return section
    return "Public Affairs"


def extract_story(session: requests.Session, url: str) -> dict | None:
    r = session.get(url, timeout=40)
    r.raise_for_status()
    page_html = r.text
    soup = BeautifulSoup(page_html, "html.parser")

    if not author_verified(soup):
        return None

    title = (
        meta(soup, "property", "og:title")
        or meta(soup, "name", "twitter:title")
        or clean(soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else "")
    )
    title = re.sub(r"\s*\|\s*The Daily Star\s*$", "", title, flags=re.I)

    excerpt = (
        meta(soup, "property", "og:description")
        or meta(soup, "name", "description")
        or meta(soup, "name", "twitter:description")
    )

    raw_date = (
        meta(soup, "property", "article:published_time")
        or meta(soup, "name", "date")
        or meta(soup, "name", "pubdate")
    )
    if not raw_date:
        for obj in ld_objects(soup):
            if isinstance(obj, dict) and isinstance(obj.get("datePublished"), str):
                raw_date = obj["datePublished"]
                break
    if not raw_date:
        time_node = soup.find("time")
        if time_node:
            raw_date = time_node.get("datetime") or time_node.get_text(" ", strip=True)

    raw_section = (
        meta(soup, "property", "article:section")
        or meta(soup, "name", "section")
    )
    section = clean(raw_section).title() if raw_section else section_from_url(url)

    image = (
        meta(soup, "property", "og:image")
        or meta(soup, "name", "twitter:image")
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
    body_text = clean(BeautifulSoup(body_html, "html.parser").get_text(" ", strip=True))
    if len(body_text) < 180:
        body_html = fallback_body(soup, url)

    if not title:
        return None

    body_text_final = clean(BeautifulSoup(body_html, "html.parser").get_text(" ", strip=True))
    story = {
        "title": title,
        "date": parse_date(raw_date),
        "section": section,
        "story_type": simplify_story_type(url, section),
        "topic": topic_from_story(url, section, title),
        "excerpt": excerpt,
        "url": canonical_source(url),
        "authors": extract_authors(soup),
        "image": image,
        "body_html": body_html,
        "word_count": len(body_text_final.split()),
        "verified_author": True,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }
    story["local_url"] = local_url(story)
    return story


def display_date(value: str) -> str:
    try:
        d = datetime.strptime(value, "%Y-%m-%d")
        return f"{d.day} {d.strftime('%B %Y')}"
    except Exception:
        return value or ""


def generate_story_page(story: dict) -> str:
    title = html_lib.escape(story.get("title", "Story"))
    excerpt = html_lib.escape(story.get("excerpt", ""))
    category = html_lib.escape(story.get("story_type", "Reporting"))
    topic = html_lib.escape(story.get("topic", "Public Affairs"))
    date = html_lib.escape(display_date(story.get("date", "")))
    source = html_lib.escape(story.get("url", ""), quote=True)
    authors = html_lib.escape(", ".join(story.get("authors") or [AUTHOR_NAME]))
    body = story.get("body_html", "").strip()
    sid = story_id(story.get("url", ""))

    if not body:
        body = (
            '<p>This article was verified as part of Arafat Rahaman’s archive, '
            'but the body could not be extracted cleanly during this refresh.</p>'
            f'<p><a href="{source}" target="_blank" rel="noopener">Read the original publication ↗</a></p>'
        )

    standfirst = f'<p class="story-standfirst">{excerpt}</p>' if excerpt else ""

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{source}"><meta name="description" content="{excerpt}"><title>{title} — Arafat Rahaman</title><link rel="stylesheet" href="../../styles.css"></head>
<body class="story-page" data-source-url="{source}" data-story-id="{sid}">
<header class="topbar"><div class="shell topbar-inner"><a class="wordmark" href="../../"><span class="monogram">AR</span><span>Arafat Rahaman</span></a><nav><a href="../../">Home</a><a href="../../archive.html">Archive</a><a href="../../about.html">About</a><a class="publisher-link" href="{source}" target="_blank" rel="noopener">Original ↗</a></nav></div></header>
<main class="story-v6 shell"><a class="story-back" href="../../archive.html">← Back to archive</a><section class="story-v6-head"><div class="story-v6-meta"><span>{category}</span><span>{topic}</span><time>{date}</time></div><h1>{title}</h1>{standfirst}<div class="story-byline-line"><span>By <strong>{authors}</strong></span><span id="story-reading-time"></span></div></section><section class="story-cover-v6"><div class="story-cover-copy"><span>{topic}</span><strong>AR</strong><small>{category}</small></div><div class="story-cover-rings"></div></section><div class="story-content-grid"><aside class="story-side"><p>Originally published by <em>The Daily Star</em>.</p><a href="{source}" target="_blank" rel="noopener">Original source ↗</a><div class="story-side-nav"><a href="../../archive.html">Archive</a><a href="../../about.html">About</a><a href="../../contact.html">Contact</a></div></aside><article class="story-body-card"><div class="story-body">{body}</div></article></div><section id="story-numbers" class="story-visual-section" hidden></section><section id="story-quote" class="story-quote-card" hidden></section><div id="curated-visuals"></div><section id="related-stories" class="related-section"></section></main>
<footer class="visual-footer"><div class="footer-art shell"><img src="../../assets/footer-editorial.svg" alt=""></div><div class="shell footer-links"><a href="../../">Home</a><a href="../../archive.html">Archive</a><a href="../../about.html">About</a><a href="{source}" target="_blank" rel="noopener">Original source ↗</a></div></footer><script src="../../common.js"></script><script src="../../story.js"></script><script src="../../visuals.js"></script></body></html>"""


def write_story_pages(stories: list[dict]) -> None:
    if STORIES_DIR.exists():
        shutil.rmtree(STORIES_DIR)
    STORIES_DIR.mkdir(parents=True, exist_ok=True)

    for story in stories:
        folder = SITE / story["local_url"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(
            generate_story_page(story),
            encoding="utf-8"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=60)
    parser.add_argument("--delay", type=float, default=0.35)
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update({
        "User-Agent": UA,
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
    })

    candidates = []
    candidate_set = set()
    empty_page_streak = 0

    for page in range(max(1, args.pages)):
        try:
            links = discover_candidates(session, page)
        except Exception as exc:
            print(f"Archive page {page}: {exc}", file=sys.stderr)
            empty_page_streak += 1
            if page >= 4 and empty_page_streak >= 4:
                break
            continue

        new_links = [u for u in links if u not in candidate_set]
        for url in new_links:
            candidate_set.add(url)
            candidates.append(url)

        print(
            f"Archive page {page}: {len(links)} candidates, "
            f"{len(new_links)} new, {len(candidates)} unique candidates",
            file=sys.stderr
        )

        if new_links:
            empty_page_streak = 0
        else:
            empty_page_streak += 1

        if page >= 4 and empty_page_streak >= 4:
            break

        time.sleep(max(0.0, args.delay))

    if not candidates:
        raise SystemExit("No candidate story URLs were discovered.")

    verified = []
    rejected = 0

    for i, url in enumerate(candidates, 1):
        try:
            story = extract_story(session, url)
            if story:
                verified.append(story)
                print(f"[{i}/{len(candidates)}] VERIFIED {story['title']}", file=sys.stderr)
            else:
                rejected += 1
                print(f"[{i}/{len(candidates)}] rejected non-author story: {url}", file=sys.stderr)
        except Exception as exc:
            print(f"[{i}/{len(candidates)}] failed {url}: {exc}", file=sys.stderr)

        if i < len(candidates):
            time.sleep(max(0.0, args.delay))

    unique = {}
    for story in verified:
        unique[story["url"]] = story

    stories = sorted(
        unique.values(),
        key=lambda a: (a.get("date", ""), a.get("title", "")),
        reverse=True
    )

    if not stories:
        raise SystemExit("No Arafat Rahaman stories passed author verification.")

    write_story_pages(stories)

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": AUTHOR_URL,
        "author": AUTHOR_NAME,
        "candidate_urls_checked": len(candidates),
        "non_author_urls_rejected": rejected,
        "articles": stories,
    }

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(
        f"Completed: {len(stories)} VERIFIED stories; "
        f"{rejected} non-author candidates rejected.",
        file=sys.stderr
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
