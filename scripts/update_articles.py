#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, html as html_lib, json, re, shutil, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import trafilatura

AUTHOR_NAME="Arafat Rahaman"
AUTHOR_SLUG="/author/arafat-rahaman"
AUTHOR_URL="https://www.thedailystar.net/author/arafat-rahaman"
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"site"; DATA_FILE=SITE/"data"/"articles.json"; STORIES=SITE/"stories"; CACHE=ROOT/".portfolio-cache"/"articles"
CONFIG_FILE=SITE/"data"/"site_config.json"; ENHANCEMENTS_FILE=SITE/"data"/"story_enhancements.json"
ARTICLE_ID=re.compile(r"-(\d{5,})/?$")
STORY_HINTS=("/news/","/opinion/","/business/","/sports/","/entertainment/","/lifestyle/","/youth/","/supplements/","/slow-reads/","/analysis/","/views/","/culture/","/star-multimedia/","/ds/")
UA="Mozilla/5.0 (compatible; ArafatRahamanPortfolio/7.0; public-author-portfolio-indexer)"
ALLOWED={"p","h2","h3","h4","blockquote","ul","ol","li","strong","b","em","i","a","br","table","thead","tbody","tr","th","td","caption"}
BD_TZ=timezone(timedelta(hours=6))

def clean(v:str)->str:return re.sub(r"\s+"," ",v or "").strip()
def canonical_source(url:str)->str:
    p=urlparse(url); return p._replace(query="",fragment="").geturl()
def meta(soup,key,value):
    n=soup.find("meta",attrs={key:value}); return clean(n.get("content","")) if n else ""
def walk_json(v):
    if isinstance(v,dict):
        yield v
        for c in v.values(): yield from walk_json(c)
    elif isinstance(v,list):
        for c in v: yield from walk_json(c)
def ld_objects(soup):
    for n in soup.find_all("script",attrs={"type":"application/ld+json"}):
        raw=n.string or n.get_text()
        if not raw.strip(): continue
        try: payload=json.loads(raw)
        except Exception: continue
        yield from walk_json(payload)
def types_of(obj):
    t=obj.get("@type",[]) if isinstance(obj,dict) else []
    return [str(x) for x in (t if isinstance(t,list) else [t])]
def url_candidates(obj):
    vals=[]
    for key in ("url","@id"):
        v=obj.get(key) if isinstance(obj,dict) else None
        if isinstance(v,str): vals.append(v)
    m=obj.get("mainEntityOfPage") if isinstance(obj,dict) else None
    if isinstance(m,str): vals.append(m)
    elif isinstance(m,dict):
        for key in ("@id","url"):
            if isinstance(m.get(key),str): vals.append(m[key])
    return [canonical_source(urljoin(AUTHOR_URL,v)) for v in vals]
def same_article_url(a,b):
    pa,pb=urlparse(canonical_source(a)),urlparse(canonical_source(b)); return pa.netloc==pb.netloc and pa.path.rstrip("/")==pb.path.rstrip("/")
def article_ld_objects(soup,source_url):
    matched=[]; fallback=[]
    for obj in ld_objects(soup):
        if not isinstance(obj,dict): continue
        if not any("article" in t.lower() for t in types_of(obj)): continue
        urls=url_candidates(obj)
        if urls and any(same_article_url(u,source_url) for u in urls): matched.append(obj)
        elif not urls: fallback.append(obj)
    return matched or fallback[:2]
def author_names(obj):
    out=[]; authors=obj.get("author",[]) if isinstance(obj,dict) else []
    for a in (authors if isinstance(authors,list) else [authors]):
        if isinstance(a,dict): n=clean(str(a.get("name","")))
        else: n=clean(str(a))
        if n: out.append(n)
    return out
def author_verified(soup,source_url):
    for obj in article_ld_objects(soup,source_url):
        if AUTHOR_NAME.casefold() in {n.casefold() for n in author_names(obj)}: return True
    containers=[x for x in (soup.find("article"),soup.find("main")) if x] or [soup]
    for c in containers:
        for a in c.find_all("a",href=True):
            href=urlparse(urljoin(source_url,a["href"])).path.rstrip("/")
            if href==AUTHOR_SLUG and clean(a.get_text(" ",strip=True)).casefold()==AUTHOR_NAME.casefold(): return True
    for sel in (".author-name",".byline","[class*='author-name']","[class*='byline']","[rel='author']"):
        for n in soup.select(sel):
            if AUTHOR_NAME.casefold() in clean(n.get_text(" ",strip=True)).casefold(): return True
    return False

