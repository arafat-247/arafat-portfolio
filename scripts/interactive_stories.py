"""Story-specific interactive journalism renderer.

Interactive pages are opt-in. A story gets an interactive route only when its
editorial override supplies one or more factual modules.
"""
import json
from urllib.parse import urlsplit
from core import clean, date, esc, sanitise

SUPPORTED={'ratio','scenario','bar_chart','compare','explorer','timeline'}

def has_interactive(article):
    config=article.get('interactive')
    if not isinstance(config,dict) or config.get('enabled') is False:
        return False
    modules=config.get('modules')
    return isinstance(modules,list) and any(isinstance(m,dict) and m.get('type') in SUPPORTED for m in modules)

def _json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def _fmt(value, decimals=None):
    if isinstance(value,bool) or value is None:return ''
    if isinstance(value,(int,float)):
        if decimals is not None:return f'{value:.{int(decimals)}f}'
        if isinstance(value,float) and not value.is_integer():return f'{value:g}'
        return f'{int(value):,}'
    return clean(value)

def _module_header(module,index):
    eyebrow=esc(module.get('eyebrow') or f'Explore {index:02d}')
    title=esc(module.get('title') or 'Explore the reporting')
    text=esc(module.get('text') or '')
    text_html=f'<p>{text}</p>' if text else ''
    return f'<header class="ix-module-head"><span>{eyebrow}</span><h2>{title}</h2>{text_html}</header>'

def _method(note):
    return f'<p class="ix-method">{note}</p>' if note else ''

def _ratio(module,index):
    numerator=float(module.get('numerator') or 0)
    denominator=float(module.get('denominator') or 0)
    secondary=max(0,denominator-numerator)
    pct=(numerator/denominator*100) if denominator else 0
    primary=esc(module.get('primary_label') or 'Part')
    secondary_label=esc(module.get('secondary_label') or 'Remainder')
    unit=esc(module.get('unit') or '')
    note=esc(module.get('note') or '')
    payload={**module,'secondary_value':secondary}
    return (
      f'<section class="ix-module ix-ratio" id="interactive-{index}" data-ix-module="ratio">'
      f'{_module_header(module,index)}'
      f'<div class="ix-ratio-controls" role="group" aria-label="Choose measure">'
      f'<button type="button" data-ratio-choice="primary" aria-pressed="true">{primary}</button>'
      f'<button type="button" data-ratio-choice="secondary" aria-pressed="false">{secondary_label}</button></div>'
      f'<div class="ix-ratio-stage"><div class="ix-ratio-number"><strong data-ratio-value>{_fmt(numerator)}</strong><span>{unit}</span></div>'
      f'<div class="ix-ratio-track" aria-hidden="true"><span data-ratio-fill style="width:{pct:.2f}%"></span></div>'
      f'<p data-ratio-sentence>{primary}: {_fmt(numerator)} of {_fmt(denominator)} ({pct:.1f}%).</p></div>'
      f'{_method(note)}'
      f'<script type="application/json" data-ix-config>{_json(payload)}</script></section>'
    )

def _scenario(module,index):
    minimum=int(module.get('min') or 1); maximum=int(module.get('max') or minimum)
    start=int(module.get('start') or minimum); total=float(module.get('total') or 0)
    input_label=esc(module.get('input_label') or 'Value')
    output_label=esc(module.get('output_label') or 'Result')
    unit=esc(module.get('output_unit') or '')
    decimals=int(module.get('decimals') or 1)
    result=(total/start) if start else 0
    presets=''.join(
      f'<button type="button" data-scenario-preset="{int(p.get("value",start))}">{esc(p.get("label") or p.get("value"))}</button>'
      for p in module.get('presets',[]) if isinstance(p,dict)
    )
    note=esc(module.get('note') or '')
    return (
      f'<section class="ix-module ix-scenario" id="interactive-{index}" data-ix-module="scenario">'
      f'{_module_header(module,index)}'
      f'<div class="ix-scenario-grid"><div class="ix-control-panel"><label>{input_label}<strong data-scenario-input>{start}</strong>'
      f'<input type="range" min="{minimum}" max="{maximum}" value="{start}" step="1" data-scenario-range></label>'
      f'<div class="ix-presets">{presets}</div></div>'
      f'<div class="ix-output-panel"><span>{output_label}</span><strong data-scenario-output>{_fmt(result,decimals)}</strong><em>{unit}</em>'
      f'<div class="ix-people" data-scenario-visual aria-hidden="true"></div></div></div>'
      f'{_method(note)}'
      f'<script type="application/json" data-ix-config>{_json(module)}</script></section>'
    )

