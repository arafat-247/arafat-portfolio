"""Build public pages from durable content; drafts never enter dist."""
import json, re, shutil
from datetime import datetime
from urllib.parse import urlsplit
from core import *
from social_cards import SocialCardRenderer

STREAMS={'reporting':('Reports & Features','Reports, interviews, features and credited contributions.'),'opinion':('Opinion & Analysis','Published columns, commentary and analysis.'),'thoughts':('Thoughts','Personal essays, reflections and field notes.')}
PATHS={'reporting':'reporting.html','opinion':'opinion.html','thoughts':'thoughts.html'}
ASSET_VERSION='17.0.1'

def meta_description(value,limit=190):
    value=clean(value)
    if len(value)<=limit:return value
    return value[:limit-1].rsplit(' ',1)[0].rstrip(' ,;:')+'…'

def text_body(value):
    result=[]
    for para in re.split(r'\n\s*\n',value.strip()):
        if para.startswith('## '): result.append('<h2>'+esc(para[3:])+'</h2>')
        elif para.startswith('### '): result.append('<h3>'+esc(para[4:])+'</h3>')
        elif para.startswith('> '): result.append('<blockquote><p>'+esc(para[2:])+'</p></blockquote>')
        else: result.append('<p>'+esc(para).replace('\n','<br>')+'</p>')
    return ''.join(result)

def safe_asset(path):
    path=str(path or '')
    return path if path.startswith('assets/') and '..' not in path.split('/') and '\\' not in path and not urlsplit(path).scheme else ''

def date_label(value):
    normal=date(value)
    if not normal:return 'Date not recorded'
    d=datetime.fromisoformat(normal);return f'{d.day} {d.strftime("%B %Y")}'

