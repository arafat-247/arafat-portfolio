"""Apply the approved mobile homepage after all existing homepage restoration passes.
Desktop and the four approved portfolio-panel backgrounds remain untouched.
"""
from __future__ import annotations
import html,json,re
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HOME=ROOT/'dist'/'index.html'
CASES=ROOT/'content'/'case-studies.json'
STYLE_ID='approved-mobile-home-v2'

def esc(v):return html.escape(str(v or ''),quote=True)
def date_label(v):
    try:d=datetime.fromisoformat(str(v).replace('Z','+00:00'))
    except ValueError:return ''
    return f'{d.day} {d.strftime("%b %Y")}'

def selected_reporting():
    data=json.loads(CASES.read_text(encoding='utf-8')) if CASES.is_file() else {'case_studies':[]}
    studies=list(data.get('case_studies',[]))[:3]
    if not studies:return ''
    images=['assets/home/reference-report.webp','assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp','assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (1).webp']
    def card(s,i,lead=False):
        title=s.get('source_title') or s.get('title') or 'Selected reporting'
        href=s.get('source_path') or 'reporting/'
        desc=s.get('description') or ''
        date=date_label(s.get('date_published',''))
        cls='selectedstory selectedstory-lead' if lead else 'selectedstory'
        return f'''<a class="{cls}" href="{esc(href)}"><figure aria-hidden="true"><img src="{esc(images[min(i,2)])}" alt="" loading="lazy" decoding="async"></figure><div class="selectedstory-copy"><span class="selectedstory-meta">{esc(date)}{' · ' if date else ''}Reporting</span><h3>{esc(title)}</h3>{f'<p>{esc(desc)}</p>' if lead and desc else ''}</div></a>'''
    lead=card(studies[0],0,True)
    rest=''.join(card(s,i) for i,s in enumerate(studies[1:],1))
    return f'''<section class="selectedreporting" id="selected-reporting" aria-labelledby="selected-reporting-title"><header class="selectedreporting-head"><span>Selected work</span><h2 id="selected-reporting-title">Selected reporting</h2></header><div class="selectedreporting-grid">{lead}<div class="selectedstory-pair">{rest}</div></div></section><div class="portfolio-divider" aria-label="The rest of the portfolio continues below"><span>Explore the portfolio</span><b aria-hidden="true">↓</b></div>'''