def archive_url(page): return AUTHOR_URL if page==0 else f"{AUTHOR_URL}?page={page}"
def discover_candidates(session,page):
    r=session.get(archive_url(page),timeout=35); r.raise_for_status(); soup=BeautifulSoup(r.text,"html.parser"); host=urlparse(AUTHOR_URL).netloc
    found=[]; seen=set()
    for a in soup.find_all("a",href=True):
        u=canonical_source(urljoin(AUTHOR_URL,a["href"])); p=urlparse(u)
        if p.netloc!=host or not ARTICLE_ID.search(p.path) or not any(t in p.path.lower() for t in STORY_HINTS) or u in seen: continue
        seen.add(u); found.append(u)
    return found

def normalise_datetime(raw):
    raw=clean(raw)
    if not raw:return ""
    try:
        d=datetime.fromisoformat(raw.replace("Z","+00:00"))
        if d.tzinfo is None:d=d.replace(tzinfo=BD_TZ)
        return d.isoformat()
    except Exception: pass
    formats=("%d %B %Y","%d %b %Y","%B %d, %Y","%b %d, %Y","%B %d %Y","%b %d %Y")
    candidate=re.sub(r",\s*\d{1,2}:\d{2}.*$","",raw)
    for fmt in formats:
        try:return datetime.strptime(candidate,fmt).replace(tzinfo=BD_TZ).isoformat()
        except ValueError:pass
    m=re.match(r"^(\d{4}-\d{2}-\d{2})",raw)
    if m:return datetime.fromisoformat(m.group(1)).replace(tzinfo=BD_TZ).isoformat()
    return ""
def published_sort(value):
    try:return int(datetime.fromisoformat(value.replace("Z","+00:00")).timestamp())
    except Exception:return 0
def display_date(value):
    m=re.match(r"^(\d{4})-(\d{2})-(\d{2})",value or "")
    if not m:return value or ""
    d=datetime(int(m[1]),int(m[2]),int(m[3])); return f"{d.day} {d.strftime('%B %Y')}"
def section_from_url(url):
    path=urlparse(url).path.lower(); mapping=[("/education/","Education"),("/politics/","Politics"),("/governance/","Governance"),("/health","Health"),("/environment/","Environment"),("/business/","Business"),("/sports/","Sports"),("/opinion/","Opinion"),("/views/","Opinion"),("/analysis/","Analysis"),("/culture/","Culture"),("/youth/","Youth")]
    for token,label in mapping:
        if token in path:return label
    return "News"
def story_type(url,section):
    text=f"{url} {section}".lower(); return "Opinion / Analysis" if any(x in text for x in ("/opinion/","/views/","/analysis/","opinion","analysis")) else "Reporting"
def topic_from_story(url,section,title):
    text=f"{url} {section} {title}".lower(); rules=[
        (("education","school","university","ssc","hsc","ugc","nctb","teacher","student","curriculum"),"Education"),
        (("politic","parliament","government","cabinet","bnp","jamaat","election","minister"),"Politics & Governance"),
        (("rights","disappear","police","court","justice","mob","law and order","worker"),"Human Rights & Justice"),
        (("health","dengue","hospital","medical","disease"),"Health"),
        (("environment","climate","pollution","noise","river"),"Environment"),
        (("business","budget","economy","inflation","fertiliser","agriculture","wage","salary"),"Economy & Livelihoods"),
        (("sports","football","cricket","messi"),"Sport")]
    for needles,label in rules:
        if any(n in text for n in needles):return label
    if section and section.lower() not in {"news","bangladesh"}:return section
    return "Public Affairs"
def format_tag(url,section):
    t=f"{url} {section}".lower(); return "Feature" if "feature" in t or "/slow-reads/" in t else ""