class Builder:
    def __init__(self):
        self.config=read(CONTENT/'settings.json',{})
        self.base=self.config.get('site_url','').rstrip('/')
        if urlsplit(self.base).scheme!='https': raise ValueError('Set a valid HTTPS site_url in content/settings.json.')
        self.routes=[]
        self.social_cards=SocialCardRenderer(SITE/'assets/social-preview-v2.jpg',OUT/'assets/social')
    def page(self,path,title,body,home=False,desc='',article_data=None,profile=False,social_image_path=''):
        prefix='../'*path.count('/')
        c=self.config; name=c.get('site_name',NAME); portrait=safe_asset(c.get('portrait'))
        sidebar_portrait='assets/portraits/contact.webp'
        email=c.get('email',''); linkedin=c.get('social',{}).get('linkedin','')
        socials=f'<a href="mailto:{esc(email)}">Email</a>' if email else ''
        if urlsplit(linkedin).scheme=='https':socials+=f'<a href="{esc(linkedin)}" rel="me noopener">LinkedIn</a>'
        nav_items=(('01','index.html','Portfolio'),('02','reporting.html','Reports & Features'),('03','opinion.html','Opinion & Analysis'),('04','thoughts.html','Thoughts'),('05','photography.html','Photography'),('06','about.html','About'),('07','contact.html','Contact'))
        menu=''.join(f'<a href="{prefix}{href}"><span>{number}</span>{label}</a>' for number,href,label in nav_items)
        same_as=[u for u in c.get('social',{}).values() if urlsplit(str(u)).scheme=='https']
        profile_url=self.base+'/about.html'
        person={'@context':'https://schema.org','@type':'Person','@id':profile_url+'#person','name':name,'givenName':'Arafat','familyName':'Rahaman','url':profile_url,'image':self.base+'/'+portrait,'description':c.get('description',''),'jobTitle':'Journalist','worksFor':{'@type':'Organization','name':c.get('organisation','The Daily Star'),'url':'https://www.thedailystar.net/'},'homeLocation':{'@type':'Place','name':c.get('location','Dhaka, Bangladesh')},'knowsAbout':c.get('areas',[]),'sameAs':same_as}
        if c.get('education'):person['alumniOf']={'@type':'CollegeOrUniversity','name':c['education'][0].get('institution','University of Rajshahi')}
        if c.get('membership'):person['memberOf']={'@type':'Organization','name':c['membership'].get('name','')}
        profile_person={key:value for key,value in person.items() if key!='@context'}
        metadata=article_data or ({'@context':'https://schema.org','@type':'ProfilePage','url':profile_url,'mainEntity':profile_person} if profile else person)
        schema=json.dumps(metadata,ensure_ascii=False).replace('<','\\u003c')
        page_key=re.sub(r'[^a-z0-9]+','-',path.lower()).strip('-')
        canonical_path='' if path=='index.html' else (path[:-10] if path.endswith('/index.html') else path)
        canonical_url=self.base+'/'+canonical_path
        description=meta_description(desc or c.get('description',''))
        social_image=self.base+'/'+(social_image_path or 'assets/social-preview-v2.jpg')
        measurement_id=str(c.get('analytics',{}).get('measurement_id','')).strip()
        analytics=''
        if re.fullmatch(r'G-[A-Z0-9]{6,16}',measurement_id):
            analytics=f'''<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{measurement_id}');</script>'''
        og_type='article' if article_data else 'website'
        article_tags=''
        if article_data:
            if article_data.get('datePublished'):article_tags+=f'<meta property="article:published_time" content="{esc(article_data["datePublished"])}">'
            if article_data.get('dateModified'):article_tags+=f'<meta property="article:modified_time" content="{esc(article_data["dateModified"])}">'
        document_title=f'{name} — Journalist at The Daily Star' if home else f'{title} — {name}'
        social_title=f'{name} — Journalist and Writer' if home else title
        head=f'''{analytics}<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{esc(document_title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#0b2f2a"><script>if(location.protocol==='http:'&&location.hostname==='arafatrahaman.com')location.replace('https://'+location.host+location.pathname+location.search+location.hash);try{{document.documentElement.dataset.theme=localStorage.getItem('portfolio-theme')||'light'}}catch(e){{document.documentElement.dataset.theme='light'}}</script><link rel="canonical" href="{esc(canonical_url)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" href="{prefix}feed.xml" title="Arafat Rahaman"><link rel="stylesheet" href="{prefix}portfolio.css?v={ASSET_VERSION}"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(name)}"><meta property="og:locale" content="en_GB"><meta property="og:title" content="{esc(social_title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical_url)}"><meta property="og:image" content="{esc(social_image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Arafat Rahaman, journalist at The Daily Star"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(social_title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{esc(social_image)}"><meta name="twitter:image:alt" content="Arafat Rahaman, journalist at The Daily Star">{article_tags}<script type="application/ld+json">{schema}</script>'''
        document=f'''<!doctype html><html lang="en"><head>{head}</head><body class="{'home' if home else 'inner'}" data-root="{prefix}" data-page="{page_key}" id="top"><a class="skip" href="#main">Skip to content</a><aside class="identity" aria-label="Profile and navigation"><a class="identityportrait" href="{prefix}index.html" aria-label="Arafat Rahaman homepage"><img class="portrait" src="{prefix}{esc(sidebar_portrait)}" width="112" height="112" alt="Arafat Rahaman smiling outdoors" decoding="async"></a><a class="name" href="{prefix}index.html">ARAFAT<br>RAHAMAN</a><p>Journalist at The Daily Star<br>Dhaka, Bangladesh</p><nav aria-label="Main navigation">{menu}</nav><div class="social">{socials}</div></aside><div class="right"><header class="mobilehead"><a class="mobilebrand" href="{prefix}index.html"><span class="mark" aria-hidden="true">A</span><span>Arafat Rahaman</span></a><div class="mobileactions"><button class="themetoggle" type="button" aria-pressed="false"><span class="themesymbol" aria-hidden="true">◐</span><span class="themelabel">Dark</span></button><button class="menutoggle" type="button" aria-expanded="false" aria-controls="mobile-menu"><span class="menulines" aria-hidden="true"><i></i><i></i></span><span>Menu</span></button></div></header><button class="menubackdrop" hidden aria-label="Close menu"></button><nav class="mobilemenu" id="mobile-menu" hidden aria-label="Mobile navigation"><div class="drawerhead"><strong>Navigation</strong><button class="drawerclose" type="button" aria-label="Close menu">×</button></div><div class="drawerprofile"><img src="{prefix}{esc(portrait)}" width="72" height="72" alt="Portrait of Arafat Rahaman"><div><h2>Arafat Rahaman</h2><p>Journalist · Dhaka</p></div></div><div class="drawernav">{menu}</div><div class="menumeta">{socials}</div></nav><main id="main">{body}</main><footer><span>© {datetime.now().year} {esc(name)}</span><span>Independent portfolio · Dhaka</span><a class="top" href="#top">Back to top ↑</a></footer></div><script src="{prefix}portfolio.js?v={ASSET_VERSION}" defer></script></body></html>'''
        target=OUT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(document,encoding='utf-8'); self.routes.append(path)
    def redirect(self,path,target):
        if path==target:return
        destination=self.base+'/'+target
        document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{esc(destination)}"><meta http-equiv="refresh" content="0;url={esc(destination)}"><title>Moved — Arafat Rahaman</title></head><body><p>This story has moved to a clearer address. <a href="{esc(destination)}">Continue to the article</a>.</p><script>location.replace({json.dumps(destination)}+location.search+location.hash)</script></body></html>'''
        target_path=OUT/path;target_path.parent.mkdir(parents=True,exist_ok=True);target_path.write_text(document,encoding='utf-8')
    def card(self,a):
        href=esc(a['local_url']); by=esc(a.get('source_name') or NAME)
        return f'<article class="workitem"><div class="workmeta"><span>{esc(date_label(a.get("date_published","")))}</span><span>{esc(a.get("category") or "Reporting")}</span><span>{by}</span></div><div class="workcopy"><h2><a href="{href}">{esc(a["title"])}</a></h2><p>{esc(a.get("excerpt",""))}</p></div><a class="read" href="{href}" aria-label="Read {esc(a["title"])}"><span>Read</span> →</a></article>'
    def story(self,a):
        path=a['local_url']+'index.html'; prefix='../'*path.count('/'); stream=a.get('stream','reporting'); section=PATHS.get(stream,'reporting.html')
        title=a['title']; original=a.get('original_authors') or ([] if a.get('source_url') else [NAME]); credit=', '.join(original) or 'Original byline not supplied by the source'
        byline='<strong>'+esc(credit)+'</strong>'
        if a.get('manual_import') and not a.get('verified_author'):byline+=f'<span>Portfolio contribution: {NAME} · {esc(a.get("contribution","Reporting"))}</span>'
        body=a.get('body_html') or text_body(a.get('body',''))
        body=sanitise(body,a.get('source_url',self.base+'/'))
        cover=safe_asset(a.get('cover_image')); figure=''
        if cover and not a.get('source_url'):figure=f'<figure class="cover"><img src="{prefix}{esc(cover)}" alt="{esc(a.get("cover_alt",""))}" decoding="async"><figcaption>{esc(a.get("cover_credit", ""))}</figcaption></figure>'
        source=''
        if a.get('source_url'):
            u=a['source_url']
            if urlsplit(u).scheme=='https':source=f'<div class="sourcebox">Originally published by {esc(a.get("source_name",""))}. <a href="{esc(u)}" rel="noopener noreferrer">Read the original publication</a>.<br>First archived: {esc(date_label(a.get("first_archived_at","")))}. This local copy does not depend on the source remaining online.</div>'
        update=f' · Updated {esc(date_label(a["date_modified"]))}' if a.get('date_modified') and a.get('date_modified')!=a.get('date_published') else ''
        share_dialog='''<dialog class="sharedialog" id="share-dialog" aria-labelledby="share-dialog-title"><div class="sharehead"><div><span>Share</span><h2 id="share-dialog-title">Share this story</h2></div><button type="button" data-close-share aria-label="Close sharing window">×</button></div><div class="sharegrid"><a href="#" data-share-service="facebook"><strong>Facebook</strong><span>Share in a new window ↗</span></a><a href="#" data-share-service="whatsapp"><strong>WhatsApp</strong><span>Send to a contact ↗</span></a><a href="#" data-share-service="x"><strong>X</strong><span>Post this story ↗</span></a><a href="#" data-share-service="linkedin"><strong>LinkedIn</strong><span>Share with your network ↗</span></a><button type="button" data-copy-share><strong>Copy link</strong><span>Copy the clean article address</span></button></div><p class="sharestatus" data-share-status role="status" aria-live="polite"></p></dialog>'''
        content=f'<article class="page reading"><a class="back" href="{prefix}{section}">← {esc(STREAMS.get(stream,STREAMS["reporting"])[0])}</a><div class="storylabel"><a href="{prefix}{section}?category={esc(a.get("category",""))}">{esc(a.get("category",""))}</a></div><h1>{esc(title)}</h1><p class="standfirst">{esc(a.get("excerpt",""))}</p><div class="byline"><img src="{prefix}{esc(safe_asset(self.config.get("portrait")))}" alt="" width="37" height="37" decoding="async"><div>{byline}<span class="meta">{esc(date_label(a.get("date_published","")))}{update}</span></div></div><div class="storyactions"><button type="button" data-share aria-haspopup="dialog">Share</button><button type="button" data-print>Print / Save PDF</button></div>{share_dialog}{figure}<div class="bodycopy">{body}</div>{source}</article>'
        profile_url=self.base+'/about.html'
        authors=[]
        for author in original:
            item={'@type':'Person','name':author}
            if clean(author).casefold()==clean(self.config.get('site_name',NAME)).casefold():
                item.update({'@id':profile_url+'#person','url':profile_url})
            authors.append(item)
        meta={'@context':'https://schema.org','@type':'Article','headline':title,'datePublished':a.get('date_published',''),'dateModified':a.get('date_modified','') or a.get('date_published',''),'author':authors,'url':self.base+'/'+a['local_url'],'mainEntityOfPage':self.base+'/'+a['local_url']}
        if a.get('source_url'):meta['isBasedOn']=a['source_url']
        social_image_path=self.social_cards.render(a)
        self.page(path,title,content,desc=a.get('excerpt',''),article_data=meta,social_image_path=social_image_path)

