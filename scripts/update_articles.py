#!/usr/bin/env python3
"""
Refresh the public portfolio index from Arafat Rahaman's Daily Star author page.

The script deliberately stores only discovery metadata:
headline, short description, date, section, source URL and an optional OG image URL.
It does not republish full article bodies.

If the source blocks an automated request or changes markup, the script keeps the
existing JSON file instead of destroying the working archive.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

AUTHOR_URL = "https://www.thedailystar.net/author/arafat-rahaman"
OUTPUT = Path(__file__).resolve().parents[1] / "site" / "data" / "articles.json"
UA = "Mozilla/5.0 (compatible; ArafatPortfolioIndexer/1.0; public-author-page-indexer)"

ARTICLE_ID = re.compile(r"-\d{5,}/?$")
ARTICLE_HINTS = (
    "/news/", "/opinion/", "/business/", "/sports/", "/entertainment/",
    "/lifestyle/", "/youth/", "/supplements/", "/slow-reads/", "/star-multimedia/"
)

def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()

def get_meta(soup: BeautifulSoup, key: str, value: str) -> str:
    node = soup.find("meta", attrs={key: value})
    return clean(node.get("content", "")) if node else ""

def section_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    if "/education/" in path:
        return "Education"
    if "/sports/" in path:
        return "Sports"
    if "/business/" in path:
        return "Business"
    if "/opinion/" in path or "/views/" in path:
        return "Opinion"
    if "/entertainment/" in path or "/culture/" in path:
        return "Culture"
    if "/youth/" in path:
        return "Youth"
    if "/supplements/" in path:
        return "Supplement"
    return "News"

def parse_date(raw: str) -> str:
    raw = clean(raw)
    if not raw:
        return ""
    # ISO metadata is preferred.
    if re.match(r"^\d{4}-\d{2}-\d{2}", raw):
        return raw[:10]
    for fmt in ("%d %B %Y", "%d %b %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            pass
    return raw

def discover_links(session: requests.Session, limit: int) -> list[str]:
    r = session.get(AUTHOR_URL, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    found, seen = [], set()
    host = urlparse(AUTHOR_URL).netloc

    for a in soup.find_all("a", href=True):
        url = urljoin(AUTHOR_URL, a["href"]).split("#", 1)[0]
        parsed = urlparse(url)
        if parsed.netloc != host:
            continue
        if not any(h in parsed.path for h in ARTICLE_HINTS):
            continue
        if not ARTICLE_ID.search(parsed.path):
            continue
        if url in seen:
            continue
        seen.add(url)
        found.append(url)
        if limit and len(found) >= limit:
            break
    return found

def parse_story(session: requests.Session, url: str) -> dict:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title = (
        get_meta(soup, "property", "og:title")
        or get_meta(soup, "name", "twitter:title")
        or clean(soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else "")
    )

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
        t = soup.find("time")
        if t:
            raw_date = t.get("datetime") or t.get_text(" ", strip=True)

    section = (
        get_meta(soup, "property", "article:section")
        or get_meta(soup, "name", "section")
        or section_from_url(url)
    )

    image = (
        get_meta(soup, "property", "og:image")
        or get_meta(soup, "name", "twitter:image")
    )

    if not title:
        raise ValueError("No headline found")

    return {
        "title": title,
        "date": parse_date(raw_date),
        "section": clean(section).title() if section else section_from_url(url),
        "excerpt": excerpt,
        "url": url,
        "image": image,
        "featured": False,
    }

def load_existing() -> dict:
    if OUTPUT.exists():
        try:
            return json.loads(OUTPUT.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"updated_at": "", "articles": []}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--delay", type=float, default=0.7)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    existing = load_existing()
    session = requests.Session()
    session.headers.update({
        "User-Agent": UA,
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
    })

    try:
        links = discover_links(session, args.limit)
        if not links:
            raise RuntimeError("No story links discovered")

        old = {a.get("url"): a for a in existing.get("articles", []) if a.get("url")}
        refreshed = []

        for i, url in enumerate(links, 1):
            try:
                story = parse_story(session, url)
                refreshed.append(story)
                print(f"[{i}/{len(links)}] {story['title']}")
            except Exception as exc:
                print(f"[{i}/{len(links)}] keeping prior metadata for {url}: {exc}", file=sys.stderr)
                if url in old:
                    refreshed.append(old[url])
            if i < len(links):
                time.sleep(max(0.0, args.delay))

        # Keep older entries that are no longer visible on the first author-page batch.
        seen = {a.get("url") for a in refreshed}
        refreshed.extend(a for u, a in old.items() if u not in seen)

        # Dedupe and sort.
        unique = {}
        for item in refreshed:
            if item.get("url"):
                unique[item["url"]] = item
        articles = sorted(
            unique.values(),
            key=lambda a: a.get("date", ""),
            reverse=True
        )
        if articles:
            articles[0]["featured"] = True

        payload = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "source": AUTHOR_URL,
            "articles": articles,
        }
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {len(articles)} entries to {OUTPUT}")
        return 0

    except Exception as exc:
        print(f"Refresh failed: {exc}", file=sys.stderr)
        if args.strict:
            return 1
        if existing.get("articles"):
            print("Existing archive retained; continuing with current site.", file=sys.stderr)
            return 0
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
