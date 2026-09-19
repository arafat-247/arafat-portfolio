"""Release checks: local routes, unsafe HTML, draft exclusion and durable data."""
import json, sys
from pathlib import Path
from urllib.parse import urlsplit, unquote
from core import *
def validate():
    errors=[]; pages=list(OUT.rglob('*.html')); css_versions=set(); js_versions=set()
    for path in pages:
        source=path.read_text(encoding='utf-8')
        doc=Document(source)
        css_versions.update(re.findall(r'portfolio\\.css\\?v=([0-9.]+)',source,re.I))
        js_versions.update(re.findall(r'portfolio\\.js\\?v=([0-9.]+)',source,re.I))
        for n in doc.root.walk():
            if any(k.startswith('on') for k in n.attrs):errors.append(f'Inline handler in {path}')
            for key in ('src','href'):
                u=n.attrs.get(key,''); p=urlsplit(u)
                if p.scheme in ('javascript','data'):errors.append(f'Unsafe URL in {path}')
                if not u or p.scheme or p.netloc or u.startswith('#'):continue
                link_path=unquote(p.path)
                target=((OUT/link_path.lstrip('/')) if link_path.startswith('/') else (path.parent/link_path)).resolve()
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
    if len(css_versions)>1:errors.append('Mixed portfolio.css cache versions: '+', '.join(sorted(css_versions)))
    if len(js_versions)>1:errors.append('Mixed portfolio.js cache versions: '+', '.join(sorted(js_versions)))
    if css_versions and js_versions and css_versions!=js_versions:errors.append('CSS/JS cache versions differ: css='+','.join(sorted(css_versions))+' js='+','.join(sorted(js_versions)))
    if errors:raise SystemExit('\n'.join(errors[:30]))
    print(f'PASS: {len(pages)} HTML pages; local links; safe attributes; {len(ids)} public records; draft exclusion.')
if __name__=='__main__':validate()