def build():
    OUT.mkdir(exist_ok=True)
    # Only regenerate the dedicated output tree, never the repository or content.
    for p in list(OUT.iterdir()):
        if p.is_dir():shutil.rmtree(p)
        else:p.unlink()
    shutil.copytree(SITE/'assets',OUT/'assets',ignore=shutil.ignore_patterns('photography-src','uploads','imported'))
    for file in ('portfolio.css','portfolio.js'):shutil.copy2(SITE/file,OUT/file)
    shutil.copytree(SITE/'admin',OUT/'admin')
    b=Builder(); c=b.config; overrides=read(CONTENT/'overrides.json',{'articles':{}})['articles']; articles=[]
    for path in sorted((CONTENT/'articles').glob('*.json')):
        a=read(path,{}); a.update(overrides.get(a['id'],{}));
        if a.get('status')=='published' and a.get('body_html') and date(a.get('date_published','')):articles.append(a)
    for a in read(CONTENT/'posts.json',{'posts':[]})['posts']:
        if a.get('status')!='published':continue
        if not a.get('title') or not date(a.get('date_published','')):raise ValueError('Published posts require a title and valid date.')
        if a.get('format')=='html':a['body_html']=sanitise(a.get('body',''))
        else:a['body_html']=text_body(a.get('body','')) if a.get('body') else sanitise(a.get('body_html',''))
        a.setdefault('local_url','thoughts/'+a['id']+'/'); a.setdefault('original_authors',[NAME]);articles.append(a)
    normalise_public_urls(articles)
    public_records=list(articles)
    # Some publisher URLs are near-identical editions of the same story. Keep
    # one public page per clean route while retaining every archived record.
    deduplicated={}
    def record_rank(item):
        source_number=re.search(r'(\d{5,})/?$',item.get('source_url',''))
        return (int(item.get('word_count') or 0),-int(source_number.group(1)) if source_number else 0)
    for item in articles:
        current=deduplicated.get(item['local_url'])
        if current is None or record_rank(item)>record_rank(current):deduplicated[item['local_url']]=item
    articles=list(deduplicated.values())
    articles.sort(key=lambda a:datetime.fromisoformat(date(a.get('date_published',''))).timestamp(),reverse=True)
    for a in articles:
        if not re.fullmatch(r'(stories|thoughts)/[a-zA-Z0-9_-]+/',a['local_url']): raise ValueError('Unsafe story path.')
        b.story(a)
    for a in public_records:
        for old in a.get('legacy_urls',[]):
            if re.fullmatch(r'(stories|thoughts)/[a-zA-Z0-9_-]+/',old) and old!=a['local_url']:
                b.redirect(old+'index.html',a['local_url'])
    keys=('id','title','excerpt','category','stream','date_published','date_modified','cover_image','cover_alt','source_name','local_url')
    write(OUT/'data/index.json',{'articles':[{k:a.get(k,'') for k in keys} for a in articles]})
    home_profile='<section class="homeprofile" aria-labelledby="home-profile-title"><img src="assets/portraits/contact.webp" alt="Arafat Rahaman smiling outdoors" width="430" height="520"><div><span>Journalist · Dhaka</span><h2 id="home-profile-title">Arafat Rahaman</h2><p>Reporting on education, governance, rights, social policy and public accountability.</p></div></section>'
    chosen=[]
    for wanted in ('reporting','opinion','thoughts','reporting'):
        item=next((a for a in articles if a.get('stream')==wanted and a not in chosen),None)
        if item:chosen.append(item)
    for item in articles:
        if len(chosen)>=4:break
        if item not in chosen:chosen.append(item)
    def home_story(a):
        return f'<article class="homework"><div class="homework-meta"><span>{esc(a.get("category") or STREAMS.get(a.get("stream"),STREAMS["reporting"])[0])}</span><time datetime="{esc(date(a.get("date_published","")))}">{esc(date_label(a.get("date_published","")))}</time></div><h2><a href="{esc(a["local_url"])}">{esc(a["title"])}</a></h2><p>{esc(a.get("excerpt",""))}</p><a class="homework-read" href="{esc(a["local_url"])}" aria-label="Read {esc(a["title"])}">Read story <span>→</span></a></article>'
    recent='<section class="recentwork" aria-labelledby="recent-work-title"><header><div><span class="eyebrow">Selected work</span><h1 id="recent-work-title">Latest journalism</h1></div><p>Reporting, analysis and personal writing from Bangladesh.</p></header><div class="recentgrid">'+''.join(home_story(a) for a in chosen)+'</div></section>'
    b.page('index.html','Arafat Rahaman','<section class="homecontent">'+home_profile+recent+'</section>',home=True)
    for stream,(title,description) in STREAMS.items():
        subset=[a for a in articles if a.get('stream')==stream]
        cards=''.join(b.card(a) for a in subset[:12]) or '<p class="empty">No entries published here yet.</p>'
        content=f'<section class="page archivepage" data-archive="{stream}"><header class="pageintro"><div><span class="eyebrow">Published work</span><h1>{title}</h1><p>{description}</p></div><div class="archive-total"><strong>{len(subset)}</strong><span>published pieces</span></div></header><button class="filtertoggle" type="button" aria-expanded="false" aria-controls="archive-filters">Search & filters</button><form class="tools" id="archive-filters" role="search"><label>Search<input type="search" name="q" placeholder="Search {title.lower()}" autocomplete="off"></label><label>Category<select name="category"><option value="">All categories</option></select></label><label>Year<select name="year"><option value="">All years</option></select></label></form><div class="count" role="status">{len(subset)} entries</div><div class="work-list">{cards}</div><nav class="pagination" aria-label="Results pages"><button data-prev disabled>Previous</button><span data-page>Page 1</span><button data-next>Next</button></nav><noscript><p>Enable JavaScript for search and filters. <a href="all-work.html">Read the complete text index</a>.</p></noscript></section>'
        b.page(PATHS[stream],title,content,desc=description)
    all_links=''.join(f'<li><a href="{esc(a["local_url"])}">{esc(a["title"])}</a> · {esc(date_label(a.get("date_published","")))}</li>' for a in articles)
    b.page('all-work.html','Complete index','<section class="page"><h1>Complete index</h1><ul>'+all_links+'</ul></section>')
    photos=[p for p in read(CONTENT/'photos.json',{'photos':[]})['photos'] if p.get('status','published')=='published']
    # Do not publish a draft's uploaded cover just because it exists in source.
    used={safe_asset(a.get('cover_image')) for a in articles if not a.get('source_url')}
    used.update(safe_asset(p.get('src')) for p in photos)
    used.update(safe_asset(p) for p in c.get('home_images',[]))
    used.add(safe_asset(c.get('portrait')))
    for asset in used:
        if asset and (SITE/asset).is_file():
            target=OUT/asset;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SITE/asset,target)
    gallery=''
    for index,p in enumerate(photos):
        src=safe_asset(p.get('src')); alt=p.get('alt') or p.get('caption','')
        if not src:continue
        loading='eager' if index<4 else 'lazy'
        gallery+=f'<figure data-photo-item><button data-photo="{esc(src)}" data-caption="{esc(p.get("caption",""))}" data-location="{esc(p.get("location",""))}" aria-label="Open photograph: {esc(alt)}"><img src="{esc(src)}" alt="{esc(alt)}" loading="{loading}" decoding="async"></button><figcaption><strong>{esc(p.get("caption",""))}</strong><small>{esc(p.get("location",""))}</small></figcaption></figure>'
    flickr=c.get('social',{}).get('flickr','')
    photo_intro=f'<header class="photohero"><div><span class="eyebrow">Visual journalism & observations</span><h1>Photography</h1><p>People, public spaces and everyday life, photographed across Bangladesh.</p></div><div class="photoindex"><strong>{len(photos):02d}</strong><span>photographs</span></div></header><div class="photobar"><p>A visual notebook by Arafat Rahaman.</p><a href="{esc(flickr)}" rel="me noopener">See more on Flickr ↗</a></div>'
    photo_dialog='<dialog id="photo-dialog" class="photodialog"><div class="photodialog-bar"><button data-prev-photo aria-label="Previous photograph">←</button><p><strong data-dialog-caption></strong><span data-dialog-location></span></p><button data-next-photo aria-label="Next photograph">→</button><button data-close-photo aria-label="Close photograph">×</button></div><img alt=""></dialog>'
    b.page('photography.html','Photography','<section class="page photopage">'+photo_intro+'<div class="photogrid">'+(gallery or '<p>No photographs published yet.</p>')+'</div>'+photo_dialog+'</section>')
    bio=c.get('biography') or 'I am a journalist at The Daily Star, reporting on education, governance, rights, social policy and public accountability.\n\nThis space brings together my published journalism, personal writing and photography.'
    areas=''.join(f'<li>{esc(x)}</li>' for x in c.get('areas',[]))
    career=''.join(f'<li><span>{esc(x.get("years",""))}</span><div><h3>{esc(x.get("role",""))}</h3><p>{esc(x.get("organisation",""))} · {esc(x.get("location",""))}</p></div></li>' for x in c.get('career',[]))
    education=''.join(f'<li><span>{esc(x.get("year",""))}</span><div><h3>{esc(x.get("degree",""))}</h3><p>{esc(x.get("subject",""))}<br>{esc(x.get("institution",""))}</p></div></li>' for x in c.get('education',[]))
    membership=c.get('membership',{})
    member=f'<aside class="membership"><span class="eyebrow">Professional network</span><div><strong>{esc(membership.get("name",""))}</strong><p>{esc(membership.get("detail",""))} · Since {esc(membership.get("since",""))}</p></div></aside>' if membership.get('name') else ''
    awards=''.join(f'<li><span class="awardyear">{esc(a.get("year",""))}</span><div><h3>{esc(a.get("title",""))}</h3><p>{esc(a.get("organisation",""))}</p></div></li>' for a in c.get('recognition',[]))
    facts='<div class="aboutfacts"><div><strong>Since 2017</strong><span>Reporting for The Daily Star</span></div><div><strong>300+</strong><span>Published stories</span></div><div><strong>Dhaka</strong><span>Reporting across Bangladesh</span></div></div>'
    details=f'<section class="profiledetails"><div><span class="eyebrow">Experience</span><h2>Newsroom work</h2><ol>{career}</ol></div><div><span class="eyebrow">Education</span><h2>Academic foundation</h2><ol>{education}</ol></div></section>'
    about=f'<section class="page aboutpage"><header class="pageintro"><div><span class="eyebrow">Profile</span><h1>About Arafat</h1><p>Public-interest journalism shaped by field reporting, evidence and accountability.</p></div></header><div class="aboutlead"><figure><img src="{esc(safe_asset(c.get("portrait")))}" alt="Arafat Rahaman" decoding="async"></figure><div class="biocopy"><span class="eyebrow">Arafat Rahaman</span>{text_body(bio)}<a class="textlink" href="contact.html">Get in touch →</a></div></div>{facts}<section class="coverage"><div><span class="eyebrow">Reporting areas</span><h2>What I cover</h2></div><ul>{areas}</ul></section>{details}{member}<section class="recognition" id="recognition"><header><span class="eyebrow">Recognition</span><h2>Awards & fellowships</h2></header><ol>{awards}</ol></section></section>'
    b.page('about.html','About',about,profile=True)
    b.page('contact.html','Contact',f'<section class="page contactpage"><header class="pageintro"><div><span class="eyebrow">Contact</span><h1>Start a conversation</h1><p>For reporting enquiries, story leads and professional correspondence.</p></div></header><div class="contactgrid"><a href="mailto:{esc(c.get("email",""))}"><span>Email</span><strong>{esc(c.get("email",""))}</strong><i>Write to me →</i></a><a href="{esc(c.get("social",{}).get("linkedin",""))}" rel="me noopener"><span>LinkedIn</span><strong>Arafat Rahaman</strong><i>View profile ↗</i></a><div><span>Based in</span><strong>Dhaka, Bangladesh</strong><i>Reporting across Bangladesh</i></div></div></section>')
    for path,target in {'published-work.html':'reporting.html','archive.html':'reporting.html','daily-star.html':'reporting.html','journal.html':'thoughts.html','awards.html':'about.html#recognition'}.items():
        (OUT/path).write_text(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><title>Moved</title><a href="{target}">Continue</a>',encoding='utf-8')
    b.page('404.html','Page not found','<section class="page"><h1>Page not found</h1><p>This address may have changed.</p><a href="'+esc(b.base)+'/">Return to the portfolio</a></section>')
    write(OUT/'data/site.json',{'publishing':c.get('publishing',{}),'site_url':b.base})
    state=read(CONTENT/'sync-state.json',{})
    write(OUT/'data/sync.json',{k:state.get(k) for k in ('last_completed','last_discovery_success','saved_this_run','known_sources','pending')})
    def sitemap_url(path):
        route='' if path=='index.html' else (path[:-10] if path.endswith('/index.html') else path)
        return b.base+'/'+route
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(sitemap_url(p))+'</loc></url>' for p in b.routes if p!='404.html')+'</urlset>',encoding='utf-8')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: '+urlsplit(b.base).path+'/admin/\nSitemap: '+b.base+'/sitemap.xml\n',encoding='utf-8')
    items=''.join('<item><title>'+esc(a['title'])+'</title><link>'+esc(b.base+'/'+a['local_url'])+'</link><guid>'+esc(b.base+'/'+a['local_url'])+'</guid><description>'+esc(a.get('excerpt',''))+'</description></item>' for a in articles[:50])
    (OUT/'feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Arafat Rahaman</title><link>'+esc(b.base)+'</link><description>Reporting, opinion and thoughts</description>'+items+'</channel></rss>',encoding='utf-8')
    (OUT/'CNAME').write_text('arafatrahaman.com\n',encoding='utf-8')
    (OUT/'.nojekyll').touch()
    print(f'Built {len(b.routes)} pages, {len(articles)} published articles, {len(photos)} photographs. Drafts excluded.')
if __name__=='__main__':build()
