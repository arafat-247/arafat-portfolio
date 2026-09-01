#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'
js=list(SITE.glob('*.js')); css=list(SITE.glob('*.css'))
code=sum(p.stat().st_size for p in js+css)
limit=180*1024
if code>limit: raise SystemExit(f'Performance budget exceeded: CSS+JS {code/1024:.1f}KB > {limit/1024:.0f}KB')
large=[]
for p in (SITE/'assets').rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.webp','.avif','.jpg','.jpeg','.png'} and p.stat().st_size>550*1024: large.append((p,p.stat().st_size))
if large: raise SystemExit('Oversized images: '+', '.join(f'{p}:{n/1024:.0f}KB' for p,n in large))
print(f'Performance budget OK: CSS+JS {code/1024:.1f}KB; {len(js)} JS files, {len(css)} CSS files.')
