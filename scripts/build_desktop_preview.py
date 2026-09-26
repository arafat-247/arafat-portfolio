"""Build the isolated desktop concept; the published homepage is never modified."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
HOME = DIST / 'index.html'
PREVIEW = DIST / 'desktop-preview' / 'index.html'
STUDIES = ROOT / 'content' / 'case-studies.json'


def selected_stories():
    if not STUDIES.exists():
        return ''
    items = json.loads(STUDIES.read_text(encoding='utf-8')).get('case_studies', [])[:3]
    rows = []
    for item in items:
        path = str(item.get('source_path') or '')
        if not re.fullmatch(r'stories/[a-zA-Z0-9_-]+/', path):
            continue
        title = html.escape(str(item.get('source_title') or item.get('title') or 'Reporting'))
        date = str(item.get('date_published') or '')
        try:
            date = datetime.fromisoformat(date).strftime('%d %b %Y').lstrip('0')
        except ValueError:
            date = ''
        rows.append(f'<a class="preview-story" href="{path}"><span class="preview-story-meta">Reporting · {html.escape(date)}</span><strong>{title}</strong><span class="preview-story-arrow" aria-hidden="true">↗</span></a>')
    return ''.join(rows)


PREVIEW_DESKTOP = '''<section class="deskhome cinematic-home" aria-labelledby="preview-title">
  <div class="cinematic-hero">
    <div class="cinematic-photo" aria-hidden="true"><picture><source srcset="assets/portraits/byline.avif" type="image/avif"><img src="assets/portraits/byline.webp" alt="" width="1000" height="991" loading="eager" fetchpriority="high" decoding="async"></picture></div>
    <header class="cinematic-header"><a class="cinematic-brand" href="desktop-preview/">Arafat Rahaman<span>Journalist · Bangladesh</span></a><nav aria-label="Desktop preview navigation"><a href="about/">About</a><a href="#preview-work">Work</a><a href="all-work/">Archive</a><a href="contact/">Contact</a></nav></header>
    <div class="cinematic-identity"><span class="cinematic-eyebrow">The Daily Star · Dhaka</span><h1 id="preview-title">Arafat<br><em>Rahaman</em></h1><p>Stories from a changing Bangladesh.</p></div>
    <div class="cinematic-index" id="preview-work"><div class="cinematic-index-intro"><span class="cinematic-eyebrow">Journalism / Photography</span><p>I report on education, governance and public life, following decisions from the official record to the people they affect.</p></div><nav aria-label="Explore work"><a href="reporting/"><span>Reporting</span><b aria-hidden="true">↗</b></a><a href="opinion/"><span>Opinion &amp; Analysis</span><b aria-hidden="true">↗</b></a><a href="thoughts/"><span>Thoughts</span><b aria-hidden="true">↗</b></a><a href="photography/"><span>Photography</span><b aria-hidden="true">↗</b></a></nav><a class="cinematic-index-bottom" href="#preview-selected">Selected stories <span aria-hidden="true">↓</span></a></div>
  </div>
  <section class="preview-selected" id="preview-selected" aria-labelledby="preview-selected-title"><div class="preview-selected-heading"><span class="preview-eyebrow">The reporting</span><h2 id="preview-selected-title">Selected<br><em>stories.</em></h2><p>Education, public institutions and the choices that shape lives.</p><a href="reporting/">All reporting <span aria-hidden="true">↗</span></a></div><div class="preview-stories">STORY_LINKS</div></section>
  <a class="preview-photography" href="photography/"><img src="assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (6).webp" alt="Arafat Rahaman's photograph at dusk" loading="lazy" decoding="async"><span class="preview-photo-shade"></span><span class="preview-photo-copy"><small>Through the lens</small><strong>Photography</strong><span>View the gallery ↗</span></span></a>
  <footer class="preview-footer"><span>Arafat Rahaman · Journalist</span><a href="mailto:arafat.mcj@yahoo.com">Get in touch ↗</a><span>Dhaka, Bangladesh</span></footer>
</section>'''


def main():
    source = HOME.read_text(encoding='utf-8')
    desktop = PREVIEW_DESKTOP.replace('STORY_LINKS', selected_stories())
    pattern = re.compile(r'<section class="deskhome\b[^>]*>.*?</section>', re.S)
    source, count = pattern.subn(lambda _: desktop, source, count=1)
    if count != 1:
        raise RuntimeError('Desktop homepage section not found; preview not built')
    css = (ROOT / 'scripts' / 'desktop_preview.css').read_text(encoding='utf-8')
    js = (ROOT / 'scripts' / 'desktop_preview.js').read_text(encoding='utf-8')
    source = source.replace('<head>', '<head><base href="/"><meta name="robots" content="noindex,nofollow">', 1)
    source = source.replace('</head>', f'<style id="cinematic-desktop-preview">\n{css}\n</style></head>', 1)
    source = source.replace('</body>', f'<script id="cinematic-preview-interaction">\n{js}\n</script></body>', 1)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW.write_text(source, encoding='utf-8')
    print('Isolated desktop preview built; live homepage unchanged')


if __name__ == '__main__':
    main()