def sanitise_body(raw_html,source_url):
    soup=BeautifulSoup(raw_html or "","html.parser")
    for bad in soup.find_all(["script","style","iframe","form","button","input","svg","video"]):bad.decompose()
    for tag in list(soup.find_all(True)):
        if tag.name not in ALLOWED: tag.unwrap(); continue
        keep={}
        if tag.name=="a" and tag.get("href"):
            keep={"href":urljoin(source_url,tag["href"]),"rel":"noopener","target":"_blank"}
        tag.attrs=keep
    return str(soup).strip()
def fallback_body(soup,source_url):
    for sel in ("article .article-content","article [class*='article-body']","article [class*='story-body']",".article-content",".article-body",".story-content",".field--name-body","article"):
        n=soup.select_one(sel)
        if not n:continue
        clone=BeautifulSoup(str(n),"html.parser")
        for bad in clone.select("script,style,nav,aside,form,button,iframe,.related,.share,[class*='advert'],[id*='advert'],[class*='newsletter'],[class*='social']"):bad.decompose()
        pieces=[]
        for el in clone.find_all(["p","h2","h3","h4","blockquote","ul","ol","table"]):
            if len(clean(el.get_text(" ",strip=True)))>=2:pieces.append(str(el))
        return sanitise_body("\n".join(pieces),source_url)
    return ""
def strip_duplicate_intro(body,title):
    soup=BeautifulSoup(body or "","html.parser"); title_norm=clean(title).casefold()
    candidates=soup.find_all(["p","h2","h3"],limit=6)
    for node in candidates:
        txt=clean(node.get_text(" ",strip=True)); norm=txt.casefold()
        if norm==title_norm or (len(title_norm)>20 and (norm.startswith(title_norm) or title_norm.startswith(norm))):node.decompose();continue
        if norm in {AUTHOR_NAME.casefold(),f"by {AUTHOR_NAME}".casefold()}:node.decompose()
    return str(soup).strip()
def slugify(value):
    v=re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-"); return v[:86].strip("-") or "story"
def story_id(url):
    m=ARTICLE_ID.search(urlparse(url).path);return m.group(1) if m else hashlib.sha1(url.encode()).hexdigest()[:10]
def old_local_url(story):return f"stories/{story_id(story['url'])}-{slugify(story['title'])}/"

def load_cache(url):
    path=CACHE/f"{story_id(url)}.json"
    if not path.exists():return None
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
        if data.get("cache_schema")!=7 or data.get("url")!=canonical_source(url):return None
        pub=data.get("date_published","")
        if pub and published_sort(pub)<int((datetime.now(timezone.utc)-timedelta(days=10)).timestamp()):return data
    except Exception:return None
    return None
def save_cache(story):
    CACHE.mkdir(parents=True,exist_ok=True); d=dict(story);d["cache_schema"]=7;(CACHE/f"{story_id(story['url'])}.json").write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")

