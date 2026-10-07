"""Recent-first DS sync and approved manual links. No cache is authoritative."""
import argparse, hashlib, json, re, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, quote
from core import *

def is_due(status,is_fresh=False,retry_failed=False,current=None):
    if status.get('status')=='unsupported': return False
    if retry_failed and status.get('status')=='failed' and not status.get('last_success'): return True
    last=status.get('last_checked','')
    if not last:return True
    age=((current or datetime.now(timezone.utc))-datetime.fromisoformat(last)).total_seconds()
    if status.get('status')=='author_unverified': return age>7*86400
    if status.get('status')=='failed': return age>min(86400,1200*2**min(status.get('failures',0),6))
    return age>((6*3600) if is_fresh else 7*86400)

def article_links(source,base,scoped=False):
    doc=Document(source.decode('utf-8',errors='replace')); result=[]
    scopes=[n for n in doc.nodes('article') if 'article-author' in n.attrs.get('class','').split()] if scoped else [doc.root]
    if scoped and not scopes:
        raise ValueError('Author listing structure changed; discovery paused instead of scanning unrelated site links.')
    for scope in scopes:
        for n in scope.walk():
            if n.tag!='a':continue
            link=canonical(urljoin(base,n.attrs.get('href','')))
            path=urlsplit(link).path.rstrip('/')
            tail=path.rsplit('-',1)[-1]
            if urlsplit(link).hostname=='www.thedailystar.net' and tail.isdigit() and len(tail)>=5:
                if link not in result:result.append(link)
    return result

def mirror_url(url):
    p=urlsplit(url)
    if p.hostname not in ('www.thedailystar.net','thedailystar.net'):return url
    return p._replace(netloc='online92.thedailystar.net').geturl()

def fetch_daily_star(url,limit=5_000_000):
    mirror=mirror_url(url)
    if mirror!=url:
        try:return fetch(mirror,limit)
        except (HTTPError,URLError):
            return fetch(url,limit)
    return fetch(url,limit)

def discover(url):
    data,typ,final=fetch_daily_star(url)
    if typ not in ('text/html','application/xhtml+xml'):
        raise ValueError('Author page is not HTML.')
    try:return article_links(data,final,scoped=True)
    except ValueError:
        # Mirror pages do not always retain the same author-card wrapper.
        if urlsplit(final).hostname=='online92.thedailystar.net':
            return article_links(data,final,scoped=False)
        raise

def fallback_discover():
    """Discover recent work through The Daily Star's alternate public host.

    URLs are canonicalised back to www.thedailystar.net and still require
    article-level author verification before publication.
    """
    seeds=[
        *[
            'https://online92.thedailystar.net/author/arafat-rahaman?page='+str(page)
            for page in range(0,6)
        ],
        'https://online92.thedailystar.net/news/education',
        'https://online92.thedailystar.net/news/crime-justice',
        'https://online92.thedailystar.net/news/bangladesh',
        'https://online92.thedailystar.net/opinion',
    ]
    result=[]; errors=[]
    for seed in seeds:
        try:
            data,typ,final=fetch(seed)
            if typ not in ('text/html','application/xhtml+xml'):continue
            for link in article_links(data,final,scoped=False):
                if link not in result:result.append(link)
        except (HTTPError,URLError,ValueError,OSError) as exc:
            errors.append(str(exc)[:180])
    if not result and errors:
        raise ValueError('Fallback discovery failed: '+'; '.join(errors[:3]))
    return result[:160]

def store_article(item, old=None):
    # Do not replace a complete saved article with a likely paywall/error extract.
    if old and item['word_count'] < old.get('word_count',0)*0.55:
        raise ValueError('New extraction is substantially shorter. Existing archive preserved; review source manually.')
    item['local_url']=(old or {}).get('local_url','')
    item['legacy_urls']=(old or {}).get('legacy_urls',[])
    existing=[read(path,{}) for path in (CONTENT/'articles').glob('*.json') if path.stem!=item['id']]
    normalise_public_urls([*existing,item])
    item['first_archived_at']=(old or {}).get('first_archived_at') or now()
    if not item.get('date_published') and old: item['date_published']=old.get('date_published','')
    if not item.get('source_image') and old: item['source_image']=old.get('source_image','')
    if not item.get('cover_image') and old: item['cover_image']=old.get('cover_image','')
    item['content_hash']=hashlib.sha256(json.dumps({k:item.get(k) for k in ('title','excerpt','body_html','date_published','date_modified','original_authors','source_image')},sort_keys=True).encode()).hexdigest()
    if old and old.get('content_hash')!=item['content_hash']:
        revision=CONTENT/'revisions'/item['id']/(old.get('content_hash') or hashlib.sha256(old.get('body_html','').encode()).hexdigest())
        if not revision.with_suffix('.json').exists(): write(revision.with_suffix('.json'),old)
    write(CONTENT/'articles'/f"{item['id']}.json",item)

