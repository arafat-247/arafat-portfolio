#!/usr/bin/env python3
import argparse, io, json, os, re, sys, unicodedata, urllib.request, uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
POSTS=ROOT/"content/posts.json"
UPLOADS=ROOT/"site/assets/uploads"
LABELS={
"Publishing action":"action","Headline":"title","Deck / short description":"excerpt",
"Section":"section","Category":"category","Publication date":"date",
"Article text":"body","Cover image":"cover","Image description":"cover_alt","Image credit":"cover_credit"}
STREAMS={"Thoughts":"thoughts","Opinion & Analysis":"opinion","Reporting":"reporting"}

def parse(body):
    names="|".join(re.escape(x) for x in LABELS)
    pat=re.compile(rf"(?m)^###\s+({names})\s*$")
    hits=list(pat.finditer(body or "")); out={}
    for i,m in enumerate(hits):
        end=hits[i+1].start() if i+1<len(hits) else len(body)
        v=re.sub(r"<!--.*?-->","",body[m.end():end],flags=re.S).strip()
        out[LABELS[m.group(1)]]="" if v in {"_No response_","No response"} else v
    return out

def slug(s):
    s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()
    s=re.sub(r"[^a-z0-9]+","-",s).strip("-")
    return (s[:75].rsplit("-",1)[0] if len(s)>75 else s) or "story"

def pubdate(s):
    if s:
        d=datetime.strptime(s.strip(),"%Y-%m-%d").date()
    else:
        d=datetime.now(ZoneInfo("Asia/Dhaka")).date()
    return d.isoformat()+"T00:00:00+06:00"

def image_url(v):
    if not v.strip(): return ""
    m=re.search(r"https://[^\s)>\]]+",v)
    if not m: raise ValueError("Cover image has no usable HTTPS link.")
    u=m.group(0).rstrip(".,"); p=urlsplit(u); h=(p.hostname or "").lower()
    ok=(h=="github.com" and p.path.startswith("/user-attachments/")) or h.endswith("githubusercontent.com")
    if p.scheme!="https" or not ok: raise ValueError("Use an image uploaded into the GitHub issue.")
    return u

def save_image(url,post_id):
    req=urllib.request.Request(url,headers={"User-Agent":"ArafatPortfolioPublisher/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        data=r.read(20*1024*1024+1)
    if len(data)>20*1024*1024: raise ValueError("Cover image is larger than 20 MB.")
    Image.MAX_IMAGE_PIXELS=80_000_000
    with Image.open(io.BytesIO(data)) as src:
        src.load(); im=ImageOps.exif_transpose(src)
        if im.width*im.height>80_000_000: raise ValueError("Cover image dimensions are too large.")
        if max(im.size)>1800: im.thumbnail((1800,1800),Image.Resampling.LANCZOS)
        im=im.convert("RGBA" if im.mode in {"RGBA","LA"} else "RGB")
        UPLOADS.mkdir(parents=True,exist_ok=True)
        path=UPLOADS/f"{post_id}.webp"; im.save(path,"WEBP",quality=86,method=6)
    return f"assets/uploads/{post_id}.webp"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--event",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args(); event=json.loads(Path(a.event).read_text())
    if event["issue"]["user"]["login"]!=os.environ.get("GITHUB_REPOSITORY_OWNER"):
        raise PermissionError("Only the repository owner may use quick publish.")
    f=parse(event["issue"].get("body") or "")
    for key in ("title","excerpt","section","category","body"):
        if not f.get(key,"").strip(): raise ValueError(f"Missing required field: {key}")
    action=f.get("action","Publish now").strip()
    status="published" if action=="Publish now" else "draft"
    stream=STREAMS.get(f["section"].strip())
    if not stream: raise ValueError("Invalid section.")
    data=json.loads(POSTS.read_text()); posts=data.setdefault("posts",[])
    issue_no=int(event["issue"]["number"])
    old=next((p for p in posts if p.get("publisher_issue")==issue_no),None)
    pid=(old or {}).get("id") or str(uuid.uuid4())
    published=pubdate(f.get("date",""))
    prefix="thoughts" if stream=="thoughts" else "stories"
    local=(old or {}).get("local_url")
    if not local:
        base=f"{prefix}/{slug(f['title'])}/"; used={p.get("local_url") for p in posts}
        local=base if base not in used else f"{prefix}/{slug(f['title'])}-{published[:4]}/"
    now=datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")
    item={**(old or {}),"source_url":"","source_name":"","original_authors":["Arafat Rahaman"],
      "contribution":"","rights_confirmed":False,"title":f["title"].strip(),"stream":stream,
      "category":f["category"].strip(),"date_published":published,"excerpt":f["excerpt"].strip(),
      "format":"text","body":f["body"].strip(),"cover_alt":f.get("cover_alt","").strip(),
      "cover_credit":f.get("cover_credit","").strip(),"id":pid,"status":status,"updated_at":now,
      "local_url":local,"manual_import":False,"verified_author":True,
      "first_archived_at":(old or {}).get("first_archived_at") or now,"publisher_issue":issue_no}
    u=image_url(f.get("cover",""))
    if u: item["cover_image"]=save_image(u,pid)
    data["posts"]=[item if p.get("id")==pid else p for p in posts] if old else [item,*posts]
    POSTS.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    with open(a.output,"a") as o:
        o.write(f"status={status}\nlocal_url={local}\n")
if __name__=="__main__":
    try: main()
    except Exception as e:
        print(f"Quick publish failed: {e}",file=sys.stderr); raise
