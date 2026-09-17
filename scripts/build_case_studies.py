"""Build distinct portfolio case-study pages from verified flagship reporting metadata."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CONTENT = ROOT / "content"
SITE = "https://arafatrahaman.com"
TITLE_RE = re.compile(r"<title>.*?</title>", re.I | re.S)
META_RE = re.compile(r'<meta name="description" content="[^"]*">', re.I)
CANON_RE = re.compile(r'<link rel="canonical" href="[^"]+">', re.I)
OG_TITLE_RE = re.compile(r'<meta property="og:title" content="[^"]*">', re.I)
OG_DESC_RE = re.compile(r'<meta property="og:description" content="[^"]*">', re.I)
OG_URL_RE = re.compile(r'<meta property="og:url" content="[^"]*">', re.I)
OG_IMAGE_RE = re.compile(r'<meta property="og:image" content="([^"]+)">', re.I)
TW_TITLE_RE = re.compile(r'<meta name="twitter:title" content="[^"]*">', re.I)
TW_DESC_RE = re.compile(r'<meta name="twitter:description" content="[^"]*">', re.I)
MAIN_RE = re.compile(r'<main id="main">.*?</main>', re.I | re.S)
NESTED_LINK_RE = re.compile(r'(?P<attr>\b(?:href|src)=["\'])\.\./', re.I)

CSS = """
/* Flagship reporting case studies */
.casehero{max-width:860px}.casehero h1{max-width:820px}.casegrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,.42fr);gap:34px;margin-top:30px}.casepanel{padding:22px;border:1px solid var(--line);background:var(--surface)}.casepanel h2,.caseblock h2{margin-top:0}.caseblock{margin-top:34px;max-width:820px}.caseevidence{padding-left:20px}.caseevidence li{margin:0 0 12px}.caseoriginal{margin-top:34px;padding:20px;border-left:3px solid var(--accent);background:var(--surface)}.casecards{display:grid;gap:18px;margin-top:28px}.casecard{padding:22px;border:1px solid var(--line);background:var(--surface)}.casecard h2{margin:.35rem 0}.casecard p{max-width:760px}.casekicker{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
@media(max-width:760px){.casegrid{grid-template-columns:1fr}}
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

    css = DIST / "portfolio.css"
    if css.is_file():
        source = css.read_text(encoding="utf-8")
        if "/* Flagship reporting case studies */" not in source:
            css.write_text(source + "\n" + CSS + "\n", encoding="utf-8")

    sitemap = DIST / "sitemap.xml"
    xml = sitemap.read_text(encoding="utf-8")
    additions = "".join(f"<url><loc>{esc(url)}</loc></url>" for url in urls if f"<loc>{url}</loc>" not in xml)
    if additions:
        sitemap.write_text(xml.replace("</urlset>", additions + "</urlset>", 1), encoding="utf-8")

    print(f"Case studies: built={len(studies)}, index=1")


if __name__ == "__main__":
    main()
