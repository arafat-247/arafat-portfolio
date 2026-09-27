"""Build desktop-only inner-page prototypes without touching live inner pages."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CSS = (ROOT / "scripts" / "inner_preview.css").read_text(encoding="utf-8")

SWITCHER = """<div class="prototype-switcher" aria-label="Prototype views"><strong>Desktop inner-page prototype</strong><a href="/inner-preview/reporting/">Reporting index</a><a href="/inner-preview/story/">Story page</a><a href="/inner-preview/about/">About page</a></div>"""

def masthead(view: str) -> str:
    work_current = ' aria-current="page"' if view in {"reporting", "story"} else ""
    about_current = ' aria-current="page"' if view == "about" else ""
    return f"""<header class="prototype-head"><div class="prototype-head-inner"><a class="prototype-brand" href="/"><strong>Arafat Rahaman</strong><small>Journalist</small></a><nav aria-label="Prototype main navigation"><a href="/">Home</a><a href="/inner-preview/about/"{about_current}>About</a><a href="/inner-preview/reporting/"{work_current}>Work</a><a href="/thoughts/">Writing</a><a href="/contact/">Contact</a></nav><div class="prototype-location">Dhaka, Bangladesh<br>Desktop prototype</div></div></header><div class="prototype-context"><span>Warm desk palette · paper-led editorial pages</span></div>"""

def decorate(source: str, view: str, title: str) -> str:
    source = re.sub(r"<title>.*?</title>", f"<title>Prototype — {title} — Arafat Rahaman</title>", source, count=1, flags=re.I | re.S)
    source = source.replace("<head>", '<head><base href="/"><meta name="robots" content="noindex,nofollow">', 1)
    source = source.replace("</head>", f'<style id="inner-desktop-prototype">\n{CSS}\n</style><script>try{{document.documentElement.dataset.theme="light"}}catch(e){{}}</script></head>', 1)
    source = re.sub(r'<body class="inner"', f'<body class="inner inner-prototype" data-prototype-view="{view}"', source, count=1)
    marker = '<aside class="identity"'
    if marker not in source:
        raise RuntimeError("Expected inner-page shell not found")
    source = source.replace(marker, SWITCHER + masthead(view) + marker, 1)
    active = f'href="/inner-preview/{view}/"'
    source = source.replace(active, active + ' aria-current="page"', 1)
    return source

def first_story_path(reporting_source: str) -> Path:
    match = re.search(r'href="\.\./((?:stories|thoughts)/[A-Za-z0-9_-]+/)"', reporting_source)
    if not match:
        raise RuntimeError("No story route found in the reporting archive")
    return DIST / match.group(1) / "index.html"

def write_preview(relative: str, source: str) -> None:
    target = DIST / "inner-preview" / relative / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")

def main() -> None:
    reporting_path = DIST / "reporting" / "index.html"
    about_path = DIST / "about" / "index.html"
    if not reporting_path.is_file() or not about_path.is_file():
        raise RuntimeError("Build the live site before building the inner-page prototype")

    reporting_source = reporting_path.read_text(encoding="utf-8")
    story_path = first_story_path(reporting_source)
    story_source = story_path.read_text(encoding="utf-8")
    about_source = about_path.read_text(encoding="utf-8")

    write_preview("reporting", decorate(reporting_source, "reporting", "Reports & Features"))
    write_preview("story", decorate(story_source, "story", "Story page"))
    write_preview("about", decorate(about_source, "about", "About"))

    landing = DIST / "inner-preview" / "index.html"
    landing.parent.mkdir(parents=True, exist_ok=True)
    landing.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow">'
        '<meta http-equiv="refresh" content="0;url=/inner-preview/reporting/"><title>Desktop inner-page prototype</title></head>'
        '<body><p><a href="/inner-preview/reporting/">Open the desktop inner-page prototype</a></p></body></html>',
        encoding="utf-8",
    )
    print("Desktop inner-page prototypes built at /inner-preview/ without modifying live inner pages")

if __name__ == "__main__":
    main()
