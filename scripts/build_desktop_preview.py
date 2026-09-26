"""Build a coded desk composition at /desktop-preview/ only."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dist' / 'index.html'
PREVIEW = ROOT / 'dist' / 'desktop-preview' / 'index.html'

DESK = '''<section class="deskhome desk-rebuild" aria-labelledby="desk-title">
  <div class="deskstage desk-scene" id="desk-top">
    <img class="desk-photography" src="assets/home/approved-desk-desktop.webp" alt="" width="1447" height="1087" fetchpriority="high" decoding="async">
    <header class="desk-masthead">
      <a class="desk-brand" href="desktop-preview/" aria-current="page"><strong id="desk-title">Arafat Rahaman</strong><span>Journalist · Bangladesh</span></a>
      <nav class="desk-nav" aria-label="Main navigation"><a href="desktop-preview/" aria-current="page">Home</a><a href="about/">About</a><a href="desktop-preview/#desk-work">Work</a><a href="thoughts/">Writing</a><a href="contact/">Contact</a></nav>
      <button class="desk-menu-button" type="button" aria-expanded="false" aria-controls="desk-mobile-nav" aria-label="Open navigation"><span></span><span></span><span></span></button>
    </header>
    <nav class="desk-mobile-nav" id="desk-mobile-nav" aria-label="Mobile navigation" hidden><a href="desktop-preview/">Home</a><a href="about/">About</a><a href="desktop-preview/#desk-work">Work</a><a href="thoughts/">Writing</a><a href="contact/">Contact</a></nav>
    <p class="desk-scribble">Stories<br>People<br>Places</p>
    <a class="desk-portrait" href="about/" aria-label="Read about Arafat Rahaman"><span class="desk-portrait-image" aria-hidden="true"></span><span class="desk-portrait-caption"><strong>Arafat Rahaman</strong><span>Journalist covering education, governance, accountability and social issues.</span></span></a>
    <p class="desk-intro">Reporting from the ground, unpacking what it means, and keeping a notebook for what lingers. Four ways I tell stories.</p>
    <div class="desk-work" id="desk-work">
      <a class="desk-object desk-reporting" href="reporting/" aria-label="Explore reporting"><span class="desk-sheet desk-sheet-back" aria-hidden="true"></span><span class="desk-sheet desk-sheet-middle" aria-hidden="true"></span><span class="desk-report-top"><small>The Daily Star</small><strong>On a changing<br>Bangladesh</strong><span class="desk-report-image" aria-hidden="true"></span><span>From the floodplains to the city, large questions often begin with ordinary people.</span></span><span class="desk-tab"><span class="desk-number">1</span><span class="desk-tab-copy"><strong>Reporting</strong><small>People, places and the big picture from the ground.</small></span><span class="desk-arrow" aria-hidden="true">↗</span></span></a>
      <a class="desk-object desk-opinion" href="opinion/" aria-label="Explore opinion and analysis"><span class="desk-sheet desk-sheet-back" aria-hidden="true"></span><span class="desk-sheet desk-sheet-middle" aria-hidden="true"></span><span class="desk-opinion-page"><strong>Progress is not only what we build,<br>but who we make room for.</strong><span class="desk-opinion-lines" aria-hidden="true"></span><em>Development<br>for whom?</em></span><span class="desk-tab"><span class="desk-number">2</span><span class="desk-tab-copy"><strong>Opinion &amp; Analysis</strong><small>Sharper takes on the issues shaping Bangladesh.</small></span><span class="desk-arrow" aria-hidden="true">↗</span></span></a>
      <a class="desk-object desk-thoughts" href="thoughts/" aria-label="Explore thoughts"><span class="desk-notebook"><span>Ideas from<br>the in-between.</span><span class="desk-notebook-list">— Notes<br>— Observations<br>— Unfinished questions<br>— A more humane tomorrow?</span></span><span class="desk-tab"><span class="desk-number">3</span><span class="desk-tab-copy"><strong>Thoughts</strong><small>Notes, reflections and work in progress.</small></span><span class="desk-arrow" aria-hidden="true">↗</span></span></a>
      <a class="desk-object desk-photo" href="photography/" aria-label="Explore photography"><span class="desk-photo-print" aria-hidden="true"></span><span class="desk-tab"><span class="desk-number">4</span><span class="desk-tab-copy"><strong>Photography</strong><small>A visual diary of people, places and daily life.</small></span><span class="desk-arrow" aria-hidden="true">↗</span></span></a>
    </div>
    <div class="desk-signoff"><a href="contact/">Have a story? Get in touch ↗</a><time id="desk-dhaka-time" aria-label="Current time in Dhaka"><span class="desk-clock" aria-hidden="true"><i class="desk-hour-hand"></i><i class="desk-minute-hand"></i></span><span class="desk-clock-label"></span></time></div>
  </div>
</section>'''


def main():
    source = HOME.read_text(encoding='utf-8')
    source, count = re.subn(r'<section class="deskhome\b[^>]*>.*?</section>', lambda _: DESK, source, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError('Desk homepage section not found')
    css = (ROOT / 'scripts' / 'desktop_preview.css').read_text(encoding='utf-8')
    js = (ROOT / 'scripts' / 'desktop_preview.js').read_text(encoding='utf-8')
    source = source.replace('<head>', '<head><base href="/"><meta name="robots" content="noindex,nofollow">', 1)
    source = source.replace('href="#main"', 'href="desktop-preview/#main"', 1)
    source = source.replace('</head>', f'<style id="coded-desk-preview">\n{css}\n</style></head>', 1)
    source = source.replace('</body>', f'<script id="coded-desk-interaction">\n{js}\n</script></body>', 1)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW.write_text(source, encoding='utf-8')
    print('Coded desk preview built without modifying the live homepage')


if __name__ == '__main__':
    main()
