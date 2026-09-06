"""Build public pages from durable content; drafts never enter dist."""
import json, re, shutil
from datetime import datetime
from urllib.parse import urlsplit
from core import *

STREAMS={'reporting':('Reporting','News reports, interviews and reported features.'),'opinion':('Opinion & Analysis','Published columns, commentary and analysis.'),'thoughts':('Thoughts','Personal essays, reflections and field notes.')}
PATHS={'reporting':'reporting.html','opinion':'opinion.html','thoughts':'thoughts.html'}

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
    def page(self,path,title,body,home=False,desc='',article_data=None):
        prefix='../'*path.count('/')
        c=self.config; name=c.get('site_name',NAME); portrait=safe_asset(c.get('portrait'))
        email=c.get('email',''); linkedin=c.get('social',{}).get('linkedin','')
        socials=f'<a href="mailto:{esc(email)}">Email</a>' if email else ''
        if urlsplit(linkedin).scheme=='https':socials+=f'<a href="{esc(linkedin)}" rel="me noopener">LinkedIn</a>'
        menu=''.join(f'<a href="{prefix}{v}">{esc(STREAMS[k][0])}</a>' for k,v in PATHS.items())
        menu+=f'<a href="{prefix}photography.html">Photography</a><a href="{prefix}awards.html">Awards</a><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a>'
        metadata=article_data or {'@context':'https://schema.org','@type':'Person','name':name,'url':self.base+'/','jobTitle':'Journalist'}
        schema=json.dumps(metadata,ensure_ascii=False).replace('<','\\u003c')
        document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} — {esc(name)}</title><meta name="description" content="{esc(desc or c.get('description',''))}"><meta name="theme-color" content="#454545"><link rel="canonical" href="{esc(self.base+'/'+path)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" href="{prefix}feed.xml" title="Arafat Rahaman"><link rel="stylesheet" href="{prefix}portfolio.css"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc or c.get('description',''))}"><meta property="og:url" content="{esc(self.base+'/'+path)}"><script type="application/ld+json">{schema}</script></head><body class="{'home' if home else 'inner'}" data-root="{prefix}" id="top"><a class="skip" href="#main">Skip to content</a><aside class="identity" aria-label="Profile and navigation"><a href="{prefix}index.html" aria-label="Arafat Rahaman homepage"><img class="portrait" src="{prefix}{esc(portrait)}" width="148" height="148" alt="Arafat Rahaman"></a><div class="social">{socials}</div><a class="name" href="{prefix}index.html">ARAFAT<br>RAHAMAN</a><p>Journalist at The Daily Star<br>Dhaka, Bangladesh</p><nav aria-label="Main navigation"><a href="{prefix}index.html">Portfolio</a><a href="{prefix}about.html">About me</a><a href="{prefix}contact.html">Contact</a></nav></aside><div class="right"><header class="mobilehead"><a class="mobilebrand" href="{prefix}index.html"><span class="mark" aria-hidden="true">A</span>Arafat Rahaman</a><button class="menutoggle" aria-expanded="false" aria-controls="mobile-menu">☰ Menu</button></header><nav class="mobilemenu" id="mobile-menu" hidden aria-label="Mobile navigation">{menu}<div class="menumeta">{socials}</div></nav><main id="main">{body}</main><footer><span>© {datetime.now().year} {esc(name)}</span><span>Dhaka, Bangladesh</span><a class="top" href="#top">Back to top ↑</a></footer></div><script src="{prefix}portfolio.js" defer></script></body></html>'''
        target=OUT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(document,encoding='utf-8'); self.routes.append(path)
    def card(self,a):
        image=safe_asset(a.get('cover_image')); src=f'<img class="cardimage" src="{esc(image)}" loading="lazy" alt="{esc(a.get("cover_alt",""))}">' if image else ''
        href=esc(a['local_url']); by=esc(a.get('source_name') or NAME)
        return f'<article class="card">{src}<div class="copy"><div class="meta">{by} · {esc(date_label(a.get("date_published","")))}</div><h2><a href="{href}">{esc(a["title"])}</a></h2><p>{esc(a.get("excerpt",""))}</p><a class="read" href="{href}">Read story →</a></div></article>'
    def story(self,a):
        path=a['local_url']+'index.html'; prefix='../'*path.count('/'); stream=a.get('stream','reporting'); section=PATHS.get(stream,'reporting.html')
        title=a['title']; original=a.get('original_authors') or ([] if a.get('source_url') else [NAME]); credit=', '.join(original) or 'Original byline not supplied by the source'
        byline='<strong>'+esc(credit)+'</strong>'
        if a.get('manual_import') and not a.get('verified_author'):byline+=f'<span>Portfolio contribution: {NAME} · {esc(a.get("contribution","Reporting"))}</span>'
        body=a.get('body_html') or text_body(a.get('body',''))
        body=sanitise(body,a.get('source_url',self.base+'/'))
        cover=safe_asset(a.get('cover_image')); figure=''
        if cover:figure=f'<figure class="cover"><img src="{prefix}{esc(cover)}" alt="{esc(a.get("cover_alt",""))}"><figcaption>{esc(a.get("cover_credit") or ("Image from the original publication" if a.get("source_image") else ""))}</figcaption></figure>'
        source=''
        if a.get('source_url'):
            u=a['source_url']
            if urlsplit(u).scheme=='https':source=f'<div class="sourcebox">Originally published by {esc(a.get("source_name",""))}. <a href="{esc(u)}" rel="noopener noreferrer">Read the original publication</a>.<br>First archived: {esc(date_label(a.get("first_archived_at","")))}. This local copy does not depend on the source remaining online.</div>'
        update=f' · Updated {esc(date_label(a["date_modified"]))}' if a.get('date_modified') and a.get('date_modified')!=a.get('date_published') else ''
        content=f'<article class="page reading"><a class="back" href="{prefix}{section}">← {esc(STREAMS.get(stream,STREAMS["reporting"])[0])}</a><div class="meta"><a href="{prefix}{section}?category={esc(a.get("category",""))}">{esc(a.get("category",""))}</a></div><h1>{esc(title)}</h1><p class="standfirst">{esc(a.get("excerpt",""))}</p><div class="byline"><img src="{prefix}{esc(safe_asset(self.config.get("portrait")))}" alt="" width="37" height="37"><div>{byline}<span class="meta">{esc(date_label(a.get("date_published","")))}{update}</span></div></div><div class="storyactions"><button data-share>Share</button><button data-print>Print / Save PDF</button><span data-share-status role="status"></span></div>{figure}<div class="bodycopy">{body}</div>{source}</article>'
        meta={'@context':'https://schema.org','@type':'Article','headline':title,'datePublished':a.get('date_published',''),'author':[{'@type':'Person','name':x} for x in original],'url':self.base+'/'+a['local_url']}
        if a.get('source_url'):meta['isBasedOn']=a['source_url']
        self.page(path,title,content,desc=a.get('excerpt',''),article_data=meta)

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
    articles.sort(key=lambda a:datetime.fromisoformat(date(a.get('date_published',''))).timestamp(),reverse=True)
    for a in articles:
        if not re.fullmatch(r'(stories|thoughts)/[a-zA-Z0-9_-]+/',a['local_url']): raise ValueError('Unsafe story path.')
        b.story(a)
    keys=('id','title','excerpt','category','stream','date_published','date_modified','cover_image','cover_alt','source_name','local_url')
    write(OUT/'data/index.json',{'articles':[{k:a.get(k,'') for k in keys} for a in articles]})
    tiles=[]
    destinations=[('reporting','Reporting','News reports, interviews and reported features'),('opinion','Opinion & Analysis','Published columns, commentary and analysis'),('thoughts','Thoughts','Personal essays, reflections and field notes'),('photos','Photography','People, places and everyday observations')]
    for i,(key,title,desc) in enumerate(destinations):
        src=safe_asset(c['home_images'][i]); href=PATHS.get(key,'photography.html')
        tiles.append(f'<a class="tile" href="{href}"><img src="{esc(src)}" alt="" width="640" height="420"><span><strong>{esc(title)}</strong><small>{esc(desc)}</small></span></a>')
    b.page('index.html','Portfolio','<section class="homecontent"><h1>Portfolio</h1><div class="tiles">'+''.join(tiles)+'</div></section>',home=True)
    for stream,(title,description) in STREAMS.items():
        subset=[a for a in articles if a.get('stream')==stream]
        cards=''.join(b.card(a) for a in subset[:12]) or '<p class="empty">No entries published here yet.</p>'
        content=f'<section class="page" data-archive="{stream}"><h1>{title}</h1><p>{description}</p><form class="tools" role="search"><label>Search<input type="search" name="q" placeholder="Search {title.lower()}" autocomplete="off"></label><label>Category<select name="category"><option value="">All categories</option></select></label><label>Year<select name="year"><option value="">All years</option></select></label></form><div class="count" role="status">{len(subset)} entries</div><div class="cards">{cards}</div><nav class="pagination" aria-label="Results pages"><button data-prev disabled>Previous</button><span data-page>Page 1</span><button data-next>Next</button></nav><noscript><p>Enable JavaScript for search and filters. <a href="all-work.html">Read the complete text index</a>.</p></noscript></section>'
        b.page(PATHS[stream],title,content,desc=description)
    all_links=''.join(f'<li><a href="{esc(a["local_url"])}">{esc(a["title"])}</a> · {esc(date_label(a.get("date_published","")))}</li>' for a in articles)
    b.page('all-work.html','Complete index','<section class="page"><h1>Complete index</h1><ul>'+all_links+'</ul></section>')
    photos=[p for p in read(CONTENT/'photos.json',{'photos':[]})['photos'] if p.get('status','published')=='published']
    # Do not publish a draft's uploaded cover just because it exists in source.
    used={safe_asset(a.get('cover_image')) for a in articles}
    used.update(safe_asset(p.get('src')) for p in photos)
    used.update(safe_asset(p) for p in c.get('home_images',[]))
    used.add(safe_asset(c.get('portrait')))
    for asset in used:
        if asset and (SITE/asset).is_file():
            target=OUT/asset;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SITE/asset,target)
    gallery=''
    for p in photos:
        src=safe_asset(p.get('src')); alt=p.get('alt') or p.get('caption','')
        if not src:continue
        gallery+=f'<figure><button data-photo="{esc(src)}" aria-label="Open photograph: {esc(alt)}"><img src="{esc(src)}" alt="{esc(alt)}" loading="lazy"></button><figcaption>{esc(p.get("caption",""))}<small>{esc(p.get("location",""))}</small></figcaption></figure>'
    b.page('photography.html','Photography','<section class="page"><h1>Photography</h1><p>People, places and everyday observations.</p><div class="photogrid">'+(gallery or '<p>No photographs published yet.</p>')+'</div><dialog id="photo-dialog"><button data-close-photo>Close photograph ×</button><img alt=""></dialog></section>')
    bio=c.get('biography') or 'I am a journalist at The Daily Star, reporting on education, governance, rights, social policy and public accountability.\n\nThis space brings together my published journalism, personal writing and photography.'
    b.page('about.html','About',f'<section class="page"><h1>About</h1><div class="bio"><img src="{esc(safe_asset(c.get("portrait")))}" alt="Arafat Rahaman"><div><h2>Arafat Rahaman</h2>{text_body(bio)}<p><a href="awards.html">Awards & recognition</a></p><p><a href="contact.html">Get in touch</a></p></div></div></section>')
    awards=''.join(f'<li><span class="meta">{esc(a.get("year",""))}</span><h2>{esc(a.get("title",""))}</h2><p>{esc(a.get("organisation",""))}</p></li>' for a in c.get('recognition',[]))
    b.page('awards.html','Awards & recognition','<section class="page"><h1>Awards & recognition</h1><ul class="recognition">'+awards+'</ul></section>')
    b.page('contact.html','Contact',f'<section class="page"><h1>Contact</h1><p>For reporting enquiries, story leads and professional correspondence.</p><div class="contactrow"><h2>Email</h2><a href="mailto:{esc(c.get("email",""))}">{esc(c.get("email",""))}</a></div><div class="contactrow"><h2>LinkedIn</h2><a href="{esc(c.get("social",{}).get("linkedin",""))}" rel="me noopener">Arafat Rahaman on LinkedIn</a></div></section>')
    for path,target in {'published-work.html':'reporting.html','archive.html':'reporting.html','daily-star.html':'reporting.html','journal.html':'thoughts.html'}.items():
        (OUT/path).write_text(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><title>Moved</title><a href="{target}">Continue</a>',encoding='utf-8')
    b.page('404.html','Page not found','<section class="page"><h1>Page not found</h1><p>This address may have changed.</p><a href="'+esc(b.base)+'/">Return to the portfolio</a></section>')
    write(OUT/'data/site.json',{'publishing':c.get('publishing',{}),'site_url':b.base})
    state=read(CONTENT/'sync-state.json',{})
    write(OUT/'data/sync.json',{k:state.get(k) for k in ('last_completed','last_discovery_success','saved_this_run','known_sources','pending')})
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(b.base+'/'+p)+'</loc></url>' for p in b.routes if p!='404.html')+'</urlset>',encoding='utf-8')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: '+urlsplit(b.base).path+'/admin/\nSitemap: '+b.base+'/sitemap.xml\n',encoding='utf-8')
    items=''.join('<item><title>'+esc(a['title'])+'</title><link>'+esc(b.base+'/'+a['local_url'])+'</link><guid>'+esc(b.base+'/'+a['local_url'])+'</guid><description>'+esc(a.get('excerpt',''))+'</description></item>' for a in articles[:50])
    (OUT/'feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Arafat Rahaman</title><link>'+esc(b.base)+'</link><description>Reporting, opinion and thoughts</description>'+items+'</channel></rss>',encoding='utf-8')
    (OUT/'.nojekyll').touch()
    print(f'Built {len(b.routes)} pages, {len(articles)} published articles, {len(photos)} photographs. Drafts excluded.')
if __name__=='__main__':build()
