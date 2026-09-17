"""Post-process generated output for cleaner search-engine migration signals."""
from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE_HOST = "arafatrahaman.com"
SITE_BASE = f"https://{SITE_HOST}"
INSTANT_REFRESH = re.compile(r'<meta http-equiv="refresh" content="0;url=[^"]+">', re.I)
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)">', re.I)
OG_IMAGE = re.compile(r'<meta property="og:image" content="([^"]+)">', re.I)
JSON_LD = re.compile(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.I | re.S)
ARTICLE_MODIFIED = re.compile(r'<meta property="article:modified_time" content="([^"]+)">', re.I)
ARTICLE_PUBLISHED = re.compile(r'<meta property="article:published_time" content="([^"]+)">', re.I)
SITEMAP_URL = re.compile(r'<url><loc>([^<]+)</loc>(?:<lastmod>[^<]+</lastmod>)?</url>')
META_DESCRIPTION = re.compile(r'<meta name="description" content="([^"]*)">', re.I)
STANDFIRST = re.compile(r'<p class="standfirst">(.*?)</p>', re.I | re.S)
BODYCOPY = re.compile(r'<div class="bodycopy">(.*?)</div>', re.I | re.S)
TITLE_TAG = re.compile(r'<title>.*?</title>', re.I | re.S)
MAIN = re.compile(r'<main id="main">.*?</main>', re.I | re.S)

TOPICS = (
    {
        "slug": "education",
        "title": "Education reporting",
        "short": "Education",
        "description": "Selected reporting and analysis on schools, curricula, teachers, students and education policy in Bangladesh.",
        "terms": (
            "education", "school", "teacher", "student", "textbook", "curriculum", "ssc", "hsc",
            "university", "college", "madrasa", "ugc", "nctb", "admission", "academic", "primary",
            "secondary", "campus",
        ),
    },
    {
        "slug": "public-universities",
        "title": "Public university reporting",
        "short": "Public universities",
        "description": "Selected reporting on public universities, campus governance, admissions, appointments and student affairs in Bangladesh.",
        "terms": (
            "public university", "public universities", "university", "universities", "vice-chancellor",
            "vice chancellor", "ugc", "campus", "admission", "ducsu", "jucsu", "rucsu", "buet",
            "cuet", "kuet", "jagannath university", "rajshahi university", "dhaka university",
            "jahangirnagar university",
        ),
    },
    {
        "slug": "governance-accountability",
        "title": "Governance & accountability",
        "short": "Governance & accountability",
        "description": "Reporting and analysis on public institutions, administration, policing, recruitment, rights and accountability in Bangladesh.",
        "terms": (
            "government", "govt", "police", "commission", "ministry", "administration", "recruitment",
            "accountability", "corruption", "irregular", "probe", "investigation", "rights", "custody",
            "brutality", "harassment", "misuse", "reform", "public institution",
        ),
    },
    {
        "slug": "data-evidence",
        "title": "Data & evidence",
        "short": "Data & evidence",
        "description": "Selected reporting built around budgets, examination results, surveys, official reports and other quantitative evidence.",
        "terms": (
            "data", "survey", "statistics", "budget", "spending", "expenditure", "outlay", "pass rate",
            "gpa-5", "gpa 5", "percent", "percentage", "results", "official report", "report says",
        ),
    },
)

ARCHIVE_DESCRIPTIONS = {
    "/reporting/": "Reports, interviews and features by Arafat Rahaman on education, public institutions, rights, social policy and accountability in Bangladesh.",
    "/opinion/": "Opinion, analysis and commentary by Arafat Rahaman on education, governance, rights, public institutions and accountability in Bangladesh.",
    "/thoughts/": "Personal essays, reflections and field notes by Arafat Rahaman on journalism, public life, sport, culture and everyday experience in Bangladesh.",
    "/all-work/": "A complete chronological index of reporting, analysis, essays and other published work in Arafat Rahaman's journalism portfolio.",
    "/photography/": "Photography by Arafat Rahaman documenting people, public spaces and everyday life across Bangladesh.",
    "/contact/": "Contact Arafat Rahaman for reporting enquiries, story leads and professional correspondence in Bangladesh.",
}

