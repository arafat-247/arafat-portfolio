"""Small, dependency-free content and HTTP utilities."""
import hashlib, html, ipaddress, json, re, socket, time
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
SITE = ROOT / 'site'
OUT = ROOT / 'dist'
NAME = 'Arafat Rahaman'
AUTHOR = 'https://www.thedailystar.net/author/arafat-rahaman'
UA = 'ArafatPortfolio/17.1 (+https://arafatrahaman.com/contact/)'

def now(): return datetime.now(timezone.utc).isoformat()
def read(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)
def clean(value): return re.sub(r'\s+', ' ', str(value or '')).strip()
def esc(value): return html.escape(str(value or ''), quote=True)
def identity(url): return hashlib.sha256(canonical(url).encode()).hexdigest()[:20]
def slug(value):
    result=re.sub(r'[^a-z0-9]+','-',value.lower()).strip('-')
    if len(result)>75:result=result[:75].rsplit('-',1)[0]
    return result or 'story'
STORY_PATH=re.compile(r'^(stories|thoughts)/[a-zA-Z0-9_-]+/$')

def normalise_public_urls(records):
    """Replace legacy ID-led paths with stable headline paths in place.

    Exact title/date duplicates intentionally share one public route; the build
    keeps the strongest archived copy and redirects every legacy address.
    """
    pending=[]; reserved={}
    for item in records:
        section='thoughts' if item.get('stream')=='thoughts' else 'stories'
        current=str(item.get('local_url') or '')
        ident=str(item.get('id') or '')
        part=current.rstrip('/').split('/')[-1] if current else ''
        legacy=not STORY_PATH.fullmatch(current) or part==ident or (ident and part.startswith(ident+'-'))
        if legacy:
            pending.append((item,section,slug(item.get('title','story'))))
        else:
            reserved.setdefault(current,[]).append(item)

    groups={}
    for item,section,base in pending:
        groups.setdefault((section,base),[]).append(item)

    for (section,base),items in sorted(groups.items()):
        by_day={}
        for item in items:
            by_day.setdefault(date(item.get('date_published',''))[:10],[]).append(item)
        multiple_days=len(by_day)>1
        for day,day_items in sorted(by_day.items()):
            stem=base
            if multiple_days:
                year=day[:4]
                stem+=('-'+year) if year and sum(1 for key in by_day if key.startswith(year))==1 else ('-'+day if day else '')
            candidate=f'{section}/{stem}/'
            owners=reserved.get(candidate,[])
            same_story=owners and all(slug(x.get('title',''))==base and date(x.get('date_published',''))[:10]==day for x in owners)
            if owners and not same_story:
                token=day or str(day_items[0].get('id',''))[:8]
                candidate=f'{section}/{stem}-{token}/'
            reserved.setdefault(candidate,[]).extend(day_items)
            for item in day_items:
                old=str(item.get('local_url') or '')
                if old and old!=candidate and STORY_PATH.fullmatch(old):
                    item['legacy_urls']=list(dict.fromkeys([*item.get('legacy_urls',[]),old]))
                item['local_url']=candidate
    return records
def canonical(url):
    p = urlsplit(url)
    # Preserve meaningful query parameters; only remove common trackers.
    from urllib.parse import parse_qsl, urlencode
    query = urlencode([(k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith('utm_') and k not in ('fbclid','gclid')])
    host = (p.hostname or '').lower()
    if host == 'thedailystar.net': host = 'www.thedailystar.net'
    return urlunsplit((p.scheme.lower(), host, p.path or '/', query, ''))

def public_url(url):
    p = urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password or p.port not in (None,443):
        raise ValueError('Use a public HTTPS URL without credentials or a custom port.')
    if p.hostname.lower() == 'localhost' or p.hostname.lower().endswith(('.local','.internal')):
        raise ValueError('Private network URLs are not allowed.')
    # Fixed trusted publisher hosts can use the environment's configured HTTPS
    # proxy, which may resolve names remotely. Arbitrary pasted hosts must pass
    # local public-address checks; redirects are checked with the same rules.
    if p.hostname.lower() in {'www.thedailystar.net','thedailystar.net','tds-images.thedailystar.net'}:
        return url
    answers = socket.getaddrinfo(p.hostname,443,type=socket.SOCK_STREAM)
    if not answers or any(not ipaddress.ip_address(a[4][0]).is_global for a in answers):
        raise ValueError('URL does not resolve exclusively to public addresses.')
    return url

class Redirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch(url, limit=5_000_000):
    public_url(url)
    req = Request(url,headers={'User-Agent':UA,'Accept':'text/html,application/xhtml+xml,image/*;q=0.5'})
    with build_opener(Redirects()).open(req,timeout=25) as response:
        data = response.read(limit+1)
        if len(data)>limit: raise ValueError('Response exceeds the import size limit.')
        return data, response.headers.get_content_type(), response.geturl()

def date(value):
    value=clean(value)
    if not value: return ''
    try: dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:
        try: dt=parsedate_to_datetime(value)
        except (ValueError,TypeError):
            dt=None
            for fmt in ('%d %B %Y','%d %b %Y','%B %d, %Y','%b %d, %Y'):
                try: dt=datetime.strptime(value,fmt); break
                except ValueError: pass
            if dt is None: return ''
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone(timedelta(hours=6)))
    return dt.isoformat()

