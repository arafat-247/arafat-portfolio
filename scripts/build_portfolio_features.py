"""Build All Work search data, curated collections and the About career timeline."""
from __future__ import annotations
import html,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"
CONTENT=ROOT/"content"
SITE="https://arafatrahaman.com"

BEATS=[
 {"slug":"education","title":"Education","description":"Schools, teachers, curriculum, examinations and higher education.","terms":["education","school","teacher","student","university","college","curriculum","textbook","nctb","exam","ssc","hsc","ugc","admission"]},
 {"slug":"governance-public-institutions","title":"Governance & public institutions","description":"Public administration, recruitment, accountability and institutional decision-making.","terms":["government","ministry","administration","public service","recruitment","bcs","psc","cabinet","corruption","governance","authority","commission","policy"]},
 {"slug":"rights-social-justice","title":"Rights & social justice","description":"Rights, gender, labour, children, minorities and access to justice.","terms":["rights","woman","women","gender","worker","labour","child","children","minority","justice","violence","abuse","discrimination","freedom"]},
 {"slug":"politics-civic-life","title":"Politics & civic life","description":"Parties, elections, parliament, protests and civic movements.","terms":["election","vote","voter","parliament","political","politics","party","bnp","jamaat","ncp","protest","movement","uprising"]},
 {"slug":"media-journalism","title":"Media & journalism","description":"Newsrooms, press freedom, media ethics and journalism practice.","terms":["journalist","journalism","newsroom","media","press freedom","newspaper","cyber","misinformation","reporter"]},
]
SERIES=[
 {"slug":"teacher-shortages-recruitment","title":"Teacher shortages & recruitment","description":"Staffing gaps, appointments and what shortages mean inside classrooms.","terms":["teacher shortage","teacher recruitment","vacant","vacancy","assistant teacher","headteacher","head teacher"]},
 {"slug":"universities-campus-governance","title":"Universities & campus governance","description":"Leadership, admissions, campus politics and public-university governance.","terms":["vice-chancellor","vice chancellor","university","ugc","campus","admission"]},
 {"slug":"curriculum-textbooks-assessment","title":"Curriculum, textbooks & assessment","description":"NCTB, textbooks, curriculum reform and examination changes.","terms":["nctb","textbook","curriculum","assessment","ssc","hsc","examination"]},
 {"slug":"public-recruitment-administration","title":"Public recruitment & administration","description":"BCS, viva voce, recruitment rules and public administration.","terms":["bcs","viva","public recruitment","government recruitment","public administration","psc","public service"]},
]

def esc(v): return html.escape(str(v or ""),quote=True)
def text(item): return " ".join(str(item.get(k,"")) for k in ("title","excerpt","category")).casefold()
def score(item,d): return sum((2 if " " in term else 1) for term in d["terms"] if term in text(item))

def enrich(items):
    out=[]
    for item in items:
        row=dict(item)
        ranked=sorted(((score(item,d),i,d) for i,d in enumerate(BEATS)),key=lambda x:(-x[0],x[1]))
        if ranked and ranked[0][0]>0:
            row["beat"],row["beat_title"]=ranked[0][2]["slug"],ranked[0][2]["title"]
        else:
            row["beat"],row["beat_title"]="other","Other"
        row["series"]=[d["slug"] for d in SERIES if score(item,d)>0]
        out.append(row)
    return out

def replace_main(source,body):
    return re.sub(r'<main id="main">.*?</main>',f'<main id="main">{body}</main>',source,count=1,flags=re.S)

def meta(source,title,description,canonical):
    source=re.sub(r'<title>.*?</title>',f'<title>{esc(title)} — Arafat Rahaman</title>',source,count=1,flags=re.S)
    source=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{esc(description)}">',source,count=1)
    source=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{canonical}">',source,count=1)
    return source

def deepen(source):
    source=re.sub(r'(?P<a>\b(?:href|src)=["\'])\.\./',lambda m:m.group("a")+"../../",source)
    return source.replace('data-root="../"','data-root="../../"')

def card(item,prefix):
    image=""
    cover=str(item.get("cover_image") or "")
    if cover.startswith("assets/"):
        image=f'<figure><img src="{prefix}{esc(cover)}" alt="" loading="lazy" decoding="async"></figure>'
    badge="Non-byline" if item.get("credit_type")=="contribution" else item.get("stream","").title()
    return f'<article class="featurecard">{image}<div><div class="featuremeta"><span>{esc(str(item.get("date_published") or "")[:10])}</span><b>{esc(badge)}</b><span>{esc(item.get("beat_title"))}</span></div><h2><a href="{prefix}{esc(item.get("local_url"))}">{esc(item.get("title"))}</a></h2><p>{esc(item.get("excerpt"))}</p></div></article>'

def rows_for(d,items,kind):
    return [x for x in items if x.get("credit_type")=="byline" and (x.get("beat")==d["slug"] if kind=="beat" else d["slug"] in x.get("series",[]))]

