#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'; CONFIG=SITE/'data'/'site_config.json'
config=json.loads(CONFIG.read_text(encoding='utf-8')); site_url=config.get('site_url','').rstrip('/')
if not site_url.startswith('http'): raise SystemExit('site_url must be an absolute http(s) URL')
for p in SITE.glob('*.html'):
    text=p.read_text(encoding='utf-8').replace('__SITE_URL__',site_url)
    p.write_text(text,encoding='utf-8')
# Legacy V6 pages should not be deployed if they remain in the repository.
for name in ('cv.html','investigations.html','visuals.js'):
    legacy=SITE/name
    if legacy.exists(): legacy.unlink()
for name in ('header-editorial.svg','footer-editorial.svg'):
    legacy=SITE/'assets'/name
    if legacy.exists(): legacy.unlink()
legacy_data=SITE/'data'/'story_visuals.json'
if legacy_data.exists(): legacy_data.unlink()
print('Static pages prepared for',site_url)