class Node:
    def __init__(self,tag='',attrs=None,parent=None):
        self.tag=tag; self.attrs=dict(attrs or []); self.children=[]; self.parent=parent
    def walk(self):
        yield self
        for n in self.children:
            if isinstance(n,Node): yield from n.walk()
    def text(self): return clean(' '.join(n.text() if isinstance(n,Node) else n for n in self.children))
    def rawtext(self): return ''.join(n.rawtext() if isinstance(n,Node) else n for n in self.children)
    def render(self):
        if not self.tag: return ''.join(n.render() if isinstance(n,Node) else esc(n) for n in self.children)
        attrs=''.join(f' {k}="{esc(v)}"' for k,v in self.attrs.items() if v is not None)
        return '<'+self.tag+attrs+'>'+''.join(n.render() if isinstance(n,Node) else esc(n) for n in self.children)+'</'+self.tag+'>'

class Document(HTMLParser):
    VOID={'img','meta','link','br','hr','input','source','wbr','area','base','embed','param','track','col'}
    def __init__(self,source):
        super().__init__(convert_charrefs=True); self.root=Node(); self.stack=[self.root]; self.feed(source)
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs,self.stack[-1]); self.stack[-1].children.append(n)
        if tag not in self.VOID: self.stack.append(n)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in self.VOID: self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag: del self.stack[i:]; break
    def handle_data(self,value): self.stack[-1].children.append(value)
    def nodes(self,tag): return [n for n in self.root.walk() if n.tag==tag]
    def meta(self,key):
        return next((n.attrs.get('content','') for n in self.nodes('meta') if n.attrs.get('property',n.attrs.get('name','')).lower()==key.lower()),'')

SAFE={'p','h2','h3','h4','blockquote','ul','ol','li','strong','b','em','i','a','br','table','thead','tbody','tr','th','td','caption','figure','figcaption'}
DROP={'script','style','iframe','object','embed','form','input','button','svg','math','video','audio','noscript','template','nav','aside'}
def sanitise(source, base=''):
    def render(n):
        if not isinstance(n,Node): return esc(n)
        if n.tag in DROP: return ''
        inner=''.join(render(x) for x in n.children)
        if n.tag not in SAFE: return inner
        attrs=''
        if n.tag=='a':
            u=urljoin(base,n.attrs.get('href',''))
            if urlsplit(u).scheme in ('http','https','mailto'): attrs=f' href="{esc(u)}" rel="noopener noreferrer"'
        if n.tag=='br': return '<br>'
        return f'<{n.tag}{attrs}>{inner}</{n.tag}>'
    return render(Document(source).root).strip()

def objects(value):
    if isinstance(value,dict):
        yield value
        for item in value.values(): yield from objects(item)
    elif isinstance(value,list):
        for item in value: yield from objects(item)