def build_all_work(items,template):
    beatopts="".join(f'<option value="{d["slug"]}">{esc(d["title"])}</option>' for d in BEATS)
    latest="".join(card(x,"../") for x in items[:24])
    body=f'''<section class="page featurepage" data-all-work><header class="featurehero"><div><span class="eyebrow">Portfolio archive</span><h1>All work</h1><p>Search the full archive by keyword, format, beat, year and byline status.</p><div class="featurelinks"><a href="../case-studies/">Reporting case studies →</a><a href="../collections/">Beat collections & story series →</a></div></div><div class="archive-total"><strong>{len(items)}</strong><span>published pieces</span></div></header><form class="featuretools" id="all-work-tools"><label>Search<input name="q" type="search" placeholder="Search headline, topic or keyword"></label><label>Format<select name="stream"><option value="">All formats</option><option value="reporting">Reporting</option><option value="opinion">Opinion</option><option value="thoughts">Thoughts</option></select></label><label>Beat<select name="beat"><option value="">All beats</option>{beatopts}<option value="other">Other</option></select></label><label>Year<select name="year"><option value="">All years</option></select></label><label>Credit<select name="credit"><option value="">All credits</option><option value="byline">Bylined</option><option value="contribution">Non-byline</option></select></label><button type="button" data-all-reset>Reset</button></form><div class="featurecount" data-all-count>{len(items)} results</div><div class="featuregrid" data-all-results>{latest}</div><div class="featuremore"><button type="button" data-all-more>Load more</button></div></section>'''
    page=meta(replace_main(template,body),"All work","Search and browse Arafat Rahaman's reporting, opinion and personal writing.",SITE+"/all-work/")
    return page.replace("</body>",'<script src="../all-work.js?v=21.11.0" defer></script></body>',1)

def build_collections(items,template):
    sections=[]
    for kind,label,defs in (("beat","Beat",BEATS),("series","Series",SERIES)):
        cards=[]
        for d in defs:
            count=len(rows_for(d,items,kind))
            cards.append(f'<a class="collectioncard" href="{d["slug"]}/"><span>{label}</span><h3>{esc(d["title"])}</h3><p>{esc(d["description"])}</p><small>{count} bylined pieces →</small></a>')
        sections.append(f'<section class="collectionsection"><h2>{"Beats" if kind=="beat" else "Story series"}</h2><div class="collectioncards">{"".join(cards)}</div></section>')
    body=f'''<section class="page featurepage"><header class="featurehero"><div><span class="eyebrow">Curated archive</span><h1>Beat collections & story series</h1><p>Browse the portfolio by subject or follow recurring reporting threads across multiple stories.</p><div class="featurelinks"><a href="../all-work/">Search all work →</a><a href="../case-studies/">Reporting case studies →</a></div></div></header>{"".join(sections)}</section>'''
    page=meta(replace_main(template,body),"Beat collections & story series","Curated beat collections and recurring reporting series.",SITE+"/collections/")
    p=DIST/"collections/index.html";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(page,encoding="utf-8")
    for kind,defs in (("beat",BEATS),("series",SERIES)):
        for d in defs:
            rows=rows_for(d,items,kind)
            cards="".join(card(x,"../../") for x in rows)
            body=f'''<section class="page featurepage"><header class="collectionintro"><a href="../">← Beat collections & story series</a><span class="eyebrow">{"Beat collection" if kind=="beat" else "Story series"}</span><h1>{esc(d["title"])}</h1><p>{esc(d["description"])}</p><div class="featurecount">{len(rows)} bylined pieces</div></header><div class="featuregrid">{cards}</div></section>'''
            detail=meta(replace_main(deepen(template),body),d["title"],d["description"],SITE+f'/collections/{d["slug"]}/')
            p=DIST/"collections"/d["slug"]/"index.html";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(detail,encoding="utf-8")

def build_about(settings):
    p=DIST/"about/index.html"
    if not p.is_file(): return
    source=p.read_text(encoding="utf-8")
    entries=[]
    for c in settings.get("career",[]): entries.append((str(c.get("years","")),"Role",c.get("role",""),c.get("organisation",""),c.get("location","")))
    for r in settings.get("recognition",[]): entries.append((str(r.get("year","")),"Milestone",r.get("title",""),r.get("organisation",""),""))
    def year(row):
        m=re.search(r'\d{4}',row[0]); return int(m.group()) if m else 0
    entries.sort(key=year,reverse=True)
    timeline="".join(f'<li class="timeline-item"><div class="timeline-year">{esc(y)}</div><div class="timeline-copy"><span>{esc(k)}</span><h3>{esc(t)}</h3><p>{esc(o)}{(" · "+esc(l)) if l else ""}</p></div></li>' for y,k,t,o,l in entries)
    edu="".join(f'<li><strong>{esc(x.get("degree"))} · {esc(x.get("subject"))}</strong><span>{esc(x.get("institution"))} · {esc(x.get("year"))}</span></li>' for x in settings.get("education",[]))
    block=f'''<section class="career-timeline" id="career-timeline"><header><div><span class="eyebrow">Career</span><h2>Timeline</h2></div><p>Newsroom roles and selected professional milestones.</p></header><ol>{timeline}</ol></section><section class="education-compact"><div><span class="eyebrow">Education</span><h2>Academic foundation</h2></div><ul>{edu}</ul></section>'''
    source=re.sub(r'<section class="profiledetails">.*?</section>',block,source,count=1,flags=re.S)
    p.write_text(source,encoding="utf-8")

def main():
    idx=DIST/"data/index.json";allp=DIST/"all-work/index.html"
    if not idx.is_file() or not allp.is_file(): raise FileNotFoundError("Build site first.")
    items=enrich(json.loads(idx.read_text(encoding="utf-8")).get("articles",[]))
    items.sort(key=lambda x:str(x.get("date_published") or ""),reverse=True)
    (DIST/"data/portfolio-features.json").write_text(json.dumps({"articles":items,"beats":BEATS,"series":SERIES},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    template=allp.read_text(encoding="utf-8")
    allp.write_text(build_all_work(items,template),encoding="utf-8")
    build_collections(items,template)
    build_about(json.loads((CONTENT/"settings.json").read_text(encoding="utf-8")))
    print(f"Portfolio features built: {len(items)} works, {len(BEATS)} beats, {len(SERIES)} series.")

if __name__=="__main__": main()