CSS=r'''
@media(max-width:800px){
.portalnav{position:relative!important;top:auto!important;z-index:20!important;display:flex!important;min-height:66px!important;width:100%!important;align-items:center!important;justify-content:flex-start!important;padding:10px 16px!important;border-bottom:1px solid rgb(39 29 20 / 12%)!important;background:#f7f1e7!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
.portalbrand{display:flex!important;align-items:center!important;gap:11px!important;color:#171512!important;text-decoration:none!important}.portalmonogram{display:grid;width:40px;height:40px;place-items:center;flex:0 0 auto;border-radius:50%;background:#0b5b50;color:#fff;font:700 14px/1 var(--serif);letter-spacing:-.04em}.portalbrandcopy{display:grid;gap:3px;min-width:0}.portalbrandcopy strong{font:400 21px/.95 var(--serif);letter-spacing:-.035em}.portalbrandcopy small{color:#746654;font:800 6.3px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase}.portalnavlinks,.portalmenu{display:none!important}
.portalhero{position:relative!important;display:block!important;width:100%!important;min-height:430px!important;overflow:hidden!important;padding:0!important;background:#073f38!important;color:#fff!important}.portalhero-copy{position:relative!important;z-index:5!important;width:61%!important;min-height:430px!important;padding:62px 14px 34px 20px!important;color:#fff!important;background:none!important;clip-path:none!important}.portalkicker,.portalhero-script,.portalhero-panel{display:none!important}.portalhero h1{margin:0 0 14px!important;color:#fff!important;font:400 clamp(34px,9.8vw,44px)/.92 var(--serif)!important;letter-spacing:-.05em!important}.portalhero-deck{max-width:95%!important;margin:0!important;color:#f1ece2!important;font:400 clamp(11.5px,3vw,13px)/1.45 var(--serif)!important}.portalhero-actions{display:flex!important;flex-wrap:wrap!important;gap:8px!important;margin-top:18px!important}.portalhero-actions a{display:inline-flex!important;min-height:38px!important;align-items:center!important;gap:10px!important;padding:0 13px!important;border:1px solid rgb(255 255 255 / 72%)!important;border-radius:999px!important;background:transparent!important;color:#fff!important;font:750 8.5px/1 var(--sans)!important;text-decoration:none!important}.portalhero-actions .portalhero-primary{background:#f7f1e7!important;border-color:#f7f1e7!important;color:#073f38!important}.portalhero-visual{position:absolute!important;z-index:3!important;inset:0!important;min-height:0!important}.portalhero-photo{position:absolute!important;z-index:3!important;top:0!important;right:0!important;width:49%!important;height:100%!important;margin:0!important;overflow:hidden!important;clip-path:polygon(21% 0,100% 0,100% 100%,0 100%,12% 50%)!important}.portalhero-photo picture,.portalhero-photo img{display:block!important;width:100%!important;height:100%!important}.portalhero-photo img{object-fit:cover!important;object-position:51% 38%!important;filter:grayscale(1) contrast(1.03)!important}.portalhero-photo:after{content:""!important;position:absolute!important;inset:0!important;background:linear-gradient(90deg,#073f38 0,rgba(7,63,56,.52) 15%,transparent 46%)!important;pointer-events:none!important}
.selectedreporting{padding:30px 17px 24px;background:#f4eee4;color:#171512;border-top:1px solid rgb(39 29 20 / 10%)}.selectedreporting-head{display:flex;align-items:end;justify-content:space-between;gap:12px;margin-bottom:15px}.selectedreporting-head>span{color:#0b5b50;font:800 6.7px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase}.selectedreporting-head h2{margin:0;font:400 clamp(25px,7vw,31px)/.95 var(--serif);letter-spacing:-.04em;text-align:right}.selectedreporting-grid{display:grid;gap:11px}.selectedstory{display:block;overflow:hidden;border:1px solid rgb(58 43 28 / 12%);border-radius:4px;background:#faf5ed;color:#171512;text-decoration:none}.selectedstory figure{margin:0;overflow:hidden;background:#ddd4c6;aspect-ratio:16/10}.selectedstory figure img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(.82) contrast(1.02)}.selectedstory-copy{padding:10px 10px 12px}.selectedstory-meta{display:block;margin-bottom:6px;color:#7d6a54;font:800 6.4px/1.1 var(--sans);letter-spacing:.11em;text-transform:uppercase}.selectedstory h3{margin:0;font:600 16px/1.08 var(--serif);letter-spacing:-.025em}.selectedstory-lead{display:grid;grid-template-columns:1.08fr .92fr;min-height:156px}.selectedstory-lead figure{height:100%;min-height:156px;aspect-ratio:auto}.selectedstory-lead .selectedstory-copy{display:flex;flex-direction:column;justify-content:center;padding:13px}.selectedstory-lead h3{font-size:20px;line-height:1.04}.selectedstory-lead p{margin:8px 0 0;color:#685948;font:400 10.5px/1.35 var(--serif)}.selectedstory-pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.portfolio-divider{display:flex;min-height:48px;align-items:center;justify-content:center;gap:9px;padding:8px 16px;border-top:1px solid rgb(57 43 30 / 18%);border-bottom:1px solid rgb(57 43 30 / 18%);background:#eee5d8;color:#164f48}.portfolio-divider span{font:700 11px/1 var(--serif);letter-spacing:.01em}.portfolio-divider b{font:700 13px/1 var(--sans)}.portalwork{margin:0!important}
}
@media(max-width:360px){.portalnav{min-height:62px!important;padding-inline:13px!important}.portalmonogram{width:37px;height:37px;font-size:13px}.portalbrandcopy strong{font-size:19px}.portalhero{min-height:438px!important}.portalhero-copy{width:64%!important;min-height:438px!important;padding:58px 10px 28px 16px!important}.portalhero h1{font-size:34px!important}.portalhero-deck{font-size:11.3px!important}.portalhero-photo{width:48%!important}.selectedreporting{padding-inline:14px}.selectedstory-lead{grid-template-columns:1fr;min-height:0}.selectedstory-lead figure{min-height:0;aspect-ratio:16/9}.selectedstory-lead p{display:none}}
'''.strip()

def main():
    if not HOME.is_file():raise FileNotFoundError('dist/index.html does not exist; run the build first')
    source=HOME.read_text(encoding='utf-8')
    nav_start=source.find('<nav class="portalnav"')
    hero_start=source.find('<section class="portalhero"',nav_start)
    work_start=source.find('<section class="portalwork"',hero_start)
    if min(nav_start,hero_start,work_start)<0:raise RuntimeError('Expected mobile homepage structure is missing')
    nav='''<nav class="portalnav" aria-label="Homepage identity"><a class="portalbrand" href="./"><span class="portalmonogram" aria-hidden="true">AR</span><span class="portalbrandcopy"><strong>Arafat Rahaman</strong><small>Journalist · Bangladesh</small></span></a></nav>'''
    hero='''<section class="portalhero" aria-labelledby="portal-home-title"><div class="portalhero-copy"><span class="portalkicker">Journalist · Bangladesh</span><h1 id="portal-home-title">Arafat Rahaman</h1><p class="portalhero-deck">Journalist at The Daily Star, reporting on education, governance, public accountability and social issues across Bangladesh.</p><div class="portalhero-actions"><a class="portalhero-primary" href="about/">About me <b aria-hidden="true">→</b></a><a href="#selected-reporting">Explore my work <b aria-hidden="true">↓</b></a></div></div><div class="portalhero-visual" aria-hidden="true"><figure class="portalhero-photo"><picture><source srcset="assets/portraits/byline.avif" type="image/avif"><img src="assets/portraits/byline.webp" alt="" width="1000" height="991" loading="eager" fetchpriority="high" decoding="async"></picture></figure></div></section>'''
    source=source[:nav_start]+nav+hero+selected_reporting()+source[work_start:]
    source=re.sub(rf'<style id="{STYLE_ID}">.*?</style>','',source,flags=re.I|re.S)
    source=source.replace('</head>',f'<style id="{STYLE_ID}">\n{CSS}\n</style></head>',1)
    HOME.write_text(source,encoding='utf-8')
    print('Approved mobile homepage applied: header_option=1, selected_reporting=3, divider=slim, portfolio_backgrounds=preserved, desktop_untouched=1')

if __name__=='__main__':main()
