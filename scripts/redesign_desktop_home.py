"""Replace only the desktop homepage with a restrained editorial portfolio."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dist' / 'index.html'
STUDIES = ROOT / 'content' / 'case-studies.json'
ARTICLES = ROOT / 'content' / 'articles'
POSTS = ROOT / 'content' / 'posts.json'


def selected_stories():
    article_map={}
    if ARTICLES.is_dir():
        for path in ARTICLES.glob('*.json'):
            try:item=json.loads(path.read_text(encoding='utf-8'))
            except (OSError,ValueError):continue
            local=str(item.get('local_url') or '').lstrip('/')
            if local:article_map[local]=item
    posts=[]
    if POSTS.is_file():
        try:posts=json.loads(POSTS.read_text(encoding='utf-8')).get('posts',[])
        except (OSError,ValueError):posts=[]
    post_map={str(item.get('local_url') or '').lstrip('/'):item for item in posts if item.get('status')=='published'}
    picks=[
        (article_map.get('stories/higher-viva-marks-may-undermine-fairness-in-public-recruitment/'),'Opinion & Analysis'),
        (article_map.get('stories/when-mobile-journalism-crosses-the-line-into-public-shaming/'),'Opinion & Analysis'),
        (article_map.get('stories/what-else-must-women-do/'),'Opinion & Analysis'),
        (article_map.get('stories/half-the-children-can-t-read-comprehend/'),'Reporting'),
        (post_map.get('thoughts/i-get-eid-off-do-my-colleagues-get-the-same-for-puja/'),'Thoughts'),
    ]
    links=[]
    for item,label in picks:
        if not item:continue
        path=str(item.get('local_url') or '').lstrip('/')
        if not re.fullmatch(r'(stories|thoughts)/[a-zA-Z0-9_-]+/',path):continue
        title=html.escape(str(item.get('title') or 'Selected work'))
        meta=html.escape(label)
        links.append(f'<a href="{path}"><span><small>{meta}</small>{title}</span><span aria-hidden="true">↗</span></a>')
    return ''.join(links)

def main():
    source = HOME.read_text(encoding='utf-8')
    desktop = '''<section class="deskhome editorial-home" aria-labelledby="editorial-title">
      <header class="editorial-header">
        <a class="editorial-brand" href="./" aria-label="Arafat Rahaman, home">Arafat Rahaman<span>Journalist · Bangladesh</span></a>
        <nav aria-label="Main navigation"><a href="./" aria-current="page">Home</a><a href="about/">About</a><a href="all-work/">All work</a><a href="photography/">Photography</a><a href="contact/">Contact</a></nav>
      </header>
      <div class="editorial-main">
        <div class="editorial-intro">
          <span class="editorial-eyebrow">Journalist · The Daily Star</span>
          <h1 id="editorial-title">Arafat<br><em>Rahaman.</em></h1>
          <p>Reporting on education, governance and the decisions that shape everyday life in Bangladesh.</p>
          <a class="editorial-text-link" href="about/">About the journalist <span aria-hidden="true">↗</span></a>
        </div>
        <a class="editorial-portrait" href="about/" aria-label="Read about Arafat Rahaman"><picture><source srcset="assets/portraits/byline.avif" type="image/avif"><img src="assets/portraits/byline.webp" alt="Portrait of Arafat Rahaman" width="1000" height="991" loading="eager" fetchpriority="high" decoding="async"></picture><span>Arafat Rahaman / Dhaka</span></a>
        <aside class="editorial-aside"><span class="editorial-aside-label">The work</span><p>People, policy<br><i>&amp; public life.</i></p><div class="editorial-aside-rule"></div><span>Field reporting, public records and analysis from across Bangladesh.</span><a href="reporting/">Explore reporting <span aria-hidden="true">↗</span></a></aside>
      </div>
      <section class="editorial-work" aria-label="Explore the portfolio"><a href="reporting/"><span>Reporting</span><small>Stories from the ground</small><b aria-hidden="true">↗</b></a><a href="opinion/"><span>Opinion &amp; Analysis</span><small>Arguments and context</small><b aria-hidden="true">↗</b></a><a href="thoughts/"><span>Thoughts</span><small>Notes and reflections</small><b aria-hidden="true">↗</b></a><a href="photography/"><span>Photography</span><small>People and places</small><b aria-hidden="true">↗</b></a></section>
      <section class="editorial-selected" aria-labelledby="editorial-selected-title"><div><span class="editorial-eyebrow">From the archive</span><h2 id="editorial-selected-title">Selected work</h2><a class="editorial-text-link" href="all-work/">View all work <span aria-hidden="true">↗</span></a></div><div class="editorial-story-links">STORY_LINKS</div></section>
      <footer class="editorial-footer"><span>© 2026 Arafat Rahaman</span><a href="mailto:arafat.mcj@yahoo.com">Get in touch ↗</a><span>Dhaka, Bangladesh</span></footer>
    </section>'''.replace('STORY_LINKS', selected_stories())
    pattern = re.compile(r'<section class="deskhome\b[^>]*>.*?</section>', re.S)
    source, count = pattern.subn(lambda _: desktop, source, count=1)
    if count != 1:
        raise RuntimeError('Desktop homepage section not found')
    source = re.sub(r'<style id="editorial-desktop-home">.*?</style>', '', source, flags=re.S)
    css = (ROOT / 'scripts' / 'redesign_desktop_home.css').read_text(encoding='utf-8')
    source = source.replace('</head>', '<style id="editorial-desktop-home">\n' + css + '\n</style></head>', 1)
    HOME.write_text(source, encoding='utf-8')
    print('Editorial desktop homepage applied; mobile homepage retained')


if __name__ == '__main__':
    main()
