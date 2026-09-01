#!/usr/bin/env python3
"""Optimise future story-cover and photography source images.
Drop JPG/PNG originals into site/assets/story-covers-src or photography-src.
The build creates matching WebP and AVIF files without deleting sources.
"""
from pathlib import Path
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'/'assets'
for src_name,out_name in [('story-covers-src','story-covers'),('photography-src','photography')]:
    src=SITE/src_name; out=SITE/out_name; out.mkdir(parents=True,exist_ok=True)
    if not src.exists(): continue
    for p in src.iterdir():
        if p.suffix.lower() not in {'.jpg','.jpeg','.png','.webp'}: continue
        im=ImageOps.exif_transpose(Image.open(p)).convert('RGB'); im.thumbnail((1800,1800),Image.Resampling.LANCZOS)
        stem=out/p.stem
        im.save(str(stem)+'.webp','WEBP',quality=82,method=6)
        try: im.save(str(stem)+'.avif','AVIF',quality=58)
        except Exception as e: print('AVIF skipped for',p.name,e)
        print('Optimised',p.name)