def archive_image(item):
    if not item.get('source_image'): return
    data,typ,_=fetch(item['source_image'],8_000_000)
    kinds={'image/jpeg':('.jpg',b'\xff\xd8\xff'),'image/png':('.png',b'\x89PNG\r\n\x1a\n'),'image/webp':('.webp',b'RIFF'),'image/avif':('.avif',None)}
    if typ not in kinds: raise ValueError('Unsupported cover format; no remote image embedded.')
    ext,magic=kinds[typ]
    if magic and not data.startswith(magic): raise ValueError('Image signature mismatch.')
    if typ=='image/avif' and b'ftypavif' not in data[:32] and b'ftypavis' not in data[:32]: raise ValueError('Image signature mismatch.')
    name=hashlib.sha256(data).hexdigest()[:24]+ext
    target=SITE/'assets'/'imported'/name; target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists(): target.write_bytes(data)
    item['cover_image']='assets/imported/'+name

def run(args):
    state=read(CONTENT/'sync-state.json',{'sources':{},'archive_cursor':0})
    state['last_attempt']=now(); sources=state['sources']; errors=[]; fresh=[]
    for status in sources.values():
        if status.get('status')=='failed' and status.get('failures',0)>=3 and 'Too little article text' in status.get('error',''):
            status['status']='unsupported'
    manual=read(CONTENT/'imports.json',{'imports':[]})['imports']
    # Manual links are explicit claims of contribution and republication permission.
    requests_by_url={canonical(x['url']):x for x in manual if x.get('rights_confirmed') and x.get('contribution_confirmed') and x.get('status')!='cancelled'}
    for u in requests_by_url: sources.setdefault(u,{'discovered_at':now()})
    # Records carried over from V15 were originally discovered through the
    # configured author listing, before that provenance flag was stored.
    for u,status in sources.items():
        if u not in requests_by_url and not status.get('fallback_candidate') and status.get('discovered_at') and urlsplit(u).hostname in ('www.thedailystar.net','thedailystar.net'):
            status['author_listing']=True
            if status.get('status')=='author_unverified':
                status.pop('last_checked',None);status['status']='discovered';status['error']=''
    discovery_failed=False
    fallback_ok=False
    try:
        pages=list(range(args.pages)) if args.full else [0]
        # Incremental backfill continues across runs instead of assuming 12 pages is a complete archive.
        if not args.full:
            cursor=max(3,int(state.get('archive_cursor',3)))
            pages+=list(range(cursor,min(cursor+1,args.pages)))
            state['archive_cursor']=3 if cursor+1>=args.pages else cursor+1
        previous=set()
        for page in pages:
            found=discover(AUTHOR if page==0 else AUTHOR+'?page='+str(page))
            if not found:
                state['listing_complete']=True
                state['archive_cursor']=3
                break
            unique=set(found)-previous
            if not unique and args.full:
                errors.append('Author pagination repeated earlier results; discovery stopped. This is not proof of archive completeness.')
                break
            previous.update(found)
            for u in found:
                entry=sources.setdefault(u,{'discovered_at':now()})
                entry['author_listing']=True
                if entry.get('status')=='author_unverified':
                    entry.pop('last_checked',None);entry['status']='discovered';entry['error']=''
                if page<3: fresh.append(u)
            time.sleep(args.delay)
        state['last_discovery_success']=now()
    except (HTTPError,URLError,ValueError,OSError) as exc:
        discovery_failed=True
        errors.append('Discovery: '+str(exc)[:220])

    # The author page can lag behind publication or be blocked. Fallback
    # candidates are recent official Daily Star URLs, never authorship proof.
    try:
        fallback=fallback_discover()
        for u in fallback:
            entry=sources.setdefault(u,{'discovered_at':now()})
            entry['fallback_candidate']=True
            if u not in fresh:fresh.append(u)
        fallback_ok=True
        state['last_fallback_discovery_success']=now()
        state['fallback_candidates']=len(fallback)
    except (HTTPError,URLError,ValueError,OSError) as exc:
        errors.append('Fallback discovery: '+str(exc)[:220])
    def due(u):
        return is_due(sources[u],u in fresh,bool(getattr(args,'retry_failed',False)))
    pending=[u for u in sources if not sources[u].get('last_success') and due(u)]
    recent=[u for u in dict.fromkeys(fresh) if due(u)]
    queue=list(dict.fromkeys([u for u in requests_by_url if due(u)]+recent[:30]+pending+recent+[u for u in sources if due(u)]))
    saved=0
    selected=queue[:args.limit]
    def extract(u):
        status=sources[u];old=read(CONTENT/'articles'/f'{identity(u)}.json');request=requests_by_url.get(u)
        try:
            data,typ,final=fetch_daily_star(u)
            if typ not in ('text/html','application/xhtml+xml'): raise ValueError('URL is not an HTML article.')
            source=data.decode('utf-8',errors='replace')
            item=article(source,u,manual=bool(request),author_listing=bool(status.get('author_listing')))
            if status.get('fallback_candidate') and not request and not item.get('verified_author'):
                raise ValueError('Fallback candidate does not carry Arafat Rahaman byline.')
            item['resolved_source_url']=final
            source_doc=Document(source)
            image=source_doc.meta('og:image') or source_doc.meta('og:image:url') or source_doc.meta('twitter:image') or source_doc.meta('twitter:image:src')
            if image:item['source_image']=urljoin(final,image)
            elif old:item['source_image']=old.get('source_image','')
            if not item.get('date_published'):raise ValueError('Publication date could not be extracted.')
            if request:
                item['manual_import']=True; item['contribution']=request.get('contribution','Reporting contribution')
                item['rights_confirmed']=True
                requested_stream=request.get('stream','reporting')
                item['stream']=requested_stream if requested_stream in ('reporting','opinion','thoughts') else 'reporting'
                item['category']=request.get('category') or item.get('category') or ('Opinion' if item['stream']=='opinion' else 'Reporting contribution')
                requested_credit=request.get('credit_type','contribution')
                item['credit_type_override']=requested_credit if requested_credit in ('author-page','contribution') else 'contribution'
            item['status']='published'
            try:archive_image(item)
            except (HTTPError,URLError,ValueError,OSError):
                if old:item['cover_image']=old.get('cover_image','')
            return item,old,None
        except (HTTPError,URLError,ValueError,OSError) as exc:
            return None,old,str(exc)[:260]
    for u in selected:sources[u]['last_checked']=now()
    workers=max(1,min(int(getattr(args,'workers',3)),4))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_map={pool.submit(extract,u):u for u in selected}
        for future in as_completed(future_map):
            u=future_map[future];status=sources[u]
            try:item,old,error=future.result()
            except Exception as exc:item,old,error=None,None,str(exc)[:260]
            if error:
                rejected_fallback=status.get('fallback_candidate') and 'Author not verified' in error
                status.update(status='author_unverified' if rejected_fallback else 'failed',error=error,failures=status.get('failures',0)+1)
                if not rejected_fallback:errors.append(error)
            else:
                store_article(item,old);status.update(status='saved',last_success=now(),failures=0,error='',article_id=item['id'],title=item['title']);saved+=1
            write(CONTENT/'sync-state.json',state)
    state.update(last_completed=now(),saved_this_run=saved,known_sources=len(sources),pending=sum(not x.get('last_success') and x.get('status') not in ('author_unverified','unsupported') for x in sources.values()),unsupported=sum(x.get('status')=='unsupported' for x in sources.values()),errors=errors[:30])
    state['degraded_discovery']=discovery_failed
    state['refresh_ok']=(not discovery_failed) or fallback_ok
    write(CONTENT/'sync-state.json',state)
    print(f'Saved {saved}; known URLs {len(sources)}; pending {state["pending"]}. Existing articles were not removed.')
    if errors: print('Warnings:', '\n'.join(errors[:5]))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--full',action='store_true'); p.add_argument('--retry-failed',action='store_true'); p.add_argument('--pages',type=int,default=180); p.add_argument('--limit',type=int,default=60); p.add_argument('--delay',type=float,default=.35);p.add_argument('--workers',type=int,default=4)
    run(p.parse_args())