def article(source,url,manual=False,author_listing=False):
    doc=Document(source); candidates=[]; embedded=[]
    for n in doc.nodes('script'):
        if n.attrs.get('type') not in ('application/ld+json','application/json'): continue
        try: data=json.loads(n.rawtext())
        except (ValueError,TypeError): continue
        embedded.append(data)
        if n.attrs.get('type')!='application/ld+json': continue
        for obj in objects(data):
            typ=obj.get('@type',[]); typ=typ if isinstance(typ,list) else [typ]
            if any(t in ('Article','NewsArticle','ReportageNewsArticle','BlogPosting','OpinionNewsArticle') for t in typ): candidates.append(obj)
    def matches(obj):
        values=[obj.get('url'),obj.get('@id'),obj.get('mainEntityOfPage')]
        return any(canonical(v.get('@id','') if isinstance(v,dict) else v)==canonical(url) for v in values if isinstance(v,(str,dict)))
    ld=next((x for x in candidates if matches(x)), candidates[0] if len(candidates)==1 else {})
    title=clean(ld.get('headline') or doc.meta('og:title') or next((n.text() for n in doc.nodes('h1')),''))
    title=re.sub(r'\s*\|\s*The Daily Star\s*$','',title,flags=re.I)
    names=ld.get('author',[]); names=names if isinstance(names,list) else [names]
    authors=[clean(a.get('name','') if isinstance(a,dict) else a) for a in names]; authors=[x for x in authors if x]
    if not authors:
        authors=[n.text() for n in doc.root.walk() if n.attrs.get('rel')=='author' or re.search(r'(^|\s)(byline|author-name)(\s|$)',n.attrs.get('class',''))]
        authors=[a for a in authors if a and len(a)<180]
    verified=any(NAME.casefold()==a.casefold() or NAME.casefold() in [x.strip().casefold() for x in re.split(r',| and | & ',a)] for a in authors)
    if not verified and not manual and not author_listing: raise ValueError('Author not verified; retained in the discovery log, not published.')
    if not title: raise ValueError('Article title could not be extracted.')
    if ld.get('isAccessibleForFree') in (False,'False','false'): raise ValueError('Source marks this article as restricted. Add authorised text manually.')
    body=ld.get('articleBody','')
    if isinstance(body,str) and len(clean(body))>=180:
        body=''.join('<p>'+esc(p.strip())+'</p>' for p in re.split(r'\n\s*\n|\n',body) if p.strip())
    else:
        ranked=[]
        for n in doc.root.walk():
            marker=(n.attrs.get('class','')+' '+n.attrs.get('id','')).lower()
            exact=bool(re.search(r'article[-_ ]?(body|content)|story[-_ ]?(body|content)|field--name-body|section-content|block-field-blocknode[a-z]*body',marker))
            if not exact and n.tag not in ('article','main'): continue
            parts=[]
            for p in n.walk():
                if p.tag not in ('p','h2','h3','blockquote','ul','ol','table'): continue
                ancestors=[]; a=p.parent
                while a and a is not n: ancestors.append(a); a=a.parent
                if any(a.tag in DROP or a.tag in ('blockquote','ul','ol','table') or re.search(r'related|newsletter|social|advert|share|recommended',a.attrs.get('class',''),re.I) for a in ancestors): continue
                if len(p.text())>2: parts.append(p.render())
            if parts: ranked.append((int(exact)*100000+len(''.join(parts)), ''.join(parts)))
        body=max(ranked,default=(0,''))[1]
    body=sanitise(body,url)
    text=Document(body).root.text()
    if len(text)<180: raise ValueError('Too little article text found; extraction rejected and logged.')
    section=clean(ld.get('articleSection') or doc.meta('article:section') or 'News')
    stream='opinion' if re.search(r'/opinion/|/views/|/analysis/|opinion|analysis',url+' '+section,re.I) else 'reporting'
    published=date(ld.get('datePublished') or doc.meta('article:published_time') or doc.meta('pubdate'))
    modified=date(ld.get('dateModified') or doc.meta('article:modified_time'))
    if not published:
        for n in doc.root.walk():
            if n.attrs.get('itemprop')=='datePublished' or n.tag=='time':
                published=date(n.attrs.get('datetime') or n.attrs.get('content') or n.text())
                if published:break
    if not published:
        # Drupal's current article header uses a plain span, not a time element.
        scopes=[n for n in doc.root.walk() if 'node-content' in n.attrs.get('class','').split()]
        if not scopes:scopes=doc.nodes('article')
        for n in scopes:
            for child in n.walk():
                if child.tag=='span' and re.fullmatch(r'\d{1,2} [A-Za-z]+ \d{4}',child.text()):
                    published=date(child.text())
                    if published:break
            if published:break
    if not published:
        # Some current Daily Star pages omit standard publication metadata but
        # expose the exact Unix timestamp in Drupal's analytics settings.
        for data in embedded:
            for obj in objects(data):
                stamp=obj.get('created') if obj.get('NodeType') or obj.get('NodeID') else None
                if isinstance(stamp,str) and re.fullmatch(r'\d{9,12}',stamp):
                    published=datetime.fromtimestamp(int(stamp),timezone.utc).astimezone(timezone(timedelta(hours=6))).isoformat()
                    break
            if published:break
    if section=='News':
        for token,label in (('/education/','Education'),('/politics/','Politics'),('/crime-justice/','Rights & Justice'),('/environment/','Environment'),('/health/','Health'),('/business/','Economy'),('/opinion/','Opinion'),('/sports/','Sports')):
            if token in urlsplit(url).path:section=label;break
    image=ld.get('image') or doc.meta('og:image') or ''
    if isinstance(image,list): image=image[0] if image else ''
    if isinstance(image,dict): image=image.get('url','')
    publisher=ld.get('publisher',{})
    publisher=publisher.get('name','') if isinstance(publisher,dict) else str(publisher)
    return {'id':identity(url),'title':title,'excerpt':clean(ld.get('description') or doc.meta('og:description') or doc.meta('description')),'source_url':canonical(url),'source_name':publisher or ('The Daily Star' if urlsplit(url).hostname in ('www.thedailystar.net','thedailystar.net') else urlsplit(url).hostname),'original_authors':authors,'verified_author':verified,'author_listing_verified':author_listing,'stream':stream,'category':section,'date_published':published,'date_modified':modified,'body_html':body,'source_image':'','cover_image':'','word_count':len(text.split()),'fetched_at':now()}