def extract_story(session,url):
    cached=load_cache(url)
    if cached:return cached
    r=session.get(url,timeout=40);r.raise_for_status();page_html=r.text;soup=BeautifulSoup(page_html,"html.parser")
    if not author_verified(soup,url):return None
    title=meta(soup,"property","og:title") or meta(soup,"name","twitter:title") or clean(soup.find("h1").get_text(" ",strip=True) if soup.find("h1") else "")
    title=re.sub(r"\s*\|\s*The Daily Star\s*$","",title,flags=re.I)
    if not title:return None
    excerpt=meta(soup,"property","og:description") or meta(soup,"name","description") or meta(soup,"name","twitter:description")
    article_objs=article_ld_objects(soup,url); ld=article_objs[0] if article_objs else {}
    raw_pub=(ld.get("datePublished") if isinstance(ld.get("datePublished"),str) else "") or meta(soup,"property","article:published_time") or meta(soup,"name","date") or meta(soup,"name","pubdate")
    raw_mod=(ld.get("dateModified") if isinstance(ld.get("dateModified"),str) else "") or meta(soup,"property","article:modified_time")
    if not raw_pub:
        tn=soup.find("time");raw_pub=(tn.get("datetime") or tn.get_text(" ",strip=True)) if tn else ""
    pub=normalise_datetime(raw_pub);mod=normalise_datetime(raw_mod)
    section_raw=meta(soup,"property","article:section") or meta(soup,"name","section");section=clean(section_raw).title() if section_raw else section_from_url(url)
    extracted=trafilatura.extract(page_html,url=url,include_comments=False,include_tables=True,include_images=False,favor_precision=True,output_format="html") or ""
    body=sanitise_body(extracted,url); text=clean(BeautifulSoup(body,"html.parser").get_text(" ",strip=True))
    if len(text)<180:body=fallback_body(soup,url)
    body=strip_duplicate_intro(body,title);text=clean(BeautifulSoup(body,"html.parser").get_text(" ",strip=True))
    authors=[]
    for obj in article_objs:
        for n in author_names(obj):
            if n not in authors:authors.append(n)
    if AUTHOR_NAME not in authors:authors.insert(0,AUTHOR_NAME)
    nums=len(re.findall(r"\b\d[\d,.]*%?\b",text));tables=len(BeautifulSoup(body,"html.parser").find_all("table"))
    story={"title":title,"excerpt":excerpt,"url":canonical_source(url),"authors":authors[:8],"section":section,"story_type":story_type(url,section),"topic":topic_from_story(url,section,title),"format_tag":format_tag(url,section),"date_published":pub,"date_modified":mod,"date":pub[:10] if pub else "","published_sort":published_sort(pub),"word_count":len(text.split()),"table_count":tables,"numeric_mentions":nums,"data_rich":bool(tables or (nums>=24 and len(text.split())>=650)),"body_html":body,"verified_author":True,"scraped_at":datetime.now(timezone.utc).isoformat()}
    save_cache(story);return story

def load_config():return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
def load_enhancements():
    try:return json.loads(ENHANCEMENTS_FILE.read_text(encoding="utf-8"))
    except Exception:return {}
def abs_site(config,path=""):
    return config.get("site_url","").rstrip("/")+"/"+path.lstrip("/")
def picture_markup(base,alt,prefix="../../",eager=True):
    if not base:return ""
    return f'<picture><source srcset="{prefix}{html_lib.escape(base)}.avif" type="image/avif"><source srcset="{prefix}{html_lib.escape(base)}.webp" type="image/webp"><img src="{prefix}{html_lib.escape(base)}.webp" alt="{html_lib.escape(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"></picture>'
def story_header():
    return '''<header class="site-header"><div class="masthead shell"><a class="brand" href="../../"><span class="brand-mark">A/R</span><span class="brand-copy"><strong>Arafat Rahaman</strong><small>Staff Reporter</small></span></a><nav class="desktop-nav" aria-label="Primary"><a href="../../">Home</a><a href="../../archive.html">Archive</a><a href="../../photography.html">Photography</a><a href="../../about.html">About</a><a href="../../contact.html">Contact</a><a class="tip-nav" href="../../contact.html#send-a-tip">Send a tip</a><button class="theme-toggle" type="button" data-theme-toggle>☾</button></nav><div class="mobile-actions"><button class="theme-toggle" type="button" data-theme-toggle>☾</button><button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span><b class="sr-only">Menu</b></button></div></div><nav id="mobile-nav" class="mobile-nav shell" data-mobile-nav hidden><a href="../../">Home</a><a href="../../archive.html">Archive</a><a href="../../photography.html">Photography</a><a href="../../about.html">About</a><a href="../../contact.html">Contact</a><a class="tip-nav" href="../../contact.html#send-a-tip">Send a tip</a></nav></header>'''
