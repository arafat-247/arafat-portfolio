"""Strengthen person/entity signals in generated portfolio pages.

Runs after the normal site build so the source builder stays focused on content
rendering while entity metadata remains explicit, testable and easy to audit.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
SETTINGS = ROOT / "content" / "settings.json"

SCHEMA_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    flags=re.DOTALL,
)


def load_settings():
    return json.loads(SETTINGS.read_text(encoding="utf-8"))


def unique(values):
    seen = set()
    result = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def enrich_person(person, config):
    base = config["site_url"].rstrip("/")
    profile_url = base + "/about/"
    social = config.get("social", {})
    career = config.get("career", [])
    education = config.get("education", [])
    recognition = config.get("recognition", [])
    membership = config.get("membership", {})

    current_role = career[0].get("role") if career else config.get("title", "Journalist")
    person.update({
        "@type": "Person",
        "@id": profile_url + "#person",
        "name": config.get("site_name", "Arafat Rahaman"),
        "givenName": "Arafat",
        "familyName": "Rahaman",
        "url": profile_url,
        "mainEntityOfPage": {"@id": profile_url},
        "description": config.get("description", ""),
        "jobTitle": current_role,
        "worksFor": {
            "@type": "Organization",
            "@id": "https://www.thedailystar.net/#organization",
            "name": config.get("organisation", "The Daily Star"),
            "url": "https://www.thedailystar.net/",
        },
        "homeLocation": {
            "@type": "Place",
            "name": config.get("location", "Dhaka, Bangladesh"),
        },
        "knowsAbout": config.get("areas", []),
        "sameAs": unique([
            social.get("daily_star"),
            social.get("muck_rack"),
            social.get("linkedin"),
            social.get("facebook"),
            social.get("instagram"),
            social.get("flickr"),
        ]),
    })

    portrait = config.get("portrait")
    if portrait:
        person["image"] = base + "/" + portrait.lstrip("/")

    if education:
        institution = education[0].get("institution", "University of Rajshahi")
        alumni = {"@type": "CollegeOrUniversity", "name": institution}
        if institution == "University of Rajshahi":
            alumni["url"] = "https://www.ru.ac.bd/"
        person["alumniOf"] = alumni

    if membership.get("name"):
        member = {"@type": "Organization", "name": membership["name"]}
        if membership["name"] == "Investigative Reporters & Editors":
            member["url"] = "https://www.ire.org/"
        person["memberOf"] = member

    awards = []
    for item in recognition:
        title = item.get("title", "").strip()
        organisation = item.get("organisation", "").strip()
        year = str(item.get("year", "")).strip()
        if not title:
            continue
        label = title
        if organisation:
            label += f" — {organisation}"
        if year:
            label += f" ({year})"
        awards.append(label)
    if awards:
        person["award"] = awards

    return person


def replace_jsonld(document, config, profile=False):
    matches = list(SCHEMA_RE.finditer(document))
    if not matches:
        return document

    target = matches[0]
    try:
        data = json.loads(target.group(1))
    except json.JSONDecodeError:
        return document

    profile_url = config["site_url"].rstrip("/") + "/about/"

    if data.get("@type") == "ProfilePage":
        person = enrich_person(data.get("mainEntity", {}), config)
        data.update({
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "@id": profile_url + "#profile",
            "url": profile_url,
            "name": "Arafat Rahaman — Journalist at The Daily Star",
            "description": config.get("description", ""),
            "mainEntity": person,
            "about": {"@id": person["@id"]},
            "inLanguage": "en-GB",
        })
    elif data.get("@type") == "Person":
        data = enrich_person(data, config)
    else:
        return document

    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    replacement = f'<script type="application/ld+json">{encoded}</script>'
    return document[:target.start()] + replacement + document[target.end():]


def enrich_about(document, config):
    name = config.get("site_name", "Arafat Rahaman")
    title = f"{name} — Journalist at The Daily Star"
    description = config.get("description", "")
    social = config.get("social", {})

    document = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", document, count=1)
    document = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">',
        document,
        count=1,
    )
    document = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title}">',
        document,
        count=1,
    )
    document = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{title}">',
        document,
        count=1,
    )

    identity_links = unique([
        social.get("daily_star"),
        social.get("muck_rack"),
        social.get("linkedin"),
    ])
    head_additions = [
        f'<meta name="author" content="{name}">',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
    ]
    head_additions.extend(f'<link rel="me" href="{url}">' for url in identity_links)
    marker = "</head>"
    if marker in document and 'meta name="author"' not in document:
        document = document.replace(marker, "".join(head_additions) + marker, 1)

    if "Professional profiles" not in document and identity_links:
        labels = [
            ("The Daily Star author profile", social.get("daily_star")),
            ("Muck Rack", social.get("muck_rack")),
            ("LinkedIn", social.get("linkedin")),
        ]
        links = " · ".join(
            f'<a href="{url}" rel="me noopener">{label}</a>'
            for label, url in labels if url
        )
        block = (
            '<aside class="membership" aria-label="Professional profiles">'
            '<span class="eyebrow">Professional profiles</span>'
            '<div><strong>Arafat Rahaman elsewhere</strong>'
            f'<p>{links}</p></div></aside>'
        )
        anchor = '<section class="coverage">'
        if anchor in document:
            document = document.replace(anchor, block + anchor, 1)

    return document


def add_website_schema(document, config):
    if '"@type":"WebSite"' in document:
        return document
    base = config["site_url"].rstrip("/")
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": base + "/#website",
        "url": base + "/",
        "name": config.get("site_name", "Arafat Rahaman"),
        "description": config.get("description", ""),
        "creator": {"@id": base + "/about/#person"},
        "inLanguage": "en-GB",
    }
    encoded = json.dumps(website, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    schema = f'<script type="application/ld+json">{encoded}</script>'
    return document.replace("</head>", schema + "</head>", 1)


def process(path, transform):
    if not path.exists():
        raise FileNotFoundError(path)
    original = path.read_text(encoding="utf-8")
    updated = transform(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")


def main():
    config = load_settings()
    home = OUT / "index.html"
    about = OUT / "about" / "index.html"

    process(home, lambda doc: add_website_schema(replace_jsonld(doc, config), config))
    process(about, lambda doc: enrich_about(replace_jsonld(doc, config, profile=True), config))
    print("Entity enrichment applied to homepage and /about/.")


if __name__ == "__main__":
    main()
