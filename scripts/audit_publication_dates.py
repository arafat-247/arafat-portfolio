"""Recheck every archived article's dates against its original publisher page.

Only dates and their provenance change with --apply. Article text is preserved.
An optional HTML cache is a local checkpoint, never the published archive.
"""
import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen

from core import CONTENT, UA, Document, article_dates, now, objects, read, write


def inspect(path, cache):
    item=read(path)
    url=item['source_url']
    cached=cache/(item['id']+'.html')
    try:
        if cached.exists():
            source=cached.read_text(encoding='utf-8')
        else:
            with urlopen(Request(url,headers={'User-Agent':UA,'Accept':'text/html'}),timeout=25) as response:
                if response.headers.get_content_type() not in ('text/html','application/xhtml+xml'):
                    raise ValueError('Publisher did not return HTML')
                source=response.read(5_000_001).decode('utf-8',errors='replace')
            if len(source)>5_000_000: raise ValueError('Publisher page exceeds size limit')
            cached.write_text(source,encoding='utf-8')
        doc=Document(source)
        # Standard metadata is read by article_dates. The labelled article
        # header and node-specific timestamp are authoritative for this repair.
        embedded=[]
        for script in doc.nodes('script'):
            if script.attrs.get('type') not in ('application/json','application/ld+json'): continue
            try: embedded.append(json.loads(script.rawtext()))
            except (ValueError,TypeError): pass
        node_id=url.rstrip('/').rsplit('-',1)[-1]
        identified=any(str(obj.get('NodeID',''))==node_id for data in embedded for obj in objects(data))
        canonical_url=next((n.attrs.get('href','') for n in doc.nodes('link') if n.attrs.get('rel')=='canonical'),'')
        if not identified and canonical_url.rstrip('/')!=url.rstrip('/'):
            raise ValueError('Publisher page identity could not be confirmed')
        candidates=[obj for data in embedded for obj in objects(data) if obj.get('@type') in ('NewsArticle','Article','ReportageNewsArticle','OpinionNewsArticle')]
        ld=next((obj for obj in candidates if obj.get('mainEntityOfPage')==url),candidates[0] if len(candidates)==1 else {})
        published,modified,provenance=article_dates(doc,ld,embedded,url)
        if not published: raise ValueError('No article-specific publication date')
        return {'id':item['id'],'title':item['title'],'source_url':url,'previous_date':item.get('date_published',''),'verified_date':published,'verified_modified':modified,'evidence':provenance,'page_sha256':hashlib.sha256(source.encode()).hexdigest(),'status':'verified'}
    except Exception as exc:
        return {'id':item['id'],'title':item['title'],'source_url':url,'previous_date':item.get('date_published',''),'status':'unresolved','error':str(exc)}


def run(args):
    cache=Path(args.cache);cache.mkdir(parents=True,exist_ok=True)
    paths=sorted((CONTENT/'articles').glob('*.json'))
    results=[]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed(pool.submit(inspect,path,cache) for path in paths):
            result=future.result();results.append(result)
            if len(results)%20==0 or result['status']=='unresolved':
                print(f"Checked {len(results)}/{len(paths)}: {result['status']} {result['title']}",flush=True)
    overrides=read(CONTENT/'overrides.json',{'articles':{}})
    changed=0;override_changes=0
    for row in results:
        if row['status']!='verified': continue
        override=overrides['articles'].get(row['id'],{})
        row['previous_public_date']=override.get('date_published',row['previous_date'])
        row['calendar_date_changed']=row['previous_public_date'][:10]!=row['verified_date'][:10]
        changed+=row['calendar_date_changed']
        if args.apply:
            path=CONTENT/'articles'/(row['id']+'.json');item=read(path)
            item.update(date_published=row['verified_date'],date_modified=row['verified_modified'],date_published_source=row['evidence'],date_verified_at=now())
            # Match store_article's hash so a later refresh does not manufacture
            # a content revision merely because this date-only repair ran.
            item['content_hash']=hashlib.sha256(json.dumps({k:item.get(k) for k in ('title','excerpt','body_html','date_published','date_modified','original_authors','source_image')},sort_keys=True).encode()).hexdigest()
            write(path,item)
            if 'date_published' in override:
                if override['date_published'][:10]!=row['verified_date'][:10]: override_changes+=1
                override['date_published']=row['verified_date']
    if args.apply: write(CONTENT/'overrides.json',overrides)
    report={'checked_at':now(),'total':len(paths),'verified':sum(r['status']=='verified' for r in results),'unresolved':sum(r['status']=='unresolved' for r in results),'calendar_dates_corrected':changed,'conflicting_overrides_corrected':override_changes,'applied':args.apply,'articles':sorted(results,key=lambda r:r['id'])}
    write(Path(args.report),report)
    print(json.dumps({k:v for k,v in report.items() if k!='articles'},indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--cache',required=True)
    parser.add_argument('--report',default=str(CONTENT/'date-audit.json'))
    parser.add_argument('--workers',type=int,default=4)
    run(parser.parse_args())
