"""Build distinct portfolio case-study pages from verified flagship reporting metadata."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CONTENT = ROOT / "content"
SITE = "https://arafatrahaman.com"
TITLE_RE = re.compile(r"<title>.*?</title>", re.I | re.S)
META_RE = re.compile(r'<meta name="description" content="[^"]*">', re.I)
META_DESC_RE = re.compile(r'<meta name="description" content="([^"]*)">', re.I)
CANON_RE = re.compile(r'<link rel="canonical" href="[^"]+">', re.I)
OG_TITLE_RE = re.compile(r'<meta property="og:title" content="[^"]*">', re.I)
OG_DESC_RE = re.compile(r'<meta property="og:description" content="[^"]*">', re.I)
OG_URL_RE = re.compile(r'<meta property="og:url" content="[^"]*">', re.I)
OG_IMAGE_RE = re.compile(r'<meta property="og:image" content="([^"]+)">', re.I)
TW_TITLE_RE = re.compile(r'<meta name="twitter:title" content="[^"]*">', re.I)
TW_DESC_RE = re.compile(r'<meta name="twitter:description" content="[^"]*">', re.I)
MAIN_RE = re.compile(r'<main id="main">.*?</main>', re.I | re.S)
NESTED_LINK_RE = re.compile(r'(?P<attr>\b(?:href|src)=["\'])\.\./', re.I)
SOURCEBOX_RE = re.compile(
    r'<div class="sourcebox">Originally published by (?P<source>.*?)\. '
    r'<a href="(?P<url>[^"]+)" rel="noopener noreferrer">Read the original publication</a>\.'
    r'<br>First archived: (?P<archived>.*?)\. This local copy does not depend on the source remaining online\.</div>',
    re.I | re.S,
)
RELATEDBOX_RE = re.compile(
    r'<aside class="sourcebox" data-seo-related="1" aria-label="More from the portfolio">(?P<body>.*?)</aside>',
    re.I | re.S,
)
RELATED_LINK_RE = re.compile(r'<a href="(?P<href>[^"]+)">(?P<title>.*?)</a>', re.I | re.S)
SECTION_RE = re.compile(r'<body[^>]*data-section="([^"]+)"', re.I)
STORYLABEL_RE = re.compile(r'<div class="storylabel">\s*<a[^>]*>(.*?)</a>\s*</div>', re.I | re.S)

CSS = """
/* Flagship reporting case studies */
.casehero{max-width:860px}.casehero h1{max-width:820px}.casegrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,.42fr);gap:34px;margin-top:30px}.casepanel{padding:22px;border:1px solid var(--line);background:var(--surface)}.casepanel h2,.caseblock h2{margin-top:0}.caseblock{margin-top:34px;max-width:820px}.caseevidence{padding-left:20px}.caseevidence li{margin:0 0 12px}.caseoriginal{margin-top:34px;padding:20px;border-left:3px solid var(--accent);background:var(--surface)}.casecards{display:grid;gap:18px;margin-top:28px}.casecard{padding:22px;border:1px solid var(--line);background:var(--surface)}.casecard h2{margin:.35rem 0}.casecard p{max-width:760px}.casekicker{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
@media(max-width:760px){.casegrid{grid-template-columns:1fr}}
""".strip()

ARTICLE_END_CSS = """
/* Compact responsive article endings */
.publication-strip{display:grid;grid-template-columns:minmax(155px,.78fr) minmax(0,1.35fr) auto;gap:14px;align-items:center;max-width:720px;margin-top:30px;padding:12px 14px;border:1px solid var(--line);border-radius:8px;background:#e8e5dc}
.publication-strip__brand,.publication-strip__meta{min-width:0}
.publication-strip__eyebrow{display:block;margin-bottom:4px;color:var(--muted);font-size:9px;font-weight:850;letter-spacing:.12em;text-transform:uppercase}
.publication-strip__logo{display:block;font:700 24px/1 var(--serif);letter-spacing:-.02em}
.publication-strip__meta{display:grid;gap:2px;padding-left:14px;border-left:1px solid var(--line)}
.publication-strip__meta strong{font:700 14px/1.25 var(--serif)}
.publication-strip__meta span{color:var(--muted);font-size:11px;line-height:1.35}
.publication-strip__action{display:inline-flex;align-items:center;justify-content:center;padding:9px 11px;border-radius:6px;color:#fff;background:var(--forest);font-size:11px;font-weight:800;line-height:1.2;text-decoration:none;white-space:nowrap}
.publication-strip__action:hover{background:var(--forest-2)}
.portfolio-related{max-width:900px;margin-top:34px;padding-top:4px}
.portfolio-related__head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:12px}
.portfolio-related__head h2{margin:0;font:700 clamp(26px,3vw,34px)/1.05 var(--serif);letter-spacing:-.025em}
.portfolio-related__kicker{display:block;margin-bottom:4px;color:var(--accent);font-size:9px;font-weight:850;letter-spacing:.12em;text-transform:uppercase}
.portfolio-related__all{flex:0 0 auto;color:var(--forest);font-size:11px;font-weight:800;text-decoration:none}
.portfolio-related__all:hover{text-decoration:underline}
.portfolio-related__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.portfolio-related-card{overflow:hidden;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.portfolio-related-card__image{display:block;overflow:hidden;aspect-ratio:16/9;background:linear-gradient(135deg,#d8d3c8,#bfc9c3)}
.portfolio-related-card__image img{width:100%;height:100%;object-fit:cover;transition:transform .25s ease}
.portfolio-related-card:hover .portfolio-related-card__image img{transform:scale(1.025)}
.portfolio-related-card__placeholder{display:block;width:100%;height:100%;background:linear-gradient(135deg,color-mix(in srgb,var(--forest) 82%,#fff),color-mix(in srgb,var(--accent) 55%,var(--paper)))}
.portfolio-related-card__body{padding:10px 11px 11px}
.portfolio-related-card__tag{display:block;margin-bottom:4px;color:var(--accent);font-size:8px;font-weight:850;letter-spacing:.1em;text-transform:uppercase}
.portfolio-related-card h3{margin:0;font:700 16px/1.16 var(--serif);letter-spacing:-.01em}
.portfolio-related-card h3 a{text-decoration:none}
.portfolio-related-card h3 a:hover{text-decoration:underline}
.portfolio-related-card p{display:-webkit-box;overflow:hidden;margin:7px 0 8px;color:var(--muted);font-size:11px;line-height:1.45;-webkit-line-clamp:3;-webkit-box-orient:vertical}
.portfolio-related-card__more{color:var(--forest);font-size:10px;font-weight:800;text-decoration:none}
html[data-theme="dark"] .publication-strip{background:#1a2320}
html[data-theme="dark"] .publication-strip__action{background:#235a51}
html[data-theme="dark"] .portfolio-related__all,html[data-theme="dark"] .portfolio-related-card__more{color:#9bc4b8}
@media(max-width:800px){
  .publication-strip{grid-template-columns:minmax(0,1fr) auto;gap:8px 10px;margin-top:24px;padding:10px 11px}
  .publication-strip__logo{font-size:20px}
  .publication-strip__meta{grid-column:1/-1;grid-row:2;padding:6px 0 0;border-left:0;border-top:1px solid var(--line)}
  .publication-strip__meta strong{display:none}
  .publication-strip__meta span{font-size:10px}
  .publication-strip__action{padding:8px 9px;font-size:10px}
  .portfolio-related{margin-top:27px}
  .portfolio-related__head{align-items:center;margin-bottom:10px}
  .portfolio-related__head h2{font-size:25px}
  .portfolio-related__kicker{display:none}
  .portfolio-related__all{font-size:10px}
  .portfolio-related__grid{grid-template-columns:1fr;gap:7px}
  .portfolio-related-card{display:grid;grid-template-columns:92px minmax(0,1fr);gap:9px;padding:7px}
  .portfolio-related-card__image{aspect-ratio:1/1;border-radius:5px}
  .portfolio-related-card__body{align-self:center;padding:0}
  .portfolio-related-card__tag{font-size:7px}
  .portfolio-related-card h3{font-size:14px;line-height:1.16}
  .portfolio-related-card p,.portfolio-related-card__more{display:none}
}
@media(max-width:420px){
  .publication-strip__meta{display:none}
  .publication-strip{grid-template-columns:minmax(0,1fr) auto}
  .publication-strip__logo{font-size:18px}
  .publication-strip__action{max-width:116px;white-space:normal;text-align:center}
  .portfolio-related-card{grid-template-columns:82px minmax(0,1fr)}
}
@media print{.portfolio-related{display:none}.publication-strip{border:1px solid #aaa;background:#fff}}
""".strip()


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def load() -> list[dict]:
    path = CONTENT / "case-studies.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("case_studies", [])


def apply_meta(source: str, *, title: str, description: str, canonical: str) -> str:
    source = TITLE_RE.sub(f"<title>{esc(title)} — Arafat Rahaman</title>", source, count=1)
    source = META_RE.sub(f'<meta name="description" content="{esc(description)}">', source, count=1)
    source = CANON_RE.sub(f'<link rel="canonical" href="{esc(canonical)}">', source, count=1)
    source = OG_TITLE_RE.sub(f'<meta property="og:title" content="{esc(title)}">', source, count=1)
    source = OG_DESC_RE.sub(f'<meta property="og:description" content="{esc(description)}">', source, count=1)
    source = OG_URL_RE.sub(f'<meta property="og:url" content="{esc(canonical)}">', source, count=1)
    source = TW_TITLE_RE.sub(f'<meta name="twitter:title" content="{esc(title)}">', source, count=1)
    source = TW_DESC_RE.sub(f'<meta name="twitter:description" content="{esc(description)}">', source, count=1)
    return source


def deepen_template_links(source: str) -> str:
    """Rebase one-level-up template links for /case-studies/<slug>/ pages."""
    return NESTED_LINK_RE.sub(lambda match: match.group("attr") + "../../", source)


def source_article_image(study: dict, fallback_page: str) -> str | None:
    """Reuse the archived source article's social image for case-study Article schema."""
    source_path = str(study.get("source_path", "")).strip("/")
    if source_path:
        article = DIST / source_path / "index.html"
        if article.is_file():
            match = OG_IMAGE_RE.search(article.read_text(encoding="utf-8"))
            if match:
                return html.unescape(match.group(1))
    fallback = OG_IMAGE_RE.search(fallback_page)
    return html.unescape(fallback.group(1)) if fallback else None


def schema_block(study: dict, canonical: str, image_url: str | None = None) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": canonical + "#article",
        "headline": study["title"],
        "description": study["description"],
        "datePublished": study.get("date_published", ""),
        "author": {"@type": "Person", "@id": SITE + "/about/#person", "name": "Arafat Rahaman", "url": SITE + "/about/"},
        "mainEntityOfPage": canonical,
        "isBasedOn": study.get("source_url", ""),
        "about": study.get("topics", []),
    }
    if image_url:
        data["image"] = image_url
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Reporting case studies", "item": SITE + "/case-studies/"},
            {"@type": "ListItem", "position": 3, "name": study["title"], "item": canonical},
        ],
    }
    return (
        '<script type="application/ld+json" data-case-study="1">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        + "</script>"
        + '<script type="application/ld+json" data-case-study-breadcrumb="1">'
        + json.dumps(crumbs, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        + "</script>"
    )


def study_body(study: dict) -> str:
    topics = " · ".join(esc(t) for t in study.get("topics", []))
    evidence = "".join(f"<li>{esc(item)}</li>" for item in study.get("evidence", []))
    return f'''<section class="page casepage"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><a href="/case-studies/">Reporting case studies</a><span aria-hidden="true">›</span><span aria-current="page">{esc(study['title'])}</span></nav><header class="pageintro casehero"><div><span class="eyebrow">Flagship reporting case study</span><h1>{esc(study['title'])}</h1><p>{esc(study['description'])}</p></div></header><div class="casegrid"><div><section class="caseblock"><span class="casekicker">Reporting question</span><h2>What the reporting set out to establish</h2><p>{esc(study['question'])}</p></section><section class="caseblock"><span class="casekicker">Approach</span><h2>How the story was reported</h2><p>{esc(study['reporting_note'])}</p></section><section class="caseblock"><span class="casekicker">Evidence</span><h2>Key evidence used</h2><ul class="caseevidence">{evidence}</ul></section><section class="caseblock"><span class="casekicker">Why it matters</span><h2>What this adds</h2><p>{esc(study['why_it_matters'])}</p></section></div><aside class="casepanel"><span class="casekicker">Original publication</span><h2>{esc(study['source_title'])}</h2><p>Published by The Daily Star on {esc(study.get('date_published',''))}.</p><p><a class="textlink" href="{esc(study['source_url'])}" rel="noopener noreferrer">Read the original Daily Star story ↗</a></p><p><a class="textlink" href="/{esc(study['source_path'])}">Read the archived portfolio copy →</a></p><p>{topics}</p></aside></div><div class="caseoriginal"><strong>About this page</strong><p>This is a portfolio case study, not a replacement publication of the original article. It adds reporting context and evidence notes while preserving a direct link to The Daily Star version.</p></div></section>'''


def index_body(studies: list[dict]) -> str:
    cards = "".join(
        f'''<article class="casecard"><span class="casekicker">{esc(s.get('date_published',''))}</span><h2><a href="/case-studies/{esc(s['slug'])}/">{esc(s['title'])}</a></h2><p>{esc(s['description'])}</p><a class="textlink" href="/case-studies/{esc(s['slug'])}/">View reporting case study →</a></article>'''
        for s in studies
    )
    return f'''<section class="page"><header class="pageintro casehero"><div><span class="eyebrow">Selected work</span><h1>Reporting case studies</h1><p>Selected investigations and data-led reports, with notes on the reporting question, evidence and method behind the published story.</p></div></header><div class="casecards">{cards}</div></section>'''


def insert_nav_link(source: str) -> str:
    if 'href="/case-studies/"' in source or "</footer>" not in source:
        return source
    link = '<a href="/case-studies/">Case studies</a>'
    return source.replace("</footer>", link + "</footer>", 1)


def compact_text(value: str, limit: int = 125) -> str:
    value = " ".join(html.unescape(value).split())
    if len(value) <= limit:
        return value
    cut = value[: limit + 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "…"


def local_page_for_href(href: str) -> Path | None:
    path = urlsplit(href).path
    if not path.startswith("/") or ".." in path.split("/"):
        return None
    if not path.endswith("/"):
        return None
    return DIST / path.lstrip("/") / "index.html"


def related_card(href: str, title: str) -> str:
    target = local_page_for_href(href)
    image_url = ""
    description = ""
    category = "Published work"
    if target and target.is_file():
        target_source = target.read_text(encoding="utf-8")
        image_match = OG_IMAGE_RE.search(target_source)
        if image_match:
            image_url = html.unescape(image_match.group(1))
        desc_match = META_DESC_RE.search(target_source)
        if desc_match:
            description = compact_text(desc_match.group(1))
        category_match = STORYLABEL_RE.search(target_source)
        if category_match:
            category = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", category_match.group(1))).split()) or category
    visual = (
        f'<img src="{esc(image_url)}" alt="" loading="lazy" decoding="async">'
        if image_url
        else '<span class="portfolio-related-card__placeholder" aria-hidden="true"></span>'
    )
    return (
        '<article class="portfolio-related-card">'
        f'<a class="portfolio-related-card__image" href="{esc(href)}" aria-label="Read {esc(title)}">{visual}</a>'
        '<div class="portfolio-related-card__body">'
        f'<span class="portfolio-related-card__tag">{esc(category)}</span>'
        f'<h3><a href="{esc(href)}">{esc(title)}</a></h3>'
        + (f'<p>{esc(description)}</p>' if description else "")
        + f'<a class="portfolio-related-card__more" href="{esc(href)}">Read more →</a>'
        + '</div></article>'
    )


def render_publication_strip(match: re.Match[str]) -> str:
    source_name = match.group("source").strip()
    source_url = match.group("url").strip()
    archived = match.group("archived").strip()
    return (
        '<section class="publication-strip" data-article-source="1" aria-label="Original publication">'
        '<div class="publication-strip__brand">'
        '<span class="publication-strip__eyebrow">Originally published by</span>'
        f'<strong class="publication-strip__logo">{source_name}</strong></div>'
        '<div class="publication-strip__meta">'
        f'<strong>This article was originally published in {source_name}</strong>'
        f'<span>First archived: {archived}</span></div>'
        f'<a class="publication-strip__action" href="{esc(source_url)}" rel="noopener noreferrer">Read original article ↗</a>'
        '</section>'
    )


def render_related_section(page_source: str, match: re.Match[str]) -> str:
    section_key_match = SECTION_RE.search(page_source)
    section_key = section_key_match.group(1) if section_key_match else "reporting"
    sections = {
        "reporting": ("Reports & Features", "/reporting/"),
        "opinion": ("Opinion & Analysis", "/opinion/"),
        "thoughts": ("Thoughts", "/thoughts/"),
    }
    label, section_url = sections.get(section_key, sections["reporting"])
    links = []
    for link in RELATED_LINK_RE.finditer(match.group("body")):
        href = html.unescape(link.group("href")).strip()
        title = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", link.group("title"))).split())
        if href == "/all-work/" or not title or not href.startswith("/"):
            continue
        links.append((href, title))
        if len(links) == 3:
            break
    if not links:
        return match.group(0)
    cards = "".join(related_card(href, title) for href, title in links)
    return (
        '<section class="portfolio-related" data-seo-related="1" aria-label="More from this section">'
        '<div class="portfolio-related__head"><div>'
        '<span class="portfolio-related__kicker">More from this section</span>'
        f'<h2>From {esc(label)}</h2></div>'
        f'<a class="portfolio-related__all" href="{esc(section_url)}">Browse all {esc(label.lower())} →</a>'
        '</div>'
        f'<div class="portfolio-related__grid">{cards}</div>'
        '</section>'
    )


def redesign_article_endings() -> tuple[int, int]:
    """Turn the two plain source boxes into compact responsive editorial components."""
    source_changed = 0
    related_changed = 0
    pages = list((DIST / "stories").glob("*/index.html")) + list((DIST / "thoughts").glob("*/index.html"))
    for page in pages:
        source = page.read_text(encoding="utf-8")
        updated, source_count = SOURCEBOX_RE.subn(render_publication_strip, source, count=1)
        if source_count:
            source_changed += 1
        current = updated
        related_match = RELATEDBOX_RE.search(current)
        if related_match:
            replacement = render_related_section(current, related_match)
            if replacement != related_match.group(0):
                current = current[: related_match.start()] + replacement + current[related_match.end() :]
                related_changed += 1
        if current != source:
            page.write_text(current, encoding="utf-8")
    return source_changed, related_changed


def main() -> None:
    studies = load()
    if not studies:
        print("Case studies: none configured")
        return
    template_path = DIST / "all-work" / "index.html"
    if not template_path.is_file():
        raise FileNotFoundError("dist/all-work/index.html was not generated")
    template = template_path.read_text(encoding="utf-8")

    index_canonical = SITE + "/case-studies/"
    index = apply_meta(
        template,
        title="Reporting case studies",
        description="Flagship reporting by Arafat Rahaman with notes on evidence, methodology and the reporting questions behind selected Daily Star stories.",
        canonical=index_canonical,
    )
    index = MAIN_RE.sub(f'<main id="main">{index_body(studies)}</main>', index, count=1)
    index_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": index_canonical + "#webpage",
        "url": index_canonical,
        "name": "Reporting case studies",
        "about": {"@id": SITE + "/about/#person"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(studies),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": SITE + "/case-studies/" + s["slug"] + "/", "name": s["title"]}
                for i, s in enumerate(studies)
            ],
        },
    }
    index = index.replace("</head>", '<script type="application/ld+json" data-case-index="1">' + json.dumps(index_schema, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + "</script></head>", 1)
    target = DIST / "case-studies" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(index, encoding="utf-8")

    nested_template = deepen_template_links(template)
    urls = [index_canonical]
    for study in studies:
        canonical = SITE + "/case-studies/" + study["slug"] + "/"
        page = apply_meta(nested_template, title=study["title"], description=study["description"], canonical=canonical)
        page = MAIN_RE.sub(f'<main id="main">{study_body(study)}</main>', page, count=1)
        image_url = source_article_image(study, page)
        page = page.replace("</head>", schema_block(study, canonical, image_url) + "</head>", 1)
        out = DIST / "case-studies" / study["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        urls.append(canonical)

    for page in DIST.rglob("index.html"):
        if "admin" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        updated = insert_nav_link(source)
        if updated != source:
            page.write_text(updated, encoding="utf-8")

    article_sources, article_related = redesign_article_endings()

    css = DIST / "portfolio.css"
    if css.is_file():
        source = css.read_text(encoding="utf-8")
        additions = []
        if "/* Flagship reporting case studies */" not in source:
            additions.append(CSS)
        if "/* Compact responsive article endings */" not in source:
            additions.append(ARTICLE_END_CSS)
        if additions:
            css.write_text(source + "\n" + "\n".join(additions) + "\n", encoding="utf-8")

    sitemap = DIST / "sitemap.xml"
    xml = sitemap.read_text(encoding="utf-8")
    additions = "".join(f"<url><loc>{esc(url)}</loc></url>" for url in urls if f"<loc>{url}</loc>" not in xml)
    if additions:
        sitemap.write_text(xml.replace("</urlset>", additions + "</urlset>", 1), encoding="utf-8")

    print(
        f"Case studies: built={len(studies)}, index=1, "
        f"article_sources={article_sources}, related_sections={article_related}"
    )


if __name__ == "__main__":
    main()