def story_footer():
    return '''<footer class="site-footer"><div class="footer-rule"></div><div class="shell footer-main"><div class="footer-identity"><p class="footer-name">Arafat Rahaman</p><p>Staff Reporter · Dhaka, Bangladesh</p><a href="mailto:arafat.mcj@yahoo.com">arafat.mcj@yahoo.com</a></div><div class="footer-nav"><p>Explore</p><a href="../../">Home</a><a href="../../archive.html">Archive</a><a href="../../photography.html">Photography</a><a href="../../about.html">About</a><a href="../../contact.html">Contact</a></div><div class="footer-social"><p>Professional profiles</p><a href="https://www.thedailystar.net/author/arafat-rahaman" target="_blank" rel="noopener">The Daily Star ↗</a><a href="https://muckrack.com/arafat-rahaman" target="_blank" rel="noopener">Muck Rack ↗</a><a href="https://bd.linkedin.com/in/arafat-rahaman" target="_blank" rel="noopener">LinkedIn ↗</a><a href="https://www.facebook.com/araafat.rahaman/" target="_blank" rel="noopener">Facebook ↗</a><a href="https://www.instagram.com/araafat.rahaman/" target="_blank" rel="noopener">Instagram ↗</a><a href="https://www.flickr.com/photos/arafat-rahaman/" target="_blank" rel="noopener">Flickr ↗</a></div><a class="footer-tip" href="../../contact.html#send-a-tip"><span>Have information?</span><strong>Send a news tip</strong><b>→</b></a></div><div class="shell footer-bottom"><span>© Arafat Rahaman</span><span>Personal journalism portfolio</span><a href="../../feed.xml">RSS</a></div></footer>'''

