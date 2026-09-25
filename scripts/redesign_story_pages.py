"""Apply the final editorial redesign to generated story pages.

The redesign keeps article text and credits untouched while rebuilding the visual
hierarchy around them: a homepage-inspired split hero, pill labels, one date,
no estimated reading-time row, compact source/actions, and a responsive reading
column. Local authorised covers are promoted into the hero; sourced stories use
an abstract editorial panel rather than unrelated photography.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
STYLE_ID = 'inside-story-redesign-v1'

STYLE_RE = re.compile(rf'<style id="{STYLE_ID}">.*?</style>', re.I | re.S)
FACTS_RE = re.compile(r'<div class="storyfacts">(?P<body>.*?)</div>', re.I | re.S)
SPAN_RE = re.compile(r'<span>(.*?)</span>', re.I | re.S)
HEADER_RE = re.compile(
    r'<header class="storyhead">(?P<header>.*?)</header>'
    r'<div class="storymain">(?P<cover><figure class="cover">.*?</figure>)?',
    re.I | re.S,
)

CSS = r'''
/* Homepage-inspired editorial story system */
.reading{
  width:min(100% - 48px,1120px)!important;
  max-width:1120px!important;
  padding-top:30px!important;
}
.storyhead.storyhero{
  position:relative!important;
  display:grid!important;
  grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr)!important;
  gap:0!important;
  max-width:none!important;
  margin:0!important;
  padding:0!important;
  overflow:hidden!important;
  border:1px solid color-mix(in srgb,var(--line) 88%,transparent)!important;
  border-radius:8px!important;
  background:#f3eadc!important;
  box-shadow:0 18px 48px rgb(21 38 33 / 7%)!important;
}
.storyhero-copy{
  position:relative!important;
  z-index:2!important;
  display:flex!important;
  min-width:0!important;
  flex-direction:column!important;
  justify-content:center!important;
  padding:34px 40px 30px!important;
  background:
    linear-gradient(112deg,#f7f1e7 0 82%,rgb(247 241 231 / 70%) 100%)!important;
}
.storyhero-copy:before{
  content:""!important;
  position:absolute!important;
  top:0!important;
  left:0!important;
  width:96px!important;
  height:5px!important;
  background:var(--story-accent)!important;
}
.storyhero .back{
  align-self:flex-start!important;
  margin:0 0 19px!important;
  padding:0!important;
  color:#6f6559!important;
  font-size:10px!important;
  font-weight:800!important;
  letter-spacing:.04em!important;
  text-transform:uppercase!important;
}
.storykicker{
  display:flex!important;
  flex-wrap:wrap!important;
  align-items:center!important;
  gap:7px!important;
  margin:0 0 13px!important;
  font-size:9px!important;
  font-weight:850!important;
  letter-spacing:.1em!important;
  text-transform:uppercase!important;
}
.storykicker-sep{display:none!important}
.storytype,.storycategory{
  display:inline-flex!important;
  min-height:29px!important;
  box-sizing:border-box!important;
  align-items:center!important;
  justify-content:center!important;
  padding:6px 11px 5px!important;
  border:1px solid var(--story-accent)!important;
  border-radius:999px!important;
  line-height:1!important;
  text-decoration:none!important;
}
.storytype{color:#fff!important;background:var(--story-accent)!important}
.storycategory{
  color:var(--story-accent)!important;
  background:color-mix(in srgb,var(--story-accent) 7%,#f7f1e7)!important;
}
.storycategory:hover{color:#fff!important;background:var(--story-accent)!important}
.storyhero h1{
  max-width:760px!important;
  margin:0!important;
  color:#171512!important;
  font:700 clamp(42px,4.8vw,64px)/.96 var(--serif)!important;
  letter-spacing:-.044em!important;
  text-wrap:balance!important;
  overflow-wrap:normal!important;
}
.storyhero .standfirst{
  max-width:700px!important;
  margin:18px 0 0!important;
  color:#59544b!important;
  font:400 18px/1.48 var(--serif)!important;
}
.storyfooter{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) auto auto!important;
  align-items:center!important;
  gap:12px 15px!important;
  margin-top:26px!important;
  padding-top:17px!important;
  border-top:1px solid rgb(77 65 51 / 17%)!important;
}
.storyfooter .byline{margin:0!important;color:#171512!important}
.storyfooter .byline img{
  width:48px!important;
  height:54px!important;
  flex:0 0 48px!important;
  border:0!important;
  border-radius:4px!important;
  box-shadow:0 0 0 1px rgb(58 43 28 / 12%)!important;
}
.storyfooter .byline strong{font-size:12px!important;line-height:1.25!important}
.storyfooter .byline .meta{margin-top:4px!important;color:#776d61!important;font-size:10px!important}
.storypublication{
  display:flex!important;
  flex-direction:column!important;
  align-items:flex-end!important;
  gap:3px!important;
  white-space:nowrap!important;
}
.storypublication span{
  color:#8b7e6e!important;
  font-size:7px!important;
  font-weight:850!important;
  letter-spacing:.12em!important;
  text-transform:uppercase!important;
}
.storypublication strong{color:#342f29!important;font-size:10px!important;font-weight:850!important}
.storyactions{display:flex!important;gap:7px!important;margin:0!important}
.storyactions button{
  min-height:36px!important;
  padding:8px 12px!important;
  border:1px solid rgb(58 43 28 / 18%)!important;
  border-radius:999px!important;
  color:#2d2a25!important;
  background:rgb(255 255 255 / 42%)!important;
  font-size:9px!important;
  font-weight:800!important;
  cursor:pointer!important;
}
.storyactions button:hover{
  border-color:var(--story-accent)!important;
  color:var(--story-accent)!important;
  background:#fff!important;
}
.storyhero-visual{
  position:relative!important;
  min-height:100%!important;
  overflow:hidden!important;
  background:
    linear-gradient(145deg,color-mix(in srgb,var(--story-accent) 86%,#173f38),#123f37)!important;
}
.storyhero-art{
  display:flex!important;
  min-height:100%!important;
  align-items:flex-end!important;
  padding:28px!important;
  color:#fff!important;
}
.storyhero-art:before{
  content:""!important;
  position:absolute!important;
  inset:0!important;
  background:
    radial-gradient(circle at 74% 22%,rgb(255 218 169 / 23%),transparent 25%),
    linear-gradient(125deg,transparent 0 54%,rgb(255 255 255 / 8%) 54% 55%,transparent 55% 68%,rgb(255 255 255 / 7%) 68% 69%,transparent 69%),
    linear-gradient(180deg,transparent 0 72%,rgb(0 0 0 / 17%) 100%)!important;
}
.storyhero-art:after{
  content:""!important;
  position:absolute!important;
  width:170px!important;
  height:170px!important;
  right:-46px!important;
  bottom:-50px!important;
  border:1px solid rgb(255 255 255 / 28%)!important;
  border-radius:50%!important;
  box-shadow:0 0 0 34px rgb(255 255 255 / 5%),0 0 0 68px rgb(255 255 255 / 4%)!important;
}
.storyhero-art-copy{
  position:relative!important;
  z-index:2!important;
  display:grid!important;
  gap:8px!important;
  max-width:240px!important;
}
.storyhero-art-copy span{
  font-size:8px!important;
  font-weight:900!important;
  letter-spacing:.17em!important;
  text-transform:uppercase!important;
}
.storyhero-art-copy strong{
  font:400 29px/1.02 var(--serif)!important;
  letter-spacing:-.03em!important;
}
.storyhero-photo{min-height:410px!important;background:#192a27!important}
.storyhero-photo .cover{height:100%!important;margin:0!important;background:transparent!important}
.storyhero-photo .cover img{
  width:100%!important;
  height:100%!important;
  min-height:410px!important;
  object-fit:cover!important;
}
.storyhero-photo .cover figcaption{
  position:absolute!important;
  z-index:3!important;
  right:14px!important;
  bottom:12px!important;
  left:14px!important;
  margin:0!important;
  padding:8px 10px!important;
  color:rgb(255 255 255 / 84%)!important;
  background:rgb(7 19 16 / 62%)!important;
  font-size:8px!important;
  line-height:1.35!important;
  backdrop-filter:blur(6px)!important;
}
.storymain{
  max-width:760px!important;
  margin:42px auto 0!important;
}
.bodycopy{
  max-width:none!important;
  color:#20211e!important;
  font:400 19px/1.76 var(--reading-serif)!important;
}
.bodycopy>p:first-child strong{
  font-weight:600!important;
}
.sourcebox{
  margin-top:44px!important;
  padding:17px 0!important;
  border-top:1px solid var(--line)!important;
  border-bottom:1px solid var(--line)!important;
  background:transparent!important;
}
html[data-theme="dark"] .storyhead.storyhero{background:#17201d!important;border-color:#34403c!important}
html[data-theme="dark"] .storyhero-copy{background:#151d1b!important}
html[data-theme="dark"] .storyhero h1{color:#eff2ec!important}
html[data-theme="dark"] .storyhero .standfirst{color:#bdc5bf!important}
html[data-theme="dark"] .storyhero .back{color:#abb4ae!important}
html[data-theme="dark"] .storyfooter{border-color:#34403c!important}
html[data-theme="dark"] .storyfooter .byline{color:#eff2ec!important}
html[data-theme="dark"] .storyfooter .byline .meta,html[data-theme="dark"] .storypublication span{color:#aeb6b0!important}
html[data-theme="dark"] .storypublication strong{color:#eff2ec!important}
html[data-theme="dark"] .storyactions button{color:#eff2ec!important;border-color:#44504c!important;background:#19221f!important}
html[data-theme="dark"] .bodycopy{color:#edf0eb!important}

@media(max-width:920px){
  .storyhead.storyhero{grid-template-columns:minmax(0,1.2fr) minmax(250px,.8fr)!important}
  .storyhero-copy{padding:30px 30px 27px!important}
  .storyhero h1{font-size:clamp(38px,5.7vw,55px)!important}
  .storyfooter{grid-template-columns:1fr auto!important}
  .storyfooter .byline{grid-column:1 / -1!important}
  .storypublication{align-items:flex-start!important}
}
@media(max-width:800px){
  .reading{width:min(100% - 28px,720px)!important;padding-top:18px!important}
  .storyhead.storyhero{
    grid-template-columns:1fr!important;
    border-radius:6px!important;
  }
  .storyhero-copy{padding:25px 19px 20px!important}
  .storyhero-copy:before{width:68px!important;height:4px!important}
  .storyhero .back{margin-bottom:14px!important;font-size:9px!important}
  .storykicker{margin-bottom:10px!important;gap:6px!important}
  .storytype,.storycategory{min-height:27px!important;padding:6px 9px 5px!important;font-size:8px!important}
  .storyhero h1{font-size:clamp(32px,9.2vw,45px)!important;line-height:.99!important}
  .storyhero .standfirst{margin-top:14px!important;font-size:15.5px!important;line-height:1.46!important}
  .storyfooter{
    grid-template-columns:minmax(0,1fr) auto!important;
    gap:11px!important;
    margin-top:20px!important;
    padding-top:14px!important;
  }
  .storyfooter .byline{grid-column:1 / -1!important}
  .storypublication{align-items:flex-start!important}
  .storyactions{justify-self:end!important}
  .storyactions button{min-height:34px!important;padding:7px 10px!important;font-size:8.5px!important}
  .storyhero-visual{min-height:190px!important}
  .storyhero-art{min-height:190px!important;padding:20px!important}
  .storyhero-art-copy{max-width:190px!important}
  .storyhero-art-copy strong{font-size:23px!important}
  .storyhero-photo{min-height:220px!important}
  .storyhero-photo .cover img{min-height:220px!important;max-height:330px!important}
  .storymain{margin-top:30px!important}
  .bodycopy{font-size:17.5px!important;line-height:1.72!important}
}
@media(max-width:470px){
  .storyfooter{grid-template-columns:1fr!important}
  .storyfooter .byline,.storypublication,.storyactions{grid-column:1!important;justify-self:start!important}
  .storyhero-visual{min-height:170px!important}
  .storyhero-art{min-height:170px!important}
}
'''.strip()


def plain(value: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', value)).strip()


def publication_from_facts(body: str) -> str:
    values = [plain(value) for value in SPAN_RE.findall(body)]
    values = [value for value in values if value]
    for value in reversed(values):
        if re.fullmatch(r'\d+\s+min\s+read', value, re.I):
            continue
        if re.fullmatch(r'\d{1,2}\s+[A-Za-z]+\s+\d{4}', value):
            continue
        return value
    return ''


def art_label(source: str) -> str:
    match = re.search(r'<span class="storytype">(.*?)</span>', source, re.I | re.S)
    return plain(match.group(1)) if match else 'Journalism'


def art_title(source: str) -> str:
    match = re.search(r'<a class="storycategory"[^>]*>(.*?)</a>', source, re.I | re.S)
    category = plain(match.group(1)) if match else ''
    return category or 'Field reporting'


def polish(path: Path) -> bool:
    source = path.read_text(encoding='utf-8')
    if '<article class="page reading">' not in source:
        return False

    facts = FACTS_RE.search(source)
    if facts:
        publication = publication_from_facts(facts.group('body'))
        replacement = ''
        if publication:
            replacement = (
                '<div class="storypublication"><span>Published in</span>'
                f'<strong>{html.escape(publication)}</strong></div>'
            )
        source = source[:facts.start()] + replacement + source[facts.end():]

    match = HEADER_RE.search(source)
    if match:
        header = match.group('header')
        cover = match.group('cover') or ''
        if cover:
            visual = f'<div class="storyhero-visual storyhero-photo">{cover}</div>'
        else:
            label = html.escape(art_label(header))
            title = html.escape(art_title(header))
            visual = (
                '<div class="storyhero-visual storyhero-art" aria-hidden="true">'
                f'<div class="storyhero-art-copy"><span>{label}</span><strong>{title}</strong></div>'
                '</div>'
            )
        rebuilt = (
            '<header class="storyhead storyhero">'
            f'<div class="storyhero-copy">{header}</div>{visual}'
            '</header><div class="storymain">'
        )
        source = source[:match.start()] + rebuilt + source[match.end():]

    source = STYLE_RE.sub('', source)
    source = source.replace('</head>', f'<style id="{STYLE_ID}">\n{CSS}\n</style></head>', 1)
    path.write_text(source, encoding='utf-8')
    return True


def main() -> None:
    changed = 0
    for path in DIST.rglob('index.html'):
        changed += int(polish(path))
    print(f'Redesigned inside story pages: {changed}')


if __name__ == '__main__':
    main()