def _bar_chart(module,index):
    data=[d for d in module.get('data',[]) if isinstance(d,dict) and isinstance(d.get('value'),(int,float))]
    max_value=max([float(d['value']) for d in data],default=1)
    rows=''
    for i,item in enumerate(data):
        value=float(item['value']); width=(value/max_value*100) if max_value else 0
        rows+=(f'<button type="button" class="ix-bar-row" data-bar-index="{i}" aria-pressed="false">'
               f'<span class="ix-bar-label">{esc(item.get("label",""))}</span>'
               f'<span class="ix-bar-track"><i style="width:{width:.2f}%"></i></span>'
               f'<strong>{_fmt(value,module.get("decimals"))}{esc(module.get("suffix") or "")}</strong></button>')
    detail=esc(data[0].get('note','')) if data else ''
    note=esc(module.get('note') or '')
    return (
      f'<section class="ix-module ix-bars" id="interactive-{index}" data-ix-module="bar_chart">'
      f'{_module_header(module,index)}'
      f'<div class="ix-toolbar"><button type="button" data-bar-sort="original" aria-pressed="true">Reported order</button>'
      f'<button type="button" data-bar-sort="rank" aria-pressed="false">Rank</button></div>'
      f'<div class="ix-bar-list" data-bar-list>{rows}</div><p class="ix-chart-detail" data-bar-detail>{detail}</p>'
      f'{_method(note)}'
      f'<script type="application/json" data-ix-config>{_json(module)}</script></section>'
    )

def _compare(module,index):
    left=esc(module.get('left_label') or 'A'); right=esc(module.get('right_label') or 'B')
    metrics=[m for m in module.get('metrics',[]) if isinstance(m,dict)]
    buttons=''.join(f'<button type="button" data-compare-index="{i}" aria-pressed="{"true" if i==0 else "false"}">{esc(m.get("label") or f"Measure {i+1}")}</button>' for i,m in enumerate(metrics))
    first=metrics[0] if metrics else {}
    unit=esc(first.get('unit') or '')
    note=esc(module.get('note') or '')
    return (
      f'<section class="ix-module ix-compare" id="interactive-{index}" data-ix-module="compare">'
      f'{_module_header(module,index)}<div class="ix-tabs" role="group" aria-label="Choose measure">{buttons}</div>'
      f'<div class="ix-compare-stage"><article><span>{left}</span><strong data-compare-left>{_fmt(first.get("left"),first.get("decimals"))}</strong><em data-compare-unit-left>{unit}</em><i data-compare-bar-left></i></article>'
      f'<div class="ix-vs">vs</div><article><span>{right}</span><strong data-compare-right>{_fmt(first.get("right"),first.get("decimals"))}</strong><em data-compare-unit-right>{unit}</em><i data-compare-bar-right></i></article></div>'
      f'<p class="ix-delta" data-compare-delta></p>'
      f'{_method(note)}'
      f'<script type="application/json" data-ix-config>{_json(module)}</script></section>'
    )

def _explorer(module,index):
    options=[o for o in module.get('options',[]) if isinstance(o,dict)]
    tabs=''.join(f'<button type="button" data-explorer-index="{i}" aria-pressed="{"true" if i==0 else "false"}">{esc(o.get("label") or f"Option {i+1}")}</button>' for i,o in enumerate(options))
    first=options[0] if options else {}
    cards=''
    for metric in first.get('metrics',[]):
        small=f'<small>{esc(metric.get("note",""))}</small>' if metric.get('note') else ''
        cards+=(f'<article><span>{esc(metric.get("label",""))}</span><strong>{_fmt(metric.get("value"),metric.get("decimals"))}{esc(metric.get("suffix") or "")}</strong>'
                f'{small}</article>')
    note=esc(module.get('note') or '')
    return (
      f'<section class="ix-module ix-explorer" id="interactive-{index}" data-ix-module="explorer">'
      f'{_module_header(module,index)}<div class="ix-tabs ix-tabs-scroll" role="group" aria-label="Choose case">{tabs}</div>'
      f'<div class="ix-explorer-title"><strong data-explorer-title>{esc(first.get("title") or first.get("label") or "")}</strong><p data-explorer-text>{esc(first.get("text") or "")}</p></div>'
      f'<div class="ix-metric-grid" data-explorer-metrics>{cards}</div>'
      f'{_method(note)}'
      f'<script type="application/json" data-ix-config>{_json(module)}</script></section>'
    )

def _timeline(module,index):
    events=[e for e in module.get('events',[]) if isinstance(e,dict)]
    buttons=''.join(f'<button type="button" data-timeline-index="{i}" aria-pressed="{"true" if i==0 else "false"}"><span>{esc(e.get("date",""))}</span><strong>{esc(e.get("label",""))}</strong></button>' for i,e in enumerate(events))
    first=events[0] if events else {}
    note=esc(module.get('note') or '')
    return (
      f'<section class="ix-module ix-timeline" id="interactive-{index}" data-ix-module="timeline">'
      f'{_module_header(module,index)}<div class="ix-timeline-track" data-timeline-track>{buttons}</div>'
      f'<article class="ix-timeline-card"><span data-timeline-date>{esc(first.get("date",""))}</span><h3 data-timeline-title>{esc(first.get("label",""))}</h3><p data-timeline-text>{esc(first.get("text",""))}</p></article>'
      f'{_method(note)}'
      f'<script type="application/json" data-ix-config>{_json(module)}</script></section>'
    )

RENDERERS={'ratio':_ratio,'scenario':_scenario,'bar_chart':_bar_chart,'compare':_compare,'explorer':_explorer,'timeline':_timeline}

