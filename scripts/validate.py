"""Release checks: local routes, unsafe HTML, draft exclusion and durable data."""
import json, sys
from pathlib import Path
from urllib.parse import urlsplit, unquote
from core import *
def validate():
    errors=[]; pages=list(OUT.rglob('*.html'))
    for path in pages:
        doc=Document(path.read_text(encoding='utf-8'))
        for n in doc.root.walk():
            if any(k.startswith('on') for k in n.attrs):errors.append(f'Inline handler in {path}')
            for key in ('src','href'):
                u=n.attrs.get(key,''); p=urlsplit(u)
                if p.scheme in ('javascript','data'):errors.append(f'Unsafe URL in {path}')
                if not u or p.scheme or p.netloc or u.startswith('#'):continue
                target=(path.parent/unquote(p.path)).resolve()
                if not target.is_relative_to(OUT.resolve()):errors.append(f'Escaping link {u}')
                if not target.exists():errors.append(f'Missing local asset/page: {path.relative_to(OUT)} -> {u}')
                elif target.is_dir() and not (target/'index.html').exists():errors.append(f'Missing directory index: {u}')
    index=read(OUT/'data/index.json',{'articles':[]})['articles']
    ids=[a['id'] for a in index]
    if len(ids)!=len(set(ids)):errors.append('Duplicate article IDs')
    for a in read(CONTENT/'posts.json',{'posts':[]})['posts']:
        if a.get('status')!='published' and a['id'] in ids:errors.append('Draft appeared in public index')
    for hidden in ('content','sync-state.json','imports.json','posts.json'):
        if (OUT/hidden).exists():errors.append('Private/source content leaked into output')
    if errors:raise SystemExit('\n'.join(errors[:30]))
    print(f'PASS: {len(pages)} HTML pages; local links; safe attributes; {len(ids)} public records; draft exclusion.')
if __name__=='__main__':validate()