SEO_CSS = """
/* SEO navigation enhancements */
.breadcrumbs{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;margin:0 0 20px;font-size:12px;color:var(--muted)}
.breadcrumbs a{color:inherit;text-decoration:none}.breadcrumbs a:hover{text-decoration:underline}
.topiclinks{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.topiclinks a{white-space:nowrap}
.topicpage .work-list{margin-top:28px}.topicpage .topicintro{max-width:760px}
.topicpage .topiccount{color:var(--muted);font-size:13px;margin-top:8px}
""".strip()


def is_site_url(url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == "https" and parts.hostname == SITE_HOST


def text_only(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html_lib.unescape(value).split())


def trim_text(value: str, limit: int = 155) -> str:
    value = " ".join(value.split()).strip()
    if len(value) <= limit:
        return value
    cut = value[: limit + 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "…"


def replace_meta_content(source: str, key: str, value: str, *, prop: bool = False) -> str:
    attr = "property" if prop else "name"
    pattern = re.compile(rf'<meta {attr}="{re.escape(key)}" content="[^"]*">', re.I)
    replacement = f'<meta {attr}="{key}" content="{html_lib.escape(value, quote=True)}">'
    return pattern.sub(replacement, source, count=1)


def optimise_permanent_redirects() -> int:
    """Make legacy GitHub Pages redirects immediate and visually silent."""
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
        source = page.read_text(encoding="utf-8")
        image_match = OG_IMAGE.search(source)
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

        updated = JSON_LD.sub(replace_schema, source)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
    return changed


def optimise_meta_descriptions() -> int:
    """Keep descriptions specific and within a practical search-snippet length."""
    changed = 0
    for page in DIST.rglob("index.html"):
        if "admin" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        canonical = CANONICAL.search(source)
        meta = META_DESCRIPTION.search(source)
        if not canonical or not meta or not is_site_url(canonical.group(1)):
            continue
        path = urlsplit(canonical.group(1)).path
        current = html_lib.unescape(meta.group(1))
        desired = ARCHIVE_DESCRIPTIONS.get(path)

        if desired is None and (path.startswith("/stories/") or path.startswith("/thoughts/")):
            if len(current) > 160:
                desired = trim_text(current)
            elif len(current) < 80:
                standfirst = STANDFIRST.search(source)
                body = BODYCOPY.search(source)
                parts = [text_only(standfirst.group(1))] if standfirst else [current]
                if body:
                    body_text = text_only(body.group(1))
                    if body_text and body_text not in parts[0]:
                        parts.append(body_text)
                desired = trim_text(" ".join(p for p in parts if p))
        elif desired is None and len(current) > 160:
            desired = trim_text(current)

        if not desired or desired == current:
            continue
        updated = replace_meta_content(source, "description", desired)
        updated = replace_meta_content(updated, "og:description", desired, prop=True)
        updated = replace_meta_content(updated, "twitter:description", desired)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def rewrite_nonarticle_schemas() -> int:
    """Use page-level schema on archives instead of repeating a Person entity as the page type."""
    page_types = {
        "/reporting/": "CollectionPage",
        "/opinion/": "CollectionPage",
        "/thoughts/": "CollectionPage",
        "/all-work/": "CollectionPage",
        "/photography/": "CollectionPage",
        "/contact/": "ContactPage",
    }
    changed = 0
    for page in DIST.rglob("index.html"):
        source = page.read_text(encoding="utf-8")
        canonical = CANONICAL.search(source)
        if not canonical or not is_site_url(canonical.group(1)):
            continue
        path = urlsplit(canonical.group(1)).path
        page_type = page_types.get(path)
        if not page_type:
            continue
        title_match = TITLE_TAG.search(source)
        meta_match = META_DESCRIPTION.search(source)
        name = text_only(title_match.group(0).replace("<title>", "").replace("</title>", "")) if title_match else "Arafat Rahaman"
        description = html_lib.unescape(meta_match.group(1)) if meta_match else ""
        replacement_data = {
            "@context": "https://schema.org",
            "@type": page_type,
            "@id": canonical.group(1) + "#webpage",
            "url": canonical.group(1),
            "name": name,
            "description": description,
            "isPartOf": {"@type": "WebSite", "@id": SITE_BASE + "/#website", "url": SITE_BASE + "/", "name": "Arafat Rahaman"},
            "about": {"@id": SITE_BASE + "/about/#person"},
        }

        replaced = False

        def replace_schema(match: re.Match[str]) -> str:
            nonlocal replaced
            try:
                data = json.loads(match.group(2))
            except json.JSONDecodeError:
                return match.group(0)
            if replaced or data.get("@type") != "Person":
                return match.group(0)
            replaced = True
            payload = json.dumps(replacement_data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
            return match.group(1) + payload + match.group(3)

        updated = JSON_LD.sub(replace_schema, source)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def load_index_records() -> list[dict]:
    index_path = DIST / "data" / "index.json"
    if not index_path.is_file():
        raise FileNotFoundError("dist/data/index.json was not generated")
    return [r for r in json.loads(index_path.read_text(encoding="utf-8")).get("articles", []) if r.get("local_url") and r.get("title")]


def add_breadcrumbs() -> int:
    """Add visible and structured breadcrumbs to every clean article page."""
    records = load_index_records()
    streams = {
        "reporting": ("Reports & Features", "/reporting/"),
        "opinion": ("Opinion & Analysis", "/opinion/"),
        "thoughts": ("Thoughts", "/thoughts/"),
    }
    changed = 0
    for record in records:
        page = DIST / record["local_url"] / "index.html"
        if not page.is_file():
            continue
        source = page.read_text(encoding="utf-8")
        if 'data-seo-breadcrumb="1"' in source:
            continue
        label, section_url = streams.get(record.get("stream") or "reporting", streams["reporting"])
        title = record["title"]
        current_url = SITE_BASE + "/" + record["local_url"]
        visible = (
            '<nav class="breadcrumbs" data-seo-breadcrumb="1" aria-label="Breadcrumb">'
            '<a href="/">Home</a><span aria-hidden="true">›</span>'
            f'<a href="{section_url}">{html_lib.escape(label)}</a><span aria-hidden="true">›</span>'
            f'<span aria-current="page">{html_lib.escape(title)}</span></nav>'
        )
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": label, "item": SITE_BASE + section_url},
                {"@type": "ListItem", "position": 3, "name": title, "item": current_url},
            ],
        }
        script = '<script type="application/ld+json" data-seo-breadcrumb="1">' + json.dumps(
            breadcrumb_data, ensure_ascii=False, separators=(",", ":")
        ).replace("<", "\\u003c") + "</script>"
        updated = source.replace('<article class="page reading">', '<article class="page reading">' + visible, 1)
        updated = updated.replace("</head>", script + "</head>", 1)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def topic_matches(record: dict, topic: dict) -> bool:
    haystack = " ".join(
        str(record.get(key, "")) for key in ("title", "excerpt", "category")
    ).casefold()
    return any(term.casefold() in haystack for term in topic["terms"])


def set_topic_metadata(source: str, topic: dict, canonical: str) -> str:
    title = topic["title"] + " — Arafat Rahaman"
    description = topic["description"]
    source = TITLE_TAG.sub(f"<title>{html_lib.escape(title)}</title>", source, count=1)
    source = META_DESCRIPTION.sub(
        f'<meta name="description" content="{html_lib.escape(description, quote=True)}">', source, count=1
    )
    source = CANONICAL.sub(f'<link rel="canonical" href="{canonical}">', source, count=1)
    source = replace_meta_content(source, "og:title", topic["title"], prop=True)
    source = replace_meta_content(source, "og:description", description, prop=True)
    source = replace_meta_content(source, "og:url", canonical, prop=True)
    source = replace_meta_content(source, "twitter:title", topic["title"])
    source = replace_meta_content(source, "twitter:description", description)
    return source


def build_topic_hubs() -> tuple[int, list[str]]:
    """Generate server-rendered topic hubs from existing article metadata."""
    template = DIST / "all-work" / "index.html"
    if not template.is_file():
        raise FileNotFoundError("dist/all-work/index.html was not generated")
    template_source = template.read_text(encoding="utf-8")
    records = load_index_records()
    built = 0
    urls: list[str] = []

    for topic in TOPICS:
        matches = [record for record in records if topic_matches(record, topic)]
        matches = matches[:80]
        cards = []
        for record in matches:
            date = html_lib.escape(str(record.get("date_published", ""))[:10])
            category = html_lib.escape(record.get("category") or "Published work")
            title = html_lib.escape(record["title"])
            excerpt = html_lib.escape(record.get("excerpt") or "")
            href = "/" + html_lib.escape(record["local_url"], quote=True)
            cards.append(
                '<article class="workitem"><div class="workmeta">'
                f'<span>{date}</span><span>{category}</span></div>'
                f'<div class="workcopy"><h2><a href="{href}">{title}</a></h2><p>{excerpt}</p></div>'
                f'<a class="read" href="{href}" aria-label="Read {title}"><span>Read</span> →</a></article>'
            )
        listing = "".join(cards) or '<p class="empty">No matching entries are available yet.</p>'
        body = (
            '<section class="page topicpage"><header class="pageintro topicintro"><div>'
            '<span class="eyebrow">Reporting topic</span>'
            f'<h1>{html_lib.escape(topic["title"])}</h1><p>{html_lib.escape(topic["description"])}</p>'
            f'<p class="topiccount">{len(matches)} selected pieces</p></div></header>'
            f'<div class="work-list">{listing}</div>'
            '<p><a class="textlink" href="/all-work/">Browse the complete portfolio index →</a></p></section>'
        )
        canonical = SITE_BASE + "/" + topic["slug"] + "/"
        page_source = set_topic_metadata(template_source, topic, canonical)
        page_source = MAIN.sub(f'<main id="main">{body}</main>', page_source, count=1)
        page_source = JSON_LD.sub("", page_source)
        collection = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": topic["title"],
            "description": topic["description"],
            "isPartOf": {"@type": "WebSite", "@id": SITE_BASE + "/#website", "url": SITE_BASE + "/", "name": "Arafat Rahaman"},
            "about": {"@id": SITE_BASE + "/about/#person"},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(matches),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index + 1,
                        "url": SITE_BASE + "/" + record["local_url"],
                        "name": record["title"],
                    }
                    for index, record in enumerate(matches[:25])
                ],
            },
        }
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": topic["short"], "item": canonical},
            ],
        }
        schemas = (
            '<script type="application/ld+json">'
            + json.dumps(collection, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
            + "</script>"
            + '<script type="application/ld+json" data-seo-breadcrumb="1">'
            + json.dumps(breadcrumb, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
            + "</script>"
        )
        page_source = page_source.replace("</head>", schemas + "</head>", 1)
        target = DIST / topic["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_source, encoding="utf-8")
        built += 1
        urls.append(canonical)

    return built, urls


def add_internal_discovery_links() -> tuple[int, int, int]:
    """Give every clean page a crawl hub, topic routes and every article crawlable neighbours."""
    records = load_index_records()
    groups: dict[str, list[dict]] = {}
    for record in records:
        groups.setdefault(record.get("stream") or "reporting", []).append(record)

    related_added = 0
    for group in groups.values():
        for pos, record in enumerate(group):
            page = DIST / record["local_url"] / "index.html"
            if not page.is_file():
                continue
            source = page.read_text(encoding="utf-8")
            if 'data-seo-related="1"' in source or "</article>" not in source:
                continue
            candidates: list[dict] = []
            for offset in (-1, 1, -2, 2):
                idx = pos + offset
                if 0 <= idx < len(group):
                    candidate = group[idx]
                    if candidate.get("local_url") != record.get("local_url") and candidate not in candidates:
                        candidates.append(candidate)
                if len(candidates) == 3:
                    break
            if len(candidates) < 3:
                for candidate in group:
                    if candidate.get("local_url") != record.get("local_url") and candidate not in candidates:
                        candidates.append(candidate)
                    if len(candidates) == 3:
                        break
            links = " · ".join(
                f'<a href="/{html_lib.escape(c["local_url"], quote=True)}">{html_lib.escape(c["title"])}</a>'
                for c in candidates
            )
            related = (
                '<aside class="sourcebox" data-seo-related="1" aria-label="More from the portfolio">'
                '<strong>More from this portfolio</strong><br>' + links
                + ' · <a href="/all-work/">Complete index</a></aside>'
            )
            page.write_text(source.replace("</article>", related + "</article>", 1), encoding="utf-8")
            related_added += 1

    hub_added = 0
    marker = '<a class="top" href="#top">Back to top ↑</a>'
    replacement = '<a class="archiveindex" href="/all-work/">Complete index</a>' + marker
    for page in DIST.rglob("index.html"):
        source = page.read_text(encoding="utf-8")
        if 'class="archiveindex"' in source or marker not in source:
            continue
        page.write_text(source.replace(marker, replacement, 1), encoding="utf-8")
        hub_added += 1

    topic_links_added = 0
    topic_nav = '<nav class="topiclinks" data-seo-topics="1" aria-label="Reporting topics">' + "".join(
        f'<a href="/{topic["slug"]}/">{html_lib.escape(topic["short"])}</a>' for topic in TOPICS
    ) + "</nav>"
    for page in DIST.rglob("index.html"):
        if "admin" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        if 'data-seo-topics="1"' in source or "</footer>" not in source:
            continue
        page.write_text(source.replace("</footer>", topic_nav + "</footer>", 1), encoding="utf-8")
        topic_links_added += 1

    css = DIST / "portfolio.css"
    if css.is_file():
        source = css.read_text(encoding="utf-8")
        if "/* SEO navigation enhancements */" not in source:
            css.write_text(source + "\n" + SEO_CSS + "\n", encoding="utf-8")

    return related_added, hub_added, topic_links_added


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
    source = page.read_text(encoding="utf-8")
    match = ARTICLE_MODIFIED.search(source) or ARTICLE_PUBLISHED.search(source)
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


def add_topic_urls_to_sitemap(urls: list[str]) -> int:
    sitemap = DIST / "sitemap.xml"
    xml = sitemap.read_text(encoding="utf-8")
    added = 0
    entries = []
    for url in urls:
        if f"<loc>{url}</loc>" in xml:
            continue
        entries.append(f"<url><loc>{url}</loc></url>")
        added += 1
    if entries:
        xml = xml.replace("</urlset>", "".join(entries) + "</urlset>", 1)
        sitemap.write_text(xml, encoding="utf-8")
    return added


def main() -> None:
    if not DIST.is_dir():
        raise FileNotFoundError("dist/ does not exist; run scripts/build.py first")
    redirects = optimise_permanent_redirects()
    schemas = add_article_images_to_schema()
    meta = optimise_meta_descriptions()
    page_schemas = rewrite_nonarticle_schemas()
    breadcrumbs = add_breadcrumbs()
    topics, topic_urls = build_topic_hubs()
    related, hubs, topic_links = add_internal_discovery_links()
    sitemap = add_sitemap_lastmods()
    topic_sitemap = add_topic_urls_to_sitemap(topic_urls)
    print(
        f"SEO post-process: redirects={redirects}, article_images={schemas}, meta={meta}, "
        f"page_schemas={page_schemas}, breadcrumbs={breadcrumbs}, topics={topics}, "
        f"related_links={related}, crawl_hubs={hubs}, topic_links={topic_links}, "
        f"article_lastmod={sitemap}, topic_sitemap={topic_sitemap}"
    )


if __name__ == "__main__":
    main()