def render_interactive_page(article, *, site_url, asset_version, social_image_path, cover_image, date_label, analytics=''):
    config=article.get('interactive') or {}
    modules=[m for m in config.get('modules',[]) if isinstance(m,dict) and m.get('type') in RENDERERS]
    if not modules:return ''
    local_url=article['local_url']
    path=local_url+'interactive/index.html'
    prefix='../'*path.count('/')
    title=clean(article.get('title') or '')
    excerpt=clean(article.get('excerpt') or '')
    article_url=site_url+'/'+local_url
    interactive_url=article_url+'interactive/'
    source_name=clean(article.get('source_name') or '')
    authors=article.get('original_authors') or ['Arafat Rahaman']
    byline=', '.join(authors)
    cover=clean(cover_image or article.get('cover_image') or '')
    hero_visual=(f'<div class="ix-hero-media"><img src="{prefix}{esc(cover)}" alt="{esc(article.get("cover_alt") or "")}" fetchpriority="high" decoding="async"></div>' if cover.startswith('assets/') else '<div class="ix-hero-art" aria-hidden="true"><i></i><i></i><i></i></div>')
    hero_class=' has-image' if cover.startswith('assets/') else ''
    nav=''.join(f'<a href="#interactive-{i}"><span>{i:02d}</span>{esc(m.get("short_title") or m.get("title") or f"Explore {i}")}</a>' for i,m in enumerate(modules,1))
    module_html=''.join(RENDERERS[m['type']](m,i) for i,m in enumerate(modules,1))
    body=article.get('body_html') or ''
    body=sanitise(body,article.get('source_url',site_url+'/'))
    source=''
    if article.get('source_url') and urlsplit(article['source_url']).scheme=='https':
        source=(f'<p>Originally published by {esc(source_name)}. <a href="{esc(article["source_url"])}" rel="noopener noreferrer">Read the original publication ↗</a>.</p>')
    published=esc(date_label(article.get('date_published','')))
    social_image=site_url+'/'+(social_image_path or 'assets/social-preview-v2.jpg')
    description=excerpt[:187].rsplit(' ',1)[0]+'…' if len(excerpt)>190 else excerpt
    schema={
      '@context':'https://schema.org','@type':'WebPage','name':'Interactive: '+title,
      'url':interactive_url,'isPartOf':{'@type':'WebSite','url':site_url+'/'},
      'about':{'@type':'Article','headline':title,'url':article_url,'datePublished':article.get('date_published','')}
    }
    disclosure=esc(config.get('disclosure') or 'Interactive presentation built from figures and reporting in the published story. Derived values are labelled where used; quotations and reported facts are unchanged.')
    intro=esc(config.get('intro') or 'Use the controls to examine the figures, comparisons and cases behind this report.')
    kicker=esc(config.get('kicker') or 'Interactive reporting')
    return f'''<!doctype html><html lang="en"><head>{analytics}<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Interactive: {esc(title)} — Arafat Rahaman</title><meta name="description" content="{esc(description)}"><meta name="robots" content="noindex,follow"><meta name="theme-color" content="#063f37"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('portfolio-theme')||'light'}}catch(e){{document.documentElement.dataset.theme='light'}}</script><link rel="canonical" href="{esc(article_url)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap"><link rel="stylesheet" href="{prefix}interactive-story.css?v={asset_version}"><meta property="og:type" content="article"><meta property="og:site_name" content="Arafat Rahaman"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(interactive_url)}"><meta property="og:image" content="{esc(social_image)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{esc(social_image)}"><script type="application/ld+json">{_json(schema)}</script></head><body><a class="ix-skip" href="#explore">Skip to interactive</a><header class="ix-topbar"><a class="ix-brand" href="{prefix}"><span class="ix-brand-mark">A</span><span>Arafat Rahaman</span></a><nav class="ix-mode" aria-label="Reading mode"><a href="../">Article</a><span aria-current="page">Interactive</span></nav><a class="ix-exit" href="../">Exit interactive</a></header><main data-interactive-story><section class="ix-hero{hero_class}">{hero_visual}<div class="ix-hero-copy"><span class="ix-kicker">{kicker}</span><h1>{esc(title)}</h1><p class="ix-deck">{esc(excerpt)}</p><div class="ix-meta"><span>{published}</span><span>{esc(byline)}</span>{f"<span>{esc(source_name)}</span>" if source_name else ""}</div><a class="ix-start" href="#explore">Explore the reporting ↓</a></div></section><section class="ix-orientation"><strong>This is not a second version of the article.</strong><p>{intro}</p><small>{disclosure}</small></section><div class="ix-shell" id="explore"><aside class="ix-rail"><span>Explore</span><nav data-module-nav>{nav}</nav><div class="ix-progress"><i data-progress-fill></i></div></aside><div class="ix-modules">{module_html}<section class="ix-source-report"><span>Source reporting</span><h2>Read the full article behind the interactive</h2><details><summary>Open article text</summary><div class="ix-article-copy">{body}</div></details>{source}<a href="../">Return to standard article →</a></section></div></div></main><script src="{prefix}interactive-story.js?v={asset_version}" defer></script></body></html>'''
