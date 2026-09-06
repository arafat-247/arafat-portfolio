"""Import existing V13/V14 content once, without overwriting V15 records."""
from core import *
def main():
    if not (CONTENT/'settings.json').exists():
        c=read(SITE/'data/site_config.json',{})
        c.update(title='Journalist',description='Journalist at The Daily Star, reporting on education, governance, rights, social policy and public accountability.',portrait='assets/identity/asset0.webp',home_images=['assets/identity/asset1.webp','assets/identity/asset2.webp','assets/identity/asset2.webp','assets/identity/asset3.webp'])
        write(CONTENT/'settings.json',c)
    if not (CONTENT/'photos.json').exists():
        photos=read(SITE/'data/photography.json',{'photos':[]})
        for i,p in enumerate(photos['photos']): p.setdefault('id','legacy-'+str(i)); p.setdefault('status','published')
        write(CONTENT/'photos.json',photos)
    state=read(CONTENT/'sync-state.json',{'sources':{},'archive_cursor':3})
    for a in read(SITE/'data/articles.json',{'articles':[]})['articles']:
        u=canonical(a.get('url',''))
        if not u: continue
        state['sources'].setdefault(u,{'discovered_at':now()})
        target=CONTENT/'articles'/f'{identity(u)}.json'
        if a.get('body_html') and a.get('verified_author') and not target.exists():
            a.update(id=identity(u),source_url=u,original_authors=a.get('authors',[NAME]),source_name='The Daily Star',stream='opinion' if 'Opinion' in a.get('story_type','') else 'reporting',category=a.get('topic') or a.get('section','News'),status='published',first_archived_at=a.get('scraped_at',now()))
            write(target,a)
    # Recover a successfully saved record even if a previous run was interrupted
    # before it could write its final sync summary.
    for target in (CONTENT/'articles').glob('*.json'):
        a=read(target,{})
        if a.get('source_url'):
            entry=state['sources'].setdefault(a['source_url'],{'discovered_at':a.get('first_archived_at',now())})
            entry.update(article_id=a['id'],title=a['title'])
    write(CONTENT/'sync-state.json',state)
    posts=read(CONTENT/'posts.json',{'posts':[]})
    known={x['id'] for x in posts['posts']}
    for a in read(SITE/'data/journal-index.json',{'articles':[]})['articles']:
        key=a.get('slug') or slug(a.get('title','story'))
        if key not in known:
            a.update(id=key,stream='thoughts',excerpt=a.get('deck',''),date_published=a.get('date_published') or date(a.get('date','')),local_url='thoughts/'+key+'/')
            posts['posts'].append(a)
    write(CONTENT/'posts.json',posts)
if __name__=='__main__': main()