def generate_story_page(story,config,enhancements):
    source=story["url"]; title=html_lib.escape(story["title"]); excerpt=html_lib.escape(story.get("excerpt","") or ""); typ=html_lib.escape(story["story_type"]);topic=html_lib.escape(story["topic"]);pub=display_date(story.get("date_published",""));mod=display_date(story.get("date_modified",""));body=story.get("body_html","") or '<p>The article body could not be extracted cleanly. Please read the original publication.</p>'
    local_abs=abs_site(config,story["local_url"]); category_q=quote(story["story_type"]);topic_q=quote(story["topic"]); e=enhancements.get(source,{}) if isinstance(enhancements.get(source,{}),dict) else {};hero=e.get("hero",{}) if isinstance(e,dict) else {}; hero_html=""
    og_image=""
    if isinstance(hero,dict) and hero.get("base"):
        hero_html=f'<figure class="story-hero-media">{picture_markup(hero["base"],hero.get("alt") or f"Editorial illustration for {story["title"]}")}<figcaption><span>{html_lib.escape(hero.get("caption","") or "")}</span><span>{html_lib.escape(hero.get("credit","") or "")}</span></figcaption></figure>'
        og_image=abs_site(config,hero["base"]+".webp")
    raw_pub=story.get("date_published","")
    raw_mod=story.get("date_modified","")
    updated="" if not raw_mod or published_sort(raw_mod) <= published_sort(raw_pub)+60 else f'<span>Updated {html_lib.escape(mod)}</span>'
    jsonld={"@context":"https://schema.org","@type":"NewsArticle" if story["story_type"]=="Reporting" else "Article","headline":story["title"],"description":story.get("excerpt","") or "","datePublished":story.get("date_published","") or None,"dateModified":story.get("date_modified","") or story.get("date_published","") or None,"author":{"@type":"Person","name":"Arafat Rahaman","url":abs_site(config,"about.html"),"sameAs":[config.get("social",{}) for _ in []]},"publisher":{"@type":"Organization","name":"The Daily Star","url":"https://www.thedailystar.net/"},"isBasedOn":source,"mainEntityOfPage":source,"url":local_abs}
    jsonld["author"]["sameAs"]=[v for v in config.get("social",{}).values() if v]
    if og_image:jsonld["image"]=og_image
    jsonld_text=json.dumps(jsonld,ensure_ascii=False).replace("</", "<" + "\\/")
    stand=f'<p class="story-standfirst">{excerpt}</p>' if excerpt else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>{title} — Arafat Rahaman</title><meta name="description" content="{excerpt}"><link rel="canonical" href="{html_lib.escape(source,quote=True)}"><link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" href="../../feed.xml"><meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{excerpt}"><meta property="og:url" content="{html_lib.escape(local_abs,quote=True)}">{f'<meta property="og:image" content="{html_lib.escape(og_image,quote=True)}">' if og_image else ''}<script>(function(){{try{{var t=localStorage.getItem('ar-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}}})();</script><script type="application/ld+json">{jsonld_text}</script><link rel="stylesheet" href="../../styles.css"></head><body class="story-page" data-root="../../" data-source-url="{html_lib.escape(source,quote=True)}" data-word-count="{story.get('word_count',0)}"><div id="reading-progress" class="reading-progress" hidden><span></span></div><a class="skip-link" href="#article">Skip to article</a>{story_header()}<main class="story-main shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span>/</span><a href="../../archive.html?type={category_q}">{typ}</a><span>/</span><span>Article</span></nav><header class="story-header"><div class="story-header-meta"><a href="../../archive.html?type={category_q}">{typ}</a><a href="../../archive.html?topic={topic_q}">{topic}</a><span>Published {html_lib.escape(pub)}</span>{updated}</div><h1>{title}</h1>{stand}<div class="story-byline"><span>By <strong>Arafat Rahaman</strong> <span aria-hidden="true">·</span> {max(1,round(story.get('word_count',0)/220))} min read</span><div class="story-tools-inline"><button class="story-tool" data-share="copy">Copy link</button><button class="story-tool" data-print>Print / Save PDF</button></div></div></header>{hero_html}<div class="story-layout"><article id="article" class="story-prose">{body}</article><aside class="story-sidebar" aria-label="Story tools"><div class="sidebar-stack"><section class="side-card source-card"><p class="side-card-title">ORIGINAL PUBLICATION</p><p>Originally published by <em>The Daily Star</em>.</p><time>{html_lib.escape(pub)}</time><a class="side-action" href="{html_lib.escape(source,quote=True)}" target="_blank" rel="noopener"><span>Read original</span><b>↗</b></a></section><section class="side-card share-card"><p class="side-card-title">SHARE</p><div class="share-buttons"><button data-share="copy">Copy</button><button data-share="whatsapp">WhatsApp</button><button data-share="facebook">Facebook</button><button data-share="x">X</button><button data-share="linkedin">LinkedIn</button><button data-print>Print</button></div></section><section class="side-card"><p class="side-card-title">EXPLORE</p><div class="explore-links"><a href="../../archive.html?topic={topic_q}"><span>More on {topic}</span><b>→</b></a><a href="#related-stories"><span>Related stories</span><b>↓</b></a><a href="../../archive.html"><span>Full archive</span><b>→</b></a></div></section><section id="evidence-card" class="side-card" hidden><p class="side-card-title">EVIDENCE &amp; CONTEXT</p><div class="evidence-links"></div></section></div></aside></div><div class="mobile-share-bar" aria-label="Share this story" hidden><button data-share="copy">Copy</button><button data-share="whatsapp">WhatsApp</button><button data-share="facebook">Facebook</button><button data-print>Print</button></div><div class="source-end"><p>Original publication: <em>The Daily Star</em> · {html_lib.escape(pub)}</p><a href="{html_lib.escape(source,quote=True)}" target="_blank" rel="noopener">View original article ↗</a></div><section id="related-stories" class="related-section"></section><nav id="story-sequence" class="story-sequence" aria-label="Previous and next stories"></nav></main>{story_footer()}<script src="../../common.js"></script><script src="../../story.js"></script></body></html>'''

def assign_local_urls(stories):
    used={}
    for s in stories:
        base=slugify(s["title"]); slug=base if base not in used else f"{base}-{story_id(s['url'])}"; used[base]=used.get(base,0)+1; s["local_url"]=f"stories/{slug}/"
def write_redirect(path,target):
    path.mkdir(parents=True,exist_ok=True); path.joinpath("index.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="../../{target}"><meta http-equiv="refresh" content="0; url=../../{target}"><script>location.replace("../../{target}")</script><a href="../../{target}">Continue</a>',encoding="utf-8")
def write_story_pages(stories,config,enhancements):
    if STORIES.exists():shutil.rmtree(STORIES)
    STORIES.mkdir(parents=True,exist_ok=True)
    for s in stories:
        folder=SITE/s["local_url"];folder.mkdir(parents=True,exist_ok=True);folder.joinpath("index.html").write_text(generate_story_page(s,config,enhancements),encoding="utf-8")
        old=old_local_url(s)
        if old!=s["local_url"]:write_redirect(SITE/old,s["local_url"])
def xml_escape(s):return html_lib.escape(str(s or ""),quote=True)
def write_feed(stories,config):
    items=[]
    for s in stories[:50]:
        link=abs_site(config,s["local_url"]);pub=s.get("date_published","")
        try:rfc=datetime.fromisoformat(pub.replace("Z","+00:00")).strftime("%a, %d %b %Y %H:%M:%S %z")
        except Exception:rfc=""
        items.append(f'<item><title>{xml_escape(s["title"])}</title><link>{xml_escape(link)}</link><guid isPermaLink="false">{xml_escape(s["url"])}</guid><description>{xml_escape(s.get("excerpt",""))}</description>{f"<pubDate>{rfc}</pubDate>" if rfc else ""}</item>')
    rss=f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Arafat Rahaman — Latest work</title><link>{xml_escape(abs_site(config))}</link><description>Latest verified reporting and analysis by Arafat Rahaman.</description>{"".join(items)}</channel></rss>'
    SITE.joinpath("feed.xml").write_text(rss,encoding="utf-8")
def write_sitemap(config):
    urls=["","archive.html","photography.html","about.html","contact.html"]
    xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{xml_escape(abs_site(config,u))}</loc></url>' for u in urls)+'</urlset>'
    SITE.joinpath("sitemap.xml").write_text(xml,encoding="utf-8")
    SITE.joinpath("robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {abs_site(config,"sitemap.xml")}\n',encoding="utf-8")
def write_art_queue(stories,enhancements):
    q=[]
    for s in stories:
        e=enhancements.get(s["url"],{}) if isinstance(enhancements,dict) else {}
        if not isinstance(e,dict) or not e.get("hero"):
            q.append({"url":s["url"],"local_url":s["local_url"],"title":s["title"],"excerpt":s.get("excerpt",""),"topic":s.get("topic"),"story_type":s.get("story_type"),"art_direction":"Create an original editorial illustration that communicates the specific subject or central argument of this story. Avoid generic newsroom branding, text-heavy covers and decorative AR monograms."})
    SITE.joinpath("data","story_art_queue.json").write_text(json.dumps({"stories":q},ensure_ascii=False,indent=2),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--pages",type=int,default=60);ap.add_argument("--delay",type=float,default=.30);args=ap.parse_args()
    config=load_config();enhancements=load_enhancements();session=requests.Session();session.headers.update({"User-Agent":UA,"Accept-Language":"en-GB,en;q=0.9","Accept":"text/html,application/xhtml+xml"})
    candidates=[];seen=set()
    for page in range(max(1,args.pages)):
        try:links=discover_candidates(session,page)
        except Exception as exc:print(f"Archive page {page}: {exc}",file=sys.stderr);continue
        new=[u for u in links if u not in seen]
        for u in new:seen.add(u);candidates.append(u)
        print(f"Archive page {page}: {len(links)} candidates, {len(new)} new, {len(candidates)} unique",file=sys.stderr);time.sleep(max(0,args.delay))
    if not candidates:raise SystemExit("No candidate story URLs discovered.")
    verified=[];rejected=0
    for i,url in enumerate(candidates,1):
        try:
            s=extract_story(session,url)
            if s:verified.append(s);print(f"[{i}/{len(candidates)}] VERIFIED {s['title']}",file=sys.stderr)
            else:rejected+=1;print(f"[{i}/{len(candidates)}] rejected {url}",file=sys.stderr)
        except Exception as exc:print(f"[{i}/{len(candidates)}] failed {url}: {exc}",file=sys.stderr)
        if i<len(candidates):time.sleep(max(0,args.delay))
    unique={s["url"]:s for s in verified};stories=sorted(unique.values(),key=lambda s:(s.get("published_sort",0),s.get("title","")),reverse=True)
    if not stories:raise SystemExit("No Arafat Rahaman stories passed verification.")
    assign_local_urls(stories);write_story_pages(stories,config,enhancements)
    payload={"updated_at":datetime.now(timezone.utc).isoformat(),"source":AUTHOR_URL,"author":AUTHOR_NAME,"candidate_urls_checked":len(candidates),"non_author_urls_rejected":rejected,"articles":stories}
    DATA_FILE.parent.mkdir(parents=True,exist_ok=True);DATA_FILE.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    write_feed(stories,config);write_sitemap(config);write_art_queue(stories,enhancements)
    print(f"Completed: {len(stories)} verified stories; {rejected} unrelated candidates rejected.",file=sys.stderr);return 0
if __name__=="__main__":raise SystemExit(main())
